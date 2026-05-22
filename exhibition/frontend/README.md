# Exhibition Frontend

組員前端工作目錄。**完整 spec 請看 [`../../docs/exhibition_interface.md`](../../docs/exhibition_interface.md)**。

## TL;DR

- **Deadline**: 2026-05-26 (二) 晚上
- **賣點**: 並排對比「純 Opus 一發」vs.「本系統 (multi-agent pipeline)」
- **你的裁量範圍**: 整個前端 UI/UX、技術選型、設計風格（React/Vue/SvelteKit/Astro 皆可）
- **不能改的**: API endpoint 名稱、JSON schema、必須包含對比賣點、必須顯示 baseline 公平性聲明

## 快速開始

```bash
cd exhibition/frontend

# 框架自選，舉例 Vite + React
npm create vite@latest . -- --template react-ts
npm install
npm run dev
```

## Mock data

`/api/gallery` 還沒上線前，前端可直接 fetch `/static/data/gallery.json` 開發。我會先放一個假資料版。

## 交付

- `exhibition/frontend/dist/` — `npm run build` 產出的靜態檔
- FastAPI 會把這個目錄掛到 `/`

## 詳細規格

→ [`docs/exhibition_interface.md`](../../docs/exhibition_interface.md)

包含：
- 所有 API endpoint + JSON schema
- 靜態素材路徑
- 頁面最低需求
- 部署方式
- 賣點包裝建議
