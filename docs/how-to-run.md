# 実行手順

## 前提条件

- Docker / Docker Compose が使える状態
- Python 3.11 以上
- WSL または Linux 環境

---

## 1. 環境構築

### 1-1. コンテナ起動

```bash
cd /path/to/project   # このリポジトリのルート

# .env が存在することを確認（パスワードが設定されていること）
cat .env
# → NEO4J_PASSWORD=password  ← 任意のパスワードに変更推奨

docker-compose up -d
```

### 1-2. Ollama モデルのダウンロード

```bash
# 軽量モデル（~2GB）
docker exec kg-ollama ollama pull llama3.2

# 高精度モデル（~4.7GB）
docker exec kg-ollama ollama pull llama3.1:8b

# RAG用埋め込みモデル（~274MB）
docker exec kg-ollama ollama pull nomic-embed-text
```

ダウンロード確認：
```bash
docker exec kg-ollama ollama list
```

### 1-3. Python パッケージのインストール

```bash
pip install -r requirements.txt
```

---

## 2. ナレッジグラフの構築

```bash
# small データセット（デフォルト、1〜2ホップ検証向け）
python app/build_kg.py --data-dir data/small --clear

# medium データセット（2〜3ホップ検証向け）
python app/build_kg.py --data-dir data/medium --clear

# large データセット（3+ホップ、本格検証向け）
python app/build_kg.py --data-dir data/large --clear
```

> `--clear` をつけると既存グラフを削除してから投入します。切り替え時は必ずつけてください。

Neo4j ブラウザ（`http://localhost:7474`）で確認できます。ログイン: `neo4j` / `.env` のパスワード

---

## 3. RAG / GraphRAG の実行

### オプション一覧

| オプション | 値 | 説明 |
|-----------|-----|------|
| `--mode` | `rag` / `graphrag` / `both` | 実行モード |
| `--model` | `small` / `large` | LLMモデル選択 |
| `--data-dir` | `data/small` 等 | 使用データセット |
| `--n-results` | 整数（デフォルト 5） | RAGの取得ドキュメント数 |

### 3-1. 対話形式（`main_interactive.py`）

```bash
# GraphRAG + RAG 両方を軽量モデルで試す
python app/main_interactive.py --mode both --model small --data-dir data/small

# GraphRAGのみ、高精度モデル
python app/main_interactive.py --mode graphrag --model large --data-dir data/large

# RAGのみ
python app/main_interactive.py --mode rag --model small --data-dir data/medium
```

実行後、`質問>` プロンプトが表示されるので日本語で質問を入力してください。
終了するには `exit` を入力するか `Ctrl+C` を押します。

### 3-2. ファイル入力（`main_file.py`）

プロンプトファイルに記載した質問をまとめて実行します。

```bash
# シンプルクエリを両モードで比較（smallデータ）
python app/main_file.py \
    --prompt-file prompts/simple.txt \
    --mode both \
    --model small \
    --data-dir data/small

# マルチホップクエリを高精度モデルで両モード比較（largeデータ）
python app/main_file.py \
    --prompt-file prompts/multihop.txt \
    --mode both \
    --model large \
    --data-dir data/large
```

**プロンプトファイルの形式:**
```text
# コメント行（#で始まる行は無視）
criticalなバグは何件ありますか？
Backendチームが担当するバグを教えてください。
```

---

## 4. レポートの確認

実行後、`docs/reports/` にMarkdownレポートが自動生成されます。

```
docs/reports/
├── 20260401_120000_graphrag_llama3.2.md
├── 20260401_120015_rag_llama3.2.md
└── ...
```

各レポートの内容：

| 項目 | 内容 |
|------|------|
| 実行日時 | タイムスタンプ |
| モード | rag / graphrag / both |
| モデル | 使用したOllamaモデル名 |
| データソース | 使用したデータディレクトリ |
| プロンプト | 入力した質問 |
| 生成Cypherクエリ | GraphRAGのみ |
| Cypher実行結果 | GraphRAGのみ |
| 回答 | LLMの回答テキスト |
| 回答時間 | 秒 |
| 入力トークン | Ollamaメタデータより |
| 出力トークン | Ollamaメタデータより |

---

## 5. 比較検証のおすすめシナリオ

### シナリオA: モデルサイズの比較

同じクエリ・同じデータで small vs large を比較する。

```bash
# small モデル
python app/main_file.py --prompt-file prompts/medium.txt --mode graphrag --model small --data-dir data/medium

# large モデル
python app/main_file.py --prompt-file prompts/medium.txt --mode graphrag --model large --data-dir data/medium
```

### シナリオB: RAG vs GraphRAG の比較

同じクエリ・同じモデルで mode を切り替える。

```bash
python app/main_file.py --prompt-file prompts/multihop.txt --mode both --model small --data-dir data/large
```

### シナリオC: データ量による精度変化

同じクエリを small / medium / large で比較する。

```bash
for dir in small medium large; do
    python app/main_file.py \
        --prompt-file prompts/simple.txt \
        --mode graphrag --model small \
        --data-dir data/$dir
done
```

> ⚠️ データを切り替えるたびに `build_kg.py --clear` でグラフを再構築してください。

---

## 6. モデルのカスタマイズ

`app/modules/models.py` の `MODEL_CONFIG` を編集することで他のOllamaモデルに変更できます。

```python
MODEL_CONFIG = {
    "small": {
        "name": "llama3.2",          # ← 変更可能
        "description": "...",
    },
    "large": {
        "name": "llama3.1:8b",       # ← 変更可能
        "description": "...",
    },
}
```

使用可能なモデルの確認：
```bash
docker exec kg-ollama ollama list
```

RAG用の埋め込みモデルは `EMBEDDING_MODEL = "nomic-embed-text"` で指定しています。

---

## トラブルシューティング

| 症状 | 原因と対処 |
|------|-----------|
| `NEO4J_PASSWORD 環境変数を設定してください` | `.env` ファイルが読み込まれていない。プロジェクトルートから実行しているか確認 |
| Ollama接続エラー | `docker-compose up -d` でコンテナが起動しているか確認。`OLLAMA_BASE_URL` 環境変数で URL を変更可 |
| ChromaDBのエラー | `pip install chromadb` が完了しているか確認 |
| Neo4j接続エラー | コンテナ起動直後は30秒ほど待ってから実行 |
