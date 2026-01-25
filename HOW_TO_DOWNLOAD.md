# 📥 如何下載 GitHub 檔案到知識庫

## 🚀 快速開始（3 步驟）

### Step 1: 確保知識庫結構已建立

```bash
python scripts/quick_start.py
```

（如果已經執行過，可以跳過這步）

---

### Step 2: 執行下載腳本

```bash
python scripts/download_from_github.py
```

---

### Step 3: 按照提示操作

腳本會引導您完成以下步驟：

#### 1️⃣ 輸入 GitHub URL

當看到提示時，貼上您的 GitHub 網址：

```
請輸入 GitHub URL: [在這裡貼上您的網址]
```

**支援的 URL 格式**：
- ✅ `https://github.com/user/repo/blob/branch/path/file.py`
- ✅ `https://raw.githubusercontent.com/user/repo/branch/path/file.py`

**範例**：
```
https://github.com/ManimCommunity/manim/blob/main/examples/basic_scenes.py
```

#### 2️⃣ 選擇分類

腳本會顯示選項：

```
選擇分類:
  1. geometry (幾何)
  2. algebra (代數)
  3. calculus (微積分)
  4. arithmetic (算術)
  5. statistics (統計)
  6. 自動判斷

請選擇 (1-6，預設 6):
```

**建議**：
- 如果不確定，選擇 `6`（自動判斷）
- 腳本會根據檔名和內容自動判斷分類

#### 3️⃣ 自訂檔名（可選）

```
自訂檔名（直接 Enter 使用原檔名）: 
```

- 直接按 Enter：使用原檔名
- 或輸入自訂檔名，例如：`geometry_pythagorean_theorem.py`

---

## 📋 完整操作範例

```
C:\Users\Cherry\LLManim_Agent> python scripts/download_from_github.py

======================================================================
📥 GitHub 檔案下載工具
======================================================================

支援的 URL 格式:
  - https://github.com/user/repo/blob/branch/path/file.py
  - https://raw.githubusercontent.com/user/repo/branch/path/file.py

輸入 'q' 或 'quit' 結束

請輸入 GitHub URL: https://github.com/ManimCommunity/manim/blob/main/examples/basic_scenes.py

選擇分類:
  1. geometry (幾何)
  2. algebra (代數)
  3. calculus (微積分)
  4. arithmetic (算術)
  5. statistics (統計)
  6. 自動判斷

請選擇 (1-6，預設 6): 6

💡 自動建議分類: geometry

自訂檔名（直接 Enter 使用原檔名）: 

📥 下載: https://raw.githubusercontent.com/ManimCommunity/manim/main/examples/basic_scenes.py
✅ 已保存: knowledge_base\geometry\basic_scenes.py

✅ 下載完成！
   建議執行: python scripts/verify_examples.py 來驗證檔案

----------------------------------------------------------------------
```

---

## 🔄 批量下載多個檔案

### 方法 1: 連續使用互動模式

執行腳本後，可以連續輸入多個 URL，每次下載完成後會繼續詢問下一個 URL。

輸入 `q` 或 `quit` 結束。

### 方法 2: 命令列模式（適合批量）

```bash
# 下載單個檔案
python scripts/download_from_github.py <URL> <分類> <檔名>

# 範例
python scripts/download_from_github.py https://github.com/... geometry example.py
```

---

## ⚡ 快速命令參考

### 下載單個檔案（自動判斷分類）

```bash
python scripts/download_from_github.py "https://github.com/user/repo/blob/main/file.py"
```

### 下載並指定分類

```bash
python scripts/download_from_github.py "https://github.com/user/repo/blob/main/file.py" geometry
```

### 下載並指定分類和檔名

```bash
python scripts/download_from_github.py "https://github.com/user/repo/blob/main/file.py" geometry my_custom_name.py
```

---

## ❓ 常見問題

### Q: 檔案已經存在怎麼辦？

A: 腳本會詢問是否覆蓋：
```
⚠️  檔案已存在: example.py
   是否覆蓋？(y/n): 
```
- 輸入 `y` 覆蓋
- 輸入 `n` 跳過

### Q: 下載失敗怎麼辦？

A: 檢查：
1. URL 是否正確（必須是有效的 GitHub URL）
2. 檔案是否為 `.py` 格式
3. 網路連線是否正常

### Q: 如何知道檔案下載到哪裡？

A: 檔案會下載到：
```
knowledge_base/<分類>/<檔名>.py
```

例如：
- `knowledge_base/geometry/example.py`
- `knowledge_base/algebra/quadratic.py`

### Q: 下載後需要做什麼？

A: 建議執行驗證：
```bash
python scripts/verify_examples.py
```

這會檢查所有檔案是否可以正常運行。

### Q: 如何為檔案添加說明？

A: 有兩種方式：

**方式 1: 下載時添加**
下載完成後，腳本會詢問是否要添加說明，選擇 `y` 並輸入說明即可。

**方式 2: 為已下載的檔案添加說明**
```bash
python scripts/add_file_description.py
```

這會引導您選擇分類和檔案，然後添加說明。

---

## 🎯 完整工作流程

```bash
# 1. 設置知識庫（只需一次）
python scripts/quick_start.py

# 2. 下載檔案（每次找到新檔案時）
python scripts/download_from_github.py
# 然後按照提示輸入 URL

# 3. 驗證檔案（下載幾個檔案後）
python scripts/verify_examples.py

# 4. 查看進度
python scripts/stats_knowledge_base.py
```

---

## 💡 提示

1. **準備好您的 URL 列表**：可以先把所有要下載的 URL 整理在一個文件中
2. **使用自動判斷**：如果不確定分類，選擇選項 6 讓腳本自動判斷
3. **定期驗證**：每下載幾個檔案後，執行一次驗證確保品質
4. **查看進度**：使用 `stats_knowledge_base.py` 追蹤收集進度

---

**需要更多幫助？** 查看 `STEP_BY_STEP_GUIDE.md` 了解詳細流程。
