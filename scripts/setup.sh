#!/usr/bin/env bash
# =============================================================================
# setup.sh — 環境構築スクリプト
#
# 使い方:
#   cd /path/to/llm-rag-trial
#   bash scripts/setup.sh
#
# 実行順序:
#   1. 実行環境検出 + .env 確認・修正  ← 接続確認より先に行う
#   2. Python / pip 確認
#   3. Ollama / Neo4j 接続確認
#   4. Python 依存パッケージのインストール
#   5. メモリ確認 → 利用可能なモデルのみ pull
#   6. Neo4j グラフデータのロード
# =============================================================================

set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/_common.sh

# ── ユーティリティ ────────────────────────────────────────────────────────────
step() { echo -e "\n${BOLD}${CYAN}▶ $*${RESET}"; }
ok()   { echo -e "  ${GREEN}✅ $*${RESET}"; }
warn() { echo -e "  ${YELLOW}⚠️  $*${RESET}"; }
fail() { echo -e "  ${RED}❌ $*${RESET}"; }
info() { echo -e "  ${DIM}   $*${RESET}"; }

# ── 環境検出 ──────────────────────────────────────────────────────────────────
DETECTED_HOST=$(detect_host)
ENV_LABEL=$(detect_env_label)

# ── ヘッダー ─────────────────────────────────────────────────────────────────
clear
echo -e "${BOLD}============================================================${RESET}"
echo -e "${BOLD}     環境構築スクリプト — setup.sh${RESET}"
echo -e "${BOLD}============================================================${RESET}"
echo -e "  実行環境: ${BOLD}${ENV_LABEL}${RESET}  (推奨ホスト: ${DETECTED_HOST})"
echo ""

# ──────────────────────────────────────────────────────────────────────────────
# 1. .env 確認・修正（接続確認より先に実施）
# ──────────────────────────────────────────────────────────────────────────────
step ".env ファイルの確認・修正"

if [[ ! -f .env ]]; then
    warn ".env が見つかりません。${ENV_LABEL} 向けの設定で作成します。"
    cat > .env <<ENV
# 自動生成 (setup.sh) — 実行環境: ${ENV_LABEL}
NEO4J_PASSWORD=password
NEO4J_URI=bolt://${DETECTED_HOST}:7687
NEO4J_USER=neo4j
OLLAMA_BASE_URL=http://${DETECTED_HOST}:11434
ENV
    ok ".env を作成しました (ホスト: ${DETECTED_HOST})"
    info "Neo4j のパスワードが異なる場合は .env を編集してください"
fi

# .env を読み込む
set -a && source .env && set +a

# .env のホスト部分を抽出して検出環境と比較
ACTUAL_OLLAMA_HOST=$(echo "${OLLAMA_BASE_URL:-}" | sed 's|https\?://||;s|:.*||')
ACTUAL_NEO4J_HOST=$(echo "${NEO4J_URI:-}"        | sed 's|bolt://||;s|:.*||')

MISMATCH=0
[[ -n "$ACTUAL_OLLAMA_HOST" && "$ACTUAL_OLLAMA_HOST" != "$DETECTED_HOST" ]] && MISMATCH=1
[[ -n "$ACTUAL_NEO4J_HOST"  && "$ACTUAL_NEO4J_HOST"  != "$DETECTED_HOST" ]] && MISMATCH=1

if (( MISMATCH )); then
    warn ".env のホストが実行環境と一致していません。"
    info "  実行環境の推奨ホスト : ${DETECTED_HOST}"
    info "  .env の Ollama ホスト: ${ACTUAL_OLLAMA_HOST:-未設定}"
    info "  .env の Neo4j ホスト : ${ACTUAL_NEO4J_HOST:-未設定}"
    echo ""
    printf "  .env を ${DETECTED_HOST} に合わせて自動修正しますか？ [Y/n]: "
    read -r fix_env
    if [[ ! "$fix_env" =~ ^[Nn]$ ]]; then
        NEO4J_PASSWORD_CURRENT="${NEO4J_PASSWORD:-password}"
        cat > .env <<ENV
# 自動修正 (setup.sh) — 実行環境: ${ENV_LABEL}
NEO4J_PASSWORD=${NEO4J_PASSWORD_CURRENT}
NEO4J_URI=bolt://${DETECTED_HOST}:7687
NEO4J_USER=${NEO4J_USER:-neo4j}
OLLAMA_BASE_URL=http://${DETECTED_HOST}:11434
ENV
        set -a && source .env && set +a
        ok ".env を ${DETECTED_HOST} 向けに更新しました"
    else
        warn "既存の .env をそのまま使用します"
    fi
else
    ok ".env のホスト設定は実行環境と一致しています (${DETECTED_HOST})"
fi

# 接続先を確定（.env 優先、未設定なら検出ホスト）
NEO4J_URI="${NEO4J_URI:-bolt://${DETECTED_HOST}:7687}"
NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:-password}"
OLLAMA_URL="${OLLAMA_BASE_URL:-http://${DETECTED_HOST}:11434}"

# ──────────────────────────────────────────────────────────────────────────────
# 2. Python / pip 確認
# ──────────────────────────────────────────────────────────────────────────────
step "Python / pip 確認"

if python3 --version &>/dev/null; then
    ok "Python: $(python3 --version)"
else
    fail "Python3 が見つかりません"
    exit 1
fi

if python3 -m pip --version &>/dev/null; then
    ok "pip: 利用可能"
else
    warn "pip が見つかりません。インストールを試みます..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3 - --break-system-packages
fi

# ──────────────────────────────────────────────────────────────────────────────
# 3. 接続確認（修正済み .env の値で試す）
# ──────────────────────────────────────────────────────────────────────────────
step "接続確認"

# Ollama
if curl -sf "${OLLAMA_URL}/api/tags" &>/dev/null; then
    ok "Ollama: ${OLLAMA_URL}"
else
    fail "Ollama に接続できません: ${OLLAMA_URL}"
    info "Ollama が起動しているか、.env の OLLAMA_BASE_URL を確認してください"
    exit 1
fi

# Neo4j（neo4j パッケージがまだ入っていない場合は pip install してから再試行）
check_neo4j() {
    python3 - <<PYEOF 2>/dev/null
from neo4j import GraphDatabase
d = GraphDatabase.driver("${NEO4J_URI}", auth=("${NEO4J_USER}", "${NEO4J_PASSWORD}"))
d.verify_connectivity()
d.close()
PYEOF
}

if check_neo4j; then
    ok "Neo4j: ${NEO4J_URI}"
else
    # neo4j パッケージ未インストールの可能性 → 先にインストールして再試行
    warn "Neo4j 接続失敗。パッケージをインストールして再試行します..."
    python3 -m pip install "neo4j>=5.0" --break-system-packages -q 2>/dev/null || true
    if check_neo4j; then
        ok "Neo4j: ${NEO4J_URI} (パッケージインストール後に接続成功)"
    else
        fail "Neo4j に接続できません: ${NEO4J_URI}"
        info "Neo4j が起動しているか確認してください"
        info "  docker ps | grep neo4j  でコンテナの状態を確認"
        info "  .env の NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD を確認"
        exit 1
    fi
fi

# ──────────────────────────────────────────────────────────────────────────────
# 4. Python 依存パッケージのインストール
# ──────────────────────────────────────────────────────────────────────────────
step "Python 依存パッケージのインストール"

if python3 -m pip install -r requirements.txt --break-system-packages -q; then
    ok "requirements.txt インストール完了"
else
    fail "pip install 失敗"
    exit 1
fi

# ──────────────────────────────────────────────────────────────────────────────
# 5. モデル pull（メモリ確認付き）
# ──────────────────────────────────────────────────────────────────────────────
step "Ollama モデルの pull"

AVAIL_MB=$(get_available_ram_mb)
echo -e "  利用可能 RAM: ${BOLD}${AVAIL_MB}MB${RESET}"
echo ""

PULLED_MODELS=$(curl -s "${OLLAMA_URL}/api/tags" | python3 -c "
import sys, json
for m in json.load(sys.stdin).get('models', []):
    print(m['name'])
" 2>/dev/null)

echo "  モデル別の状態:"
PULLABLE_INDICES=()

for i in "${!MODEL_KEYS[@]}"; do
    name="${MODEL_NAMES[$i]}"
    label="${MODEL_LABEL[$i]}"
    required="${MODEL_SIZE_MB[$i]}"

    already_pulled=0
    echo "$PULLED_MODELS" | grep -qF "$name"          && already_pulled=1
    echo "$PULLED_MODELS" | grep -qF "${name}:latest" && already_pulled=1

    if (( AVAIL_MB < required )); then
        printf "    ${DIM}-) %s  ${RED}[スキップ — メモリ不足: 必要%dMB / 空き%dMB]${RESET}\n" \
            "$label" "$required" "$AVAIL_MB"
    elif (( already_pulled )); then
        printf "    ${GREEN}✅ %s  [pull済み]${RESET}\n" "$label"
    else
        printf "    %d) %s  ${YELLOW}[未pull]${RESET}\n" $((i+1)) "$label"
        PULLABLE_INDICES+=("$i")
    fi
done

# 埋め込みモデル
EMBED_MODEL="nomic-embed-text"
embed_pulled=0
echo "$PULLED_MODELS" | grep -qF "$EMBED_MODEL" && embed_pulled=1

if (( embed_pulled )); then
    printf "    ${GREEN}✅ nomic-embed-text  [pull済み] (RAG用埋め込みモデル)${RESET}\n"
else
    printf "    ${YELLOW}   nomic-embed-text  [未pull] (RAG用埋め込みモデル — 必須)${RESET}\n"
    PULLABLE_INDICES+=("embed")
fi

if [[ ${#PULLABLE_INDICES[@]} -eq 0 ]]; then
    echo ""
    ok "全ての必要モデルが pull 済みです。"
else
    echo ""
    MODELS_TO_PULL=()
    for i in "${PULLABLE_INDICES[@]}"; do
        if [[ "$i" == "embed" ]]; then
            MODELS_TO_PULL+=("$EMBED_MODEL")
        else
            MODELS_TO_PULL+=("${MODEL_NAMES[$i]}")
        fi
    done

    echo -e "  以下を pull します:"
    for m in "${MODELS_TO_PULL[@]}"; do
        echo -e "    - ${m}"
    done
    echo ""
    printf "  続けますか？ [Y/n]: "
    read -r confirm
    if [[ "$confirm" =~ ^[Nn]$ ]]; then
        warn "モデル pull をスキップしました。"
    else
        for m in "${MODELS_TO_PULL[@]}"; do
            pull_model "$m" || warn "${m} の pull に失敗しました。後で再試行してください。"
        done
    fi
fi

# ──────────────────────────────────────────────────────────────────────────────
# 6. Neo4j グラフデータのロード
# ──────────────────────────────────────────────────────────────────────────────
step "Neo4j グラフデータのロード"

EXISTING_COUNT=$(python3 - <<PYEOF 2>/dev/null || echo "0"
from neo4j import GraphDatabase
d = GraphDatabase.driver("${NEO4J_URI}", auth=("${NEO4J_USER}", "${NEO4J_PASSWORD}"))
with d.session() as s:
    print(s.run("MATCH (n) RETURN count(n) AS cnt").single()["cnt"])
d.close()
PYEOF
)

SKIP_LOAD=0
if (( EXISTING_COUNT > 0 )); then
    echo -e "  Neo4j に既存データがあります（ノード数: ${EXISTING_COUNT}）"
    printf "  上書きしますか？ [y/N]: "
    read -r overwrite
    [[ "$overwrite" =~ ^[Yy]$ ]] || SKIP_LOAD=1
fi

if (( SKIP_LOAD == 0 )); then
    echo ""
    echo -e "  ロードするデータサイズを選択:"
    for i in "${!DATA_KEYS[@]}"; do
        printf "  %d) %s\n" $((i+1)) "${DATA_DESC[$i]}"
    done
    printf "  > "
    read -r data_choice

    DATA_IDX=$((data_choice - 1))
    if (( DATA_IDX < 0 || DATA_IDX >= ${#DATA_KEYS[@]} )); then
        warn "無効な選択。large を使用します。"
        DATA_IDX=2
    fi

    DATA_DIR="data/${DATA_KEYS[$DATA_IDX]}"
    echo ""
    echo -e "  ${DATA_DIR} をロード中..."
    if python3 app/build_kg.py --data-dir "$DATA_DIR" --clear; then
        ok "${DATA_DIR} のロード完了"
    else
        fail "グラフデータのロードに失敗しました"
        exit 1
    fi
else
    ok "既存データをそのまま使用します。"
fi

# ──────────────────────────────────────────────────────────────────────────────
# 7. スモークテスト
# ──────────────────────────────────────────────────────────────────────────────
step "動作確認"

python3 - <<PYEOF
import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv(dotenv_path='.env')
from app.modules.env_utils import get_neo4j_uri, get_ollama_url
from neo4j import GraphDatabase
import os, requests

errors = []

# Neo4j
try:
    d = GraphDatabase.driver(get_neo4j_uri(), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))
    with d.session() as s:
        cnt = s.run('MATCH (n) RETURN count(n) AS c').single()['c']
    d.close()
    print(f"  ✅ Neo4j: {cnt} ノード")
except Exception as e:
    errors.append(f"Neo4j: {e}")
    print(f"  ❌ Neo4j: {e}")

# Ollama
try:
    r = requests.get(get_ollama_url() + '/api/tags', timeout=5)
    models = [m['name'] for m in r.json()['models']]
    print(f"  ✅ Ollama: {len(models)} モデル")
except Exception as e:
    errors.append(f"Ollama: {e}")
    print(f"  ❌ Ollama: {e}")

# ChromaDB
try:
    import chromadb
    print(f"  ✅ ChromaDB: OK")
except Exception as e:
    errors.append(f"ChromaDB: {e}")
    print(f"  ❌ ChromaDB: {e}")

sys.exit(1 if errors else 0)
PYEOF

# ── 完了 ─────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}============================================================${RESET}"
echo -e "${BOLD} セットアップ完了 ✅${RESET}"
echo -e "${BOLD}============================================================${RESET}"
echo ""
echo -e "  次のコマンドで実行できます:"
echo -e "  ${BOLD}bash scripts/run_all.sh${RESET}"
echo ""
