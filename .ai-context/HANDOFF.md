# LLManim_Agent — Handoff

> 給任何新 AI（Claude / Gemini / ChatGPT / Cursor）的開場文件。
> **純手寫，不自動更新**。內容若與 `git log` / 程式碼衝突，以 git 跟 code 為準。
> 想知道「上次改了什麼」請看 `git log --oneline -20`，不要在這找。

---

## 1. 當前焦點

<!-- SECTION_1_UPDATED_AT: 2026-05-21 -->
- **Active**: FJ Phase 2 切 Opus 預設完成（`.env FJ_VISION_BACKEND=opus`）+ A 組 5 題假 FAIL rescore 後全 PASS、A 組真實 30/30；benchmark_set 30 題字幕改寫 27 題待人工核對
- **Next**: 重跑 A vs C 30 題 full Opus eval 拿完整 baseline，或推進 BJ benchmark_set 30 題精修（下個 session 拍板）
- **Blocked**: 無

> 改動規則：完成就直接覆寫，不留歷史、不打勾、不加日期。歷史去 git log 查。
> Section 1 由 `/handoff` slash command 維護。

---

## 2. 踩坑鐵律（append-only，不要刪）

### Manim API 幻覺
- `LayoutObject` / `LayoutEngine` / `LayoutSolver` 不存在，lint rule 13 會攔
- Triangle 用 `Polygon(A,B,C)`，**不要用 3 個 `Line`** 拼
- `Line`/`Arrow` 已給 `start`/`end` 就**不能再 `move_to`**（雙重 offset）
- `step_explanation` footer `Text` 已禁用（撞字幕）

### 專案鐵律
- `manimator/` 是第三方 submodule，**絕對不改**
- `3b1b/videos` 是 ManimGL，本專案 ManimCE，**只能參考邏輯不能 copy**
- `RefiningLoop` 主迭代上限 5，**不要調高**
- `pre_render_patch()` 只做確定性修復，**不加 LLM call**
- Planner / RAG / Audio **平行執行**，不要改成串行
- Linter 有獨立 `LINTER_RETRY_BUDGET=3`，**不消耗主迭代**
- Planner system prompt **改前必先問用戶**
- `git push` 由用戶執行（pre-push hook 需互動），AI 只到 commit

### LLM 路由現況
- Planner: `google/gemini-2.5-flash`（OpenRouter）
- Coder: `claude-opus-4-7` via `claudealt` 系統帳號 subprocess（月費 quota，不扣 API token）
- Vision: `gpt-4o`（OpenAI 直連）
- FinalJudge / BenchmarkJudge: Claude Code 訂閱（已遷出 OpenRouter）

### Claude Code CLI 冷知識
- **月費訂閱可看本地圖**：`--tools "Read" --add-dir <dir>` 讓 Opus 自己 Read jpg/png，扣 quota 不扣 API
- `_call_claude_code` 預設 `--tools ""` 禁用工具，要看圖**必須 override**
- `-p` 模式**沒有 image flag**，只能透過 Read tool 路徑載圖
- 切 claudealt：`sudo -u claudealt claude logout && sudo -u claudealt -i claude login`

---

## 3. 架構一句話

```
題目 → TaskRouter
  ├─ 算術 → templates/ (deterministic)
  └─ 一般 → Planner(gemini-2.5-flash) ∥ RAG ∥ Audio
              → Coder(opus via claudealt)
              → RefiningLoop(≤5, lint+RAG)
              → VisionAgent(gpt-4o) QA
```

---

## 4. 環境

- `.env` 必填：`GROQ_API_KEY` `DEEPSEEK_API_KEY` `AZURE_SPEECH_KEY` `AZURE_SPEECH_REGION` `OPENAI_API_KEY`
- `AUDIO_BACKEND=azure`（大量 eval 易 429，單題沒問題）
- Claude memory（只有 Claude 看得到）：`~/.claude/projects/-Users-liaozhenting-Desktop-LLManim-Agent/memory/MEMORY.md`
- Session logs：`runs/{TIMESTAMP}/`

---

## 開場 prompt（複製貼給任何 AI）

```
請先讀 .ai-context/HANDOFF.md 跟 CLAUDE.md，然後用一句話告訴我你理解的「當前焦點」，不要問我專案背景。
```
