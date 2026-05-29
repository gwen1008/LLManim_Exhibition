"""Test Planner Lite on 5 selected topics — compare against existing system & naked.

Output:
  exhibition/static/batch_20/lite/{id}.mp4   ← new Lite videos
  exhibition/static/batch_20/lite/{id}.py    ← source
  exhibition/static/batch_20/lite_results.json
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
RUNS_DIR = HERE / "static" / "runs"
BATCH = HERE / "static" / "batch_20"
LITE_DIR = BATCH / "lite"
LITE_RESULTS = BATCH / "lite_results.json"
RESULTS_CSV = BATCH / "results.csv"
LITE_RUNNER = HERE / "full_system_lite_runner.py"


# 5 representative topics across difficulty bands
TEST_TOPICS = ["Q01_riemann_sum", "Q07_unit_roots", "Q10_sierpinski", "Q19_mandelbrot", "Q16_lorenz"]


def _probe(p: Path):
    if not p.exists(): return None, None
    size_kb = round(p.stat().st_size / 1024)
    try:
        ff = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=duration", "-of", "json", str(p)],
            capture_output=True, text=True, timeout=30,
        )
        dur = round(float(json.loads(ff.stdout)["streams"][0]["duration"]), 2)
        return dur, size_kb
    except Exception:
        return None, size_kb


def run_lite(topic_id: str, prompt: str) -> dict:
    task_id = f"lite_{topic_id}_{int(time.time())}"
    out_dir = RUNS_DIR / task_id
    out_dir.mkdir(parents=True, exist_ok=True)
    target_file = ROOT / f"test_script_{task_id}.py"

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["TASK_TARGET_FILE"] = str(target_file)

    print(f"  ▶ LITE: {topic_id}", end="", flush=True)
    t0 = time.time()
    proc = subprocess.run(
        [sys.executable, str(LITE_RUNNER), task_id, str(out_dir)],
        input=prompt + "\n",
        text=True,
        capture_output=True,
        env=env,
        timeout=900,
    )
    dur = time.time() - t0

    render_success = any(l.startswith("[VIDEO] ") for l in proc.stdout.splitlines())

    # Preserve source.py
    if target_file.exists():
        shutil.copy2(str(target_file), str(out_dir / "source.py"))
    try:
        target_file.unlink(missing_ok=True)
    except Exception:
        pass

    # Copy to canonical
    LITE_DIR.mkdir(parents=True, exist_ok=True)
    if render_success:
        src_v = out_dir / "video.mp4"
        if src_v.exists():
            shutil.copy2(str(src_v), str(LITE_DIR / f"{topic_id}.mp4"))
    src_py = out_dir / "source.py"
    if src_py.exists():
        shutil.copy2(str(src_py), str(LITE_DIR / f"{topic_id}.py"))

    vid_dur, vid_kb = _probe(LITE_DIR / f"{topic_id}.mp4") if render_success else (None, None)

    # Count subtitles in source
    subs = 0
    plays = 0
    lines = 0
    py = LITE_DIR / f"{topic_id}.py"
    if py.exists():
        import re
        src = py.read_text(encoding="utf-8", errors="ignore")
        lines = src.count("\n")
        plays = len(re.findall(r"self\.play\(", src))
        subs = len(re.findall(r"set_subtitle\(", src))

    print(f"  {'✅' if render_success else '❌'} {dur:.0f}s, video {vid_dur}s, {lines} lines, {subs} subs")

    # Stderr tail if failed
    stderr_tail = ""
    if not render_success and proc.stderr:
        stderr_tail = "\n".join(proc.stderr.splitlines()[-10:])[-500:]

    return {
        "render": render_success,
        "gen_time_sec": round(dur, 1),
        "video_dur_sec": vid_dur,
        "video_kb": vid_kb,
        "code_lines": lines,
        "animations": plays,
        "subtitles": subs,
        "stderr_tail": stderr_tail if not render_success else "",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", help="Comma-separated topic IDs, default 5 test set")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    rows = list(csv.DictReader(open(RESULTS_CSV, encoding="utf-8")))
    by_id = {r["id"]: r for r in rows}

    if args.items:
        wanted = args.items.split(",")
        targets = [by_id[i] for i in wanted if i in by_id]
    else:
        targets = [by_id[i] for i in TEST_TOPICS if i in by_id]

    print(f"Running Planner Lite on {len(targets)} topics...")
    print(f"Test set: {[t['id'] for t in targets]}\n")

    done = {}
    if LITE_RESULTS.exists():
        done = json.loads(LITE_RESULTS.read_text(encoding="utf-8"))
        print(f"Already done: {len(done)} (use --force to re-run)\n")

    t_global = time.time()
    for i, r in enumerate(targets, 1):
        tid = r["id"]
        print(f"[{i}/{len(targets)}] {tid}  ·  {r['topic']}")
        if tid in done and not args.force:
            print(f"  ⏭️  cached")
            continue

        result = run_lite(tid, r["prompt"])
        # Also save naked + sys comparison row for context
        result["topic"] = r["topic"]
        result["naked_render"] = r["naked_render"]
        result["naked_video_sec"] = r.get("naked_video_sec", "")
        result["sys_render"] = r["sys_render"]
        result["sys_video_sec"] = r.get("sys_video_sec", "")
        result["sys_lines"] = r.get("sys_lines", "")
        result["sys_subs"] = r.get("sys_subtitles", "")
        done[tid] = result
        LITE_RESULTS.write_text(json.dumps(done, ensure_ascii=False, indent=2), encoding="utf-8")

    elapsed = time.time() - t_global

    # Final summary
    print(f"\n{'='*80}")
    print(f"PLANNER LITE TEST DONE in {elapsed/60:.1f} min")
    print(f"{'='*80}")
    print(f"  {'ID':<22} {'lite':<6} {'naked':<7} {'sys':<6} {'lite_dur':<9} {'lite_lines':<10} {'lite_subs'}")
    print(f"  {'-'*80}")
    for tid, d in done.items():
        lr = "✅" if d["render"] else "❌"
        nr = "✅" if d.get("naked_render") == "True" else "❌"
        sr = "✅" if d.get("sys_render") == "True" else "❌"
        ld = d.get("video_dur_sec") or "—"
        ll = d.get("code_lines") or "—"
        ls = d.get("subtitles") or "—"
        print(f"  {tid:<22} {lr:<6} {nr:<7} {sr:<6} {str(ld)+'s':<9} {ll:<10} {ls}")

    print(f"\nResults: {LITE_RESULTS}")
    print(f"Videos:  {LITE_DIR}/")


if __name__ == "__main__":
    main()
