# LLManim_Agent — Handoff Document

> 給任何新 AI（Claude / Gemini / ChatGPT / Cursor）的開場交接文件。
> 讀完這份文件即可接手，不需要問專案背景。
> **由 git post-commit hook 自動更新**，永遠對應最新 commit。

**更新時間**：2026-05-20
**Branch**：main

---

## 現在要做什麼

- [x] KB150 v2 完全發佈：29 題 docstring 注入 + Weaviate ingestion 完成
- [x] GT-match \frac 修復
- [ ] 切換 main.py RAG collection 預設到 ManimKB150v2
- [ ] BenchmarkJudge runner path adapter 實作
- [ ] benchmark_set 30 題精修狀態確認（目前全 draft，awaiting manual curation）
- [ ] kb_quick_audit 驗證腳本完成

## 上次 Session 改了什麼

| 檔案 | 改了什麼 | 注意事項 |
|------|----------|----------|
| `knowledge_base/kb150_v2/` (29 files) | 注入 teaching method docstring (+2936 lines) | f082c31：docstring 已進 Weaviate ManimKB150v2 collection |
| `rag/ingest_code.py` + `ingest_rules.py` | docstring 擷取與 metadata 優化 (+39 lines) | 472b02a：v2 RAG ingestion pipeline 完整 |
| `agents/utils/final_judge.py` | normalize \frac{a}{b} → a/b 前置處理 | de4cc85：修復字串匹配 bug，GT-match 穩定度提升 |
| `run_evaluation.py` | self-check + BenchmarkJudge 整合 (+63 lines) | bc23f61/0e0baab：B-track 系統完整 |
| `main.py` | 支援 RAG_COLLECTION 環境變數 (+20 lines) | 預設仍需手動切至 ManimKB150v2 |

## 踩過的坑（新 AI 最容易重犯）

- **`LayoutObject` / `LayoutEngine` / `LayoutSolver`** 是幻覺 API，lint rule 13 會攔截，不要用
- **Triangle 必須用 `Polygon(A,B,C)`**，不能用 3 個 `Line` 物件
- **`Line`/`Arrow` 有 `start`/`end` 就不能再 `move_to`**（雙重 offset）
- **`step_explanation` footer Text** 已禁止（會跟字幕衝突）
- **`manimator/`** 是第三方 submodule，絕對不能改
- **3b1b/videos** 是 ManimGL，本專案是 ManimCE，不能 copy-paste
- **RefiningLoop 最多 5 次**，不要調高
- **Claude Code CLI 月費訂閱可看本地圖**：用 `--tools "Read" --add-dir <dir>` 讓 Opus 自己 Read jpg/png；月費 quota 計（不扣 API）。`_call_claude_code` 預設 `--tools ""` 禁用工具，要看圖必須 override。`-p` 模式無 image flag，**只能透過 Read tool 路徑載圖**

---

## 架構一句話

```
自然語言題目 → TaskRouter
  ├── 算術題 → templates/（deterministic，100% 正確）
  └── 一般題 → Planner(gemini-2.5-flash) → Coder(claude-opus-4-7 via claudealt) 
               → RefiningLoop(≤5次, RAG+lint) → VisionAgent(gpt-4o) QA
```

**關鍵限制**：
- Planner / RAG / Audio 三者**平行執行**，不要改成串行
- `pre_render_patch()` 只做確定性修復，不加 LLM call
- Linter 失敗有獨立 budget（`LINTER_RETRY_BUDGET=3`），不消耗主迭代次數

---

## 環境與帳號

- `.env` 需要：`GROQ_API_KEY`, `DEEPSEEK_API_KEY`, `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`, `OPENAI_API_KEY`
- Coder 走 `claudealt` 系統帳號（月費 Claude Max），切換用 `sudo -u claudealt claude logout && sudo -u claudealt -i claude login`
- TTS：`AUDIO_BACKEND=azure`（大量 eval 會 429，single topic 沒問題）

---

## 硬限制（不要挑戰）

- `manimator/` 是第三方 submodule，不可改
- RefiningLoop 最多 5 次迭代（`MAX_ITERATIONS=5`）
- ManimCE 相容性必須保持（3b1b repo 只能參考邏輯不能 copy）
- `pre_render_patch()` 只做確定性修復，不加 LLM call
- Planner / RAG / Audio 三者平行執行，不要改成串行

---

## 外部資源

- Session logs：`runs/{TIMESTAMP}/`
- Evaluation cases：`evaluation/` + `run_evaluation.py`
- Claude Code 記憶（只有 Claude 看得到）：`~/.claude/projects/-Users-liaozhenting-Desktop-LLManim-Agent/memory/MEMORY.md`

---

## 開場 prompt（複製貼給任何 AI）

```
請先讀 .ai-context/HANDOFF.md，然後用一段話告訴我你理解的「現在要做什麼」，不要問我專案背景。
```
