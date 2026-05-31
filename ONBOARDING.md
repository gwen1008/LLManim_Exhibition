# 組員 Onboarding — LLManim_Agent Vision 系統優化

> **目標讀者**：剛加入的學生 / 新手工程師
> **預期時間**：Phase 0 半天 + Phase 1 兩天 + Phase 2-4 持續
> **任務一句話**：讓 VisionAgent 抓 bug 更準（precision/recall 同時上升）

---

## 目錄

1. [這個專案在做什麼](#1-這個專案在做什麼)
2. [你要做的事](#2-你要做的事)
3. [Setup（環境安裝）](#3-setup環境安裝)
4. [跑第一題 smoke test](#4-跑第一題-smoke-test)
5. [架構與 Vision 系統詳解](#5-架構與-vision-系統詳解)
6. [量測工具：`cost_report.json`](#6-量測工具cost_reportjson)
7. [建 labeled set 流程](#65-建-labeled-set-流程)
8. [Vision eval harness](#66-vision-eval-harness)
9. [優化方向（5 條，順序執行）](#7-優化方向5-條順序執行)
10. [禁區（絕對不要動）](#8-禁區絕對不要動)
11. [Quota Budget](#quota-budget)
12. [Git 工作流](#10-git-工作流)
13. [常見問題與 Debug](#11-常見問題與-debug)
14. [Baseline 數字](#12-baseline-數字)
15. [連絡與資源](#13-連絡與資源)

---

## 1. 這個專案在做什麼

LLManim_Agent 是一個 **AI 驅動的數學動畫生成器**。輸入一個數學題目，它會自動產出一支配音的 Manim 動畫，展示解題過程。

整個流程是 **多 agent 編排** 系統：

```
題目 → Planner → Coder → Render(Manim) → Vision QA(Opus) → FinalJudge → mp4
                                ↑          ↓ FAIL 就回去 Coder 修
                                └──────────┘  最多 5 輪
```

**Vision QA 在這流程裡是「看門人」**——每輪 Coder 生成 code → render 成 mp4 → 抽 4-frame grid → 餵給 VisionAgent → 判 PASS/FAIL → FAIL 就把 defect 描述回灌給 Coder 修。VisionAgent 看得準不準，直接決定整個 pipeline 的修復品質。

**你的工作就是讓 VisionAgent 抓 bug 更準**。

---

## 2. 你要做的事

**讓 `agents/utils/vision_agent.py` 的 `audit_frame()` 在自建 labeled set 上 F1 ≥ baseline + 10pp，同時 30 題完整 pipeline FJ verdict 不退化。**

### 怎麼算成功？

1. **建 50 部 labeled set**（從 `runs/` 撈 ELEM/MID/HIGH 系列，自己標 PASS/FAIL + defect code）
2. **跑 Opus baseline**（方向 1 接好之後，作為所有後續方向的對照基準）
3. **改 prompt 迭代**（方向 1 → 2 → 3 → 4 → 5 順序）
4. **每次 PR 附 before/after F1/precision/recall**
5. **交付前跑 30 題 FJ verify**（要先跟 owner approve quota）

### 成功標準

- Labeled set F1 ≥ baseline + 10pp
- Per-defect-code recall：新增 code recall ≥ 50%，原有 code 不退
- 30 題 FJ verdict PASS 率 **不下降**
- borderline 比例 < 20%（schema 夠清楚）

### 不算成功的例子

- 「我把 prompt 改得 recall 從 60% → 90% 但 precision 從 80% → 30%」→ F1 算下來反而退 → ❌
- 「我覺得這樣 prompt 比較好」→ 沒附 labeled set 數字 → ❌
- 「我把 `vision_conf_accept` 從 4 改成 3 所以 recall 大漲」→ 把閾值放寬不算優化，是作弊 → ❌

---

## 3. Setup（環境安裝）

### 3.1 系統前置

```bash
python --version          # 3.10+，建議 3.11
brew install ffmpeg       # macOS；Linux 用 apt
ffmpeg -version
```

Windows 用 WSL2。

### 3.2 clone + 切分支

```bash
git clone git@github.com:childe0905/LLManim_Agent.git
cd LLManim_Agent
git checkout vision/prompt-eng   # ← 你的工作分支
```

### 3.3 Python 環境

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Manim 系統依賴看 [Manim 官方安裝指南](https://docs.manim.community/en/stable/installation.html)。

### 3.4 環境變數 `.env`

```bash
cp .env.example .env
```

**你 95% 時間在做的事 = 跑 vision eval harness**（餵 grid jpg → Opus → 比對 label），完全不碰 Planner/Coder/RAG/Audio/Render，所以環境可以最簡。

**日常開發必填**：
- `DISABLE_RAG=1` — vision eval 不需要 Weaviate，直接關掉省麻煩
- Claude Code CLI 登入（見 §3.5）— Opus vision call 走這個

**Vision 設定**：
- `VISION_BACKEND=opus` — 方向 1 接好後設這個，整個 project 都用 Opus

**只有兩個時機需要完整 pipeline 環境**：
1. §4 ELEM_01 smoke test — 確認環境裝對了，跑一次
2. §Phase 4 30 題 FJ verify — 交付前驗收，跑一次

**完整 pipeline 額外要**（跟 owner 拿）：
- `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION` — TTS

**不需要**：
- ❌ `OPENAI_API_KEY` — 你不跑 GPT-4o，全程 Opus
- ❌ `GROQ_API_KEY` / `DEEPSEEK_API_KEY` — 別的 agent 用的
- ❌ Weaviate — DISABLE_RAG=1

### 3.5 Claude Code CLI（給 Opus vision call 用）

```bash
# 安裝 Claude CLI（如果還沒）
# 參考：https://docs.claude.com/en/docs/claude-code/quickstart

# 你的帳號選擇（跟 owner 確認）：
# 選項 A：你自己的 Claude 帳號（最簡單，扣你 quota）
# 選項 B：claudealt 系統帳號（owner 提供，方向 1 用 Opus 時建議用這個）

claude login
which claude
# 路徑不是 /usr/local/bin/claude 就把實際路徑寫進 .env CLAUDE_BIN
```

---

## 4. 跑第一題 smoke test

**用 `ELEM_01`（披薩 1/2=2/4，教授 15 題之一）**：

```bash
source .venv/bin/activate

# 跑單題 smoke test
python run_evaluation.py --case ELEM_01 \
    --sample evaluation/test_cases.json
```

### 預期輸出

```
🧠 [Planner] 規劃視覺腳本...
🔍 [RAG] 檢索相似範例...
🎙️ [Audio] 生成語音...
👨‍💻 [Coder] 生成動畫程式碼...
👁️ [Vision QA] 審查影格...
🏛️ [FinalJudge] 兩階段評分...
✅ 完成！
```

### 完跑後**必做**：看 vision audit log

```bash
# 找最新一個 ELEM_01 run
ls -t runs/ | head -1
cat runs/<ts>/ELEM_01/vision_audit_log.json | python -m json.tool
```

你要看懂的欄位：

| 欄位 | 意思 |
|---|---|
| `verdict` | `PASS` / `FAIL` / `ERROR` — 整體判定 |
| `confidence_score` | 1-5，模型對自己判定的信心 |
| `defects[]` | 抓到的 bug list（含 code/severity/frame） |
| `overall_critique` | 一句話技術摘要 |

**這個 json 就是你後面所有迭代的對照基準**。改 prompt 後同一支影片再跑一次，比較 verdict / defects 變化。

### 如果跑失敗

跳到 §11 找錯誤訊息。

---

## 5. 架構與 Vision 系統詳解

### 5.1 進入點

| 檔案 | 用途 | 你需要看嗎 |
|---|---|---|
| `main.py` | 主編排 | ⚠️ 讀就好，不准改 |
| `run_evaluation.py` | 批次跑 benchmark | ✅ 跑 baseline 用 |
| `agents/utils/vision_agent.py` | **VisionAgent 本體** | ✅ **你的主戰場** |
| `agents/core/llm_client.py` | LLM provider 統一介面 | ⚠️ 只能動 `ask_vision()` line 436-495 |
| `agents/utils/final_judge.py` | FJ 評分（已用 Opus） | ✅ 讀（Opus 串接 reference），❌ 不准改 |

### 5.2 Vision 模組地圖

```
agents/
├── utils/
│   ├── vision_agent.py     ← 你的主戰場
│   └── final_judge.py      ← Opus 串接 reference (read-only)
├── core/
│   ├── llm_client.py       ← ask_vision() L436-495 可動，其他不准
│   └── pipeline_config.py  ← vision_conf_accept / vision_conf_soft_fail 可動
└── orchestrator/
    └── refining_loop.py    ← Vision 呼叫點 L1124/1188/1196 (read-only)
```

### 5.3 Vision QA 在 pipeline 的位置

```
RefiningLoop（最多 5 輪）：
  ┌──────────────────────────────────┐
  │ [1] Lint (zero-cost)              │
  │ [2] Render (Manim → mp4)          │
  │ [3] ffmpeg 抽 4-frame 2×2 grid    │ ← refining_loop.py:1030-1093
  │ [4] VisionAgent.audit_frame(grid) │ ← refining_loop.py:1124
  │     → verdict PASS → break        │
  │     → verdict FAIL → reflex prompt 給 Coder 修
  └──────────────────────────────────┘
```

### 5.4 VisionAgent 內部：CoVT 5-phase

`vision_agent.py:18-124` 的 system_prompt 採用 **Chain-of-Visual-Thought (CoVT)** 框架，強制模型按 5 階段推理：

| Phase | 做什麼 | 失敗代碼 |
|---|---|---|
| **Phase 0** | Topic Conformance（內容對不對） | `WRONG_CONTENT` |
| **Phase 0.5** | Conceptual Fidelity（視覺隱喻像不像） | `WRONG_METAPHOR` |
| **Phase 1** | Visual Inventory（scene graph） | — |
| **Phase 2** | Well-Formedness（負空間規則） | `OVERLAP` `OVERFLOW` `MISALIGNED` `CLUTTER` |
| **Phase 3** | Temporal Delta Analysis（影格間變化） | `TOO_FAST` |
| **Phase 4** | Defect Classification | （用上面 codes） |
| **Phase 5** | Confidence & Verdict | confidence 1-5 / PASS|FAIL |

**為什麼這樣設計**：直接問 LLM「這影片有 bug 嗎」會得到「感覺有點怪」這種不可用答案。強制 5-phase 讓模型先建 scene graph 再判定，準確度差異很大。**改 prompt 時要保留這個骨架**，動的是各 phase 內的規則細節。

### 5.5 兩條 Vision Code Path（**你只動上面那條**）

| | RefiningLoop VisionAgent | FJ Phase 2 |
|---|---|---|
| 檔案 | `vision_agent.py` | `final_judge.py:646-786` |
| 入口 | `llm.ask_vision()` | `_call_claude_code()` + Read tool |
| 預設 model | GPT-4o（`VISION_MODEL=openai/gpt-4o`）| Opus（`FJ_VISION_BACKEND=opus`）|
| 路徑 | OpenAI / OpenRouter API 直連 | Claude Code CLI subprocess + 本地 jpg |
| **你的範圍** | ✅ **這條** | ❌ read-only |

**重點**：兩條 code path **完全不共用**。FJ 已經切 Opus 了，你的工作（方向 1）是把 RefiningLoop VisionAgent **也接 Opus backend**——但**直接在 `ask_vision()` 內加 if-else 分支，不要抽公共 helper**（避免動到 FJ）。

### 5.6 `audit_frame()` vs `audit_video()`

`vision_agent.py` 有兩個 entry：

| | `audit_frame()` | `audit_video()` |
|---|---|---|
| 行數 | L339 | L449 |
| 輸入 | grid jpg path | mp4 path |
| Grid | 4-frame 2×2 | 8-frame |
| **prod 使用** | ✅ `refining_loop.py:1124/1188/1196` | ❌ 沒用到 |
| **你 eval 用** | ✅ harness 跟它對焦 | ⚠️ 不要用 |

**Signature（已驗證）**：
```python
audit_frame(self, image_path, script_context, code_context=None,
            detail="low", spatial_metadata=None, telemetry_context=None,
            num_passes=1)
```

`script_context` 必填，如果 labeled video 沒對應 planner_output.json，傳 `{}` degraded 模式。

---

## 6. 量測工具：`cost_report.json`

每次跑完 `stable_outputs/cost_report.json` 會有：

```json
{
  "time_vision_sec": 9.5,
  "vision_per_iter_sec": [3.1, 3.4, 3.0],
  "time_final_judge_sec": 8.2,
  "final_judge": {
    "verdict": "PASS",
    "weighted_total": 87.5
  },
  "calls": [
    {"model": "...", "elapsed": ...}
  ]
}
```

| 欄位 | 你怎麼用 |
|---|---|
| `time_vision_sec` | Vision 累計耗時，切 Opus 後預期 +30-50% |
| `vision_per_iter_sec` | 每輪 vision 耗時 list，看有沒有單輪暴衝 |
| `final_judge.verdict` | **30 題 verify 的核心指標**，不能退 |

---

## 6.5 建 labeled set 流程

### Step 1：撈素材（**限定 ELEM/MID/HIGH，排除 kb150 + benchmark_set**）

```bash
# 列出所有 ELEM/MID/HIGH 題目資料夾且有 video.mp4 的
find runs/ -type d -regextype posix-extended \
    -regex '.*/(ELEM|MID|HIGH)_[0-9]+$' \
  | while read d; do [ -f "$d/video.mp4" ] && echo "$d"; done > /tmp/candidates.txt

wc -l /tmp/candidates.txt   # 應該 ~1000+ 行
```

**素材池**：1227 個資料夾 / 5368 mp4 / 136 個 session。

**不要碰**：
- ❌ `runs/<session>/Q*/`（kb150 系列）
- ❌ `runs/merged_q01_q100/`（kb150）
- ❌ `evaluation/benchmark_set/Q024-Q148/`（教授 150 題 subset）
- ❌ `evaluation/kb150_full_cases.json`

挑 50 部，**多樣性原則**：
- 同題不同 session/coder 版本可重複入選（例：5 個 ELEM_01 來自不同 run）
- 涵蓋三難度（建議 20 ELEM / 20 MID / 10 HIGH）
- 含 PASS / FAIL / borderline
- 涵蓋不同 coder 版本（看 commit 日期）

### Step 2：抽 4-frame 2×2 grid（跟 prod 一致）

規格：4 frame at 10/40/70/95%，2×2 layout，每 tile 640×360 jpg。

ffmpeg skeleton（包成 `evaluation/build_grids.py` 批次跑）：

```bash
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 video.mp4)
T1=$(echo "$D * 0.10" | bc); T2=$(echo "$D * 0.40" | bc)
T3=$(echo "$D * 0.70" | bc); T4=$(echo "$D * 0.95" | bc)

ffmpeg -y \
  -ss $T1 -i video.mp4 -ss $T2 -i video.mp4 \
  -ss $T3 -i video.mp4 -ss $T4 -i video.mp4 \
  -filter_complex "\
    [0:v]scale=640:360,setsar=1[a];\
    [1:v]scale=640:360,setsar=1[b];\
    [2:v]scale=640:360,setsar=1[c];\
    [3:v]scale=640:360,setsar=1[d];\
    [a][b]hstack[top];[c][d]hstack[bot];[top][bot]vstack" \
  -frames:v 1 -q:v 3 grid.jpg
```

### Step 3：標 label

邊看 mp4 邊填 schema，存 `evaluation/vision_labels/labels.json`：

```json
{
  "ELEM_01_run20260421_101329": {
    "video_path": "runs/20260421_101329/ELEM_01/video.mp4",
    "code_path": "runs/20260421_101329/ELEM_01/code.py",
    "grid_path": "evaluation/vision_labels/grids/ELEM_01_run20260421_101329.jpg",
    "script_context_path": "runs/20260421_101329/ELEM_01/planner_output.json",
    "human_verdict": "FAIL",
    "real_defects": [
      {"code": "SUBTITLE_OFFSCREEN", "evidence": "0:08 字幕超出畫面右邊"}
    ],
    "false_alarm_risk": ["LOW_CONTRAST"],
    "labeler": "<name>",
    "labeled_at": "2026-05-XX",
    "borderline": false
  }
}
```

**Defect code 提示**（現有 7 個 + 你可能要新增的）：

現有：`WRONG_CONTENT` `WRONG_METAPHOR` `OVERLAP` `OVERFLOW` `MISALIGNED` `CLUTTER` `TOO_FAST`
建議新增：`SUBTITLE_OFFSCREEN` `SUBTITLE_OVERLAP` `LATEX_RENDER_FAIL` `TICK_MISALIGN` `STROKE_TOO_THIN`

`false_alarm_risk` 欄位：標「VisionAgent 容易誤報但實際 OK」的 code（給方向 4 用）。

建議用 VS Code split view 左 mp4 右 json。

### Step 4：品質檢查

- 每題隔一天 review 第二次，不一致 → `borderline: true`
- borderline 比例必須 < 20%，否則 schema 不夠清楚要 refactor
- 抽 5 題請 owner double-label，比對 inter-rater agreement

### Step 5：commit

```bash
# .gitignore 已忽略 grids/，labels.json 要 commit
git add evaluation/vision_labels/labels.json
git commit -m "vision(labels): initial 50-case labeled set"
```

---

## 6.6 Vision eval harness

`evaluation/run_vision_eval.py`（你自己寫，skeleton 如下）：

```python
import json, os
from collections import defaultdict
from datetime import date
from pathlib import Path
from agents.utils.vision_agent import VisionAgent

def run_eval(labels_path: str, output_path: str, backend: str = "opus"):
    os.environ["VISION_BACKEND"] = backend
    labels = json.loads(Path(labels_path).read_text())
    agent = VisionAgent()
    results = {}

    for case_id, label in labels.items():
        if label.get("borderline"):
            continue

        ctx_path = label.get("script_context_path")
        script_context = (
            json.loads(Path(ctx_path).read_text())
            if ctx_path and Path(ctx_path).exists()
            else {}
        )

        pred = agent.audit_frame(
            image_path=label["grid_path"],
            script_context=script_context,
            detail="low",
        )
        results[case_id] = {
            "human": label["human_verdict"],
            "pred": pred.get("verdict", "ERROR"),
            "pred_defects": [d["code"] for d in pred.get("defects", [])],
            "real_defects": [d["code"] for d in label["real_defects"]],
        }

    # === Overall confusion matrix ===
    tp = sum(1 for r in results.values() if r["human"] == "FAIL" and r["pred"] == "FAIL")
    fp = sum(1 for r in results.values() if r["human"] == "PASS" and r["pred"] == "FAIL")
    fn = sum(1 for r in results.values() if r["human"] == "FAIL" and r["pred"] == "PASS")
    tn = sum(1 for r in results.values() if r["human"] == "PASS" and r["pred"] == "PASS")
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0

    # === Per-defect-code recall ===
    code_stats = defaultdict(lambda: {"human_count": 0, "pred_hit": 0, "pred_only": 0})
    for r in results.values():
        real_set, pred_set = set(r["real_defects"]), set(r["pred_defects"])
        for c in real_set:
            code_stats[c]["human_count"] += 1
            if c in pred_set:
                code_stats[c]["pred_hit"] += 1
        for c in pred_set - real_set:
            code_stats[c]["pred_only"] += 1

    per_code = {
        c: {
            "recall": s["pred_hit"] / s["human_count"] if s["human_count"] else None,
            "human_count": s["human_count"],
            "false_positive_count": s["pred_only"],
        }
        for c, s in code_stats.items()
    }

    Path(output_path).write_text(json.dumps({
        "backend": backend,
        "overall": {
            "precision": precision, "recall": recall, "f1": f1,
            "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        },
        "per_defect_code": per_code,
        "borderline_excluded": sum(1 for l in labels.values() if l.get("borderline")),
        "total_evaluated": len(results),
        "raw": results,
    }, indent=2, ensure_ascii=False))
    print(f"F1={f1:.3f}  P={precision:.3f}  R={recall:.3f}")
    for c, s in sorted(per_code.items()):
        r = s["recall"]
        rs = f"{r:.2f}" if r is not None else "N/A"
        print(f"  {c}: recall={rs}  n={s['human_count']}  FP={s['false_positive_count']}")

if __name__ == "__main__":
    run_eval(
        "evaluation/vision_labels/labels.json",
        f"evaluation/vision_labels/baseline_{date.today()}_opus.json",
        backend="opus",
    )
```

跑：`python evaluation/run_vision_eval.py`

---

## 7. 優化方向（5 條，**順序執行**）

**順序鐵則**：方向 1 → 2 → 3 → 4 → 5。**每個 PR merge 完才能開下一個**，避免 system_prompt 同段 git conflict。

### 🥇 方向 1：VisionAgent 切換到 Opus（**強制第一步**）

**動機**：FJ Phase 2 已用 Opus，證明它在細粒度視覺 QA 比 GPT-4o-mini/4o 強。RefiningLoop VisionAgent 還是 GPT-4o，要一致化。

**怎麼做**：
- 在 `llm_client.py:436` `ask_vision()` 內**直接加 backend 分支**
- 當 `os.getenv("VISION_BACKEND") == "opus"` 時走 `_call_claude_code` + Read tool 讀本地 jpg
- **參考** `final_judge.py:730-786` 寫法（read-only reference，不要改 FJ）
- **不抽公共 helper**（允許代碼重複換邊界清晰）

**約束**：
- 修改範圍**只限 `llm_client.py:436-495`**
- commit 前用 `git diff agents/core/llm_client.py` 確認沒動到其他 method
- 改完跑 **ELEM_01** smoke test 確認 Planner/Coder/FJ/Vision **四條 LLM call path 都沒壞**

**驗證**：跑 Opus baseline（`VISION_BACKEND=opus`），記錄 F1/precision/recall 作為**所有後續方向的對照基準**

**檔案**：`agents/core/llm_client.py:436-495`、`.env`

**難度**：⭐⭐⭐

---

### 🥈 方向 2：Few-shot example injection

**動機**：目前 prompt zero-shot，加 2-3 個 labeled example 通常 F1 跳一階。

**怎麼做**：
- 從 labeled set 挑 2-3 個典型例子（PASS / FAIL / borderline）
- **用純文字描述加進 prompt，不塞 base64 image**（避免 token 爆炸）
- 範例格式：
  ```
  EXAMPLE FAIL: A frame showing two equations stacked vertically, where the
  bottom equation (y = 2x+1) extends beyond the right canvas edge.
  → defect: OVERFLOW, severity: Critical
  ```
- **few-shot 例子必須從 hold-out test set 排除**（你 50 部裡留 10 部當 hold-out）

**驗證**：hold-out F1（用沒進 prompt 的 10 部）

**檔案**：`agents/utils/vision_agent.py:18-124` system_prompt

**難度**：⭐⭐

---

### 🥉 方向 3：Defect code 重新設計

**動機**：現有 7 個 code 粒度不一致，缺常見 bug 類別。

**怎麼做**：
- 從 labeled set 統計 bug 分佈（你 `real_defects` 欄位的 code 出現次數）
- 新增建議 code：
  - `SUBTITLE_OFFSCREEN` — 字幕切到畫面外
  - `SUBTITLE_OVERLAP` — 字幕跟其他元素重疊
  - `LATEX_RENDER_FAIL` — LaTeX 渲染失敗變原始字串
  - `TICK_MISALIGN` — 座標軸刻度跟標籤不對齊
  - `STROKE_TOO_THIN` — 線太細看不清
- 改 system_prompt **Phase 4 defect classification** 段
- 注意：新增 code 要在 prompt 給明確定義 + 觸發條件

**驗證**：新 code recall（baseline 0% → ≥50%）+ 原有 code recall 不退

**檔案**：`agents/utils/vision_agent.py:18-124`

**難度**：⭐⭐

---

### 方向 4：Negative example injection（防誤報）

**動機**：LLM 對 "DO NOT FLAG" rule 敏感度低，對 negative example 敏感度高。

**怎麼做**：
- 從 labeled set 找出 `false_alarm_risk` 標記的 case
- 純文字描述加進 prompt 當 "DO NOT FLAG" 範例：
  ```
  DO NOT FLAG: A frame with white text on black background should NEVER be
  flagged LOW_CONTRAST (Manim default theme passes WCAG AA).
  ```

**驗證**：precision 上升（FP 降低）+ recall 不退

**檔案**：`agents/utils/vision_agent.py:18-124`

**難度**：⭐⭐

---

### 方向 5：Chain-of-Thought 順序重排

**動機**：學術 CoT 研究強烈支持「先推理再下結論」。現在 prompt schema 是 `confidence_score → verdict → defects`（結論在前），改成 `defects → verdict`（推理→結論）通常 F1 跳一階。

**怎麼做**：
- 改 `vision_agent.py:96-115` JSON OUTPUT FORMAT 段
- schema 順序從：
  ```
  visual_rationale, temporal_analysis, confidence_score, verdict, overall_critique, defects
  ```
  改成：
  ```
  visual_rationale, temporal_analysis, defects, overall_critique, confidence_score, verdict
  ```
- prompt 明確指示「**先列 defects，再根據 defects 決定 verdict**」

**約束**：
- JSON 物件理論上鍵值無序，但 prompt-induced ordering 會影響 LLM 輸出穩定性
- 改完先 grep `verdict.*confidence` 確認沒有 parser 依賴順序
- 跑 5 題 dry-run 看 output JSON 結構穩定

**驗證**：labeled set F1 對比 baseline；特別看 borderline case 的 verdict 一致性

**檔案**：`agents/utils/vision_agent.py:96-115`（OUTPUT FORMAT 段）

**難度**：⭐⭐

---

**不在你範圍內**（動了會被 reject）：
- frame extraction 改良（要動 `refining_loop.py`）
- dual-model agreement（要動 FJ）
- Multi-pass self-consistency（要動 `audit_frame` 邏輯，留給下一位組員的 track）
- confidence calibration（要動 `pipeline_config.py` 多個欄位）
- Defect bounding box localization（影響 Coder 修復品質，跨 vision/coder 邊界）

---

## 8. 禁區（絕對不要動）

### 可以動（PR 必附 labeled set before/after + 30 題 FJ before/after）

- ✅ `agents/utils/vision_agent.py` 全檔
- ✅ `agents/core/llm_client.py:436-495` `ask_vision()`（**僅此 method**，不可動 `ask` / `ask_with_tools` / `_call_claude_code` / `_update_stats`）
- ✅ `.env` 的 `VISION_MODEL` / 新增 `VISION_BACKEND`
- ✅ `agents/core/pipeline_config.py` 的 `vision_conf_accept` / `vision_conf_soft_fail`

### 動 `llm_client.py` 的額外規則

每個 PR 必須附：
- `git diff agents/core/llm_client.py` 確認只在 line 436-495 範圍
- ELEM_01 smoke test 通過證明（Planner/Coder/FJ/Vision 4 條 path 全綠）

### 仍然鎖死

- ❌ `manimator/` 第三方
- ❌ Planner / Coder / Audio / RAG 任何檔案
- ❌ `RefiningLoop`（包含 frame extraction `refining_loop.py:1030-1093`）
- ❌ `max_refine_attempts=5`、`visual_attempts_limit=3`、`LINTER_RETRY_BUDGET=3` 等 budget
- ❌ Audio + RAG + Coder 平行架構
- ❌ `pre_render_patch()`
- ❌ FinalJudge / BenchmarkJudge **內部行為**（可 read-only 參考，不可 modify）

### 行為禁區

- ❌ **動 `vision_conf_accept` 閾值就為了讓數字好看** — PR description 必須說明依據
- ❌ **把不確定的 label 標 borderline 來提高 F1** — borderline 比例 > 20% 整份 baseline 作廢

### 不要 commit 的檔案

- ❌ `runs/` / `stable_outputs/` — 執行輸出
- ❌ `.env` — API key
- ❌ `evaluation/vision_labels/grids/*.jpg` — 已 gitignore
- ❌ `evaluation/vision_labels/baseline_*.json` 大檔（看大小，<1MB OK）

---

## Quota Budget

組員 Opus 消耗預估：

| 階段 | Opus call 數 | 累計 |
|---|---|---|
| Opus baseline 跑一次（50 部）| 50 | 50 |
| 每輪 prompt 迭代 baseline 重跑 | 50 × 5 輪 = 250 | 300 |
| 30 題 FJ verify（每題 RefiningLoop 最壞 5 輪 × 1 vision + FJ Phase 2 ~3 pass = 8）| 30 × 8 = 240 | **540** |
| **總計（單一組員整個 project）** | | **~540 次** |

**重要假設**：
- RefiningLoop `max_refine_attempts=5`，每輪一次 vision call，**最壞** 5 次/題（PASS 早期 break 通常 1-2 次）
- FJ Phase 2 多 pass swap 評分，保守抓 3
- 實際 quota 可能 ±30%，**跑 30 題 verify 前先抓 5 題 dry-run** 校準

**Claude Max 訂閱限制**：跟 owner 確認實際 5hr reset cap 與 claudealt 帳號額度。**30 題 FJ verify 建議分 2-3 個 reset window 跑**避免撞 cap。

**回退路徑**：quota 用完或 Opus 出問題 → `.env` 改 `VISION_BACKEND=gpt4o` 回退到 GPT-4o（**需要先跟 owner 拿 `OPENAI_API_KEY`**），所有 prompt 改動仍然 work（prompt 跟 backend 解耦）。

---

## 9. 如果你用 AI 工具寫 code

學生用 Claude Code / Cursor / Copilot 很正常，但要遵守：

### 必做

1. 把 `CLAUDE.md` 整個丟給 AI 當 system context
2. 跟 AI 強調禁區（§8 整段貼給它）
3. 每次 AI 改完，你自己 review 一遍才能 commit
4. 跑 syntax check：
   ```bash
   python -c "import ast; ast.parse(open('agents/utils/vision_agent.py').read())"
   ```
5. 跑單題 smoke test 確認沒爛掉

### 不要做

- ❌ 讓 AI 自動 `git push` — pre-push hook 會擋
- ❌ 讓 AI 自動跑 30 題 verify — 先跟 owner approve quota
- ❌ 盲信 AI 的「我已經測過」 — AI 沒真的跑你的環境
- ❌ AI 一次改超過 vision_agent.py + llm_client.py 兩個檔 — 多了會混進 bug

### 推薦的 AI 用法

```
Good：「我要實作方向 1（Opus backend）。讀 agents/core/llm_client.py
       的 ask_vision() L436-495，跟 agents/utils/final_judge.py:730-786 的
       Opus 呼叫方式對比，加 if-else 分支。只動 ask_vision，不要動 FJ。」

Bad：「幫我優化 vision。」
```

---

## 10. Git 工作流

### 你的分支：`vision/prompt-eng`

```bash
git branch --show-current   # 應該是 vision/prompt-eng
git pull origin vision/prompt-eng
```

### Commit 規範

```bash
git add agents/utils/vision_agent.py
git commit -m "vision(prompt): add SUBTITLE_OFFSCREEN defect code

- Phase 4 新增 SUBTITLE_OFFSCREEN 定義 + 觸發條件
- Labeled set 統計顯示 12/50 題有此 bug，現有 code 全漏

Before: SUBTITLE_OFFSCREEN recall=0%, F1=0.62
After:  SUBTITLE_OFFSCREEN recall=58%, F1=0.71 (+9pp)
30q FJ: PASS=27/30 → 28/30 (不退化)"
```

**訊息格式**：
- 標題 `vision(<area>): <一句話>`（area = backend / prompt / harness / labels）
- 內文：改了什麼 + 為什麼 + before/after 數字

### PR 規範

```bash
git push origin vision/prompt-eng
# 在 GitHub 開 PR：base = main, compare = vision/prompt-eng
```

PR description 模板：

```markdown
## 做了什麼
（一段話描述）

## 為什麼這樣做
（解釋思路 + 為何選這方向）

## Labeled Set Before/After

跑 `python evaluation/run_vision_eval.py`：

| Metric | Before | After | Δ |
|---|---|---|---|
| Overall F1 | 0.62 | 0.71 | **+9pp** |
| Precision | 0.78 | 0.75 | -3pp |
| Recall | 0.51 | 0.67 | **+16pp** |

Per-defect-code recall：
| Code | Before | After |
|---|---|---|
| OVERLAP | 0.80 | 0.82 |
| SUBTITLE_OFFSCREEN | 0.00 | 0.58 |
| ... | ... | ... |

borderline 比例：8/50 = 16% ✅

## 30 題 FJ Verify

跑前 quota approve：✅ owner approved on 2026-05-XX

| | Before | After |
|---|---|---|
| PASS / 30 | 27 (90%) | 28 (93%) |

## 風險 / 注意事項

## 測試方式
- `python evaluation/run_vision_eval.py`
- `python run_evaluation.py --case ELEM_01`
```

### 禁止

- ❌ `git push --force` — 洗別人 commit
- ❌ 直接 push 到 `main` — 走 PR
- ❌ `git commit -a` — 容易誤加檔案
- ❌ `git push --no-verify` — 跳過 hook 有理由

---

## 11. 常見問題與 Debug

### Q1: `pip install -r requirements.txt` 失敗

macOS：
```bash
brew install py3cairo ffmpeg
brew install --cask mactex-no-gui   # LaTeX 渲染
```

### Q2: 跑 ELEM_01 卡在 Coder 不動

最常見：**Claude CLI 沒登入**或 `CLAUDE_BIN` 路徑錯。
```bash
claude --version
which claude
```

### Q3: Azure 429 / TTS 失敗

跑單題不會。如果 30 題 verify 撞到，題目間 `sleep 10`。

### Q4: VisionAgent verdict 跟你的 label 不一致怎麼診斷

```bash
# 看 raw 輸出
cat runs/<ts>/<case>/vision_audit_log.json | python -m json.tool
```

對照你的 label 看：
1. **是 verdict 對但 defect code 錯**？→ 方向 3 補 code 定義
2. **是真的看走眼**？→ 方向 2 加 few-shot 例子
3. **是規則太嚴抓到不該抓的**？→ 方向 4 加 negative example
4. **是你 label 標錯**？→ review 自己的 label，是否能歸 borderline

### Q5: `manim` command not found

```bash
source .venv/bin/activate
which manim
pip install manim
```

### Q6: 我改完 code，怎麼確認沒爛掉？

```bash
# 1. Syntax check
python -c "import ast; ast.parse(open('agents/utils/vision_agent.py').read())"
python -c "import ast; ast.parse(open('agents/core/llm_client.py').read())"

# 2. Smoke test ELEM_01
python run_evaluation.py --case ELEM_01

# 3. 看 cost_report
cat stable_outputs/cost_report.json | python -m json.tool | head -20

# 4. 看 vision_audit_log
cat runs/<latest>/ELEM_01/vision_audit_log.json | python -m json.tool
```

### Q7: log 在哪？

| 用途 | 位置 |
|---|---|
| 完整 session log | `logs/<timestamp>_<topic>.log` |
| 單題渲染結果 | `runs/<timestamp>/<case>/` |
| 最終 mp4 | `stable_outputs/<topic>_<timestamp>.mp4` |
| 成本/timing | `stable_outputs/cost_report.json` |
| **Vision QA 細節** | `runs/<ts>/<case>/vision_audit_log.json` ← **你會常看** |
| Scene state | `runs/<ts>/<case>/scene_state_log.json` |

### Q8: 我懷疑某次 LLM call 特別慢

```bash
cat stable_outputs/cost_report.json | jq '.calls[] | {model, elapsed}'
```

### Q9: prompt 改完怎麼驗證沒退化？

**順序**：
```bash
# 1. Syntax check
python -c "import ast; ast.parse(open('agents/utils/vision_agent.py').read())"

# 2. Single case smoke
python run_evaluation.py --case ELEM_01

# 3. Labeled set harness (對比 baseline)
python evaluation/run_vision_eval.py
# 輸出會直接印 F1/precision/recall + per-defect

# 4. 跟前一次 baseline 對比
diff <(jq .overall evaluation/vision_labels/baseline_<prev>.json) \
     <(jq .overall evaluation/vision_labels/baseline_<new>.json)

# 5. 確定 F1 沒退 + per-defect 沒大幅退化才能 commit
```

---

## 12. Baseline 數字

> ⚠️ 待組員第一週跑完 Opus baseline 後回填

### Opus Baseline（方向 1 接好後跑）

```bash
echo "VISION_BACKEND=opus" >> .env
python evaluation/run_vision_eval.py
```

```
日期：YYYY-MM-DD
Backend：claude-opus-4-7 via claudealt CLI
樣本：evaluation/vision_labels/labels.json (50 題，borderline N 排除)

Overall:
  Precision: __
  Recall:    __
  F1:        __

Per-defect-code recall:
  OVERLAP:          __ (n=__)
  OVERFLOW:         __ (n=__)
  MISALIGNED:       __ (n=__)
  WRONG_CONTENT:    __ (n=__)
  WRONG_METAPHOR:   __ (n=__)
  CLUTTER:          __ (n=__)
  TOO_FAST:         __ (n=__)

borderline 排除：__ / 50
平均耗時：__ sec/call
```

**你的每個 PR 拿這份 Opus baseline 當對照基準**。後續方向 2-5 都在 Opus 之上改 prompt。

---

## 13. 連絡與資源

### 卡住超過 30 分鐘 → 來問

不要硬撐，直接問 owner @childe0905：
- 環境/setup 問題 → 通常 5 分鐘解決
- VisionAgent 行為看不懂 → 一起 trace
- 不確定優化方向是否合理 → 先問，不要做白工
- **30 題 FJ verify 跑之前一定要問**（quota approve）

### 參考檔案優先級

1. ⭐⭐⭐ `ONBOARDING.md`（本檔）— 從這開始
2. ⭐⭐⭐ `CLAUDE.md` — 專案規範（改 code 前必讀）
3. ⭐⭐⭐ `agents/utils/vision_agent.py` — **你的主戰場**
4. ⭐⭐ `agents/core/llm_client.py:436-495` — `ask_vision()` 你會改
5. ⭐⭐ `agents/utils/final_judge.py:646-786` — Opus 串接 reference（read-only）
6. ⭐⭐ `agents/orchestrator/refining_loop.py:1124-1210` — vision 呼叫點（read-only）
7. ⭐ `evaluation/test_cases.json` — 15 題定義
8. （選讀）`.ai-context/HANDOFF.md` — owner 歷史進度

### 外部資源

- [Manim Community 文檔](https://docs.manim.community/en/stable/)
- [Claude Code CLI 文檔](https://docs.claude.com/en/docs/claude-code/overview)
- [Claude Vision API](https://docs.claude.com/en/docs/build-with-claude/vision)（Opus 視覺 QA）

---

## 最後

歡迎加入。你的目標是**讓 VisionAgent 看得更準**，不是重寫整個 vision 系統。

第一個 PR 是 **方向 1（接 Opus backend）**——做完它，後面四個方向才有意義。

有疑問就問，**不要默默改下去**。
