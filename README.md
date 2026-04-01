# llm-rag-trial — GraphRAG vs RAG 検証環境

Neo4j + Ollama を使った GraphRAG とベクターRAGの比較検証プロジェクト。

## 比較内容

| 比較軸 | 内容 |
|--------|------|
| GraphRAG vs RAG | 精度・速度・トークン量 |
| モデルサイズ | small (llama3.2) vs large (llama3.1:8b) |
| クエリ複雑度 | simple / medium / multi-hop |
| データ量 | small / medium / large |

## ディレクトリ構成

```
.
├── app/
│   ├── build_kg.py           # Neo4j ナレッジグラフ構築
│   ├── main_interactive.py   # 対話形式実行
│   ├── main_file.py          # ファイル入力一括実行
│   └── modules/
│       ├── graphrag_engine.py  # GraphRAGエンジン
│       ├── rag_engine.py       # ベクターRAGエンジン（ChromaDB）
│       ├── report.py           # レポート生成
│       └── models.py           # モデル設定
├── data/
│   ├── small/    # 3エンジニア, 3バグ（1ホップ検証向け）
│   ├── medium/   # 10エンジニア, 30バグ（2ホップ検証向け）
│   └── large/    # 30エンジニア, 100バグ（3+ホップ検証向け）
├── prompts/
│   ├── simple.txt    # 1ホップ以内の単純クエリ
│   ├── medium.txt    # 2ホップ程度のクエリ
│   └── multihop.txt  # 3ホップ以上の複雑クエリ
├── docs/
│   ├── minutes/   # セッション議事録
│   └── reports/   # 実行レポート（自動生成）
└── docker-compose.yml
```

## グラフ構造

```
(Bug)-[:ASSIGNED_TO]->(Engineer)-[:MEMBER_OF]->(Team)-[:BELONGS_TO]->(Department)
(Bug)-[:FOUND_IN]->(Module)-[:PART_OF]->(Project)
(Bug)-[:BLOCKS]->(Release)-[:BELONGS_TO]->(Project)
```

## セットアップ

WSL またはホスト環境から `setup.sh` を実行するだけで完結します。

```bash
cd /path/to/llm-rag-trial
bash scripts/setup.sh
```

実行内容:
1. Python / pip / Ollama / Neo4j の接続確認
2. `.env` の自動生成（実行環境に合わせたホスト設定）
3. Python パッケージのインストール
4. メモリ確認 → 搭載 RAM に収まるモデルのみ pull
5. Neo4j へのグラフデータロード（データサイズを対話選択）

> **ホスト自動切替について**
> Docker コンテナ内から実行する場合は `host.docker.internal`、
> WSL / ホスト直実行の場合は `localhost` が `.env` と接続先に自動設定されます。
> 既存の `.env` とズレがある場合は修正確認プロンプトが表示されます。

## 実行方法

### 全パターン一括実行（推奨）

```bash
bash scripts/run_all.sh
```

モデル・データサイズ・クエリ種別・モードを対話選択し、全組み合わせを順に実行します。
メモリに収まらないモデルは自動的に選択肢から除外されます。

### シナリオ単位で実行

```bash
python app/run_scenario.py \
    --prompt-file prompts/multihop.txt \
    --mode both \
    --model qwen-small \
    --data-dir data/large \
    --scenario-name "multihop_large_qwen-small"
```

## モデル設定

| キー | モデル名 | サイズ | 用途 |
|------|----------|--------|------|
| `small` | llama3.2 | ~2GB | 汎用軽量・ベースライン |
| `qwen-small` | qwen2.5-coder:7b | ~4.7GB | Cypher/コード特化・軽量 |
| `qwen-large` | qwen2.5-coder:14b | ~9GB | Cypher/コード特化・高精度 |
| `large` | gemma2:27b | ~15GB | 汎用高精度 |

GraphRAG の Cypher 生成精度向上には `qwen-small` または `qwen-large` を推奨。
モデルは `app/modules/models.py` の `MODEL_CONFIG` で追加・変更可能。

## レポート

各実行後に `docs/reports/` へMarkdownレポートが自動生成されます。
レポートには実行日時・プロンプト・回答・経過時間・トークン数が含まれます。
