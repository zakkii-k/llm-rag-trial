"""
graphrag_engine.py — Neo4j + LLM を使ったGraphRAGエンジン

精度向上のための改善:
- Few-shot例をCypher生成プロンプトに追加
- Cypherバリデーション（実行前の静的チェック）
- エラー時は最大3回リトライ（エラー内容をLLMにフィードバック）
- リトライ履歴を GraphRAGResult.attempts に記録
- Ollama / Gemini API を LLMClient で統一
"""

import os
import re
import time
from dataclasses import dataclass, field

from langchain_core.prompts import PromptTemplate
from langchain_neo4j import Neo4jGraph

from app.modules.env_utils import get_neo4j_uri
from app.modules.llm_client import LLMClient


# ──────────────────────────────────────────────────────────────────────────────
# Cypherクエリ生成プロンプト（Few-Shot例付き）
# ──────────────────────────────────────────────────────────────────────────────
_CYPHER_GENERATION_TEMPLATE = """\
あなたはNeo4j Cypherクエリの専門家です。
以下のスキーマ定義と例に従って、質問に答えるCypherクエリを生成してください。

## グラフスキーマ（オントロジー）

### ノードラベルとプロパティ
- Bug       : id(STRING), title(STRING), severity(STRING: critical/high/medium/low), status(STRING: open/in_progress/resolved)
- Engineer  : id(STRING), name(STRING), email(STRING)
- Team      : id(STRING), name(STRING)
- Department: id(STRING), name(STRING)
- Project   : id(STRING), name(STRING), status(STRING: active/completed)
- Module    : id(STRING), name(STRING)
- Release   : id(STRING), version(STRING), status(STRING: released/in_progress/planned)

### リレーション（方向に注意）
- (:Bug)-[:ASSIGNED_TO]->(:Engineer)      バグの担当者
- (:Engineer)-[:MEMBER_OF]->(:Team)       エンジニアが所属するチーム
- (:Team)-[:BELONGS_TO]->(:Department)    チームが所属する部署
- (:Bug)-[:FOUND_IN]->(:Module)           バグが発見されたモジュール
- (:Module)-[:PART_OF]->(:Project)        モジュールが属するプロジェクト
- (:Bug)-[:BLOCKS]->(:Release)            バグがブロックするリリース
- (:Release)-[:BELONGS_TO]->(:Project)    リリースが属するプロジェクト

### 重要なルール
1. 上記以外のノードラベル（Person, User, Issue 等）は絶対に使わないこと。
2. 上記以外のリレーション型（CREATED_BY, IS_related_to 等）は絶対に使わないこと。
3. 名前での検索は CONTAINS または完全一致（=）を使うこと。
4. GROUP BY は使わない。集計は RETURN d.name, count(b) AS cnt のように書く。
5. EXISTS() はサブクエリ構文 EXISTS {{ MATCH ... }} で使うこと。
6. Cypherクエリのみを出力すること。説明文や``` は不要。

## クエリ例（Few-Shot）

### 例1: 特定部署のエンジニアが担当するオープンバグ
質問: Engineering部署のエンジニアが担当しているオープンなバグを教えてください。
Cypher:
MATCH (b:Bug {{status: 'open'}})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department {{name: 'Engineering'}})
RETURN b.id, b.title, b.severity, e.name

### 例2: 部署ごとの集計（GROUP BYは使わない）
質問: 部署ごとのcriticalバグ件数を教えてください。
Cypher:
MATCH (b:Bug {{severity: 'critical'}})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department)
RETURN d.name AS department, count(b) AS bug_count
ORDER BY bug_count DESC

### 例3: リリースをブロックするバグとその担当者
質問: v1.0リリースをブロックしているバグの担当エンジニアを教えてください。
Cypher:
MATCH (b:Bug)-[:BLOCKS]->(r:Release {{version: 'v1.0'}})-[:BELONGS_TO]->(p:Project)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN b.id, b.title, e.name AS assignee, t.name AS team, p.name AS project

### 例4: モジュール→プロジェクト経由のバグ検索
質問: ECサイトリニューアルプロジェクトのモジュールで発見されたバグを教えてください。
Cypher:
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {{name: 'ECサイトリニューアル'}})
RETURN b.id, b.title, b.severity, b.status, m.name AS module

### 例5: 特定チームのエンジニアが担当するバグ（ASSIGNED_TO方向に注意）
質問: BackendチームのエンジニアがアサインされているバグのIDとタイトルを教えてください。
Cypher:
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {{name: 'Backend'}})
RETURN b.id, b.title, b.severity, e.name AS engineer

## 質問
{question}

## Cypherクエリ
"""

# エラー発生時のCypher修正プロンプト
_CYPHER_CORRECTION_TEMPLATE = """\
あなたはNeo4j Cypherクエリの専門家です。
前回生成したCypherクエリでエラーが発生しました。エラー内容を確認して修正してください。

## リレーション（方向を再確認）
- (:Bug)-[:ASSIGNED_TO]->(:Engineer)       ← BugからEngineerへ
- (:Engineer)-[:MEMBER_OF]->(:Team)        ← EngineerからTeamへ
- (:Team)-[:BELONGS_TO]->(:Department)     ← TeamからDepartmentへ
- (:Bug)-[:FOUND_IN]->(:Module)
- (:Module)-[:PART_OF]->(:Project)
- (:Bug)-[:BLOCKS]->(:Release)
- (:Release)-[:BELONGS_TO]->(:Project)

## 修正ルール
- GROUP BY は使わない → RETURN x, count(y) AS cnt を使う
- SQL構文（EXISTS(), HAVING, JOIN 等）は使わない
- Cypherクエリのみを出力すること（説明文・```は不要）

## 質問
{question}

## 前回のCypherクエリ（エラーあり）
{previous_cypher}

## エラー内容
{error}

## 修正されたCypherクエリ
"""

# Cypher実行結果をもとに回答を生成するプロンプト
_QA_TEMPLATE = """\
あなたはデータベースの検索結果を日本語で説明するアシスタントです。
以下のCypher実行結果を読み取り、質問に対して正確に回答してください。

## 結果の読み方
Cypher実行結果はPythonのリスト形式です。
- 空リスト `[]` → 該当データなし
- それ以外 → 各辞書のキーがプロパティ名、値がその内容

### 読み取り例
結果: `[{{'b.id': 'BUG-001', 'b.title': 'ログイン失敗', 'e.name': '田中太郎'}}]`
→ バグ BUG-001「ログイン失敗」の担当者は田中太郎 と読み取る

結果: `[{{'department': 'Engineering', 'bug_count': 5}}, {{'department': 'QA', 'bug_count': 3}}]`
→ Engineering部署に5件、QA部署に3件 と読み取る

## 重要なルール
- 結果が空リスト `[]` の場合のみ「該当するデータが見つかりませんでした」と答えること
- 結果に値が含まれている場合は、必ずその値を使って回答すること
- 辞書のキー名（例: `b.id`, `e.name`）ではなく、値（例: `BUG-001`, `田中太郎`）を使って答えること
- 複数件ある場合はリスト形式で列挙すること

## 質問
{question}

## Cypher実行結果
{context}

## 回答
"""


@dataclass
class GraphRAGAttempt:
    """1回のCypher生成・実行試行の記録"""
    attempt_num: int
    cypher_query: str
    error: str | None
    cypher_result: str | None


@dataclass
class GraphRAGResult:
    answer: str
    cypher_query: str
    cypher_result: str
    elapsed_sec: float
    prompt_tokens: int
    completion_tokens: int
    attempts: list = field(default_factory=list)  # list[GraphRAGAttempt]
    total_attempts: int = 1


# SQL由来の構文パターン（Neo4j Cypherでは無効）
_SQL_ANTIPATTERNS = [
    (r"\bGROUP\s+BY\b",   "GROUP BY は使えません。RETURN x, count(y) AS cnt を使ってください。"),
    (r"\bHAVING\b",        "HAVING は使えません。WITH句でフィルタしてください。"),
    (r"\bJOIN\b",          "JOIN は使えません。MATCHでリレーションをたどってください。"),
    (r"\bSELECT\b",        "SELECT は使えません。MATCH ... RETURN を使ってください。"),
    (r"\bFROM\s+\w",       "FROM は使えません。MATCH ... RETURN を使ってください。"),
]


def _validate_cypher(cypher: str) -> str | None:
    for pattern, reason in _SQL_ANTIPATTERNS:
        if re.search(pattern, cypher, re.IGNORECASE):
            return f"構文エラー（静的チェック）: {reason} 検出パターン: {pattern}"
    return None


def run_graphrag(
    prompt: str,
    model_name: str,
    max_retries: int = 3,
) -> GraphRAGResult:
    """
    GraphRAGで質問に回答する。

    Parameters
    ----------
    prompt      : 自然言語の質問
    model_name  : モデル名（Ollama: "llama3.2" 等 / Gemini: "gemini-1.5-flash" 等）
    max_retries : 最大試行回数（デフォルト3）
    """
    neo4j_uri      = get_neo4j_uri()
    neo4j_user     = os.getenv("NEO4J_USER",     "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    assert neo4j_password, "NEO4J_PASSWORD 環境変数を設定してください"

    graph = Neo4jGraph(
        url=neo4j_uri,
        username=neo4j_user,
        password=neo4j_password,
        refresh_schema=False,
    )

    llm = LLMClient(model_name)

    cypher_gen_prompt = PromptTemplate(
        input_variables=["question"],
        template=_CYPHER_GENERATION_TEMPLATE,
    )
    cypher_fix_prompt = PromptTemplate(
        input_variables=["question", "previous_cypher", "error"],
        template=_CYPHER_CORRECTION_TEMPLATE,
    )
    qa_prompt = PromptTemplate(
        input_variables=["question", "context"],
        template=_QA_TEMPLATE,
    )

    attempts: list[GraphRAGAttempt] = []
    last_cypher = ""
    last_error = ""
    answer = ""
    final_cypher = ""
    final_result = ""
    prompt_tokens = 0
    completion_tokens = 0

    start = time.perf_counter()

    for attempt_num in range(1, max_retries + 1):
        # ── Cypher生成 ──
        if attempt_num == 1:
            raw_cypher = llm.invoke(cypher_gen_prompt.format(question=prompt))
        else:
            raw_cypher = llm.invoke(cypher_fix_prompt.format(
                question=prompt,
                previous_cypher=last_cypher,
                error=last_error,
            ))

        cypher = _clean_cypher(raw_cypher)

        # ── 静的バリデーション ──
        static_error = _validate_cypher(cypher)
        if static_error:
            attempts.append(GraphRAGAttempt(
                attempt_num=attempt_num,
                cypher_query=cypher,
                error=static_error,
                cypher_result=None,
            ))
            last_cypher = cypher
            last_error = static_error
            continue

        # ── Neo4j実行 ──
        try:
            result = graph.query(cypher)
            result_str = str(result)

            # ── 回答生成（トークン数もここで取得）──
            gen = llm.generate(qa_prompt.format(question=prompt, context=result_str))
            answer = gen.text
            prompt_tokens = gen.prompt_tokens
            completion_tokens = gen.completion_tokens

            attempts.append(GraphRAGAttempt(
                attempt_num=attempt_num,
                cypher_query=cypher,
                error=None,
                cypher_result=result_str,
            ))
            final_cypher = cypher
            final_result = result_str
            break

        except Exception as e:
            error_str = str(e)
            attempts.append(GraphRAGAttempt(
                attempt_num=attempt_num,
                cypher_query=cypher,
                error=error_str,
                cypher_result=None,
            ))
            last_cypher = cypher
            last_error = error_str

    elapsed = time.perf_counter() - start

    if not answer:
        answer = "Cypherクエリの生成・実行に失敗しました。"

    return GraphRAGResult(
        answer=answer,
        cypher_query=final_cypher,
        cypher_result=final_result,
        elapsed_sec=elapsed,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        attempts=attempts,
        total_attempts=len(attempts),
    )


def _clean_cypher(raw: str) -> str:
    block = re.search(r"```(?:cypher)?\s*([\s\S]+?)```", raw, re.IGNORECASE)
    if block:
        return block.group(1).strip()
    match = re.search(r"(MATCH|RETURN|WITH|CALL)\b", raw, re.IGNORECASE)
    if match:
        return raw[match.start():].strip()
    return raw.strip()
