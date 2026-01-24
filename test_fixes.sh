# 測試腳本：驗證影片生成修復

echo "========================================="
echo "測試 LLManim_Agent 修復"
echo "========================================="
echo ""

# 清理舊檔案 (包含所有 mp4, py, audio)
echo "🧹 清理舊檔案..."
rm -rf media/audio/* stable_outputs/*.mp4 stable_outputs/*.py

# 測試 1: 運行第一個主題
echo "📝 測試 1: 運行主題 '6+7'"
echo "6+7" | .venv/bin/python main.py

echo ""
echo "⏸️  等待 3 秒..."
sleep 3

# 測試 2: 運行第二個主題
echo "📝 測試 2: 運行主題 '8*3'"
echo "8*3" | .venv/bin/python main.py

echo ""
echo "========================================="
echo "驗證結果"
echo "========================================="
echo ""

# 檢查影片
echo "🎬 檢查影片檔案："
if [ -f "stable_outputs/6+7.mp4" ]; then
    duration1=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "stable_outputs/6+7.mp4")
    size1=$(ls -lh "stable_outputs/6+7.mp4" | awk '{print $5}')
    echo "  ✓ 6+7.mp4 存在 - 時長: ${duration1}s, 大小: $size1"
else
    echo "  ✗ 6+7.mp4 不存在"
fi

if [ -f "stable_outputs/8x3.mp4" ]; then
    duration2=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "stable_outputs/8x3.mp4")
    size2=$(ls -lh "stable_outputs/8x3.mp4" | awk '{print $5}')
    echo "  ✓ 8x3.mp4 存在 - 時長: ${duration2}s, 大小: $size2"
else
    echo "  ✗ 8x3.mp4 不存在"
fi

echo ""

# 檢查 Python 檔案
echo "📄 檢查 Python 檔案："
if [ -f "stable_outputs/6+7.py" ]; then
    lines1=$(wc -l < "stable_outputs/6+7.py")
    echo "  ✓ 6+7.py 存在 - 行數: $lines1"
else
    echo "  ✗ 6+7.py 不存在"
fi

if [ -f "stable_outputs/8x3.py" ]; then
    lines2=$(wc -l < "stable_outputs/8x3.py")
    echo "  ✓ 8x3.py 存在 - 行數: $lines2"
else
    echo "  ✗ 8x3.py 不存在"
fi

echo ""

# 檢查音檔目錄
echo "🎙️ 檢查音檔目錄："
if [ -d "media/audio/6+7" ]; then
    audio_count1=$(ls media/audio/6+7/*.mp3 2>/dev/null | wc -l)
    echo "  ✓ 6+7 音檔目錄存在 - 音檔數量: $audio_count1"
else
    echo "  ✗ 6+7 音檔目錄不存在"
fi

if [ -d "media/audio/8x3" ]; then
    audio_count2=$(ls media/audio/8x3/*.mp3 2>/dev/null | wc -l)
    echo "  ✓ 8x3 音檔目錄存在 - 音檔數量: $audio_count2"
else
    echo "  ✗ 8x3 音檔目錄不存在"
fi

echo ""
echo "========================================="
echo "測試完成"
echo "========================================="
