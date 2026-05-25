#!/usr/bin/env bash
# 批次跑 remux.sh 對所有有 .llm-bak 備份的題目（= LLM 改寫過的題目）
# 已存在 benchmark.mp4 的題目自動跳過

set -uo pipefail  # 故意不用 -e，讓單題失敗不中斷整批

BASE="evaluation/benchmark_set"
LOG="$BASE/remux_all.log"

mkdir -p "$(dirname "$LOG")"
echo "=== Batch remux 開始: $(date) ===" > "$LOG"

ok=0; skip=0; fail=0
failed_qids=()

for bak in "$BASE"/Q*/code.py.llm-bak; do
  qd=$(dirname "$bak")
  qid=$(basename "$qd")
  out="$qd/benchmark.mp4"

  if [[ -f "$out" ]]; then
    echo "⏭  $qid 已有 benchmark.mp4，跳過"
    ((skip++))
    continue
  fi

  echo ""
  echo "▶▶▶ $qid 開始渲染..."
  if bash "$BASE/remux.sh" "$qid" >> "$LOG" 2>&1; then
    echo "    ✅ $qid 完成"
    ((ok++))
  else
    echo "    ❌ $qid 失敗（看 $LOG）"
    failed_qids+=("$qid")
    ((fail++))
  fi
done

echo ""
echo "================ 總結 ================"
echo "✅ 成功: $ok"
echo "⏭  跳過: $skip"
echo "❌ 失敗: $fail"
if (( fail > 0 )); then
  echo ""
  echo "失敗題目: ${failed_qids[*]}"
  echo "詳細 log: $LOG"
fi
