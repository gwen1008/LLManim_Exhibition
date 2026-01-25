# 📋 逐步操作指南 - 從 GitHub 收集資料

## 🎯 完整流程概覽

1. ✅ 設置知識庫結構
2. 📥 從 GitHub 下載檔案
3. 📁 分類整理檔案
4. ✅ 驗證檔案可運行
5. 📊 追蹤進度
6. 📝 添加描述（可選）

---

## Step 1: 設置知識庫結構

### 方法 A: 使用自動化腳本（推薦）

```bash
python scripts/quick_start.py
```

這個腳本會自動：
- 建立 `knowledge_base/` 資料夾
- 建立所有分類資料夾（geometry, algebra, calculus 等）
- 檢查 Manim 環境
- 顯示現有檔案統計

### 方法 B: 手動建立

```bash
python scripts/setup_knowledge_base.py
```

**預期結果**: 
```
knowledge_base/
├── geometry/
├── algebra/
├── calculus/
├── arithmetic/
└── statistics/
```

---

## Step 2: 從 GitHub 下載檔案

### 方法 A: 使用下載腳本（推薦）✨

#### 互動模式（最簡單）

```bash
python scripts/download_from_github.py
```

然後按照提示：
1. 貼上 GitHub URL
2. 選擇分類（或選擇自動判斷）
3. 可選：自訂檔名

**範例操作**:
```
請輸入 GitHub URL: https://github.com/ManimCommunity/manim/blob/main/examples/basic_scenes.py
選擇分類: 6 (自動判斷)
自訂檔名: (直接 Enter)
✅ 下載完成！
```

#### 命令列模式

```bash
# 基本用法
python scripts/download_from_github.py <GitHub_URL>

# 指定分類
python scripts/download_from_github.py <GitHub_URL> geometry

# 指定分類和檔名
python scripts/download_from_github.py <GitHub_URL> geometry pythagorean_theorem.py
```

### 方法 B: 手動下載

#### 步驟 1: 取得 Raw URL

如果您的 GitHub URL 是：
```
https://github.com/user/repo/blob/main/path/file.py
```

轉換為 Raw URL：
```
https://raw.githubusercontent.com/user/repo/main/path/file.py
```

#### 步驟 2: 下載檔案

**選項 A: 使用瀏覽器**
1. 打開 Raw URL
2. 全選複製代碼（Ctrl+A, Ctrl+C）
3. 在對應分類資料夾建立新檔案
4. 貼上代碼並保存

**選項 B: 使用 curl (Windows PowerShell)**
```powershell
# 下載到指定分類
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/..." -OutFile "knowledge_base\geometry\example.py"
```

#### 步驟 3: 分類檔案

根據檔案內容，將檔案放入對應資料夾：
- `geometry/` - 幾何相關（圓形、三角形、變換等）
- `algebra/` - 代數相關（方程式、函數圖形等）
- `calculus/` - 微積分相關（導數、積分等）
- `arithmetic/` - 算術相關（加減乘除等）
- `statistics/` - 統計相關

---

## Step 3: 驗證檔案

### 驗證所有檔案

```bash
python scripts/verify_examples.py
```

**輸出範例**:
```
🔍 找到 5 個 Python 檔案，開始驗證...

📄 驗證: geometry/pythagorean_theorem.py ... ✅
📄 驗證: algebra/quadratic_equation.py ... ✅
📄 驗證: calculus/derivative.py ... ❌
   錯誤: Scene class not found

============================================================
📊 驗證結果統計
============================================================
總檔案數: 5
✅ 通過: 4
❌ 失敗: 1
```

### 手動驗證單個檔案

```bash
# 先找出 Scene 類別名稱
# 然後執行：
manim -pql knowledge_base/geometry/your_file.py YourSceneName
```

**常見問題處理**:
- ❌ "Scene class not found" → 檢查檔案中是否有 `class XxxScene(Scene)`
- ❌ "Import error" → 確認使用 `from manim import *`
- ❌ "Syntax error" → 檢查代碼語法

---

## Step 4: 查看進度

```bash
python scripts/stats_knowledge_base.py
```

**輸出範例**:
```
============================================================
📊 知識庫統計報告
============================================================

📁 總檔案數: 12

📂 分類詳細統計:
----------------------------------------------------------------------

🔹 ALGEBRA
   檔案數: 4
   總行數: 456
   代碼行: 312
   註解行: 89
   註解比例: 19.5%

🔹 GEOMETRY
   檔案數: 5
   總行數: 523
   代碼行: 378
   註解行: 98
   註解比例: 18.7%

----------------------------------------------------------------------
🎯 目標進度:
   目前: 12 / 20 個檔案 (60.0%)
   ⚠️  還需要 8 個檔案才能達到目標
============================================================
```

---

## Step 5: 添加檔案描述（可選但推薦）

### 自動生成描述

```bash
# 互動模式（會詢問每個檔案）
python scripts/generate_description.py geometry

# 自動模式（為所有檔案生成）
python scripts/generate_description.py algebra --auto
```

**注意**: 需要配置 `.env` 中的 `GROQ_API_KEY`

### 手動添加描述

編輯對應分類的 `README.md`，例如 `knowledge_base/geometry/README.md`:

```markdown
## pythagorean_theorem.py
**功能**: 展示畢氏定理的視覺化證明，使用三個正方形來演示 a² + b² = c²
**關鍵技巧**: 
- 使用 `Square` 和 `VGroup` 組合形狀
- 使用 `Transform` 動畫展示面積關係
- 使用 `MathTex` 顯示公式
```

---

## 🔄 完整工作流程範例

假設您找到了一個 GitHub URL，完整流程如下：

```bash
# 1. 設置環境（只需執行一次）
python scripts/quick_start.py

# 2. 下載檔案（每次找到新檔案時執行）
python scripts/download_from_github.py
# 然後貼上 URL，選擇分類

# 3. 驗證檔案（下載幾個檔案後執行）
python scripts/verify_examples.py

# 4. 查看進度（隨時執行）
python scripts/stats_knowledge_base.py

# 5. 生成描述（收集完一批檔案後執行）
python scripts/generate_description.py geometry --auto
```

---

## 📝 檔案命名建議

建議使用清晰的命名格式：

**格式**: `分類_主題_功能.py`

**範例**:
- ✅ `geometry_pythagorean_theorem.py`
- ✅ `algebra_quadratic_equation.py`
- ✅ `calculus_derivative_visualization.py`
- ❌ `example1.py` (太模糊)
- ❌ `test.py` (沒有意義)

---

## ⚠️ 常見問題

### Q: 下載的檔案無法運行？
A: 
1. 檢查是否使用 Manim Community 語法（不是舊版 3b1b 語法）
2. 確認有 `from manim import *`
3. 確認有 `class XxxScene(Scene)` 定義
4. 執行 `python scripts/verify_examples.py` 查看詳細錯誤

### Q: 不知道檔案應該放在哪個分類？
A: 
1. 使用下載腳本的自動判斷功能
2. 或根據檔案內容關鍵詞判斷：
   - 幾何：circle, square, triangle, transform
   - 代數：equation, function, quadratic
   - 微積分：derivative, integral, limit

### Q: 如何批量下載多個檔案？
A: 
1. 使用下載腳本的互動模式，連續輸入多個 URL
2. 或建立一個 URL 列表，寫簡單腳本循環下載

### Q: 檔案已經存在怎麼辦？
A: 下載腳本會提示是否覆蓋，選擇 'y' 覆蓋或 'n' 跳過

---

## ✅ 完成檢查清單

完成數據收集後，確認：

- [ ] `knowledge_base/` 資料夾已建立
- [ ] 至少 3 個分類資料夾有檔案
- [ ] **總計至少 20 個 `.py` 檔案**
- [ ] 所有檔案都通過驗證（`verify_examples.py`）
- [ ] 每個分類都有 `README.md`
- [ ] 至少 50% 的檔案有功能描述
- [ ] 執行 `stats_knowledge_base.py` 顯示進度 ≥ 100%

---

## 🎉 完成後

當您達到 20 個檔案的目標後：

1. **最終驗證**
   ```bash
   python scripts/verify_examples.py
   ```

2. **生成最終統計報告**
   ```bash
   python scripts/stats_knowledge_base.py
   ```

3. **提交到 Git**（如果使用版本控制）
   ```bash
   git add knowledge_base/
   git commit -m "Add knowledge base with 20+ Manim examples"
   ```

---

**需要幫助？** 查看 `DATA_COLLECTION_GUIDE.md` 了解更多細節。
