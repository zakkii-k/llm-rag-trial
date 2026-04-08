"""
s2g_chat.py – source2graph × ローカルLLM チャット

source2graph MCP サーバーのツールを Ollama のツール呼び出しに接続し、
ローカルLLM（llama / qwen2.5-coder / qwen3 / qwen3.5 / gemma2）が
コードグラフを参照しながら回答できるようにする。

使い方:
    python app/s2g_chat.py --repo /path/to/repo --model qwen-small

オプション:
    --repo   解析対象リポジトリのパス（デフォルト: /app）
    --model  使用モデルキー（デフォルト: qwen-small = Qwen 2.5 Coder 7B）
    --s2g    source2graph CLI パス（デフォルト: /app/source2graph/dist/cli/index.js）
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.modules.env_utils import get_ollama_url
from app.modules.models import MODEL_CONFIG
from app.modules.s2g_mcp_client import DEFAULT_S2G_CLI, S2GClient

LOCAL_MODELS = {k: v for k, v in MODEL_CONFIG.items() if not k.startswith("gemini")}

SYSTEM_PROMPT = """\
あなたはコードグラフ解析アシスタントです。
source2graph のツールを使ってコードの構造・依存関係・呼び出し関係を調べ、
ユーザーの質問に日本語で答えてください。

利用可能なツール:
- analyze        : リポジトリを解析してグラフを構築
- query_nodes    : ラベル・名前・ファイルパスでノードを検索
- get_callers    : 指定シンボルを呼び出している箇所を取得
- get_callees    : 指定シンボルが呼び出すものを取得
- get_context    : シンボルの360度ビュー（呼び出し元・先・継承関係）
"""


async def chat_loop(repo_path: str, model_key: str, s2g_cli: str) -> None:
    model_name = LOCAL_MODELS[model_key]["name"]
    ollama_url = get_ollama_url()

    print(f"source2graph MCP サーバーに接続中... (repo: {repo_path})")

    async with S2GClient(repo_path, s2g_cli) as s2g:
        tools = s2g.get_ollama_tools()
        print(f"接続完了 — ツール: {', '.join(s2g.tool_names)}")
        print(f"モデル : {model_name}")
        print("終了するには 'exit' または Ctrl+C\n")

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        while True:
            try:
                question = input("質問> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n終了します")
                break

            if question.lower() in ("exit", "quit", "q"):
                break
            if not question:
                continue

            messages.append({"role": "user", "content": question})

            # ツール呼び出しループ
            while True:
                resp = requests.post(
                    f"{ollama_url}/api/chat",
                    json={
                        "model": model_name,
                        "messages": messages,
                        "tools": tools,
                        "stream": False,
                    },
                    timeout=300,
                )
                resp.raise_for_status()
                msg = resp.json()["message"]

                if msg.get("tool_calls"):
                    messages.append(msg)
                    for tc in msg["tool_calls"]:
                        fn = tc["function"]
                        args = fn.get("arguments", {})
                        if isinstance(args, str):
                            args = json.loads(args)

                        print(
                            f"  → {fn['name']}({json.dumps(args, ensure_ascii=False)})"
                        )
                        result = await s2g.call_tool(fn["name"], args)
                        messages.append({"role": "tool", "content": result})
                else:
                    print(f"\n{msg['content']}\n")
                    messages.append(msg)
                    break


def main() -> None:
    parser = argparse.ArgumentParser(
        description="source2graph × ローカルLLM チャット"
    )
    parser.add_argument(
        "--repo",
        default="/app",
        help="解析対象リポジトリのパス（デフォルト: /app）",
    )
    parser.add_argument(
        "--model",
        default="qwen-small",
        choices=list(LOCAL_MODELS.keys()),
        help="使用モデルキー（デフォルト: qwen-small）",
    )
    parser.add_argument(
        "--s2g",
        default=DEFAULT_S2G_CLI,
        help=f"source2graph CLI パス（デフォルト: {DEFAULT_S2G_CLI}）",
    )
    args = parser.parse_args()

    if args.model not in LOCAL_MODELS:
        print(f"不明なモデル: {args.model}")
        print(f"利用可能: {', '.join(LOCAL_MODELS.keys())}")
        sys.exit(1)

    asyncio.run(chat_loop(args.repo, args.model, args.s2g))


if __name__ == "__main__":
    main()
