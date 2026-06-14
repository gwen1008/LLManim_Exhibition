產生 LLManim_Agent benchmark eval 的**正確命令**讓用戶手動執行。

## 鐵則(來自反覆踩過的坑)
- **不要自動跑全批**。≥10 題一律只印命令,讓用戶自己跑(CLAUDE.md `## Execution Boundaries`)。
- 只在用戶明說「smoke / 試跑」時,才實際執行 ≤3 題的小子集。
- flag 別搞錯:
  - `--test-cases <path>` = 測試案例 **JSON 檔路徑**(別名 `--sample`)。
  - `--cases <ID,ID>` = 跑哪幾個 **Case ID**,逗號分隔(別名 `--qids`)。**不是 `--cases <檔案>`**。
  - `--case <ID>` = 單一 case。`--case` 與 `--cases/--qids` 互斥。
- runner 入口:`python run_evaluation.py`(repo root,不是巢狀 LLManim_Agent/)。

## 解析 `$ARGUMENTS`
用戶可能給:題號清單(`Q026,Q123`)、檔名(`q20`)、variant(`A/B/C`)、`resume`、`smoke`。
判斷規則:
- 看起來像 `Qxxx` / `Hxx` 逗號清單 → `--cases`。
- 看起來像檔名片段(`q20`、`ab30`)→ 對到 `evaluation/test_cases_*.json` 的 `--test-cases`。
- `A`/`B`/`C` → `--variant`。
- 「resume <dir>」→ `--resume runs/<dir>`。

## Resume 注意(踩過的 bug)
- `--resume` 接 **session 目錄**(如 `runs/20260321_020857`)。
- 提醒用戶:resume 邏輯曾把 **Failed case 當已完成跳過**。resume 前先確認要不要重跑 Failed;若要,得先從 session 目錄移除那些 Failed 的產出,否則會被略過。

## 預設測試檔對照
- 全套:`evaluation/test_cases.json`(預設,不傳 `--test-cases` 即用此)
- 20 題:`evaluation/test_cases_q20.json`
- A/B 30:`evaluation/test_cases_ab30.json`
- Q21–100:`evaluation/test_cases_q21_q100.json`
- Q101–150:`evaluation/test_cases_q101_q150.json`

## 輸出格式
1. 一句話說明這次要跑什麼(幾題、哪個檔、variant)。
2. 用 ```bash``` code block 印**確切命令**(含 `cd` 到 repo root)。
3. 若 ≥10 題:明講「請自己跑,我不代跑」。
4. 若涉 resume:附上 Failed-skip 警告 + 如何強制重跑。
5. 跑完後可接 `/debug-session <session_dir>` 分析結果。

輸出語言:繁體中文。
