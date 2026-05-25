# BenchmarkJudge Calibration Report

**Sample size**: n = 1  (dropped: 0 insufficient_passes, 0 errored)


## Overall (BJ final_100 vs human_final_100)

- n: 1
- Spearman ρ: —
- Pearson r:  —
- MAE: 0.000
- BJ variance: 0.000   Human variance: 0.000

## Per-Dimension (where human_dim provided)

| Dim | n | ρ | r | MAE | BJ var | Human var |
|---|---|---|---|---|---|---|
| completeness | 1 | — | — | — | — | — *insufficient data* |
| accuracy | 1 | — | — | — | — | — *insufficient data* |
| clarity | 1 | — | — | — | — | — *insufficient data* |

## Per-Video

| ID | BJ | Human | Δ | comp/acc/clar mode | Notes |
|---|---|---|---|---|---|
| BV_PLACEHOLDER_Q050_self | 100 | 100 | 0.0 | same/same/same | PLACEHOLDER — self-vs-self pipeline smoke. Replace once real benchmark videos exist in evaluation/benchmark_set/. |

## Hints

- ⚠️  BJ variance=0.0 (低) — 鑑別力不足