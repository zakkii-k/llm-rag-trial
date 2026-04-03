#!/usr/bin/env bash
# =============================================================================
# bootstrap.sh — 新規ユーザー向け初回セットアップスクリプト
#
# 使い方:
#   git clone <repo>
#   cd llm-rag-trial
#   bash scripts/bootstrap.sh
#
# 実行内容:
#   1. 前提条件チェック（Docker, Python3）
#   2. .env ファイルの生成
#   3. docker-compose up -d でコンテナ起動
#   4. Neo4j / Ollama の起動待機
#   5. scripts/setup.sh を呼び出し（モデルpull・データロード）
# =============================================================================

set -euo pipefail
cd "$(dirname "$0")/.."

# ── カラー定義 ────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; DIM='\033[2m'; RESET='\033[0m'

step() { echo -e "\n${BOLD}${CYAN}▶ $*${RESET}"; }
ok()   { echo -e "  ${GREEN}✅ $*${RESET}"; }
warn() { echo -e "  ${YELLOW}⚠️  $*${RESET}"; }
fail() { echo -e "  ${RED}❌ $*${RESET}"; }
info() { echo -e "  ${DIM}   $*${RESET}"; }

# ── ヘッダー ──────────────────────────────────────────────────────────────────
clear
echo -e "${BOLD}============================================================${RESET}"
echo -e "${BOLD}     初回セットアップ — bootstrap.sh${RESET}"
echo -e "${BOLD}============================================================${RESET}"
echo ""
echo -e "  このスクリプトは以下を自動で行います:"
echo -e "    1. 前提条件チェック（Docker, Python3）"
echo -e "    2. .env ファイルの生成"
echo -e "    3. Docker コンテナの起動（Neo4j + Ollama）"
echo -e "    4. 各サービスの起動待機"
echo -e "    5. setup.sh の呼び出し（モデルpull・データロード）"
echo ""

# ──────────────────────────────────────────────────────────────────────────────
# 1. 前提条件チェック
# ──────────────────────────────────────────────────────────────────────────────
step "前提条件チェック"

# Docker
if ! command -v docker &>/dev/null; then
    fail "Docker が見つかりません"
    echo ""
    echo -e "  ${BOLD}Docker のインストール方法:${RESET}"
    echo -e "  ${CYAN}Windows / Mac${RESET}: https://www.docker.com/products/docker-desktop/"
    echo -e "  ${CYAN}Ubuntu/Debian${RESET}:"
    echo -e "    curl -fsSL https://get.docker.com | bash"
    echo -e "    sudo usermod -aG docker \$USER   # ログインし直してから反映"
    echo ""
    echo -e "  インストール後、このスクリプトを再実行してください。"
    exit 1
fi
ok "Docker: $(docker --version | cut -d' ' -f3 | tr -d ',')"

# Docker Compose（v2: "docker compose"、v1: "docker-compose"）
if docker compose version &>/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose &>/dev/null; then
    COMPOSE_CMD="docker-compose"
else
    fail "Docker Compose が見つかりません"
    info "Docker Desktop をインストールすると Compose も含まれます"
    exit 1
fi
ok "Docker Compose: $($COMPOSE_CMD version --short 2>/dev/null || echo 'ok')"

# Docker デーモン起動確認
if ! docker info &>/dev/null; then
    fail "Docker デーモンが起動していません"
    echo ""
    echo -e "  ${BOLD}起動方法:${RESET}"
    echo -e "  ${CYAN}Windows / Mac${RESET}: Docker Desktop を起動してください"
    echo -e "  ${CYAN}Linux${RESET}:          sudo systemctl start docker"
    exit 1
fi
ok "Docker デーモン: 起動中"

# Python3
if ! command -v python3 &>/dev/null; then
    fail "Python3 が見つかりません"
    echo ""
    echo -e "  ${BOLD}Python3 のインストール方法:${RESET}"
    echo -e "  ${CYAN}Ubuntu/Debian${RESET}: sudo apt install python3 python3-pip"
    echo -e "  ${CYAN}Windows (WSL)${RESET}: sudo apt install python3 python3-pip"
    echo -e "  ${CYAN}Mac${RESET}:            brew install python3"
    exit 1
fi
ok "Python3: $(python3 --version)"

# ──────────────────────────────────────────────────────────────────────────────
# 2. .env ファイルの生成
# ──────────────────────────────────────────────────────────────────────────────
step ".env ファイルの確認・生成"

if [[ -f .env ]]; then
    ok ".env は既に存在します"
    info "既存の .env を使用します（編集が必要な場合は直接編集してください）"
else
    echo -e "  Neo4j のパスワードを設定してください（空Enterでデフォルト 'password' を使用）:"
    printf "  NEO4J_PASSWORD > "
    read -r neo4j_pass
    neo4j_pass="${neo4j_pass:-password}"

    # WSL / Docker どちらから実行するか確認
    echo ""
    echo -e "  このプロジェクトを実行する環境を選択してください:"
    echo -e "    1) WSL またはホスト（推奨）  → localhost"
    echo -e "    2) Docker コンテナ内         → host.docker.internal"
    printf "  > "
    read -r env_choice
    if [[ "$env_choice" == "2" ]]; then
        DEFAULT_HOST="host.docker.internal"
    else
        DEFAULT_HOST="localhost"
    fi

    cat > .env <<ENV
# 自動生成 (bootstrap.sh)
NEO4J_PASSWORD=${neo4j_pass}
NEO4J_URI=bolt://${DEFAULT_HOST}:7687
NEO4J_USER=neo4j
OLLAMA_BASE_URL=http://${DEFAULT_HOST}:11434

# Google Gemini API を使う場合は以下のコメントを外して API キーを設定
# GOOGLE_API_KEY=your_api_key_here
ENV
    ok ".env を生成しました (ホスト: ${DEFAULT_HOST})"
fi

# .env を読み込む
set -a && source .env && set +a

# ──────────────────────────────────────────────────────────────────────────────
# 3. Docker コンテナの起動
# ──────────────────────────────────────────────────────────────────────────────
step "Docker コンテナの起動"

echo -e "  ${DIM}$COMPOSE_CMD up -d${RESET}"
if ! $COMPOSE_CMD up -d; then
    fail "docker-compose up に失敗しました"
    info "docker-compose.yml が存在するか、ポート 7474 / 7687 / 11434 が使用中でないか確認してください"
    exit 1
fi
ok "コンテナを起動しました"

# ──────────────────────────────────────────────────────────────────────────────
# 4. サービスの起動待機
# ──────────────────────────────────────────────────────────────────────────────
step "サービスの起動待機"

OLLAMA_URL="${OLLAMA_BASE_URL:-http://localhost:11434}"
NEO4J_URI_VAL="${NEO4J_URI:-bolt://localhost:7687}"
NEO4J_PASS_VAL="${NEO4J_PASSWORD:-password}"
NEO4J_USER_VAL="${NEO4J_USER:-neo4j}"

# Ollama 待機（最大60秒）
echo -e "  Ollama の起動を待機中..."
WAIT=0
until curl -sf "${OLLAMA_URL}/api/tags" &>/dev/null; do
    if (( WAIT >= 60 )); then
        fail "Ollama が60秒以内に起動しませんでした"
        info "docker ps でコンテナ状態を確認してください"
        exit 1
    fi
    printf "."
    sleep 3
    WAIT=$((WAIT + 3))
done
echo ""
ok "Ollama: 起動確認 (${OLLAMA_URL})"

# Neo4j 待機（最大90秒、起動に時間がかかることがある）
echo -e "  Neo4j の起動を待機中..."
WAIT=0
until python3 -c "
from neo4j import GraphDatabase
try:
    d = GraphDatabase.driver('${NEO4J_URI_VAL}', auth=('${NEO4J_USER_VAL}', '${NEO4J_PASS_VAL}'))
    d.verify_connectivity()
    d.close()
except: exit(1)
" 2>/dev/null; do
    if (( WAIT >= 90 )); then
        warn "Neo4j が90秒以内に起動しませんでした"
        info "setup.sh 内で再確認します。このまま続行します..."
        break
    fi
    printf "."
    sleep 5
    WAIT=$((WAIT + 5))
done
echo ""
ok "Neo4j: 起動確認 (${NEO4J_URI_VAL})"

# ──────────────────────────────────────────────────────────────────────────────
# 5. setup.sh へ引き継ぎ
# ──────────────────────────────────────────────────────────────────────────────
step "setup.sh を呼び出します"

echo ""
echo -e "  ${DIM}Dockerコンテナが起動しました。${RESET}"
echo -e "  ${DIM}引き続き setup.sh でモデルのpullとデータロードを行います。${RESET}"
echo ""

bash scripts/setup.sh

# ── 完了 ─────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}============================================================${RESET}"
echo -e "${BOLD} 初回セットアップ完了 ✅${RESET}"
echo -e "${BOLD}============================================================${RESET}"
echo ""
echo -e "  次回以降は以下のコマンドで実行できます:"
echo ""
echo -e "  ${BOLD}# 全パターン一括実行${RESET}"
echo -e "  bash scripts/run_all.sh"
echo ""
echo -e "  ${BOLD}# コンテナ再起動が必要な場合${RESET}"
echo -e "  $COMPOSE_CMD up -d && bash scripts/setup.sh"
echo ""
