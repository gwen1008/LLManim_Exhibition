# 電機系專題海報 — 製作說明（v2 競賽強化版）

> 🏆 **目標等級**：跨校競賽得獎 / AIED poster session 引人駐足
> 📐 **當前狀態**：文字內容 + 5 張圖完備；待補 Hero Visual 素材（影片截圖）

## 規格
- **尺寸**：A1 直式 60cm × 85cm
- **平台**：PowerPoint
- **繳交單位**：國立臺灣師範大學 電機工程學系
- **設計原則**：圖為主、文字為輔；訊息漏斗（5m / 1m / 駐足三層）

---

## 👥 給組員的話

👉 **如果你是被分派做海報排版的組員，請先讀 [`GUIDE_FOR_TEAMMATE.md`](GUIDE_FOR_TEAMMATE.md)**，那裡有完整的 9 步驟製作流程、字級配色規範、Hero Visual 製作教學、列印建議。

預估完成時間 **9-12 小時**，建議分 2-3 天做。

---

## 📂 檔案地圖

### 主文稿（依海報區塊順序）

| 檔名 | 對應海報區塊 | 狀態 |
|---|---|---|
| `00_layout.md` | **整體排版示意圖**（v2 結構） | ✅ 定稿 |
| `01_title.md` | ① 標題列（含 Tagline 候選） | ✅ 定稿 |
| `02_hero_visual.md` | ② **Hero Visual**（v2 新增，最重要） | ⚠️ 待組員製作素材 |
| `02_abstract.md` | ③ 摘要（與動機合併） | ✅ 定稿 |
| `03_motivation.md` | ③ 研究動機（含 hook 開場） | ✅ 定稿 |
| `04_architecture.md` | ④ 系統架構（含 drawio 圖） | ✅ 定稿 |
| `05b_repair_funnel.md` | ⑤ **三層自修復漏斗**（v2 新增） | ✅ 定稿 |
| `05c_method_comparison.md` | ⑥ **方法對比表**（v2 新增） | ⚠️ 引用待確認 |
| `05_results.md` | ⑦ 實驗結果（2 張圖） | ✅ 定稿 |
| `06_conclusion.md` | ⑧ 結論 | ✅ 定稿 |
| `07_future_work.md` | ⑨ 未來展望 | ✅ 定稿 |
| `08_qr_acknowledgement.md` | ⑩ QR + 致謝（v2 改 3 個 QR） | ⚠️ 三個 URL 待填 |

### 圖片素材（`figures/`）

| 檔案 | 用途 | 對應區塊 |
|---|---|---|
| `figures/電機專題誠品.drawio.png` | 系統架構圖 | ④ |
| `figures/figure_repair_funnel.png` | **三層自修復漏斗（v2 新增）** | ⑤ |
| `figures/figure5_per_stage_pass.png` | 分學階通過率（實驗主視覺） | ⑦ |
| `figures/figure6_veto_stacked.png` | 失敗原因堆疊圖 | ⑦ |
| `figures/make_repair_funnel.py` | 漏斗圖生成腳本（可改數字重跑） | — |
| `figures/_optional/figure3_radar.png` | FJ 四維雷達（v2 不放海報，書面備用） | — |
| `figures/_optional/figure4_fjw_distribution.png` | FJW 分布（v2 不放海報） | — |

---

## ⚠️ 待補項目

### 1. Hero Visual 素材（最關鍵，組員要做）
**動作**：依 `02_hero_visual.md` 指引，從 `runs/` 撈影片，用 ffmpeg 抽 frame，做紅綠標註。
- 4 題 baseline 失敗截圖 + 4 題本系統成功截圖
- 中央 +172% 巨字 + 標籤

### 2. 三個 QR URL（廖振廷之後給，組員不用問）
1. Demo 影片連結 — ⏳ 廖振廷之後給
2. GitHub Repo — ⏳ 廖振廷之後給
3. AIED 2026 LBR 論文 — ⏳ 廖振廷之後給（會議報告後才有）

→ 組員先在 QR 區放 3 個灰色佔位方框，等 URL 給了再用 `qrencode` 生成替換。

### 3. 方法對比表的引用確認（組員可協助查）
`05c_method_comparison.md` 中 Generative Manim / ChatAnimator 等需確認真實論文名稱。
若不確定，可改用通用分類詞（如「Naive LLM Code Generation」），詳見該檔案底部說明。

---

## 🎨 設計建議

| 項目 | 建議 |
|---|---|
| 配色 | 師大藍 `#1f3a5f` + 強調藍 `#2e6fb8` + 橘紅 `#d95f4a`（數字） + 金色 `#d4a017`（AIED badge） |
| 中文字型 | 思源黑體（標題 Heavy，內文 Regular） |
| 英文字型 | Inter 或 Source Sans Pro |
| 列印 | A1 全銅板紙霧面（不要光面，反光毀掉） |
| 材質升級 | 加裱 PP 板（不會捲、不會折） |

---

## 📊 真實數字一覽（從 `dept_report/analysis/stats_summary.txt` 撈）

| 指標 | 本系統 | Baseline |
|---|---:|---:|
| Strict PASS（≥2/3 runs） | **49/60 = 81.7%** | 18/60 = 30.0% |
| Run 1 / Run 2 / Run 3 | 41 / 51 / 46 | — |
| FJW 平均 | 4.46 | 3.52 |
| Render 成功率 | **60/60 = 100%** | 40/60 = 66.7% |
| Fisher exact p | **1.62 × 10⁻⁸** | — |
| Cohen's d (FJW) | **1.03**（大效應量） | — |
| 高中段提升 | **+63.3 pp**（5% → 68.3%） | — |

---

## 🏆 v2 vs v1 主要差異

| 項目 | v1 | **v2（現在）** |
|---|---|---|
| 頂部視覺 | 摘要 + 動機文字 | **Hero Visual + Tagline** |
| 核心數字 | 摘要文字內 +172% | **Hero 中央 140pt 橘紅巨字** |
| 三層自修復 | 文字埋在架構區 | **獨立漏斗圖** |
| 方法新穎性 | 無 | **新增對比表** |
| 統計圖數量 | 4 張塞 2×2 | **減為 2 張（精選）** |
| Tagline | 無 | **一句口號** |
| QR 數量 | 2 個 | **3 個（+ Paper）** |
| 評審意見回應 | — | **Hero+ Hook + 對比表 + 漏斗圖** |

---

## 📌 製作順序建議

1. **先做 Hero Visual** ← 70% 海報成敗在這
2. PPT 開新檔，A1 直式，照 `00_layout.md` 配置區塊框架
3. 文字內容依各區塊 markdown 貼入
4. 插入 5 張圖
5. 處理強調數字視覺跳出
6. 三個 QR 生成 + 插入
7. 校對名字（注意：周庭伊 / 巫冠儀 / 賴以威，非書面報告誌謝段那組）
8. 列印前先螢幕縮到 20% 看整體視覺平衡

---

## 🔗 相關檔案

- 完整書面報告：`../基於大型語言模型之_修訂版.md`
- 系上專題分析報告：`../dept_report/dept_report_v1.md`
- 原始實驗數據：`../dept_report/run_data/*.csv`
- 統計摘要：`../dept_report/analysis/stats_summary.txt`
