"""
report.py — 実行結果をMarkdownレポートとして保存する
"""

import os
from datetime import datetime
from pathlib import Path


REPORTS_DIR = Path("docs/reports")


def save_scenario_report(
    scenario_name: str,
    mode: str,
    model_name: str,
    data_dir: str,
    results: list[dict],
    started_at: datetime | None = None,
) -> Path:
    """
    シナリオ単位（複数クエリをまとめて）のレポートを1ファイルに保存する。

    results の各要素:
        {
          "prompt": str,
          "answer": str,
          "elapsed": float,
          "tokens_in": int,
          "tokens_out": int,
          "cypher": str,        # GraphRAGのみ
          "cypher_result": str, # GraphRAGのみ
          "error": str,         # エラー時のみ
        }
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    now = started_at or datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    safe_model = model_name.replace(":", "-").replace("/", "-")
    filename = f"{timestamp}_{scenario_name}_{mode}_{safe_model}.md"
    report_path = REPORTS_DIR / filename

    total_elapsed = sum(r.get("elapsed", 0) for r in results)
    total_tokens_in = sum(r.get("tokens_in", 0) for r in results)
    total_tokens_out = sum(r.get("tokens_out", 0) for r in results)

    lines = [
        f"# 実行レポート — {scenario_name}",
        "",
        "| 項目 | 値 |",
        "|------|-----|",
        f"| 実行日時 | {now.strftime('%Y-%m-%d %H:%M:%S')} |",
        f"| シナリオ | {scenario_name} |",
        f"| モード | {mode} |",
        f"| モデル | {model_name} |",
        f"| データソース | {data_dir} |",
        f"| クエリ数 | {len(results)} |",
        f"| 合計回答時間 | {total_elapsed:.2f} 秒 |",
        f"| 合計トークン（入力） | {total_tokens_in} |",
        f"| 合計トークン（出力） | {total_tokens_out} |",
        "",
        "---",
        "",
    ]

    for i, r in enumerate(results, 1):
        lines += [
            f"## Q{i}. {r['prompt']}",
            "",
        ]

        if "error" in r:
            lines += [f"**エラー:** {r['error']}", ""]
            continue

        if mode in ("graphrag", "both") and r.get("cypher"):
            lines += [
                "**生成Cypherクエリ:**",
                "",
                "```cypher",
                r["cypher"].strip(),
                "```",
                "",
                "**Cypher実行結果:**",
                "",
                "```",
                str(r.get("cypher_result", "")).strip(),
                "```",
                "",
            ]

        lines += [
            "**回答:**",
            "",
            r.get("answer", "（回答なし）").strip(),
            "",
            "| 指標 | 値 |",
            "|------|-----|",
            f"| 回答時間 | {r.get('elapsed', 0):.2f} 秒 |",
            f"| 入力トークン | {r.get('tokens_in', 0)} |",
            f"| 出力トークン | {r.get('tokens_out', 0)} |",
            "",
        ]

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def save_report(
    mode: str,
    model_name: str,
    prompt: str,
    answer: str,
    elapsed_sec: float,
    prompt_tokens: int,
    completion_tokens: int,
    cypher_query: str = "",
    cypher_result: str = "",
    data_dir: str = "",
) -> Path:
    """
    1回の実行結果をMarkdownファイルに保存して、そのパスを返す。

    Parameters
    ----------
    mode            : "rag" / "graphrag" / "both"
    model_name      : 使用したOllamaモデル名
    prompt          : ユーザーが入力した質問
    answer          : LLMの回答
    elapsed_sec     : 回答にかかった秒数
    prompt_tokens   : 入力トークン数（メタデータより）
    completion_tokens: 出力トークン数（メタデータより）
    cypher_query    : GraphRAGで生成されたCypherクエリ（GraphRAGのみ）
    cypher_result   : Cypherの実行結果（GraphRAGのみ）
    data_dir        : 使用したデータディレクトリ
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{mode}_{model_name.replace(':', '-').replace('/', '-')}.md"
    report_path = REPORTS_DIR / filename

    lines = [
        f"# 実行レポート",
        f"",
        f"| 項目 | 値 |",
        f"|------|-----|",
        f"| 実行日時 | {now.strftime('%Y-%m-%d %H:%M:%S')} |",
        f"| モード | {mode} |",
        f"| モデル | {model_name} |",
        f"| データソース | {data_dir or '—'} |",
        f"",
        f"## プロンプト",
        f"",
        f"```",
        prompt.strip(),
        f"```",
        f"",
    ]

    if mode in ("graphrag", "both") and cypher_query:
        lines += [
            f"## 生成されたCypherクエリ（GraphRAG）",
            f"",
            f"```cypher",
            cypher_query.strip(),
            f"```",
            f"",
            f"## Cypher実行結果",
            f"",
            f"```",
            str(cypher_result).strip(),
            f"```",
            f"",
        ]

    lines += [
        f"## 回答",
        f"",
        answer.strip(),
        f"",
        f"## パフォーマンス",
        f"",
        f"| 指標 | 値 |",
        f"|------|-----|",
        f"| 回答時間 | {elapsed_sec:.2f} 秒 |",
        f"| 入力トークン | {prompt_tokens} |",
        f"| 出力トークン | {completion_tokens} |",
        f"| 合計トークン | {prompt_tokens + completion_tokens} |",
        f"",
    ]

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
