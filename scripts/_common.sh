#!/usr/bin/env bash
# =============================================================================
# _common.sh — setup.sh / run_all.sh 共通定義
# このファイルは直接実行しない。source して使う。
# =============================================================================

# ── カラー ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; DIM='\033[2m'; RESET='\033[0m'

# ── モデル定義 ────────────────────────────────────────────────────────────────
MODEL_KEYS=("small"      "qwen-small"          "qwen-large"           "large")
MODEL_NAMES=("llama3.2"  "qwen2.5-coder:7b"    "qwen2.5-coder:14b"    "gemma2:27b")
MODEL_SIZE_MB=(2500       6000                  11000                  17000)
MODEL_LABEL=("llama3.2 (~2GB)   汎用軽量"
             "qwen2.5-coder:7b  (~4.7GB)  Cypher特化・軽量"
             "qwen2.5-coder:14b (~9GB)    Cypher特化・高精度"
             "gemma2:27b (~15GB)  汎用高精度")

# ── データ定義 ────────────────────────────────────────────────────────────────
DATA_KEYS=("small"  "medium"  "large")
DATA_DESC=("small   — Bug×3,  Engineer×3"
           "medium  — Bug×30, Engineer×10"
           "large   — Bug×100,Engineer×30")

# ── クエリ定義 ────────────────────────────────────────────────────────────────
QUERY_KEYS=("simple"  "medium"  "multihop")
QUERY_DESC=("simple   — 単一エンティティの基本クエリ"
            "medium   — 複数エンティティ・集計クエリ"
            "multihop — 3ホップ以上の複合クエリ")

# ── モード定義 ────────────────────────────────────────────────────────────────
MODE_KEYS=("both" "graphrag" "rag")
MODE_DESC=("both     — GraphRAG と RAG を両方実行"
           "graphrag — GraphRAG のみ"
           "rag      — RAG のみ")

# ── 実行環境の自動検出 ────────────────────────────────────────────────────────
# /.dockerenv が存在する → Docker コンテナ内
# それ以外           → WSL / ホスト直実行
detect_host() {
    if [ -f /.dockerenv ]; then
        echo "host.docker.internal"
    else
        echo "localhost"
    fi
}

detect_env_label() {
    if [ -f /.dockerenv ]; then
        echo "Docker コンテナ内"
    else
        echo "WSL / ホスト環境"
    fi
}

# ── Ollama / Neo4j URL（.env > 自動検出の優先順位） ──────────────────────────
_DEFAULT_HOST=$(detect_host)
OLLAMA_URL="${OLLAMA_BASE_URL:-http://${_DEFAULT_HOST}:11434}"
NEO4J_DEFAULT_URI="bolt://${_DEFAULT_HOST}:7687"

# ── 利用可能RAM (MB) を取得 ───────────────────────────────────────────────────
get_available_ram_mb() {
    free -m | awk '/^Mem:/{print $7}'
}

# ── Ollama にpull済みか確認 ───────────────────────────────────────────────────
# 引数: モデル名 (例: llama3.2, qwen2.5-coder:7b)
is_model_pulled() {
    local model="$1"
    # :latest タグ省略に対応
    curl -s "${OLLAMA_URL}/api/tags" \
        | python3 -c "
import sys, json
models = [m['name'] for m in json.load(sys.stdin).get('models', [])]
name = sys.argv[1]
print('yes' if name in models or name + ':latest' in models else 'no')
" "$model" 2>/dev/null
}

# ── モデルの状態を判定 ────────────────────────────────────────────────────────
# 引数: index (MODEL_KEYS のインデックス)
# 出力: "ok" / "ram" / "notpulled"
check_model_status() {
    local idx="$1"
    local avail_mb
    avail_mb=$(get_available_ram_mb)
    local required_mb="${MODEL_SIZE_MB[$idx]}"
    local model_name="${MODEL_NAMES[$idx]}"

    if (( avail_mb < required_mb )); then
        echo "ram"
        return
    fi

    local pulled
    pulled=$(is_model_pulled "$model_name")
    if [[ "$pulled" != "yes" ]]; then
        echo "notpulled"
        return
    fi

    echo "ok"
}

# ── モデル選択メニュー（メモリ・pull状態チェック付き） ────────────────────────
# 出力: SELECTED_MODEL_IDX (グローバル配列)
select_models() {
    local avail_mb
    avail_mb=$(get_available_ram_mb)

    echo ""
    echo -e "${BOLD}${CYAN}モデルを選択${RESET}  (利用可能RAM: ${avail_mb}MB)"
    echo ""

    local selectable=()
    for i in "${!MODEL_KEYS[@]}"; do
        local status
        status=$(check_model_status "$i")
        local required_mb="${MODEL_SIZE_MB[$i]}"
        local label="${MODEL_LABEL[$i]}"

        case "$status" in
            ok)
                printf "  %d) %s\n" $((i+1)) "$label"
                selectable+=("$i")
                ;;
            ram)
                printf "  ${DIM}-) %s  ${RED}[メモリ不足 — 必要:%dMB / 空き:%dMB]${RESET}${DIM}${RESET}\n" \
                    "$label" "$required_mb" "$avail_mb"
                ;;
            notpulled)
                printf "  ${DIM}-) %s  ${YELLOW}[未pull — setup.sh を実行してください]${RESET}${DIM}${RESET}\n" \
                    "$label"
                ;;
        esac
    done

    if [[ ${#selectable[@]} -eq 0 ]]; then
        echo -e "\n  ${RED}選択可能なモデルがありません。${RESET}"
        echo -e "  scripts/setup.sh を実行してモデルをpullするか、不要なプロセスを終了してRAMを確保してください。"
        exit 1
    fi

    echo ""
    echo -e "  番号をスペース区切りで入力（例: 1 3）、${BOLD}all${RESET} で全選択:"
    printf "  > "
    read -r input

    SELECTED_MODEL_IDX=()
    if [[ "$input" == "all" || "$input" == "ALL" ]]; then
        SELECTED_MODEL_IDX=("${selectable[@]}")
    else
        for num in $input; do
            if [[ "$num" =~ ^[0-9]+$ ]]; then
                local idx=$((num - 1))
                # 選択可能なものだけ受け付ける
                local ok=0
                for s in "${selectable[@]}"; do [[ "$s" == "$idx" ]] && ok=1; done
                if (( ok )); then
                    SELECTED_MODEL_IDX+=("$idx")
                else
                    echo -e "  ${RED}  ${num} は選択できません（メモリ不足または未pull）。スキップします。${RESET}"
                fi
            fi
        done
    fi

    if [[ ${#SELECTED_MODEL_IDX[@]} -eq 0 ]]; then
        echo -e "  ${YELLOW}何も選択されませんでした。先頭の利用可能モデル(${MODEL_KEYS[${selectable[0]}]})を使用します。${RESET}"
        SELECTED_MODEL_IDX=("${selectable[0]}")
    fi
}

# ── 汎用 複数選択メニュー ─────────────────────────────────────────────────────
# 引数: タイトル, キー配列名, 説明配列名
# 出力: SELECTED_INDICES (グローバル配列)
multiselect() {
    local title="$1"
    local -n _keys=$2
    local -n _desc=$3

    echo ""
    echo -e "${BOLD}${CYAN}${title}${RESET}"
    for i in "${!_keys[@]}"; do
        printf "  %d) %s\n" $((i+1)) "${_desc[$i]}"
    done
    echo ""
    echo -e "  番号をスペース区切りで入力、${BOLD}all${RESET} で全選択:"
    printf "  > "
    read -r input

    SELECTED_INDICES=()
    if [[ "$input" == "all" || "$input" == "ALL" ]]; then
        for i in "${!_keys[@]}"; do SELECTED_INDICES+=("$i"); done
    else
        for num in $input; do
            if [[ "$num" =~ ^[0-9]+$ ]] && (( num >= 1 && num <= ${#_keys[@]} )); then
                SELECTED_INDICES+=($((num - 1)))
            else
                echo -e "  ${RED}  無効な入力をスキップ: ${num}${RESET}"
            fi
        done
    fi

    if [[ ${#SELECTED_INDICES[@]} -eq 0 ]]; then
        echo -e "  ${YELLOW}何も選択されませんでした。先頭(1)を使用します。${RESET}"
        SELECTED_INDICES=(0)
    fi
}

# ── 選択結果表示 ──────────────────────────────────────────────────────────────
show_selection() {
    local title="$1"
    local -n _keys=$2
    local -n _indices=$3
    echo -e "  ${GREEN}✓ ${title}:${RESET}"
    for i in "${_indices[@]}"; do
        echo -e "      - ${_keys[$i]}"
    done
}

# ── モデルpull（ストリーミング進捗付き） ──────────────────────────────────────
pull_model() {
    local model="$1"
    echo -e "  ${CYAN}Pulling ${model} ...${RESET}"
    curl -s -X POST "${OLLAMA_URL}/api/pull" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"${model}\"}" \
        | python3 -u - <<'PYEOF'
import sys, json

prev_status = ""
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
    except Exception:
        continue

    status    = d.get("status", "")
    total     = d.get("total", 0)
    completed = d.get("completed", 0)

    if total and completed:
        pct = int(completed * 100 / total)
        bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
        print(f"\r    [{bar}] {pct:3d}%  {status:<30}", end="", flush=True)
    elif status != prev_status:
        print(f"\r    {status:<60}", end="", flush=True)
        prev_status = status

print()  # 改行
PYEOF

    # 成否確認
    local result
    result=$(curl -s "${OLLAMA_URL}/api/tags" \
        | python3 -c "
import sys, json
models = [m['name'] for m in json.load(sys.stdin).get('models', [])]
name = sys.argv[1]
print('ok' if name in models or name + ':latest' in models else 'fail')
" "$model" 2>/dev/null)

    if [[ "$result" == "ok" ]]; then
        echo -e "  ${GREEN}  ✅ ${model} pull 完了${RESET}"
        return 0
    else
        echo -e "  ${RED}  ❌ ${model} pull 失敗${RESET}"
        return 1
    fi
}
