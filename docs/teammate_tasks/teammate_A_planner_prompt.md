# 組員 A 任務說明 — Planner Prompt 優化

> 這份文件是你的完整工作說明，不需要看其他文件也能執行。
> 有問題直接問 @liaozhenting。

---

## 你在做什麼

這個專案會把數學題目自動轉成教育動畫影片。整條流程：

```
題目 → [Planner] → JSON blueprint → [Coder] → Manim code → 影片
```

**你只負責 Planner 這一塊**。Planner 的工作是把題目設計成「動畫藍圖」（JSON），告訴後面的 Coder 要畫什麼、放哪裡、怎麼教。

**你的任務**：Planner 的 system prompt 現在有 380 行，太長了。你要在不犧牲品質的前提下，讓它變短（目標 -30% token）。短 = 便宜 + 快。

**你不需要懂 Manim，不需要跑渲染，不需要看影片。** 你的工作完全在 Python + LLM 層面。

---

## 環境 Setup（10-15 分鐘）

### 1. Clone 專案

```bash
git clone <repo_url>
cd LLManim_Agent
```

### 2. 安裝依賴

```bash
pip install -r requirements.txt
```

如果 `weaviate-client` 安裝失敗，單獨裝它（其實你不用跑 Weaviate，只是 import 會用到）：
```bash
pip install weaviate-client
```

### 3. 設定 .env

跟 @liaozhenting 要 `.env` 檔，放到專案根目錄。你至少需要：

```
OPENROUTER_API_KEY=...   # 用來跑 judge（Claude Opus 4.7 via OpenRouter）
DEEPSEEK_API_KEY=...     # preflight 會檢查這個，沒設會卡住（你不用它，但要有）
PLANNER_MODEL=claude-code-planner-full
```

> 注意：Planner 本身走 Claude Code CLI 月費，不消耗 OpenRouter token。
> 你不需要 AZURE_SPEECH_KEY、OPENAI_API_KEY。

### 4. 驗證環境

```bash
python run_planner_eval.py --dry-run
```

看到 `✅ Dry run successful!` 就代表環境 OK 了。如果失敗，截圖給 @liaozhenting。

---

## 你要改的檔案（只有這三個）

| 檔案 | 你可以改什麼 |
|---|---|
| `agents/planner/templates.py` | `OPUS_PLANNER_SYSTEM_PROMPT`（精簡版 prompt 的內容） |
| `agents/planner/planner.py` | 路由邏輯（讓 `claude-code-planner-compact` alias 可以用） |
| `run_planner_eval.py` | 只能改 `MODELS` list 和 `SELECTED_CASES`，**不要動其他東西** |

**嚴禁改動的檔案**（不要碰，碰了會破壞整條 pipeline）：
- `agents/orchestrator/refining_loop.py`
- `agents/core/llm_client.py`
- `agents/coder/`（整個目錄）
- `agents/utils/`（整個目錄）
- `run_planner_eval.py` 的 judge 邏輯（`JUDGE_SYSTEM`、`WEIGHTS`、`JUDGE_MODEL`）

---

## 評分工具說明

你的主要武器是 `run_planner_eval.py`：

- **只跑 Planner 階段**（不跑 Coder、不渲染）
- 用 **Claude Opus 4.7 當 judge**，4 維度評分（1-5 分）：
  - `math_accuracy` — 視覺是否正確表達數學概念（權重 30%）
  - `pedagogy` — 步驟是否利於教學（25%）
  - `spatial_design` — 座標是否合理、物件不重疊（25%）
  - `feasibility` — 計畫在 Manim 裡能否實作（20%）
- 每題跑 3 次取平均，產出 `weighted_total`（1-5 分）

**使用方式**：
```bash
python run_planner_eval.py --dry-run   # 測環境，跑 1 題
python run_planner_eval.py             # 完整 eval
python run_planner_eval.py --resume 20260508_143000  # 從斷點繼續
```

結果存在 `runs/{timestamp}/judge_scores/` 底下，格式是 JSON。

---

## 執行步驟（Day by Day）

### Day 1 — Setup + 讀 code

1. 照上面 Setup 跑通 `--dry-run`
2. 讀 `agents/planner/templates.py`：
   - `PLANNER_SYSTEM_PROMPT`（380 行，現在 production 在用的版本）
   - `OPUS_PLANNER_SYSTEM_PROMPT`（127 行，已寫好但沒被啟用）
3. 讀 `agents/planner/planner.py` 第 1-30 行，理解 alias 路由邏輯

### Day 2 — 建立 Baseline

**Step 1**：修改 `run_planner_eval.py` 的 `MODELS` list（行 34-44）：

```python
MODELS = [
    {"id": "opus-full",    "model": "claude-code-planner-full",    "thinking": False},
    {"id": "opus-compact", "model": "claude-code-planner-compact", "thinking": False},
]
```

**Step 2**：修改 `SELECTED_CASES`（行 46），擴充到 12 題（從 `evaluation/test_cases.json` 挑，涵蓋 ELEM/MID/HIGH 各 4 題）：

```python
SELECTED_CASES = [
    "ELEM_01", "ELEM_02", "ELEM_03", "ELEM_04",
    "MID_01",  "MID_02",  "MID_03",  "MID_04",
    "HIGH_01", "HIGH_02", "HIGH_03", "HIGH_04",
]
```

**Step 3**：在 `agents/planner/planner.py` 確認路由（行 10-11）：
```python
_OPUS_COMPACT_ALIASES = {"claude-code-planner-compact"}
_OPUS_FULL_ALIASES    = {"claude-code-planner", "claude-code-planner-full"}
```
如果 `claude-code-planner-full` 不在 `_OPUS_FULL_ALIASES`，加進去。

**Step 4**：跑 baseline：
```bash
python run_planner_eval.py
```

**Step 5**：把 `opus-full` 的結果記錄下來（這是 baseline，後面所有實驗都跟它比）：

| 維度 | Baseline (opus-full) |
|---|---|
| math_accuracy | ? |
| pedagogy | ? |
| spatial_design | ? |
| feasibility | ? |
| weighted_total | ? |
| prompt tokens (avg) | ? |
| 時間 (avg sec) | ? |

### Day 3-4 — 實驗 1 + 2

**實驗 1**：直接跑 `opus-compact`（127 行版），看 4 維度跟 baseline 的差距。

重點看：
- 哪個維度掉最多？
- 哪些維度幾乎沒變？

**實驗 2**：如果某個維度下降 > 0.5 分，從 380 行版找出對應的 section，合併進精簡版做「混合版」。

例如 `spatial_design` 掉很多 → 從 `PLANNER_SYSTEM_PROMPT` 的 `PHASE 1: NEURO-SYMBOLIC REASONING` section 把 layout zones 說明加回來。

> 改 `OPUS_PLANNER_SYSTEM_PROMPT` 的內容，不要動 `PLANNER_SYSTEM_PROMPT`。

### Day 5 — 實驗 3（邊際貢獻分析）

把混合版的每個 section 逐一刪掉，各跑一次 eval，記錄哪個 section 對哪個維度貢獻最大。

| Section | 刪掉後 spatial_design 變化 | 刪掉後 feasibility 變化 |
|---|---|---|
| Layout zones | ? | ? |
| Banned classes | ? | ? |
| Key rules | ? | ? |
| ... | ... | ... |

找出「最小可用版」（刪掉也不影響任何維度超過 0.2 分的 section 全部刪掉）。

### Day 6 — 開 PR

開一個 Pull Request，標題：

```
feat: planner prompt slimming (opus-compact, -30% tokens)
```

PR 描述必須附：

1. **Before/After 對比表**（所有數字從 `runs/{ts}/judge_scores/` 抓，不要手填）
2. **邊際貢獻分析結果**（哪些 section 不可少、哪些砍掉沒差）
3. 你做了哪些實驗、結論是什麼

---

## 驗收標準

@liaozhenting 在 review 你的 PR 時會看這些數字：

| 指標 | 必須達到 |
|---|---|
| Planner input tokens | 比 baseline 少 ≥ 30% |
| weighted_total | 比 baseline 下降 ≤ 0.3 分 |
| spatial_design | 不低於 baseline - 0.5 分，且絕對值 ≥ 3.5 |
| 任一維度 | 絕對值 ≥ 3.5 |

---

## 常見問題

**Q：跑到一半 API timeout 怎麼辦？**
用 `--resume {timestamp}` 從上次斷點繼續，不用重跑。

**Q：judge 的分數每次跑有差異很正常嗎？**
正常，所以每題跑 3 次取平均。如果你覺得某題分數很奇怪，可以去 `runs/{ts}/judge_scores/{model}/{case}/` 看 judge 的 rationale 解釋。

**Q：我可以改 OPUS_PLANNER_SYSTEM_PROMPT 以外的東西嗎？**
只能改上面表格列出的檔案。有疑問先問 @liaozhenting。

**Q：我需要懂 Manim 嗎？**
不需要。但你要能看懂 `spatial_design` 的 judge rationale（會說「物件超出 y 邊界」之類），知道它在講什麼。

---

## 目錄結構（你需要關心的部分）

```
LLManim_Agent/
├── agents/
│   └── planner/
│       ├── planner.py          ← 路由邏輯
│       └── templates.py        ← Prompt 內容（你的主要工作在這）
├── evaluation/
│   └── test_cases.json         ← 題庫（挑 SELECTED_CASES 用）
├── run_planner_eval.py         ← 評分工具（主要武器）
├── runs/                       ← eval 結果自動存在這
└── .env                        ← API keys（跟 @liaozhenting 要）
```
