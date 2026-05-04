# LLManim_Agent — Active Context

> 給跨 AI 協作用（ChatGPT / Cursor / Gemini）。
> 規則：只放「現在進行 + 最近決策」。超過 100 行就砍舊的。
> Claude Code 用戶請參考 `~/.claude/projects/-Users-liaozhenting-Desktop-LLManim-Agent/memory/MEMORY.md`（自動載入）。

**更新日期**：2026-05-04
**當前 branch**：`feat/core-and-agents`

---

## 🎯 現在在做什麼

- Pipeline context / telemetry / final judge 元件整合
- A/B 測試流程（Route A vs Route B），輸出在 `ab_test_runs/`
- 多題批次評測（`run_ab_batch_20.py`、`test_script_q*.py` 是 per-question runtime 暫存檔）

## 🧠 最近的關鍵決策（新→舊，最多 10 條）

- **2026-05-02**：移除舊版 agents 和過時的 dev_tools，重構 rag_retriever 並大幅簡化 ingest_3b1b.py，移除 424 行冗餘程式碼，以清理專案結構並減少維護負擔

- **2026-05-02**：移除舊版 agents 和過時的 dev_tools，重構 rag_retriever 並大幅簡化 ingest_3b1b.py，移除 424 行冗餘程式碼，以清理專案結構並減少維護負擔

- **2026-05-02**：移除舊版 agents 和過時的 dev_tools，重構 rag_retriever 並大幅簡化 ingest_3b1b.py，移除 424 行冗餘程式碼，以清理專案結構並減少維護負擔

- **2026-05-02**：移除舊版 agents 和過時的 dev_tools，重構 rag_retriever 並大幅簡化 ingest_3b1b.py，移除 424 行冗餘程式碼，以清理專案結構並減少維護負擔








## 🚧 未完成 / 卡點

- [ ] 20+ 個 `test_script_q*.py` 未 gitignore，git status 髒（2026-04-22 待處理）
- [ ] `ab_test_runs/`、`stable_outputs_route_b/` 要決定是 gitignore 還是加進版控
- [ ] 上次 eval（20260329）僅 8/15 pass（53%），TIMEOUT × 5 還沒根因分析
- [ ] `knowledge_base/examples` 和 `manimator` 檔案被標記為 dirty，需確認是否為 submodule 或空目錄變更

## 🧱 硬限制（不要挑戰）

- `manimator/` 是第三方 submodule，不可改
- RefiningLoop 最多 5 次迭代（`MAX_ITERATIONS=5`）
- ManimCE 相容性必須保持（3b1b repo 只能參考邏輯不能 copy）
- `pre_render_patch()` 只做確定性修復，不加 LLM call

## 🔌 外部資源對照

- Claude Code 記憶：`~/.claude/projects/-Users-liaozhenting-Desktop-LLManim-Agent/memory/MEMORY.md`
- 專案規則：`CLAUDE.md`（repo root）
- Session logs：`runs/{TIMESTAMP}/`
- Evaluation：`evaluation/` + `run_evaluation.py`

---

**開場貼給其他 AI 的 prompt 模板**：
```
請先讀這個 LLManim_Agent 專案的當前 context，再回答我問題：
[貼上這份 CONTEXT.md 全文]
```
