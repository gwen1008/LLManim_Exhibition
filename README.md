# LLManim Agent 🎬

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Manim](https://img.shields.io/badge/Manim-Community-green)](https://www.manim.community/)
[![TTS](https://img.shields.io/badge/Azure-Speech-0078D4)](https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/)

**LLManim Agent** 是一個先進的自動化教學影片生成系統。它結合了大型語言模型 (LLM)、確定性算法模板與語音合成技術，能夠自動產出高品質、影音同步且具備互動性的數學教學影片。

---

## ✨ 核心功能 (Key Features)

## 🏗️ 系統架構 (System Architecture)

```mermaid
graph TD
    User([👤 User]) -->|Input Topic| Streamlit[🖥️ Streamlit UI]
    Streamlit -->|subprocess| Main[⚙️ Main Loop]
    
    subgraph "Phase 1: Planning & Coding"
        Main -->|Topic| Planner[🧠 Planner Agent]
        Planner -->|Script JSON| Coder[💻 Coder Agent]
        Coder -->|Python Code| ManimFile[🐍 Generated Scene]
    end
    
    subgraph "Phase 2: Rendering & QA"
        ManimFile -->|Render| ManimEngine[🎬 Manim Engine]
        ManimEngine -->|Success?| CheckRender{Render OK?}
        CheckRender -->|No| FixRender[🔧 Syntax Fixer]
        FixRender --> Coder
        CheckRender -->|Yes| VisionQA[👁️ Vision Agent]
    end
    
    subgraph "Phase 3: Visual Audit Loop"
        VisionQA -->|Audit Frame| AuditResult{Audit Pass?}
        AuditResult -->|Fail| CheckLimit{Attempts < 5?}
        CheckLimit -->|Yes| VisualFixER[🛠️ Visual Fix Prompter]
        VisualFixER -->|Fix Instructions| Coder
        CheckLimit -->|No| Inbox
    end
    
    subgraph "Phase 4: Output"
        AuditResult -->|Pass| Inbox[📥 Inbox]
        Inbox -->|Auto-Sort| Categories[📂 Subject Folders]
    end
```

### 1. 🧠 四階段 Multi-Agent 工作流 (4-Stage Pipeline)

系統採用職責分離的 Agent 架構，並內建嚴密的防呆與自我修正機制：

- **Phase 1：Planner (導演)**：接收輸入後，透過 Translator 轉換語境，將數學概念拆解成邏輯序列，並輸出包含視覺佈局提示 (Spatial Hints) 的結構化 JSON 分鏡表。
- **Phase 2：Coder (工程師)**：以低溫度 (T=0.3) 確保邏輯穩定性，負責將 Planner 給出的 JSON 翻譯成高精確度的 Manim Python 程式碼，並自動調適畫面的元件位置。
- **Phase 3：Render & Audio Sync (精準影音渲染)**：整合 Azure Text-to-Speech 生成高擬真旁白。為了達成「完美影音同步」，系統會在產出代碼後，透過代碼注入自動分析 AST 將具體的音訊時長替換回代碼，保證動畫與旁白的時間誤差 < 0.1 秒，並支援自動產生逐字字幕。
- **Phase 4：Review & Vision QA (自動審查與修復)**：若 Manim 渲染出 Syntax Error 或發生畫面元件交疊，Vision Agent 會立刻介入。系統允許最多 5 次 (5 Iterations) 的自動修復嘗試，讓模型自我糾正。

### 2. ⚡ 核心工程最佳化 (Engineering Optimizations)

- **三路平行處理 (Parallel Execution)**：RAG 檢索、Audio 生成與 Coder 是**並行運作的**。Planner 一給出腳本，Audio Engine 就開始合成語音；而 Coder 只要等到 RAG 結果就立刻動工。這套非同步設計為單次生成省下了 15~28 秒。
- **RAG 動態知識庫 (Weaviate Vector DB)**：為解決 LLM 憑空捏造的問題，寫 Code 前會先從向量資料庫抓出高相關性的「Manim 黃金範例代碼」塞進 Context 中，大幅降低幻覺 (Hallucinations)。
- **互動式教育模式 (Interactive Mode)**：在特定的算術或推理關卡，系統能自動觸發「提問機制」，在畫面上打出閃爍的問號 (?) 並延長留白時間，藉此控制學生的認知負載並引導主動思考。

---

## 📊 效能表現與測試基準 (Performance & Benchmarks)

在近期針對 240 題 K-12（國小至高中）的數學標竿測試中，本系統繳出了極具統治力的表現：

- **生成成功率**：高達 **90.0% (216/240)** 的主題能完美通過所有驗證並產出影片，其中有 **75.9%** 是「0 錯誤、一次通關 (1-Iteration)」。
- **極致成本控管**：平均每支影片的 API 推理成本僅約 **$0.0115 USD**。
- **高效率**：包含撰碼、渲染、語音與修復，產生一支平均 88 秒的教學動畫，系統耗時僅需 **~233 秒**（不到 4 分鐘）。

### 🚀 未來展望與突破 (Roadmap)

- 目前已具備發表水準，正著手準備投稿 **AIED 2026 LBR (Late Breaking Results)** 論文。
- **模型私有化與專武打造**：未來計畫不再完全依賴閉源巨型 LLM。準備透過 **SFT, DPO, GRPO** 等三階段訓練法，把代碼生成能力蒸餾到 7B-14B 的輕量級開源模型中，實現地端自主運行的最強 Manim Coder。

---

## 🛠️ 安裝與設定 (Installation)

### 1. 系統需求

- **OS**: macOS (推薦) / Linux
- **Python**: 3.10+
- **依賴工具**:

  ```bash
  brew install ffmpeg librsvg
  brew install --cask mactex-no-gui  # LaTeX 環境
  ```

### 2. 下載與安裝

```bash
git clone https://github.com/childe0905/LLManim_Agent.git
cd LLManim_Agent

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. 環境變數配置 (.env)

請在專案根目錄建立 `.env` 檔案，填入以下金鑰：

```ini
# --- Core LLM ---
GROQ_API_KEY=gsk_xxxxxxxxxxxx  # Agent 核心推理

# --- Azure Speech (Required for Audio) ---
AZURE_SPEECH_KEY=xxxxxxxxxxxx
AZURE_SPEECH_REGION=eastus

# --- Optional (RAG Video Ingestion ONLY) ---
OPENAI_API_KEY=sk-xxxxxxxx    # 僅在使用 RAG 寫入影片描述時需要
```

> **注意**：若未配置 Azure Key，系統會自動降級為「模擬模式」，僅根據字數估算時長，不會生成真實語音。

---

## 🚀 使用指南 (Usage)

### 1. 通用教學影片生成器 (General Generator)

本專案支援任意 K-12 數學或科學主題生成。啟動主程式後，系統將依序執行 Planner (規劃) -> Coder (寫碼) -> Audio Engine (語音對齊) -> Vision Agent (修復) 工作流：

```bash
python main.py
```
> **💡 提示**：啟動後輸入任何主題（例如：「圖解勾股定理的證明」、「說明圓柱體的體積怎麼算」、「國小分數加法」），系統即可自動完成全部創作。

### 2. 特定算術模板 (Arithmetic Template)

如果只需要簡單演示專門的直式計算，可直接調用算術腳本：

```bash
# 生成 84 + 985 的直式計算影片與語音
python run_arithmetic_with_audio.py 84 985

# 互動模式：加入提問與暫停 (閃爍問號)引導思考
python run_arithmetic_with_audio.py 84 985 --interactive
```

**手動渲染代碼**:
生成的代碼皆存放於 `stable_outputs/` 或 `stable_outputs_interactive/`。

```bash
# 預覽低畫質 (-pql)
manim -pql stable_outputs_interactive/addition_84_985.py VerticalAddition
```

### 3. Web 介面 (Streamlit)

提供友善的網頁介面，適合展示與測試。

```bash
streamlit run app.py
```

在瀏覽器打開顯示的 URL，輸入主題即可生成並即時預覽。

---

## 📚 RAG 知識庫設定 (RAG Setup)

若您的團隊需要使用 RAG 功能，請按照以下步驟設置**本地向量資料庫**。

### 1. 啟動資料庫

本專案使用 Weaviate。請確保已安裝 Docker。

```bash
docker-compose up -d
```

### 2. 資料入庫 (Ingestion)

初次使用需將範例代碼寫入資料庫：

```bash
pip install weaviate-client opencv-python openai

python rag/ingest_code.py   # 寫入代碼範例
python rag/ingest_video.py  # 寫入影片描述 (可選，需 OpenAI Key)
```

詳細進階說明請見 [rag/README.md](rag/README.md)。

---

## 🧪 測試與驗證 (Testing)

確保模板在各種情況下都能正確運作。

```bash
python tests/test_addition_cases.py
```

---

## 🛠️ 常見問題 (Troubleshooting)

- **ffmpeg not found**: 請確認已運行 `brew install ffmpeg` 並且它在 PATH 中。
- **Manim Latex Error**: 確保已安裝 TeX 發行版 (如 MacTeX)。
- **ValueError: Called Scene.play with no animations**: 這是 Manim 的已知行為，若動畫列表為空會報錯。我們的模板已修復此問題 (使用 `wait` 替代)，若您手寫代碼遇到此問題，請檢查傳入 `play` 的物件是否為空。
- **AudioEngine Error**: 若看到 Azure 相關錯誤，請檢查 `.env` 中的 `AZURE_SPEECH_KEY` 和 `REGION` 是否正確。

---

## 📂 專案結構圖

```
LLManim_Agent/
├── agents/                 # 智能體核心邏輯
├── templates/              # 確定性算術模板
│   └── IMPLEMENTER_GUIDE.md # [重要] 團隊成員開發指南
├── run_arithmetic_with_audio.py  # 算術生成主程式
├── main.py                 # 通用生成入口
├── app.py                  # Web App
├── rag/                    # RAG 模組
├── stable_outputs/         # 產出 (一般模式)
├── stable_outputs_interactive/ # 產出 (互動模式)
└── tests/                  # 測試腳本
```

---

## 🤝 貢獻指南 (Contributing)

我們歡迎所有形式的貢獻！為了保持 `main` 分支的穩定性，請遵循 **GitHub Flow**：

1. **Fork** 本倉庫。
2. **Clone** 到本地。
3. **開分支 (Branch)**：`git checkout -b feature/amazing-feature`
4. **提交 (Commit)**：`git commit -m 'Add amazing feature'`
5. **推送 (Push)**：`git push origin feature/amazing-feature`
6. **開 PR (Pull Request)**：在 GitHub 上發起合併請求。

---
**Lead Developer**: Liao Zhenting
