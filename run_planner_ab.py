"""
Planner A/B Experiment: Opus (claude-code-planner) vs Gemini-2.5-Flash
=======================================================================
Pairwise blind evaluation with counterbalancing, difficulty stratification,
and statistical tests.

Usage:
    python run_planner_ab.py --pilot              # Phase 0: 5 topics, N=1
    python run_planner_ab.py --full               # Phase 1: 24 topics, N=3
    python run_planner_ab.py --cross-check        # Phase 2: GPT-4o spot check
    python run_planner_ab.py --report             # Regenerate report from existing runs
    python run_planner_ab.py --pilot --difficulty elem  # Filter by difficulty
"""
import os
import sys
import re
import json
import time
import random
import argparse
import traceback
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

from dotenv import load_dotenv
load_dotenv()

PROJECT_ROOT = Path(__file__).parent.resolve()
TEST_CASES_FILE = PROJECT_ROOT / "evaluation" / "test_cases_ab24.json"
RUNS_ROOT = PROJECT_ROOT / "runs"

# ────────────────────────────────────────────────────────────────────
# Experiment Config
# ────────────────────────────────────────────────────────────────────

CONTESTANTS = [
    {"id": "opus_full",    "model": "claude-code-planner-full"},
    {"id": "opus_compact", "model": "claude-code-planner-compact"},
]

N_RUNS = 3                    # Repetitions per topic per model
PLANNER_TIMEOUT_SEC = 300     # Opus can be slow

JUDGE_MODEL_PRIMARY    = "claude-sonnet-judge"
JUDGE_MODEL_CROSSCHECK = "google/gemini-2.5-pro-preview"
WEIGHTS = {"math": 0.30, "pedagogy": 0.25, "spatial": 0.25, "feasibility": 0.20}

# Metadata keys to scrub from stripped plan (blind evaluation)
_SCRUB_KEYS = re.compile(
    r'"(model_id|planner_model|model|generated_by|source|provider|contestant_id)"',
    re.IGNORECASE,
)
_SCRUB_VALUES = re.compile(
    r'(claude|opus|gemini|flash|anthropic|google|openrouter)',
    re.IGNORECASE,
)

# ────────────────────────────────────────────────────────────────────
# Judge Prompts
# ────────────────────────────────────────────────────────────────────

JUDGE_SYSTEM = """You are an expert evaluator of Manim animation blueprints for math education.

You will receive a math topic, its ground truth, and two anonymized plans (Plan A and Plan B).
Your task: decide which plan is better for producing a high-quality educational animation.

EVALUATION CRITERIA (4 dimensions):
1. math_accuracy   — Does the visualization correctly teach the mathematical concept?
2. pedagogy        — Is the step sequence logical? Does narration guide the viewer?
3. spatial_design  — Are coordinates within bounds? No overlapping objects? Clean layout?
4. feasibility     — Can this be implemented in Manim CE without impossible transformations?

IMPORTANT ANTI-BIAS RULES:
- Length is NOT quality. A concise, correct plan beats a verbose, correct plan.
- Do NOT prefer a plan simply because it mentions more objects or steps.
- Judge purely on quality, not quantity.

REQUIRED REASONING (step-by-step, no shortcuts):
Step 1: List Plan A's strengths (2-3 points)
Step 2: List Plan A's weaknesses (2-3 points)
Step 3: List Plan B's strengths (2-3 points)
Step 4: List Plan B's weaknesses (2-3 points)
Step 5: Compare directly on each dimension
Step 6: Decide winner

OUTPUT (strict JSON, no markdown wrapper):
{
  "reasoning": {
    "plan_a_strengths": ["..."],
    "plan_a_weaknesses": ["..."],
    "plan_b_strengths": ["..."],
    "plan_b_weaknesses": ["..."]
  },
  "dimension_winner": {
    "math_accuracy": "A" | "B" | "tie",
    "pedagogy": "A" | "B" | "tie",
    "spatial_design": "A" | "B" | "tie",
    "feasibility": "A" | "B" | "tie"
  },
  "winner": "A" | "B" | "tie",
  "confidence": 1-7
}"""


def judge_user_prompt(topic: str, ground_truth: dict, plan_a: str, plan_b: str) -> str:
    gt_str = json.dumps(ground_truth, ensure_ascii=False)
    return f"""TOPIC:
{topic}

GROUND TRUTH (for your reference only, do not mention to contestants):
{gt_str}

PLAN A:
{plan_a}

PLAN B:
{plan_b}

Evaluate both plans following the required step-by-step reasoning. Output strict JSON only."""


# ────────────────────────────────────────────────────────────────────
# Session Management
# ────────────────────────────────────────────────────────────────────

class ABSession:
    def __init__(self, session_dir: Path):
        self.dir = session_dir
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / "blueprints").mkdir(exist_ok=True)
        (self.dir / "judge_results").mkdir(exist_ok=True)
        self.progress_file = self.dir / "progress.json"
        self.progress = self._load()

    def _load(self) -> dict:
        if self.progress_file.exists():
            return json.loads(self.progress_file.read_text())
        return {
            "planner_done": [],
            "judge_done": [],
            "failed": [],
            "started_at": datetime.now().isoformat(),
        }

    def save(self):
        self.progress_file.write_text(json.dumps(self.progress, indent=2, ensure_ascii=False))

    def planner_key(self, contestant_id: str, topic_id: str, run: int) -> str:
        return f"plan/{contestant_id}/{topic_id}/r{run}"

    def judge_key(self, topic_id: str, run: int, position: str) -> str:
        return f"judge/{topic_id}/r{run}/{position}"

    def is_planner_done(self, contestant_id: str, topic_id: str, run: int) -> bool:
        return self.planner_key(contestant_id, topic_id, run) in self.progress["planner_done"]

    def is_judge_done(self, topic_id: str, run: int, position: str) -> bool:
        return self.judge_key(topic_id, run, position) in self.progress["judge_done"]

    def mark_planner_done(self, contestant_id: str, topic_id: str, run: int):
        k = self.planner_key(contestant_id, topic_id, run)
        if k not in self.progress["planner_done"]:
            self.progress["planner_done"].append(k)
        self.save()

    def mark_judge_done(self, topic_id: str, run: int, position: str):
        k = self.judge_key(topic_id, run, position)
        if k not in self.progress["judge_done"]:
            self.progress["judge_done"].append(k)
        self.save()

    def mark_failed(self, key: str, reason: str):
        self.progress["failed"].append({"key": key, "reason": reason[:300], "ts": datetime.now().isoformat()})
        self.save()

    def blueprint_path(self, contestant_id: str, topic_id: str, run: int) -> Path:
        d = self.dir / "blueprints" / contestant_id / topic_id
        d.mkdir(parents=True, exist_ok=True)
        return d / f"r{run}.json"

    def judge_path(self, topic_id: str, run: int, position: str) -> Path:
        d = self.dir / "judge_results" / topic_id
        d.mkdir(parents=True, exist_ok=True)
        return d / f"r{run}_{position}.json"


# ────────────────────────────────────────────────────────────────────
# Blind Stripping
# ────────────────────────────────────────────────────────────────────

def strip_metadata(blueprint: dict) -> dict:
    """Remove any keys/values that reveal model identity."""
    raw = json.dumps(blueprint, ensure_ascii=False)
    # Remove identifying key-value pairs entirely
    cleaned = re.sub(
        r'"(?:model_id|planner_model|model|generated_by|source|provider|contestant_id)"\s*:\s*"[^"]*",?\s*',
        "",
        raw,
        flags=re.IGNORECASE,
    )
    # Scrub model names from values too (e.g. inside strings)
    cleaned = re.sub(
        r'\b(claude-opus|claude-code-planner|gemini-2\.5-flash|google/gemini|anthropic/claude)\b',
        "[MODEL]",
        cleaned,
        flags=re.IGNORECASE,
    )
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: return original without the known keys
        return {k: v for k, v in blueprint.items()
                if k.lower() not in {"model_id", "planner_model", "model", "generated_by", "source", "provider"}}


# ────────────────────────────────────────────────────────────────────
# Planner Runner
# ────────────────────────────────────────────────────────────────────

def run_planner_once(contestant: dict, topic: str, temperature: float = 0.3) -> tuple[dict, dict]:
    """Run one planner call. Returns (blueprint_dict, meta_dict)."""
    from agents.planner.planner import Planner
    from agents.core.llm_client import LLMClient

    os.environ["PLANNER_MODEL"] = contestant["model"]
    os.environ.pop("PLANNER_THINKING", None)

    llm = LLMClient(debug=False)
    llm.models["planner"] = contestant["model"]
    planner = Planner(llm_client=llm)

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(planner.plan_script_from_prompt, topic)
        try:
            script_json_str, thought_tree = future.result(timeout=PLANNER_TIMEOUT_SEC)
        except FuturesTimeoutError:
            raise TimeoutError(f"Planner exceeded {PLANNER_TIMEOUT_SEC}s")
    dt = time.time() - t0

    try:
        blueprint = json.loads(script_json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from Planner: {e}")

    meta = {
        "contestant_id": contestant["id"],
        "model": contestant["model"],
        "duration_sec": round(dt, 2),
        "thought_tree_chars": len(thought_tree) if thought_tree else 0,
        "tokens": dict(llm.session_stats),
    }
    try:
        llm.close()
    except Exception:
        pass
    return blueprint, meta


def run_planner_with_retry(contestant: dict, topic: str, max_attempts: int = 2) -> tuple[dict, dict] | tuple[None, None]:
    last_err = None
    for attempt in range(max_attempts):
        try:
            return run_planner_once(contestant, topic)
        except Exception as e:
            last_err = e
            if attempt < max_attempts - 1:
                print(f"    retry ({attempt+1}): {str(e)[:80]}")
                time.sleep(3)
    print(f"    FAILED: {last_err}")
    return None, None


# ────────────────────────────────────────────────────────────────────
# Pairwise Judge
# ────────────────────────────────────────────────────────────────────

def judge_pairwise(
    topic: str,
    ground_truth: dict,
    plan_a: dict,
    plan_b: dict,
    judge_model: str = JUDGE_MODEL_PRIMARY,
) -> dict:
    from agents.core.llm_client import LLMClient

    llm = LLMClient(debug=False)
    llm.models["planner"] = judge_model

    a_str = json.dumps(plan_a, ensure_ascii=False, indent=2)
    b_str = json.dumps(plan_b, ensure_ascii=False, indent=2)
    # Truncate if enormous
    if len(a_str) > 15000:
        a_str = a_str[:15000] + "\n...[truncated]"
    if len(b_str) > 15000:
        b_str = b_str[:15000] + "\n...[truncated]"

    user_msg = judge_user_prompt(topic, ground_truth, a_str, b_str)

    t0 = time.time()
    resp = llm.ask(JUDGE_SYSTEM, user_msg, role="planner", json_mode=True, temperature=0.0)
    dt = time.time() - t0

    # _call_claude_code() ignores json_mode — strip markdown fences if present
    resp_clean = re.sub(r"```json\s*|\s*```", "", resp).strip()
    # Extract first {...} block in case there's surrounding prose
    m = re.search(r"\{.*\}", resp_clean, re.DOTALL)
    if m:
        resp_clean = m.group(0)
    parsed = json.loads(resp_clean)
    parsed["_judge_model"] = judge_model
    parsed["_judge_duration_sec"] = round(dt, 2)

    try:
        llm.close()
    except Exception:
        pass
    return parsed


# ────────────────────────────────────────────────────────────────────
# Phase 0: Pilot
# ────────────────────────────────────────────────────────────────────

def run_pilot(session: ABSession, cases: list, judge_model: str):
    # Pick 1 Elem + 2 Mid + 2 High
    by_diff = defaultdict(list)
    for c in cases:
        by_diff[c["category"].lower()].append(c)

    pilot_cases = []
    for diff, count in [("elementary", 1), ("middle", 2), ("high", 2)]:
        subset = by_diff.get(diff, [])
        pilot_cases.extend(random.sample(subset, min(count, len(subset))))

    print(f"\n{'='*60}")
    print(f"Phase 0 — Pilot ({len(pilot_cases)} topics, N=1, with position swap)")
    print(f"{'='*60}")
    for c in pilot_cases:
        print(f"  {c['id']} [{c['category']}] {c['topic_en'][:60]}")

    _run_cases(session, pilot_cases, n_runs=1, judge_model=judge_model)
    _generate_report(session, pilot_cases)


# ────────────────────────────────────────────────────────────────────
# Phase 1: Full
# ────────────────────────────────────────────────────────────────────

def run_full(session: ABSession, cases: list, judge_model: str, difficulty_filter: str | None = None):
    if difficulty_filter:
        diff_map = {"elem": "elementary", "mid": "middle", "high": "high"}
        target = diff_map.get(difficulty_filter.lower(), difficulty_filter.lower())
        cases = [c for c in cases if c["category"].lower() == target]
        print(f"  Filtered to {len(cases)} {difficulty_filter} cases")

    print(f"\n{'='*60}")
    print(f"Phase 1 — Full A/B ({len(cases)} topics, N={N_RUNS}, with position swap)")
    print(f"{'='*60}")

    _run_cases(session, cases, n_runs=N_RUNS, judge_model=judge_model)
    _generate_report(session, cases)


# ────────────────────────────────────────────────────────────────────
# Core Runner
# ────────────────────────────────────────────────────────────────────

def _run_cases(session: ABSession, cases: list, n_runs: int, judge_model: str):
    """Run all planner calls then all judge calls."""
    # Step 1: Generate all plans
    print(f"\n--- Step 1: Generating Plans ---")
    for run in range(1, n_runs + 1):
        print(f"\n  Run {run}/{n_runs}")
        for case in cases:
            for contestant in CONTESTANTS:
                _generate_plan(session, contestant, case, run)

    # Step 2: Pairwise judging with position swap
    print(f"\n--- Step 2: Pairwise Judging ---")
    for run in range(1, n_runs + 1):
        print(f"\n  Run {run}/{n_runs}")
        for case in cases:
            _judge_pair(session, case, run, judge_model)


def _generate_plan(session: ABSession, contestant: dict, case: dict, run: int):
    cid = contestant["id"]
    tid = case["id"]

    if session.is_planner_done(cid, tid, run):
        print(f"    skip {cid}/{tid}/r{run} (cached)")
        return

    print(f"    {cid:8s} {tid} r{run}", end="  ", flush=True)
    blueprint, meta = run_planner_with_retry(contestant, case["topic"])

    if blueprint is None:
        session.mark_failed(f"plan/{cid}/{tid}/r{run}", "planner_failed")
        return

    bp_path = session.blueprint_path(cid, tid, run)
    bp_path.write_text(json.dumps({"blueprint": blueprint, "meta": meta}, indent=2, ensure_ascii=False))
    session.mark_planner_done(cid, tid, run)
    print(f"done ({meta['duration_sec']:.0f}s)")


def _judge_pair(session: ABSession, case: dict, run: int, judge_model: str):
    """Run two judge calls per pair (original + swapped position)."""
    tid = case["id"]
    topic = case["topic_en"] or case["topic"]
    gt = case.get("ground_truth", {})

    id_a = CONTESTANTS[0]["id"]
    id_b = CONTESTANTS[1]["id"]

    # Load both blueprints
    bp_path_a = session.blueprint_path(id_a, tid, run)
    bp_path_b = session.blueprint_path(id_b, tid, run)

    if not bp_path_a.exists() or not bp_path_b.exists():
        print(f"    skip judge {tid}/r{run}: missing blueprint(s)")
        return

    data_a = json.loads(bp_path_a.read_text())
    data_b = json.loads(bp_path_b.read_text())

    stripped_a = strip_metadata(data_a["blueprint"])
    stripped_b = strip_metadata(data_b["blueprint"])

    # Position "orig": A=id_a, B=id_b
    # Position "swap": A=id_b, B=id_a
    for position, plan_a, plan_b in [
        ("orig", stripped_a, stripped_b),
        ("swap", stripped_b, stripped_a),
    ]:
        if session.is_judge_done(tid, run, position):
            print(f"    skip judge {tid}/r{run}/{position} (cached)")
            continue

        print(f"    judge {tid}/r{run}/{position}", end="  ", flush=True)
        try:
            result = judge_pairwise(topic, gt, plan_a, plan_b, judge_model)
        except Exception as e:
            print(f"FAILED: {str(e)[:80]}")
            session.mark_failed(f"judge/{tid}/r{run}/{position}", str(e))
            continue

        # Translate winner back to contestant id
        raw_winner = result.get("winner", "tie")
        if position == "orig":
            winner_id = {"A": id_a, "B": id_b, "tie": "tie"}.get(raw_winner, "tie")
        else:
            winner_id = {"A": id_b, "B": id_a, "tie": "tie"}.get(raw_winner, "tie")

        result["_position"] = position
        result["_winner_contestant"] = winner_id
        result["_topic_id"] = tid
        result["_run"] = run

        jp = session.judge_path(tid, run, position)
        jp.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        session.mark_judge_done(tid, run, position)
        print(f"winner={winner_id} conf={result.get('confidence','?')}")


# ────────────────────────────────────────────────────────────────────
# Phase 2: Cross-check
# ────────────────────────────────────────────────────────────────────

def run_crosscheck(session: ABSession, cases: list, crosscheck_model: str = JUDGE_MODEL_CROSSCHECK):
    """Re-judge a random 5-case sample with a second judge model."""
    print(f"\n{'='*60}")
    print(f"Phase 2 — Cross-check judge: {crosscheck_model}")
    print(f"{'='*60}")

    by_diff = defaultdict(list)
    for c in cases:
        by_diff[c["category"].lower()].append(c)

    sample = []
    for diff, count in [("elementary", 2), ("middle", 2), ("high", 2)]:
        subset = by_diff.get(diff, [])
        sample.extend(random.sample(subset, min(count, len(subset))))
    sample = sample[:5]

    print(f"  Cross-check cases: {[c['id'] for c in sample]}")

    xcheck_dir = session.dir / "cross_check"
    xcheck_dir.mkdir(exist_ok=True)

    primary_results = []
    secondary_results = []

    for case in sample:
        tid = case["id"]
        topic = case["topic_en"] or case["topic"]
        gt = case.get("ground_truth", {})

        # Use run=1, orig position for cross-check
        jp_primary = session.judge_path(tid, 1, "orig")
        if not jp_primary.exists():
            print(f"    skip {tid}: no primary judge result for r1/orig")
            continue

        primary_data = json.loads(jp_primary.read_text())
        primary_winner = primary_data.get("_winner_contestant", "tie")

        opus_bp  = session.blueprint_path("opus",  tid, 1)
        flash_bp = session.blueprint_path("flash", tid, 1)
        if not opus_bp.exists() or not flash_bp.exists():
            print(f"    skip {tid}: missing blueprints")
            continue

        opus_stripped  = strip_metadata(json.loads(opus_bp.read_text())["blueprint"])
        flash_stripped = strip_metadata(json.loads(flash_bp.read_text())["blueprint"])

        print(f"    xcheck {tid}", end="  ", flush=True)
        try:
            result = judge_pairwise(topic, gt, opus_stripped, flash_stripped, crosscheck_model)
        except Exception as e:
            print(f"FAILED: {str(e)[:80]}")
            continue

        raw_winner = result.get("winner", "tie")
        winner_id = {"A": "opus", "B": "flash", "tie": "tie"}.get(raw_winner, "tie")
        result["_winner_contestant"] = winner_id
        result["_primary_winner"] = primary_winner
        result["_agree"] = (winner_id == primary_winner)

        out_path = xcheck_dir / f"{tid}_r1_orig.json"
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))

        primary_results.append(primary_winner)
        secondary_results.append(winner_id)
        print(f"primary={primary_winner} secondary={winner_id} agree={result['_agree']}")

    # Cohen's kappa
    if primary_results:
        kappa = _cohens_kappa(primary_results, secondary_results)
        print(f"\n  Cohen's kappa = {kappa:.3f}")
        (xcheck_dir / "kappa.json").write_text(
            json.dumps({"kappa": kappa, "primary": primary_results, "secondary": secondary_results}, indent=2)
        )


def _cohens_kappa(y1: list, y2: list) -> float:
    from collections import Counter
    labels = list(set(y1 + y2))
    n = len(y1)
    if n == 0:
        return 0.0
    # Observed agreement
    p_o = sum(a == b for a, b in zip(y1, y2)) / n
    # Expected agreement
    c1 = Counter(y1)
    c2 = Counter(y2)
    p_e = sum(c1[l] / n * c2[l] / n for l in labels)
    if p_e == 1.0:
        return 1.0
    return (p_o - p_e) / (1.0 - p_e)


# ────────────────────────────────────────────────────────────────────
# Analysis & Report
# ────────────────────────────────────────────────────────────────────

def _collect_judge_results(session: ABSession, cases: list) -> list[dict]:
    """Collect all judge result records."""
    records = []
    for case in cases:
        tid = case["id"]
        jd = session.dir / "judge_results" / tid
        if not jd.exists():
            continue
        for f in sorted(jd.glob("r*_*.json")):
            try:
                data = json.loads(f.read_text())
                data["_topic_id"] = data.get("_topic_id", tid)
                data["_category"] = case["category"].lower()
                data["_is_application"] = case.get("is_application", False)
                records.append(data)
            except Exception:
                pass
    return records


def _sign_test(wins_a: int, wins_b: int) -> float:
    """Two-sided binomial sign test. Returns p-value (excluding ties)."""
    n = wins_a + wins_b
    if n == 0:
        return 1.0
    from math import comb, pow
    # P(X >= wins_a) under H0: p=0.5
    # Two-sided: 2 * min(p_lower, p_upper)
    k = max(wins_a, wins_b)
    p_one_side = sum(comb(n, i) * (0.5 ** n) for i in range(k, n + 1))
    return min(1.0, 2 * p_one_side)


def _ci_95(wins: int, total: int) -> tuple[float, float]:
    """Wilson score interval."""
    if total == 0:
        return (0.0, 1.0)
    from math import sqrt
    z = 1.96
    p = wins / total
    denom = 1 + z**2 / total
    centre = (p + z**2 / (2 * total)) / denom
    margin = z * sqrt(p * (1 - p) / total + z**2 / (4 * total**2)) / denom
    return (max(0.0, centre - margin), min(1.0, centre + margin))


def _deduplicate_pairs(records: list[dict]) -> list[dict]:
    """
    Keep only one record per (topic_id, run) pair by averaging orig+swap
    to remove position bias. Returns deduplicated list with consensus winner.
    """
    pairs: dict[str, dict] = {}
    for r in records:
        k = f"{r['_topic_id']}/r{r['_run']}"
        if k not in pairs:
            pairs[k] = {"orig": None, "swap": None, "meta": r}
        position = r.get("_position", "orig")
        pairs[k][position] = r

    deduped = []
    for k, v in pairs.items():
        orig = v["orig"]
        swap = v["swap"]
        meta = v["meta"]

        if orig and swap:
            w_orig = orig.get("_winner_contestant", "tie")
            w_swap = swap.get("_winner_contestant", "tie")
            # Consensus: agree = use that, disagree = tie
            consensus = w_orig if w_orig == w_swap else "tie"
            position_bias = (w_orig != w_swap)
        elif orig:
            consensus = orig.get("_winner_contestant", "tie")
            position_bias = False
        elif swap:
            consensus = swap.get("_winner_contestant", "tie")
            position_bias = False
        else:
            continue

        deduped.append({
            "_topic_id": meta["_topic_id"],
            "_run": meta["_run"],
            "_category": meta["_category"],
            "_is_application": meta["_is_application"],
            "_consensus_winner": consensus,
            "_position_bias": position_bias,
            "_orig": orig,
            "_swap": swap,
        })
    return deduped


def _generate_report(session: ABSession, cases: list):
    all_records = _collect_judge_results(session, cases)
    deduped = _deduplicate_pairs(all_records)

    if not deduped:
        print("  No judge results to report yet.")
        return

    id_a = CONTESTANTS[0]["id"]
    id_b = CONTESTANTS[1]["id"]

    lines = ["# Planner A/B Experiment Report\n\n"]
    lines.append(f"Session: `{session.dir.name}`  \n")
    lines.append(f"Generated: {datetime.now().isoformat()}  \n")
    lines.append(f"Contestants: **{id_a}** ({CONTESTANTS[0]['model']}) vs **{id_b}** ({CONTESTANTS[1]['model']})  \n\n")

    # ── Per-difficulty table ──
    lines.append("## Win Rate by Difficulty\n\n")
    lines.append(f"| Difficulty | N pairs | {id_a} wins | {id_b} wins | Ties | {id_a} WR | 95% CI | p-value |\n")
    lines.append("|---|---|---|---|---|---|---|---|\n")

    diff_groups = {"elementary": [], "middle": [], "high": [], "all": deduped}
    for r in deduped:
        diff_groups[r["_category"]].append(r)

    for diff_key, label in [("elementary", "Elementary"), ("middle", "Middle"), ("high", "High"), ("all", "**ALL**")]:
        group = diff_groups[diff_key]
        n = len(group)
        a_wins = sum(1 for r in group if r["_consensus_winner"] == id_a)
        b_wins = sum(1 for r in group if r["_consensus_winner"] == id_b)
        ties   = sum(1 for r in group if r["_consensus_winner"] == "tie")
        n_decisive = a_wins + b_wins
        wr = a_wins / n_decisive if n_decisive > 0 else 0.0
        lo, hi = _ci_95(a_wins, n_decisive)
        p = _sign_test(a_wins, b_wins)
        lines.append(f"| {label} | {n} | {a_wins} | {b_wins} | {ties} | {wr:.2f} | [{lo:.2f},{hi:.2f}] | {p:.4f} |\n")

    lines.append("\n")

    # ── Per-dimension breakdown ──
    lines.append(f"## Dimension Win Breakdown ({id_a} vs {id_b})\n\n")
    lines.append(f"| Dimension | {id_a} wins | {id_b} wins | Tie |\n|---|---|---|---|\n")

    dim_counts: dict[str, dict] = {}
    for r in deduped:
        for position_record in [r["_orig"], r["_swap"]]:
            if not position_record:
                continue
            dw = position_record.get("dimension_winner", {})
            for dim, raw_winner in dw.items():
                if dim not in dim_counts:
                    dim_counts[dim] = {id_a: 0, id_b: 0, "tie": 0}
                position = position_record.get("_position", "orig")
                if position == "orig":
                    contestant_winner = {"A": id_a, "B": id_b, "tie": "tie"}.get(raw_winner, "tie")
                else:
                    contestant_winner = {"A": id_b, "B": id_a, "tie": "tie"}.get(raw_winner, "tie")
                dim_counts[dim][contestant_winner] = dim_counts[dim].get(contestant_winner, 0) + 1

    for dim, counts in dim_counts.items():
        lines.append(f"| {dim} | {counts.get(id_a,0)} | {counts.get(id_b,0)} | {counts.get('tie',0)} |\n")
    lines.append("\n")

    # ── Application sub-analysis ──
    app_group    = [r for r in deduped if r["_is_application"]]
    nonapp_group = [r for r in deduped if not r["_is_application"]]

    if app_group and nonapp_group:
        lines.append("## Application vs Non-Application Sub-analysis\n\n")
        for label, group in [("Application (E07,E08,M07,M08,H07,H08)", app_group), ("Non-application", nonapp_group)]:
            n = len(group)
            aw = sum(1 for r in group if r["_consensus_winner"] == id_a)
            bw = sum(1 for r in group if r["_consensus_winner"] == id_b)
            nd = aw + bw
            wr = aw / nd if nd > 0 else 0.0
            p  = _sign_test(aw, bw)
            lines.append(f"**{label}**: N={n}, {id_a} WR={wr:.2f}, p={p:.4f}  \n")
        lines.append("\n")

        # Chi-square
        app_a  = sum(1 for r in app_group    if r["_consensus_winner"] == id_a)
        app_b  = sum(1 for r in app_group    if r["_consensus_winner"] == id_b)
        na_a   = sum(1 for r in nonapp_group if r["_consensus_winner"] == id_a)
        na_b   = sum(1 for r in nonapp_group if r["_consensus_winner"] == id_b)
        chi2_p = _chi2_2x2(app_a, app_b, na_a, na_b)
        lines.append(f"Chi-square (app vs non-app win rate): p={chi2_p:.4f}  \n\n")

    # ── Position bias ──
    bias_count = sum(1 for r in deduped if r["_position_bias"])
    total_pairs = len([r for r in deduped if r["_orig"] and r["_swap"]])
    if total_pairs > 0:
        bias_rate = bias_count / total_pairs
        lines.append(f"## Position Bias Check\n\n")
        lines.append(f"Counterbalance disagreement rate: {bias_rate:.1%} ({bias_count}/{total_pairs})  \n")
        if bias_rate > 0.15:
            lines.append("⚠️ WARNING: >15% disagreement rate. Judge may have position bias.  \n")
        lines.append("\n")

    # ── Cross-check ──
    xcheck_kappa_file = session.dir / "cross_check" / "kappa.json"
    if xcheck_kappa_file.exists():
        kdata = json.loads(xcheck_kappa_file.read_text())
        lines.append(f"## Inter-judge Agreement (Cross-check)\n\n")
        lines.append(f"Cohen's kappa = **{kdata['kappa']:.3f}**  \n")
        kappa = kdata["kappa"]
        if kappa < 0.4:
            lines.append("⚠️ Low agreement — results should be interpreted cautiously.  \n")
        elif kappa >= 0.6:
            lines.append("Good inter-judge agreement.  \n")
        lines.append("\n")

    # ── Failures ──
    if session.progress.get("failed"):
        lines.append("## Failures\n\n")
        for f in session.progress["failed"]:
            lines.append(f"- `{f['key']}`: {f['reason'][:80]}  \n")
        lines.append("\n")

    # ── Conclusion ──
    lines.append("## Conclusion\n\n")
    for diff_key, label in [("elementary", "Elementary"), ("middle", "Middle"), ("high", "High")]:
        group = diff_groups[diff_key]
        if not group:
            continue
        aw  = sum(1 for r in group if r["_consensus_winner"] == id_a)
        bw  = sum(1 for r in group if r["_consensus_winner"] == id_b)
        nd  = aw + bw
        wr  = aw / nd if nd > 0 else 0.0
        p   = _sign_test(aw, bw)
        verdict = f"{id_a} significantly better (p<0.05)" if p < 0.05 and wr > 0.5 \
             else f"{id_b} significantly better (p<0.05)" if p < 0.05 and wr < 0.5 \
             else "No significant difference (p>=0.05)"
        lines.append(f"- **{label}**: {id_a} WR={wr:.2f}, p={p:.4f} → {verdict}  \n")

    report_path = session.dir / "final_report.md"
    report_path.write_text("".join(lines))
    print(f"\nReport: {report_path}")

    # Also write CSV
    csv_rows = ["topic_id,run,category,is_application,consensus_winner,position_bias"]
    for r in deduped:
        csv_rows.append(
            f"{r['_topic_id']},{r['_run']},{r['_category']},{r['_is_application']},"
            f"{r['_consensus_winner']},{r['_position_bias']}"
        )
    csv_path = session.dir / "results.csv"
    csv_path.write_text("\n".join(csv_rows))
    print(f"CSV:    {csv_path}")


def _chi2_2x2(a: int, b: int, c: int, d: int) -> float:
    """Chi-square for 2x2 contingency table [[a,b],[c,d]]. Returns p-value."""
    from math import sqrt
    n = a + b + c + d
    if n == 0:
        return 1.0
    expected_a = (a + b) * (a + c) / n
    expected_b = (a + b) * (b + d) / n
    expected_c = (c + d) * (a + c) / n
    expected_d = (c + d) * (b + d) / n

    chi2 = 0.0
    for obs, exp in [(a, expected_a), (b, expected_b), (c, expected_c), (d, expected_d)]:
        if exp > 0:
            chi2 += (obs - exp) ** 2 / exp

    # Degrees of freedom = 1, use chi2 CDF approximation
    # Use scipy if available, otherwise regularized incomplete gamma
    try:
        from scipy.stats import chi2 as chi2_dist
        return float(1 - chi2_dist.cdf(chi2, df=1))
    except ImportError:
        # Rough approximation via normal (chi2(1) = Z^2)
        z = sqrt(chi2)
        # erfc approximation
        import math
        p = 2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2))))
        return max(0.0, min(1.0, p))


# ────────────────────────────────────────────────────────────────────
# Pre-flight
# ────────────────────────────────────────────────────────────────────

def preflight(contestants: list, judge_model: str) -> bool:
    print(f"\n{'='*60}")
    print("Pre-flight Checks")
    print(f"{'='*60}")

    ok = True
    for key in ["OPENROUTER_API_KEY"]:
        val = os.getenv(key)
        status = "OK" if val else "MISSING"
        print(f"  {key}: {status}")
        if not val:
            ok = False

    if not TEST_CASES_FILE.exists():
        print(f"  test_cases_ab24.json: MISSING ({TEST_CASES_FILE})")
        return False
    cases = json.loads(TEST_CASES_FILE.read_text())
    print(f"  test_cases_ab24.json: {len(cases)} cases loaded")

    print(f"\n  Testing judge model: {judge_model}")
    try:
        from agents.core.llm_client import LLMClient
        llm = LLMClient(debug=False)
        llm.models["planner"] = judge_model
        resp = llm.ask("Reply in JSON.", '{"ok": true}', role="planner", json_mode=True, temperature=0.0)
        resp_clean = re.sub(r"```json\s*|\s*```", "", resp).strip()
        m = re.search(r"\{.*\}", resp_clean, re.DOTALL)
        if m:
            resp_clean = m.group(0)
        json.loads(resp_clean)
        print(f"  Judge OK")
        llm.close()
    except Exception as e:
        print(f"  Judge FAILED: {e}")
        return False

    print(f"\n  Testing contestant models:")
    for c in contestants:
        print(f"    {c['id']:8s} ({c['model']})", end="  ", flush=True)
        try:
            os.environ["PLANNER_MODEL"] = c["model"]
            from agents.core.llm_client import LLMClient
            llm = LLMClient(debug=False)
            llm.models["planner"] = c["model"]
            t0 = time.time()
            resp = llm.ask("You output JSON.", '{"ok": true}', role="planner")
            dt = time.time() - t0
            print(f"OK ({dt:.1f}s)")
            llm.close()
        except Exception as e:
            print(f"FAILED: {str(e)[:60]}")
            ok = False

    return ok


# ────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot",        action="store_true", help="Phase 0: 5-topic pilot")
    parser.add_argument("--full",         action="store_true", help="Phase 1: all 24 topics")
    parser.add_argument("--cross-check",  action="store_true", help="Phase 2: secondary judge")
    parser.add_argument("--report",       action="store_true", help="Regenerate report only")
    parser.add_argument("--resume",       type=str,            help="Resume session by timestamp")
    parser.add_argument("--difficulty",   type=str,            help="Filter: elem|mid|high")
    parser.add_argument("--skip-preflight", action="store_true")
    parser.add_argument("--judge",        type=str,            default=JUDGE_MODEL_PRIMARY)
    args = parser.parse_args()

    cases = json.loads(TEST_CASES_FILE.read_text())

    if args.resume:
        session_dir = RUNS_ROOT / args.resume
        if not session_dir.exists():
            print(f"Resume dir not found: {session_dir}")
            sys.exit(1)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = RUNS_ROOT / f"ab_{ts}"

    session = ABSession(session_dir)
    print(f"Session: {session_dir}")

    judge_model = args.judge

    if args.report:
        _generate_report(session, cases)
        return

    if not args.skip_preflight:
        if not preflight(CONTESTANTS, judge_model):
            print("\nPre-flight failed. Use --skip-preflight to bypass.")
            sys.exit(1)

    if args.pilot:
        run_pilot(session, cases, judge_model)
    elif args.full:
        run_full(session, cases, judge_model, difficulty_filter=args.difficulty)
    elif args.cross_check:
        run_crosscheck(session, cases)
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Resume with: python run_planner_ab.py --full --resume <timestamp>")
        sys.exit(130)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
