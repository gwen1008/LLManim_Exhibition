"""Aggregate stats from runs/merged_q01_q150_with_review.csv into stats.json.

Strict numbers — every aggregate has an explicit denominator (n=...) to avoid
the "average of unevaluated" optimism bias.
"""
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent
CSV_PATH = ROOT / "runs" / "merged_q01_q150_with_review.csv"
OUT_PATH = Path(__file__).parent / "static" / "data" / "stats.json"


def num(s, default=None):
    if not s or s in ("-", "N/A", ""):
        return default
    s = re.sub(r"[\$s,]", "", str(s).strip())
    m = re.match(r"(-?\d+(?:\.\d+)?)", s)
    return float(m.group(1)) if m else default


def main():
    rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8-sig")))
    n = len(rows)

    def col(key, cast=float):
        return [cast(num(r[key])) for r in rows if num(r[key]) is not None]

    iters = col("Iterations", int)
    cost = col("Cost USD")
    dur = col("Duration Sec")
    code_lines = col("Code Lines", int)
    vid_dur = col("Video Duration Sec")
    fj_math = col("FJ Math")
    verdict = Counter(r["FJ Verdict"] for r in rows)
    gt = Counter(r["FJ GT Match"] for r in rows)
    cat = Counter(r["Category"] for r in rows)
    iter_dist = Counter(iters)

    # Vision QA by category (P2 — layer the metric)
    elem_pass = sum(1 for r in rows if r["FJ Verdict"] == "PASS" and r["Category"] == "Elementary")
    elem_n = cat.get("Elementary", 0)
    mid_pass = sum(1 for r in rows if r["FJ Verdict"] == "PASS" and r["Category"] == "Middle")
    mid_n = cat.get("Middle", 0)

    # GT match: exclude unjudged (P0 — fix denominator bias)
    gt_true = gt.get("True", 0)
    gt_false = gt.get("False", 0)
    gt_judged_n = gt_true + gt_false
    gt_unjudged_n = n - gt_judged_n

    # Reflexion truth: split iter==1 vs iter>1 outcomes (P1 — narrative honesty)
    one_iter = [r for r in rows if int(r["Iterations"]) == 1]
    multi_iter = [r for r in rows if int(r["Iterations"]) > 1]
    one_iter_pass = sum(1 for r in one_iter if r["FJ Verdict"] == "PASS")
    multi_iter_pass = sum(1 for r in multi_iter if r["FJ Verdict"] == "PASS")
    multi_iter_fail = len(multi_iter) - multi_iter_pass

    tok_total = 0
    for r in rows:
        m = re.match(r"(\d+)", r["Total Tokens"].replace(",", ""))
        if m:
            tok_total += int(m.group(1))

    stats = {
        # Headline
        "total_videos_generated": n,
        "total_video_minutes": round(sum(vid_dur) / 60, 1),
        "total_cost_usd": round(sum(cost), 2),
        "total_compute_minutes": round(sum(dur) / 60, 1),
        "total_compute_hours": round(sum(dur) / 3600, 1),
        "total_tokens": tok_total,
        # Quality — Vision QA (overall + layered)
        "vision_qa_pass_rate": round(verdict.get("PASS", 0) / n, 3),
        "vision_qa_pass_elementary": round(elem_pass / elem_n, 3) if elem_n else 0,
        "vision_qa_pass_middle": round(mid_pass / mid_n, 3) if mid_n else 0,
        "vision_qa_elem_n": [elem_pass, elem_n],
        "vision_qa_mid_n": [mid_pass, mid_n],
        # Quality — GT (excluding unjudged)
        "gt_match_rate_judged": round(gt_true / gt_judged_n, 3) if gt_judged_n else 0,
        "gt_match_true": gt_true,
        "gt_match_false": gt_false,
        "gt_match_unjudged": gt_unjudged_n,
        "gt_judged_n": gt_judged_n,
        # Quality — FJ Math
        "fj_math_avg": round(sum(fj_math) / len(fj_math), 2) if fj_math else 0,
        "fj_math_n": len(fj_math),
        # Reflexion honest split
        "iter1_count": len(one_iter),
        "iter1_pass_count": one_iter_pass,
        "iter1_pass_rate": round(one_iter_pass / len(one_iter), 3),
        "iter_multi_count": len(multi_iter),
        "iter_multi_pass_count": multi_iter_pass,
        "iter_multi_fail_count": multi_iter_fail,
        "iter_multi_pass_rate": round(multi_iter_pass / len(multi_iter), 3) if multi_iter else 0,
        "iter_avg": round(sum(iters) / len(iters), 2),
        "iter_max": max(iters),
        "iter_distribution": {str(k): v for k, v in sorted(iter_dist.items())},
        # Per-video
        "cost_avg_usd": round(sum(cost) / len(cost), 3),
        "duration_avg_sec": round(sum(dur) / len(dur), 1),
        "code_lines_avg": round(sum(code_lines) / len(code_lines)),
        "video_duration_avg_sec": round(sum(vid_dur) / len(vid_dur), 1),
        "tokens_avg": tok_total // n,
        # Static
        "refining_loop_max_iterations": 5,
        "benchmark_pass_rate": f"{verdict.get('PASS', 0)}/{n}",
        "fj_fail_count": verdict.get("FAIL", 0),
        "fail_rate": round(verdict.get("FAIL", 0) / n, 3),
        # Agents
        "agents": [
            {"name": "Planner", "model": "claude-opus-4-8", "role": "視覺計畫 JSON"},
            {"name": "Coder", "model": "claude-opus-4-8", "role": "ManimCE 代碼生成"},
            {"name": "VisionQA", "model": "gpt-4o", "role": "渲染後視覺驗收"},
            {"name": "RefiningLoop", "model": "—", "role": "Reflexion 自動修正 (最多 5 輪)"},
        ],
    }

    OUT_PATH.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT_PATH}")
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
