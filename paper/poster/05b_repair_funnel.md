# 05b — 三層自我修復漏斗圖（v2 新增）

**位置**：左中（區塊 ⑤），約 28 × 12 cm
**區塊大標**：三層自我修復 Three-Layer Self-Repair（44pt）

⚠️ 這張圖是**核心創新視覺化**，必須讓評審 10 秒內看懂「為什麼三層、為什麼這順序」。

---

## 圖片素材

**檔案**：`figures/figure_repair_funnel.png`（已生成）
**生成腳本**：`figures/make_repair_funnel.py`（可修改數字後重跑）

## 圖內容說明

| Layer | 名稱 | 機制 | 成本 | 攔截率* |
|---|---|---|---|---|
| Layer 1 | AST Linter | 30+ ManimCE 規則靜態掃描 | **零成本** | ~50% |
| Layer 2 | Layout Audit | 確定性幾何 AABB 審計 | **零成本** | ~30% |
| Layer 3 | Vision Audit | GPT-4o Chain-of-Visual-Thought | $0.02/題 | ~20% |

\* 攔截率為架構設計分配示意，實際比例隨題目難度浮動

通過後進入 Reflexion 修正迴圈（主迭代上限 5 次），失敗則回到 Layer 1 重生成。

---

## 副標文字（圖下方）

```
設計哲學：Cheap deterministic checks first, expensive vision last

▍ 為何分三層？
  將「便宜的確定性檢查」放在「昂貴的視覺推理」之前，
  讓多數錯誤在零成本層被攔截，僅 ~20% 案例需動用 GPT-4o。

▍ Vision Confidence Gradient（核心創新）
  Layer 3 不採二元 PASS/FAIL，改以 1-5 信心評分：
  conf ≥ 4 PASS；conf = 3 且預算將盡時軟通過；
  conf < 3 觸發 Reflexion 重生成，避免邊際案例陷入無效迴圈。
```

---

## 視覺重點

- 三層用 **綠 / 黃 / 紅** 配色 = 成本遞增（已在圖中實作）
- Reflexion 回流箭頭用虛線藍色（已實作）
- 「Vision Confidence Gradient」這個名詞**新穎性高**，是論文 LBR 沒寫的延伸貢獻，可加底線強調

---

## ⚠️ 真實數字替換指引

如果要把示意攔截率改成真實值，從以下位置撈：
```bash
# 從各 run session log 撈
grep -E "(linter_fail|layout_fail|vision_fail|verdict.*FAIL)" \
     runs/*/session.jsonl | awk '{...}'
```
或直接看 `paper/dept_report/run_data/*.csv` 的 `Error Types` 與 `Defects` 欄位統計。
