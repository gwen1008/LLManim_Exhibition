更新 `.ai-context/HANDOFF.md` 的 **Section 1 當前焦點**（其他 section 絕對不准動）。

## 步驟

1. **讀取現況**
   - Read `.ai-context/HANDOFF.md`，記下目前 Section 1 的 Active / Next / Blocked 三行
   - Read 註解 `<!-- SECTION_1_UPDATED_AT: YYYY-MM-DD -->` 的日期
   - Bash 跑 `git log --oneline --since="<該日期>" -20` 看這段期間發生了什麼
   - 也參考本次 conversation 已經做過的事

2. **產生 draft**
   - 根據 git log + 本次對話內容，猜一份新的 Section 1（Active / Next / Blocked 三行）
   - **顯示 draft 給用戶**，格式：
     ```
     === 目前 ===
     Active: ...
     Next: ...
     Blocked: ...

     === 我猜的新版 ===
     Active: ...
     Next: ...
     Blocked: ...
     ```

3. **問用戶一次**
   - 問：「直接用新版？(y) 或給我一行覆寫指示？」
   - **只問這一次**，不要拆三題

4. **寫入**
   - 用 Edit 工具替換 Section 1 三行（`<!-- SECTION_1_UPDATED_AT -->` 註解也要更新成今天）
   - 三行之外的內容**一個字都不准動**（鐵律段、架構段、環境段都不准碰）
   - regex 定位：從 `<!-- SECTION_1_UPDATED_AT:` 那行起，到 `> 改動規則：` 那行為止

## 鐵律

- 不准動 Section 2/3/4，只動 Section 1
- 不准打勾、不准加日期、不准留歷史（完成的事就直接覆寫掉）
- 如果用戶說「Active 沒變、只是 Next 換了」，只改 Next 那行，其他保留
- 如果 git log 自上次更新沒新 commit 且本次 conversation 也沒做事，就**不動**並回報「沒新進度，跳過」