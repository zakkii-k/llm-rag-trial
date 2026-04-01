#!/usr/bin/env bash
# =============================================================================
# setup.sh — 環境構築スクリプト
#
# 使い方:
#   cd /app
#   bash scripts/setup.sh
#
# 実行内容:
#   1. 接続確認 (Ollama / Neo4j / Python)
#   2. Python依存パッケージのインストール
#   3. メモリ確認 → 利用可能なモデルのみpull
#   4. Neo4j グラフデータのロード
# =============================================================================

set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/_common.sh

# .env があれば読み込む
[[ -f .env ]] && set -a && source .env && set +a

# ──────────────────────────────────────────────────────────────────────────────
print_header() {
    clear
    echo -e "${BOLD}============================================================${RESET}"
    echo -e "${BOLD}     環境構築スクリプト — setup.sh${RESET}"
    echo -e "${BOLD}============================================================${RESET}"
    echo ""
}

step() { echo -e "\n${BOLD}${CYAN}▶ $*${RESET}"; }
ok()   { echo -e "  ${GREEN}✅ $*${RESET}"; }
warn() { echo -e "  ${YELLOW}⚠️  $*${RESET}"; }
fail() { echo -e "  ${RED}❌ $*${RESET}"; }
info() { echo -e "  ${DIM}   $*${RESET}"; }

# ──────────────────────────────────────────────────────────────────────────────
# 1. 接続確認
# ──────────────────────────────────────────────────────────────────────────────
print_header
step "接続確認"

# Python
if python3 --version &>/dev/null; then
    ok "Python: $(python3 --version)"
else
    fail "Python3 が見つかりません"
    exit 1
fi

# pip
if python3 -m pip --version &>/dev/null; then
    ok "pip: 利用可能"
else
    warn "pip が見つかりません。インストールを試みます..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3 - --break-system-packages
fi

# Ollama
NEO4J_URI="${NEO4J_URI:-bolt://host.docker.internal:7687}"
NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:-password}"
OLLAMA_URL="${OLLAMA_BASE_URL:-http://host.docker.internal:11434}"

if curl -sf "${OLLAMA_URL}/api/tags" &>/dev/null; then
    ok "Ollama: ${OLLAMA_URL}"
else
    fail "Ollama に接続できません: ${OLLAMA_URL}"
    info ".env の OLLAMA_BASE_URL を確認してください"
    exit 1
fi

# Neo4j
if python3 - <<PYEOF 2>/dev/null; then
from neo4j import GraphDatabase
d = GraphDatabase.driver("${NEO4J_URI}", auth=("${NEO4J_USER}", "${NEO4J_PASSWORD}"))
d.verify_connectivity()
d.close()
PYEOF
    ok "Neo4j: ${NEO4J_URI}"
else
    fail "Neo4j に接続できません: ${NEO4J_URI}"
    info ".env の NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD を確認してください"
    exit 1
fi

# ──────────────────────────────────────────────────────────────────────────────
# 2. .env ファイル確認
# ──────────────────────────────────────────────────────────────────────────────
step ".env ファイル確認"
if [[ -f .env ]]; then
    ok ".env が存在します"
else
    warn ".env が見つかりません。テンプレートを作成します。"
    cat > .env <<'ENV'
NEO4J_PASSWORD=password
NEO4J_URI=bolt://host.docker.internal:7687
NEO4J_USER=neo4j
OLLAMA_BASE_URL=http://host.docker.internal:11434
ENV
    ok ".env を作成しました。必要に応じて編集してください。"
fi

# ──────────────────────────────────────────────────────────────────────────────
# 3. Python 依存パッケージ
# ──────────────────────────────────────────────────────────────────────────────
step "Python 依存パッケージのインストール"
if python3 -m pip install -r requirements.txt --break-system-packages -q; then
    ok "requirements.txt インストール完了"
else
    fail "pip install 失敗"
    exit 1
fi

# ──────────────────────────────────────────────────────────────────────────────
# 4. モデルpull（メモリ確認付き）
# ──────────────────────────────────────────────────────────────────────────────
step "Ollama モデルのpull"

AVAIL_MB=$(get_available_ram_mb)
echo -e "  利用可能RAM: ${BOLD}${AVAIL_MB}MB${RESET}"
echo ""

# 現在のpull済みモデル一覧
PULLED_MODELS=$(curl -s "${OLLAMA_URL}/api/tags" | python3 -c "
import sys, json
for m in json.load(sys.stdin).get('models', []):
    print(m['name'])
" 2>/dev/null)

echo "  モデル別の状態:"
PULLABLE_INDICES=()
for i in "${!MODEL_KEYS[@]}"; do
    key="${MODEL_KEYS[$i]}"
    name="${MODEL_NAMES[$i]}"
    label="${MODEL_LABEL[$i]}"
    required="${MODEL_SIZE_MB[$i]}"

    already_pulled=0
    echo "$PULLED_MODELS" | grep -qF "$name" && already_pulled=1
    [[ "$already_pulled" == "0" ]] && echo "$PULLED_MODELS" | grep -qF "${name}:latest" && already_pulled=1

    if (( AVAIL_MB < required )); then
        printf "  ${DIM}  -) %s  ${RED}[スキップ — メモリ不足: 必要%dMB / 空き%dMB]${RESET}\n" \
            "$label" "$required" "$AVAIL_MB"
    elif (( already_pulled )); then
        printf "  ${GREEN}  ✅ %s  [pull済み]${RESET}\n" "$label"
    else
        printf "  %d) %s  ${YELLOW}[未pull]${RESET}\n" $((i+1)) "$label"
        PULLABLE_INDICES+=("$i")
    fi
done

# 埋め込みモデルは常に必要
EMBED_MODEL="nomic-embed-text"
echo "$PULLED_MODELS" | grep -qF "$EMBED_MODEL" \
    && ok "埋め込みモデル (${EMBED_MODEL}) はpull済みです" \
    || PULLABLE_INDICES+=("embed")

if [[ ${#PULLABLE_INDICES[@]} -eq 0 ]]; then
    ok "全ての必要モデルがpull済みです。"
else
    echo ""
    # pull対象の確認
    MODELS_TO_PULL=()
    for i in "${PULLABLE_INDICES[@]}"; do
        if [[ "$i" == "embed" ]]; then
            MODELS_TO_PULL+=("$EMBED_MODEL")
        else
            MODELS_TO_PULL+=("${MODEL_NAMES[$i]}")
        fi
    done

    echo -e "  以下をpullします:"
    for m in "${MODELS_TO_PULL[@]}"; do
        echo -e "    - ${m}"
    done
    echo ""
    printf "  続けますか？ [Y/n]: "
    read -r confirm
    if [[ "$confirm" =~ ^[Nn]$ ]]; then
        warn "モデルpullをスキップしました。"
    else
        for m in "${MODELS_TO_PULL[@]}"; do
            pull_model "$m" || warn "${m} のpullに失敗しました。後で再試行してください。"
        done
    fi
fi

# 埋め込みモデルが未pullなら個別に対応
echo "$PULLED_MODELS" | grep -qF "$EMBED_MODEL" || {
    echo ""
    echo -e "  ${YELLOW}埋め込みモデル (${EMBED_MODEL}) が未pullです。pullします...${RESET}"
    pull_model "$EMBED_MODEL" || { fail "埋め込みモデルのpullに失敗しました。RAGが動作しません。"; }
}

# ──────────────────────────────────────────────────────────────────────────────
# 5. Neo4j グラフデータのロード
# ──────────────────────────────────────────────────────────────────────────────
step "Neo4j グラフデータのロード"

# 現在のノード数を確認
EXISTING_COUNT=$(python3 - <<PYEOF 2>/dev/null || echo "0"
from neo4j import GraphDatabase
d = GraphDatabase.driver("${NEO4J_URI}", auth=("${NEO4J_USER}", "${NEO4J_PASSWORD}"))
with d.session() as s:
    r = s.run("MATCH (n) RETURN count(n) AS cnt")
    print(r.single()["cnt"])
d.close()
PYEOF
)

if (( EXISTING_COUNT > 0 )); then
    echo -e "  Neo4j に既存データがあります（ノード数: ${EXISTING_COUNT}）"
    printf "  上書きしますか？ [y/N]: "
    read -r overwrite
    if [[ ! "$overwrite" =~ ^[Yy]$ ]]; then
        ok "既存データをそのまま使用します。"
        SKIP_LOAD=1
    else
        SKIP_LOAD=0
    fi
else
    SKIP_LOAD=0
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
fi

# ──────────────────────────────────────────────────────────────────────────────
# 6. 動作確認（スモークテスト）
# ──────────────────────────────────────────────────────────────────────────────
step "動作確認"

python3 - <<PYEOF
import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from neo4j import GraphDatabase
import os, requests

errors = []

# Neo4j
try:
    d = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))
    with d.session() as s:
        cnt = s.run('MATCH (n) RETURN count(n) AS c').single()['c']
    d.close()
    print(f"  ✅ Neo4j: {cnt}ノード")
except Exception as e:
    errors.append(f"Neo4j: {e}")
    print(f"  ❌ Neo4j: {e}")

# Ollama
try:
    r = requests.get(os.getenv('OLLAMA_BASE_URL', 'http://host.docker.internal:11434') + '/api/tags', timeout=5)
    models = [m['name'] for m in r.json()['models']]
    print(f"  ✅ Ollama: {len(models)} モデル利用可能")
except Exception as e:
    errors.append(f"Ollama: {e}")
    print(f"  ❌ Ollama: {e}")

# ChromaDB
try:
    import chromadb
    print(f"  ✅ ChromaDB: インポート成功")
except Exception as e:
    errors.append(f"ChromaDB: {e}")
    print(f"  ❌ ChromaDB: {e}")

sys.exit(1 if errors else 0)
PYEOF

# ──────────────────────────────────────────────────────────────────────────────
# 完了
# ──────────────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}============================================================${RESET}"
echo -e "${BOLD} セットアップ完了 ✅${RESET}"
echo -e "${BOLD}============================================================${RESET}"
echo ""
echo -e "  実行コマンド:"
echo -e "  ${BOLD}bash scripts/run_all.sh${RESET}"
echo ""
