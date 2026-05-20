# BenchmarkJudge — Design Document

> 新建模組：將 candidate 影片相對於人類優化過的 benchmark 影片打分（0-100）。
> 與舊 FJ 並存，不取代。FJ 繼續在 RefiningLoop 中用，BenchmarkJudge 用於 eval / paper。

---

## 1. 目標與範圍

### 1.1 目標
給定一部 candidate.mp4 與一部對應題目的 benchmark.mp4（人類手工優化過），
輸出一個 0-100 分數（100 = 完全達到 benchmark 水準），並附拆解的維度分數。

### 1.2 範圍
- ✅ Post-hoc 評估：跑完 main.py 後，用此工具給出對標分數
- ✅ Paper / report 數據生成
- ❌ **不**用於 RefiningLoop（速度慢、需要 benchmark，不適合 in-loop）
- ❌ **不**取代 FJ（FJ 仍負責 RefiningLoop 的 PASS/FAIL 訊號）

### 1.3 非目標
- candidate 不能拿超過 100 分（即使在某維度比 benchmark 好，最高就是 100）
- 不評估 audio / TTS quality（純看視覺）
- 不對抗 benchmark 本身的瑕疵（假設 benchmark 是該題的合理上限）

---

## 2. 架構

```
┌──────────────────────────────────────────────────────────────────┐
│  BenchmarkJudge.judge(candidate_mp4, benchmark_mp4,              │
│                       question_topic, candidate_code, ...)        │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Phase A: Grid construction                                  │  │
│  │   - candidate frames (4-6 張，採樣方式跟 FJ 一致)            │  │
│  │   - benchmark frames (同樣 4-6 張)                          │  │
│  │   - 拼成 2-row labeled grid (上 candidate / 下 benchmark)   │  │
│  │     每張 tile 角落印 "C1/C2/.../B1/B2/..."                  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                              ↓                                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Phase B: Opus pairwise vision (multi-pass + position swap)  │  │
│  │   每 pass 對 3 dim 做 Likert 比較 + evidence                 │  │
│  │   - completeness (視覺涵蓋度)                               │  │
│  │   - accuracy     (數學正確/視覺隱喻)                         │  │
│  │   - clarity      (排版/可讀性)                              │  │
│  └────────────────────────────────────────────────────────────┘  │
│                              ↓                                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Phase C: Deterministic signals (補強)                       │  │
│  │   - code review (Claude Opus 讀 candidate code → math_score)│  │
│  │   - layout audit (LayoutAuditor → candidate + benchmark)    │  │
│  │   - difference: candidate_layout_score - benchmark_layout   │  │
│  └────────────────────────────────────────────────────────────┘  │
│                              ↓                                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Phase D: Score synthesis (Python 端)                        │  │
│  │   per_dim_100 = base100 + likert_offset + det_adjustment    │  │
│  │   final_100   = 0.4·accuracy + 0.3·completeness + 0.3·clarity │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. 維度定義

### 3.1 completeness（涵蓋度，權重 0.30）
**問**：candidate 是否包含 benchmark 所有關鍵視覺元素？
- benchmark 有的圖形、公式、標籤、過程步驟，candidate 有沒有？
- 不問「兩邊長得一不一樣」，問「該講的有沒有講」

**evidence 形式**：列出 benchmark 有但 candidate 沒有的元素（或反之）

### 3.2 accuracy（正確性，權重 0.40）
**問**：candidate 教的數學內容是否正確、視覺隱喻是否準確？
- 公式對不對（vision + code 雙重驗證）
- 「pizza」是不是真的畫成圓形（不是方形）
- 角度標記值對不對
- 跟 benchmark 比較，candidate 有沒有引入新錯誤

**evidence 形式**：列出 candidate 的數學/視覺錯誤

### 3.3 clarity（清晰度，權重 0.30）
**問**：candidate 的排版/可讀性 vs benchmark
- 文字遮擋、出框、過密
- LayoutAuditor 數據比較
- 視覺 hierarchy 是否清楚

**evidence 形式**：列出 candidate 的 layout 缺陷

---

## 4. Vision Prompt 設計

### 4.1 System prompt
```
你是 AI 生成的數學教學動畫的對標評審員。

你會收到一個 2-row × N-col 的 grid 圖：
- 上排 (C1, C2, ...) = candidate animation 的時序截圖
- 下排 (B1, B2, ...) = benchmark animation 的時序截圖（人類已優化的標準答案）

兩部影片試圖教同一個數學概念。Benchmark 是教學品質的合理上限。

針對 completeness / accuracy / clarity 三個維度，對每維輸出：
  - likert: one of {"much_better", "better", "same", "worse", "much_worse", "broken"}
    含義：candidate vs benchmark 在這個維度的相對位置
    - much_better: candidate 明顯比 benchmark 還好（罕見，請慎用）
    - better:      candidate 略好
    - same:        基本持平
    - worse:       candidate 稍差
    - much_worse:  candidate 明顯差
    - broken:      candidate 在此維度上完全失敗
  - evidence: 1-2 句話列出具體觀察（哪張 frame、什麼問題）

純看視覺；如果無法判斷（例如 frame 沒抓到關鍵時刻），明說「inconclusive」。

Output strict JSON, no other text:
{
  "completeness": {"likert": "...", "evidence": "..."},
  "accuracy":     {"likert": "...", "evidence": "..."},
  "clarity":      {"likert": "...", "evidence": "..."}
}
```

### 4.2 User prompt（per pass）
```
Question being taught: {question_topic}

Optional candidate code summary: {math_review_summary if exists}

Grid layout: top row C1...Cn = candidate frames, bottom row B1...Bn = benchmark frames.

Output the JSON object.
```

### 4.3 Position swap
為消除 grid 位置偏誤，跑 2 個版本：
- normal: candidate 在上、benchmark 在下
- swapped: candidate 在下、benchmark 在上 + 標籤改成 "C/B" 對應

每個版本跑 N passes（預設 3），合計 6 passes 投票。

---

## 5. Score Synthesis（Python 端，不交給 Vision）

### 5.1 Likert → score offset

**起始值（calibration 後可調）**：
```python
LIKERT_OFFSET = {
    "much_better":  0,    # cap at 100, no bonus
    "better":       0,
    "same":         0,
    "worse":      -15,    # 小瑕疵，有感扣分
    "much_worse": -30,    # 大瑕疵，降級到 70 區
    "broken":     -60,    # 完全崩壞，不及格
    "inconclusive": -5,   # 無資訊時輕罰
}
```

**為什麼選這組值（vs 原本 -10/-25/-50）**：
- LLM-as-judge 普遍有寬容偏誤（MT-Bench 2306.05685 證實 verbosity/self-enhancement bias 推高分數）
- 用戶 16 部 golden set 親自證實：concept_alignment GPT-4o ρ=-0.01、Opus ρ=-0.525，飽和率 33-53%
- -10 offset 太鬆：兩個維度小瑕疵 final 還拿 94，失去 benchmark 區分度
- -15 offset：兩個小瑕疵 → 91；一個 worse + 一個 much_worse → 86.5；
  有明顯下落但不是懸崖

**最終值要靠 calibration 決定**，這只是起始點。

「最高 100」原則：candidate 比 benchmark 好不加分，差的話扣分。
這跟用戶決策一致：「candidate 超越 benchmark」應該升級 benchmark，而不是給高分。

### 5.2 Per-dim score（從多 pass 投票合成）
```python
# 6 passes（3 normal + 3 swapped）的 likert votes
votes = ["worse", "worse", "same", "worse", "same", "worse"]

# Mode（眾數）= "worse" → offset = -10
# 用眾數而非平均，避免極端 likert（如 broken）拉低整體
per_dim_score = 100 + LIKERT_OFFSET[mode]
```

### 5.3 Deterministic 補強（accuracy + clarity）
```python
# accuracy 維度：併入 Claude 讀 code 的 math_score
if math_score is not None:
    # math_score 1-5 → 0/-5/-15/-30/-60 penalty
    math_penalty = {5:0, 4:-5, 3:-15, 2:-30, 1:-60}[math_score]
    accuracy_score = min(accuracy_score, 100 + math_penalty)

# clarity 維度：併入 LayoutAuditor
# candidate_layout - benchmark_layout（兩個都跑 LayoutAuditor）
layout_gap = (candidate_layout - benchmark_layout)  # negative = candidate worse
layout_penalty = layout_gap * 10  # -1 score = -10 pts
clarity_score += layout_penalty
clarity_score = max(0, min(100, clarity_score))
```

### 5.4 Final（with accuracy gate — 平滑版 veto）

**問題**：純線性加權會發生「教錯數學但 clarity/completeness 滿分 → 拿 80 分」的荒謬情況。

**簡單但錯誤的解**：hard veto ceiling
```python
# ❌ Don't use this — cliff edge at accuracy=75
if accuracy_score < 75:
    final_100 = min(final_100, accuracy_score)
```

cliff 問題：accuracy=74 跟 75 差別巨大，且失去排序鑑別力（30 跟 50 都被壓到 < accuracy）。

**正確解：平滑 multiplier**
```python
final_100 = round(
    0.40 * accuracy_score
  + 0.30 * completeness_score
  + 0.30 * clarity_score
)

# Accuracy gate: 平滑衰減，accuracy < 75 開始整體拉低
# accuracy=80 → factor=1.0（不影響）
# accuracy=60 → factor=0.8（整體 × 0.8）
# accuracy=30 → factor=0.4（整體 × 0.4）
accuracy_factor = min(1.0, accuracy_score / 75)
final_100 = round(final_100 * accuracy_factor)
```

**設計依據**：
- Prometheus 2 (2405.01535) 強調 rubric 嚴格性，但沒提 veto 機制
- Design2Code (2403.03163) 用線性加權但領域不涉及高利害教育內容
- **教育影片教錯數學是「下限事件」**，必須有機制壓低，但平滑衰減比 cliff veto 更穩健
- 平滑衰減保留鑑別力：accuracy=30 跟 50 仍有差，方便 RefiningLoop 收斂訊號

---

## 6. API & Files

### 6.1 主要檔案
- `agents/utils/benchmark_judge.py`（新建，仿 `pairwise_judge.py`）
- `evaluation/benchmark_set/`（新建目錄，放 benchmark mp4）
  - 結構：`evaluation/benchmark_set/<question_id>/benchmark.mp4` + `benchmark.py`
- `evaluation/benchmark_calibration.py`（新建，仿 `judge_calibration.py`）

### 6.2 BenchmarkJudge class signature
```python
class BenchmarkJudge:
    def __init__(self, llm_client=None, passes=3, model="claude-opus-4-7"):
        ...

    def judge(self,
              candidate_video: str,
              benchmark_video: str,
              question_topic: str,
              candidate_code: str = None,           # for math review補強
              candidate_state_log: str = None,      # for LayoutAuditor
              benchmark_state_log: str = None,      # for LayoutAuditor
              ground_truth: dict = None) -> dict:
        """
        Returns:
        {
          "final_100": 73,
          "scores": {
            "completeness": 90,
            "accuracy":     70,
            "clarity":      65
          },
          "likert_votes": {
            "completeness": ["same", "same", "worse", ...],
            ...
          },
          "evidence": {
            "completeness": "...",
            ...
          },
          "deterministic_adjustments": {
            "math_penalty": -15,
            "layout_gap":   -2
          }
        }
        """
```

### 6.3 Benchmark 影片庫結構
```
evaluation/benchmark_set/
├── README.md          # how to add a new benchmark
├── V02_Q050/
│   ├── benchmark.mp4
│   ├── benchmark.py
│   ├── scene_state_log.json   # 可選
│   └── meta.json              # 題目、答案、優化備註
├── V13_MEX_110_10/
│   ├── benchmark.mp4
│   ├── ...
└── ...
```

`meta.json`:
```json
{
  "question_id": "MEX_110_10",
  "topic": "將半徑為 6 的圓形紙片沿著兩條半徑剪開...",
  "ground_truth": {"answer": "..."},
  "optimization_notes": "原 candidate 排版亂，手動調整 next_to buff 與 FadeOut 順序",
  "rendered_at": "2026-05-20",
  "duration_sec": 95.3
}
```

---

## 7. Calibration Plan

### 7.1 重新標 human_score
原 golden_set 的 1-5 整數打分不適用（那是絕對打分）。
新增 `evaluation/golden_set/benchmark_labels.json`：
```json
[
  {
    "candidate_id": "V02_Q050",
    "candidate_video": "runs/.../video.mp4",
    "candidate_code": "runs/.../code.py",
    "benchmark_id": "BM_Q050",
    "benchmark_video": "evaluation/benchmark_set/V02_Q050/benchmark.mp4",
    "human_score_0_100": 95,
    "human_dim_scores": {
      "completeness": 100,
      "accuracy":     90,
      "clarity":      95
    }
  },
  ...
]
```

### 7.2 Calibration 指標
- Spearman ρ (BJ final_100 vs human_score_0_100)：主指標
- Pearson r (同上)
- MAE (絕對誤差 in 0-100 scale)
- Per-dim ρ
- Likert 投票分布（檢查有沒有特定 likert 被永遠跳過）

### 7.3 驗收標準
- Overall ρ ≥ 0.7（n=16 仍粗糙，但相對 baseline 必須提升 ≥ 0.15）
- 無單一 likert 飽和（任何 likert > 80% 的話需重看 prompt）

---

## 8. 計算與成本

### 8.1 Per-judgement cost
- Grid 拼接：~2s (ffmpeg, local)
- Opus passes：6 passes × ~30s = ~3 min（並行可降到 ~30s）
- LayoutAuditor candidate + benchmark：~20ms
- Math review (Claude Opus)：~10-30s（可選）
- **總計**：1-4 分鐘 per judgement

### 8.2 Calibration 全跑 (16 部) cost
- 16 × 4 min = ~1 小時（並行可降）
- Opus quota：每 pass 約 3-5k tokens（grid 圖大 + JSON 輸出），16 × 6 × 5k = 480k tokens
- **不會打爆月費 quota**（Claude Max 應該夠）

### 8.3 Benchmark 影片庫成本
- 你手工優化 16 部，每部 30-60 分鐘 = **8-16 小時**
- **這是最大的人力成本**，不能省

---

## 9. 風險與緩解

| 風險 | 緩解 |
|---|---|
| Opus 對「same」太寬鬆，多數都打 same → ρ 低 | Likert 投票眾數要 ≥ 4/6 才採用，否則降級為 inconclusive |
| Grid 截圖採樣不對齊（candidate vs benchmark 時序不同步）| 採樣百分比一致（兩部都用 15/38/62/88%）；不強求 frame-by-frame 對齊 |
| Benchmark 本身有瑕疵 → 評分系統失真 | meta.json 紀錄 optimization_notes，定期 review benchmark |
| Position bias（candidate 在上 vs 下打分不同）| Position swap 已涵蓋 |
| Math + Layout penalty 過重 → final 動不動 < 50 | calibration 看結果調 penalty 係數 |
| 16 部 benchmark 不足以 calibrate | 先跑 calibration 看 baseline ρ；不夠再補 |

---

## 10. 實作順序

1. **P1 — Mock proof of concept**（半天）
   - 不寫 benchmark_judge.py，直接用 pairwise_judge.py 跑 1 對 case，看 likert 投票是否合理
   - 如果這步就敗（例如 Opus 對截圖不會做 pairwise 區分），整個架構要重想

2. **P2 — 寫 benchmark_judge.py**（1 天）
   - 框架仿 pairwise_judge.py
   - 加 deterministic 補強邏輯
   - 寫 unit test（mock LLM 回 likert vote，驗證 score synthesis 公式）

3. **P3 — 建 1 部 benchmark 影片**（你手工，30 分鐘）
   - 挑 V02_Q050（你打 5 分的好影片）當第一個 benchmark
   - 跑 BenchmarkJudge(V02 candidate, V02 benchmark)，預期 final ~95（兩部都好）

4. **P4 — 建剩下 15 部 benchmark + 標 human 0-100 分**（你 8-16 小時 + 1-2 小時標註）

5. **P5 — calibration 全跑 + 看 ρ**（1 小時 + 看數據）

6. **P6 — 調 prompt / penalty 公式 / 二輪 calibration**（iterative）

---

## 11. 與舊 FJ 的關係

| 場景 | 用哪個 |
|---|---|
| RefiningLoop 內 PASS/FAIL | FJ |
| 單 candidate 絕對品質評估 | FJ |
| Candidate vs benchmark 對標 0-100 | **BenchmarkJudge** |
| Paper 數據 / A/B test | BenchmarkJudge |
| 沒有 benchmark 影片時 | FJ |

兩者共用：
- `LayoutAuditor`（兩個都用）
- Claude Opus code review（兩個都用，但 prompt 略不同）
- `_extract_frames`（兩個都用，但 BJ 多一步拼 2-row labeled grid）

---

## 12. 待用戶確認

1. **Likert offset 值（-10/-25/-50）是否合理**？或要更嚴/更鬆
2. **權重 0.4/0.3/0.3**（accuracy/completeness/clarity）是否合理
3. **是否同意 P1 mock proof of concept 先**（半天就能知道架構可行性）
4. Benchmark 影片庫**路徑命名規則**是否合理（用 candidate_id 命名 vs 用 question_id 命名）
