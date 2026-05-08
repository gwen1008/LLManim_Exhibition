"""
FinalJudge Calibration — measure agreement between FJ verdicts and human labels.

Workflow:
  1. You hand-label 10-15 videos in evaluation/golden_set/labels.json
     (see labels.example.json for schema).
  2. Run: python evaluation/golden_set/judge_calibration.py
  3. Inspect confusion matrix + Cohen's kappa.
     - kappa >= 0.6  → substantial agreement (good)
     - kappa < 0.4   → tweak FinalJudge.PASS_THRESHOLD / DIMENSION_FLOOR

Tweak strategy:
  - High false-positive (FJ says PASS, human says FAIL): raise PASS_THRESHOLD or
    add stricter prompts in _CODE_REVIEW_SYSTEM.
  - High false-negative (FJ says FAIL, human says PASS): lower PASS_THRESHOLD,
    or relax DIMENSION_FLOOR from 2 to 1.

Each calibration run adds ~$0.05 × N to OpenRouter/OpenAI bill.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from agents.utils.final_judge import FinalJudge  # noqa: E402
from agents.core.llm_client import LLMClient    # noqa: E402

LABELS_PATH = Path(__file__).parent / "labels.json"


def _load_labels() -> list[dict]:
    if not LABELS_PATH.exists():
        print(f"❌ Labels file not found: {LABELS_PATH}")
        print(f"   Copy labels.example.json → labels.json and fill in real entries.")
        sys.exit(1)
    with open(LABELS_PATH, encoding="utf-8") as f:
        return json.load(f)


def _read_code(code_path: str) -> str:
    p = Path(code_path)
    if not p.is_absolute():
        p = ROOT / code_path
    return p.read_text(encoding="utf-8")


def _resolve_video(video_path: str) -> str:
    p = Path(video_path)
    if not p.is_absolute():
        p = ROOT / video_path
    return str(p)


def _cohens_kappa(matrix: dict) -> float:
    """Cohen's kappa for 2 raters × 2 categories (PASS/FAIL).
    Treat ERROR as separate category (excluded from kappa)."""
    tp = matrix["TP"]
    tn = matrix["TN"]
    fp = matrix["FP"]
    fn = matrix["FN"]
    n = tp + tn + fp + fn
    if n == 0:
        return 0.0
    po = (tp + tn) / n
    p_pass_human = (tp + fn) / n
    p_pass_fj    = (tp + fp) / n
    pe = p_pass_human * p_pass_fj + (1 - p_pass_human) * (1 - p_pass_fj)
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


def main():
    labels = _load_labels()
    print(f"📋 Loaded {len(labels)} golden labels from {LABELS_PATH}")

    llm = LLMClient()
    fj = FinalJudge(llm_client=llm)

    matrix = {"TP": 0, "TN": 0, "FP": 0, "FN": 0, "ERR": 0}
    rows = []

    for entry in labels:
        cid = entry["id"]
        video = _resolve_video(entry["video_path"])
        try:
            code = _read_code(entry["code_path"])
        except FileNotFoundError as e:
            print(f"⚠️  [{cid}] code missing: {e}")
            continue

        if not Path(video).exists():
            print(f"⚠️  [{cid}] video missing: {video}")
            continue

        topic = entry.get("topic", "")
        gt = entry.get("ground_truth")
        expected = entry["expected_verdict"]

        print(f"\n{'─'*60}\n🎬 [{cid}] Running FJ — expected={expected}")
        result = fj.judge(video, topic, code, ground_truth=gt)
        actual = result.get("verdict", "ERROR")

        # Categorize
        if actual == "ERROR":
            matrix["ERR"] += 1
            outcome = "⚪ ERROR"
        elif actual == expected == "PASS":
            matrix["TP"] += 1; outcome = "✅ TP"
        elif actual == expected == "FAIL":
            matrix["TN"] += 1; outcome = "✅ TN"
        elif actual == "PASS" and expected == "FAIL":
            matrix["FP"] += 1; outcome = "❌ FP (false PASS)"
        elif actual == "FAIL" and expected == "PASS":
            matrix["FN"] += 1; outcome = "❌ FN (false FAIL)"
        else:
            outcome = "?"

        rows.append({
            "id": cid,
            "expected": expected,
            "actual": actual,
            "weighted": result.get("weighted_total"),
            "veto": result.get("veto_reason") or "",
            "outcome": outcome,
        })
        print(f"   → actual={actual} weighted={result.get('weighted_total')} {outcome}")

    # ── Report ──────────────────────────────────────────────────────────────
    print("\n" + "═"*70)
    print("  Calibration Report")
    print("═"*70)
    print(f"{'Case':<8}{'Expected':<10}{'Actual':<10}{'Weighted':<10}{'Outcome':<22}{'Veto':<20}")
    print("─"*70)
    for r in rows:
        print(f"{r['id']:<8}{r['expected']:<10}{r['actual']:<10}{str(r['weighted']):<10}{r['outcome']:<22}{r['veto']:<20}")

    print("\n" + "─"*70)
    n_total = sum(matrix[k] for k in ("TP", "TN", "FP", "FN"))
    n_with_err = n_total + matrix["ERR"]
    print(f"  Total labeled: {n_with_err}  (ERROR excluded from kappa: {matrix['ERR']})")
    print(f"  TP={matrix['TP']}  TN={matrix['TN']}  FP={matrix['FP']}  FN={matrix['FN']}")
    if n_total > 0:
        accuracy = (matrix['TP'] + matrix['TN']) / n_total
        kappa = _cohens_kappa(matrix)
        print(f"  Accuracy: {accuracy:.2%}")
        print(f"  Cohen's kappa: {kappa:.3f}  ", end="")
        if kappa >= 0.8:
            print("(almost perfect)")
        elif kappa >= 0.6:
            print("(substantial — good)")
        elif kappa >= 0.4:
            print("(moderate — needs tuning)")
        else:
            print("(poor — review prompts/thresholds)")

    print("═"*70)


if __name__ == "__main__":
    main()
