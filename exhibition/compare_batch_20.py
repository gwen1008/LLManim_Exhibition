"""Detailed code-level comparison between naked Opus and full system for 20 topics."""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BATCH = HERE / "static" / "batch_20"
CSV = BATCH / "results.csv"


def analyze(path: Path) -> dict:
    if not path.exists():
        return {"missing": True}
    src = path.read_text(encoding="utf-8", errors="ignore")
    lines_total = src.count("\n")
    code_lines = sum(1 for l in src.splitlines() if l.strip() and not l.strip().startswith("#"))
    comment_lines = sum(1 for l in src.splitlines() if l.strip().startswith("#"))

    def count(pat):
        return len(re.findall(pat, src))

    return {
        "missing": False,
        "total_lines": lines_total,
        "code_lines": code_lines,
        "comments": comment_lines,
        "plays": count(r"self\.play\("),
        "waits": count(r"self\.wait\("),
        "for_loops": count(r"\bfor\s+\w+\s+in\s+"),
        "functions": count(r"^\s*def\s+\w+"),
        "rectangles": count(r"Rectangle\(|Square\("),
        "circles": count(r"Circle\(|Arc\("),
        "polygons": count(r"Polygon\(|Triangle\("),
        "arrows": count(r"Arrow\(|Vector\("),
        "lines": count(r"\bLine\("),
        "dots": count(r"\bDot\("),
        "mathtex": count(r"MathTex\("),
        "text": count(r"\bText\("),
        "axes": count(r"\bAxes\(|NumberPlane\("),
        "valuetrackers": count(r"ValueTracker\("),
        "always_redraw": count(r"always_redraw\("),
        "subtitles": count(r"set_subtitle\("),
        "is_3d": "ThreeDScene" in src or "set_camera_orientation" in src,
        "has_audio": "add_sound" in src,
    }


def fmt(v):
    if isinstance(v, bool):
        return "Y" if v else "·"
    return str(v) if v else "·"


def main():
    rows = list(csv.DictReader(open(CSV)))

    print("\n" + "=" * 100)
    print("DETAILED CODE COMPARISON — 20 TOPICS, NAKED vs SYSTEM")
    print("=" * 100)

    summary = []
    for r in rows:
        tid = r["id"]
        topic = r["topic"]
        np = BATCH / "naked" / f"{tid}.py"
        sp = BATCH / "system" / f"{tid}.py"
        n = analyze(np)
        s = analyze(sp)

        print(f"\n{'─'*100}")
        print(f"  {tid}  ·  {topic}")
        render_n = "✅" if r["naked_render"] == "True" else "❌"
        render_s = "✅" if r["sys_render"] == "True" else "❌"
        print(f"  Render: naked {render_n}   system {render_s}")

        if n.get("missing") or s.get("missing"):
            print(f"  ⚠️  source missing  (n={not n.get('missing')}, s={not s.get('missing')})")
            continue

        # Side-by-side table
        keys = [
            ("total_lines", "Lines"),
            ("plays", "Animations (self.play)"),
            ("waits", "Waits (self.wait)"),
            ("for_loops", "For loops"),
            ("functions", "Function defs"),
            ("rectangles", "Rectangles"),
            ("circles", "Circles/Arcs"),
            ("polygons", "Polygons"),
            ("arrows", "Arrows/Vectors"),
            ("dots", "Dots"),
            ("mathtex", "MathTex (公式)"),
            ("text", "Text"),
            ("axes", "Axes"),
            ("valuetrackers", "ValueTracker"),
            ("always_redraw", "always_redraw"),
            ("subtitles", "Subtitles (旁白)"),
            ("is_3d", "3D scene"),
            ("has_audio", "Has audio"),
        ]
        print(f"    {'metric':<22} {'naked':>10} {'system':>10}  delta")
        for k, label in keys:
            nv, sv = n[k], s[k]
            if isinstance(nv, bool):
                delta = ""
            else:
                if sv == nv:
                    delta = "="
                elif sv > nv:
                    delta = f"+{sv-nv}"
                else:
                    delta = f"-{nv-sv}"
            print(f"    {label:<22} {fmt(nv):>10} {fmt(sv):>10}  {delta}")

        # Save summary row
        winner = "system" if (r["sys_render"] == "True" and r["naked_render"] != "True") else (
            "system" if s["subtitles"] > 0 and n["subtitles"] == 0 else "tie"
        )
        summary.append({
            "id": tid,
            "topic": topic,
            "naked_render": r["naked_render"],
            "n_lines": n["total_lines"],
            "s_lines": s["total_lines"],
            "n_plays": n["plays"],
            "s_plays": s["plays"],
            "n_subs": n["subtitles"],
            "s_subs": s["subtitles"],
            "winner": winner,
        })

    # Final summary
    print(f"\n{'='*100}\nSUMMARY (sorted by drama potential)\n{'='*100}")
    # Sort: naked fails first, then by line ratio
    def drama_score(row):
        n_fail = row["naked_render"] == "False"
        line_ratio = row["s_lines"] / max(row["n_lines"], 1)
        return (-int(n_fail), -line_ratio)

    summary.sort(key=drama_score)
    print(f"  {'ID':<22} {'render':<14} {'lines(n→s)':<14} {'plays(n→s)':<12} {'subs(n→s)'}")
    print(f"  {'-'*80}")
    for r in summary:
        rn = "❌" if r["naked_render"] == "False" else "✅"
        print(f"  {r['id']:<22} {rn} → ✅      {r['n_lines']:>3} → {r['s_lines']:<5}     {r['n_plays']:>2} → {r['s_plays']:<5}    {r['n_subs']} → {r['s_subs']}")


if __name__ == "__main__":
    main()
