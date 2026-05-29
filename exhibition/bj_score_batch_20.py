"""Run BenchmarkJudge on 20 topics: naked (candidate) vs system (benchmark).

BJ uses Claude Opus 4.7 via subscription to compare videos visually in a
4-frame grid, scoring 0-100 on completeness/clarity/accuracy.

  final_100 = 0    → naked much worse than system  (BIG drama)
  final_100 = 50   → roughly equal
  final_100 = 100  → naked matches or exceeds system

For naked-failed topics (no video), we skip BJ and assign score 0 manually.

Incremental: writes results to bj_results.json after each topic.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

HERE = Path(__file__).resolve().parent
BATCH = HERE / "static" / "batch_20"
RESULTS_CSV = BATCH / "results.csv"
BJ_OUT = BATCH / "bj_scores.json"
WORKDIR = BATCH / "bj_workdir"


def load_done() -> dict:
    if BJ_OUT.exists():
        return json.loads(BJ_OUT.read_text(encoding="utf-8"))
    return {}


def save(results: dict):
    BJ_OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", help="Comma-separated topic prefix")
    ap.add_argument("--force", action="store_true", help="Re-judge even if cached")
    ap.add_argument("--passes", type=int, default=3)
    args = ap.parse_args()

    rows = list(csv.DictReader(open(RESULTS_CSV)))
    if args.items:
        wanted = set(args.items.split(","))
        rows = [r for r in rows if any(r["id"].startswith(w) for w in wanted)]

    WORKDIR.mkdir(parents=True, exist_ok=True)
    done = load_done()

    from agents.utils.benchmark_judge import BenchmarkJudge
    from agents.core.llm_client import LLMClient

    llm = LLMClient()
    bj = BenchmarkJudge(llm_client=llm, passes=args.passes)

    print(f"Running BJ on {len(rows)} topics (passes={args.passes})...")
    print(f"Already done: {len(done)} (use --force to re-run)")

    t_global = time.time()
    for i, r in enumerate(rows, 1):
        tid = r["id"]
        topic = r["topic"]
        print(f"\n[{i}/{len(rows)}] {tid}  ·  {topic}")

        if tid in done and not args.force:
            print(f"  ⏭️  cached: BJ score = {done[tid].get('final_100')}")
            continue

        naked_v = BATCH / "naked" / f"{tid}.mp4"
        sys_v = BATCH / "system" / f"{tid}.mp4"

        # Naked failed (no video) → score 0 by default
        if not naked_v.exists():
            done[tid] = {
                "final_100": 0,
                "status": "naked_render_failed",
                "topic": topic,
                "note": "Naked Opus did not produce a renderable video; system wins by default.",
            }
            save(done)
            print(f"  ❌ naked render failed → score 0 (auto)")
            continue

        if not sys_v.exists():
            done[tid] = {"final_100": None, "status": "system_missing", "topic": topic}
            save(done)
            print(f"  ⚠️  system video missing")
            continue

        t0 = time.time()
        try:
            result = bj.judge(
                candidate_video=str(naked_v),
                benchmark_video=str(sys_v),
                question_topic=topic,
                workdir=str(WORKDIR / tid),
            )
        except Exception as e:
            print(f"  💥 BJ crashed: {e}")
            done[tid] = {"final_100": None, "status": "judge_error", "topic": topic, "error": str(e)}
            save(done)
            continue

        dur = time.time() - t0
        score = result.get("final_100")
        scores = result.get("scores", {})
        done[tid] = {
            "final_100": score,
            "scores": scores,
            "evidence": result.get("evidence", {}),
            "topic": topic,
            "status": "ok",
            "judge_time_sec": round(dur, 1),
        }
        save(done)
        print(f"  ✅ BJ score = {score}/100  ({dur:.0f}s)")
        if scores:
            sline = "    " + "  ".join(f"{k}={v}" for k, v in scores.items())
            print(sline)

    elapsed = time.time() - t_global
    print(f"\n{'='*70}\nDONE in {elapsed/60:.1f} min · saved to {BJ_OUT}")

    # Ranking
    print(f"\n{'='*70}\nRANKING (low score = naked worse = big system advantage)")
    print(f"{'='*70}")
    ranked = sorted(
        [(tid, d) for tid, d in done.items() if d.get("final_100") is not None],
        key=lambda kv: kv[1]["final_100"]
    )
    for tid, d in ranked:
        s = d["final_100"]
        topic = d.get("topic", "")
        if d.get("status") == "naked_render_failed":
            tag = "❌naked"
        else:
            tag = "      "
        bar = "█" * (s // 5) + "░" * (20 - s // 5)
        print(f"  {tid:<22} {s:>3}/100 {bar}  {tag} {topic}")


if __name__ == "__main__":
    main()
