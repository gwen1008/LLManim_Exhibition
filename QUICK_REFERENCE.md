# 🚀 快速參考卡片

## 一鍵開始

```bash
python scripts/quick_start.py
```

## 📍 數據來源（優先順序）

1. ⭐ **Manim Community 官方文檔**
   - https://docs.manim.community/en/stable/examples.html
   - 直接複製代碼

2. **GitHub 搜索**
   - 關鍵詞: `manim-community-examples`
   - 倉庫: `ManimCommunity/manim`

3. **YouTube 教程**
   - 3Blue1Brown 頻道
   - 影片描述中的代碼連結

## 📂 目標結構

```
knowledge_base/
├── geometry/     (目標: 7-8 個檔案)
├── algebra/      (目標: 7-8 個檔案)
└── calculus/     (目標: 5-6 個檔案)
```

**總目標**: 至少 20 個高品質檔案

## ✅ 驗證清單（每個檔案）

- [ ] 可以正常運行 (`manim -pql file.py SceneName`)
- [ ] 有清晰的註解
- [ ] 使用現代 Manim Community 語法
- [ ] 展示明確的數學概念

## 🛠️ 常用命令

```bash
# 驗證所有檔案
python scripts/verify_examples.py

# 查看統計
python scripts/stats_knowledge_base.py

# 生成描述（需要 API Key）
python scripts/generate_description.py geometry
```

## 📊 進度追蹤

執行 `python scripts/stats_knowledge_base.py` 查看：
- 目前檔案數
- 各分類進度
- 距離目標還差多少

---

**詳細指南**: 請查看 `DATA_COLLECTION_GUIDE.md`
