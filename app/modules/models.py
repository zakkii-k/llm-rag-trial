"""
models.py — 使用するLLMモデルの設定

メモリ: 27GB RAM
- small : llama3.2          (3B,  ~2GB)  — 軽量・高速
- coder : qwen2.5-coder:7b  (7B,  ~4.7GB) — コード/Cypher特化（GraphRAG精度向上）
- large : gemma2:27b        (27B, ~15GB) — 高精度

GraphRAGのCypher生成精度を上げたい場合は --model coder を使用。
モデル変更は MODEL_CONFIG を編集するか --model 引数で切り替える。
"""

MODEL_CONFIG = {
    "small": {
        "name": "llama3.2",
        "description": "Llama 3.2 3B — 軽量モデル (~2GB)",
    },
    "coder": {
        "name": "qwen2.5-coder:7b",
        "description": "Qwen 2.5 Coder 7B — コード/Cypher特化モデル (~4.7GB)。GraphRAG精度向上に推奨",
    },
    "large": {
        "name": "gemma2:27b",
        "description": "Gemma 2 27B — 高精度モデル (~15GB)",
    },
}

# ChromaDB/RAG用の埋め込みモデル
EMBEDDING_MODEL = "nomic-embed-text"
