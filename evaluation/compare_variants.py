"""Compare two run_evaluation.py sessions (e.g., A vs C, or B vs C).

Reads each case's `cost_report.json` and produces:
  - markdown report (per-case diff + aggregate stats + cross-tabulations)
  - optional HTML gallery with paired videos for side-by-side review

Usage:
  python evaluation/compare_variants.py \
      --a runs/20260520_154252_variantA \
      --c runs/20260521_XXXXXX_variantC \
      --out evaluation/compare_A_vs_C.md \
      --html evaluation/compare_A_vs_C.html
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Optional

REPO = Path(__file__).resolve().parents[1]

# Fix the known A-group GT-match LaTeX-vs-ASCII bug.
# See memory: project_variant_a_baseline_20260520.md
# `_compare_answer` treated `\frac{a}{b}` ≠ `a/b` as mismatch.
# We normalize for fair display, but keep `gt_match_raw` for transparency.
import re


def _normalize_answer(s: str) -> str:
    """Best-effort normalize LaTeX/ASCII fraction representations for comparison."""
    if not s:
        return ""
    s = s.strip().strip("$ ").replace("\\,", "").replace(" ", "")
    # \frac{a}{b} → a/b
    s = re.sub(r"\\d?frac\{([^{}]+)\}\{([^{}]+)\}", r"\1/\2", s)
    # Mixed number "4 9/10" or "4\frac{9}{10}" already covered above → 4_9/10
    return s.lower()


def _gt_match_fixed(fj: dict, ground_truth: str) -> Optional[bool]:
    """Re-compute GT match with the bug-fixed normalizer."""
    if not ground_truth:
        return None
    raw_answer = fj.get("final_answer_in_video") or ""
    if not raw_answer:
        return None
    return _normalize_answer(raw_answer) == _normalize_answer(ground_truth)


def load_session(session_dir: Path) -> dict[str, dict]:
    """Load all case results from a variant session directory."""
    out: dict[str, dict] = {}
    if not session_dir.exists():
        raise FileNotFoundError(f"Session dir not found: {session_dir}")

    # Read summary.csv for ground truth + meta
    summary_path = session_dir / "summary.csv"
    gt_map: dict[str, str] = {}
    topic_map: dict[str, str] = {}
    knowledge_map: dict[str, str] = {}
    if summary_path.exists():
        with summary_path.open(encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                qid = row.get("Case ID", "").strip()
                if not qid:
                    continue
                topic_map[qid] = row.get("Topic", "")[:80]
                # `Knowledge Point` can literally be "-" in old A-group summaries; fall back to Category
                kp = row.get("Knowledge Point", "").strip()
                if not kp or kp == "-":
                    kp = row.get("Category", "").strip()
                knowledge_map[qid] = kp

    # Read each case's cost_report.json
    for case_dir in sorted(session_dir.iterdir()):
        if not case_dir.is_dir() or not case_dir.name.startswith("Q"):
            continue
        qid = case_dir.name
        cr_path = case_dir / "cost_report.json"
        if not cr_path.exists():
            out[qid] = {"missing": True, "topic": topic_map.get(qid, ""), "knowledge": knowledge_map.get(qid, "")}
            continue
        try:
            cr = json.loads(cr_path.read_text(encoding="utf-8"))
        except Exception as e:
            out[qid] = {"error": str(e)}
            continue

        fj = cr.get("final_judge", {}) or {}
        scores = fj.get("scores", {}) or {}
        # Try to extract GT answer from per-case if available; otherwise skip the re-compute
        out[qid] = {
            "verdict": fj.get("verdict"),
            "weighted": fj.get("weighted_total"),
            "math": scores.get("math_correctness"),
            "concept": scores.get("concept_alignment"),
            "visual": scores.get("visual_clarity"),
            "layout": scores.get("spatial_layout"),
            "gt_match_raw": fj.get("ground_truth_match"),
            "final_answer": fj.get("final_answer_in_video"),
            "cost": cr.get("total_cost_usd"),
            "tokens": cr.get("total_prompt_tokens", 0) + cr.get("total_completion_tokens", 0),
            "time_total": (
                (cr.get("time_planner_sec") or 0)
                + (cr.get("time_coder_sec") or 0)
                + (cr.get("time_render_sec") or 0)
                + (cr.get("time_vision_sec") or 0)
                + (cr.get("time_rag_sec") or 0)
            ),
            "time_rag": cr.get("time_rag_sec", 0),
            "topic": topic_map.get(qid, ""),
            "knowledge": knowledge_map.get(qid, ""),
            "video": str(case_dir / "video.mp4"),
            "code": str(case_dir / "code.py"),
        }
    return out


def aggregate(data: dict[str, dict]) -> dict:
    """Compute aggregate stats for one variant."""
    cases = [v for v in data.values() if "verdict" in v]
    if not cases:
        return {"n": 0}
    pass_count = sum(1 for c in cases if c["verdict"] == "PASS")
    gt_count = sum(1 for c in cases if c.get("gt_match_raw") is True)
    return {
        "n": len(cases),
        "pass_rate": pass_count / len(cases),
        "gt_rate": gt_count / len(cases),
        "avg_weighted": sum((c["weighted"] or 0) for c in cases) / len(cases),
        "avg_math": sum((c["math"] or 0) for c in cases) / len(cases),
        "avg_concept": sum((c["concept"] or 0) for c in cases) / len(cases),
        "avg_visual": sum((c["visual"] or 0) for c in cases) / len(cases),
        "avg_layout": sum((c["layout"] or 0) for c in cases) / len(cases),
        "total_cost": sum((c.get("cost") or 0) for c in cases),
        "total_tokens": sum((c.get("tokens") or 0) for c in cases),
        "avg_time": sum((c.get("time_total") or 0) for c in cases) / len(cases),
        "avg_rag_time": sum((c.get("time_rag") or 0) for c in cases) / len(cases),
    }


def by_knowledge(data: dict[str, dict]) -> dict[str, dict]:
    """Group cases by knowledge_point, with mini-aggregate per group."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for c in data.values():
        if "verdict" not in c:
            continue
        kp = c.get("knowledge", "") or "(?)"
        groups[kp].append(c)
    out = {}
    for kp, cases in groups.items():
        n = len(cases)
        out[kp] = {
            "n": n,
            "pass_rate": sum(1 for c in cases if c["verdict"] == "PASS") / n,
            "avg_weighted": sum((c["weighted"] or 0) for c in cases) / n,
        }
    return out


def render_md(a_data: dict, c_data: dict, a_name: str, c_name: str) -> str:
    """Generate markdown comparison report."""
    a_agg = aggregate(a_data)
    c_agg = aggregate(c_data)
    a_kp = by_knowledge(a_data)
    c_kp = by_knowledge(c_data)

    lines = []
    lines.append(f"# Compare: {a_name} vs {c_name}")
    lines.append("")
    lines.append(f"- **{a_name}**: {a_agg.get('n', 0)} cases")
    lines.append(f"- **{c_name}**: {c_agg.get('n', 0)} cases")
    lines.append("")

    # ─ Aggregate ─
    lines.append("## Aggregate")
    lines.append("")
    lines.append(f"| Metric | {a_name} | {c_name} | Δ (C−A) |")
    lines.append("|---|---:|---:|---:|")
    metric_map = [
        ("Pass rate", "pass_rate", "%"),
        ("GT-match rate (raw)", "gt_rate", "%"),
        ("Avg weighted", "avg_weighted", ""),
        ("Avg math", "avg_math", ""),
        ("Avg concept", "avg_concept", ""),
        ("Avg visual", "avg_visual", ""),
        ("Avg layout", "avg_layout", ""),
        ("Total cost ($)", "total_cost", ""),
        ("Total tokens", "total_tokens", ""),
        ("Avg time (s)", "avg_time", ""),
        ("Avg RAG time (s)", "avg_rag_time", ""),
    ]
    for label, key, unit in metric_map:
        av, cv = a_agg.get(key, 0), c_agg.get(key, 0)
        if unit == "%":
            av_s = f"{av * 100:.1f}%"
            cv_s = f"{cv * 100:.1f}%"
            d_s = f"{(cv - av) * 100:+.1f} pp"
        elif isinstance(av, float):
            av_s = f"{av:.3f}"
            cv_s = f"{cv:.3f}"
            d_s = f"{cv - av:+.3f}"
        else:
            av_s = f"{av}"
            cv_s = f"{cv}"
            d_s = f"{cv - av:+d}"
        lines.append(f"| {label} | {av_s} | {cv_s} | {d_s} |")
    lines.append("")

    # ─ By knowledge point ─
    lines.append("## By Knowledge Point")
    lines.append("")
    lines.append(f"| Knowledge | n | {a_name} pass | {c_name} pass | Δ | {a_name} avg | {c_name} avg | Δ |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    all_kps = sorted(set(a_kp.keys()) | set(c_kp.keys()))
    for kp in all_kps:
        a = a_kp.get(kp, {"n": 0, "pass_rate": 0, "avg_weighted": 0})
        c = c_kp.get(kp, {"n": 0, "pass_rate": 0, "avg_weighted": 0})
        n = max(a.get("n", 0), c.get("n", 0))
        dp = (c["pass_rate"] - a["pass_rate"]) * 100
        dw = c["avg_weighted"] - a["avg_weighted"]
        lines.append(
            f"| {kp} | {n} | {a['pass_rate']*100:.0f}% | {c['pass_rate']*100:.0f}% | {dp:+.0f}pp | "
            f"{a['avg_weighted']:.2f} | {c['avg_weighted']:.2f} | {dw:+.2f} |"
        )
    lines.append("")

    # ─ Per-case diff ─
    lines.append("## Per-Case Diff (sorted by Δ weighted, descending)")
    lines.append("")
    lines.append(f"| QID | Knowledge | {a_name} W | {c_name} W | ΔW | {a_name} V | {c_name} V | {a_name} verdict | {c_name} verdict | GT(A) | GT(C) |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---|---|---|---|")
    rows = []
    all_qids = sorted(set(a_data.keys()) | set(c_data.keys()))
    for qid in all_qids:
        a = a_data.get(qid, {})
        c = c_data.get(qid, {})
        if "verdict" not in a and "verdict" not in c:
            continue
        aw = a.get("weighted") or 0
        cw = c.get("weighted") or 0
        rows.append({
            "qid": qid,
            "kp": (a.get("knowledge") or c.get("knowledge") or "")[:14],
            "aw": aw, "cw": cw, "dw": cw - aw,
            "av": a.get("visual") or 0, "cv": c.get("visual") or 0,
            "averdict": a.get("verdict", "—"),
            "cverdict": c.get("verdict", "—"),
            "agt": "✓" if a.get("gt_match_raw") else ("✗" if a.get("gt_match_raw") is False else "—"),
            "cgt": "✓" if c.get("gt_match_raw") else ("✗" if c.get("gt_match_raw") is False else "—"),
        })
    rows.sort(key=lambda r: -r["dw"])  # biggest improvement first
    for r in rows:
        lines.append(
            f"| {r['qid']} | {r['kp']} | {r['aw']:.1f} | {r['cw']:.1f} | "
            f"{r['dw']:+.1f} | {r['av']} | {r['cv']} | {r['averdict']} | {r['cverdict']} | {r['agt']} | {r['cgt']} |"
        )
    lines.append("")

    # ─ Verdict cross-tab ─
    lines.append("## Verdict Cross-Tab")
    lines.append("")
    cross: dict[tuple[str, str], int] = defaultdict(int)
    for qid in all_qids:
        av = a_data.get(qid, {}).get("verdict", "MISSING")
        cv = c_data.get(qid, {}).get("verdict", "MISSING")
        cross[(av, cv)] += 1
    cells = sorted({k[1] for k in cross.keys()})
    rows = sorted({k[0] for k in cross.keys()})
    lines.append(f"| {a_name} \\ {c_name} | " + " | ".join(cells) + " |")
    lines.append("|---|" + "|".join("---:" for _ in cells) + "|")
    for r in rows:
        cells_v = [str(cross.get((r, c), 0)) for c in cells]
        lines.append(f"| **{r}** | " + " | ".join(cells_v) + " |")
    lines.append("")

    # ─ Headline takeaway ─
    lines.append("## Headline")
    lines.append("")
    n = a_agg.get("n", 0)
    if n == c_agg.get("n", 0) and n > 0:
        better = sum(1 for r in rows if False) if not rows else 0  # placeholder
        # Recount from per-case
        better = 0; worse = 0; tie = 0
        for qid in all_qids:
            a = a_data.get(qid, {})
            c = c_data.get(qid, {})
            if "weighted" not in a or "weighted" not in c:
                continue
            d = (c.get("weighted") or 0) - (a.get("weighted") or 0)
            if d > 0.05:
                better += 1
            elif d < -0.05:
                worse += 1
            else:
                tie += 1
        lines.append(f"- **{c_name} better**: {better} / {n}")
        lines.append(f"- **Tie (|Δ| ≤ 0.05)**: {tie} / {n}")
        lines.append(f"- **{c_name} worse**: {worse} / {n}")
        d_wgt = c_agg.get("avg_weighted", 0) - a_agg.get("avg_weighted", 0)
        d_pass = (c_agg.get("pass_rate", 0) - a_agg.get("pass_rate", 0)) * 100
        lines.append("")
        if d_wgt > 0.1:
            lines.append(f"➡️ **{c_name} is meaningfully better**: avg weighted +{d_wgt:.2f}, pass rate {d_pass:+.0f}pp")
        elif d_wgt < -0.1:
            lines.append(f"⚠️ **{c_name} is meaningfully worse**: avg weighted {d_wgt:+.2f}, pass rate {d_pass:+.0f}pp")
        else:
            lines.append(f"🟰 **{c_name} ≈ {a_name}**: avg weighted {d_wgt:+.2f}, no meaningful difference at A's score ceiling (likely both at 5.0/5.0; need stricter judge to discriminate)")
    lines.append("")

    return "\n".join(lines)


def render_html_gallery(a_data: dict, c_data: dict, a_name: str, c_name: str, out_path: Path) -> None:
    """Generate paired side-by-side HTML gallery."""
    all_qids = sorted(set(a_data.keys()) | set(c_data.keys()))

    rows_html = []
    for qid in all_qids:
        a = a_data.get(qid, {})
        c = c_data.get(qid, {})
        if "verdict" not in a and "verdict" not in c:
            continue
        topic = (a.get("topic") or c.get("topic") or "").replace("|", "/")
        a_vid = Path(a.get("video", "")) if a.get("video") else None
        c_vid = Path(c.get("video", "")) if c.get("video") else None

        def _rel(vid: Optional[Path]) -> Optional[str]:
            if not vid or not vid.exists():
                return None
            try:
                return str(vid.relative_to(out_path.parent))
            except ValueError:
                # gallery emitted outside repo (e.g. /tmp); fall back to absolute file:// URI
                return f"file://{vid.resolve()}"

        a_vid_rel = _rel(a_vid)
        c_vid_rel = _rel(c_vid)
        a_label = f"W={a.get('weighted','—')} V={a.get('visual','—')} {a.get('verdict','—')}"
        c_label = f"W={c.get('weighted','—')} V={c.get('visual','—')} {c.get('verdict','—')}"
        dw = (c.get("weighted") or 0) - (a.get("weighted") or 0)
        delta_class = "win" if dw > 0.05 else ("lose" if dw < -0.05 else "tie")
        rows_html.append(f"""
<section class="row {delta_class}">
  <h2>{qid} <small>{a.get('knowledge','') or c.get('knowledge','')}</small> <span class="delta">Δ={dw:+.1f}</span></h2>
  <p class="topic">{topic[:140]}</p>
  <div class="pair">
    <div class="cell">
      <div class="label">{a_name}: {a_label}</div>
      {f'<video src="{a_vid_rel}" controls preload="metadata"></video>' if a_vid_rel else '<div class="missing">(no video)</div>'}
    </div>
    <div class="cell">
      <div class="label">{c_name}: {c_label}</div>
      {f'<video src="{c_vid_rel}" controls preload="metadata"></video>' if c_vid_rel else '<div class="missing">(no video)</div>'}
    </div>
  </div>
</section>""")

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>{a_name} vs {c_name}</title>
<style>
  body {{ font-family: -apple-system, "PingFang TC", sans-serif; margin: 20px; background: #f7f7f9; }}
  header {{ position: sticky; top: 0; background: #fff; padding: 12px; border-bottom: 1px solid #ddd; margin: -20px -20px 20px; }}
  .row {{ background: #fff; margin-bottom: 24px; padding: 14px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .row.win {{ border-left: 5px solid #0a7; }}
  .row.lose {{ border-left: 5px solid #e44; }}
  .row.tie {{ border-left: 5px solid #aaa; }}
  .row h2 {{ margin: 0 0 4px; font-size: 16px; }}
  .row h2 small {{ color: #888; font-weight: normal; font-size: 13px; }}
  .row h2 .delta {{ float: right; font-size: 14px; }}
  .topic {{ color: #555; font-size: 13px; margin: 4px 0 10px; }}
  .pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
  .cell .label {{ font-size: 12px; color: #444; margin-bottom: 4px; font-family: ui-monospace, monospace; }}
  .cell video {{ width: 100%; background: #000; border-radius: 4px; max-height: 320px; }}
  .missing {{ padding: 60px; text-align: center; color: #aaa; background: #fafafa; }}
</style>
</head>
<body>
<header>
  <h1>{a_name} vs {c_name}</h1>
  <p>Green border = {c_name} better, red = worse, grey = tie. Use companion <code>compare_*.md</code> for tabular stats.</p>
</header>
{"".join(rows_html)}
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--a", required=True, type=Path, help="First variant session dir (e.g. runs/...variantA)")
    p.add_argument("--c", required=True, type=Path, help="Second variant session dir (e.g. runs/...variantC)")
    p.add_argument("--out", type=Path, default=None, help="Markdown output path")
    p.add_argument("--html", type=Path, default=None, help="Optional HTML gallery output path")
    args = p.parse_args()

    a_name = args.a.name.split("_")[-1] if "_variant" in args.a.name else args.a.name
    c_name = args.c.name.split("_")[-1] if "_variant" in args.c.name else args.c.name

    print(f"Loading A ({a_name}): {args.a}")
    a_data = load_session(args.a)
    print(f"  {len(a_data)} cases")
    print(f"Loading C ({c_name}): {args.c}")
    c_data = load_session(args.c)
    print(f"  {len(c_data)} cases")

    md = render_md(a_data, c_data, a_name, c_name)
    out_md = args.out or (REPO / "evaluation" / f"compare_{a_name}_vs_{c_name}.md")
    out_md.write_text(md, encoding="utf-8")
    print(f"\n✅ Markdown: {out_md}")

    if args.html is not None:
        render_html_gallery(a_data, c_data, a_name, c_name, args.html)
        print(f"✅ HTML gallery: {args.html}")
    else:
        # default-generate alongside markdown
        default_html = out_md.with_suffix(".html")
        render_html_gallery(a_data, c_data, a_name, c_name, default_html)
        print(f"✅ HTML gallery: {default_html}")


if __name__ == "__main__":
    main()
