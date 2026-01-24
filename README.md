# LLManim Agent

這是一個基於 LLM (Groq/Llama-3) 和 NLP 技術的自動化 Manim 動畫生成代理系統。它可以根據數學主題自動規劃腳本、生成 Python 代碼、合併語音解說，並修復代碼錯誤，最終產出高品質的教學影片。

## 📋 系統需求 (Prerequisites)

在開始之前，請確保您的電腦已安裝以下軟體：

- **Python 3.10+**
- **Git**
- **FFmpeg** (用於音訊/影片處理)
- **LaTeX** (Manim 渲染公式需要)

### 安裝系統依賴 (macOS)

```bash
brew install python
brew install ffmpeg
brew install librsvg
brew install --cask mactex-no-gui  # 安裝 BasicTeX (較輕量)
```

## 🚀 快速開始 (Getting Started)

### 1. 取得專案

```bash
git clone <repository-url>
cd LLManim_Agent
```

### 2. 建立並啟用虛擬環境

推薦使用 `venv` 來隔離專案依賴。

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安裝 Python 依賴

```bash
pip install -r requirements.txt
```

### 4. 設定環境變數 (.env)

本專案需要 API Key 才能運作。請在專案根目錄建立 `.env` 檔案。
**⚠️ 注意**：`.env` 包含敏感資訊，請勿提交到 Git。請向專案負責人索取金鑰。

`.env` 範例內容：
```ini
# Groq API (LLM)
GROQ_API_KEY=gsk_xxxxxxxxxxxx

# Azure Speech (TTS) - 如果使用 Azure 語音
AZURE_SPEECH_KEY=xxxxxxxxxxxx
AZURE_SPEECH_REGION=eastus

# 模型配置 (可選，預設已設定)
GROQ_MODEL_DEFAULT=llama-3.3-70b-versatile
GROQ_MODEL_REVIEWER=llama-3.1-8b-instant
```

### 5. 運行代碼

使用以下命令生成動畫。範例主題："Pythagorean theorem" (畢氏定理)。

```bash
# 透過管道輸入主題
echo "Pythagorean theorem" | python main.py

# 或者交互式運行 (如果代碼支援)
python main.py
```

生成結果將存放於 `stable_outputs/` 目錄中。

## 📂 專案結構

- `main.py`: 程式入口，協調各個 Agent。
- `agents/`: 包含各個專職 Agent (Planner, Coder, Reviewer...)。
- `media/`: Manim 的臨時輸出目錄 (可隨時清理)。
- `stable_outputs/`: 最終生成的影片和代碼備份。
- `logs/`: 系統運行日誌。

## 🤝 協作指南

1. **分支開發**：請勿直接推送到 `main` 分支。請為每個功能創建新分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **提交代碼**：完成開發後，提交並推送到遠端，然後發起 Pull Request (PR)。

## 🛠️ 常見問題

- **ffmpeg not found**: 請確認已運行 `brew install ffmpeg` 並且他在 PATH 中。
- **Manim Latex Error**: 確保已安裝 TeX 發行版 (如 MacTeX)。

---
專案負責人: Liao Zhenting
