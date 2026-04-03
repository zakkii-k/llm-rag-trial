"""
models.py — 使用するLLMモデルの設定

メモリ: 27GB RAM
ローカル (Ollama):
  small            : llama3.2           (3B,  ~2GB)
  qwen-small       : qwen2.5-coder:7b   (7B,  ~4.7GB) Cypher特化
  qwen-large       : qwen2.5-coder:14b  (14B, ~9GB)   Cypher特化
  qwen-coder-32b   : qwen2.5-coder:32b  (32B, ~20GB)  Cypher特化・最大
  qwen3-small      : qwen3:8b           (8B,  ~5.2GB) 最新世代軽量
  qwen3-medium     : qwen3:14b          (14B, ~9.3GB) 最新世代中規模
  qwen3-large      : qwen3:32b          (32B, ~18.8GB)最新世代大規模
  qwen35-small     : qwen3.5:4b         (4B,  ~3GB)   マルチモーダル世代軽量
  qwen35-medium    : qwen3.5:9b         (9B,  ~6GB)   マルチモーダル世代中規模
  qwen35-large     : qwen3.5:27b        (27B, ~16GB)  マルチモーダル世代大規模
  large            : gemma2:27b         (27B, ~15GB)  汎用高精度

API:
  gemini-flash     : gemini-1.5-flash   高速・低コスト
  gemini-pro       : gemini-1.5-pro     最高精度

GraphRAG の Cypher 生成精度を上げたい場合は qwen3 系または qwen-coder 系を推奨。
"""

MODEL_CONFIG = {
    # ── Ollama ローカルモデル ──────────────────────────────────────────────────
    "small": {
        "name": "llama3.2",
        "description": "Llama 3.2 3B — 汎用軽量モデル (~2GB)",
    },
    "qwen-small": {
        "name": "qwen2.5-coder:7b",
        "description": "Qwen 2.5 Coder 7B — コード/Cypher特化・軽量 (~4.7GB)",
    },
    "qwen-large": {
        "name": "qwen2.5-coder:14b",
        "description": "Qwen 2.5 Coder 14B — コード/Cypher特化・高精度 (~9GB)",
    },
    "qwen-coder-32b": {
        "name": "qwen2.5-coder:32b",
        "description": "Qwen 2.5 Coder 32B — コード/Cypher特化・最大 (~20GB)",
    },
    "qwen3-small": {
        "name": "qwen3:8b",
        "description": "Qwen3 8B — 最新世代・軽量 (~5.2GB)",
    },
    "qwen3-medium": {
        "name": "qwen3:14b",
        "description": "Qwen3 14B — 最新世代・中規模 (~9.3GB)",
    },
    "qwen3-large": {
        "name": "qwen3:32b",
        "description": "Qwen3 32B — 最新世代・大規模 (~18.8GB)",
    },
    "qwen35-small": {
        "name": "qwen3.5:4b",
        "description": "Qwen3.5 4B — マルチモーダル世代・軽量 (~3GB)",
    },
    "qwen35-medium": {
        "name": "qwen3.5:9b",
        "description": "Qwen3.5 9B — マルチモーダル世代・中規模 (~6GB)",
    },
    "qwen35-large": {
        "name": "qwen3.5:27b",
        "description": "Qwen3.5 27B — マルチモーダル世代・大規模 (~16GB)",
    },
    "large": {
        "name": "gemma2:27b",
        "description": "Gemma 2 27B — 汎用高精度モデル (~15GB)",
    },
    # ── Google Gemini API ─────────────────────────────────────────────────────
    "gemini-flash": {
        "name": "gemini-1.5-flash",
        "description": "Gemini 1.5 Flash — API経由 / 高速・高機能",
    },
    "gemini-pro": {
        "name": "gemini-1.5-pro",
        "description": "Gemini 1.5 Pro — API経由 / 最高精度",
    },
}

# ChromaDB/RAG用の埋め込みモデル（常にOllama経由）
EMBEDDING_MODEL = "nomic-embed-text"
