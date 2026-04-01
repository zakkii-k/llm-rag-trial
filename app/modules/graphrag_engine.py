"""
graphrag_engine.py — Neo4j + LangChain を使ったGraphRAGエンジン

回答、生成Cypherクエリ、Cypher結果、トークン数、経過時間を返す。
"""

import os
import time
from dataclasses import dataclass

import requests
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_ollama import OllamaLLM


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
    )

    llm = OllamaLLM(model=model_name, base_url=ollama_url)

    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=False,
        return_intermediate_steps=True,
        allow_dangerous_requests=True,
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
