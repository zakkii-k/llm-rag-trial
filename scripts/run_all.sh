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
# メモリ確認により、利用不可のモデルは選択肢から除外される。
# =============================================================================

set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/_common.sh

# .env があれば読み込む（検出より .env を優先）
[[ -f .env ]] && set -a && source .env && set +a

# ──────────────────────────────────────────────────────────────────────────────
clear
echo -e "${BOLD}============================================================${RESET}"
echo -e "${BOLD}     GraphRAG / RAG 全パターン実行スクリプト${RESET}"
echo -e "${BOLD}============================================================${RESET}"
echo -e "  実行環境: ${BOLD}$(detect_env_label)${RESET}  (ホスト: $(detect_host))"

# ── 事前チェック ──────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${CYAN}▶ 事前チェック${RESET}"

# Ollama
if ! curl -sf "${OLLAMA_URL}/api/tags" &>/dev/null; then
    echo -e "  ${RED}❌ Ollama に接続できません: ${OLLAMA_URL}${RESET}"
    echo -e "  ${DIM}   scripts/setup.sh を実行してください。${RESET}"
    exit 1
fi
echo -e "  ${GREEN}✅ Ollama: 接続OK${RESET}"

# Neo4j
NEO4J_URI="${NEO4J_URI:-bolt://host.docker.internal:7687}"
NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:-password}"

NODE_COUNT=$(python3 - <<PYEOF 2>/dev/null || echo "0"
from neo4j import GraphDatabase
d = GraphDatabase.driver("${NEO4J_URI}", auth=("${NEO4J_USER}", "${NEO4J_PASSWORD}"))
with d.session() as s:
    print(s.run("MATCH (n) RETURN count(n) AS c").single()["c"])
d.close()
PYEOF
)

if (( NODE_COUNT == 0 )); then
    echo -e "  ${RED}❌ Neo4j にデータがありません。scripts/setup.sh を先に実行してください。${RESET}"
    exit 1
fi
echo -e "  ${GREEN}✅ Neo4j: ${NODE_COUNT}ノード${RESET}"

# ── 選択フェーズ ──────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}------------------------------------------------------------${RESET}"
echo -e "${BOLD} 実行条件を選択してください${RESET}"
echo -e "${BOLD}------------------------------------------------------------${RESET}"

# モデル（メモリ・pull状態チェック付き）
echo -e "\n${BOLD}${CYAN}【1/4】使用するモデルを選択${RESET}"
select_models
SELECTED_MODEL_IDX=("${SELECTED_MODEL_IDX[@]}")

# データサイズ
multiselect "【2/4】データサイズを選択" DATA_KEYS DATA_DESC
SELECTED_DATA_IDX=("${SELECTED_INDICES[@]}")

# クエリ種別
multiselect "【3/4】クエリ種別を選択" QUERY_KEYS QUERY_DESC
SELECTED_QUERY_IDX=("${SELECTED_INDICES[@]}")

# モード
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
        echo -e "${BOLD}[${COMBO_NUM}/${TOTAL}]${RESET} ${CYAN}${SCENARIO_NAME}${RESET}  mode=${MODE_KEY}"
        echo -e "  ${DIM}モデル: ${MODEL_KEY}  データ: ${DATA_DIR}  プロンプト: ${PROMPT_FILE}${RESET}"

        START_TIME=$(date +%s)

        set +e
        python3 app/run_scenario.py \
              --prompt-file   "$PROMPT_FILE" \
              --mode          "$MODE_KEY" \
              --model         "$MODEL_KEY" \
              --data-dir      "$DATA_DIR" \
              --scenario-name "$SCENARIO_NAME"
        EXIT_CODE=$?
        set -e

        END_TIME=$(date +%s)
        ELAPSED=$((END_TIME - START_TIME))

        if (( EXIT_CODE == 0 )); then
            echo -e "  ${GREEN}✅ 完了${RESET}  (${ELAPSED}秒)"
            SUCCEEDED=$((SUCCEEDED + 1))
        elif (( EXIT_CODE == 2 )); then
            echo -e "  ${YELLOW}⚠️  メモリ不足のためスキップ${RESET}  (${ELAPSED}秒)"
            echo -e "  ${DIM}   残りのシナリオも同モデルはスキップします。${RESET}"
            FAILED=$((FAILED + 1))
            FAILED_LIST+=("${SCENARIO_NAME} [${MODE_KEY}] — メモリ不足")
            # 同モデルの残シナリオをスキップ
            break 3
        else
            echo -e "  ${RED}❌ エラー${RESET}  (${ELAPSED}秒)"
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
