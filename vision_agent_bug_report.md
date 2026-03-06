# Vision Agent Bug Report
**Date**: 2026-03-05
**Project**: LLManim Agent
**Severity**: Critical
**Status**: Root cause confirmed, fix not yet implemented

---

## 一句話摘要

Vision Agent 在 Benchmark MID_02 中對一支**內容完全錯誤**的影片給出了 PASS，導致系統將「Tape Diagram 牛奶與水」的題目輸出為「單位圓 + 正弦波動畫」，且被標記為成功。

---

## 完整失敗鏈條（MID_02 案例）

### 題目
> 一種混合物含有 2 份牛奶與 5 份水。使用帶有標籤的條型圖（Tape Diagram）來視覺化 2:5 的比例。

### 失敗順序（共 10 次 API 呼叫，花費 $0.0198）

| 步驟 | 發生什麼 | 結果 |
|------|---------|------|
| 1 | Planner 規劃正確的 Tape Diagram | ✅ |
| 2 | Coder 初稿含 `\mathrm{}` | Linter 攔截 |
| 3 | Patch 修正後，code 含 `CYAN`（未定義顏色） | Render 失敗 |
| 4 | 修正後的 code 含 `add_updater + become()` | Render timeout（120s） |
| 5 | **Template Override 觸發** → 注入硬編碼的單位圓+正弦波骨架 | 🔴 Root cause |
| 6 | Self-Consistency N=3 投票 → 三份代碼都是正弦波 | 題目已被替換 |
| 7 | Audio sync check 失敗 → R1 escalation | 費用爆炸 |
| 8 | R1 拿到正弦波骨架生成代碼 | 完美的正弦波動畫 |
| 9 | Vision Agent 審查截圖：正弦波流暢無出界 → **PASS** | 🔴 誤判 |
| 10 | 系統標記為成功，歸檔輸出 | 錯誤結果被接受 |

---

## Bug 1：Template Override 是 Topic-Specific 骨架（已修）

### 位置
`agents/orchestrator/refining_loop.py` 第 834~891 行

### 原本代碼
```python
if consecutive_timeouts >= 1:
    template_override = """
[TEMPLATE OVERRIDE ACTIVATED]
...
        theta = ValueTracker(0)
        # --- LEFT: Unit Circle ---
        circle = Circle(radius=2, color=BLUE).move_to(circle_center)
        # --- RIGHT: Sine Graph ---
        axes = Axes(x_range=[0, TWO_PI, np.pi/2], ...)
        sine_curve = axes.plot(lambda x: np.sin(x), ...)
        self.play(Create(circle), Create(axes))
...
"""
```

這是把 HIGH_03（單位圓+正弦波）的完整代碼直接 hardcode 成系統的 Timeout 備用骨架。**任何題目只要 timeout，都會被強制改成正弦波動畫。**

### 已套用的修復
**修復 A（使用者）**：把骨架換成 topic-agnostic 的空骨架：
```python
template_override = """
[TEMPLATE OVERRIDE ACTIVATED]
You MUST use the following safe, linear skeleton. Do NOT use any `always_redraw`,
`add_updater`, or complex `ValueTracker` logic.

class GeneratedScene(Scene):
    def construct(self):
        # 1. Create static elements
        # 2. Build the main diagram step-by-step
        # ... your code here ...
        # 3. Animate changes linearly (no updaters)
        self.wait(1)
"""
```

**修復 B（補充）**：在 Template Override 的 feedback prompt 裡加回 `script_json`：
```python
feedback_for_llm = f"""
{template_override}

═══════════════════════════════════════════════════════════
ORIGINAL TASK — YOU MUST IMPLEMENT THIS, NOT SOMETHING ELSE
═══════════════════════════════════════════════════════════
{script_json}
═══════════════════════════════════════════════════════════
...
"""
```

原本 Template Override 路徑沒有傳入 `script_json`，LLM 不知道要畫什麼，只能靠記憶（或骨架暗示）猜測題目。

---

## Bug 2：Vision Agent 沒有「內容符合度審查」（未修）

### 位置
`agents/utils/vision_agent.py`，`system_prompt`（第 18~99 行）

### 問題描述
Vision Agent 的審查流程分 5 個 Phase，全部都是**畫面品質審查**：

| Phase | 內容 |
|-------|------|
| Phase 1 | Visual Inventory（列出畫面元素） |
| Phase 2 | Well-Formedness（沒有重疊/出界） |
| Phase 3 | Temporal Delta（元素的出現順序） |
| Phase 4 | Defect Classification（OVERLAP/OVERFLOW/MISALIGNED等） |
| Phase 5 | Confidence & Verdict |

**沒有任何一個 Phase 要求 Vision Agent 比對截圖內容與 `script_context` 是否一致。**

### Vision Agent 實際收到的 context
`audit_frame()` 在 `refining_loop.py` 的呼叫：
```python
audit = vision_agent.audit_frame(
    frame_path,
    script_json,           # ← Planner 的完整 JSON 規劃（有題目資訊）
    code_context=current_code,
    detail=_frame_detail,
    spatial_metadata=_spatial_metadata
)
```

`script_json` 裡確實包含 "Tape Diagram", "milk", "water" 等關鍵字。**Vision Agent 收得到題目，但 system prompt 沒有叫它去比對。**

### MID_02 的 Vision 實際輸出
```json
{
  "visual_rationale": "The frames depict a dynamic scene where a unit circle and sine graph
   are being animated...",
  "confidence_score": 5,
  "verdict": "PASS",
  "overall_critique": "All checks passed, with no defects identified.",
  "defects": []
}
```

Vision Agent 看到漂亮的正弦波動畫（無重疊、無出界、流暢）→ confidence_score=5 → PASS。
完全沒有注意到這跟題目要求的 Tape Diagram 毫無關係。

---

## 建議修復方案（Bug 2）

在 Vision Agent 的 `system_prompt` 裡加入 **Phase 0: Topic Conformance Check**，作為最高優先級的前置檢查：

```
### Phase 0: Topic Conformance Check (HIGHEST PRIORITY)
Before any spatial analysis, verify that the animation content matches the task description.

Steps:
1. Extract the key visual elements described in `script_context`:
   - What type of diagram/chart is expected? (e.g., Tape Diagram, number line, axes, pie chart)
   - What are the main labeled objects? (e.g., "Milk", "Water", specific equations)
2. Check if these elements are actually visible in the frames.
3. If the frames show a COMPLETELY DIFFERENT type of visualization than described:
   - Set verdict = "FAIL" immediately
   - Add a defect with code "WRONG_CONTENT", severity "Critical"
   - Skip Phases 1-4 (spatial analysis is irrelevant if content is wrong)

Example triggers for WRONG_CONTENT:
- script_context describes a "Tape Diagram" but frames show a sine wave / unit circle
- script_context describes "number line" but frames show a matrix
- script_context describes "pie chart" but frames show bar charts with unrelated labels
```

---

## 影響範圍

這兩個 bug 的組合形成一個**完美的誤判路徑**：

```
任何題目 timeout
    → Template Override（任意骨架） + 沒有 script_json
    → LLM 產出骨架指示的動畫（或亂猜）
    → Vision Agent 只看畫面品質
    → 只要畫面漂亮就 PASS
    → 系統以為成功，歸檔輸出
```

修了 Bug 1（骨架 + 加回 script_json）後，LLM 大概率會生出正確內容，但**沒有 Bug 2 的保護，這個誤判路徑依然存在**——只要 LLM 生出任何「漂亮但錯誤」的動畫，Vision 仍然會 PASS。

---

## 討論問題

1. **Phase 0 的觸發門檻怎麼設？** 完全不同的視覺化類型（bar vs sine wave）容易判斷，但「Tape Diagram 畫成普通矩形」這種語義接近的情況怎麼處理？

2. **`script_context` 對 Vision 來說夠用嗎？** 目前傳入的是完整 `script_json`（含 layout_plan, sequence），資訊量很大。是否應該只傳「題目摘要（1-2句）+ 預期的主要視覺元素列表」，避免 Vision LLM 被大量 JSON 分散注意力？

3. **Phase 0 失敗後要做什麼？** 直接 FAIL 讓 refining loop 觸發完整重寫？還是需要一個新的 error code（`WRONG_CONTENT`）觸發特殊的修復路徑？

4. **cost 影響**：Phase 0 增加了 Vision 的推理複雜度，對 gpt-4o-mini 的 completion tokens 影響有多大？目前每次 Vision audit 約 150~200 completion tokens，加了 Phase 0 後可能增加到 300~400。

---

## 相關檔案

| 檔案 | 關聯 |
|------|------|
| `agents/orchestrator/refining_loop.py:829~891` | Template Override 邏輯（Bug 1，已修） |
| `agents/utils/vision_agent.py:18~99` | Vision Agent system_prompt（Bug 2，未修） |
| `agents/utils/vision_agent.py:292~395` | `audit_frame()` 呼叫介面 |
| `runs/20260305_020347/MID_02/thought_trace.log` | 完整失敗記錄 |