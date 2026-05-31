#!/usr/bin/env bash
# remux.sh — 抽舊 mp4 的中文 TTS audio + 渲新 code.py 的無聲 video + mux 成 benchmark.mp4
#
# 流程：
#   1. 從 raw/draft_v1.mp4 抽 audio (.aac) — 只做一次，已抽過就跳過
#   2. manim -ql 渲新 code.py，輸出無聲 mp4
#   3. ffmpeg mux audio + video → benchmark.mp4
#
# 用法：
#   bash evaluation/benchmark_set/remux.sh Q024
#   bash evaluation/benchmark_set/remux.sh Q024 -qh    # 高品質渲染
#
# 假設 cwd = repo root (/Users/liaozhenting/Desktop/LLManim_Agent)

set -euo pipefail

QID="${1:-}"
QUALITY="${2:--ql}"  # 預設低品質快渲；用 -qh 切高品質

if [[ -z "$QID" ]]; then
  echo "Usage: bash $0 <QID> [-ql|-qm|-qh]"
  exit 1
fi

BASE="evaluation/benchmark_set/$QID"
SRC_MP4="$BASE/raw/draft_v1.mp4"
AUDIO="$BASE/raw/audio.aac"
CODE="$BASE/code.py"

if [[ ! -f "$SRC_MP4" ]]; then
  echo "❌ 找不到 $SRC_MP4"; exit 1
fi
if [[ ! -f "$CODE" ]]; then
  echo "❌ 找不到 $CODE"; exit 1
fi

# 1. 抽 audio（只做一次）
if [[ ! -f "$AUDIO" ]]; then
  echo "▶ [1/3] 抽 audio 從 draft_v1.mp4 → audio.aac"
  ffmpeg -loglevel error -y -i "$SRC_MP4" -vn -acodec copy "$AUDIO"
else
  echo "✓ [1/3] audio.aac 已存在，跳過抽取"
fi

# 2. 渲新無聲 video
# 抓繼承 Scene 的 class（避開 SubtitleManager 這種 helper class）
SCENE_NAME=$(grep -oE "^class +([A-Za-z_][A-Za-z0-9_]*)\(Scene\)" "$CODE" | head -1 | awk '{print $2}' | sed 's/(Scene)//')
if [[ -z "$SCENE_NAME" ]]; then
  echo "❌ 在 $CODE 找不到 Scene class"; exit 1
fi
echo "▶ [2/3] manim $QUALITY $CODE $SCENE_NAME"

# manim 預設輸出到 media/videos/<filename>/<resolution>/<SceneName>.mp4
manim "$QUALITY" "$CODE" "$SCENE_NAME"

# 找出 manim 剛輸出的 mp4（依品質設定）
case "$QUALITY" in
  -ql) RES_DIR="480p15" ;;
  -qm) RES_DIR="720p30" ;;
  -qh) RES_DIR="1080p60" ;;
  *)   RES_DIR="480p15" ;;
esac
SILENT_MP4="media/videos/code/${RES_DIR}/${SCENE_NAME}.mp4"
if [[ ! -f "$SILENT_MP4" ]]; then
  # fallback: manim 有時把 code.py 的目錄名當輸出夾名
  SILENT_MP4=$(find media/videos -name "${SCENE_NAME}.mp4" -print -quit)
fi
if [[ -z "$SILENT_MP4" || ! -f "$SILENT_MP4" ]]; then
  echo "❌ 找不到 manim 輸出的 mp4"; exit 1
fi
echo "✓ video 渲完: $SILENT_MP4"

# 3. mux
OUT="$BASE/benchmark.mp4"
echo "▶ [3/3] mux video + audio → $OUT"
ffmpeg -loglevel error -y -i "$SILENT_MP4" -i "$AUDIO" \
  -c:v copy -c:a copy -map 0:v:0 -map 1:a:0 -shortest "$OUT"

echo ""
echo "✅ 完成: $OUT"
echo "   播放：open $OUT"
