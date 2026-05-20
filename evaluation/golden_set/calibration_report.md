# FinalJudge Calibration Report — Phase A Baseline

**Sample size**: n = 16


## Per-Dimension Stats (FJ vs Human)

| Dimension | n | Spearman ρ | Pearson r | MAE | FJ var | Human var | FJ sat | Human sat |
|---|---|---|---|---|---|---|---|---|
| math_correctness | 16 | 0.352 | 0.537 | 0.875 | 0.762 | 1.396 | 0.500 | 0.438 |
| concept_alignment | 15 | -0.525 | -0.525 | 1.733 | 0.238 | 1.695 | 0.333 | 0.267 |
| visual_clarity | 15 | 0.538 | 0.487 | 1.067 | 0.971 | 1.638 | 0.200 | 0.200 |
| spatial_layout | 15 | 0.173 | 0.202 | 1.400 | 1.838 | 1.352 | 0.667 | 0.200 |

## Overall (weighted_total vs human overall)

- n: 16
- Spearman ρ: 0.317
- Pearson r:  0.491

## Binary Verdict Agreement (PASS/FAIL)

- TP=4  TN=4  FP=7  FN=1  ERROR=0
- Accuracy: 0.500
- Cohen's kappa: 0.123

## Per-Video Detail

| ID | Expected | Actual | Weighted | Veto | Outcome |
|---|---|---|---|---|---|
| V01_proof_triangle | FAIL | PASS | 4.214 |  | FP |
| V02_Q050 | PASS | PASS | 4.700 |  | TP |
| V03_Q18 | FAIL | PASS | 4.850 |  | FP |
| V08_HSAT_115_17 | PASS | PASS | 4.850 |  | TP |
| V09_MEX_111_7 | FAIL | FAIL | 4.000 | low_dimension_visual_clarity | TN |
| V10_MEX_NEW_03 | PASS | FAIL | 3.250 | low_dimension_spatial_layout | FN |
| V11_HSAT_109_C | FAIL | PASS | 3.950 |  | FP |
| V13_MEX_110_10 | PASS | PASS | 3.900 |  | TP |
| V14_ELEM_01_20260328 | FAIL | FAIL | 2.429 | critical_code_issue | TN |
| V15_HIGH_03_20260406 | FAIL | PASS | 4.450 |  | FP |
| V16_HIGH_05_20260421 | FAIL | PASS | 4.100 |  | FP |
| V17_Q19 | PASS | PASS | 4.850 |  | TP |
| V18_HIGH_02_20260421 | FAIL | FAIL | 3.650 | low_dimension_spatial_layout | TN |
| V19_HIGH_04_20260421 | FAIL | PASS | 4.300 |  | FP |
| V20_ELEM_03_20260421 | FAIL | FAIL | 4.000 | low_dimension_visual_clarity | TN |
| V21_MID_02_20260421 | FAIL | PASS | 4.550 |  | FP |

## Diagnosis Hints

- ⚠️  **math_correctness**: saturation=50.00% — FJ 太常打滿分，缺鑑別力（B1 主要解這個）
- ⚠️  **concept_alignment**: ρ=-0.52 (low) — 排序與人類差很多，這維可能要重做
- ⚠️  **concept_alignment**: FJ variance=0.24 — FJ 對所有影片打差不多分數
- ⚠️  **spatial_layout**: ρ=0.17 (low) — 排序與人類差很多，這維可能要重做
- ⚠️  **spatial_layout**: saturation=66.67% — FJ 太常打滿分，缺鑑別力（B1 主要解這個）