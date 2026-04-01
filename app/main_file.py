"""
main_file.py — プロンプトファイルを読み込んでRAG/GraphRAGを一括実行する

使い方:
    python app/main_file.py --prompt-file prompts/simple.txt --mode rag --model small --data-dir data/small
    python app/main_file.py --prompt-file prompts/multihop.txt --mode both --model large --data-dir data/large

プロンプトファイル形式:
    - 1行1質問
    - "#" で始まる行はコメントとして無視
    - 空行は無視

オプション:
    --prompt-file : 質問が書かれたtxtファイルのパス（必須）
    --mode        : rag / graphrag / both  (default: both)
    --model       : small / large          (default: small)
    --data-dir    : CSVのあるディレクトリ   (default: data/small)
    --n-results   : RAGの取得ドキュメント数 (default: 5)
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from app.modules.models import MODEL_CONFIG
from app.modules.report import save_report


def parse_args():
    parser = argparse.ArgumentParser(description="ファイル入力 RAG/GraphRAG 比較ツール")
    parser.add_argument("--prompt-file", required=True, help="質問一覧txtファイル")
    parser.add_argument("--mode",        choices=["rag", "graphrag", "both"], default="both")
    parser.add_argument("--model",       choices=["small", "large"],          default="small")
    parser.add_argument("--data-dir",    default="data/small")
    parser.add_argument("--n-results",   type=int, default=5)
    return parser.parse_args()


def load_prompts(filepath: str) -> list[str]:
    lines = Path(filepath).read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines if l.strip() and not l.startswith("#")]


def main():
    args   = parse_args()
    mode   = args.mode
    config = MODEL_CONFIG[args.model]
    model_name = config["name"]
    data_dir   = args.data_dir

    prompts = load_prompts(args.prompt_file)
    if not prompts:
        print("質問が見つかりませんでした。ファイルを確認してください。")
        sys.exit(1)

    print(f"\n=== ファイル入力 RAG/GraphRAG 比較ツール ===")
    print(f"  モード   : {mode}")
    print(f"  モデル   : {model_name} ({config['description']})")
    print(f"  データ   : {data_dir}")
    print(f"  質問数   : {len(prompts)} 件\n")

    collection = None
    if mode in ("rag", "both"):
        print("RAGのベクターストアを構築中...")
        from app.modules.rag_engine import build_vector_store
        collection = build_vector_store(data_dir)
        print("ベクターストア構築完了\n")

    for i, prompt in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] 質問: {prompt}")

        if mode in ("graphrag", "both"):
            print("  [GraphRAG] 実行中...")
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
            print("  [RAG] 実行中...")
            from app.modules.rag_engine import run_rag
            rr = run_rag(prompt, model_name, collection, args.n_results)
            report_path = save_report(
                mode="rag", model_name=model_name, prompt=prompt,
                answer=rr.answer, elapsed_sec=rr.elapsed_sec,
                prompt_tokens=rr.prompt_tokens, completion_tokens=rr.completion_tokens,
                data_dir=data_dir,
            )
            _print_result("RAG", rr.answer, rr.elapsed_sec,
                          rr.prompt_tokens, rr.completion_tokens, report_path)

        print()

    print("全質問の処理が完了しました。")


def _print_result(label, answer, elapsed, pt, ct, report_path):
    print(f"  --- {label} ---")
    print(f"  回答: {answer[:120]}{'...' if len(answer) > 120 else ''}")
    print(f"  時間: {elapsed:.2f}s  |  トークン: {pt}(in) + {ct}(out) = {pt+ct}(合計)")
    print(f"  レポート: {report_path}")


if __name__ == "__main__":
    main()
