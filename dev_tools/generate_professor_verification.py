#!/usr/bin/env python3
"""Generate a professor review packet for high-overlap evaluation cases.

Outputs to /tmp by default so we never create repo artifacts under runs/.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from agents.utils.telemetry import compute_iou_summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate professor verification markdown from an eval run")
    parser.add_argument("session_dir", help="Path to a run session directory, e.g. runs/20260402_102257")
    parser.add_argument("--top-k", type=int, default=5, help="Number of highest-overlap success cases to include")
    parser.add_argument(
        "--output",
        type=str,
        help="Output markdown path. Defaults to /tmp/professor_verification_<session>.md",
    )
    return parser.parse_args()


def load_summary_rows(session_dir: Path) -> list[dict]:
    summary_csv = session_dir / "summary.csv"
    with open(summary_csv, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def pick_top_cases(rows: list[dict], top_k: int) -> list[dict]:
    success = [
        row for row in rows
        if row.get("Status") == "Success" and row.get("Max Overlap Pairs", "").strip()
    ]
    success.sort(key=lambda row: int(row["Max Overlap Pairs"]), reverse=True)
    return success[:top_k]


def build_markdown(session_dir: Path, cases: list[dict]) -> str:
    lines = [
        "# 教授驗證包：高 Overlap 案例分析",
        "",
        f"**Session**: `{session_dir}`",
        "",
        "請逐案標註：",
        "1. 是否真的有「物件擋住」問題？",
        "2. 類型：`label overlap` / `overflow` / `z-order` / `只是畫面擠` / `沒問題`",
        "3. 問題發生的大約時間點？",
        "4. 除了物件擋住，還有沒有其他你在意的影片品質問題？",
        "",
        "---",
        "",
    ]

    for idx, row in enumerate(cases, start=1):
        case_id = row["Case ID"]
        topic = row["Topic"]
        case_dir = session_dir / case_id
        log_path = case_dir / "scene_state_log.json"
        video_path = case_dir / "video.mp4"

        with open(log_path, encoding="utf-8") as f:
            log = json.load(f)
        summary = compute_iou_summary(log)

        lines.extend([
            f"## Case {idx}: {case_id}",
            f"**題目**: {topic}",
            "",
            f"**影片**: `{video_path}`",
            "",
            f"**原始 AABB Overlap**: max_pairs={row['Max Overlap Pairs']}, steps={row['Steps with Overlap']}",
            f"**IoU-filtered Overlap**: max_pairs={summary['iou_overlap_pairs_max']}, "
            f"steps={summary['steps_with_iou_overlap']}/{summary['total_steps']}",
            f"**Worst overlap step**: {summary['worst_overlap_step']}/{summary['total_steps']} "
            f"(~{summary['worst_overlap_step_pct']:.0%} of animation)",
            "",
        ])

        if summary["top_overlap_pairs"]:
            lines.append("**Top overlap pairs (by IoU)**:")
            for pair in summary["top_overlap_pairs"]:
                lines.append(f"- {pair['type_a']} + {pair['type_b']}: IoU={pair['iou']:.2f}")
            lines.append("")

        lines.extend([
            "### 教授標註",
            "- [ ] 有物件擋住問題",
            "- 類型：________________",
            "- 時間點：________________",
            "- 其他品質問題：________________",
            "",
            "---",
            "",
        ])

    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    session_dir = Path(args.session_dir).resolve()
    output_path = Path(args.output).resolve() if args.output else Path(f"/tmp/professor_verification_{session_dir.name}.md")

    rows = load_summary_rows(session_dir)
    cases = pick_top_cases(rows, args.top_k)
    markdown = build_markdown(session_dir, cases)

    output_path.write_text(markdown, encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
