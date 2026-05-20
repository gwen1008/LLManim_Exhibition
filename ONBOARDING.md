# 組員 Onboarding — LLManim_Agent 效能優化

## 你的任務

**降低單題生成 wall-clock 時間，不能讓正確率下降。**

成功標準：拿 30 題 sample 跑前後對比，總時間明顯降低 + 正確率（FinalJudge verdict）不退化。

---

## 5 分鐘跑起來

```bash
# 1. clone + 切到你的分支
git clone git@github.com:childe0905/LLManim_Agent.git
cd LLManim_Agent
git checkout perf/optimization

# 2. Python 環境（建議 venv 或 conda）
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. 環境變數
cp .env.example .env
# 編輯 .env：OPENAI_API_KEY / AZURE_SPEECH_KEY / AZURE_SPEECH_REGION 跟 owner 拿
# 其他 key 可先空著（有 default）

# 4. Coder 走 Claude Code CLI 訂閱（不是 API），需先安裝並登入：
# 跟 owner 確認你用哪個帳號（claudealt or 你自己的）

# 5. 跑單題 smoke test（~2-3 分鐘）
python run_evaluation.py --variant A --case Q028 --sample evaluation/experiment_sample_30.json

# 成功會在 stable_outputs/ 看到 cost_report.json，包含所有 timing 欄位
```

---

## Pipeline 一頁圖

```
main.py
  ├─ TaskRouter             (算術題用 deterministic template 直接渲染，不走 LLM)
  └─ Planner (Gemini Flash) ─→ visual plan JSON
        │
        ├──────── ┬──────────── ┬───────────┐  ← ThreadPoolExecutor 三路並行
        │         │              │           │
        Audio     RAG            Coder       │
       (Azure)   (Weaviate)    (Opus CLI)    │
        │         │              ↑           │
        │         └─ Coder 先 block 等 RAG ──┘
        │
        ▼
   RefiningLoop (主迴圈 ≤5 iter)
        │
        ├─ Render (Manim) → 失敗則 Coder 修
        └─ Vision QA (GPT-4o) → 視覺有問題則 Coder 修
        │
        ▼
   FinalJudge (兩階段：code analysis + vision pass × N)
        │
        ▼
   stable_outputs/cost_report.json  ← 所有 timing 在這
```

---

## 量測工具：`cost_report.json`

每次跑完 `run_evaluation.py`，每題的 `cost_report.json` 都會有以下欄位（單位：秒）：

```json
{
  "time_planner_sec": 2.3,
  "time_rag_sec": 1.1,
  "time_audio_sec": 18.4,
  "time_coder_sec": 65.7,
  "time_render_sec": 12.0,
  "time_vision_sec": 9.5,
  "time_final_judge_sec": 8.2,
  "vision_per_iter_sec": [3.1, 3.4, 3.0],
  "total_prompt_tokens": ...,
  "total_completion_tokens": ...,
  "total_cost_usd": ...,
  "final_judge": { "verdict": "PASS", ... }
}
```

**改完任何優化前後，都用這個檔的數字證明你動到的階段真的變快**（不是「感覺有快」）。

**注意 Audio / RAG / Coder 三者是並行的** — 三段時間相加 ≠ 總 wall-clock。瓶頸是「最慢那條」，不是總和。

---

## 已知熱點（先量測再動手，不要瞎猜）

| 階段 | 為什麼可能慢 | 量測欄位 |
|---|---|---|
| Coder | 每題啟動一次 Claude CLI subprocess，cold start ~5-15s | `time_coder_sec` |
| RefiningLoop Vision QA | 每輪串行 GPT-4o，最多 5 輪 | `vision_per_iter_sec` |
| Audio (Azure TTS) | 大量 eval 時容易 429 retry | `time_audio_sec` |
| RAG (Weaviate) | 待量測，可能不是瓶頸 | `time_rag_sec` |
| Render (Manim) | preview fps=8 已優化，但 final fps=15 還是吃時間 | `time_render_sec` |

---

## 🚫 禁區（絕對不要動）

從 `CLAUDE.md` 抄出來，這些動了會被 reject：

- `manimator/` — 第三方專案（目前已被 gitignore，但別碰它的概念）
- **Planner system prompt 不可改** — 必須先跟 owner 提案
- **RefiningLoop 主迭代上限 5 不可加** — 已是性能/成本平衡點
- **Audio / RAG / Coder 三者並行不可改成序列** — 並行是設計決策
- **`LINTER_RETRY_BUDGET=3` / `LAYOUT_RETRY_BUDGET=2` 等輔助 budget 不可動**
- **不要 commit**：`runs/` / `stable_outputs/` / `test_script.py` / `.env` / `evaluation/benchmark_set/*.mp4` / `參考文獻/`
- **不要動 `vision_agent.py` 的 `verdict=PASS` 閾值**（會直接影響正確率）

---

## 如果你用 AI 工具（Claude Code / Cursor / Copilot）

1. **必讀** `CLAUDE.md`（專案規範）— 把它丟給 AI 當 system context
2. **如果你拿到 owner 給的 memory 目錄**（`memory/MEMORY.md` 等），也讀
3. 禁區同樣適用 AI 生成的 code — 你 review 過才能 commit
4. **別讓 AI 自動 `git push`**（pre-push hook 限制，會掉 hook、有 token 問題）
5. AI 改完後一定要 `python -c "import ast; ast.parse(open('main.py').read())"` 等做 syntax check

---

## 工作流

- **你的分支**：`perf/optimization`（已建好）
- **每個議題**：建議在 `perf/optimization` 上直接 commit，commit 訊息寫清楚改了什麼+為什麼
- **PR 目標**：`main`，由 owner review
- **每個 PR 必附**：baseline 前後 30 題對比表（用 cost_report.json 的數字）
  - 範例格式：

    | 階段 | Before (sec, avg) | After (sec, avg) | Δ |
    |---|---|---|---|
    | time_coder_sec | 65.7 | 41.2 | -37% |
    | total | 110.3 | 85.1 | -23% |
- **不要 force push、不要碰 main、不要 push --force**
- 一般 `git push origin perf/optimization` 是 OK 的

---

## Baseline 數字（owner 會回填）

跑 30 題 sample 後填這裡：

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
```

跑 baseline 指令（owner 執行）：
```bash
python run_evaluation.py --variant A --sample evaluation/experiment_sample_30.json
```

---

## 連絡

有問題直接問 owner（@childe0905）。卡住超過 30 分鐘就問，不要硬撐。

額外資源：
- `CLAUDE.md` — 專案規範總覽
- `.ai-context/HANDOFF.md` — 最近的 session 進度（有點亂，挑相關的看）
- `evaluation/benchmark_set/README.md` — benchmark 資料說明
