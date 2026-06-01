"""
Planner Model Comparison Evaluation
====================================
Compares N Planner models on M topics by running ONLY the Planner step,
then having Claude Opus 4.7 judge each blueprint on 4 dimensions.

Usage:
    python run_planner_eval.py --dry-run             # validate environment + 1 sample
    python run_planner_eval.py                       # full eval (Round 1: 3 runs)
    python run_planner_eval.py --resume {timestamp}  # resume from checkpoint
"""
import os
import sys
import json
import time
import argparse
import traceback
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

from dotenv import load_dotenv
load_dotenv()

PROJECT_ROOT = Path(__file__).parent.resolve()
TEST_CASES_FILE = PROJECT_ROOT / "evaluation" / "test_cases.json"
RUNS_ROOT = PROJECT_ROOT / "runs"

# ────────────────────────────────────────────────────────────────────
# Experiment Configuration
# ────────────────────────────────────────────────────────────────────

MODELS = [
    # {"id": "deepseek-v4-flash",       "model": "deepseek-v4-flash",                      "thinking": False},
    # {"id": "deepseek-v4-pro",         "model": "deepseek-v4-pro",                        "thinking": False},
    # {"id": "deepseek-v4-pro-thinking","model": "deepseek-v4-pro",                        "thinking": True},
    # {"id": "qwen3-235b",              "model": "qwen/qwen3-235b-a22b-2507",              "thinking": False},
    # {"id": "gemini-2.5-flash",        "model": "google/gemini-2.5-flash",                "thinking": False},
    # {"id": "gemini-2.5-pro",          "model": "google/gemini-2.5-pro-preview",          "thinking": False},
    # {"id": "gemini-3-flash-preview",  "model": "google/gemini-3-flash-preview",          "thinking": False},
    # {"id": "llama-4-maverick",        "model": "meta-llama/llama-4-maverick",            "thinking": False},
    {"id": "claude-haiku-4.5",        "model": "anthropic/claude-haiku-4.5",             "thinking": False},
]

SELECTED_CASES = ["ELEM_03", "MID_03", "MID_05", "HIGH_01", "HIGH_03"]

ROUND1_RUNS = 3
ROUND2_EXTRA = 2
TIEBREAKER_THRESHOLD = 0.5
PLANNER_TIMEOUT_SEC = 180
MAX_BUDGET_USD = 30.0

WEIGHTS = {"math": 0.30, "pedagogy": 0.25, "spatial": 0.25, "feasibility": 0.20}

JUDGE_MODEL = "anthropic/claude-opus-4-8"

# ────────────────────────────────────────────────────────────────────
# Judge Prompt
# ────────────────────────────────────────────────────────────────────

JUDGE_SYSTEM = """You are a strict evaluator of Planner blueprints for a math education animation system.
Your job is to score a JSON blueprint that describes how to visualize a math concept using Manim animations.

You must score 4 dimensions on a 1-5 integer scale (1=poor, 5=excellent), then provide a brief rationale.

DIMENSIONS:
1. **math_accuracy** (1-5): Does the visualization approach correctly represent the mathematical concept? Score 5 if the visual metaphor genuinely teaches the concept; score 1 if the metaphor is wrong or misleading.

2. **pedagogy** (1-5): Is the step sequence logical for teaching? Does narration guide the viewer? Score 5 if a student would learn from this; score 1 if steps are confused or out of order.

3. **spatial_design** (1-5): Are coordinates within bounds (y ∈ [-2.5, +2.5] for content)? Are objects laid out without overlap? Is the layout clear? Score 5 for clean, well-spaced design; score 1 for chaotic or out-of-bounds layout.

4. **feasibility** (1-5): Can this plan be reasonably implemented in Manim? Are the proposed Mobjects appropriate? Score 5 for obviously implementable; score 1 if it requires impossible transformations.

OUTPUT FORMAT (strict JSON, no markdown):
{
  "scores": {"math_accuracy": int, "pedagogy": int, "spatial_design": int, "feasibility": int},
  "rationale": {
    "math_accuracy": "1-2 sentence explanation",
    "pedagogy": "1-2 sentence explanation",
    "spatial_design": "1-2 sentence explanation",
    "feasibility": "1-2 sentence explanation"
  },
  "overall_critique": "1 paragraph summary of strengths and weaknesses"
}

Be strict. Reserve 5/5 for genuinely excellent plans. Do not give pity scores."""


def judge_user_prompt(topic: str, blueprint_json: str) -> str:
    return f"""TOPIC (the math concept to visualize):
{topic}

BLUEPRINT TO EVALUATE:
{blueprint_json}

Score this blueprint on the 4 dimensions. Output strict JSON only."""


# ────────────────────────────────────────────────────────────────────
# Infrastructure
# ────────────────────────────────────────────────────────────────────

class EvalSession:
    def __init__(self, session_dir: Path):
        self.dir = session_dir
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / "blueprints").mkdir(exist_ok=True)
        (self.dir / "judge_scores").mkdir(exist_ok=True)
        self.progress_file = self.dir / "progress.json"
        self.config_file = self.dir / "config.json"
        self.progress = self._load_progress()

    def _load_progress(self) -> dict:
        if self.progress_file.exists():
            return json.loads(self.progress_file.read_text())
        return {"completed": [], "failed": [], "started_at": datetime.now().isoformat()}

    def save_progress(self):
        self.progress_file.write_text(json.dumps(self.progress, indent=2, ensure_ascii=False))

    def save_config(self, cfg: dict):
        self.config_file.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))

    def is_done(self, model_id: str, case_id: str, run_idx: int) -> bool:
        key = f"{model_id}/{case_id}/run_{run_idx}"
        return key in self.progress["completed"]

    def mark_done(self, model_id: str, case_id: str, run_idx: int):
        key = f"{model_id}/{case_id}/run_{run_idx}"
        if key not in self.progress["completed"]:
            self.progress["completed"].append(key)
        self.save_progress()

    def mark_failed(self, model_id: str, case_id: str, run_idx: int, reason: str):
        self.progress["failed"].append({
            "key": f"{model_id}/{case_id}/run_{run_idx}",
            "reason": reason[:300],
            "ts": datetime.now().isoformat(),
        })
        self.save_progress()

    def blueprint_path(self, model_id: str, case_id: str, run_idx: int) -> Path:
        d = self.dir / "blueprints" / model_id / case_id
        d.mkdir(parents=True, exist_ok=True)
        return d / f"run_{run_idx}.json"

    def score_path(self, model_id: str, case_id: str, run_idx: int) -> Path:
        d = self.dir / "judge_scores" / model_id / case_id
        d.mkdir(parents=True, exist_ok=True)
        return d / f"run_{run_idx}.json"


# ────────────────────────────────────────────────────────────────────
# Pre-flight Checks
# ────────────────────────────────────────────────────────────────────

def preflight_checks(models: list, judge_model: str) -> tuple[bool, list]:
    print("\n" + "═" * 60)
    print("🔍 Pre-flight Checks")
    print("═" * 60)

    available = []
    failures = []

    keys = {
        "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY"),
        "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY"),
    }
    for k, v in keys.items():
        status = "✅" if v else "❌"
        print(f"  {status} {k}: {'set' if v else 'MISSING'}")
        if not v:
            failures.append(f"{k} not set")

    if failures:
        return False, []

    from agents.core.llm_client import LLMClient
    llm = LLMClient(debug=False)

    print(f"\n  Testing {len(models)} Planner models...")
    for m in models:
        try:
            os.environ["PLANNER_MODEL"] = m["model"]
            if m["thinking"]:
                os.environ["PLANNER_THINKING"] = "1"
            else:
                os.environ.pop("PLANNER_THINKING", None)
            llm.models["planner"] = m["model"]
            t0 = time.time()
            resp = llm.ask("You are a JSON generator.", 'Reply with {"ok": true} only.', role="planner")
            dt = time.time() - t0
            if resp and len(resp) > 0:
                print(f"    ✅ {m['id']:30s} {dt:.1f}s")
                available.append(m)
            else:
                print(f"    ❌ {m['id']:30s} empty response")
        except Exception as e:
            print(f"    ❌ {m['id']:30s} {str(e)[:60]}")

    print(f"\n  Testing judge model: {judge_model}")
    try:
        llm.models["planner"] = judge_model
        resp = llm.ask("Reply in JSON.", 'Reply with {"ok": true} only.', role="planner", json_mode=True)
        json.loads(resp)
        print(f"    ✅ Judge ready")
    except Exception as e:
        print(f"    ❌ Judge failed: {e}")
        return False, available

    if not TEST_CASES_FILE.exists():
        print(f"    ❌ test_cases.json missing")
        return False, available
    cases_data = json.loads(TEST_CASES_FILE.read_text())
    case_ids = {c["id"] for c in cases_data}
    missing = [c for c in SELECTED_CASES if c not in case_ids]
    if missing:
        print(f"    ❌ Missing cases: {missing}")
        return False, available
    print(f"  ✅ All {len(SELECTED_CASES)} cases found")

    return len(available) > 0, available


# ────────────────────────────────────────────────────────────────────
# Planner Runner
# ────────────────────────────────────────────────────────────────────

def load_test_case(case_id: str) -> dict:
    cases = json.loads(TEST_CASES_FILE.read_text())
    for c in cases:
        if c["id"] == case_id:
            return c
    raise ValueError(f"Case {case_id} not found")


def run_planner_once(model_cfg: dict, topic: str, timeout_sec: int = PLANNER_TIMEOUT_SEC) -> tuple[dict, dict]:
    from agents.planner.planner import Planner
    from agents.core.llm_client import LLMClient

    os.environ["PLANNER_MODEL"] = model_cfg["model"]
    if model_cfg["thinking"]:
        os.environ["PLANNER_THINKING"] = "1"
    else:
        os.environ.pop("PLANNER_THINKING", None)

    llm = LLMClient(debug=False)
    llm.models["planner"] = model_cfg["model"]
    planner = Planner(llm_client=llm)

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(planner.plan_script_from_prompt, topic)
        try:
            script_json_str, thought_tree = future.result(timeout=timeout_sec)
        except FuturesTimeoutError:
            raise TimeoutError(f"Planner exceeded {timeout_sec}s")
    dt = time.time() - t0

    try:
        blueprint = json.loads(script_json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from Planner: {e}")

    meta = {
        "duration_sec": round(dt, 2),
        "thought_tree_chars": len(thought_tree) if thought_tree else 0,
        "blueprint_chars": len(script_json_str),
        "tokens": dict(llm.session_stats),
    }
    try:
        llm.close()
    except Exception:
        pass
    return blueprint, meta


# ────────────────────────────────────────────────────────────────────
# Judge
# ────────────────────────────────────────────────────────────────────

def judge_blueprint(topic: str, blueprint: dict, judge_model: str = JUDGE_MODEL) -> dict:
    from agents.core.llm_client import LLMClient
    llm = LLMClient(debug=False)
    llm.models["planner"] = judge_model

    bp_str = json.dumps(blueprint, ensure_ascii=False, indent=2)
    if len(bp_str) > 20000:
        bp_str = bp_str[:20000] + "\n... [truncated]"

    user_msg = judge_user_prompt(topic, bp_str)

    t0 = time.time()
    resp = llm.ask(JUDGE_SYSTEM, user_msg, role="planner", json_mode=True, temperature=0.0)
    dt = time.time() - t0

    parsed = json.loads(resp)
    parsed["_judge_duration_sec"] = round(dt, 2)
    parsed["_judge_model"] = judge_model

    s = parsed.get("scores", {})
    weighted = (
        WEIGHTS["math"] * s.get("math_accuracy", 0)
        + WEIGHTS["pedagogy"] * s.get("pedagogy", 0)
        + WEIGHTS["spatial"] * s.get("spatial_design", 0)
        + WEIGHTS["feasibility"] * s.get("feasibility", 0)
    )
    parsed["weighted_total"] = round(weighted, 3)

    try:
        llm.close()
    except Exception:
        pass
    return parsed


# ────────────────────────────────────────────────────────────────────
# Eval Orchestrator
# ────────────────────────────────────────────────────────────────────

def execute_run(session: EvalSession, model_cfg: dict, case: dict, run_idx: int) -> dict | None:
    model_id = model_cfg["id"]
    case_id = case["id"]
    topic = case["topic"]

    if session.is_done(model_id, case_id, run_idx):
        sp = session.score_path(model_id, case_id, run_idx)
        if sp.exists():
            return json.loads(sp.read_text())
        return None

    print(f"  ▶ {model_id:30s} {case_id} run_{run_idx}", end=" ", flush=True)

    blueprint = None
    meta = None
    last_err = None
    for attempt in range(2):
        try:
            blueprint, meta = run_planner_once(model_cfg, topic)
            break
        except Exception as e:
            last_err = e
            if attempt == 0:
                print(f"\n    ⚠️ retry: {str(e)[:80]}", end="", flush=True)
                time.sleep(2)

    if blueprint is None:
        print(f"\n    ❌ FAILED: {last_err}")
        session.mark_failed(model_id, case_id, run_idx, str(last_err))
        return None

    bp_path = session.blueprint_path(model_id, case_id, run_idx)
    bp_path.write_text(json.dumps({"blueprint": blueprint, "meta": meta}, indent=2, ensure_ascii=False))

    try:
        score = judge_blueprint(topic, blueprint)
    except Exception as e:
        print(f"\n    ❌ JUDGE FAILED: {str(e)[:100]}")
        session.mark_failed(model_id, case_id, run_idx, f"judge_error: {e}")
        return None

    sp = session.score_path(model_id, case_id, run_idx)
    sp.write_text(json.dumps(score, indent=2, ensure_ascii=False))
    session.mark_done(model_id, case_id, run_idx)

    print(f"  weighted={score['weighted_total']:.2f} planner={meta['duration_sec']:.0f}s")
    return score


def round1(session: EvalSession, models: list, cases: list):
    print("\n" + "═" * 60)
    print(f"🏁 Round 1 — {len(models)} models × {len(cases)} cases × {ROUND1_RUNS} runs")
    print("═" * 60)
    for run_idx in range(1, ROUND1_RUNS + 1):
        print(f"\n— Run {run_idx}/{ROUND1_RUNS} —")
        for case in cases:
            for m in models:
                execute_run(session, m, case, run_idx)


# ────────────────────────────────────────────────────────────────────
# Analysis
# ────────────────────────────────────────────────────────────────────

def collect_scores(session: EvalSession, models: list, cases: list) -> dict:
    result = defaultdict(lambda: defaultdict(list))
    for m in models:
        for c in cases:
            d = session.dir / "judge_scores" / m["id"] / c["id"]
            if not d.exists():
                continue
            for f in sorted(d.glob("run_*.json")):
                try:
                    result[c["id"]][m["id"]].append(json.loads(f.read_text()))
                except Exception:
                    pass
    return result


def identify_tiebreakers(scores_by_case: dict, threshold: float = TIEBREAKER_THRESHOLD) -> list:
    tiebreakers = []
    for case_id, by_model in scores_by_case.items():
        if not by_model:
            continue
        means = {m: sum(s["weighted_total"] for s in scores) / len(scores)
                 for m, scores in by_model.items() if scores}
        if not means:
            continue
        top = max(means.values())
        close = [m for m, v in means.items() if (top - v) <= threshold]
        if len(close) >= 2:
            tiebreakers.extend([(case_id, m) for m in close])
    return tiebreakers


def round2(session: EvalSession, models: list, cases: list, tiebreakers: list):
    if not tiebreakers:
        print("\n✅ No tiebreakers needed.")
        return

    print(f"\n— Round 2 — {len(tiebreakers)} tiebreaker runs")
    by_case = defaultdict(list)
    for case_id, model_id in tiebreakers:
        by_case[case_id].append(model_id)

    model_lookup = {m["id"]: m for m in models}
    case_lookup = {c["id"]: c for c in cases}

    for run_idx in range(ROUND1_RUNS + 1, ROUND1_RUNS + ROUND2_EXTRA + 1):
        print(f"\n— Tiebreaker Run {run_idx} —")
        for case_id, mids in by_case.items():
            for mid in mids:
                execute_run(session, model_lookup[mid], case_lookup[case_id], run_idx)


# ────────────────────────────────────────────────────────────────────
# Reporter
# ────────────────────────────────────────────────────────────────────

def generate_report(session: EvalSession, models: list, cases: list):
    scores_by_case = collect_scores(session, models, cases)

    lines = ["# Planner Evaluation Report\n"]
    lines.append(f"Session: `{session.dir.name}`\n")
    lines.append(f"Generated: {datetime.now().isoformat()}\n")
    lines.append(f"Weights: math={WEIGHTS['math']} pedagogy={WEIGHTS['pedagogy']} spatial={WEIGHTS['spatial']} feasibility={WEIGHTS['feasibility']}\n\n")

    overall_points = defaultdict(float)
    for c in cases:
        cid = c["id"]
        lines.append(f"## {cid}: {c['topic'][:50]}...\n\n")
        by_model = scores_by_case.get(cid, {})
        if not by_model:
            lines.append("_No data._\n\n")
            continue

        rows = []
        for m in models:
            mid = m["id"]
            arr = by_model.get(mid, [])
            if not arr:
                rows.append((mid, 0.0, 0.0, 0.0, 0.0, 0.0, 0))
                continue
            n = len(arr)
            mean_w = sum(s["weighted_total"] for s in arr) / n
            mean_math = sum(s["scores"]["math_accuracy"] for s in arr) / n
            mean_ped = sum(s["scores"]["pedagogy"] for s in arr) / n
            mean_spa = sum(s["scores"]["spatial_design"] for s in arr) / n
            mean_fea = sum(s["scores"]["feasibility"] for s in arr) / n
            rows.append((mid, mean_w, mean_math, mean_ped, mean_spa, mean_fea, n))

        rows.sort(key=lambda r: r[1], reverse=True)

        lines.append("| Rank | Model | Weighted | Math | Pedagogy | Spatial | Feasibility | Runs |\n")
        lines.append("|---|---|---|---|---|---|---|---|\n")
        for i, (mid, w, math, ped, spa, fea, n) in enumerate(rows, 1):
            if n == 0:
                lines.append(f"| - | {mid} | _failed_ | - | - | - | - | 0 |\n")
                continue
            lines.append(f"| {i} | {mid} | **{w:.2f}** | {math:.1f} | {ped:.1f} | {spa:.1f} | {fea:.1f} | {n} |\n")
            overall_points[mid] += (len(rows) - i)
        lines.append("\n")

    lines.append("## Overall Ranking (Borda Count)\n\n")
    lines.append("| Rank | Model | Borda Points |\n|---|---|---|\n")
    sorted_overall = sorted(overall_points.items(), key=lambda x: x[1], reverse=True)
    for i, (mid, pts) in enumerate(sorted_overall, 1):
        lines.append(f"| {i} | {mid} | {pts:.0f} |\n")
    lines.append("\n")

    if session.progress.get("failed"):
        lines.append("## Failures\n\n")
        for f in session.progress["failed"]:
            lines.append(f"- `{f['key']}`: {f['reason'][:80]}\n")
        lines.append("\n")

    report_path = session.dir / "final_report.md"
    report_path.write_text("".join(lines))
    print(f"\n📄 Report: {report_path}")

    csv_path = session.dir / "scores.csv"
    csv_lines = ["case_id,model_id,run_idx,weighted,math,pedagogy,spatial,feasibility"]
    for cid, by_model in scores_by_case.items():
        for mid, arr in by_model.items():
            for i, s in enumerate(arr, 1):
                sc = s["scores"]
                csv_lines.append(f"{cid},{mid},{i},{s['weighted_total']},{sc['math_accuracy']},{sc['pedagogy']},{sc['spatial_design']},{sc['feasibility']}")
    csv_path.write_text("\n".join(csv_lines))
    print(f"📊 CSV: {csv_path}")


# ────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", type=str)
    parser.add_argument("--no-round2", action="store_true")
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()

    if args.resume:
        session_dir = RUNS_ROOT / args.resume
        if not session_dir.exists():
            print(f"❌ Resume dir not found: {session_dir}")
            sys.exit(1)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = RUNS_ROOT / f"planner_eval_{ts}"

    session = EvalSession(session_dir)
    print(f"📁 Session: {session_dir}")

    if args.report_only:
        cases = [load_test_case(cid) for cid in SELECTED_CASES]
        generate_report(session, MODELS, cases)
        return

    ok, available_models = preflight_checks(MODELS, JUDGE_MODEL)
    if not ok:
        print("\n❌ Pre-flight failed. Aborting.")
        sys.exit(1)

    cases = [load_test_case(cid) for cid in SELECTED_CASES]
    session.save_config({
        "models": available_models,
        "cases": [c["id"] for c in cases],
        "round1_runs": ROUND1_RUNS,
        "round2_extra": ROUND2_EXTRA,
        "weights": WEIGHTS,
        "judge": JUDGE_MODEL,
    })

    if args.dry_run:
        print("\n🧪 Dry Run — 1 model × 1 case × 1 run")
        m = available_models[0]
        c = cases[0]
        score = execute_run(session, m, c, 1)
        if score:
            print("\n✅ Dry run successful!")
            print(json.dumps(score, indent=2, ensure_ascii=False))
        else:
            print("\n❌ Dry run failed")
            sys.exit(1)
        return

    round1(session, available_models, cases)

    if not args.no_round2:
        scores = collect_scores(session, available_models, cases)
        tiebreakers = identify_tiebreakers(scores)
        round2(session, available_models, cases, tiebreakers)

    generate_report(session, available_models, cases)
    print("\n✅ Evaluation complete.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏸  Interrupted. Resume with: python run_planner_eval.py --resume <timestamp>")
        sys.exit(130)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
