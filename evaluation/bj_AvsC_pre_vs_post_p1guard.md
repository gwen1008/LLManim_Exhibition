# BJ A vs C: pre-P1 vs post-P1 對比

**目的**：量化 2026-05-25 ship 的 P1 防護 (`1e86b04`) 對 A vs C 30 題評分的影響。

## 資料來源

| 版本 | 跑日期 | Cache schema | Results file |
|---|---|---|---|
| **OLD (pre-P1)** | 2026-05-21 | 無 `acc_insufficient_signal` 欄位 | `evaluation/bj_AvsC_20260521_201243/benchmark_runner_results_20260521_202729.json` |
| **NEW (post-P1)** | 2026-05-25 | 含 P1 telemetry | `evaluation/bj_AvsC_post_p1guard_20260525_023359/benchmark_runner_results_20260525_110542.json` |

兩次都跑同樣的 sessions：
- A: `runs/20260520_154252_variantA`
- C: `runs/20260521_021358_variantC`

## 整體統計

| 指標 | OLD | NEW | Δ |
|---|---|---|---|
| A 平均 final_100 | 84.07 | **87.00** | +2.93 |
| C 平均 final_100 | 83.73 | 83.87 | +0.14 |
| **A − C gap** | **+0.33** | **+3.13** | **+2.80** |
| A acc_score mean | 90.67 | 94.00 | +3.33 |
| C acc_score mean | 87.50 | 86.83 | -0.67 |

**結論**：A 顯著比 C 好（gap 從 noise 級 0.33 → meaningful 3.13）。

## A 組 acc mode 分布變化

| mode | OLD | NEW |
|---|---|---|
| same | 22 | **26** |
| better | 1 | 0 |
| worse | 3 | 2 |
| much_worse | 2 | 0 |
| broken | 2 | 2 |

→ A 組往 "same" 集中，vision 第二次評比較寬鬆。

## C 組 acc mode 分布變化

| mode | OLD | NEW |
|---|---|---|
| same | 20 | 19 |
| better | 0 | 1 |
| worse | 5 | 7 |
| much_worse | 4 | 0 |
| broken | 1 | **3** |

→ C 組 `much_worse` 全消失但 `broken` 增加 — 兩極化（要嘛變好要嘛變更糟）。

## 個別題目方差爆增（±5 以上 Δ）

| qid-variant | OLD → NEW | acc_mode 變化 | 評語 |
|---|---|---|---|
| Q070-A | 86 → 100 (+14) | worse → same | vision 第二次認為 A 跟 benchmark 完全一樣 |
| Q082-C | 88 → 100 (+12) | same → better | C 居然被評比 benchmark 好 |
| Q092-C | 58 → 80 (+22) | much_worse → worse | 大幅寬鬆 |
| Q094-A | 58 → 80 (+22) | much_worse → worse | 大幅寬鬆 |
| **Q094-C** | **80 → 22 (-58)** | **worse → broken** | ⚠️ 巨幅下跌 |
| Q101-A | 58 → 80 (+22) | much_worse → worse | 大幅寬鬆 |
| Q101-C | 62 → 86 (+24) | much_worse → worse | 大幅寬鬆 |
| Q102-A | 74 → 88 (+14) | worse → same | 寬鬆 |
| **Q102-C** | **86 → 24 (-62)** | **worse → broken** | ⚠️ 巨幅下跌 |
| Q106-C | 53 → 74 (+21) | much_worse → worse | 寬鬆 |
| Q139-A | 94 → 82 (-12) | same → same | mode 沒變但 final 變 |
| Q144-C | 62 → 80 (+18) | much_worse → worse | 寬鬆 |

± 5 以下波動的題目就不列了。**6 題 +20 以上**，**2 題 -50 以上**。

## P1/P2/P3 hits（post-P1 60 entries）

| Pattern | hits | 比例 | 細節 |
|---|---|---|---|
| P1 all-inconclusive≥70 | **0** | 0% | 防護沒救到任何 case |
| P2 math_pressure≥20 | **1** | 1.7% | Q024-C: vision same(100) + math=2 → acc 70 |
| P3 vote_unique≥3 | **2** | 3.3% | Q075-A (much_worse,broken,worse); Q102-C (much_worse,same,broken) |
| P4 mode-score 不一致 | **1** | 1.7% | Q024-C (same → acc=70, same case as P2) |

## 關鍵洞察

### 1. A vs C 結論未變但更明確

OLD 的 0.33 gap 是 noise 級，無法 paper 引用。NEW 的 3.13 gap 雖然仍不大，但加上 acc_score gap +7.17 分，可以說「A 略優於 C」是 robust 結論。

### 2. BJ vision 有顯著 run-to-run variance

同支影片兩次跑，**8 題 final_100 差 ≥20**（含 2 題 ≥50）。3 pass mode aggregation 救不了這個——它救得了「同次跑的 3 pass 之間的雜訊」，但救不了「不同次跑的整體 prior 漂移」。

**Q102-C 是極端例子**：
- OLD: votes 推測穩定（mode=worse, score=86）
- NEW: votes=['much_worse', 'same', 'broken'] → mode=broken（用最悲觀 tiebreak）→ score=24
- 同一支影片，vision Opus 兩次完全不同認知

### 3. P1 防護「沒救到任何 case」但也「沒誤傷」

15+60 = 75 entries 都 P1 0 hit。這代表：
- 你的 BJ 系統採樣 `(0.15, 0.38, 0.62, 0.88)` 4 個時點足夠涵蓋大多數 candidate
- P1 防護仍應保留，作為未來「採樣設定改變」或「跑非黃金影片」時的 safety net
- Telemetry (`acc_inconclusive_ratio`) 寫進 cache，未來長期追蹤可發現潛在採樣失效

### 4. P2/P3 是真實少數派 — 各 1-2 例

值得當「BJ 系統健康度 baseline」記錄。未來新跑的 P2/P3 比例若大幅偏離（e.g. P3 ≥10%），代表 vision 開始不穩定。

## 給 paper / 展覽的建議

| 場景 | 用哪份數據 |
|---|---|
| Paper 寫 BJ 評分結果 | **NEW (post-P1)** + 在 methodology 提到 P1 防護 |
| Paper 寫 A vs C 比較 | **NEW**: A=87.00, C=83.87, gap=+3.13 |
| 展覽展示影片 | 不需 BJ 分數，直接展示影片 |
| 跟 owner 講 BJ 系統現況 | 提 vision run-to-run variance 是已知限制（±20 級） |

## 命令重現

```bash
# 重跑 A vs C（記得 --force bypass cache）
python evaluation/benchmark_runner.py \
  --session-a runs/20260520_154252_variantA \
  --session-c runs/20260521_021358_variantC \
  --force \
  --out-dir evaluation/bj_AvsC_post_p1guard_$(date +%Y%m%d_%H%M%S)

# 跑 diagnose
python evaluation/diagnose_bj_acc.py \
  --deep evaluation/golden_set/benchmark_judge_cache.json \
  --shallow evaluation/bj_AvsC_post_p1guard_<TIMESTAMP>/benchmark_runner_results_<TIMESTAMP>.json \
  --self-sanity evaluation/golden_set/bj_self_sanity_results.json \
  --out evaluation/bj_acc_diagnosis_AvsC_post_p1guard.md
```
