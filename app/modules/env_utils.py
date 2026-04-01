"""
env_utils.py — 実行環境の自動検出とデフォルト値解決

Docker コンテナ内か WSL/ホストかを検出し、
接続先ホストのデフォルト値を切り替える。

  Docker コンテナ内 → host.docker.internal
  WSL / ホスト直実行 → localhost
"""

import os


def detect_host() -> str:
    """
    実行環境を検出して適切なホスト名を返す。
    /.dockerenv が存在すれば Docker コンテナ内と判断する。
    """
    return "host.docker.internal" if os.path.exists("/.dockerenv") else "localhost"


def get_neo4j_uri() -> str:
    """NEO4J_URI 環境変数、なければ実行環境に合わせたデフォルトを返す"""
    return os.getenv("NEO4J_URI", f"bolt://{detect_host()}:7687")


def get_ollama_url() -> str:
    """OLLAMA_BASE_URL 環境変数、なければ実行環境に合わせたデフォルトを返す"""
    return os.getenv("OLLAMA_BASE_URL", f"http://{detect_host()}:11434")
