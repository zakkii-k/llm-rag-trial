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

```bash
# 1. Dockerコンテナ起動
docker-compose up -d

# 2. Ollamaモデルのダウンロード
docker exec kg-ollama ollama pull llama3.2
docker exec kg-ollama ollama pull llama3.1:8b
docker exec kg-ollama ollama pull nomic-embed-text  # RAG用埋め込みモデル

# 3. Pythonパッケージのインストール
pip install -r requirements.txt

# 4. ナレッジグラフの構築（データサイズを選択）
python app/build_kg.py --data-dir data/small --clear
# python app/build_kg.py --data-dir data/medium --clear
# python app/build_kg.py --data-dir data/large --clear
```

## 実行方法

### 対話形式

```bash
# GraphRAG + RAG 両方、軽量モデル、smallデータ
python app/main_interactive.py --mode both --model small --data-dir data/small

# GraphRAGのみ、大型モデル、largeデータ
python app/main_interactive.py --mode graphrag --model large --data-dir data/large
```

### ファイル入力（一括実行）

```bash
# マルチホップクエリをGraphRAG/RAG両方で実行
python app/main_file.py \
    --prompt-file prompts/multihop.txt \
    --mode both \
    --model large \
    --data-dir data/large
```

## モデル設定

| キー | モデル名 | サイズ | 用途 |
|------|----------|--------|------|
| small | llama3.2 | ~2GB | 軽量・高速比較 |
| large | llama3.1:8b | ~4.7GB | 高精度比較 |

モデルは `app/modules/models.py` の `MODEL_CONFIG` で変更可能。

## レポート

各実行後に `docs/reports/` へMarkdownレポートが自動生成されます。
レポートには実行日時・プロンプト・回答・経過時間・トークン数が含まれます。
