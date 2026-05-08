# 組員 C 任務說明 — 展覽前端網頁

> 這份文件是你的完整工作說明，不需要看其他文件也能執行。
> 有問題直接問 @liaozhenting。

---

## 你在做什麼

這個專案把數學題目自動轉成教育動畫影片。整條流程：

```
題目 → [Planner] → [Coder] → Manim 渲染 → 影片
```

現在有個 Streamlit UI（`app.py`），但太陽春，拿去展覽不夠看。

**你的任務**：寫一個 React 前端，接上已經寫好的 FastAPI 後端（`api.py`），展示：
1. 題目輸入框
2. Pipeline 進度條（7 個 stage 即時更新）
3. 影片播放器
4. FinalJudge 評分卡

**你不需要懂 AI、Manim、或 Python**。後端 API 已經寫好了，你只要接它。

---

## 你的工作範圍

```
frontend/                ← 你的主戰場，全部由你從零建起
  src/
    App.tsx
    components/
      TopicInput.tsx     # 輸入框 + 送出按鈕
      PipelineStages.tsx # 7 個 stage pills
      VideoPlayer.tsx    # 影片播放
      ScorePanel.tsx     # 評分卡
  vite.config.ts         # Proxy 設定（重要，複製下面的範本就好）
```

**嚴禁改動的檔案**（不是你負責的範圍）：
- `api.py`
- `mock_api.py`
- `main.py`
- `agents/`（整個目錄）

---

## 環境 Setup（15-20 分鐘）

### 1. Clone 專案

```bash
git clone <repo_url>
cd LLManim_Agent
```

### 2. 安裝 Node.js

需要 Node.js >= 18。確認版本：

```bash
node -v   # 應該看到 v18.x 或更新
```

沒有的話去 https://nodejs.org 裝 LTS 版。

### 3. 安裝 Python 依賴（後端要跑起來）

```bash
pip install fastapi "uvicorn[standard]" sse-starlette python-multipart
```

### 4. 初始化前端

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install -D tailwindcss @tailwindcss/vite
```

### 5. 驗證環境

**Terminal 1**（開 mock 後端）：
```bash
uvicorn mock_api:app --port 8000 --reload
```

**Terminal 2**（開前端）：
```bash
cd frontend
npm run dev
```

瀏覽器開 `http://localhost:5173`，看到 Vite 預設畫面就代表環境 OK 了。

---

## API 說明（你會用到的全部）

### POST `/animate`

送出題目，拿回 `task_id`：

```ts
const res = await fetch('/animate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ topic: 'pythagorean theorem' }),
})
const { task_id } = await res.json()
```

### GET `/animate/{task_id}/stream`

SSE 串流，接收 pipeline 進度事件：

```ts
const es = new EventSource(`/animate/${task_id}/stream`)
es.onmessage = (e) => {
  const data = JSON.parse(e.data)
  // data 的格式如下（type 欄位判斷）
}
```

**事件格式**：

```jsonc
// stage 進度更新
{ "stage": "rag",     "status": "running" }
{ "stage": "planner", "status": "done" }
{ "stage": "coder",   "status": "done" }
{ "stage": "render",  "status": "done" }
{ "stage": "judge",   "status": "done", "verdict": "PASS", "score": 0.87,
  "scores": { "math_correctness": 0.92, "visual_clarity": 0.81, "concept_alignment": 0.88 } }

// 心跳（忽略即可，不用更新 UI）
{ "type": "ping" }

// 錯誤
{ "stage": "judge", "status": "error" }
```

**7 個 stage**，依序出現：`rag` → `planner` → `audio` → `coder` → `render` → `judge`

### GET `/animate/{task_id}/result`

取得最終結果（pipeline 跑完後呼叫）：

```jsonc
{
  "task_id": "...",
  "status": "done",
  "video_path": "pythagorean_theorem_20260508.mp4",
  "judge": {
    "verdict": "PASS",
    "score": 0.87,
    "scores": { "math_correctness": 0.92, "visual_clarity": 0.81, "concept_alignment": 0.88 }
  }
}
```

### GET `/video/{filename}`

直接在 `<video>` tag 裡用：

```tsx
<video src={`/video/${videoPath}`} controls autoPlay />
```

---

## vite.config.ts（直接複製這個，不用自己想）

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/animate': 'http://localhost:8000',
      '/video':   'http://localhost:8000',
    },
  },
})
```

這個 proxy 讓你在開發時不用處理 CORS。

---

## UI 規格

### 整體佈局

```
┌─────────────────────────────────────────┐
│      LLManim — AI Math Animator         │
├─────────────────────────────────────────┤
│  [Topic: ___________________________]   │
│                              [Generate] │
├─────────────────────────────────────────┤
│  RAG ✓  Planner ⟳  Coder ○  Render ○  Judge ○  │
│  ██████████░░░░░░░░░░░░  40%            │
├───────────────────┬─────────────────────┤
│                   │  Math Accuracy  0.9 │
│   <video>         │  Visual Clarity 0.8 │
│                   │  Concept Align  0.85│
│                   │                     │
│                   │  Verdict: ✅ PASS   │
└───────────────────┴─────────────────────┘
```

### PipelineStages 規格

每個 stage pill 有 4 種狀態：

| 狀態 | 外觀 |
|------|------|
| `idle` | 灰底、灰字 |
| `running` | 藍底、白字、旋轉 spinner |
| `done` | 綠底、白字、✓ |
| `error` | 紅底、白字、✗ |

Stage 順序（左到右）：`RAG` → `Planner` → `Audio` → `Coder` → `Render` → `Judge`

整體進度條：`done` 的 stage 數 / 總 stage 數 × 100%

### VideoPlayer 規格

- 收到 `render done` 事件後才顯示（之前隱藏）
- 使用原生 `<video>` tag，不要裝 video.js 之類的 library
- 加 `controls` 和 `autoPlay`

### ScorePanel 規格

- 收到 `judge done` 事件後才顯示（之前隱藏）
- Verdict 用顏色區分：`PASS` 綠色、`FAIL` 紅色
- 分數顯示到小數點後 2 位（`0.87`）

---

## 執行步驟（Day by Day）

### Day 1 — Setup + 接 Mock API

1. 照上面 Setup 把環境跑通
2. 修改 `frontend/vite.config.ts`（複製上面的範本）
3. 在 `frontend/src/App.tsx` 寫最簡單的版本：
   - 一個 input + 按鈕
   - 按下去呼叫 `POST /animate`，把拿到的 `task_id` 印到 console
   - 建立 `EventSource`，把每個收到的事件印到 console

   目標：**能在 console 看到事件流出現**。

### Day 2 — PipelineStages

1. 建立 `frontend/src/components/PipelineStages.tsx`
2. 用 `useState` 管 6 個 stage 的狀態
3. SSE 事件進來時更新對應 stage 的狀態
4. 顯示進度條百分比

目標：**stage pills 能依序從灰 → 藍spinner → 綠勾**。

### Day 3 — VideoPlayer + ScorePanel

1. 建立 `VideoPlayer.tsx`：收到 `render done` 後顯示 `<video>`
2. 建立 `ScorePanel.tsx`：收到 `judge done` 後顯示評分
3. 從事件的 `scores` 欄位取出 3 個維度分數顯示

### Day 4 — 樣式 + 整合

1. 用 Tailwind 讓 UI 有展覽的質感（深色背景或白底卡片都行，自由發揮）
2. 確認 mock 流程走完整不出錯
3. 在真實後端（`api.py`）跑一次完整流程（跟 @liaozhenting 說一聲）

### Day 5 — Production Build 驗證

```bash
cd frontend && npm run build
cd ..
uvicorn api:app --host 0.0.0.0 --port 8000
```

瀏覽器開 `http://localhost:8000`，確認：
1. 輸入題目可以送出
2. 進度條正常
3. F5 重新整理不會 404

---

## 開發期間如何測試（不需要真實 AI）

後端有一個 `mock_api.py`，它會模擬整條 pipeline 的事件流，讓你不需要等 AI 就能測前端。

```bash
# Terminal 1（mock 後端，模擬完整 14 秒流程）
uvicorn mock_api:app --port 8000 --reload

# Terminal 2（前端開發 server）
cd frontend && npm run dev
```

mock 事件的時序（方便你寫測試）：

```
t=1s:  rag running
t=2s:  rag done
t=3s:  planner running
t=5s:  planner done
t=5.5s: audio running、coder running（同時）
t=7s:  audio done
t=8s:  coder done
t=8.5s: render running
t=11s: render done → 這時 VideoPlayer 要顯示出來
t=11.5s: judge running
t=14s: judge done → 這時 ScorePanel 要顯示出來
```

---

## 驗收標準

@liaozhenting 在 review 你的 PR 時會確認這些：

| 項目 | 標準 |
|------|------|
| 送出題目 | 按鈕呼叫 POST /animate，不能有 console error |
| 進度條 | 6 個 stage pills 依序更新，不跳過 |
| VideoPlayer | 只在 render done 後出現，不提前顯示 |
| ScorePanel | 顯示 3 個維度 + verdict |
| F5 重整 | 不 404 |
| Production build | `npm run build` 零 TypeScript 錯誤 |

---

## 常見問題

**Q：mock 後端的事件都出來了，但 UI 沒更新？**
確認 `EventSource` 的 `onmessage` 有正確呼叫 `setState`。React state 更新要用 `useState` 的 setter，不能直接 mutate 物件。

**Q：`/video/{filename}` 回 404？**
mock 後端不提供真實影片，這是正常的。只有接真實 `api.py` 後才有影片。可以先用一個假的 mp4 URL 或隱藏 VideoPlayer 的測試。

**Q：Tailwind class 沒效果？**
確認 `vite.config.ts` 裡有 `tailwindcss()` plugin，且 `src/index.css` 有 `@import "tailwindcss";`。

**Q：build 有 TypeScript 錯誤？**
先確認 SSE 事件的 type annotation 正確，`JSON.parse(e.data)` 回傳的是 `unknown`，要做 type assertion 或 type guard。

**Q：要怎麼跑真實後端？**
跟 @liaozhenting 說，要在他的機器上跑（需要 .env 和 AI API key）。你的開發流程只需要 `mock_api.py`。

---

## 目錄結構（你需要關心的部分）

```
LLManim_Agent/
├── api.py              ← 已寫好，你不用改（真實後端）
├── mock_api.py         ← 已寫好，你不用改（Mock 後端）
├── frontend/           ← 你的主要工作在這裡
│   ├── src/
│   │   ├── App.tsx
│   │   └── components/
│   │       ├── TopicInput.tsx
│   │       ├── PipelineStages.tsx
│   │       ├── VideoPlayer.tsx
│   │       └── ScorePanel.tsx
│   └── vite.config.ts
└── stable_outputs/     ← 影片輸出目錄（不要碰）
```
