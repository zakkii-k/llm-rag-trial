"""
graphrag_engine.py — Neo4j + LangChain を使ったGraphRAGエンジン

回答、生成Cypherクエリ、Cypher結果、トークン数、経過時間を返す。
"""

import os
import time
from dataclasses import dataclass

import requests
from langchain_core.prompts import PromptTemplate
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_ollama import OllamaLLM


# ──────────────────────────────────────────────────────────────────────────────
# Cypherクエリ生成プロンプト
# スキーマ（ノードラベル・プロパティ・リレーション方向）を明示的に注入し、
# 小さなモデルでも正しいCypherを生成できるよう制約を与える。
# ──────────────────────────────────────────────────────────────────────────────
_CYPHER_GENERATION_TEMPLATE = """あなたはNeo4j Cypherクエリの専門家です。
以下のスキーマ定義に従って、質問に答えるCypherクエリを生成してください。

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
1. 上記以外のノードラベル（Person, User, Issue 等）は存在しない。絶対に使わないこと。
2. 上記以外のリレーション型（CREATED_BY, IS_related_to 等）は存在しない。絶対に使わないこと。
3. 名前での検索は CONTAINS または完全一致（=）を使うこと。
4. Cypherクエリのみを出力すること。説明文や```は不要。

## 質問
{question}

## Cypherクエリ
"""


@dataclass
class GraphRAGResult:
    answer: str
    cypher_query: str
    cypher_result: str
    elapsed_sec: float
    prompt_tokens: int
    completion_tokens: int


def run_graphrag(prompt: str, model_name: str) -> GraphRAGResult:
    """
    GraphRAGで質問に回答する。

    Parameters
    ----------
    prompt      : 自然言語の質問
    model_name  : Ollamaのモデル名（例: "llama3.2", "llama3.1:8b"）
    """
    neo4j_uri      = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
    neo4j_user     = os.getenv("NEO4J_USER",     "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    ollama_url     = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    assert neo4j_password, "NEO4J_PASSWORD 環境変数を設定してください"

    graph = Neo4jGraph(
        url=neo4j_uri,
        username=neo4j_user,
        password=neo4j_password,
        refresh_schema=False,  # APOC不要にする
    )
    # APOC なしで動作するよう、スキーマを手動設定
    graph.schema = _build_schema(neo4j_uri, neo4j_user, neo4j_password)

    llm = OllamaLLM(model=model_name, base_url=ollama_url)

    cypher_prompt = PromptTemplate(
        input_variables=["schema", "question"],
        template=_CYPHER_GENERATION_TEMPLATE,
    )

    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=False,
        return_intermediate_steps=True,
        allow_dangerous_requests=True,
        cypher_prompt=cypher_prompt,
    )

    start = time.perf_counter()
    result = chain.invoke({"query": prompt})
    elapsed = time.perf_counter() - start

    answer       = result.get("result", "")
    steps        = result.get("intermediate_steps", [])
    cypher_query = steps[0].get("query", "") if steps else ""
    cypher_result = str(steps[1].get("context", "")) if len(steps) > 1 else ""

    # Ollama の /api/generate エンドポイントからトークン数を取得
    prompt_tokens, completion_tokens = _get_token_counts(
        ollama_url, model_name, prompt, answer
    )

    return GraphRAGResult(
        answer=answer,
        cypher_query=cypher_query,
        cypher_result=cypher_result,
        elapsed_sec=elapsed,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )


def _build_schema(uri: str, user: str, password: str) -> str:
    """
    APOC を使わず db.schema.visualization() + db.labels() などで
    ノード/リレーションスキーマを文字列に変換する。
    取得できない場合はハードコードされたスキーマを返す。
    """
    from neo4j import GraphDatabase
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            # ノードプロパティを取得
            node_props = {}
            result = session.run("""
                CALL db.schema.nodeTypeProperties()
                YIELD nodeType, propertyName, propertyTypes
                RETURN nodeType, propertyName, propertyTypes
            """)
            for rec in result:
                label = rec["nodeType"].strip(":`")
                prop = rec["propertyName"]
                if label not in node_props:
                    node_props[label] = []
                node_props[label].append(prop)

            # リレーションを取得
            rels = []
            result = session.run("""
                MATCH (a)-[r]->(b)
                RETURN DISTINCT labels(a)[0] AS from, type(r) AS rel, labels(b)[0] AS to
                LIMIT 50
            """)
            for rec in result:
                rels.append(f"(:{rec['from']})-[:{rec['rel']}]->(:{rec['to']})")

        driver.close()

        lines = ["Node properties are the following:"]
        for label, props in node_props.items():
            lines.append(f"{label} {{{', '.join(props)}}}")
        lines.append("Relationship properties are the following:")
        lines.append("The relationships are the following:")
        lines.extend(rels)
        return "\n".join(lines)

    except Exception:
        # フォールバック: ハードコードされたスキーマ
        return """
Node properties are the following:
Engineer {id: STRING, name: STRING, email: STRING}
Bug {id: STRING, title: STRING, severity: STRING, status: STRING}
Team {id: STRING, name: STRING}
Department {id: STRING, name: STRING}
Project {id: STRING, name: STRING, status: STRING}
Module {id: STRING, name: STRING}
Release {id: STRING, version: STRING, status: STRING}
Relationship properties are the following:
The relationships are the following:
(:Engineer)-[:MEMBER_OF]->(:Team)
(:Team)-[:BELONGS_TO]->(:Department)
(:Bug)-[:ASSIGNED_TO]->(:Engineer)
(:Bug)-[:FOUND_IN]->(:Module)
(:Module)-[:PART_OF]->(:Project)
(:Bug)-[:BLOCKS]->(:Release)
(:Release)-[:BELONGS_TO]->(:Project)
""".strip()


def _get_token_counts(base_url: str, model: str, prompt: str, response: str):
    """
    Ollama の /api/generate を使い、トークン数メタデータを取得する。
    LangChain 経由ではメタデータが取得しにくいため、
    ダミー生成（num_predict=1）でプロンプトトークン数のみ取得し、
    出力トークン数は文字数から概算する。
    """
    try:
        resp = requests.post(
            f"{base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 1},
            },
            timeout=60,
        )
        data = resp.json()
        prompt_tokens     = data.get("prompt_eval_count", 0)
        completion_tokens = data.get("eval_count", 0)
        return prompt_tokens, completion_tokens
    except Exception:
        # 取得失敗時は文字数から概算（日本語は1文字≈1.5トークン）
        return _estimate_tokens(prompt), _estimate_tokens(response)


def _estimate_tokens(text: str) -> int:
    return max(1, int(len(text) * 0.6))
