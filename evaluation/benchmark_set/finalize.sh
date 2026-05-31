#!/usr/bin/env bash
# 為 30 題全部重渲 benchmark.mp4。
# - Q024 已用新 TTS，直接 manim 渲（會自動 mux audio）
# - 其他 29 題用 remux.sh（從 raw/draft_v1.mp4 抽 audio mux 進新 video）

set -uo pipefail

BASE="evaluation/benchmark_set"
LOG="$BASE/finalize.log"
echo "=== Finalize 開始: $(date) ===" > "$LOG"

ok=0; fail=0
failed=()

for d in "$BASE"/Q*/; do
  qid=$(basename "$d")
  out="$d/benchmark.mp4"

  # 強制重渲（不論是否已存在）
  rm -f "$out"
  echo ""
  echo "▶▶▶ $qid 開始..."

  # 看 add_sound 用的是新 TTS（tts_regen 路徑）還是其他
  if grep -q "tts_regen" "$d/code.py" 2>/dev/null; then
    # 新 TTS：直接 manim 渲，audio 已 inline，無需 mux
    if manim -ql "$d/code.py" GeneratedScene >> "$LOG" 2>&1; then
      # 找輸出 mp4 路徑（manim 預設輸出在 media/videos/code/480p15/）
      src_mp4="media/videos/code/480p15/GeneratedScene.mp4"
      if [ -f "$src_mp4" ]; then
        cp "$src_mp4" "$out"
        echo "    ✅ $qid (TTS regen path)"
        ((ok++))
      else
        echo "    ❌ $qid: manim 沒輸出 mp4"
        failed+=("$qid")
        ((fail++))
      fi
    else
      echo "    ❌ $qid: manim 失敗"
      failed+=("$qid")
      ((fail++))
    fi
  else
    # 舊 audio：用 remux.sh
    if bash "$BASE/remux.sh" "$qid" >> "$LOG" 2>&1; then
      if [ -f "$out" ]; then
        echo "    ✅ $qid (remux from draft audio)"
        ((ok++))
      else
        echo "    ❌ $qid: remux 完但 mp4 不存在"
        failed+=("$qid")
        ((fail++))
      fi
    else
      echo "    ❌ $qid: remux 失敗"
      failed+=("$qid")
      ((fail++))
    fi
  fi
done

echo ""
echo "================ 總結 ================"
echo "✅ 成功: $ok"
echo "❌ 失敗: $fail"
if (( fail > 0 )); then
  echo "失敗: ${failed[*]}"
  echo "Log: $LOG"
fi
