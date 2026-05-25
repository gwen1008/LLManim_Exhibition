# Exhibition Frontend ↔ Backend Interface Spec

> **For**: 組員前端開發
> **Owner**: 廖振廷
> **Deadline**: 2026-05-26 (二) 晚上
> **Branch**: `feat/exhibition`

---

## 1. 你的工作範圍

你負責**整個前端 SPA**（`exhibition/frontend/`），消費下方定義的後端 API 與靜態素材。

**完整裁量權**：頁面佈局、視覺、配色、字型、互動細節、技術選型（React / Vue / SvelteKit / Astro 都可）、動畫效果、navbar 結構 — 你自己決定。

**硬性約束**（只有這 4 條）：

1. **不可改 API endpoint 名稱或 JSON schema** — 後端已鎖定下方定義
2. **必須包含「Opus 一發 vs. 本系統」對比** — 這是核心賣點，呈現方式自由
3. **必須顯示 baseline 公平性聲明** — 文案可改，但語意要保留：「Opus baseline = 無 RAG / 無 Vision QA / 無 Reflexion 的隔離對照組，不代表 Opus 模型本身能力上限」
4. **交付靜態 build**：`exhibition/frontend/dist/`，由 FastAPI `StaticFiles` 掛載

---

## 2. 後端 API

Base URL: `http://localhost:8000`（展場本機）

### 2.1 `GET /api/gallery` — 預生成對比影片列表

**永遠優先用這個 endpoint，這是主賣點頁的資料來源。**

Response:

```json
{
  "items": [
    {
      "id": "Q024",
      "topic": "畢氏定理",
      "topic_en": "Pythagorean theorem",
      "opus_video_url": "/static/videos/opus_only/Q024.mp4",
      "system_video_url": "/static/videos/full_system/Q024.mp4",
      "opus_metrics": {
        "render_success": false,
        "render_duration_sec": 45.2,
        "code_lines": 87,
        "deprecated_api_count": 3,
        "notes": "ManimGL syntax used, ShowCreation deprecated"
      },
      "system_metrics": {
        "render_success": true,
        "render_duration_sec": 312.5,
        "code_lines": 215,
        "deprecated_api_count": 0,
        "bj_score": 78,
        "refining_iterations": 2
      }
    }
  ],
  "generated_at": "2026-05-24T22:00:00+08:00"
}
```

**欄位語意**：
- `render_success: false` → 影片可能不存在或是 black frame，前端要 graceful 處理（顯示「Opus 生成失敗」覆蓋層）
- `deprecated_api_count` → 顯示為「使用 N 個已棄用 API」紅色標籤
- `bj_score` → 本系統的 BenchmarkJudge 分數 0-100（越高越好）

### 2.2 `GET /api/stats` — 系統聚合指標（給 tech 頁）

Response:

```json
{
  "benchmark_pass_rate": "30/30",
  "gt_match_rate": 0.951,
  "bj_average_score": 72.4,
  "total_videos_generated": 150,
  "refining_loop_max_iterations": 5,
  "agents": [
    {"name": "Planner", "model": "gemini-2.5-flash", "role": "視覺計畫 JSON"},
    {"name": "Coder", "model": "claude-opus-4-7", "role": "ManimCE 代碼生成"},
    {"name": "VisionQA", "model": "gpt-4o", "role": "渲染後視覺驗收"},
    {"name": "RefiningLoop", "model": "—", "role": "Reflexion 自動修正 (最多 5 輪)"}
  ]
}
```

### 2.3 `POST /api/generate` — Live 模式（stretch goal，可能不會做）

> ⚠️ **這個 endpoint 不保證會實作**。若到 deadline 沒做，前端**不要**註冊 `/live` route，nav 也不要顯示「Live」按鈕。後端會回 `501 Not Implemented`，前端 fetch 時可用此判斷。

Request:

```json
{ "topic": "三角形內角和", "mode": "opus_only" }
```

`mode` 為 `"opus_only"` 或 `"full_system"`。

Response（成功）:

```json
{ "task_id": "abc-123-def" }
```

Response（未實作）: HTTP 501

### 2.4 `GET /api/task/{task_id}` — Live 模式輪詢（stretch goal）

Response:

```json
{
  "status": "running",
  "progress": { "stage": "Coder 生成中", "percent": 35 },
  "artifacts": {
    "planner_json": { "...": "..." },
    "code": "from manim import *\n...",
    "vision_verdict": { "verdict": "PASS", "issues": [] },
    "video_url": "/static/runs/abc-123/video.mp4",
    "logs": ["[Planner] done in 12s", "[Coder] iteration 1..."]
  },
  "duration_sec": 142,
  "error": null
}
```

`status` 可能值：`queued` / `running` / `done` / `failed`

輪詢頻率建議：2 秒一次。

---

## 3. 靜態素材路徑

後端 FastAPI 會把 `exhibition/static/` 整個目錄掛到 `/static/*`：

```
exhibition/static/
├── videos/
│   ├── opus_only/         # 10 部 Opus baseline 影片（可能有些 render 失敗 → 占位圖）
│   │   ├── Q024.mp4
│   │   └── ...
│   └── full_system/       # 10 部本系統影片
│       ├── Q024.mp4
│       └── ...
└── data/
    ├── gallery.json       # /api/gallery 的靜態 fallback（API 掛掉時用 fetch 直接讀這個）
    └── stats.json         # /api/stats 的靜態 fallback
```

**強烈建議**：前端優先 fetch `/api/gallery`，失敗時 fallback 到 `/static/data/gallery.json` — 這樣即使後端 server 掛掉，gallery 頁面照樣能跑。

---

## 4. 頁面最低需求（**僅供參考，可自由重構**）

### 頁面 A `/` — Gallery（**必做**）

- Hero 區：標題 + 一段「本系統 vs. 純 Opus 一發」核心訊息
- 10 組對比卡片：每組左右並排兩個 `<video>`，下方標 topic + metrics 對比（render 時間 / 代碼行數 / deprecated API 數 / BJ 分數）
- 卡片底部固定顯示公平性聲明

### 頁面 B `/tech` — Tech Dashboard（**必做**）

- Multi-agent pipeline 流程圖（Planner → Coder → Vision → Refining Loop）
- BJ/FJ 評分數據（從 `/api/stats` 拉）
- 30/30 benchmark pass / 95.1% GT match 等數字 hero card

### 頁面 C `/live` — Live 互動（**stretch，不一定做**）

- 輸入框輸入 topic + 選 mode
- 並排顯示兩 pipeline 進度條 + stage 標籤
- 完成後並排播放影片 + 顯示 artifacts（planner JSON、code、vision verdict）

---

## 5. 開發環境設定

```bash
# 1. clone & checkout
git checkout feat/exhibition

# 2. 進前端目錄
cd exhibition/frontend

# 3. 你的框架自選，舉例：
npm create vite@latest . -- --template react-ts
npm install
npm run dev   # 預設跑在 :5173

# 4. 後端 mock：你可以先用 /static/data/*.json 開發，等我把 API 弄好再切過去
```

**Mock data**：開發初期 `/api/gallery` 還沒上線時，直接 fetch `/static/data/gallery.json`（我會先放一個假資料版讓你能開工）。

---

## 6. 部署

- 你 `npm run build` → 產出 `exhibition/frontend/dist/`
- 我會在 FastAPI 把 `dist/` 掛到 `/`，把 `exhibition/static/` 掛到 `/static/`
- 展場直接 `uvicorn exhibition.api:app --host 0.0.0.0 --port 8000`

---

## 7. 溝通

- 規格疑問 → 直接問廖振廷
- API schema 想改 → 必須先討論（不要自己改）
- UI/UX 決策 → **你說了算，不用問**

---

## 8. 賣點包裝建議（給你做設計時參考）

評審大概只看 30 秒就走，視覺要抓眼：

- **「同樣 prompt，兩個系統，差距有多大？」** — 標題用這種挑釁式問句
- 並排播放時加個小標 **「Opus 一發直出」vs.「本系統（5 階段 multi-agent）」**
- Metrics 用紅綠色對比：Opus 紅多綠少、本系統綠多紅少
- 失敗的 Opus 影片不要藏，秀出來「render failed」反而有說服力
