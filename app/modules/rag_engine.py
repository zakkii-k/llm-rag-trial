"""
rag_engine.py — ChromaDB + Ollama Embeddings を使ったベクターRAGエンジン

CSVデータをテキストドキュメントに変換してベクターDBに格納し、
類似度検索で関連コンテキストを取得してLLMに回答させる。

GraphRAGと公平に比較するために:
- 同じOllamaモデルを使用
- 同じデータソース（CSV）から知識を取得
- 埋め込みは nomic-embed-text（Ollama）を使用
"""

import csv
import os
import time
from dataclasses import dataclass
from pathlib import Path

import requests
import chromadb
from chromadb.utils import embedding_functions

from app.modules.env_utils import get_ollama_url


@dataclass
class RAGResult:
    answer: str
    retrieved_docs: list[str]
    elapsed_sec: float
    prompt_tokens: int
    completion_tokens: int


def build_vector_store(data_dir: str, collection_name: str = "kg_docs") -> chromadb.Collection:
    """
    CSVをテキスト化してChromaDBに格納する。
    同じcollection_nameが存在する場合は再利用する。
    """
    ollama_url = get_ollama_url()
    from app.modules.models import EMBEDDING_MODEL

    client = chromadb.Client()

    # 既存コレクションがあれば削除して再作成（データ更新対応）
    existing = [c.name for c in client.list_collections()]
    if collection_name in existing:
        client.delete_collection(collection_name)

    ef = embedding_functions.OllamaEmbeddingFunction(
        url=f"{ollama_url}/api/embeddings",
        model_name=EMBEDDING_MODEL,
    )
    collection = client.create_collection(collection_name, embedding_function=ef)

    docs, ids, metadatas = _csv_to_documents(data_dir)
    if docs:
        # ChromaDB は一度に大量追加するとエラーになる場合があるためバッチ処理
        batch_size = 100
        for i in range(0, len(docs), batch_size):
            collection.add(
                documents=docs[i:i+batch_size],
                ids=ids[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
            )
    return collection


def _csv_to_documents(data_dir: str) -> tuple[list, list, list]:
    """
    CSVの各行を自然言語のテキストドキュメントに変換する。
    GraphRAGと同等の情報量になるよう、リレーション情報も文章に含める。
    """
    # 参照テーブルをメモリに読み込む
    refs = _load_reference_tables(data_dir)

    docs, ids, metas = [], [], []

    def _read(filename):
        path = Path(data_dir) / filename
        if not path.exists():
            return []
        with open(path, encoding="utf-8") as f:
            return list(csv.DictReader(f))

    # Department
    for row in _read("departments.csv"):
        text = f"部署 {row['name']}（ID: {row['id']}）は Engineering 組織の一部です。"
        docs.append(text); ids.append(f"dept_{row['id']}"); metas.append({"type": "Department"})

    # Team
    for row in _read("teams.csv"):
        dept_name = refs["departments"].get(row.get("department_id", ""), row.get("department_id", ""))
        text = f"チーム {row['name']}（ID: {row['id']}）は {dept_name} 部署に所属しています。"
        docs.append(text); ids.append(f"team_{row['id']}"); metas.append({"type": "Team"})

    # Engineer
    for row in _read("engineers.csv"):
        team_name = refs["teams"].get(row.get("team_id", ""), row.get("team_id", ""))
        dept_name = refs["team_dept"].get(row.get("team_id", ""), "")
        text = (
            f"エンジニア {row['name']}（ID: {row['id']}, メール: {row['email']}）は "
            f"{team_name} チームに所属しています。"
        )
        if dept_name:
            text += f" {team_name} チームは {dept_name} 部署の配下です。"
        docs.append(text); ids.append(f"eng_{row['id']}"); metas.append({"type": "Engineer"})

    # Project
    for row in _read("projects.csv"):
        text = f"プロジェクト {row['name']}（ID: {row['id']}）のステータスは {row['status']} です。"
        docs.append(text); ids.append(f"proj_{row['id']}"); metas.append({"type": "Project"})

    # Module
    for row in _read("modules.csv"):
        proj_name = refs["projects"].get(row.get("project_id", ""), row.get("project_id", ""))
        text = f"モジュール {row['name']}（ID: {row['id']}）は {proj_name} プロジェクトの一部です。"
        docs.append(text); ids.append(f"mod_{row['id']}"); metas.append({"type": "Module"})

    # Release
    for row in _read("releases.csv"):
        proj_name = refs["projects"].get(row.get("project_id", ""), row.get("project_id", ""))
        text = (
            f"リリース {row['version']}（ID: {row['id']}）は {proj_name} プロジェクトのリリースで、"
            f"ステータスは {row['status']} です。"
        )
        docs.append(text); ids.append(f"rel_{row['id']}"); metas.append({"type": "Release"})

    # Bug（リレーション情報をフル展開）
    for row in _read("bugs.csv"):
        assignee_name = refs["engineers"].get(row.get("assignee_id", ""), row.get("assignee_id", ""))
        assignee_team = refs["eng_team"].get(row.get("assignee_id", ""), "")
        assignee_dept = refs["team_dept"].get(assignee_team, "")
        module_name   = refs["modules"].get(row.get("module_id", ""), row.get("module_id", ""))
        proj_name     = refs["mod_proj"].get(row.get("module_id", ""), "")
        release_ver   = refs["releases"].get(row.get("blocks_release_id", ""), "")

        text = (
            f"バグ {row['id']}「{row['title']}」は severity: {row['severity']}, "
            f"status: {row['status']} です。"
            f" 担当者は {assignee_name}（{assignee_team} チーム, {assignee_dept} 部署）です。"
            f" このバグは {module_name} モジュール（{proj_name} プロジェクト）で発見されました。"
        )
        if release_ver:
            text += f" このバグは {release_ver} のリリースをブロックしています。"

        docs.append(text); ids.append(f"bug_{row['id']}"); metas.append({"type": "Bug"})

    return docs, ids, metas


def _load_reference_tables(data_dir: str) -> dict:
    """ID → 名前のルックアップテーブルを構築する"""
    def _read(filename):
        path = Path(data_dir) / filename
        if not path.exists():
            return []
        with open(path, encoding="utf-8") as f:
            return list(csv.DictReader(f))

    depts      = {r["id"]: r["name"] for r in _read("departments.csv")}
    teams      = {r["id"]: r["name"] for r in _read("teams.csv")}
    team_dept  = {r["id"]: depts.get(r.get("department_id", ""), "") for r in _read("teams.csv")}
    engineers  = {r["id"]: r["name"] for r in _read("engineers.csv")}
    eng_team   = {r["id"]: r.get("team_id", "") for r in _read("engineers.csv")}
    projects   = {r["id"]: r["name"] for r in _read("projects.csv")}
    modules    = {r["id"]: r["name"] for r in _read("modules.csv")}
    mod_proj   = {r["id"]: projects.get(r.get("project_id", ""), "") for r in _read("modules.csv")}
    releases   = {r["id"]: r["version"] for r in _read("releases.csv")}

    return {
        "departments": depts,
        "teams": teams,
        "team_dept": team_dept,
        "engineers": engineers,
        "eng_team": eng_team,
        "projects": projects,
        "modules": modules,
        "mod_proj": mod_proj,
        "releases": releases,
    }


def run_rag(
    prompt: str,
    model_name: str,
    collection: chromadb.Collection,
    n_results: int = 5,
) -> RAGResult:
    """
    ベクターRAGで質問に回答する。

    Parameters
    ----------
    prompt      : 自然言語の質問
    model_name  : Ollamaのモデル名
    collection  : 事前に構築したChromaDBコレクション
    n_results   : 取得するドキュメント数（デフォルト5）
    """
    ollama_url = get_ollama_url()

    # 類似度検索
    results = collection.query(query_texts=[prompt], n_results=n_results)
    retrieved_docs = results["documents"][0] if results["documents"] else []

    context = "\n".join(retrieved_docs)
    full_prompt = (
        "以下のコンテキスト情報を参考にして、質問に日本語で回答してください。\n\n"
        f"コンテキスト:\n{context}\n\n"
        f"質問: {prompt}\n\n"
        "回答:"
    )

    start = time.perf_counter()
    resp = requests.post(
        f"{ollama_url}/api/generate",
        json={"model": model_name, "prompt": full_prompt, "stream": False},
        timeout=300,
    )
    elapsed = time.perf_counter() - start

    data = resp.json()
    answer            = data.get("response", "")
    prompt_tokens     = data.get("prompt_eval_count", 0)
    completion_tokens = data.get("eval_count", 0)

    return RAGResult(
        answer=answer,
        retrieved_docs=retrieved_docs,
        elapsed_sec=elapsed,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )
