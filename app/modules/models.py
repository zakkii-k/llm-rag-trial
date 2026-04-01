"""
models.py — 使用するLLMモデルの設定

メモリ: 27GB RAM
- small      : llama3.2           (3B,  ~2GB)   — 汎用軽量
- qwen-small : qwen2.5-coder:7b   (7B,  ~4.7GB) — Cypher/コード特化（軽量）
- qwen-large : qwen2.5-coder:14b  (14B, ~9GB)   — Cypher/コード特化（高精度）
- large      : gemma2:27b         (27B, ~15GB)  — 汎用高精度

Gemini API (Google AI Studio):
- gemini-flash : gemini-1.5-flash  — 高速・安価・広いコンテキスト
- gemini-pro   : gemini-1.5-pro    — 最高精度

GraphRAG の Cypher 生成精度を上げたい場合は --model qwen-small または --model qwen-large を使用。
"""

MODEL_CONFIG = {
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
    "large": {
        "name": "gemma2:27b",
        "description": "Gemma 2 27B — 汎用高精度モデル (~15GB)",
    },
    "gemini-flash": {
        "name": "gemini-1.5-flash",
        "description": "Gemini 1.5 Flash — API経由 / 高速・高機能",
    },
    "gemini-pro": {
        "name": "gemini-1.5-pro",
        "description": "Gemini 1.5 Pro — API経由 / 最高精度モデル",
    },
}

# ChromaDB/RAG用の埋め込みモデル
EMBEDDING_MODEL = "nomic-embed-text"
