# セットアップ・実行手順

## 目次

1. [前提条件](#1-前提条件)
2. [初回セットアップ](#2-初回セットアップ)
3. [環境構築（setup.sh）](#3-環境構築setupsh)
4. [全パターン実行（run_all.sh）](#4-全パターン実行run_allsh)
5. [シナリオ単体実行](#5-シナリオ単体実行)
6. [Gemini API の使い方](#6-gemini-api-の使い方)
7. [レポートの確認](#7-レポートの確認)
8. [トラブルシューティング](#8-トラブルシューティング)

---

## 1. 前提条件

| ツール | 最低バージョン | 確認コマンド |
|--------|--------------|------------|
| Docker Desktop (Windows/Mac) または Docker Engine (Linux) | 24.x 以上 | `docker --version` |
| Docker Compose | v2.x 以上 | `docker compose version` |
| Python | 3.11 以上 | `python3 --version` |
| Git | 任意 | `git --version` |

**WSL2 (Windows) の場合**: Docker Desktop の「Settings → Resources → WSL Integration」で使用する WSL ディストリビューションを有効にしてください。

---

## 2. 初回セットアップ

### 2-1. リポジトリを取得

```bash
git clone <リポジトリURL>
cd llm-rag-trial
```

### 2-2. bootstrap.sh を実行（初回のみ）

```bash
bash scripts/bootstrap.sh
```

以下を自動で行います:

1. Docker / Python3 の存在確認
2. `.env` ファイルの生成（ない場合）
3. `docker-compose up -d` でコンテナ起動
4. Neo4j / Ollama の起動待機（最大60秒）
5. `scripts/setup.sh` を呼び出してモデル pull とデータロード

> **2回目以降**は `bash scripts/setup.sh` のみで OK です。

---

## 3. 環境構築（setup.sh）

```bash
bash scripts/setup.sh
```

### ステップ詳細

| ステップ | 内容 |
|---------|------|
| 1. .env 確認・修正 | 実行環境（Docker/WSL）を検出し `.env` のホスト設定を確認。ズレがあれば修正提案 |
| 2. Python / pip 確認 | Python3 と pip の存在確認 |
| 3. 接続確認 | Ollama・Neo4j への接続テスト |
| 4. パッケージインストール | `pip install -r requirements.txt` |
| 5. モデル pull | 利用可能 RAM を確認し、収まるモデルのみ選択肢に表示。APIモデルは API キー確認のみ |
| 6. グラフデータロード | `data/small` `data/medium` `data/large` から選択して Neo4j に投入 |
| 7. 動作確認 | Neo4j / Ollama / ChromaDB の疎通スモークテスト |

### .env の設定項目

```bash
# Docker コンテナ内から実行する場合（デフォルト）
NEO4J_URI=bolt://host.docker.internal:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password        # 任意のパスワードに変更推奨
OLLAMA_BASE_URL=http://host.docker.internal:11434

# Gemini API を使う場合
GOOGLE_API_KEY=your_api_key_here
```

> `setup.sh` は実行環境（Docker 内 / WSL）を自動検出して `host.docker.internal` か `localhost` を選択します。既存の `.env` とズレがある場合は修正確認プロンプトが表示されます。

### Neo4j ブラウザで確認

コンテナ起動後、`http://localhost:7474` を開いてログイン:
- ユーザー名: `neo4j`
- パスワード: `.env` の `NEO4J_PASSWORD`

---

## 4. 全パターン実行（run_all.sh）

```bash
bash scripts/run_all.sh
```

対話形式で以下を選択し、全組み合わせを順に実行します。

```
【1/4】使用するモデルを選択
  1) llama3.2           (~2GB)    汎用軽量
  2) qwen2.5-coder:7b   (~4.7GB)  Cypher特化・軽量
  ...
  番号をスペース区切りで入力、all で全選択:

【2/4】データサイズを選択
  1) small   — Bug×3,  Engineer×3
  2) medium  — Bug×30, Engineer×10
  3) large   — Bug×100,Engineer×30

【3/4】クエリ種別を選択
  1) simple   — 単一エンティティの基本クエリ
  2) medium   — 複数エンティティ・集計クエリ
  3) multihop — 3ホップ以上の複合クエリ

【4/4】実行モードを選択
  1) both     — GraphRAG と RAG を両方実行
  2) graphrag — GraphRAG のみ
  3) rag      — RAG のみ
```

メモリ不足のモデルは自動的に選択肢から除外されます。API キー未設定の Gemini モデルも除外されます。

---

## 5. シナリオ単体実行

```bash
python3 app/run_scenario.py \
    --prompt-file prompts/multihop.txt \
    --mode both \
    --model qwen3-small \
    --data-dir data/large \
    --scenario-name "multihop_large_qwen3"
```

### オプション一覧

| オプション | 値 | デフォルト |
|-----------|-----|----------|
| `--prompt-file` | プロンプトファイルパス | 必須 |
| `--mode` | `rag` / `graphrag` / `both` | `both` |
| `--model` | モデルキー（下表参照） | `small` |
| `--data-dir` | `data/small` 等 | `data/small` |
| `--n-results` | RAG取得ドキュメント数 | `5` |
| `--scenario-name` | レポートファイル名に使用 | `scenario` |

### モデルキー一覧

| キー | モデル | サイズ |
|------|--------|--------|
| `small` | llama3.2 | ~2GB |
| `qwen-small` | qwen2.5-coder:7b | ~4.7GB |
| `qwen-large` | qwen2.5-coder:14b | ~9GB |
| `qwen-coder-32b` | qwen2.5-coder:32b | ~20GB |
| `qwen3-small` | qwen3:8b | ~5.2GB |
| `qwen3-medium` | qwen3:14b | ~9.3GB |
| `qwen3-large` | qwen3:32b | ~18.8GB |
| `qwen35-small` | qwen3.5:4b | ~3GB |
| `qwen35-medium` | qwen3.5:9b | ~6GB |
| `qwen35-large` | qwen3.5:27b | ~16GB |
| `large` | gemma2:27b | ~15GB |
| `gemini-flash` | gemini-1.5-flash | API |
| `gemini-pro` | gemini-1.5-pro | API |

### プロンプトファイルの形式

```text
# コメント行（# で始まる行は無視）
criticalなバグは何件ありますか？
Backendチームが担当するバグを教えてください。
v1.0リリースをブロックしているバグとその担当者を教えてください。
```

---

## 6. Gemini API の使い方

### APIキーの取得

[Google AI Studio](https://aistudio.google.com/) で API キーを取得してください（無料枠あり）。

### .env への設定

```bash
echo "GOOGLE_API_KEY=your_api_key_here" >> .env
```

### 利用制限（無料枠）

| モデル | RPM | RPD | TPM |
|--------|-----|-----|-----|
| gemini-1.5-flash | 15 | 1,500 | 1,000,000 |
| gemini-1.5-pro | 2 | 50 | 32,000 |

各クエリ実行後、残りの利用可能上限が標準出力に表示されます（レポートには含まれません）。

```
  [Gemini quota] RPM残り: 14/15  RPD残り: 1499/1500  TPM残り(概算): 999,500/1,000,000
```

---

## 7. レポートの確認

実行後、`docs/reports/` に Markdown レポートが自動生成されます。

```
docs/reports/
├── 20260403_120000_simple_small_qwen3-small_graphrag.md
├── 20260403_120015_simple_small_qwen3-small_rag.md
└── ...
```

### レポート内容

| 項目 | 内容 |
|------|------|
| 実行日時・モデル・データ | 実行条件サマリ |
| プロンプト | 入力した質問 |
| 回答 | LLM の回答テキスト |
| 生成 Cypher クエリ | GraphRAG のみ |
| Cypher 実行結果 | GraphRAG のみ |
| リトライ履歴 | 失敗時のエラーと修正過程（最大3回） |
| 経過時間 | 秒 |
| トークン数 | 入力 / 出力 |

---

## 8. トラブルシューティング

### Docker 関連

| 症状 | 対処 |
|------|------|
| `docker compose up` が失敗する | `NEO4J_PASSWORD` が `.env` に設定されているか確認 |
| Neo4j に接続できない | 起動直後は30秒ほど待つ。`docker ps` でコンテナ状態を確認 |
| Ollama に接続できない | `docker ps \| grep ollama` でコンテナが `Up` になっているか確認 |

### 実行環境・ホスト名

| 症状 | 対処 |
|------|------|
| WSLから実行時に接続できない | `.env` の `*_URI` / `*_URL` のホスト部分が `localhost` になっているか確認 |
| Docker内から実行時に接続できない | ホスト部分が `host.docker.internal` になっているか確認 |
| どちらかわからない | `setup.sh` を実行すると自動検出・修正提案してくれます |

### Python / パッケージ

| 症状 | 対処 |
|------|------|
| `NEO4J_PASSWORD 環境変数を設定してください` | プロジェクトルートから実行しているか確認。`.env` が存在するか確認 |
| `ModuleNotFoundError` | `pip install -r requirements.txt --break-system-packages` を再実行 |
| ChromaDB エラー | `pip install chromadb --break-system-packages` |

### モデル pull

| 症状 | 対処 |
|------|------|
| pull が失敗する | Ollama コンテナが起動しているか確認。ディスク空き容量を確認 |
| pull 中断後、状態が壊れる | `docker exec kg-ollama ollama rm <model>` で削除してから再 pull |
| メモリ不足で選択できない | 不要なプロセスを終了して RAM を確保するか、より小さいモデルを選択 |

### Gemini API

| 症状 | 対処 |
|------|------|
| `GOOGLE_API_KEY が無効` | API キーを再確認。Google AI Studio で有効になっているか確認 |
| RPM 制限エラー | gemini-1.5-pro は RPM=2 なので、クエリ間に間隔が必要 |
