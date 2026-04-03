# llm-rag-trial — GraphRAG vs RAG 検証環境

Neo4j + Ollama / Gemini API を使った GraphRAG とベクター RAG の比較検証プロジェクト。

## 概要

| 比較軸 | 内容 |
|--------|------|
| GraphRAG vs RAG | 精度・速度・トークン量 |
| モデル | llama / qwen2.5-coder / qwen3 / qwen3.5 / gemma2 / Gemini API |
| クエリ複雑度 | simple / medium / multihop |
| データ量 | small / medium / large |

## クイックスタート（初回）

```bash
git clone <このリポジトリ>
cd llm-rag-trial
bash scripts/bootstrap.sh   # Docker起動 → setup.sh まで一括
```

> 2回目以降は `bash scripts/setup.sh` のみで OK。

## ディレクトリ構成

```
.
├── app/
│   ├── build_kg.py           # Neo4j ナレッジグラフ構築
│   ├── run_scenario.py       # シナリオ単体実行
│   └── modules/
│       ├── graphrag_engine.py  # GraphRAGエンジン（Few-shot Cypher + リトライ）
│       ├── rag_engine.py       # ベクターRAGエンジン（ChromaDB）
│       ├── llm_client.py       # Ollama / Gemini API 統一クライアント
│       ├── env_utils.py        # 実行環境自動検出（Docker / WSL）
│       ├── report.py           # Markdownレポート生成
│       └── models.py           # モデル設定一覧
├── data/
│   ├── small/    # Bug×3,  Engineer×3  （1〜2ホップ向け）
│   ├── medium/   # Bug×30, Engineer×10 （2〜3ホップ向け）
│   └── large/    # Bug×100,Engineer×30 （3+ホップ向け）
├── prompts/
│   ├── simple.txt    # 単一エンティティ基本クエリ
│   ├── medium.txt    # 複数エンティティ・集計クエリ
│   └── multihop.txt  # 3ホップ以上の複合クエリ
├── scripts/
│   ├── bootstrap.sh  # 初回セットアップ（Docker起動〜setup.shまで）
│   ├── setup.sh      # 環境構築（モデルpull、グラフデータロード）
│   ├── run_all.sh    # 全パターン一括実行
│   └── _common.sh    # 共通定義（モデル・メニュー関数等）
├── docs/
│   ├── how-to-run.md   # 詳細セットアップ手順
│   └── reports/        # 実行レポート（自動生成）
└── docker-compose.yml
```

## グラフ構造

```
(Bug)-[:ASSIGNED_TO]->(Engineer)-[:MEMBER_OF]->(Team)-[:BELONGS_TO]->(Department)
(Bug)-[:FOUND_IN]->(Module)-[:PART_OF]->(Project)
(Bug)-[:BLOCKS]->(Release)-[:BELONGS_TO]->(Project)
```

## モデル一覧

### Ollama ローカルモデル

| キー | モデル名 | サイズ | 特徴 |
|------|----------|--------|------|
| `small` | llama3.2 | ~2GB | 汎用軽量・ベースライン |
| `qwen-small` | qwen2.5-coder:7b | ~4.7GB | Cypher/コード特化・軽量 |
| `qwen-large` | qwen2.5-coder:14b | ~9GB | Cypher/コード特化・高精度 |
| `qwen-coder-32b` | qwen2.5-coder:32b | ~20GB | Cypher/コード特化・最大 |
| `qwen3-small` | qwen3:8b | ~5.2GB | Qwen3世代・軽量 |
| `qwen3-medium` | qwen3:14b | ~9.3GB | Qwen3世代・中規模 |
| `qwen3-large` | qwen3:32b | ~18.8GB | Qwen3世代・大規模 |
| `qwen35-small` | qwen3.5:4b | ~3GB | Qwen3.5世代・軽量（マルチモーダル） |
| `qwen35-medium` | qwen3.5:9b | ~6GB | Qwen3.5世代・中規模 |
| `qwen35-large` | qwen3.5:27b | ~16GB | Qwen3.5世代・大規模 |
| `large` | gemma2:27b | ~15GB | 汎用高精度 |

### Google Gemini API（要 API キー）

| キー | モデル名 | 特徴 |
|------|----------|------|
| `gemini-flash` | gemini-1.5-flash | 高速・高機能 |
| `gemini-pro` | gemini-1.5-pro | 最高精度 |

> Gemini を使う場合は `.env` に `GOOGLE_API_KEY=<your_key>` を設定してください。
> `setup.sh` / `run_all.sh` 実行時にAPIキーの有効性を自動検証します。

## セットアップ

```bash
bash scripts/setup.sh
```

実行内容:
1. 実行環境検出（Docker / WSL）と `.env` 自動生成・修正
2. Python / pip / Ollama / Neo4j 接続確認
3. Python パッケージのインストール
4. メモリ確認 → 利用可能なモデルのみ pull（APIモデルはスキップ）
5. Neo4j グラフデータのロード（データサイズを対話選択）

> **ホスト自動切替**: Docker コンテナ内 → `host.docker.internal`、WSL/ホスト直実行 → `localhost` を自動設定。

## 実行方法

### 全パターン一括実行（推奨）

```bash
bash scripts/run_all.sh
```

モデル・データサイズ・クエリ種別・モードを対話選択し、全組み合わせを順に実行します。

### シナリオ単体実行

```bash
python3 app/run_scenario.py \
    --prompt-file prompts/multihop.txt \
    --mode both \
    --model qwen3-small \
    --data-dir data/large \
    --scenario-name "multihop_large_qwen3-small"
```

## レポート

各実行後に `docs/reports/` へ Markdown レポートが自動生成されます。
レポートには実行日時・プロンプト・回答・Cypher クエリ・リトライ履歴・経過時間・トークン数が含まれます。
