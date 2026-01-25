# Scripts 工具集

這個資料夾包含用於數據收集任務的實用腳本。

## 📋 腳本列表

### 1. `quick_start.py` - 快速設置
**功能**: 一鍵設置知識庫結構並檢查環境

```bash
python scripts/quick_start.py
```

### 2. `setup_knowledge_base.py` - 建立資料夾結構
**功能**: 建立 `knowledge_base/` 及其所有分類資料夾

```bash
python scripts/setup_knowledge_base.py
```

### 3. `verify_examples.py` - 驗證範例檔案
**功能**: 驗證所有 `.py` 檔案是否可以正常運行

```bash
# 詳細輸出
python scripts/verify_examples.py

# 安靜模式（僅顯示結果）
python scripts/verify_examples.py --quiet
```

**輸出**: 
- ✅ 通過驗證的檔案
- ❌ 失敗的檔案及錯誤訊息

### 4. `stats_knowledge_base.py` - 統計資訊
**功能**: 顯示知識庫的詳細統計資訊

```bash
python scripts/stats_knowledge_base.py
```

**顯示內容**:
- 總檔案數
- 各分類的檔案數、行數、註解比例
- 目標進度（20個檔案）

### 5. `generate_description.py` - 生成檔案描述
**功能**: 使用 LLM 為檔案自動生成功能描述

```bash
# 互動模式（會詢問每個檔案）
python scripts/generate_description.py geometry

# 自動模式（為所有檔案生成）
python scripts/generate_description.py algebra --auto
```

**注意**: 需要配置 `.env` 中的 `GROQ_API_KEY`

### 6. `add_file_description.py` - 手動添加檔案說明
**功能**: 為已下載的檔案添加或更新簡短說明

```bash
# 互動模式（選擇分類和檔案）
python scripts/add_file_description.py

# 批量模式（為所有沒有說明的檔案添加）
python scripts/add_file_description.py --batch
```

**用途**: 為檔案添加簡短的功能說明，會自動更新到對應分類的 README.md

## 🔄 典型工作流程

1. **初始設置**
   ```bash
   python scripts/quick_start.py
   ```

2. **收集檔案後驗證**
   ```bash
   python scripts/verify_examples.py
   ```

3. **查看進度**
   ```bash
   python scripts/stats_knowledge_base.py
   ```

4. **生成描述（可選）**
   ```bash
   python scripts/generate_description.py geometry --auto
   ```

## ⚠️ 注意事項

- 所有腳本需要在專案根目錄執行
- `verify_examples.py` 需要 Manim 已正確安裝
- `generate_description.py` 需要配置 API Key
