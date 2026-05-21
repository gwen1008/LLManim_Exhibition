# 05c — 方法新穎性對比表（v2 新增）

**位置**：右中（區塊 ⑥），約 28 × 12 cm
**區塊大標**：方法比較 Method Comparison（44pt）

⚠️ 這張表回答評審必問的問題：**「你的方法跟別人差在哪？」**

---

## 對比表內容

| 方法 | 概念分段 | 自我修復 | 同步旁白 | 可重現基準 | 同模型對照 |
|---|:-:|:-:|:-:|:-:|:-:|
| Manim 手寫 | ✓ | ✗ | 手動 | ✗ | N/A |
| LLM Zero-shot (Opus) | ✗ | ✗ | ✗ | ✗ | ✗ |
| Generative Manim (2024) | 部分 | ✗ | ✗ | ✗ | ✗ |
| ChatAnimator / Text2Animation | 部分 | ✗ | 部分 | ✗ | ✗ |
| Text2Video (商業 SaaS) | ✗ | N/A | ✓ | ✗ | N/A |
| **本系統 LLManim** | **✓ CTML 三原則** | **✓ 三層** | **✓ Azure TTS** | **✓ 60 題** | **✓ 同 Opus** |

---

## 五項對比維度說明

### ▍ 概念分段（Concept Segmentation）
是否依教學設計理論將內容拆解為可學習的步驟。
**本系統**：將 Mayer CTML 三原則（分段、預訓、信號）編碼為 Planner 硬性約束。

### ▍ 自我修復（Self-Repair）
生成失敗後是否能自動修正。
**本系統**：三層修復迴圈（Linter → Layout → Vision），主迭代上限 5 次。

### ▍ 同步旁白（Synchronized Narration）
是否生成與動畫同步的語音說明。
**本系統**：Azure TTS 平行生成，依 Planner 時間軸自動對齊。

### ▍ 可重現基準（Reproducible Benchmark）
是否提供可公開重現的評估資料集。
**本系統**：60 題涵蓋國小至高中，知識點、難度、答案完整標註。

### ▍ 同模型對照（Same-Model Baseline）
是否與「同 LLM 直接生成」做公平對照，量化系統設計貢獻。
**本系統**：Baseline 使用相同的 Claude Opus，排除「強模型 vs 弱模型」干擾，
證明 +172% 提升來自**架構設計**而非更強的 LLM。

---

## 視覺重點

| 元素 | 處理 |
|---|---|
| 「本系統」列 | 整列**淺藍底高亮** `#e9eef5` + 粗體 |
| ✓ 勾號 | 綠色 `#4caf50` 24pt |
| ✗ 叉號 | 灰色 `#999` 20pt |
| 「同模型對照」這欄 | 加紅色描邊 — 這是其他方法**全部沒有**的賣點 |
| 表格標題列 | 深藍底白字 |

---

## ⚠️ 待組員確認的引用

對比表中以下方法需確認**實際論文/工具名稱**並補進 `08_qr_acknowledgement.md` 參考文獻：

| 方法 | 需確認 |
|---|---|
| Generative Manim | 是否有正式論文/blog post（GitHub: https://github.com/360macky/generative-manim 之類） |
| ChatAnimator / Text2Animation | 需確認真實名稱（這欄目前是 placeholder） |
| Text2Video (商業) | 可舉例 Sora / Synthesia / D-ID（選一個放） |

如果找不到對應正式論文，可改用更安全的分類名稱：
- 「Naive LLM Code Generation」
- 「Single-Pass Manim Generators」
- 「Commercial Video Synthesis」

避免錯誤引用。
