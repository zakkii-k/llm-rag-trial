"""
mcp_server.py – GraphRAG / Vector RAG MCP サーバー

llm-rag-trial の GraphRAG および Vector RAG を MCP ツールとして公開します。
Ollama ローカル LLM（llama, qwen2.5-coder, qwen3, qwen3.5, gemma2）をバックエンドに使用。

起動方法（プロジェクトルートから）:
  python app/mcp_server.py

Claude Code への登録:
  claude mcp add rag -- python /path/to/llm-rag-trial/app/mcp_server.py
"""

import os
import sys
from pathlib import Path

# プロジェクトルートを sys.path に追加（app.modules.* import のため）
_project_root = Path(__file__).parent.parent
sys.path.insert(0, str(_project_root))
os.chdir(_project_root)  # data/ や chromadb/ への相対パス解決

from dotenv import load_dotenv
load_dotenv()

from mcp.server.fastmcp import FastMCP

from app.modules.graphrag_engine import run_graphrag
from app.modules.rag_engine import run_rag, build_vector_store
from app.modules.models import MODEL_CONFIG

mcp = FastMCP("llm-rag-trial")

# ベクターストアキャッシュ（data_dir ごとに保持）
_vector_store_cache: dict[str, object] = {}

LOCAL_MODELS = [k for k in MODEL_CONFIG if not k.startswith("gemini")]


# ── ツール ────────────────────────────────────────────────────────────

@mcp.tool()
def graphrag_query(question: str, model: str = "qwen-small") -> str:
    """
    ナレッジグラフに対して GraphRAG クエリを実行します。
    ローカル LLM が Cypher クエリを生成し Neo4j で実行して回答します。

    Args:
        question: 自然言語の質問
        model:    モデルキー（small/qwen-small/qwen-large/qwen3-small/qwen3-medium/large など）
                  GraphRAG には qwen-small（Qwen 2.5 Coder 7B）推奨
    """
    if model not in MODEL_CONFIG:
        return f"不明なモデル '{model}'。利用可能: {', '.join(LOCAL_MODELS)}"

    model_name = MODEL_CONFIG[model]["name"]
    result = run_graphrag(question, model_name)

    parts = [
        f"## 回答\n{result.answer}",
        f"## 生成された Cypher クエリ\n```cypher\n{result.cipher_query}\n```",
    ]
    if result.cipher_result:
        parts.append(f"## クエリ結果（生データ）\n{result.cipher_result}")
    parts.append(
        f"試行: {result.total_attempts} 回 / "
        f"経過: {result.elapsed_sec:.1f}s / "
        f"トークン: {result.prompt_tokens + result.completion_tokens}"
    )
    return "\n\n".join(parts)


@mcp.tool()
def vector_rag_query(
    question: str,
    model: str = "qwen3-small",
    data_dir: str = "data/small",
    n_results: int = 5,
) -> str:
    """
    ベクター類似検索（ChromaDB + nomic-embed-text）で RAG クエリを実行します。

    Args:
        question:  自然言語の質問
        model:     モデルキー（small/qwen3-small/qwen3-medium/large など）
        data_dir:  CSV データディレクトリ（data/small, data/medium, data/large）
        n_results: 取得ドキュメント数（デフォルト: 5）
    """
    if model not in MODEL_CONFIG:
        return f"不明なモデル '{model}'。利用可能: {', '.join(LOCAL_MODELS)}"

    if data_dir not in _vector_store_cache:
        _vector_store_cache[data_dir] = build_vector_store(data_dir)
    collection = _vector_store_cache[data_dir]

    model_name = MODEL_CONFIG[model]["name"]
    result = run_rag(question, model_name, collection, n_results=n_results)

    parts = [
        f"## 回答\n{result.answer}",
        f"取得ドキュメント数: {len(result.retrieved_docs)} / "
        f"経過: {result.elapsed_sec:.1f}s / "
        f"トークン: {result.prompt_tokens + result.completion_tokens}",
    ]
    return "\n\n".join(parts)


@mcp.tool()
def list_models() -> str:
    """利用可能なローカル LLM モデルの一覧を返します。"""
    lines = ["## 利用可能モデル\n", "| キー | モデル名 | 説明 |", "|---|---|---|"]
    for key, cfg in MODEL_CONFIG.items():
        if not key.startswith("gemini"):
            lines.append(f"| `{key}` | {cfg['name']} | {cfg['description']} |")
    return "\n".join(lines)


@mcp.tool()
def get_schema() -> str:
    """ナレッジグラフのスキーマ（ノード・リレーション定義）を返します。"""
    return """\
## ナレッジグラフ スキーマ

### ノード
| ラベル | 主な属性 |
|---|---|
| Bug | id, title, severity(critical/high/medium/low), status(open/in_progress/resolved) |
| Engineer | id, name, email |
| Team | id, name |
| Department | id, name |
| Project | id, name, status(active/completed) |
| Module | id, name |
| Release | id, version, status(released/in_progress/planned) |

### リレーションシップ
| パターン | 意味 |
|---|---|
| (Bug)-[:ASSIGNED_TO]->(Engineer) | バグの担当者 |
| (Engineer)-[:MEMBER_OF]->(Team) | エンジニアの所属チーム |
| (Team)-[:BELONGS_TO]->(Department) | チームの所属部門 |
| (Bug)-[:FOUND_IN]->(Module) | バグが発見されたモジュール |
| (Module)-[:PART_OF]->(Project) | モジュールが属するプロジェクト |
| (Bug)-[:BLOCKS]->(Release) | バグが阻害するリリース |
| (Release)-[:BELONGS_TO]->(Project) | リリースが属するプロジェクト |"""


if __name__ == "__main__":
    mcp.run()
