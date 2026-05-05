# LLManim_Agent — Handoff Document

> 給任何新 AI（Claude / Gemini / ChatGPT / Cursor）的開場交接文件。
> 讀完這份文件即可接手，不需要問專案背景。
> **由 git post-commit hook 自動更新**，永遠對應最新 commit。

**更新時間**：2026-05-05
**Branch**：feat/core-and-agents

---

## 現在要做什麼

- [x] auto-inject set_subtitle run_time from TTS duration (commit 9d29d9c)
- [ ] 提交 agents/core/llm_client.py 的改动（13行，claudealt 帐号月费订阅验证）
- [ ] 检查 .agent/skills/karpathy-guidelines/ 的用途和是否需要 commit
- [ ] 分析 eval failures 根本原因（5 TIMEOUT、hallucination、syntax 错误）
- [ ] 跑新 evaluation 验证 pass rate 提升至 80%+

## 上次 Session 改了什麼

| 檔案 | 改了什麼 | 注意事項 |
|------|----------|----------|
| `.ai-context/HANDOFF.md` | 新增（91行），完整交接文档 | Stop hook 自动生成，包含任务/架构/踩坑清单 |
| `.ai-context/CHANGELOG.md` | stop hook 自动记录（+20/-2） | 增量更新，dedup 修复完成 |
| `.ai-context/CONTEXT.md` | 精简（删除重复，+/-67） | 内容已合并至 MEMORY.md |
| `agents/core/llm_client.py` | subprocess 路由调整（13行改） | **未 commit**，待测试 claudealt 帐号月费订阅 |
| `.agent/skills/karpathy-guidelines/` | 新增文件夹 | **待确认**用途和是否需纳入版控 |

## 踩過的坑（新 AI 最容易重犯）

- **`LayoutObject` / `LayoutEngine` / `LayoutSolver`** 是幻覺 API，lint rule 13 會攔截，不要用
- **Triangle 必須用 `Polygon(A,B,C)`**，不能用 3 個 `Line` 物件
- **`Line`/`Arrow` 有 `start`/`end` 就不能再 `move_to`**（雙重 offset）
- **`step_explanation` footer Text** 已禁止（會跟字幕衝突）
- **`manimator/`** 是第三方 submodule，絕對不能改
- **3b1b/videos** 是 ManimGL，本專案是 ManimCE，不能 copy-paste
- **RefiningLoop 最多 5 次**，不要調高

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
