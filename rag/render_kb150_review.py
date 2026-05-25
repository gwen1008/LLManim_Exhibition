"""Render all kb150 Scenes for human review + log rubric scores.

Workflow:
  1. python rag/render_kb150_review.py render     # batch render all 29 scenes (-ql)
  2. python rag/render_kb150_review.py review     # interactive rubric scoring
  3. python rag/render_kb150_review.py report     # summary of scores + flagged

Output:
  runs/kb150_review/<chapter>/<scene>.mp4
  evaluation/kb150_review_log.json

Rubric (each 0/1, total 0-5):
  clean   : 畫面乾淨無殘留、無重疊
  steps   : 教學步驟清晰
  visual  : 視覺對應數學意義（顏色/位置）
  latex   : LaTeX 排版正確無斷裂
  pacing  : 節奏合理
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KB_ROOT = REPO_ROOT / "knowledge_base" / "kb150"
DEFAULT_OUT_ROOT = REPO_ROOT / "runs" / "kb150_review"
DEFAULT_LOG_PATH = REPO_ROOT / "evaluation" / "kb150_review_log.json"

RUBRIC = ["clean", "steps", "visual", "latex", "pacing"]


def list_scenes(kb_root: Path) -> list[tuple[Path, str, str]]:
    """Return [(file_path, chapter, scene_name)] for all .py files under kb_root."""
    items = []
    for py in sorted(kb_root.rglob("*.py")):
        chapter = py.parent.name
        scene = py.stem
        items.append((py, chapter, scene))
    return items


def render_one(py_path: Path, chapter: str, scene: str, out_root: Path) -> tuple[bool, str]:
    """Render a single scene at -ql to <out_root>/<chapter>/."""
    out_dir = out_root / chapter
    out_dir.mkdir(parents=True, exist_ok=True)
    target_mp4 = out_dir / f"{scene}.mp4"
    if target_mp4.exists():
        try:
            disp = target_mp4.relative_to(REPO_ROOT)
        except ValueError:
            disp = target_mp4
        return True, f"skip (exists): {disp}"

    cmd = [
        "manim", "-ql",
        "--media_dir", str(out_dir / "_media"),
        "-o", scene,
        str(py_path), scene,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        # persist stderr for debugging timeout cases
        err_dir = out_root / "_errors"
        err_dir.mkdir(parents=True, exist_ok=True)
        (err_dir / f"{scene}.log").write_text("TIMEOUT 180s — manim hang (likely LaTeX compile stuck)\n",
                                              encoding="utf-8")
        return False, "TIMEOUT (180s)"
    if result.returncode != 0:
        err_dir = out_root / "_errors"
        err_dir.mkdir(parents=True, exist_ok=True)
        (err_dir / f"{scene}.log").write_text(result.stderr or "<empty stderr>", encoding="utf-8")
        tail = result.stderr.strip().splitlines()[-5:]
        return False, "RENDER FAIL: " + " | ".join(tail)

    # manim writes to _media/videos/<scene_file>/480p15/<scene>.mp4
    produced = list((out_dir / "_media").rglob(f"{scene}.mp4"))
    if not produced:
        return False, "no mp4 produced"
    produced[0].rename(target_mp4)
    try:
        disp = target_mp4.relative_to(REPO_ROOT)
    except ValueError:
        disp = target_mp4
    return True, f"ok: {disp}"


def cmd_render(kb_root: Path, out_root: Path):
    scenes = list_scenes(kb_root)
    try:
        out_disp = out_root.relative_to(REPO_ROOT)
    except ValueError:
        out_disp = out_root
    print(f"Rendering {len(scenes)} scenes from {kb_root} → {out_disp}/")
    ok = fail = 0
    for py, chapter, scene in scenes:
        success, msg = render_one(py, chapter, scene, out_root)
        flag = "✅" if success else "❌"
        print(f"  {flag} [{chapter}/{scene}] {msg}")
        if success:
            ok += 1
        else:
            fail += 1
    print(f"\nDone. {ok} ok, {fail} fail.")
    if fail:
        print(f"  → check error logs in {out_root / '_errors'}/")


def load_log(log_path: Path) -> dict:
    if log_path.exists():
        return json.loads(log_path.read_text(encoding="utf-8"))
    return {}


def save_log(log: dict, log_path: Path):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_review(kb_root: Path, out_root: Path, log_path: Path,
               chapter_filter: str | None = None, redo: bool = False):
    log = load_log(log_path)
    scenes = list_scenes(kb_root)
    if chapter_filter:
        scenes = [s for s in scenes if s[1] == chapter_filter]
        print(f"Filtering chapter={chapter_filter} → {len(scenes)} scenes")

    for py, chapter, scene in scenes:
        key = f"{chapter}/{scene}"
        if key in log and not redo:
            continue
        mp4 = out_root / chapter / f"{scene}.mp4"
        if not mp4.exists():
            print(f"  ⚠️  no mp4 for {key}; run render first")
            continue

        print(f"\n{'='*60}")
        print(f"📹 {key}")
        print(f"   open: {mp4}")
        try:
            print(f"   code: {py.relative_to(REPO_ROOT)}")
        except ValueError:
            print(f"   code: {py}")
        print(f"{'='*60}")

        # macOS quick open
        try:
            subprocess.Popen(["open", str(mp4)])
        except Exception:
            pass

        print(f"Rubric ({'/'.join(RUBRIC)}) — enter 5 digits 0/1, e.g. 11011")
        print(f"  or 'q' to quit, 's' to skip, 'r' to replay")
        scores = None
        while scores is None:
            raw = input("> ").strip().lower()
            if raw == "q":
                save_log(log, log_path)
                print("Saved. Bye.")
                return
            if raw == "s":
                break
            if raw == "r":
                subprocess.Popen(["open", str(mp4)])
                continue
            if len(raw) == 5 and all(c in "01" for c in raw):
                scores = {RUBRIC[i]: int(raw[i]) for i in range(5)}
            else:
                print("  invalid; need 5 chars of 0/1")

        if scores is None:
            continue

        note = input("Note (free text, blank ok): ").strip()
        log[key] = {
            "scores": scores,
            "total": sum(scores.values()),
            "note": note,
        }
        save_log(log, log_path)
        print(f"  💾 saved (total={log[key]['total']}/5)")

    print("\n✅ Review pass complete.")


def cmd_report(log_path: Path):
    log = load_log(log_path)
    if not log:
        print("No log. Run review first.")
        return

    by_total: dict[int, list[str]] = {}
    by_rule_fails: dict[str, list[str]] = {r: [] for r in RUBRIC}
    for key, entry in log.items():
        by_total.setdefault(entry["total"], []).append(key)
        for rule, val in entry["scores"].items():
            if val == 0:
                by_rule_fails[rule].append(key)

    total_reviewed = len(log)
    avg = sum(e["total"] for e in log.values()) / total_reviewed
    print(f"Reviewed: {total_reviewed} | Avg score: {avg:.2f}/5\n")

    print("By total score:")
    for score in sorted(by_total.keys()):
        items = by_total[score]
        print(f"  {score}/5  ({len(items)}):  {', '.join(items[:3])}{'...' if len(items)>3 else ''}")

    print("\nFails by rubric item:")
    for rule in RUBRIC:
        fails = by_rule_fails[rule]
        print(f"  {rule:8s} fail: {len(fails)}  {', '.join(fails[:5])}{'...' if len(fails)>5 else ''}")

    needs_redo = [k for k, e in log.items() if e["total"] < 4]
    print(f"\n⚠️  Needs rework (<4/5): {len(needs_redo)}")
    for k in needs_redo:
        e = log[k]
        print(f"  {e['total']}/5  {k}  — {e.get('note','')[:50]}")


def _add_path_args(parser):
    parser.add_argument("--kb-path", type=Path, default=DEFAULT_KB_ROOT,
                        help=f"KB root (default: {DEFAULT_KB_ROOT.relative_to(REPO_ROOT)})")
    parser.add_argument("--out-root", type=Path, default=None,
                        help="Render output root (default: runs/<kb-folder-name>_review)")
    parser.add_argument("--log-path", type=Path, default=None,
                        help="Review log path (default: evaluation/<kb-folder-name>_review_log.json)")


def _resolve_paths(args) -> tuple[Path, Path, Path]:
    kb_root = args.kb_path
    kb_name = kb_root.name  # e.g. "kb150" or "kb150_v2"
    out_root = args.out_root if args.out_root else REPO_ROOT / "runs" / f"{kb_name}_review"
    log_path = args.log_path if args.log_path else REPO_ROOT / "evaluation" / f"{kb_name}_review_log.json"
    return kb_root, out_root, log_path


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    rd = sub.add_parser("render")
    _add_path_args(rd)

    rv = sub.add_parser("review")
    _add_path_args(rv)
    rv.add_argument("--chapter", default=None, help="filter by chapter folder name")
    rv.add_argument("--redo", action="store_true", help="re-score already-scored scenes")

    rp = sub.add_parser("report")
    _add_path_args(rp)

    args = p.parse_args()
    kb_root, out_root, log_path = _resolve_paths(args)

    if args.cmd == "render":
        cmd_render(kb_root, out_root)
    elif args.cmd == "review":
        cmd_review(kb_root, out_root, log_path,
                   chapter_filter=args.chapter, redo=args.redo)
    elif args.cmd == "report":
        cmd_report(log_path)


if __name__ == "__main__":
    main()
