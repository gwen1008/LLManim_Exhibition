"""Diagnose BenchmarkJudge accuracy misjudgements.

Two-layer scan over historical BJ data:
  - Layer 1 (deep): bj_cache.json with full likert_votes + deterministic.math_score
  - Layer 2 (shallow): paired runner results with only modes + scores

Outputs a markdown report with baseline distribution + pattern hits +
per-case detail for manual review.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any

# Mirror constants from agents/utils/benchmark_judge.py (do not import to keep
# this script standalone-runnable without project deps loaded).
LIKERT_OFFSET = {
    "much_better": 0,
    "better": 0,
    "same": 0,
    "worse": -20,
    "much_worse": -40,
    "broken": -70,
    "inconclusive": 0,
}
MATH_PENALTY = {5: 0, 4: -5, 3: -15, 2: -30, 1: -60}
ACCURACY_GATE_THRESHOLD = 75

# ── Layer 1 ─────────────────────────────────────────────────────────────────


def scan_deep(cache_path: Path) -> dict[str, Any]:
    blob = json.loads(cache_path.read_text())
    rows = []
    for key, entry in blob.items():
        modes = entry.get("modes") or {}
        votes = (entry.get("likert_votes") or {}).get("accuracy") or []
        det = entry.get("deterministic") or {}
        scores = entry.get("scores") or {}

        acc_mode = modes.get("accuracy")
        acc_score_final = scores.get("accuracy")
        math_score = det.get("math_score")
        math_penalty = det.get("math_penalty", 0)
        acc_factor = det.get("accuracy_factor")

        acc_vision = None
        if acc_mode in LIKERT_OFFSET:
            acc_vision = max(0, min(100, 100 + LIKERT_OFFSET[acc_mode]))

        math_pressure = None
        if acc_vision is not None and acc_score_final is not None:
            math_pressure = acc_vision - acc_score_final

        vote_unique = len(set(votes)) if votes else 0
        all_inconclusive = bool(votes) and all(v == "inconclusive" for v in votes)

        row = {
            "key": key,
            "candidate_video": entry.get("candidate_video", ""),
            "benchmark_video": entry.get("benchmark_video", ""),
            "acc_mode": acc_mode,
            "votes": votes,
            "vote_unique_count": vote_unique,
            "all_inconclusive": all_inconclusive,
            "math_score": math_score,
            "math_penalty": math_penalty,
            "acc_vision_reconstructed": acc_vision,
            "acc_score_final": acc_score_final,
            "math_pressure": math_pressure,
            "accuracy_factor": acc_factor,
            "final_100": entry.get("final_100"),
            "completeness_mode": modes.get("completeness"),
            "clarity_mode": modes.get("clarity"),
        }
        rows.append(row)

    # Patterns
    p1 = [r for r in rows if r["all_inconclusive"] and (r["final_100"] or 0) >= 70]
    p2 = [r for r in rows if (r["math_pressure"] or 0) >= 20]
    p3 = [r for r in rows if r["vote_unique_count"] >= 3]

    finals = [r["final_100"] for r in rows if r["final_100"] is not None]
    acc_finals = [r["acc_score_final"] for r in rows if r["acc_score_final"] is not None]
    return {
        "rows": rows,
        "n": len(rows),
        "final_stats": _stats(finals),
        "acc_stats": _stats(acc_finals),
        "p1_hits": p1,
        "p2_hits": p2,
        "p3_hits": p3,
    }


# ── Layer 2 ─────────────────────────────────────────────────────────────────


def scan_shallow(results_path: Path) -> dict[str, Any]:
    data = json.loads(results_path.read_text())
    rows = []
    for item in data:
        qid = item.get("qid")
        topic = (item.get("topic") or "").split("\n", 1)[0][:60]
        for vk in ("variant_A", "variant_B", "variant_C"):
            v = item.get(vk)
            if not v or v.get("status") != "ok":
                continue
            modes = v.get("modes") or {}
            scores = v.get("scores") or {}
            rows.append(
                {
                    "qid": qid,
                    "variant": vk.replace("variant_", ""),
                    "topic": topic,
                    "acc_mode": modes.get("accuracy"),
                    "acc_score": scores.get("accuracy"),
                    "completeness_mode": modes.get("completeness"),
                    "clarity_mode": modes.get("clarity"),
                    "final_100": v.get("final_100"),
                }
            )

    # P4: mode-score inconsistency (math_penalty leak from shallow view)
    p4_hits = []
    for r in rows:
        am, asc = r["acc_mode"], r["acc_score"]
        if am is None or asc is None:
            continue
        if am == "same" and asc < 80:
            p4_hits.append({**r, "reason": f"mode=same but acc_score={asc} (<80)"})
        elif am == "broken" and asc > 60:
            p4_hits.append({**r, "reason": f"mode=broken but acc_score={asc} (>60)"})
        elif am == "much_worse" and asc > 80:
            p4_hits.append({**r, "reason": f"mode=much_worse but acc_score={asc} (>80)"})

    acc_scores = [r["acc_score"] for r in rows if r["acc_score"] is not None]
    finals = [r["final_100"] for r in rows if r["final_100"] is not None]
    mode_dist = Counter(r["acc_mode"] for r in rows if r["acc_mode"])

    return {
        "rows": rows,
        "n_pairs": len(data),
        "n_variants": len(rows),
        "final_stats": _stats(finals),
        "acc_stats": _stats(acc_scores),
        "mode_dist": mode_dist,
        "p4_hits": p4_hits,
    }


# ── Self-sanity ────────────────────────────────────────────────────────────


def scan_self_sanity(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    rows = []
    for item in data:
        qid = item.get("qid")
        modes = item.get("modes") or {}
        scores = item.get("scores") or {}
        # Self-vs-self should be all "same" → acc_score=100 → final=100
        acc_mode = modes.get("accuracy")
        acc_score = scores.get("accuracy")  # may be None (schema_missing)
        rows.append(
            {
                "qid": qid,
                "status": item.get("status"),
                "final_100": item.get("final_100"),
                "acc_mode": acc_mode,
                "acc_score": acc_score,
                "schema_has_scores": "scores" in item,
            }
        )

    drift = []
    schema_missing = []
    for r in rows:
        if not r["schema_has_scores"]:
            schema_missing.append(r)
            continue
        # Only check if we actually have the field
        if r["acc_score"] is not None and r["acc_score"] < 95:
            drift.append(r)
        # Also flag mode drift even without scores
        if r["acc_mode"] and r["acc_mode"] != "same":
            drift.append({**r, "reason": f"acc_mode={r['acc_mode']} (expected 'same')"})
        elif r["final_100"] is not None and r["final_100"] < 95:
            drift.append({**r, "reason": f"final_100={r['final_100']} (<95)"})

    return {
        "rows": rows,
        "n": len(rows),
        "drift": drift,
        "schema_missing": schema_missing,
    }


# ── Helpers ────────────────────────────────────────────────────────────────


def _stats(xs: list[float]) -> dict[str, float | int | None]:
    if not xs:
        return {"n": 0, "mean": None, "std": None, "min": None, "max": None}
    return {
        "n": len(xs),
        "mean": round(statistics.mean(xs), 2),
        "std": round(statistics.pstdev(xs), 2) if len(xs) > 1 else 0.0,
        "min": min(xs),
        "max": max(xs),
    }


def _fmt_video(path: str) -> str:
    if not path:
        return "(none)"
    parts = Path(path).parts
    # Show last 3 path components for context
    return "/".join(parts[-3:]) if len(parts) >= 3 else path


# ── Report ─────────────────────────────────────────────────────────────────


def render_report(
    deep: dict[str, Any] | None,
    shallow: dict[str, Any] | None,
    self_sanity: dict[str, Any] | None,
) -> str:
    lines: list[str] = []
    lines.append("# BJ Accuracy Diagnosis Report")
    lines.append("")
    lines.append(
        "Auto-generated by `evaluation/diagnose_bj_acc.py`. "
        "Two-layer scan over historical BenchmarkJudge data to surface "
        "accuracy-dimension misjudgements."
    )
    lines.append("")

    # ── Summary ──
    lines.append("## Summary")
    lines.append("")
    summary_bits = []
    if deep:
        summary_bits.append(f"- **Layer 1 (deep)**: {deep['n']} entries")
        summary_bits.append(
            f"  - P1 all-inconclusive≥70: **{len(deep['p1_hits'])}** "
            f"({_pct(len(deep['p1_hits']), deep['n'])})"
        )
        summary_bits.append(
            f"  - P2 math-pressure≥20: **{len(deep['p2_hits'])}** "
            f"({_pct(len(deep['p2_hits']), deep['n'])})"
        )
        summary_bits.append(
            f"  - P3 vote-unique≥3: **{len(deep['p3_hits'])}** "
            f"({_pct(len(deep['p3_hits']), deep['n'])})"
        )
    if shallow:
        summary_bits.append(
            f"- **Layer 2 (shallow)**: {shallow['n_variants']} variants "
            f"across {shallow['n_pairs']} qids"
        )
        summary_bits.append(
            f"  - P4 mode-score inconsistency: **{len(shallow['p4_hits'])}** "
            f"({_pct(len(shallow['p4_hits']), shallow['n_variants'])})"
        )
    if self_sanity:
        summary_bits.append(f"- **Self-sanity**: {self_sanity['n']} entries")
        summary_bits.append(
            f"  - drift hits: **{len(self_sanity['drift'])}**, "
            f"schema_missing: {len(self_sanity['schema_missing'])}"
        )
    lines.extend(summary_bits)
    lines.append("")

    # Sample-size warning
    if deep and deep["n"] < 10:
        lines.append(
            f"> ⚠️ **Deep sample size only {deep['n']}** — patterns P1/P2/P3 "
            "with zero hits cannot conclude BJ is bug-free. "
            "Recommend rerunning BJ on 10–15 additional candidates to gather data."
        )
        lines.append("")

    # ── Layer 1 detail ──
    if deep:
        lines.append("## Layer 1: Deep scan (likert_votes + math_score)")
        lines.append("")
        lines.append(f"**Baseline**: final_100 stats = `{deep['final_stats']}`")
        lines.append(f"**Baseline**: acc_score_final stats = `{deep['acc_stats']}`")
        lines.append("")

        lines.append("### All entries")
        lines.append("")
        lines.append(
            "| key | acc_mode | votes | math_score | math_pressure | "
            "acc_vision | acc_final | accuracy_factor | final_100 |"
        )
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for r in deep["rows"]:
            lines.append(
                f"| `{r['key'][:12]}` | {r['acc_mode']} | "
                f"{','.join(r['votes'])} | {r['math_score']} | "
                f"{r['math_pressure']} | {r['acc_vision_reconstructed']} | "
                f"{r['acc_score_final']} | {r['accuracy_factor']} | "
                f"{r['final_100']} |"
            )
        lines.append("")

        for pname, hits, desc in [
            ("P1", deep["p1_hits"], "All-inconclusive votes but final_100 ≥ 70"),
            ("P2", deep["p2_hits"], "math_pressure ≥ 20 (math review compressed vision)"),
            ("P3", deep["p3_hits"], "vote_unique_count ≥ 3 (passes disagreed)"),
        ]:
            lines.append(f"### {pname} hits — {desc}")
            lines.append("")
            if not hits:
                lines.append("_No hits._")
            else:
                for h in hits:
                    lines.append(f"- **`{h['key']}`** (final_100={h['final_100']})")
                    lines.append(f"  - candidate: `{_fmt_video(h['candidate_video'])}`")
                    lines.append(f"  - benchmark: `{_fmt_video(h['benchmark_video'])}`")
                    lines.append(
                        f"  - acc_mode=**{h['acc_mode']}**, votes={h['votes']}, "
                        f"math_score={h['math_score']}, "
                        f"math_pressure={h['math_pressure']}, "
                        f"acc_vision→acc_final = "
                        f"{h['acc_vision_reconstructed']}→{h['acc_score_final']}"
                    )
            lines.append("")

    # ── Layer 2 detail ──
    if shallow:
        lines.append("## Layer 2: Shallow scan (modes + scores only)")
        lines.append("")
        lines.append(f"**Baseline**: final_100 stats = `{shallow['final_stats']}`")
        lines.append(f"**Baseline**: acc_score stats = `{shallow['acc_stats']}`")
        lines.append(f"**Baseline**: acc mode distribution = `{dict(shallow['mode_dist'])}`")
        lines.append("")

        lines.append("### P4 hits — acc mode-score inconsistency")
        lines.append("")
        if not shallow["p4_hits"]:
            lines.append("_No hits._")
        else:
            lines.append("| qid | variant | acc_mode | acc_score | final_100 | reason | topic |")
            lines.append("|---|---|---|---|---|---|---|")
            for h in shallow["p4_hits"]:
                lines.append(
                    f"| {h['qid']} | {h['variant']} | {h['acc_mode']} | "
                    f"{h['acc_score']} | {h['final_100']} | {h['reason']} | "
                    f"{h['topic']} |"
                )
        lines.append("")

    # ── Self-sanity detail ──
    if self_sanity:
        lines.append("## Self-sanity drift")
        lines.append("")
        if self_sanity["schema_missing"]:
            qids = [r["qid"] for r in self_sanity["schema_missing"]]
            lines.append(
                f"⚠️ **schema_missing** for: {qids} — "
                "self-sanity file lacks `scores.accuracy`, "
                "only `final_100` and `modes` available. "
                "Consider extending the self-sanity writer to record `scores`."
            )
            lines.append("")
        if self_sanity["drift"]:
            lines.append("Drift hits:")
            for r in self_sanity["drift"]:
                lines.append(
                    f"- qid={r['qid']} status={r['status']} "
                    f"acc_mode={r.get('acc_mode')} "
                    f"acc_score={r.get('acc_score')} "
                    f"final_100={r.get('final_100')} "
                    f"reason={r.get('reason', 'n/a')}"
                )
        else:
            lines.append("_No drift detected._")
        lines.append("")

    # ── Interpretation ──
    lines.append("## How to read this")
    lines.append("")
    lines.append(
        "- **math_pressure** = `acc_vision_reconstructed − acc_score_final`. "
        "If >0, math review compressed vision's verdict; "
        "≥20 means vision said one thing and Claude code review overrode it heavily."
    )
    lines.append(
        "- **acc_vision_reconstructed** = `100 + LIKERT_OFFSET[mode]` "
        "(same=100, worse=80, much_worse=60, broken=30). "
        "This is what BJ vision *originally* scored before the math min-cap."
    )
    lines.append(
        "- **P4 in Layer 2** is necessarily approximate — without "
        "likert_votes we can't isolate vision-vs-math pressure. "
        "Use P2 in Layer 1 for that."
    )
    lines.append("")

    return "\n".join(lines)


def _pct(n: int, total: int) -> str:
    if total == 0:
        return "0%"
    return f"{100 * n / total:.1f}%"


# ── Main ────────────────────────────────────────────────────────────────────


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deep", type=Path, help="bj_cache.json with full schema")
    ap.add_argument("--shallow", type=Path, help="benchmark_runner_results JSON")
    ap.add_argument("--self-sanity", type=Path, help="bj_self_sanity_results.json")
    ap.add_argument("--out", type=Path, required=True, help="Output markdown report")
    args = ap.parse_args()

    deep = scan_deep(args.deep) if args.deep else None
    shallow = scan_shallow(args.shallow) if args.shallow else None
    self_sanity = scan_self_sanity(args.self_sanity) if args.self_sanity else None

    report = render_report(deep, shallow, self_sanity)
    args.out.write_text(report)
    print(f"✓ wrote {args.out}")
    print(f"  layer 1: {deep['n'] if deep else 0} entries")
    print(f"  layer 2: {shallow['n_variants'] if shallow else 0} variants")
    print(f"  self-sanity: {self_sanity['n'] if self_sanity else 0} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
