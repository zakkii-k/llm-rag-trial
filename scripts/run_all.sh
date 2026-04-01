#!/usr/bin/env bash
# =============================================================================
# run_all.sh — GraphRAG / RAG 全パターン実行スクリプト
#
# 使い方:
#   cd /app
#   bash scripts/run_all.sh
#
# モデル・データサイズ・クエリ種別・モードを対話選択し、
# 全組み合わせを順に実行してレポートを生成する。
# =============================================================================

set -euo pipefail

# ── ディレクトリ確認 ──────────────────────────────────────────────────────────
cd "$(dirname "$0")/.."

# ── カラー定義 ────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

# ── 選択肢定義 ────────────────────────────────────────────────────────────────
MODEL_KEYS=("small"      "qwen-small"          "qwen-large"           "large")
MODEL_DESC=("llama3.2 (~2GB)  汎用軽量"
            "qwen2.5-coder:7b  (~4.7GB) Cypher特化・軽量"
            "qwen2.5-coder:14b (~9GB)   Cypher特化・高精度"
            "gemma2:27b (~15GB) 汎用高精度")

DATA_KEYS=("small"  "medium"  "large")
DATA_DESC=("small   (Bug×3,  Engineer×3)"
           "medium  (Bug×30, Engineer×10)"
           "large   (Bug×100,Engineer×30)")

QUERY_KEYS=("simple"  "medium"  "multihop")
QUERY_DESC=("simple   — 単一エンティティの基本クエリ"
            "medium   — 複数エンティティ・集計クエリ"
            "multihop — 3ホップ以上の複合クエリ")

MODE_KEYS=("both" "graphrag" "rag")
MODE_DESC=("both     — GraphRAG と RAG を両方実行"
           "graphrag — GraphRAG のみ"
           "rag      — RAG のみ")

# ── ユーティリティ関数 ────────────────────────────────────────────────────────

# 複数選択メニュー
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
    echo -e "  番号をスペース区切りで入力（例: 1 3）、${BOLD}all${RESET} で全選択:"
    printf "  > "
    read -r input

    SELECTED_INDICES=()
    if [[ "$input" == "all" || "$input" == "ALL" ]]; then
        for i in "${!_keys[@]}"; do
            SELECTED_INDICES+=("$i")
        done
    else
        for num in $input; do
            if [[ "$num" =~ ^[0-9]+$ ]] && (( num >= 1 && num <= ${#_keys[@]} )); then
                SELECTED_INDICES+=($((num - 1)))
            else
                echo -e "${RED}  無効な入力をスキップ: ${num}${RESET}"
            fi
        done
    fi

    if [[ ${#SELECTED_INDICES[@]} -eq 0 ]]; then
        echo -e "${RED}  何も選択されませんでした。デフォルト(1)を使用します。${RESET}"
        SELECTED_INDICES=(0)
    fi
}

# 選択結果を表示
show_selection() {
    local title="$1"
    local -n _keys=$2
    local -n _indices=$3
    echo -e "  ${GREEN}✓ ${title}:${RESET}"
    for i in "${_indices[@]}"; do
        echo -e "      - ${_keys[$i]}"
    done
}

# ── ヘッダー ─────────────────────────────────────────────────────────────────
clear
echo -e "${BOLD}============================================================${RESET}"
echo -e "${BOLD}     GraphRAG / RAG 全パターン実行スクリプト${RESET}"
echo -e "${BOLD}============================================================${RESET}"

# ── 選択フェーズ ──────────────────────────────────────────────────────────────
SELECTED_INDICES=()

multiselect "【1/4】使用するモデルを選択" MODEL_KEYS MODEL_DESC
SELECTED_MODEL_IDX=("${SELECTED_INDICES[@]}")

multiselect "【2/4】データサイズを選択" DATA_KEYS DATA_DESC
SELECTED_DATA_IDX=("${SELECTED_INDICES[@]}")

multiselect "【3/4】クエリ種別を選択" QUERY_KEYS QUERY_DESC
SELECTED_QUERY_IDX=("${SELECTED_INDICES[@]}")

multiselect "【4/4】実行モードを選択" MODE_KEYS MODE_DESC
SELECTED_MODE_IDX=("${SELECTED_INDICES[@]}")

# ── 確認 ─────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}------------------------------------------------------------${RESET}"
echo -e "${BOLD} 実行内容の確認${RESET}"
echo -e "${BOLD}------------------------------------------------------------${RESET}"
show_selection "モデル"     MODEL_KEYS SELECTED_MODEL_IDX
show_selection "データ"     DATA_KEYS  SELECTED_DATA_IDX
show_selection "クエリ種別" QUERY_KEYS SELECTED_QUERY_IDX
show_selection "モード"     MODE_KEYS  SELECTED_MODE_IDX

TOTAL=$(( ${#SELECTED_MODEL_IDX[@]} * ${#SELECTED_DATA_IDX[@]} * ${#SELECTED_QUERY_IDX[@]} * ${#SELECTED_MODE_IDX[@]} ))
echo ""
echo -e "  合計 ${BOLD}${TOTAL} 組み合わせ${RESET} を実行します。"
echo ""
printf "  続けますか？ [y/N]: "
read -r confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "中断しました。"
    exit 0
fi

# ── 実行フェーズ ──────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}============================================================${RESET}"
echo -e "${BOLD} 実行開始 $(date '+%Y-%m-%d %H:%M:%S')${RESET}"
echo -e "${BOLD}============================================================${RESET}"

TOTAL_START=$(date +%s)
COMBO_NUM=0
SUCCEEDED=0
FAILED=0
FAILED_LIST=()

for model_i in "${SELECTED_MODEL_IDX[@]}"; do
  for data_i in "${SELECTED_DATA_IDX[@]}"; do
    for query_i in "${SELECTED_QUERY_IDX[@]}"; do
      for mode_i in "${SELECTED_MODE_IDX[@]}"; do

        COMBO_NUM=$((COMBO_NUM + 1))
        MODEL_KEY="${MODEL_KEYS[$model_i]}"
        DATA_KEY="${DATA_KEYS[$data_i]}"
        QUERY_KEY="${QUERY_KEYS[$query_i]}"
        MODE_KEY="${MODE_KEYS[$mode_i]}"
        PROMPT_FILE="prompts/${QUERY_KEY}.txt"
        DATA_DIR="data/${DATA_KEY}"
        SCENARIO_NAME="${QUERY_KEY}_${DATA_KEY}_${MODEL_KEY}"

        echo ""
        echo -e "${BOLD}[${COMBO_NUM}/${TOTAL}]${RESET} ${CYAN}${SCENARIO_NAME}${RESET} mode=${MODE_KEY}"
        echo -e "  モデル: ${MODEL_KEY}  データ: ${DATA_DIR}  プロンプト: ${PROMPT_FILE}"

        START_TIME=$(date +%s)

        if python app/run_scenario.py \
              --prompt-file  "$PROMPT_FILE" \
              --mode         "$MODE_KEY" \
              --model        "$MODEL_KEY" \
              --data-dir     "$DATA_DIR" \
              --scenario-name "$SCENARIO_NAME"; then
            END_TIME=$(date +%s)
            ELAPSED=$((END_TIME - START_TIME))
            echo -e "  ${GREEN}✅ 完了${RESET} (${ELAPSED}秒)"
            SUCCEEDED=$((SUCCEEDED + 1))
        else
            END_TIME=$(date +%s)
            ELAPSED=$((END_TIME - START_TIME))
            echo -e "  ${RED}❌ エラー${RESET} (${ELAPSED}秒)"
            FAILED=$((FAILED + 1))
            FAILED_LIST+=("${SCENARIO_NAME} [${MODE_KEY}]")
        fi

      done
    done
  done
done

# ── サマリ ───────────────────────────────────────────────────────────────────
TOTAL_END=$(date +%s)
TOTAL_ELAPSED=$((TOTAL_END - TOTAL_START))
TOTAL_MIN=$((TOTAL_ELAPSED / 60))
TOTAL_SEC=$((TOTAL_ELAPSED % 60))

echo ""
echo -e "${BOLD}============================================================${RESET}"
echo -e "${BOLD} 実行完了 $(date '+%Y-%m-%d %H:%M:%S')${RESET}"
echo -e "${BOLD}============================================================${RESET}"
echo -e "  合計時間  : ${TOTAL_MIN}分${TOTAL_SEC}秒"
echo -e "  成功      : ${GREEN}${SUCCEEDED}${RESET} / ${TOTAL}"
echo -e "  失敗      : ${RED}${FAILED}${RESET} / ${TOTAL}"

if [[ ${#FAILED_LIST[@]} -gt 0 ]]; then
    echo ""
    echo -e "  ${RED}失敗シナリオ:${RESET}"
    for f in "${FAILED_LIST[@]}"; do
        echo -e "    - ${f}"
    done
fi

echo ""
echo -e "  レポート: ${BOLD}docs/reports/${RESET} を確認してください。"
echo ""
