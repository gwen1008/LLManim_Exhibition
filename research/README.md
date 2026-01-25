# AI 研究資料夾

這個資料夾包含與 AI 研究、RAG 系統設計、以及相關論文和文檔。

## 📁 檔案說明

### `deep_research_rag.md`
**內容**: RAG (檢索增強生成) 系統的研究問題和架構設計思考

**主題**:
- Indexing Strategy for Code (代碼索引策略)
- Retrieval Strategy (檢索策略，特別是語義差距問題)
- Prompt Engineering with RAG (RAG 的提示工程)

**用途**: 用於指導 RAG 系統的設計和實現

---

### `manimator_paper_extract.txt`
**內容**: Manimator 論文的提取內容

**主題**:
- Manimator: Transforming Research Papers into Visual Explanations
- Agentic architecture for Manim video generation
- 與 TheoremExplainAgent 的比較

**用途**: 參考其他類似系統的設計思路

---

## 🔗 相關資源

- **專案主 README**: `../README.md`
- **數據收集指南**: `../DATA_COLLECTION_GUIDE.md`
- **RAG 系統實現**: 待開發（將使用此資料夾的研究成果）

---

## 📝 研究筆記

### RAG 系統設計要點

1. **索引策略**: 需要考慮 Manim 代碼的上下文依賴
2. **檢索策略**: 解決用戶查詢與代碼關鍵詞的語義差距
3. **提示工程**: 如何有效地將檢索到的代碼範例傳遞給 Coder Agent

### 參考系統

- **Manimator**: 從研究論文生成 Manim 動畫
- **TheoremExplainAgent**: 專門用於數學定理的 Manim 視頻生成

---

**最後更新**: 2026-01-25
