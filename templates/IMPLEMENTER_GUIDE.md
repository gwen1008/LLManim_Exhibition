# 🛠️ 算術模板開發指南 (Implementer's Guide)

這份文件旨在引導團隊成員如何開發新的算術模板（減法、乘法、除法）。

## 🚀 流程說明

1. **切換分支**：為您的任務建立新分支。

    ```bash
    git checkout -b feat/subtraction  # 以減法為例
    ```

2. **找到您的戰場**：開啟 `templates/` 下對應的檔案（例如 `subtraction.py`）。
3. **實作邏輯**：完成「旁白生成」與「Manim 代碼生成」兩部分。
4. **測試**：使用 `run_math.py` 驗證結果。

---

## 📝 第一步：實作旁白生成 (`generate_X_narrative`)

這是影片的「劇本」。您的任務是根據輸入的兩個數字，產生一個包含多個步驟的清單。

每個步驟是一個字典：

* `narrative`: 老師要說的話（字串）。
* `phase`: 這個步驟的標籤（例如 `digit_0_identify`），幫助代碼生成器對應動畫。

**範例邏輯：**

```python
def generate_subtraction_narrative(num1, num2, interactive_mode=False):
    steps = []
    # 1. 開場白
    steps.append({"narrative": "我們來算算看這題減法。", "phase": "intro"})
    
    # 2. 逐位計算 (範例：個位)
    steps.append({"narrative": "先看個位，5 減 3 等於 2。", "phase": "digit_0_calculate"})
    
    # ... 實作借位邏輯與互動提問 ...
    return steps
```

---

## 🎬 第二步：實作 Manim 代碼生成 (`generate_vertical_X_code`)

這是影片的「視覺」。您需要根據上面的 `steps` 標籤，決定畫面要顯示什麼。

* **共用功能**：已經為您準備好了 `setup`（初始化字幕區）和 `update_subtitle`（瞬間更新字幕）。請務必從 `common.py` 匯入並使用它們。
* **動畫對應**：跑一個迴圈處理 `audio_steps`，根據 `phase` 插入對應的 Manim 動畫代碼。

**重要規則：**
* 字幕更新必須使用 `self.update_subtitle(text, duration)` 或自定義的瞬間切換邏輯，確保與語音同步。
* 若是互動模式，記得在地圖上放問號 `?` 並加上 `self.wait(2.0)`。

---

## 🧪 第三步：測試您的成果

不需要修改任何核心檔案，直接執行：

```bash
# 測試您的減法模板 (假設 num1=10, num2=5)
python run_math.py sub 10 5 --interactive --render
```

## 💡 小撇步

* **參考範本**：強烈建議參考 `templates/addition.py`。它是目前最完善、包含互動邏輯與音訊同步的範例。
* **不要重造輪子**：動畫中的數字顏色、字體、字幕位置都已經定義在 `common.py` 中，請保持風格統一。

加油，期待看到你們的成果！
