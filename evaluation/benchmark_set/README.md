# Benchmark Set — RAG-150 實驗 C 組

30 題人工精修 benchmark 影片庫。對應 `evaluation/experiment_sample_30.json`。
BenchmarkJudge (`agents/utils/benchmark_judge.py`) 會把 A/B 組 candidate 跟此處的 `benchmark.mp4` 比，給 0-100 分。

## 目錄結構

```
benchmark_set/
├── README.md            # 本檔
├── meta.json            # 全體進度索引（30 題 status 表）
└── <QXXX>/              # 每題一個資料夾，子目錄名 = case id
    ├── benchmark.mp4    # 最終定稿影片（必須）
    ├── code.py          # 對應 ManimCE 原始碼（必須）
    ├── notes.md         # 製作過程備忘（可選）
    └── raw/             # Opus 初稿 / 中間版本（可選，方便回看）
```

## 製作流程（每題 ~30-60 分鐘）

1. 看 `experiment_sample_30.json` 找該題的 `topic` / `answer` / `solution`
2. 跑 Opus 豪華模式產初稿（命令見下節）
3. 把 `runs/<session>/QXXX/code.py` + `video.mp4` 複製到 `benchmark_set/QXXX/`
4. 人工精修 `code.py` 直到動畫無破綻
5. `manim -pql code.py <SceneName>` 重渲，輸出存成 `benchmark.mp4`
6. 更新 `meta.json` 把該題 status 改 `done`

## 完成判準（升 `status: done` 的條件）

- 數學完全正確（每步、最終答案都對齊 `solution`）
- 無 overlap / 出框 / 字幕遮擋
- 動畫節奏合理（每步 1.5-3s，無冷場 > 1.5s）
- 字幕為英文（MathTex 含中文會在無 ctex 環境炸；用戶 2026-05-19 決策）
- `manim -ql` 本機可重渲（用 ManimCE 0.20）

## 約束

- **不要用任何選擇題**（已全排除）
- benchmark 拍完才能跑 A/B 評分；BJ 缺 benchmark 會 degrade 到 FJ
- 用戶親自操刀，Claude 不要自動生成成品（plan 已決議）
