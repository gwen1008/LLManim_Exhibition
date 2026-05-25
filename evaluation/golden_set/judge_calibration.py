"""
FinalJudge Calibration — measure agreement between FJ scores and human labels.

Phase A diagnostic:
  - Loads evaluation/golden_set/labels.json (16+ entries with human_scores per dim)
  - Re-runs FinalJudge.judge() on each video
  - Computes per-dimension: Spearman ρ, Pearson r, MAE, variance, saturation rate
  - Computes binary verdict agreement: Cohen's kappa, accuracy, FP/FN

Usage:
  python evaluation/golden_set/judge_calibration.py
  python evaluation/golden_set/judge_calibration.py --limit 3     # smoke test on 3 videos
  python evaluation/golden_set/judge_calibration.py --skip-fj     # use cached scores in raw_results.json

Outputs:
  - evaluation/golden_set/raw_results.json    (FJ raw output per video)
  - evaluation/golden_set/calibration_report.md
"""
import argparse
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from agents.utils.final_judge import FinalJudge  # noqa: E402
from agents.core.llm_client import LLMClient    # noqa: E402

LABELS_PATH = Path(__file__).parent / "labels.json"
RAW_PATH    = Path(__file__).parent / "raw_results.json"
REPORT_PATH = Path(__file__).parent / "calibration_report.md"

# Map FJ dimension → human label key
FJ_TO_HUMAN = {
    "math_correctness":   "math",
    "concept_alignment":  "concept",
    "visual_clarity":     "clarity",
    "spatial_layout":     None,  # no direct human counterpart; compare to overall
}


# ── stdlib stats (avoid scipy dependency) ────────────────────────────────────

def _rankdata(xs):
    """Average-rank tie handling, matches scipy.stats.rankdata default."""
    n = len(xs)
    pairs = sorted(enumerate(xs), key=lambda p: p[1])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and pairs[j + 1][1] == pairs[i][1]:
            j += 1
        avg = (i + j) / 2 + 1  # ranks are 1-indexed
        for k in range(i, j + 1):
            ranks[pairs[k][0]] = avg
        i = j + 1
    return ranks


def _pearson(xs, ys):
    if len(xs) < 2:
        return None
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def _spearman(xs, ys):
    if len(xs) < 2:
        return None
    return _pearson(_rankdata(xs), _rankdata(ys))


def _mae(xs, ys):
    if not xs:
        return None
    return sum(abs(x - y) for x, y in zip(xs, ys)) / len(xs)


def _variance(xs):
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def _saturation_rate(xs, ceiling=5):
    if not xs:
        return None
    return sum(1 for x in xs if x is not None and x >= ceiling) / len(xs)


def _cohens_kappa(matrix):
    tp, tn, fp, fn = matrix["TP"], matrix["TN"], matrix["FP"], matrix["FN"]
    n = tp + tn + fp + fn
    if n == 0:
        return 0.0
    po = (tp + tn) / n
    p_pass_h = (tp + fn) / n
    p_pass_f = (tp + fp) / n
    pe = p_pass_h * p_pass_f + (1 - p_pass_h) * (1 - p_pass_f)
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


# ── data IO ──────────────────────────────────────────────────────────────────

def _resolve(p):
    if not p:
        return None
    pp = Path(p)
    if not pp.is_absolute():
        pp = ROOT / pp
    return str(pp)


def _load_labels():
    if not LABELS_PATH.exists():
        print(f"❌ Labels file not found: {LABELS_PATH}")
        sys.exit(1)
    with open(LABELS_PATH, encoding="utf-8") as f:
        return json.load(f)


def _run_fj(labels, limit=None):
    """Run FJ on each label, persist raw results."""
    llm = LLMClient()
    fj = FinalJudge(llm_client=llm)
    results = []
    todo = labels[:limit] if limit else labels

    for i, entry in enumerate(todo, 1):
        cid = entry["id"]
        video = _resolve(entry["video_path"])
        code_path = _resolve(entry["code_path"])
        ssl = _resolve(entry.get("scene_state_log_path"))

        if not video or not Path(video).exists():
            print(f"⚠️  [{cid}] video missing: {video}")
            results.append({"id": cid, "error": f"video missing: {video}"})
            continue
        if not code_path or not Path(code_path).exists():
            print(f"⚠️  [{cid}] code missing: {code_path}")
            results.append({"id": cid, "error": f"code missing: {code_path}"})
            continue

        code = Path(code_path).read_text(encoding="utf-8")
        topic = entry.get("topic", "")
        gt = entry.get("ground_truth")

        print(f"\n{'─'*60}\n🎬 [{i}/{len(todo)}] {cid}")
        try:
            result = fj.judge(
                video, topic, code,
                ground_truth=gt,
                scene_state_log_path=ssl,
            )
        except Exception as e:
            print(f"❌ [{cid}] FJ crashed: {e}")
            results.append({"id": cid, "error": str(e)})
            continue

        results.append({"id": cid, "fj_result": result})

    with open(RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n💾 Raw results saved: {RAW_PATH}")
    return results


def _load_cached():
    if not RAW_PATH.exists():
        print(f"❌ No cache at {RAW_PATH}; remove --skip-fj or run without it first.")
        sys.exit(1)
    with open(RAW_PATH, encoding="utf-8") as f:
        return json.load(f)


def _rerun_layout_only(labels, cached_results):
    """Replay LayoutAuditor on each entry, replacing only the spatial_layout
    score + layout_audit block in cached FJ results. Re-aggregates weighted_total
    and verdict accordingly. Useful when the LLM calls are expensive but the
    deterministic auditor logic has changed."""
    from agents.utils.layout_auditor import LayoutAuditor
    from agents.utils.final_judge import FinalJudge

    auditor = LayoutAuditor()
    fj = FinalJudge.__new__(FinalJudge)  # bypass __init__ (no LLM client needed)
    by_id = {r["id"]: r for r in cached_results}

    for label in labels:
        cid = label["id"]
        r = by_id.get(cid)
        if not r or "fj_result" not in r:
            continue
        ssl = label.get("scene_state_log_path")
        if not ssl:
            continue
        ssl_path = _resolve(ssl)
        if not Path(ssl_path).exists():
            continue

        audit = auditor.audit(ssl_path)
        fj_res = r["fj_result"]
        scores = fj_res.get("scores", {})
        # Coerce strings ("None") back to actual None so aggregator skips them.
        for k, v in list(scores.items()):
            if isinstance(v, str) and v.lower() == "none":
                scores[k] = None
        scores["spatial_layout"] = audit.get("score_1_to_5")

        # Re-aggregate weighted_total with same WEIGHTS logic.
        available = {d: scores[d] for d in FinalJudge.WEIGHTS if scores.get(d) is not None}
        if available:
            tw = sum(FinalJudge.WEIGHTS[d] for d in available)
            new_weighted = round(sum(scores[d] * FinalJudge.WEIGHTS[d] / tw for d in available), 3)
        else:
            new_weighted = None
        fj_res["weighted_total"] = new_weighted
        # Update layout_audit block too.
        fj_res["layout_audit"] = {
            "verdict":    audit.get("verdict"),
            "score":      audit.get("score_1_to_5"),
            "metrics":    audit.get("metrics", {}),
            "violations": audit.get("violations", []),
            "metric_source": audit.get("metric_source"),
        }

        # Re-evaluate verdict using FJ's own logic (manual replay).
        # Only critical-issue + GT-mismatch + dim-floor + threshold matter.
        veto = None
        verdict = "PASS"
        critical = any(
            str(iss.get("severity", "")).lower() == "critical"
            for iss in fj_res.get("code_issues", [])
        )
        if critical:
            verdict, veto = "FAIL", "critical_code_issue"
        elif fj_res.get("ground_truth_match") is False:
            verdict, veto = "FAIL", "ground_truth_mismatch"
        elif scores.get("concept_alignment") is None and scores.get("visual_clarity") is None:
            verdict, veto = "ERROR", "visual_api_failure"
        elif scores.get("math_correctness") is None and new_weighted is None:
            verdict, veto = "ERROR", "all_phases_failed"
        else:
            for dim, val in scores.items():
                if val is not None and val <= FinalJudge.DIMENSION_FLOOR:
                    verdict, veto = "FAIL", f"low_dimension_{dim}"
                    break
            else:
                if new_weighted is None or new_weighted < FinalJudge.PASS_THRESHOLD:
                    verdict, veto = "FAIL", "below_threshold"
        fj_res["verdict"] = verdict
        fj_res["veto_reason"] = veto

    # Save the patched cache so subsequent --skip-fj sees the new layout.
    with open(RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(cached_results, f, ensure_ascii=False, indent=2, default=str)
    print(f"🔁 Replayed LayoutAuditor; cache updated: {RAW_PATH}")
    return cached_results


# ── diagnostics ──────────────────────────────────────────────────────────────

def _diagnose(labels, results):
    by_id = {r["id"]: r for r in results}

    paired = []
    for label in labels:
        cid = label["id"]
        r = by_id.get(cid)
        if not r or "fj_result" in r and r["fj_result"] is None:
            continue
        if "error" in r:
            continue
        fj = r["fj_result"]
        paired.append({
            "id": cid,
            "label": label,
            "fj_scores": fj.get("scores", {}),
            "fj_weighted": fj.get("weighted_total"),
            "fj_verdict": fj.get("verdict"),
            "fj_veto": fj.get("veto_reason"),
        })

    if not paired:
        print("❌ No valid paired results.")
        return None

    # ── per-dimension stats ─────────────────────────────────────────────────
    dim_stats = {}
    for fj_dim, human_key in FJ_TO_HUMAN.items():
        fj_vals = []
        human_vals = []
        for p in paired:
            fj_v = p["fj_scores"].get(fj_dim)
            if fj_v is None:
                continue
            if human_key is None:
                # spatial_layout: compare to human overall
                h = p["label"]["human_scores"].get("overall")
            else:
                h = p["label"]["human_scores"].get(human_key)
            if h is None:
                continue
            fj_vals.append(fj_v)
            human_vals.append(h)

        if len(fj_vals) < 2:
            dim_stats[fj_dim] = {"n": len(fj_vals), "note": "insufficient data"}
            continue

        dim_stats[fj_dim] = {
            "n":          len(fj_vals),
            "spearman":   _spearman(fj_vals, human_vals),
            "pearson":    _pearson(fj_vals, human_vals),
            "mae":        _mae(fj_vals, human_vals),
            "fj_variance":  _variance(fj_vals),
            "human_variance": _variance(human_vals),
            "fj_saturation":  _saturation_rate(fj_vals),
            "human_saturation": _saturation_rate(human_vals),
            "fj_values":   fj_vals,
            "human_values": human_vals,
        }

    # ── verdict agreement (binary PASS/FAIL kappa) ──────────────────────────
    matrix = {"TP": 0, "TN": 0, "FP": 0, "FN": 0, "ERR": 0}
    verdict_rows = []
    for p in paired:
        exp = p["label"]["expected_verdict"]
        act = p["fj_verdict"]
        if act == "ERROR":
            matrix["ERR"] += 1
            outcome = "ERROR"
        elif act == exp == "PASS":
            matrix["TP"] += 1; outcome = "TP"
        elif act == exp == "FAIL":
            matrix["TN"] += 1; outcome = "TN"
        elif act == "PASS" and exp == "FAIL":
            matrix["FP"] += 1; outcome = "FP"
        elif act == "FAIL" and exp == "PASS":
            matrix["FN"] += 1; outcome = "FN"
        else:
            outcome = "?"
        verdict_rows.append({
            "id": p["id"],
            "expected": exp,
            "actual": act,
            "weighted": p["fj_weighted"],
            "veto": p["fj_veto"],
            "outcome": outcome,
        })

    n_kappa = sum(matrix[k] for k in ("TP", "TN", "FP", "FN"))
    accuracy = (matrix["TP"] + matrix["TN"]) / n_kappa if n_kappa else 0
    kappa = _cohens_kappa(matrix) if n_kappa else 0.0

    # ── overall weighted_total correlation ─────────────────────────────────
    overall_fj = []
    overall_human = []
    for p in paired:
        if p["fj_weighted"] is not None:
            overall_fj.append(float(p["fj_weighted"]))
            overall_human.append(p["label"]["human_scores"]["overall"])

    overall_stats = {
        "n": len(overall_fj),
        "spearman": _spearman(overall_fj, overall_human) if len(overall_fj) >= 2 else None,
        "pearson":  _pearson(overall_fj, overall_human) if len(overall_fj) >= 2 else None,
    }

    return {
        "paired_n": len(paired),
        "dim_stats": dim_stats,
        "verdict_matrix": matrix,
        "verdict_rows": verdict_rows,
        "verdict_kappa": kappa,
        "verdict_accuracy": accuracy,
        "overall_stats": overall_stats,
    }


# ── report ───────────────────────────────────────────────────────────────────

def _fmt(v, prec=3):
    if v is None:
        return "—"
    if isinstance(v, (int, float)):
        return f"{v:.{prec}f}"
    return str(v)


def _write_report(diag):
    lines = []
    lines.append("# FinalJudge Calibration Report — Phase A Baseline\n")
    lines.append(f"**Sample size**: n = {diag['paired_n']}\n")

    lines.append("\n## Per-Dimension Stats (FJ vs Human)\n")
    lines.append("| Dimension | n | Spearman ρ | Pearson r | MAE | FJ var | Human var | FJ sat | Human sat |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for dim, s in diag["dim_stats"].items():
        if "note" in s:
            lines.append(f"| {dim} | {s['n']} | — | — | — | — | — | — | — |  *{s['note']}* |")
            continue
        lines.append(
            f"| {dim} | {s['n']} | {_fmt(s['spearman'])} | {_fmt(s['pearson'])} | "
            f"{_fmt(s['mae'])} | {_fmt(s['fj_variance'])} | {_fmt(s['human_variance'])} | "
            f"{_fmt(s['fj_saturation'])} | {_fmt(s['human_saturation'])} |"
        )

    lines.append("\n## Overall (weighted_total vs human overall)\n")
    o = diag["overall_stats"]
    lines.append(f"- n: {o['n']}")
    lines.append(f"- Spearman ρ: {_fmt(o['spearman'])}")
    lines.append(f"- Pearson r:  {_fmt(o['pearson'])}")

    lines.append("\n## Binary Verdict Agreement (PASS/FAIL)\n")
    m = diag["verdict_matrix"]
    lines.append(f"- TP={m['TP']}  TN={m['TN']}  FP={m['FP']}  FN={m['FN']}  ERROR={m['ERR']}")
    lines.append(f"- Accuracy: {_fmt(diag['verdict_accuracy'])}")
    lines.append(f"- Cohen's kappa: {_fmt(diag['verdict_kappa'])}")

    lines.append("\n## Per-Video Detail\n")
    lines.append("| ID | Expected | Actual | Weighted | Veto | Outcome |")
    lines.append("|---|---|---|---|---|---|")
    for r in diag["verdict_rows"]:
        veto = r["veto"] or ""
        lines.append(f"| {r['id']} | {r['expected']} | {r['actual']} | {_fmt(r['weighted'])} | {veto} | {r['outcome']} |")

    lines.append("\n## Diagnosis Hints\n")
    hints = []
    for dim, s in diag["dim_stats"].items():
        if "note" in s:
            continue
        rho = s.get("spearman")
        sat = s.get("fj_saturation")
        if rho is not None and rho < 0.3:
            hints.append(f"- ⚠️  **{dim}**: ρ={rho:.2f} (low) — 排序與人類差很多，這維可能要重做")
        if sat is not None and sat >= 0.5:
            hints.append(f"- ⚠️  **{dim}**: saturation={sat:.2%} — FJ 太常打滿分，缺鑑別力（B1 主要解這個）")
        if s.get("fj_variance", 0) < 0.5:
            hints.append(f"- ⚠️  **{dim}**: FJ variance={s['fj_variance']:.2f} — FJ 對所有影片打差不多分數")
    if not hints:
        hints.append("- 所有維度看起來都 OK；可能是 weighted aggregation 出問題，看 overall ρ")
    lines.extend(hints)

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n📄 Report written: {REPORT_PATH}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="Only run first N labels (smoke test)")
    ap.add_argument("--skip-fj", action="store_true", help="Use cached raw_results.json instead of re-running FJ")
    ap.add_argument("--rerun-layout", action="store_true",
                    help="Reuse cached FJ Phase1/2 results but re-run LayoutAuditor and re-aggregate")
    args = ap.parse_args()

    labels = _load_labels()
    print(f"📋 Loaded {len(labels)} labels")

    if args.rerun_layout:
        results = _load_cached()
        print(f"📂 Loaded {len(results)} cached FJ results — replaying LayoutAuditor only")
        results = _rerun_layout_only(labels, results)
    elif args.skip_fj:
        results = _load_cached()
        print(f"📂 Using cached {len(results)} FJ results")
    else:
        results = _run_fj(labels, limit=args.limit)

    diag = _diagnose(labels, results)
    if diag is None:
        sys.exit(1)

    # Console summary
    print("\n" + "═" * 70)
    print(f"  Phase A Calibration — n = {diag['paired_n']}")
    print("═" * 70)
    for dim, s in diag["dim_stats"].items():
        if "note" in s:
            print(f"  {dim:<22} insufficient data")
            continue
        print(
            f"  {dim:<22} ρ={_fmt(s['spearman'])}  r={_fmt(s['pearson'])}  "
            f"MAE={_fmt(s['mae'])}  sat={_fmt(s['fj_saturation'], 2)}  var={_fmt(s['fj_variance'], 2)}"
        )
    o = diag["overall_stats"]
    print(f"  {'OVERALL (weighted)':<22} ρ={_fmt(o['spearman'])}  r={_fmt(o['pearson'])}")
    print(f"  verdict kappa = {_fmt(diag['verdict_kappa'])}  accuracy = {_fmt(diag['verdict_accuracy'])}")
    print("═" * 70)

    _write_report(diag)


if __name__ == "__main__":
    main()
