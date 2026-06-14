# Solver 層架構設計 — 解題與視覺規劃解耦

> 狀態：設計提案（未實作）。撰於 2026-06-01。
> 目標：① 提供更豐富、專業、**可驗證**的解題步驟 ② 卸下 Planner 的解題負擔，提升影片規劃品質。

---

## 1. 問題陳述（為什麼要做）

### 現況：解題與規劃耦合在單一 Planner LLM call

```
topic ──► Planner（PHASE 0 ToT + PHASE 1 Layout + PHASE 2 解題&座標 + PHASE 3 JSON）──► Coder
                ▲
        LLMANIM_SOLUTION（外部環境變數；互動模式下永遠為空）
```

三個結構性缺陷（皆有 code 佐證）：

1. **解題在 blueprint schema 裡是隱形的**。`templates.py:116-193` 的 JSON schema 只有 `layout_plan` / `sequence` / `narrative`，**沒有任何結構化解題欄位**。數學推導被溶進 25 字上限、一句一步的 `narrative`（`templates.py:78-99`）——為配合動畫節奏而犧牲數學完整性。這正是「解題步驟不夠豐富專業」的直接成因。

2. **解題沒有驗證閘**。互動模式（無 `LLMANIM_SOLUTION`）下，Planner 在生成 blueprint 的同一次 call 裡順手算座標/交點（`templates.py:71-74`），**算錯沒人擋**。下游 Coder/Vision/FinalJudge 都不重算數學。結論：系統「會解題」是假象——只在外部餵了標準答案時（eval 模式）才看起來會。eval 95.1% 答對率來自 `run_evaluation.py:101-106` 餵進來的 ground_truth，不是系統自身能力。

3. **認知過載**。單一 LLM 同時要做：數學推導 + ToT 視覺選擇 + 精確座標計算 + Layout 分區 + 旁白字數控制。任一項都被擠壓，解題與規劃互相拖累。

### Prompt 內部自相矛盾

`templates.py:17-18`（有 SOLUTION 就跳過數學）與 `templates.py:71-74`（你必須算出所有交點座標）在 eval 模式下衝突：外部 solution 通常只有最終答案、無逐點座標，Planner 仍得自行補算座標——**這塊一樣無驗證**。

---

## 2. 解法：插入獨立的 Solver 層（三層 neuro-symbolic）

不推翻 Planner，在它**前面**加一層。

```
topic ──► Solver ──► solution_tree ──► Planner（純視覺規劃）──► Coder
            │             │
       SymPy 硬驗證    結構化解題樹
       （確定性 CAS）  （豐富、可驗證、不受旁白字數限制）
```

### 職責分工（neuro = LLM，symbolic = SymPy）

| 角色 | 工具 | 負責 | 不負責 |
|---|---|---|---|
| **Solver-LLM** | LLM (Opus) | 解題的**敘事/教學邏輯**：分幾步、每步在做什麼、為什麼 | 不負責「算對數字」 |
| **Solver-Verifier** | **SymPy** | 驗證每一步**數值/符號正確性**（積分、求導、解方程、化簡、等式相等） | 不負責教學表達 |
| **Planner** | LLM (Opus/Gemini) | 純視覺規劃：ToT 選隱喻 + Layout + sequence | **不再碰數學**（永遠走 SKIP 分支）|
| **Coder** | LLM (Opus) | 生成 Manim code | 不碰數學（現況不變）|

> **SymPy 是什麼**：Python 的符號數學庫（CAS，類 Mathematica 但開源、本地、零 API 成本）。確定性、不會跳步、不會自信算錯。涵蓋國中~大一（代數、微積分、線代、三角、解方程組）。幾何證明/純文字應用題它幫不上，那些 fallback 回純 LLM 解題樹（標 `verified: false`）。

---

## 3. `solution_tree` Schema（Solver 的輸出 = Planner 的輸入）

```json
{
  "problem_type": "definite_integral",
  "topic_normalized": "Area under f(x)=x^2 on [0,2]",
  "final_answer": "8/3",
  "answer_verified": true,
  "steps": [
    {
      "id": "s1",
      "claim": "Set up the definite integral of x^2 from 0 to 2",
      "math": "\\int_0^2 x^2 \\,dx",
      "justification": "Area under f(x)=x^2 over the interval [0,2]",
      "depends_on": [],
      "key_values": {"lower": 0, "upper": 2, "integrand": "x**2"},
      "verified": true,
      "verify_method": "sympy.integrate"
    },
    {
      "id": "s2",
      "claim": "Apply the power rule to get the antiderivative",
      "math": "\\frac{x^3}{3}\\Big|_0^2",
      "justification": "Antiderivative of x^2 is x^3/3",
      "depends_on": ["s1"],
      "key_values": {"antiderivative": "x**3/3"},
      "verified": true,
      "verify_method": "sympy.diff(roundtrip)"
    },
    {
      "id": "s3",
      "claim": "Evaluate at bounds to get 8/3",
      "math": "\\frac{8}{3} - 0 = \\frac{8}{3}",
      "depends_on": ["s2"],
      "key_values": {"result": "8/3"},
      "verified": true,
      "verify_method": "sympy.integrate"
    }
  ],
  "geometric_data": {
    "points": {},
    "comment": "若題目含幾何，SymPy 算出的精確座標放這（給 Planner 直接用，不必再算）"
  },
  "verification_summary": {
    "total_steps": 3,
    "verified_steps": 3,
    "unverified_step_ids": [],
    "confidence": "high"
  }
}
```

### 欄位設計理由

- **`steps[].verified` + `verify_method`**：這是現在**完全沒有**的解題正確性閘門。`false` 的步驟被明確標記，FinalJudge / 人評可據此扣分或觸發重解。
- **`depends_on`**：解題步驟的 DAG。Planner 據此決定動畫呈現順序、哪些可平行展示。**解題步驟數 ≠ 動畫步驟數**——一個解題步可拆成多個動畫 micro-step（motivation→execution→result），數學完整性不再被 25 字旁白上限綁架。
- **`key_values` / `geometric_data`**：SymPy 算出的精確數值/座標，Planner 直接填進 `constructor_args`，**徹底消除 `templates.py:71-74` 的「Planner 自己算座標」未驗證路徑**。
- **`math`（LaTeX）**：完整數學式，不受旁白字數限制 → 解決「解題步驟不豐富」。

---

## 4. 接入點與資料流（最小侵入）

### 4.1 main.py 改動（共存策略：有外部答案就跳過 Solver）

接在 `AcademicTranslator` 之後、`Planner` 之前（main.py:195 與 234 之間）：

```python
# main.py 既有：
user_topic = translator.translate_to_english(user_input)   # line 195
_solution  = os.environ.get("LLMANIM_SOLUTION", "").strip() or None  # line 235

# ── 新增 Solver 層 ──────────────────────────────────────────────
from agents.solver.solver import Solver
if _solution:
    # eval 模式：已有外部驗證答案 → 跳過 Solver（你的決策，零成本、零行為改動）
    print("📋 [Solver] 外部 solution 已提供 → 跳過 Solver")
    solution_tree = None          # Planner 走既有 LLMANIM_SOLUTION 路徑
else:
    # 互動模式：第一次真的解題
    print("\n🧮 [階段 0.5: Solver] 解題 + SymPy 驗證中...")
    with StageTimer("Solver", llm.session_stats, "time_solver_sec"):
        solution_tree = Solver(llm_client=llm).solve(user_topic)
    # 把驗證過的解題樹序列化成 solution 字串，餵進既有 SKIP 路徑
    _solution = solution_tree_to_solution_str(solution_tree)
# ────────────────────────────────────────────────────────────────
```

**關鍵：對既有架構幾乎零侵入。** Solver 的產物最終以既有的 `_solution` 字串形式餵給 Planner，Planner 100% 走 `templates.py:17-18` 的 SKIP 分支。**Planner system prompt 一個字都不用改**（符合 CLAUDE.md「禁止擅改 Planner prompt」）。

> 進階（第二期）：若要讓 Planner 利用 `depends_on` / `geometric_data` 結構，再考慮擴充 Planner 輸入格式——但那需另行確認，本期不做。

### 4.2 RAG 並行化考量

Solver 是序列前置（解完才能規劃）。但 Solver（LLM+SymPy，~10-20s）可與 RAG 並行——RAG 只需 `user_topic`，不需 solution。建議把 `_rag_future = submit(_rag_task)`（main.py:229）提前到 Solver **之前**提交，讓 RAG ‖ Solver。

---

## 5. Solver 內部設計

```
agents/solver/
├── __init__.py
├── solver.py          # Solver class：orchestrate LLM 解題 + SymPy 驗證
├── verifier.py        # SymPyVerifier：把 step.key_values 丟給 SymPy 實算比對
├── schema.py          # solution_tree 的 JSON Schema + validate
└── templates.py       # SOLVER_SYSTEM_PROMPT
```

### 5.1 解題流程

```python
class Solver:
    def solve(self, topic: str) -> dict:
        # 1. LLM 出結構化解題樹（強制 JSON，沿用 planner 的 _extract_first_json_object）
        raw = self.client.ask(SOLVER_SYSTEM_PROMPT, topic, role="planner")  # 復用 opus 路由
        tree = parse_solution_tree(raw)

        # 2. 逐步 SymPy 驗證
        for step in tree["steps"]:
            ok, method = self.verifier.verify(step)   # 見 5.2
            step["verified"] = ok
            step["verify_method"] = method

        # 3. 驗證最終答案
        tree["answer_verified"] = self.verifier.verify_final(tree)

        # 4. 摘要 + 信心評級
        tree["verification_summary"] = summarize(tree)
        return tree
```

### 5.2 SymPyVerifier 策略（按 problem_type 分派）

| problem_type | SymPy 驗證方式 |
|---|---|
| `definite_integral` / `indefinite_integral` | `sp.integrate(integrand, (x, a, b))` 比對 `final_answer` |
| `derivative` | `sp.diff(f, x)` 比對 |
| `solve_equation` | `sp.solve(eq, x)` 比對根集合 |
| `factor` / `simplify` | `sp.simplify(lhs - rhs) == 0` 驗證等式 |
| `limit` | `sp.limit(f, x, point)` |
| `geometry`（座標）| 用 SymPy 算交點/距離/角度，回填 `geometric_data` |
| `proof` / `word_problem` / 無法解析 | **fallback：`verified=False`，標記人/LLM review**，不阻斷流程 |

**容錯原則**：SymPy parse 失敗（LaTeX→sympy 轉換難）絕不 crash，該步標 `verified: false` 繼續。Solver 永不阻斷 pipeline——最差退化成「純 LLM 解題樹」（=你 AskUserQuestion 裡那個 fallback 選項，但這裡是 per-step fallback，不是整體放棄 SymPy）。

### 5.3 LaTeX → SymPy 的坑（投機，需驗證）

把 LLM 出的 `math`（LaTeX）轉成 SymPy 可算的式子是最大技術風險。對策：
- **不解析 LaTeX**，改要求 LLM 在 `key_values` 裡額外輸出 **Python/SymPy 語法**的純表達式（如 `"integrand": "x**2"`），Verifier 只吃 `key_values`，不碰 `math`（`math` 純粹給人/Planner 看的 LaTeX）。
- SymPy 有 `parse_latex`（需裝 `antlr4`），但脆。優先走 `key_values` 純表達式路線。

---

## 6. 成本與效能

| 項目 | 影響 |
|---|---|
| eval 模式（有外部答案）| **零影響**——跳過 Solver |
| 互動模式 | 多一次 LLM call（Solver-LLM）+ SymPy（本地毫秒級、零成本）|
| SymPy 本身 | 免費、本地、無 API。確定性，不消耗任何 quota |
| 延遲 | Solver 可與 RAG 並行（見 4.2），淨增 ~10-20s（LLM 解題那一 call）|

---

## 7. 對「兩個重點」的直接收益

| 你的重點 | 收益機制 |
|---|---|
| **更豐富專業的解題步驟** | Solver 專職解題，有 `claim`/`justification`/`depends_on`/`key_values` 結構 + LaTeX `math`，**不受 25 字旁白上限壓縮**；SymPy 硬驗證提供正確性保證 |
| **影片規劃架構優化** | Planner 卸下解題+座標計算負擔 → 認知負荷砍半 → ToT/Layout 品質上升；且拿到的是**已驗證座標/數值**，排版不再基於錯誤數學 |
| （附帶）系統第一次真的會解題 | 互動模式不再裸奔，`verified` flag = 史上第一個解題正確性閘門 |

---

## 8. 前置條件 & 待確認

- [ ] **裝 SymPy**：`pip install sympy`（純 Python 依賴，無系統依賴）。確認專案 venv 的 python 在哪（`grep` 時 `python` 不在 PATH）。
- [ ] **Planner 輸入格式**：本期維持「solution_tree → solution 字串 → 既有 SKIP 路徑」，不改 Planner prompt。第二期若要讓 Planner 吃結構化 tree 需另行確認。
- [ ] **role 路由**：Solver-LLM 復用 `role="planner"`（Opus）還是新增 `role="solver"`？建議復用，解題與規劃同屬高階推理。
- [ ] **PlannerLite 共存**：exhibition LITE 路徑（`full_system_lite_runner.py`）是否也接 Solver？解題與美學無關，理論上適用，但 LITE 強調「放寬約束」，可能想保持輕量——待確認。

---

## 9. 實作里程碑（建議分期）

- **M1**：`agents/solver/` 骨架 + `solution_tree` schema + Solver-LLM（先不接 SymPy，純 LLM 出樹）+ main.py 接點（互動模式）。可端到端跑通。
- **M2**：`SymPyVerifier` 接入，按 problem_type 分派，`key_values` 純表達式路線。`verified` flag 上線。
- **M3**：geometric_data 回填 + Planner 利用座標（驗證排版品質提升）。
- **M4**（選配）：solution_tree → 擴充 Planner 結構化輸入（需確認改 Planner prompt）。
