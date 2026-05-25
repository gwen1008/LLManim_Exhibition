"""
BenchmarkJudge Calibration — measure agreement between BJ final_100 and human labels.

Mirrors evaluation/golden_set/judge_calibration.py, but:
  - Reads evaluation/golden_set/benchmark_labels.json
    (each entry pairs a CANDIDATE with a BENCHMARK + human's gold final_100)
  - Uses BenchmarkJudge.judge() instead of FinalJudge.judge()
  - Persists raw_results to evaluation/golden_set/benchmark_raw_results.json
  - Uses BJ pair-cache (evaluation/golden_set/benchmark_judge_cache.json) so
    repeated runs skip the Opus 3-pass loop

Usage:
  python evaluation/benchmark_calibration.py                    # full
  python evaluation/benchmark_calibration.py --limit 3          # smoke
  python evaluation/benchmark_calibration.py --skip-bj          # use raw cache only
  python evaluation/benchmark_calibration.py --force            # ignore pair cache

Labels schema (per entry):
{
  "id": "BV01_Q050",
  "candidate_video": "runs/.../Q050/video.mp4",
  "benchmark_video": "evaluation/benchmark_set/Q050/benchmark.mp4",
  "candidate_code":   "runs/.../Q050/code.py",                 // optional
  "candidate_state_log": "runs/.../Q050/scene_state_log.json", // optional
  "benchmark_state_log": null,                                  // optional
  "topic": "計算 (-48) ÷ (-6) × (-3) 的值。",
  "ground_truth": {"answer": "-24"},
  "human_final_100": 90,
  "human_dim": {"completeness": 95, "accuracy": 100, "clarity": 85},   // optional
  "notes": "candidate ~ benchmark, minor clarity gap"
}
"""
import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.utils.benchmark_judge import BenchmarkJudge   # noqa: E402
from agents.core.llm_client import LLMClient              # noqa: E402


# ── A: precomputed math_score loader ─────────────────────────────────────────
# Each per-question run dir (runs/<session>/<qid>/) carries a cost_report.json
# with final_judge.scores.math_correctness (1–5). If we pass that into
# BenchmarkJudge as precomputed_math_score we skip an 8s Opus Phase-1 per call.

def _load_precomputed_math_score(candidate_video_or_dir) -> int | None:
    """Find cost_report.json next to the candidate and return its
    final_judge.scores.math_correctness (1-5), or None if unavailable.

    Accepts either the video path or the qid directory; we walk up to find a
    sibling cost_report.json.
    """
    if not candidate_video_or_dir:
        return None
    p = Path(candidate_video_or_dir)
    qid_dir = p if p.is_dir() else p.parent
    cost_report = qid_dir / "cost_report.json"
    if not cost_report.exists():
        return None
    try:
        with open(cost_report, encoding="utf-8") as f:
            blob = json.load(f)
        score = (blob.get("final_judge") or {}).get("scores", {}).get("math_correctness")
        if isinstance(score, (int, float)):
            return int(score)
    except (json.JSONDecodeError, OSError, AttributeError):
        pass
    return None

LABELS_PATH = ROOT / "evaluation" / "golden_set" / "benchmark_labels.json"
RAW_PATH    = ROOT / "evaluation" / "golden_set" / "benchmark_raw_results.json"
REPORT_PATH = ROOT / "evaluation" / "golden_set" / "benchmark_calibration_report.md"
CACHE_PATH  = ROOT / "evaluation" / "golden_set" / "benchmark_judge_cache.json"


# ── stats (stdlib, mirror judge_calibration.py to avoid scipy) ────────────────

def _rankdata(xs):
    n = len(xs)
    pairs = sorted(enumerate(xs), key=lambda p: p[1])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and pairs[j + 1][1] == pairs[i][1]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[pairs[k][0]] = avg
        i = j + 1
    return ranks


def _pearson(xs, ys):
    if len(xs) < 2:
        return None
    mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x-mx)**2 for x in xs))
    dy = math.sqrt(sum((y-my)**2 for y in ys))
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


# ── data IO ──────────────────────────────────────────────────────────────────

def _resolve(p):
    if not p:
        return None
    pp = Path(p)
    return str(pp if pp.is_absolute() else ROOT / pp)


def _load_labels():
    if not LABELS_PATH.exists():
        print(f"❌ Labels file not found: {LABELS_PATH}")
        print("   Create it from the schema in this script's docstring.")
        sys.exit(1)
    with open(LABELS_PATH, encoding="utf-8") as f:
        return json.load(f)


def _run_bj(labels, limit=None, force=False, cache_path=None):
    llm = LLMClient()
    bj = BenchmarkJudge(llm_client=llm)
    results = []
    todo = labels[:limit] if limit else labels

    for i, entry in enumerate(todo, 1):
        cid = entry["id"]
        cand_v = _resolve(entry.get("candidate_video"))
        bench_v = _resolve(entry.get("benchmark_video"))
        if not (cand_v and bench_v and Path(cand_v).exists() and Path(bench_v).exists()):
            print(f"⚠️  [{cid}] missing video — cand={cand_v} bench={bench_v}")
            results.append({"id": cid, "error": "missing video"})
            continue

        code_path = _resolve(entry.get("candidate_code"))
        code_str = Path(code_path).read_text(encoding="utf-8") if code_path and Path(code_path).exists() else None
        cand_ssl = _resolve(entry.get("candidate_state_log"))
        bench_ssl = _resolve(entry.get("benchmark_state_log"))
        topic = entry.get("topic", "")
        gt = entry.get("ground_truth")

        # A: try to skip BJ's own 8s Phase-1 by reading cached FJ math score
        precomp = entry.get("precomputed_math_score")
        if precomp is None:
            precomp = _load_precomputed_math_score(cand_v)
            if precomp is not None:
                print(f"  ↳ found cached FJ math_correctness={precomp} in sibling cost_report.json")

        print(f"\n{'─'*60}\n🎬 [{i}/{len(todo)}] {cid}")
        try:
            res = bj.judge(
                cand_v, bench_v, topic,
                candidate_code=code_str,
                candidate_state_log=cand_ssl,
                benchmark_state_log=bench_ssl,
                ground_truth=gt,
                cache_path=cache_path,
                force=force,
                precomputed_math_score=precomp,
            )
        except Exception as e:
            print(f"❌ [{cid}] BJ crashed: {e}")
            results.append({"id": cid, "error": str(e)})
            continue
        results.append({"id": cid, "bj_result": res})

    with open(RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n💾 Raw results saved: {RAW_PATH}")
    return results


def _load_cached():
    if not RAW_PATH.exists():
        print(f"❌ No cache at {RAW_PATH}")
        sys.exit(1)
    with open(RAW_PATH, encoding="utf-8") as f:
        return json.load(f)


# ── diagnostics ──────────────────────────────────────────────────────────────

DIM_KEYS = ("completeness", "accuracy", "clarity")


def _diagnose(labels, results):
    by_id = {r["id"]: r for r in results}

    # B: count outcomes so the report can surface insufficient_passes rather
    # than silently dropping them like a normal missing entry.
    n_insufficient = 0
    n_error = 0

    paired = []
    for label in labels:
        cid = label["id"]
        r = by_id.get(cid)
        if not r:
            continue
        if "error" in r:
            n_error += 1
            continue
        if "bj_result" not in r:
            continue
        bj = r["bj_result"]
        # Skip BJ runs that returned the insufficient_passes guard — final_100
        # is None and would crash _spearman / _mae. Track separately so the
        # report makes the dropped count visible.
        if bj.get("status") == "insufficient_passes" or bj.get("final_100") is None:
            n_insufficient += 1
            continue
        paired.append({
            "id":       cid,
            "label":    label,
            "bj_final": bj.get("final_100"),
            "bj_dim":   bj.get("scores", {}),
            "bj_modes": bj.get("modes", {}),
        })

    if not paired:
        print("❌ No valid paired results.")
        return None

    # overall final_100 vs human_final_100
    bj_finals = [p["bj_final"] for p in paired if p["bj_final"] is not None
                 and p["label"].get("human_final_100") is not None]
    human_finals = [p["label"]["human_final_100"] for p in paired
                    if p["bj_final"] is not None
                    and p["label"].get("human_final_100") is not None]

    overall = {
        "n":        len(bj_finals),
        "spearman": _spearman(bj_finals, human_finals) if len(bj_finals) >= 2 else None,
        "pearson":  _pearson(bj_finals, human_finals)  if len(bj_finals) >= 2 else None,
        "mae":      _mae(bj_finals, human_finals),
        "bj_variance":    _variance(bj_finals),
        "human_variance": _variance(human_finals),
        "bj_values":    bj_finals,
        "human_values": human_finals,
    }

    # per-dim (only entries that supplied human_dim)
    dim_stats = {}
    for dim in DIM_KEYS:
        bj_vs, hu_vs = [], []
        for p in paired:
            bv = p["bj_dim"].get(dim)
            hv = (p["label"].get("human_dim") or {}).get(dim)
            if bv is None or hv is None:
                continue
            bj_vs.append(bv)
            hu_vs.append(hv)
        if len(bj_vs) < 2:
            dim_stats[dim] = {"n": len(bj_vs), "note": "insufficient data"}
            continue
        dim_stats[dim] = {
            "n":          len(bj_vs),
            "spearman":   _spearman(bj_vs, hu_vs),
            "pearson":    _pearson(bj_vs, hu_vs),
            "mae":        _mae(bj_vs, hu_vs),
            "bj_variance":    _variance(bj_vs),
            "human_variance": _variance(hu_vs),
            "bj_values":   bj_vs,
            "human_values": hu_vs,
        }

    rows = []
    for p in paired:
        rows.append({
            "id":     p["id"],
            "bj":     p["bj_final"],
            "human":  p["label"].get("human_final_100"),
            "modes":  p["bj_modes"],
            "notes":  p["label"].get("notes", ""),
        })

    return {
        "paired_n":   len(paired),
        "n_insufficient": n_insufficient,
        "n_error":    n_error,
        "overall":    overall,
        "dim_stats":  dim_stats,
        "rows":       rows,
    }


# ── report ───────────────────────────────────────────────────────────────────

def _fmt(v, prec=3):
    if v is None:
        return "—"
    if isinstance(v, (int, float)):
        return f"{v:.{prec}f}"
    return str(v)


def _write_report(diag):
    o = diag["overall"]
    lines = [
        "# BenchmarkJudge Calibration Report\n",
        f"**Sample size**: n = {diag['paired_n']}  "
        f"(dropped: {diag.get('n_insufficient', 0)} insufficient_passes, "
        f"{diag.get('n_error', 0)} errored)\n",
        "\n## Overall (BJ final_100 vs human_final_100)\n",
        f"- n: {o['n']}",
        f"- Spearman ρ: {_fmt(o['spearman'])}",
        f"- Pearson r:  {_fmt(o['pearson'])}",
        f"- MAE: {_fmt(o['mae'])}",
        f"- BJ variance: {_fmt(o['bj_variance'])}   Human variance: {_fmt(o['human_variance'])}",
    ]

    lines.append("\n## Per-Dimension (where human_dim provided)\n")
    lines.append("| Dim | n | ρ | r | MAE | BJ var | Human var |")
    lines.append("|---|---|---|---|---|---|---|")
    for dim, s in diag["dim_stats"].items():
        if "note" in s:
            lines.append(f"| {dim} | {s['n']} | — | — | — | — | — *{s['note']}* |")
            continue
        lines.append(f"| {dim} | {s['n']} | {_fmt(s['spearman'])} | {_fmt(s['pearson'])} | "
                     f"{_fmt(s['mae'])} | {_fmt(s['bj_variance'])} | {_fmt(s['human_variance'])} |")

    lines.append("\n## Per-Video\n")
    lines.append("| ID | BJ | Human | Δ | comp/acc/clar mode | Notes |")
    lines.append("|---|---|---|---|---|---|")
    for r in diag["rows"]:
        delta = (r["bj"] - r["human"]) if (r["bj"] is not None and r["human"] is not None) else None
        modes = r["modes"]
        modeline = f"{modes.get('completeness','-')}/{modes.get('accuracy','-')}/{modes.get('clarity','-')}"
        lines.append(f"| {r['id']} | {r['bj']} | {r['human']} | {_fmt(delta, 1)} | {modeline} | {r['notes']} |")

    lines.append("\n## Hints\n")
    hints = []
    if o["spearman"] is not None and o["spearman"] < 0.4:
        hints.append(f"- ⚠️  overall ρ={o['spearman']:.2f} (low) — BJ 排序與人類差距大；檢查 Likert anchor prompt")
    if o["mae"] is not None and o["mae"] > 20:
        hints.append(f"- ⚠️  MAE={o['mae']:.1f} > 20 — 偏離過大；考慮調 LIKERT_OFFSET 或 accuracy_gate")
    if o["bj_variance"] < 100:
        hints.append(f"- ⚠️  BJ variance={o['bj_variance']:.1f} (低) — 鑑別力不足")
    if not hints:
        hints.append("- 數據看起來合理；可加大 sample 後再判斷")
    lines.extend(hints)

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n📄 Report written: {REPORT_PATH}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--skip-bj", action="store_true",
                    help="Use cached raw_results.json instead of re-running BJ")
    ap.add_argument("--force", action="store_true",
                    help="Bypass pair-cache and re-run all Opus passes")
    ap.add_argument("--no-cache", action="store_true",
                    help="Disable pair-cache lookup AND writes")
    args = ap.parse_args()

    labels = _load_labels()
    print(f"📋 Loaded {len(labels)} labels")

    cache_path = None if args.no_cache else str(CACHE_PATH)

    if args.skip_bj:
        results = _load_cached()
        print(f"📂 Using cached {len(results)} BJ results")
    else:
        results = _run_bj(labels, limit=args.limit, force=args.force,
                          cache_path=cache_path)

    diag = _diagnose(labels, results)
    if diag is None:
        sys.exit(1)

    print("\n" + "═" * 70)
    print(f"  BJ Calibration — n = {diag['paired_n']}  "
          f"(dropped {diag['n_insufficient']} insufficient + {diag['n_error']} errored)")
    print("═" * 70)
    o = diag["overall"]
    print(f"  OVERALL final_100  ρ={_fmt(o['spearman'])}  r={_fmt(o['pearson'])}  "
          f"MAE={_fmt(o['mae'])}  bj_var={_fmt(o['bj_variance'], 2)}")
    for dim, s in diag["dim_stats"].items():
        if "note" in s:
            print(f"  {dim:<14} insufficient data")
            continue
        print(f"  {dim:<14} ρ={_fmt(s['spearman'])}  r={_fmt(s['pearson'])}  MAE={_fmt(s['mae'])}")
    print("═" * 70)

    _write_report(diag)


if __name__ == "__main__":
    main()
