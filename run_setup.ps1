# LLManim Agent - Windows 快速設定與執行
# 在 PowerShell 中執行: .\run_setup.ps1
#
# 先決條件：Python 3.10+、FFmpeg、LaTeX (Manim 渲染公式用)。
# 若尚未安裝 FFmpeg： winget install FFmpeg  或從 https://ffmpeg.org 下載

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot
Set-Location $projectRoot

Write-Host "`n=== 1. 虛擬環境 ===" -ForegroundColor Cyan
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "已建立 .venv" -ForegroundColor Green
} else {
    Write-Host ".venv 已存在" -ForegroundColor Green
}

Write-Host "`n=== 2. 啟動虛擬環境並安裝依賴 ===" -ForegroundColor Cyan
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Write-Host "`n=== 3. 檢查 .env ===" -ForegroundColor Cyan
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "已從 .env.example 複製為 .env" -ForegroundColor Green
        Write-Host "請用編輯器開啟 .env，將 GROQ_API_KEY 改為您的金鑰後存檔。" -ForegroundColor Yellow
        Write-Host "若尚無金鑰，請向專案負責人索取，再執行: python main.py" -ForegroundColor Gray
    } else {
        Write-Host "請在專案根目錄建立 .env，並填入 GROQ_API_KEY=gsk_xxxx" -ForegroundColor Yellow
    }
} else {
    Write-Host ".env 已存在" -ForegroundColor Green
}

Write-Host "`n=== 4. 執行 main.py ===" -ForegroundColor Cyan
Write-Host "若要直接以主題 'Pythagorean theorem' 執行，可改為: " -ForegroundColor Gray
Write-Host '  "Pythagorean theorem" | python main.py' -ForegroundColor Gray
Write-Host ""
python main.py
