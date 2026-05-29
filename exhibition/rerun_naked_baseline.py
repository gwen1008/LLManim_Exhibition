"""Re-run Gallery Q01-Q10 baseline videos using the new naked_opus.py runner.

For each gallery item:
1. Invoke naked_opus.py with item.topic_prompt as stdin
2. On success → copy generated video to static/videos/naked_opus/{id}.mp4
3. Update gallery.json's opus_metrics in-place
4. Print summary

Run from project root:
    .venv/bin/python exhibition/rerun_naked_baseline.py [--items Q01,Q02,...]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
GALLERY_JSON = HERE / "static" / "data" / "gallery.json"
VIDEOS_DIR = HERE / "static" / "videos" / "naked_opus"
RUNS_DIR = HERE / "static" / "runs"
RUNNER = HERE / "naked_opus.py"


def run_one(item_id: str, prompt: str) -> dict:
    """Run naked_opus.py for one topic and return metrics dict."""
    task_id = f"naked_{item_id}_{int(time.time())}"
    out_dir = RUNS_DIR / task_id
    out_dir.mkdir(parents=True, exist_ok=True)

    target_file = ROOT / f"test_script_{task_id}.py"

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["TASK_TARGET_FILE"] = str(target_file)

    print(f"\n{'='*60}")
    print(f"▶  {item_id}: {prompt[:80]}...")
    print(f"{'='*60}")

    t0 = time.time()
    proc = subprocess.run(
        [sys.executable, str(RUNNER), task_id, str(out_dir)],
        input=prompt + "\n",
        text=True,
        capture_output=True,
        env=env,
        timeout=600,
    )
    dur = time.time() - t0

    # Parse runner stdout markers
    render_success = False
    error_notes = ""
    for line in proc.stdout.splitlines():
        print(f"  {line}")
        if line.startswith("[VIDEO] "):
            render_success = True
        elif line.startswith("[RENDER_ERROR] "):
            error_notes = line[15:].strip()
        elif line.startswith("[ERROR] "):
            error_notes = line[8:].strip()

    if proc.returncode != 0 and not render_success:
        # capture last stderr lines for diagnostic
        stderr_tail = "\n".join(proc.stderr.splitlines()[-15:])
        if not error_notes:
            error_notes = stderr_tail[-800:]

    # Compute code lines + video duration
    code_lines = None
    if target_file.exists():
        try:
            code_lines = sum(1 for _ in open(target_file, encoding="utf-8"))
        except Exception:
            pass

    video_duration_sec = None
    video_resolution = None
    if render_success:
        # Source video lives in RUNS_DIR/task_id/video.mp4
        src = out_dir / "video.mp4"
        if src.exists():
            # Copy to canonical location
            dest = VIDEOS_DIR / f"{item_id}.mp4"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src), str(dest))

            # Get duration + resolution via ffprobe
            try:
                ff = subprocess.run(
                    [
                        "ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height,duration",
                        "-of", "json", str(dest),
                    ],
                    capture_output=True, text=True, timeout=30,
                )
                info = json.loads(ff.stdout)["streams"][0]
                video_duration_sec = round(float(info.get("duration", 0)), 2)
                video_resolution = f"{info['width']}x{info['height']}"
            except Exception as e:
                print(f"  ⚠️  ffprobe failed: {e}")

    # Cleanup target file
    try:
        target_file.unlink(missing_ok=True)
    except Exception:
        pass

    metrics = {
        "render_success": render_success,
        "gen_time_sec": round(dur, 2),
        "code_lines": code_lines,
        "video_duration_sec": video_duration_sec,
        "video_resolution": video_resolution,
        "notes": "Zero-shot naked Opus (28-word system prompt)" + (
            f" — render failed: {error_notes[:300]}" if not render_success else ""
        ),
    }
    status = "✅" if render_success else "❌"
    print(f"  {status} {item_id}: render={render_success} time={dur:.1f}s lines={code_lines} dur={video_duration_sec}s")
    return metrics


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", help="Comma-separated item IDs (e.g. Q01,Q02). Default: all 10")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    gallery = json.loads(GALLERY_JSON.read_text(encoding="utf-8"))
    items = gallery["items"]
    if args.items:
        wanted = set(args.items.split(","))
        items = [i for i in items if any(i["id"].startswith(w) for w in wanted)]
        print(f"Filtered to {len(items)} items")

    if args.dry_run:
        for it in items:
            print(f"  would rerun {it['id']}: {it['topic_prompt'][:60]}...")
        return

    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

    results = {}
    for it in items:
        try:
            metrics = run_one(it["id"], it["topic_prompt"])
        except Exception as e:
            metrics = {
                "render_success": False,
                "gen_time_sec": None,
                "code_lines": None,
                "video_duration_sec": None,
                "video_resolution": None,
                "notes": f"runner crashed: {e}",
            }
        results[it["id"]] = metrics
        # Update gallery.json item in-place
        it["opus_metrics"] = {
            **metrics,
            # preserve fields that may not be re-computed
            "render_duration_sec": metrics.get("gen_time_sec"),
            "vision_qa_verdict": None,
            "llm_call_count": 1,
            "total_prompt_tokens": None,
            "total_completion_tokens": None,
            "refining_iterations": 0,
            "rag_examples_retrieved": 0,
        }
        # Save incrementally
        GALLERY_JSON.write_text(json.dumps(gallery, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  💾 gallery.json updated for {it['id']}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    succ = sum(1 for m in results.values() if m["render_success"])
    print(f"Render success: {succ}/{len(results)}")
    for k, m in results.items():
        flag = "✅" if m["render_success"] else "❌"
        print(f"  {flag} {k}: {m.get('gen_time_sec','?')}s, {m.get('code_lines','?')} lines")


if __name__ == "__main__":
    main()
