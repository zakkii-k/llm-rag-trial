"""
main_interactive.py — 対話形式でRAG/GraphRAGを実行する

使い方:
    python app/main_interactive.py --mode rag     --model small --data-dir data/medium
    python app/main_interactive.py --mode graphrag --model large --data-dir data/large
    python app/main_interactive.py --mode both    --model small --data-dir data/small

オプション:
    --mode      : rag / graphrag / both  (default: both)
    --model     : small / large          (default: small)
    --data-dir  : CSVのあるディレクトリ   (default: data/small)
    --n-results : RAGの取得ドキュメント数 (default: 5)
"""

import argparse
import sys
from pathlib import Path

# プロジェクトルートをパスに追加（app/ から実行される場合に対応）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from app.modules.models import MODEL_CONFIG
from app.modules.report import save_report


def parse_args():
    parser = argparse.ArgumentParser(description="対話形式 RAG/GraphRAG 比較ツール")
    parser.add_argument("--mode",      choices=["rag", "graphrag", "both"], default="both")
    parser.add_argument("--model",     choices=["small", "large"],          default="small")
    parser.add_argument("--data-dir",  default="data/small")
    parser.add_argument("--n-results", type=int, default=5, help="RAGの取得件数")
    return parser.parse_args()


def main():
    args   = parse_args()
    mode   = args.mode
    config = MODEL_CONFIG[args.model]
    model_name = config["name"]
    data_dir   = args.data_dir

    print(f"\n=== RAG/GraphRAG 比較ツール ===")
    print(f"  モード   : {mode}")
    print(f"  モデル   : {model_name} ({config['description']})")
    print(f"  データ   : {data_dir}")
    print(f"  終了     : 'exit' または Ctrl+C\n")

    # RAGのベクターストアを事前構築
    collection = None
    if mode in ("rag", "both"):
        print("RAGのベクターストアを構築中...")
        from app.modules.rag_engine import build_vector_store
        collection = build_vector_store(data_dir)
        print("ベクターストア構築完了\n")

    while True:
        try:
            prompt = input("質問> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n終了します。")
            break

        if not prompt:
            continue
        if prompt.lower() == "exit":
            break

        _execute_and_report(mode, model_name, data_dir, prompt, collection, args.n_results)


def _execute_and_report(mode, model_name, data_dir, prompt, collection, n_results):
    if mode in ("graphrag", "both"):
        print("\n[GraphRAG] 実行中...")
        from app.modules.graphrag_engine import run_graphrag
        gr = run_graphrag(prompt, model_name)
        report_path = save_report(
            mode="graphrag", model_name=model_name, prompt=prompt,
            answer=gr.answer, elapsed_sec=gr.elapsed_sec,
            prompt_tokens=gr.prompt_tokens, completion_tokens=gr.completion_tokens,
            cypher_query=gr.cypher_query, cypher_result=gr.cypher_result,
            data_dir=data_dir,
        )
        _print_result("GraphRAG", gr.answer, gr.elapsed_sec,
                      gr.prompt_tokens, gr.completion_tokens, report_path)

    if mode in ("rag", "both"):
        print("\n[RAG] 実行中...")
        from app.modules.rag_engine import run_rag
        rr = run_rag(prompt, model_name, collection, n_results)
        report_path = save_report(
            mode="rag", model_name=model_name, prompt=prompt,
            answer=rr.answer, elapsed_sec=rr.elapsed_sec,
            prompt_tokens=rr.prompt_tokens, completion_tokens=rr.completion_tokens,
            data_dir=data_dir,
        )
        _print_result("RAG", rr.answer, rr.elapsed_sec,
                      rr.prompt_tokens, rr.completion_tokens, report_path)


def _print_result(label, answer, elapsed, pt, ct, report_path):
    print(f"\n--- {label} 結果 ---")
    print(f"回答: {answer}")
    print(f"時間: {elapsed:.2f}s  |  トークン: {pt}(in) + {ct}(out) = {pt+ct}(合計)")
    print(f"レポート: {report_path}")


if __name__ == "__main__":
    main()
