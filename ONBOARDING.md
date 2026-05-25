# 組員 Onboarding — LLManim_Agent 效能優化

> **目標讀者**：剛加入的學生 / 新手工程師
> **預期時間**：1 天內讀完 + 環境跑通 + 提第一個 PR
> **任務一句話**：降低單題生成 wall-clock 時間，不能讓正確率退化

---

## 目錄

1. [這個專案在做什麼](#1-這個專案在做什麼)
2. [你要做的事](#2-你要做的事)
3. [Setup（環境安裝）](#3-setup環境安裝)
4. [跑第一題 smoke test](#4-跑第一題-smoke-test)
5. [架構與 Pipeline 詳解](#5-架構與-pipeline-詳解)
6. [量測工具：`cost_report.json`](#6-量測工具cost_reportjson)
7. [效能優化方向（你可以挑一個做）](#7-效能優化方向你可以挑一個做)
8. [禁區（絕對不要動）](#8-禁區絕對不要動)
9. [如果你用 AI 工具寫 code](#9-如果你用-ai-工具寫-code)
10. [Git 工作流](#10-git-工作流)
11. [常見問題與 Debug](#11-常見問題與-debug)
12. [Baseline 數字](#12-baseline-數字)
13. [連絡與資源](#13-連絡與資源)

---

## 1. 這個專案在做什麼

LLManim_Agent 是一個 **AI 驅動的數學動畫生成器**。輸入一個數學題目（例如「計算 (-45) - (-18) + 20」），它會自動產出一支配音的 Manim 動畫，展示解題過程。

整個流程是一個 **多 agent 編排（multi-agent orchestration）系統**：

```
使用者輸入題目
    ↓
Planner（規劃師）→ 產出 JSON 視覺腳本
    ↓
Coder（程式員）→ 把腳本翻譯成 Manim Python code
    ↓
Render（渲染）→ 跑 Manim 產出 mp4
    ↓
Vision QA（視覺審查）→ GPT-4o 看影片有沒有 bug，有 bug 就叫 Coder 修
    ↓（最多重試 5 輪）
FinalJudge（最終評分）→ 給品質分數
    ↓
輸出 mp4 + cost_report.json
```

**每題大概要跑 1-3 分鐘**，瓶頸主要在 Coder（呼叫 Claude Opus 寫 code）跟 Vision QA（多輪 GPT-4o）。你的工作就是**讓這流程更快**。

---

## 2. 你要做的事

**降低單題生成 wall-clock 時間，不能讓正確率（FinalJudge verdict）退化。**

### 怎麼算成功？

1. 跑 **baseline**（30 題 sample，現狀的平均時間 + 通過率）
2. 改你的優化
3. **再跑同樣 30 題**，對比前後
4. 寫個小報告（PR description）：哪一階段變快多少、總時間降多少、正確率有沒有變

### 成功標準

- 至少一個階段時間 **明顯降低**（不是 5% 雜訊那種，是 20%+）
- FinalJudge `PASS` 比例 **不變或提升**
- 不破壞既有測試（如果有的話）

### 不算成功的例子

- 「我把 Coder 的 prompt 縮短了所以快 30%」→ 但 PASS 率從 90% 掉到 60% → ❌ 拒絕
- 「我覺得這樣應該會比較快」→ 沒附 before/after 數字 → ❌ 退回去測
- 「我把 RefiningLoop 上限從 5 改成 3 所以快」→ 動了禁區（見 §8）→ ❌

---

## 3. Setup（環境安裝）

### 3.1 系統前置（macOS 為例；Linux 大同小異）

```bash
# Python 3.10+（建議 3.11）
python --version  # 確認

# ffmpeg（Manim 渲染需要）
brew install ffmpeg

# 確認 ffmpeg 裝好
ffmpeg -version
```

如果是 **Windows**：建議用 WSL2 跑，原生 Windows 對 Manim + Azure TTS + Claude CLI 都有奇怪的相容性問題。

### 3.2 clone repo + 切分支

```bash
git clone git@github.com:childe0905/LLManim_Agent.git
cd LLManim_Agent
git checkout perf/optimization  # ← 你的工作分支
```

### 3.3 Python 環境

```bash
# 建議用 venv（不要污染系統 Python）
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# Windows WSL 同上

# 確認你在 venv 裡（prompt 應該變 (.venv)）
which python  # 應該指向 .venv/bin/python

# 安裝依賴
pip install -r requirements.txt

# Manim 有額外系統依賴，照官方文件補：
# https://docs.manim.community/en/stable/installation.html
```

### 3.4 環境變數 `.env`

```bash
cp .env.example .env
# 用編輯器打開 .env
```

**必填**（跟 owner 拿）：
- `OPENAI_API_KEY` — Vision QA 用 GPT-4o
- `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION` — 中文/英文 TTS

**可選**（先用 default）：
- `PLANNER_MODEL` / `CODER_MODEL` / `VISION_MODEL` — model 路由
- 其他進階參數見 `.env.example` 註解

### 3.5 Claude Code CLI（給 Coder 用）

**Coder 不用 API key，走 Claude Code CLI 訂閱（Claude Max 帳號）。**

```bash
# 1. 安裝 Claude CLI（如果還沒）
# 參考：https://docs.claude.com/en/docs/claude-code/quickstart

# 2. 跟 owner 確認你用哪個帳號
# - 選項 A：你自己的 Claude 帳號（最簡單，扣你 quota）
# - 選項 B：claudealt 系統帳號（owner 提供）
# 大部分情況選 A 即可

# 3. 登入
claude login

# 4. 確認 claude 在 PATH 裡
which claude
# 如果結果不是 /usr/local/bin/claude 或 ~/.local/bin/claude，
# 把實際路徑寫進 .env 的 CLAUDE_BIN
```

### 3.6 Weaviate（RAG 用，可選）

預設 RAG 走遠端 Weaviate。如果你**完全不碰 RAG 相關優化**，可以 `DISABLE_RAG=1` 跳過。

如果要碰，跟 owner 拿 Weaviate 連線資訊。

---

## 4. 跑第一題 smoke test

```bash
# 確認你在 .venv 裡 + .env 填好
source .venv/bin/activate

# 跑 Q028（簡單的整數加減題，~1-2 分鐘）
python run_evaluation.py \
    --variant A \
    --case Q028 \
    --sample evaluation/experiment_sample_30.json
```

### 預期輸出

```
📝 [階段 0] 載入測資...
🧠 [階段 1: Planner] 正在規劃視覺腳本...
⏱  [Planner] 2.3s
🔍 [階段 1.5: RAG] 正在檢索相似範例...
🎙️ [階段 1.5: Audio Generation 並行中] 正在生成語音...
👨‍💻 [階段 2: Coder] 正在生成動畫程式碼...
⏱  [Render] ...s
👁️ [步驟 3/3] 正在執行視覺 QA 審查...
🏛️ [階段 4: FinalJudge] 啟動兩階段品質評分...
⏱  [FinalJudge] 8.2s

✅ 完成！輸出位置：
   - 影片：stable_outputs/<topic>_<timestamp>.mp4
   - cost report：stable_outputs/cost_report.json
```

### 看 cost_report.json

```bash
cat stable_outputs/cost_report.json | python -m json.tool
```

**這份 json 是你後面所有優化的量測依據**，看 §6 怎麼讀。

### 如果跑失敗

跳到 §11 找錯誤訊息對照。

---

## 5. 架構與 Pipeline 詳解

### 5.1 進入點

| 檔案 | 用途 | 你需要看嗎 |
|---|---|---|
| `main.py` | **主編排（最重要）** — 串接所有 agent | ✅ 必讀 |
| `run_evaluation.py` | 批次跑 benchmark 用 | ✅ 跑 baseline 用 |
| `run_math.py` | 純算術題快速渲染（用 template） | ❌ 不相關 |
| `app.py` | Streamlit UI | ❌ 不相關 |

### 5.2 Agent 模組（看這幾個就夠）

```
agents/
├── core/
│   ├── llm_client.py        ← LLM 多 provider 統一介面（OpenAI/Anthropic/Groq...）
│   ├── pipeline_config.py   ← 全域設定 + StageTimer（量測工具）
│   ├── rag_retriever.py     ← RAG（Weaviate 查相似範例）
│   └── logger.py            ← Session log
│
├── planner/
│   ├── planner.py           ← Planner 主 class
│   └── templates.py         ← Planner prompt（⚠️ 禁區，不可改）
│
├── coder/
│   ├── dspy_coder.py        ← Coder 入口（呼叫 Claude CLI）
│   ├── prompter.py          ← Coder prompt 組裝
│   ├── lint_manim.py        ← Manim API 規則 linter
│   ├── diagnoser.py         ← render 失敗時診斷錯誤類型
│   ├── misalign_fixer.py    ← 元素重疊的零成本 AST 修復
│   └── templates.py         ← Coder prompt 模板
│
├── orchestrator/
│   ├── refining_loop.py     ← ⭐ 核心迴圈：render → Vision QA → fix → repeat
│   └── task_router.py       ← 算術題 / 一般題的路由
│
└── utils/
    ├── audio_engine.py      ← Azure TTS
    ├── vision_agent.py      ← GPT-4o 看影片
    ├── final_judge.py       ← 最終 0-100 評分
    ├── benchmark_judge.py   ← (eval) candidate vs benchmark 對比
    ├── pairwise_judge.py    ← (eval) A/B pairwise 比較
    ├── layout_auditor.py    ← 元素位置稽核（preview 前先 deterministic check）
    ├── scene_instrumentor.py ← 注入 logging 到 Scene
    └── telemetry.py         ← run 階段 metadata 收集
```

### 5.3 完整 Pipeline 圖（詳細版）

```
                          run_evaluation.py
                                ↓ 載入測資
                            main.py
                                ↓
                        ┌────────────┐
                        │  Planner   │  Gemini Flash（OpenRouter）
                        │            │  → 產出視覺 JSON 腳本
                        └─────┬──────┘
                              │  parsed_script
                              ↓
        ┌─────────────────────┴─────────────────────┐
        │                                            │
        │   ThreadPoolExecutor（3 路並行）           │
        │                                            │
        │   ┌──────────┐ ┌──────┐ ┌─────────────┐   │
        │   │  Audio   │ │ RAG  │ │   Coder     │   │
        │   │  (Azure  │ │ (Wea │ │ (Claude     │   │
        │   │   TTS)   │ │ viate│ │  CLI Opus)  │   │
        │   └────┬─────┘ └──┬───┘ └──────┬──────┘   │
        │        │          │            ↑           │
        │        │          └ Coder 先 block 等 RAG  │
        │        │                                   │
        └────────┼───────────────────────────────────┘
                 │ 合併結果
                 ↓
        ┌────────────────────────────────────┐
        │   RefiningLoop (max_attempts=5)    │
        │   ┌──────────────────────────────┐ │
        │   │  [1/3] Lint (zero-cost)      │ │ ← 純 Python 規則檢查
        │   │  [2/3] Render (Manim)        │ │ ← 跑 manim subprocess
        │   │  [3/3] Vision QA (GPT-4o)    │ │ ← 看影片有沒有 bug
        │   └──────────────────────────────┘ │
        │   ↓ FAIL 就回去叫 Coder 修         │
        └────────────────┬───────────────────┘
                         │ PASS
                         ↓
                ┌──────────────────┐
                │   FinalJudge     │  Phase 1: code 分析（Opus）
                │   (兩階段)        │  Phase 2: vision pass × N（GPT-4o）
                └────────┬─────────┘
                         ↓
              stable_outputs/<topic>.mp4
              stable_outputs/cost_report.json
```

### 5.4 並行機制重點（看 `main.py:228-341`）

```python
# 用 ThreadPoolExecutor，max_workers=6
_pipeline_executor = ThreadPoolExecutor(max_workers=6)

# 3 路同時 submit
_rag_future = _pipeline_executor.submit(_rag_task)      # 行 226
_audio_future = _pipeline_executor.submit(_audio_task)  # 行 309
_coder_future = _pipeline_executor.submit(_coder_task)  # 行 334
# ↑ Coder 內部會 block 等 RAG 完成（行 313）

# 全部完成才繼續
_coder_result = _coder_future.result()
_audio_result = _audio_future.result()
_rag_result = _rag_future.result()  # 已 resolve（Coder 用過）
```

**關鍵：總 wall-clock = max(audio_time, coder_time + rag_time)**，不是三者相加。

如果你要做並行優化，記住這個式子 — 把 Audio 從 20s 縮到 10s 沒用（Coder 還在跑 60s），但把 Coder 從 60s 縮到 40s 就有效。

### 5.5 RefiningLoop 的 budget 系統

```python
# agents/core/pipeline_config.py
max_refine_attempts: int = 5  # 主迴圈最多跑 5 輪
visual_attempts_limit: int = 3
linter_retry_budget: int = 3  # ← 純 linter 失敗不算進主迴圈
tdr_t1_cap: int = 3           # 零成本 AST 修復上限
tdr_t2_cap: int = 2           # 小型 prompt 修復上限
```

**這些都不可改**（見 §8）。你要優化的是「每輪內部跑得更快」，不是「減少輪數」。

---

## 6. 量測工具：`cost_report.json`

每次跑完，`stable_outputs/cost_report.json` 會有這些欄位：

```json
{
  "total_prompt_tokens": 45230,
  "total_completion_tokens": 8120,
  "total_cost_usd": 0.0,

  "time_planner_sec": 2.3,
  "time_rag_sec": 1.1,
  "time_audio_sec": 18.4,
  "time_coder_sec": 65.7,
  "time_render_sec": 12.0,
  "time_vision_sec": 9.5,
  "time_final_judge_sec": 8.2,
  "vision_per_iter_sec": [3.1, 3.4, 3.0],

  "calls": [
    {"model": "...", "prompt_tokens": ..., "completion_tokens": ..., "elapsed": ...}
  ],

  "final_judge": {
    "verdict": "PASS",
    "weighted_total": 87.5,
    "scores": {...}
  }
}
```

### 怎麼讀

| 欄位 | 意思 | 怎麼用 |
|---|---|---|
| `time_*_sec` | 各階段累計耗時 | 找瓶頸 |
| `vision_per_iter_sec` | Vision QA 每輪各花多久 | 看是不是某一輪特別慢 |
| `total_prompt_tokens` | 全部 LLM input token 數 | 衡量 prompt 是否臃腫 |
| `final_judge.verdict` | PASS / FAIL | **驗證沒退化的關鍵** |
| `calls[]` | 每次 LLM 呼叫的細節 | debug 哪個 call 慢 |

### 30 題批次分析（手寫腳本）

```bash
# 跑完 30 題 baseline 後
ls runs/<timestamp>_variantA/Q*/cost_report.json | head

# 用 jq 算平均（每題 cost_report 在 runs/<ts>/Q###/）
for f in runs/<ts>/Q*/cost_report.json; do
    jq '[.time_planner_sec, .time_coder_sec, .time_vision_sec] | @csv' "$f"
done | python -c "
import sys, csv
rows = list(csv.reader(sys.stdin))
cols = list(zip(*[[float(x) for x in r] for r in rows]))
for name, col in zip(['planner','coder','vision'], cols):
    print(f'{name}: avg={sum(col)/len(col):.1f}s, max={max(col):.1f}s')
"
```

(也可以用現成的 `evaluation/compare_variants.py` 工具，看它的 `--help`)

---

## 7. 效能優化方向（你可以挑一個做）

下面列 6 個方向，**從最有把握到最投機**排序。**挑一個就好**，做完一個 PR 再挑下一個。

### 🥇 方向 A：Coder Claude CLI cold start

**痛點**：每題啟動一次 `claude` subprocess，cold start 約 5-15 秒（看你的網路）。30 題就是 2.5-7.5 分鐘純啟動時間。

**思路**：
- 改成 **persistent daemon**：跑一個常駐 `claude --print --resume` session，用 stdin 餵 prompt
- 或用 **batch mode**：累積多題後一次送
- 或評估改用 **Claude API**（要 owner 付錢）跟 CLI 取捨

**檔案**：`agents/core/llm_client.py` 找 `_call_claude_cli` 之類函數

**驗證**：`time_coder_sec` 平均下降 + `calls[]` 看每次 elapsed 變短

**難度**：⭐⭐⭐（要懂 subprocess + IO buffering）

---

### 🥈 方向 B：Vision QA 改成 async 或 batch

**痛點**：RefiningLoop 每輪 Vision QA 是串行 GPT-4o，最多跑 5 輪。`vision_per_iter_sec: [3, 3, 3, 3, 3]` = 15s 純等待。

**思路**：
- 用 `asyncio` + `aiohttp` 把 multi-frame 拆成並行 request
- 或先丟出推測性的修復 prompt，跟 Vision QA 並行跑（speculative execution）
- 或減少不必要的 frame（目前是 2x2 grid，看能不能降到 1 frame）

**檔案**：`agents/orchestrator/refining_loop.py` 行 1124-1210；`agents/utils/vision_agent.py`

**驗證**：`vision_per_iter_sec` 列表每項變小，**但 FinalJudge verdict 不能退化**

**難度**：⭐⭐⭐⭐（async 寫錯會卡死或 race condition）

---

### 🥉 方向 C：RAG cache

**痛點**：RAG 每題都查 Weaviate，但 30 題裡很多題的「知識點」是同一類（例如 5 題都是整數加減），其實可以 cache。

**思路**：
- 用題目的 `knowledge_point` 欄位當 cache key
- LRU cache 存記憶體；或 SQLite 持久化
- 注意 cache invalidation（kb 更新時要 bust）

**檔案**：`agents/core/rag_retriever.py`

**驗證**：`time_rag_sec` 平均下降；30 題裡同類問題第 2+ 次應該接近 0

**難度**：⭐⭐（基本 cache pattern）

---

### 方向 D：Azure TTS 並行 + 429 處理

**痛點**：Azure TTS 大量 eval 時容易 429 (rate limit)，目前是同步 retry，會卡住。

**思路**：
- 把多個 segment 改 async 並行送
- 429 加 exponential backoff
- 或評估 fallback 到本地 TTS（pyttsx3 / coqui）

**檔案**：`agents/utils/audio_engine.py`

**驗證**：`time_audio_sec` 在 30 題連跑時不再有極端值（從 60s spike 降到平穩 20s）

**難度**：⭐⭐⭐

---

### 方向 E：Render fps / 解析度調整

**痛點**：preview 已經是 fps=8 但 final render 是 fps=15，且解析度沒降。

**思路**：
- Vision QA 用 240p 而不是 480p，節省 ffprobe / ffmpeg 時間
- Final render 可以保留高品質，但中間 iteration 用更低
- 注意：解析度太低會讓 Vision QA 漏掉小字 bug

**檔案**：`agents/core/pipeline_config.py` (`fps_preview`, `fps_final`)；`agents/orchestrator/refining_loop.py` 找 `480p`

**驗證**：`time_render_sec` 下降；FinalJudge verdict 不退化

**難度**：⭐⭐（改參數為主，但要小心 vision 漏 bug）

---

### 方向 F（投機）：Planner / Coder prompt 縮短

**痛點**：prompt 越長 → input token 越多 → LLM 處理越慢。

**思路**：
- profile `total_prompt_tokens` 找出最大的 prompt
- 看能不能砍冗餘的 few-shot 範例
- 或改成 dynamic few-shot（只 retrieve 最相關 1-2 個範例，不是固定 5 個）

**檔案**：`agents/coder/prompter.py`、`agents/planner/templates.py`（⚠️ Planner templates 是禁區，要先跟 owner 提案）

**驗證**：`total_prompt_tokens` 下降 + `time_coder_sec` 下降 + verdict 不退化

**難度**：⭐⭐⭐⭐⭐（最容易把正確率搞壞）

---

### 該挑哪個？

- **第一次接觸 → 挑 C 或 D**（影響範圍小，好驗證）
- **想看到大效益 → 挑 A 或 B**（瓶頸最痛）
- **不要挑 F**（除非你已經做過 A-E 都不夠了）

挑好後，**先寫一個 issue 在 GitHub 上 claim 你要做哪個**，避免重工。

---

## 8. 禁區（絕對不要動）

從 `CLAUDE.md` 直接抄。動了會被 PR reject：

### 程式碼禁區
- ❌ `manimator/` — 第三方專案（雖然目前已被 gitignore，但別嘗試還原它做事）
- ❌ **Planner system prompt**（`agents/planner/templates.py` 內 prompt 字串）— **必須先跟 owner 提案**
- ❌ **RefiningLoop 主迭代上限 `max_refine_attempts=5`** — 已是性能/成本平衡點
- ❌ **`LINTER_RETRY_BUDGET=3` / `LAYOUT_RETRY_BUDGET=2` 等輔助 budget** — 動了會破壞 budget 邏輯
- ❌ **Audio / RAG / Coder 三路並行** — 不可改成序列，這是設計決策

### 行為禁區
- ❌ **`vision_agent.py` 的 `verdict=PASS` 閾值** — 動了會直接讓正確率假性上升
- ❌ `pre_render_patch()` 的零成本修復邏輯 — 動了可能讓某些 bug 無法自動修
- ❌ **任何把長 eval（30 題以上）自動化跑掉**的腳本 — owner 規定這要手動跑

### 不要 commit 的檔案
- ❌ `runs/` / `stable_outputs/` — 執行輸出
- ❌ `.env` — 你的 API key
- ❌ `test_script.py` / `test_script_q*.py` — 執行時暫存
- ❌ `*_log.json` / `*_audit.csv` — 都是執行產物
- ❌ `evaluation/benchmark_set/*.mp4` — 大檔案
- ❌ `參考文獻/` — 論文 PDF

這些都在 `.gitignore` 裡了，**不要為了測試方便去取消 ignore**。

---

## 9. 如果你用 AI 工具寫 code

學生用 Claude Code / Cursor / Copilot 很正常，但要遵守：

### 必做
1. **把 `CLAUDE.md` 整個丟給 AI 當 system context**（裡面有專案規範）
2. **跟 AI 強調禁區**（§8 整段貼給它）
3. **每次 AI 改完，你自己 review 一遍**才能 commit
4. **跑 syntax check**：
   ```bash
   python -c "import ast; ast.parse(open('agents/orchestrator/refining_loop.py').read())"
   ```
5. **跑單題 smoke test** 確認沒爛掉

### 不要做
- ❌ **讓 AI 自動 `git push`** — pre-push hook 會擋，而且 push 是不可逆操作
- ❌ **讓 AI 自動跑 30 題 eval** — owner 規定要人工跑
- ❌ **盲信 AI 的「我已經測過」** — AI 沒有真的跑你的環境
- ❌ **AI 一次改超過 5 個檔案** — 你 review 不完，會混進 bug

### 推薦的 AI 用法

```
Good：「我要實作方向 C（RAG cache）。讀 agents/core/rag_retriever.py
       的 retrieve() 函數，幫我加 LRU cache，key 用 knowledge_point。
       不要動其他檔案。」

Bad：「幫我優化這個專案。」
     （太籠統，AI 會亂改 + 動到禁區）
```

---

## 10. Git 工作流

### 你的分支：`perf/optimization`

```bash
# 確認你在這分支
git branch --show-current   # 應該是 perf/optimization

# 開始改 code 前先 pull（owner 可能更新 main，rebase 過來）
git pull origin perf/optimization
```

### Commit 規範

```bash
git add <你改的檔案>   # ⚠️ 不要 git add -A，避免誤加 ignored 檔
git commit -m "perf(coder): persistent claude CLI daemon

- 把 subprocess.Popen 改成常駐 session
- 用 stdin pipe 餵 prompt，省去 cold start

Before: time_coder_sec avg=65.7s
After:  time_coder_sec avg=41.2s (-37%)
30q PASS rate: 90% → 92% (不退化)"
```

**訊息格式**：
- 標題 `perf(<area>): <一句話>`（area = coder / vision / rag / audio / render）
- 內文：改了什麼 + 為什麼 + before/after 數字

### PR 規範

```bash
# 你的工作分支
git push origin perf/optimization

# 在 GitHub 開 PR：base = main, compare = perf/optimization
# PR description 模板：
```

```markdown
## 做了什麼
（一段話描述）

## 為什麼這樣做
（解釋思路 + 為何選這方向）

## Before / After 對比

跑 30 題 sample（`python run_evaluation.py --variant A --sample evaluation/experiment_sample_30.json`）：

| 階段 | Before (avg sec) | After (avg sec) | Δ |
|---|---|---|---|
| time_planner_sec | 2.3 | 2.3 | - |
| time_coder_sec | 65.7 | 41.2 | **-37%** |
| time_vision_sec | 9.5 | 9.4 | - |
| **total wall-clock** | 110.3 | 85.1 | **-23%** |

| 正確率 | Before | After |
|---|---|---|
| PASS / 30 | 27 (90%) | 28 (93%) |

## 風險 / 注意事項
（有沒有什麼會影響別人？）

## 測試方式
（owner 怎麼複測？）
```

### 禁止
- ❌ `git push --force` — 會洗掉別人的 commit
- ❌ 直接 push 到 `main` — 一定要走 PR
- ❌ 用 `git commit -a` — 容易誤加檔案
- ❌ 用 `git push --no-verify` — 跳過 hook，hook 是有理由的

---

## 11. 常見問題與 Debug

### Q1: `pip install -r requirements.txt` 失敗

通常是 Manim 的系統依賴沒裝。看 [Manim 官方安裝指南](https://docs.manim.community/en/stable/installation.html)。macOS 多半需要：
```bash
brew install py3cairo ffmpeg
brew install --cask mactex-no-gui   # LaTeX 渲染
```

### Q2: 跑 Q028 卡在 Coder 不動

最常見原因：**Claude CLI 沒登入**或 `CLAUDE_BIN` 路徑錯。
```bash
claude --version   # 確認能跑
which claude       # 確認路徑跟 .env 對得起來
```

### Q3: Azure 429 / TTS 失敗

```
❌ 語音生成發生錯誤: ... 429 Too Many Requests ...
```

跑單題不會發生，**跑 30 題連跑會**。先確認你的 `AZURE_SPEECH_KEY` 是 F0 (free) 還是 S0 (paid) tier。Free 很容易 429。

短期解法：題目間加 `sleep 10`。長期解法：見方向 D。

### Q4: Vision QA 一直 FAIL，跑滿 5 輪都不過

通常是兩種：
1. **真的 bug**：看 `vision_per_iter_sec` 跟 `final_judge.scores`，是不是元素重疊
2. **Vision 太嚴格**：看 `runs/<ts>/Q###/vision_audit_log.json`，verdict 寫什麼

如果是 2，**不要動 Vision threshold**（禁區），跟 owner 回報。

### Q5: `manim` command not found

```bash
# 確認在 venv 裡
source .venv/bin/activate
which manim

# 沒裝就重裝
pip install manim
```

### Q6: 我改完 code，怎麼確認沒爛掉？

```bash
# 1. Syntax check
python -c "import ast; ast.parse(open('<你改的檔>').read())"

# 2. 跑 3 題 smoke test（5 分鐘）
for q in Q028 Q024 Q070; do
    python run_evaluation.py --variant A --case $q \
        --sample evaluation/experiment_sample_30.json
done

# 3. 看 cost_report 數字有沒有合理
cat stable_outputs/cost_report.json | python -m json.tool | head -20

# 4. 確認 verdict 是 PASS
grep verdict stable_outputs/cost_report.json
```

### Q7: log 在哪？

| 用途 | 位置 |
|---|---|
| 完整 session log（stdout 重定向） | `logs/<timestamp>_<topic>.log` |
| 單題渲染結果 | `runs/<timestamp>/Q###/` |
| 最終 mp4 | `stable_outputs/<topic>_<timestamp>.mp4` |
| 成本/timing | `stable_outputs/cost_report.json`（單題）或 `runs/<ts>/Q###/cost_report.json`（批次） |
| Vision QA 細節 | `runs/<ts>/Q###/vision_audit_log.json` |
| Scene state | `runs/<ts>/Q###/scene_state_log.json` |

### Q8: 我懷疑某次 LLM call 特別慢，怎麼看？

```bash
cat stable_outputs/cost_report.json | jq '.calls[] | {model, elapsed}'
```

每個 call 都有 `elapsed`（秒），看是不是某個 model 特別慢。

---

## 12. Baseline 數字

> ⚠️ 待 owner 跑完 30 題 baseline 後回填

跑指令：
```bash
python run_evaluation.py --variant A --sample evaluation/experiment_sample_30.json
```

預期約 1-2 小時。完成後從 `runs/<timestamp>_variantA/` 算平均：

```
變數：variant=A (default)
樣本：evaluation/experiment_sample_30.json (30 題)
日期：YYYY-MM-DD
硬體：M2 Mac / 主機規格

階段平均（秒/題）：
  time_planner_sec:     __
  time_rag_sec:         __
  time_audio_sec:       __
  time_coder_sec:       __
  time_render_sec:      __
  time_vision_sec:      __    (per_iter avg: __)
  time_final_judge_sec: __
  TOTAL wall-clock:     __

正確率：__ / 30 PASS (__%)
Token 平均：input=__, output=__
成本平均：$__/題
```

**你的 PR 對比就拿這份當基準**。

---

## 13. 連絡與資源

### 卡住超過 30 分鐘 → 來問

不要硬撐，直接問 owner @childe0905：
- 環境/setup 問題 → 通常 5 分鐘解決
- 對某個檔案/機制看不懂 → 問 owner 或讀對應 agent 檔案
- 不確定優化方向是否合理 → 先問，不要做白工

### 參考檔案優先級

1. ⭐⭐⭐ `ONBOARDING.md`（本檔）— 從這開始
2. ⭐⭐⭐ `CLAUDE.md` — 專案規範（改 code 前必讀）
3. ⭐⭐ `.env.example` — 環境變數
4. ⭐⭐ `main.py` — 主編排邏輯（程式碼，但註解清楚）
5. ⭐⭐ `agents/orchestrator/refining_loop.py` — 核心迴圈
6. ⭐ `evaluation/benchmark_set/README.md` — benchmark 資料說明
7. （選讀）`.ai-context/HANDOFF.md` — owner 的歷史 session 進度，有點亂，挑相關看
8. （選讀）`.ai-context/BENCHMARK_JUDGE_DESIGN.md` — 評分系統設計

### 外部資源

- [Manim Community 文檔](https://docs.manim.community/en/stable/)
- [Claude Code CLI 文檔](https://docs.claude.com/en/docs/claude-code/overview)
- [Azure Speech SDK](https://learn.microsoft.com/azure/ai-services/speech-service/)

---

## 最後

歡迎加入。這個專案的設計權衡很多，**有疑問就問，不要默默改下去**。
你的目標是讓系統變快，不是重寫系統。

第一個 PR 不必很大，**先做方向 C（RAG cache）或 D（Audio 429）暖身**，
證明你能跑通完整流程：改 code → 跑 baseline → 對比 → 寫 PR。

加油 🚀
