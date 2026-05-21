分析 LLManim_Agent 的 evaluation session 結果。

**如果用戶提供了參數 `$ARGUMENTS`**，分析 `runs/$ARGUMENTS/` 這個 session。
**如果沒有提供參數**，找 `runs/` 下按字母排序最新的 session 目錄。

## 資料來源優先順序
1. `summary.csv` — 主要資料來源（Status, FJ scores, cost, stage timing, tokens）
2. `reasoning_summary.md` — 各 case 的 Vision Audit defects 詳細內容
3. `thought_trace.log` — 失敗 case 的 error message（只在分析失敗原因時讀）
4. `code.py` — 最終代碼（只在需要深入分析時讀）

## 失敗判定邏輯
- Status = "Failed" → 失敗（cost_report 缺失 or 達到最大嘗試次數）
- Vision verdict != PASS → 警告（從 reasoning_summary.md 讀）
- 兩者皆列入「失敗 / 警告案例」

---

輸出以下分析：

## Session 摘要
- Session ID、總 case 數、成功/失敗數、成功率
- FinalJudge 平均分（Weighted / Math / Concept / Visual），只計成功 case

## 成本分析表
從 summary.csv 讀取，按 Cost USD 降序排列：

| Case ID | Cost USD | Prompt Tokens | Completion Tokens | Planner(s) | Coder(s) | Render(s) | Vision(s) |
最後一行加總 / 平均。

## FinalJudge 分數表
從 summary.csv 讀取 FJ Weighted / FJ Math / FJ Concept / FJ Visual：

| Case ID | Weighted | Math | Concept | Visual | Iterations |
按 Weighted 降序排列，失敗 case 標 "—"。

## 失敗 / 警告案例
對每個失敗 case：
1. 從 thought_trace.log 找具體 error message
2. 說明 defects 內容（若有 reasoning_summary.md）
3. 推測根本原因

## 模式洞察
- 哪個階段最耗時？（比較 Planner Sec / Coder Sec / Render Sec / Vision Sec 平均值）
- 最貴的 3 個 case 有什麼共同點？
- FJ 分數最低的 case 失敗模式？
- 如果有失敗案例，失敗模式是否有規律？

輸出語言：繁體中文。