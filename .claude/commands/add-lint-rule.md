用戶描述了一個 Manim 的錯誤模式或反模式：

**$ARGUMENTS**

請根據這個描述，在 `agents/coder/lint_manim.py` 中新增一條 AST 規則。

步驟：
1. 先讀取 `agents/coder/lint_manim.py` 完整內容，了解現有規則結構
2. 確認新規則的 error code（格式如 `DEPRECATED_API`, `INVALID_ARG`, `HALLUCINATED_METHOD` 等），不得與現有 code 重複
3. 在 `visit_Call` 或其他適當的 visitor 方法內新增規則，風格與現有規則一致：
   - 使用 `self.errors.append({...})` 格式
   - 包含 `line`, `code`, `message` 三個欄位
   - message 要說明錯誤原因和正確用法
4. 如果是建議性（非阻塞）規則，用 `self.advisories.append(...)` 而非 `self.errors`
5. 在修改後說明：新增了哪條規則、error code 是什麼、會在哪種代碼模式下觸發

輸出語言：繁體中文說明 + 英文代碼。