"""
models.py — 使用するLLMモデルの設定

メモリ: 27GB RAM
- small: llama3.2 (3B, ~2GB)   — 軽量・高速
- large: llama3.1:8b (8B, ~4.7GB) — 高精度（5GB以下）

モデル変更は MODEL_CONFIG を編集するか --model 引数で切り替える。
"""

MODEL_CONFIG = {
    "small": {
        "name": "llama3.2",
        "description": "Llama 3.2 3B — 軽量モデル (~2GB)",
    },
    "large": {
        "name": "llama3.1:8b",
        "description": "Llama 3.1 8B — 高精度モデル (~4.7GB)",
    },
}

# ChromaDB/RAG用の埋め込みモデル
EMBEDDING_MODEL = "nomic-embed-text"
