"""
run_scenario.py — シナリオ実行スクリプト

レポートはシナリオ×モード単位で1ファイル生成する。
（例: 20260401_120000_A_simple_graphrag_llama3.2.md）

使い方:
    python app/run_scenario.py \
        --prompt-file prompts/simple.txt \
        --mode both \
        --model small \
        --data-dir data/small \
        --scenario-name "A_simple_small"
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dotenv import load_dotenv
load_dotenv()

from app.modules.models import MODEL_CONFIG
from app.modules.report import save_scenario_report


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--mode", choices=["rag", "graphrag", "both"], default="both")
    parser.add_argument("--model", choices=list(MODEL_CONFIG.keys()), default="small")
    parser.add_argument("--data-dir", default="data/small")
    parser.add_argument("--n-results", type=int, default=5)
    parser.add_argument("--scenario-name", default="scenario")
    return parser.parse_args()


def load_prompts(filepath):
    lines = Path(filepath).read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines if l.strip() and not l.startswith("#")]


def main():
    args = parse_args()
    config = MODEL_CONFIG[args.model]
    model_name = config["name"]
    prompts = load_prompts(args.prompt_file)
    started_at = datetime.now()

    print(f"\n{'='*60}")
    print(f"シナリオ: {args.scenario_name}")
    print(f"モード: {args.mode} | モデル: {model_name} | データ: {args.data_dir}")
    print(f"クエリ数: {len(prompts)}")
    print(f"{'='*60}\n")

    # RAGベクターストアを事前構築
    collection = None
    if args.mode in ("rag", "both"):
        print("RAGベクターストア構築中...")
        from app.modules.rag_engine import build_vector_store
        collection = build_vector_store(args.data_dir)
        print("構築完了\n")

    graphrag_results = []
    rag_results = []

    for i, prompt in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] {prompt}")

        # ── GraphRAG ──
        if args.mode in ("graphrag", "both"):
            print("  [GraphRAG] 実行中...")
            try:
                from app.modules.graphrag_engine import run_graphrag
                gr = run_graphrag(prompt, model_name)
                entry = {
                    "prompt": prompt,
                    "answer": gr.answer,
                    "cypher": gr.cypher_query,
                    "cypher_result": gr.cypher_result,
                    "elapsed": round(gr.elapsed_sec, 2),
                    "tokens_in": gr.prompt_tokens,
                    "tokens_out": gr.completion_tokens,
                    "total_attempts": gr.total_attempts,
                    "attempts": [
                        {
                            "attempt_num": a.attempt_num,
                            "cypher_query": a.cypher_query,
                            "error": a.error,
                            "cypher_result": a.cypher_result,
                        }
                        for a in gr.attempts
                    ],
                }
                retry_info = f" | {gr.total_attempts}回試行" if gr.total_attempts > 1 else ""
                print(f"  → {gr.elapsed_sec:.1f}s | {gr.prompt_tokens+gr.completion_tokens}tok{retry_info}")
                print(f"     Cypher: {gr.cypher_query[:80]}...")
                print(f"     回答: {gr.answer[:60]}")
            except Exception as e:
                entry = {"prompt": prompt, "error": str(e)}
                print(f"  → エラー: {e}")
            graphrag_results.append(entry)

        # ── RAG ──
        if args.mode in ("rag", "both"):
            print("  [RAG] 実行中...")
            try:
                from app.modules.rag_engine import run_rag
                rr = run_rag(prompt, model_name, collection, args.n_results)
                entry = {
                    "prompt": prompt,
                    "answer": rr.answer,
                    "elapsed": round(rr.elapsed_sec, 2),
                    "tokens_in": rr.prompt_tokens,
                    "tokens_out": rr.completion_tokens,
                }
                print(f"  → {rr.elapsed_sec:.1f}s | {rr.prompt_tokens+rr.completion_tokens}tok")
                print(f"     回答: {rr.answer[:60]}")
            except Exception as e:
                entry = {"prompt": prompt, "error": str(e)}
                print(f"  → エラー: {e}")
            rag_results.append(entry)

        print()

    # ── シナリオ単位でレポート保存 ──
    report_paths = []
    if graphrag_results:
        p = save_scenario_report(
            scenario_name=args.scenario_name,
            mode="graphrag",
            model_name=model_name,
            data_dir=args.data_dir,
            results=graphrag_results,
            started_at=started_at,
        )
        report_paths.append(p)
        print(f"GraphRAGレポート: {p}")

    if rag_results:
        p = save_scenario_report(
            scenario_name=args.scenario_name,
            mode="rag",
            model_name=model_name,
            data_dir=args.data_dir,
            results=rag_results,
            started_at=started_at,
        )
        report_paths.append(p)
        print(f"RAGレポート: {p}")

    # JSON サマリを返す（review用）
    summary = {
        "scenario": args.scenario_name,
        "mode": args.mode,
        "model": model_name,
        "data_dir": args.data_dir,
        "graphrag": graphrag_results,
        "rag": rag_results,
        "reports": [str(p) for p in report_paths],
    }
    print("\n--- RESULTS JSON ---")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


if __name__ == "__main__":
    main()
