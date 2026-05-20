"""
BenchmarkJudge Runner — A/B vs Benchmark batch scoring for RAG-150 experiment.

Walks an experiment sample (default: evaluation/experiment_sample_30.json),
locates the corresponding A-variant and B-variant candidate videos under
`runs/`, scores both against the human-made benchmark in
`evaluation/benchmark_set/<qid>/benchmark.mp4`, and writes a comparison report.

The framework is INTENTIONALLY robust to missing benchmark videos (A-track is
not done yet). For each question we report:
  - `benchmark_status`: "present" / "missing"
  - if missing: skip BJ for that question (but emit a placeholder row)
  - if present: run BJ(candidate_A, benchmark) and BJ(candidate_B, benchmark)

Layout convention (caller can override via flags):
  runs/<variant_session_A>/<qid>/video.mp4               (variant A)
  runs/<variant_session_B>/<qid>/video.mp4               (variant B)
  evaluation/benchmark_set/<qid>/benchmark.mp4            (gold)

Usage:
  # Pure dry-run: show which (qid, A, B, benchmark) tuples will be judged.
  python evaluation/benchmark_runner.py --dry-run \\
      --session-a runs/20260520_001000 --session-b runs/20260520_002000

  # Real run; results cached under evaluation/golden_set/benchmark_judge_cache.json
  python evaluation/benchmark_runner.py \\
      --session-a runs/20260520_001000 --session-b runs/20260520_002000

  # Specific subset
  python evaluation/benchmark_runner.py --qids Q028,Q029,Q050 ...

  # Custom benchmark dir (if user wants to test against a single benchmark video)
  python evaluation/benchmark_runner.py --benchmark-dir my_benchmarks/

Output:
  evaluation/benchmark_runner_results_<timestamp>.json
  evaluation/benchmark_runner_report_<timestamp>.md
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SAMPLE_DEFAULT = ROOT / "evaluation" / "experiment_sample_30.json"
BENCHMARK_DIR_DEFAULT = ROOT / "evaluation" / "benchmark_set"
CACHE_DEFAULT = ROOT / "evaluation" / "golden_set" / "benchmark_judge_cache.json"


# ── Path resolution (kept dumb on purpose; layout can shift) ──────────────────

def _candidate_paths(session_dir: Path, qid: str) -> dict:
    """Find candidate artifacts under runs/<session>/<qid>/."""
    qdir = session_dir / qid
    return {
        "video":      qdir / "video.mp4",
        "code":       qdir / "code.py",
        "state_log":  qdir / "scene_state_log.json",
        "dir":        qdir,
    }


def _benchmark_paths(benchmark_root: Path, qid: str) -> dict:
    """Resolve benchmark video for <qid>.

    Preferred:  evaluation/benchmark_set/<qid>/benchmark.mp4   (user-polished final)
    Fallback:   evaluation/benchmark_set/<qid>/raw/draft_v1.mp4 (A-track draft)

    When falling back, emit a one-line stderr warning so callers don't silently
    score against an un-polished draft. `source` is "final" | "draft" | "missing".
    """
    bdir = benchmark_root / qid
    final_mp4 = bdir / "benchmark.mp4"
    draft_mp4 = bdir / "raw" / "draft_v1.mp4"

    if final_mp4.exists():
        video, source = final_mp4, "final"
    elif draft_mp4.exists():
        video, source = draft_mp4, "draft"
        print(f"⚠️  using DRAFT not final benchmark for {qid} ({draft_mp4.name})")
    else:
        video, source = final_mp4, "missing"  # keep canonical missing path

    return {
        "video":     video,
        "state_log": bdir / "scene_state_log.json",
        "dir":       bdir,
        "source":    source,
    }


def _exists(p) -> bool:
    return p is not None and Path(p).exists()


# ── Loader ────────────────────────────────────────────────────────────────────

def _load_sample(sample_path: Path, qid_filter=None):
    with open(sample_path, encoding="utf-8") as f:
        items = json.load(f)
    if qid_filter:
        keep = set(qid_filter)
        items = [x for x in items if x.get("id") in keep]
    return items


# ── Build tuples (no LLM call, useful for --dry-run) ─────────────────────────

def _build_jobs(sample, session_a, session_b, benchmark_root):
    jobs = []
    for entry in sample:
        qid = entry["id"]
        topic = entry.get("topic", "")
        gt = {"answer": entry.get("answer")} if entry.get("answer") else None

        bench = _benchmark_paths(benchmark_root, qid)
        cand_a = _candidate_paths(session_a, qid) if session_a else None
        cand_b = _candidate_paths(session_b, qid) if session_b else None

        jobs.append({
            "qid":   qid,
            "topic": topic,
            "ground_truth": gt,
            "benchmark":     {k: str(v) for k, v in bench.items()},
            "benchmark_status": "present" if _exists(bench["video"]) else "missing",
            "benchmark_source": bench["source"],  # "final" | "draft" | "missing"
            "candidate_a":   {k: str(v) for k, v in cand_a.items()} if cand_a else None,
            "candidate_a_status": (
                "present" if cand_a and _exists(cand_a["video"]) else "missing"),
            "candidate_b":   {k: str(v) for k, v in cand_b.items()} if cand_b else None,
            "candidate_b_status": (
                "present" if cand_b and _exists(cand_b["video"]) else "missing"),
        })
    return jobs


def _print_dry_run(jobs):
    n = len(jobs)
    bench_ok = sum(1 for j in jobs if j["benchmark_status"] == "present")
    a_ok = sum(1 for j in jobs if j["candidate_a_status"] == "present")
    b_ok = sum(1 for j in jobs if j["candidate_b_status"] == "present")
    bench_final = sum(1 for j in jobs if j.get("benchmark_source") == "final")
    bench_draft = sum(1 for j in jobs if j.get("benchmark_source") == "draft")
    print(f"\n📊 Dry-run plan ({n} questions)")
    print(f"   benchmark present: {bench_ok}/{n}  (final={bench_final}, draft={bench_draft})")
    print(f"   variant A present: {a_ok}/{n}")
    print(f"   variant B present: {b_ok}/{n}")
    print(f"   judgable (all 3): "
          f"{sum(1 for j in jobs if j['benchmark_status']=='present' and j['candidate_a_status']=='present' and j['candidate_b_status']=='present')}/{n}")

    print("\n  qid    bench  candA  candB")
    print("  " + "-" * 40)
    for j in jobs:
        b = "✓" if j["benchmark_status"] == "present" else "✗"
        a = "✓" if j["candidate_a_status"] == "present" else "✗"
        bb = "✓" if j["candidate_b_status"] == "present" else "✗"
        print(f"  {j['qid']:<6} {b:>5}  {a:>5}  {bb:>5}")


# ── Real run (BJ scoring) ────────────────────────────────────────────────────

def _score_pair(bj, cand_info, bench_info, topic, ground_truth, cache_path, force):
    code_path = cand_info.get("code")
    code_str = (Path(code_path).read_text(encoding="utf-8")
                if _exists(code_path) else None)
    # A: reuse FJ math_score from RefiningLoop's cost_report.json if available,
    # saving ~8s of redundant Opus Phase-1 per judge.
    from evaluation.benchmark_calibration import _load_precomputed_math_score
    precomp = _load_precomputed_math_score(cand_info["video"])
    if precomp is not None:
        print(f"   ↳ reused FJ math_correctness={precomp} from cost_report.json")
    return bj.judge(
        candidate_video=cand_info["video"],
        benchmark_video=bench_info["video"],
        question_topic=topic,
        candidate_code=code_str,
        candidate_state_log=cand_info.get("state_log") if _exists(cand_info.get("state_log")) else None,
        benchmark_state_log=bench_info.get("state_log") if _exists(bench_info.get("state_log")) else None,
        ground_truth=ground_truth,
        cache_path=cache_path,
        force=force,
        precomputed_math_score=precomp,
    )


def _run(jobs, cache_path, force, only_judgable):
    from agents.utils.benchmark_judge import BenchmarkJudge
    from agents.core.llm_client import LLMClient

    bj = BenchmarkJudge(llm_client=LLMClient())
    results = []
    for j in jobs:
        qid = j["qid"]
        row = {"qid": qid, "topic": j["topic"],
               "benchmark_source": j.get("benchmark_source", "missing")}

        if j["benchmark_status"] != "present":
            row["status"] = "skip_no_benchmark"
            results.append(row)
            print(f"⏭️  [{qid}] no benchmark → skip")
            continue

        for variant_key, cand_status_key in [
            ("candidate_a", "candidate_a_status"),
            ("candidate_b", "candidate_b_status"),
        ]:
            cand = j.get(variant_key)
            tag = variant_key[-1].upper()
            if not cand or j[cand_status_key] != "present":
                row[f"variant_{tag}"] = {"status": "missing"}
                continue
            if only_judgable and (j["candidate_a_status"] != "present"
                                  or j["candidate_b_status"] != "present"):
                row[f"variant_{tag}"] = {"status": "skip_partial_pair"}
                continue
            print(f"\n🔎 [{qid} / {tag}] judging vs benchmark...")
            try:
                res = _score_pair(bj, cand, j["benchmark"], j["topic"],
                                  j["ground_truth"], cache_path, force)
                # B: respect the insufficient_passes guard from BJ
                bj_status = res.get("status", "ok")
                if bj_status == "insufficient_passes":
                    row[f"variant_{tag}"] = {
                        "status":  "insufficient_passes",
                        "n_successful_passes": res.get("n_successful_passes"),
                    }
                    print(f"   ⚠️  insufficient passes ({res.get('n_successful_passes')}/{bj.passes}) — not scored")
                else:
                    row[f"variant_{tag}"] = {
                        "status":    "ok",
                        "final_100": res.get("final_100"),
                        "scores":    res.get("scores"),
                        "modes":     res.get("modes"),
                        "cache":     res.get("_cache", {}),
                    }
            except Exception as e:
                row[f"variant_{tag}"] = {"status": "error", "error": str(e)}

        row["status"] = "done"
        results.append(row)
    return results


# ── Reporting ────────────────────────────────────────────────────────────────

def _write_outputs(results, out_dir, stamp):
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"benchmark_runner_results_{stamp}.json"
    md_path = out_dir / f"benchmark_runner_report_{stamp}.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    # Summary stats
    a_scores = [r["variant_A"]["final_100"] for r in results
                if r.get("variant_A", {}).get("status") == "ok"]
    b_scores = [r["variant_B"]["final_100"] for r in results
                if r.get("variant_B", {}).get("status") == "ok"]
    judged_pairs = [r for r in results
                    if r.get("variant_A", {}).get("status") == "ok"
                    and r.get("variant_B", {}).get("status") == "ok"]
    b_minus_a = [r["variant_B"]["final_100"] - r["variant_A"]["final_100"]
                 for r in judged_pairs]

    a_insufficient = sum(1 for r in results
                         if r.get("variant_A", {}).get("status") == "insufficient_passes")
    b_insufficient = sum(1 for r in results
                         if r.get("variant_B", {}).get("status") == "insufficient_passes")

    lines = [
        f"# BenchmarkJudge Runner Report — {stamp}\n",
        f"- total questions:   {len(results)}",
        f"- skipped (no bench): {sum(1 for r in results if r['status']=='skip_no_benchmark')}",
        f"- variant A scored:  {len(a_scores)}  (insufficient: {a_insufficient})",
        f"- variant B scored:  {len(b_scores)}  (insufficient: {b_insufficient})",
        f"- paired (both A+B): {len(judged_pairs)}",
    ]
    if a_scores:
        lines.append(f"- A mean: {sum(a_scores)/len(a_scores):.1f}")
    if b_scores:
        lines.append(f"- B mean: {sum(b_scores)/len(b_scores):.1f}")
    if b_minus_a:
        lines.append(f"- B−A mean (RAG effect): {sum(b_minus_a)/len(b_minus_a):+.1f}")
        wins = sum(1 for d in b_minus_a if d > 0)
        ties = sum(1 for d in b_minus_a if d == 0)
        loses = sum(1 for d in b_minus_a if d < 0)
        lines.append(f"- B wins/ties/loses: {wins}/{ties}/{loses}")

    lines += [
        "\n## Per-Question\n",
        "| qid | status | A | B | B−A | notes |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        a = r.get("variant_A", {})
        b = r.get("variant_B", {})
        a_s = a.get("final_100", "—") if a.get("status") == "ok" else f"({a.get('status','?')})"
        b_s = b.get("final_100", "—") if b.get("status") == "ok" else f"({b.get('status','?')})"
        delta = ""
        if a.get("status") == "ok" and b.get("status") == "ok":
            delta = f"{b['final_100'] - a['final_100']:+d}"
        lines.append(f"| {r['qid']} | {r['status']} | {a_s} | {b_s} | {delta} | |")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n💾 results: {json_path}")
    print(f"📄 report:  {md_path}")
    return json_path, md_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", default=str(SAMPLE_DEFAULT),
                    help="Path to experiment sample json")
    ap.add_argument("--benchmark-dir", default=str(BENCHMARK_DIR_DEFAULT),
                    help="Root dir for benchmark_set/<qid>/benchmark.mp4")
    ap.add_argument("--session-a", default=None,
                    help="runs/<timestamp> session that produced variant A (no-RAG)")
    ap.add_argument("--session-b", default=None,
                    help="runs/<timestamp> session that produced variant B (with-RAG)")
    ap.add_argument("--qids", default=None,
                    help="Comma-separated qid filter (e.g. Q028,Q050)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Only show what would be judged; no LLM calls")
    ap.add_argument("--force", action="store_true",
                    help="Bypass pair-cache and re-run all Opus passes")
    ap.add_argument("--no-cache", action="store_true",
                    help="Disable pair-cache lookup AND writes")
    ap.add_argument("--only-judgable", action="store_true",
                    help="Skip qids where either variant is missing (default scores singletons)")
    ap.add_argument("--out-dir", default=str(ROOT / "evaluation"),
                    help="Directory for results + report")
    args = ap.parse_args()

    sample_path = Path(args.sample)
    benchmark_root = Path(args.benchmark_dir)
    session_a = Path(args.session_a) if args.session_a else None
    session_b = Path(args.session_b) if args.session_b else None
    qid_filter = [q.strip() for q in args.qids.split(",")] if args.qids else None

    if not sample_path.exists():
        print(f"❌ sample not found: {sample_path}")
        sys.exit(1)

    sample = _load_sample(sample_path, qid_filter=qid_filter)
    print(f"📋 sample: {len(sample)} questions (filter={qid_filter})")
    print(f"   benchmark dir: {benchmark_root}  (exists={benchmark_root.exists()})")
    print(f"   variant A session: {session_a or '<none>'}")
    print(f"   variant B session: {session_b or '<none>'}")

    jobs = _build_jobs(sample, session_a, session_b, benchmark_root)

    if args.dry_run:
        _print_dry_run(jobs)
        return

    cache_path = None if args.no_cache else str(CACHE_DEFAULT)
    results = _run(jobs, cache_path=cache_path, force=args.force,
                   only_judgable=args.only_judgable)

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    _write_outputs(results, Path(args.out_dir), stamp)


if __name__ == "__main__":
    main()
