"""Score each topic on 4 dimensions to rank "system vs naked" drama.

Total = A + B + C + D (max 100):
  A. Render Gap        (40 pts) — naked fail = max drama
  B. Code Depth Gap    (25 pts) — system 多寫多少代碼
  C. Animation Gap     (20 pts) — system 動畫密度
  D. Visual Diversity  (15 pts) — system 用多少種 mobject
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BATCH = HERE / "static" / "batch_20"
CSV_FILE = BATCH / "results.csv"


def analyze(path: Path) -> dict:
    if not path.exists():
        return None
    src = path.read_text(encoding="utf-8", errors="ignore")
    def c(p): return len(re.findall(p, src))
    return {
        "lines": src.count("\n"),
        "plays": c(r"self\.play\("),
        "for_loops": c(r"\bfor\s+\w+\s+in\s+"),
        "objects": {
            "MathTex": c(r"MathTex\("),
            "Text": c(r"\bText\("),
            "Rectangle": c(r"Rectangle\(|Square\("),
            "Circle": c(r"Circle\(|Arc\("),
            "Polygon": c(r"Polygon\(|Triangle\("),
            "Arrow": c(r"Arrow\(|Vector\("),
            "Dot": c(r"\bDot\("),
            "Axes": c(r"\bAxes\(|NumberPlane\("),
            "ValueTracker": c(r"ValueTracker\("),
        },
        "is_3d": "ThreeDScene" in src or "set_camera_orientation" in src,
    }


def score_render_gap(naked_render: bool, naked_video_sec: float | None) -> int:
    """0-40: naked fail = 40, naked short = 25, naked OK = 10."""
    if not naked_render:
        return 40
    if naked_video_sec is None:
        return 30
    if naked_video_sec < 12:
        return 25
    if naked_video_sec < 18:
        return 18
    if naked_video_sec < 25:
        return 10
    return 5


def score_code_gap(n_lines: int, s_lines: int) -> int:
    """0-25: based on line ratio."""
    if n_lines == 0:
        return 25
    ratio = s_lines / n_lines
    if ratio >= 5: return 25
    if ratio >= 4: return 20
    if ratio >= 3: return 15
    if ratio >= 2: return 10
    return 5


def score_animation_gap(n_plays: int, s_plays: int) -> int:
    """0-20: animation density."""
    if s_plays - n_plays >= 6: return 20
    if s_plays - n_plays >= 4: return 15
    if s_plays - n_plays >= 2: return 10
    if s_plays >= n_plays: return 5
    return 0


def score_diversity(naked_obj: dict, sys_obj: dict) -> int:
    """0-15: how many object types system uses that naked doesn't."""
    n_types = sum(1 for v in naked_obj.values() if v > 0)
    s_types = sum(1 for v in sys_obj.values() if v > 0)
    diff = s_types - n_types
    if diff >= 4: return 15
    if diff >= 3: return 12
    if diff >= 2: return 9
    if diff >= 1: return 6
    if diff >= 0: return 3
    return 0


def grade(score: int) -> str:
    if score >= 85: return "S"
    if score >= 70: return "A"
    if score >= 55: return "B"
    if score >= 40: return "C"
    if score >= 25: return "D"
    return "F"


def main():
    rows = list(csv.DictReader(open(CSV_FILE)))
    scored = []

    for r in rows:
        tid = r["id"]
        np_ = BATCH / "naked" / f"{tid}.py"
        sp = BATCH / "system" / f"{tid}.py"
        n = analyze(np_)
        s = analyze(sp)
        if not n or not s:
            continue

        nv = float(r["naked_video_sec"]) if r["naked_video_sec"] else None

        A = score_render_gap(r["naked_render"] == "True", nv)
        B = score_code_gap(n["lines"], s["lines"])
        C = score_animation_gap(n["plays"], s["plays"])
        D = score_diversity(n["objects"], s["objects"])
        total = A + B + C + D

        scored.append({
            "id": tid,
            "topic": r["topic"],
            "naked_render": r["naked_render"] == "True",
            "naked_dur": nv,
            "n_lines": n["lines"],
            "s_lines": s["lines"],
            "n_plays": n["plays"],
            "s_plays": s["plays"],
            "n_types": sum(1 for v in n["objects"].values() if v > 0),
            "s_types": sum(1 for v in s["objects"].values() if v > 0),
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "total": total,
            "grade": grade(total),
        })

    scored.sort(key=lambda x: -x["total"])

    print("\n" + "=" * 110)
    print("SYSTEM vs NAKED — DRAMA SCORE RANKING (max 100)")
    print("  A=Render Gap(40)  B=Code Gap(25)  C=Anim Gap(20)  D=Diversity(15)")
    print("=" * 110)
    print(f"  {'#':<3} {'ID':<22} {'Topic':<22} {'A':>4} {'B':>4} {'C':>4} {'D':>4} {'TOTAL':>6} {'GRADE':>6}")
    print("  " + "-" * 100)
    for i, r in enumerate(scored, 1):
        print(f"  {i:<3} {r['id']:<22} {r['topic']:<22} {r['A']:>4} {r['B']:>4} {r['C']:>4} {r['D']:>4} {r['total']:>6}    {r['grade']:>4}")

    # Grade distribution
    print("\n  Grade distribution:")
    from collections import Counter
    gd = Counter(r["grade"] for r in scored)
    for g in ["S", "A", "B", "C", "D", "F"]:
        if gd[g]:
            print(f"    {g}: {gd[g]}")

    # Top 10 picks
    print(f"\n{'='*110}")
    print(f"🏆 TOP 10 RECOMMENDED FOR GALLERY (highest drama)")
    print(f"{'='*110}")
    for i, r in enumerate(scored[:10], 1):
        rstat = "❌" if not r["naked_render"] else f"{r['naked_dur']:.0f}s"
        print(f"  {i:>2}. {r['id']:<22}  {r['grade']} ({r['total']})  naked={rstat:<6}  lines {r['n_lines']:>3}→{r['s_lines']}  plays {r['n_plays']}→{r['s_plays']}")

    # Aggregate
    print(f"\n{'='*110}")
    print(f"AGGREGATE")
    print(f"{'='*110}")
    avg_A = sum(r["A"] for r in scored) / len(scored)
    avg_B = sum(r["B"] for r in scored) / len(scored)
    avg_C = sum(r["C"] for r in scored) / len(scored)
    avg_D = sum(r["D"] for r in scored) / len(scored)
    avg_total = sum(r["total"] for r in scored) / len(scored)
    print(f"  Average Drama Score: {avg_total:.1f} / 100  ({grade(int(avg_total))})")
    print(f"  Breakdown: A={avg_A:.1f}/40  B={avg_B:.1f}/25  C={avg_C:.1f}/20  D={avg_D:.1f}/15")


if __name__ == "__main__":
    main()
