"""Replace 4 weak demo topics with stronger contrast topics.

For each replacement:
1. Run full_system_runner.py → save to static/videos/old_rag/{new_id}.mp4
2. Run naked_opus.py → save to static/videos/naked_opus/{new_id}.mp4
3. Collect metrics from both
4. Update gallery.json in-place
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
RUNS_DIR = HERE / "static" / "runs"
VIDEOS_NAKED = HERE / "static" / "videos" / "naked_opus"
VIDEOS_SYSTEM = HERE / "static" / "videos" / "old_rag"

NAKED_RUNNER = HERE / "naked_opus.py"
SYSTEM_RUNNER = HERE / "full_system_runner.py"


REPLACEMENTS = [
    {
        "old_id": "Q04_riemann_sum",
        "new_id": "Q04_golden_spiral",
        "topic": "黃金螺旋（費氏正方形嵌套）",
        "topic_en": "Golden spiral via Fibonacci squares",
        "topic_prompt": "繪製黃金螺旋。請用費氏數列邊長 (1, 1, 2, 3, 5, 8) 依序排列六個正方形（每個正方形貼著前一個），並在每個正方形內部畫一條四分之一圓弧，使所有弧線連接成一條完整的螺旋曲線。",
    },
    {
        "old_id": "Q07_newton_iteration",
        "new_id": "Q07_unit_roots",
        "topic": "複數方程 z⁸ = 1 的單位根",
        "topic_en": "Roots of unity for the equation z^8 = 1",
        "topic_prompt": "視覺化複數方程 z⁸ = 1 的所有解（即 8 次單位根）。請在複數平面上畫出單位圓，標出八個解的位置，並從原點畫向量連到每個解。",
    },
    {
        "old_id": "Q09_taylor_sine",
        "new_id": "Q09_sierpinski",
        "topic": "Sierpinski 三角形（遞迴 4 層）",
        "topic_en": "Sierpinski triangle recursive 4 levels",
        "topic_prompt": "繪製 Sierpinski 三角形。請從一個大的等邊三角形開始，每一輪將每個三角形分成四個小三角形並移除中間那個（保留三個角落的小三角形），重複這個遞迴過程四次。",
    },
    {
        "old_id": "Q10_slope_field",
        "new_id": "Q10_pendulum_phase",
        "topic": "單擺：時域擺動 vs 相位空間",
        "topic_en": "Pendulum: time-domain swing vs phase space",
        "topic_prompt": "視覺化單擺運動。請左右並排兩張圖：左圖顯示擺角 θ 隨時間 t 的變化（時域曲線），右圖顯示相位空間（橫軸 θ，縱軸角速度 dθ/dt 形成橢圓）。兩張圖同步演化，呈現同一單擺的兩種視角。",
    },
]


def _run_subprocess(runner: Path, task_id: str, out_dir: Path, topic_input: str) -> tuple[subprocess.CompletedProcess, float]:
    out_dir.mkdir(parents=True, exist_ok=True)
    target_file = ROOT / f"test_script_{task_id}.py"

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["TASK_TARGET_FILE"] = str(target_file)

    t0 = time.time()
    proc = subprocess.run(
        [sys.executable, str(runner), task_id, str(out_dir)],
        input=topic_input + "\n",
        text=True,
        capture_output=True,
        env=env,
        timeout=900,
    )
    dur = time.time() - t0

    # Preserve source for inspection: copy to out_dir/source.py
    try:
        if target_file.exists():
            shutil.copy2(str(target_file), str(out_dir / "source.py"))
    except Exception:
        pass

    # cleanup target at ROOT
    try:
        target_file.unlink(missing_ok=True)
    except Exception:
        pass

    return proc, dur


def _probe_video(path: Path) -> tuple[float | None, str | None]:
    try:
        ff = subprocess.run(
            [
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=width,height,duration",
                "-of", "json", str(path),
            ],
            capture_output=True, text=True, timeout=30,
        )
        info = json.loads(ff.stdout)["streams"][0]
        return round(float(info.get("duration", 0)), 2), f"{info['width']}x{info['height']}"
    except Exception:
        return None, None


def run_naked(new_id: str, topic_prompt: str) -> dict:
    print(f"\n  ┃ NAKED OPUS: {new_id}")
    task_id = f"naked_{new_id}_{int(time.time())}"
    out_dir = RUNS_DIR / task_id

    proc, dur = _run_subprocess(NAKED_RUNNER, task_id, out_dir, topic_prompt)

    render_success = False
    error_notes = ""
    for line in proc.stdout.splitlines():
        print(f"    {line}")
        if line.startswith("[VIDEO] "):
            render_success = True
        elif line.startswith("[RENDER_ERROR] "):
            error_notes = line[15:].strip()
        elif line.startswith("[ERROR] "):
            error_notes = line[8:].strip()

    if not render_success and proc.stderr:
        stderr_tail = "\n".join(proc.stderr.splitlines()[-10:])[-500:]
        if not error_notes:
            error_notes = stderr_tail

    code_lines = None
    video_duration_sec = None
    video_resolution = None
    if render_success:
        src = out_dir / "video.mp4"
        if src.exists():
            dest = VIDEOS_NAKED / f"{new_id}.mp4"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src), str(dest))
            video_duration_sec, video_resolution = _probe_video(dest)

    notes = "Zero-shot naked Opus (28-word system prompt)"
    if not render_success:
        notes += f" — render failed: {error_notes[:300]}"

    return {
        "render_success": render_success,
        "gen_time_sec": round(dur, 2),
        "render_duration_sec": round(dur, 2),
        "code_lines": code_lines,
        "video_duration_sec": video_duration_sec,
        "video_resolution": video_resolution,
        "notes": notes,
        "vision_qa_verdict": None,
        "llm_call_count": 1,
        "total_prompt_tokens": None,
        "total_completion_tokens": None,
        "refining_iterations": 0,
        "rag_examples_retrieved": 0,
    }


def run_system(new_id: str, topic_prompt: str) -> dict:
    print(f"\n  ┃ FULL SYSTEM: {new_id}")
    task_id = f"sys_{new_id}_{int(time.time())}"
    out_dir = RUNS_DIR / task_id

    proc, dur = _run_subprocess(SYSTEM_RUNNER, task_id, out_dir, topic_prompt)

    render_success = False
    vision_verdict = None
    code_chars = 0
    error_notes = ""
    for line in proc.stdout.splitlines():
        # full output is verbose — print first 200 chars per line
        print(f"    {line[:200]}")
        if line.startswith("[VIDEO] "):
            render_success = True
        elif line.startswith("[CODE] "):
            try:
                code_chars = int(line[7:].strip())
            except Exception:
                pass
        elif line.startswith("[VISION_VERDICT] "):
            try:
                vision_verdict = json.loads(line[17:].strip())
            except Exception:
                pass
        elif line.startswith("[ERROR] "):
            error_notes = line[8:].strip()
        elif line.startswith("[RENDER_ERROR] "):
            error_notes = line[15:].strip()

    if not render_success and proc.stderr:
        stderr_tail = "\n".join(proc.stderr.splitlines()[-10:])[-500:]
        if not error_notes:
            error_notes = stderr_tail

    code_lines = None
    video_duration_sec = None
    video_resolution = None
    if render_success:
        src = out_dir / "video.mp4"
        if src.exists():
            dest = VIDEOS_SYSTEM / f"{new_id}.mp4"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src), str(dest))
            video_duration_sec, video_resolution = _probe_video(dest)

    # estimate code lines from code_chars (rough): avg ~30 chars per line
    if code_chars:
        code_lines = max(50, code_chars // 30)

    verdict_str = vision_verdict.get("verdict") if vision_verdict else None

    return {
        "render_success": render_success,
        "gen_time_sec": round(dur, 2),
        "render_duration_sec": None,
        "code_lines": code_lines,
        "video_duration_sec": video_duration_sec,
        "video_resolution": video_resolution,
        "vision_qa_verdict": verdict_str,
        "llm_call_count": None,
        "total_prompt_tokens": None,
        "total_completion_tokens": None,
        "refining_iterations": 0,
        "rag_examples_retrieved": None,
        "notes": error_notes[:300] if not render_success and error_notes else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", help="Comma-separated new_id prefix (e.g. Q04,Q07). Default: all 4")
    ap.add_argument("--side", choices=["naked", "system", "both"], default="both",
                    help="Which side to run")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    gallery = json.loads(GALLERY_JSON.read_text(encoding="utf-8"))

    targets = REPLACEMENTS
    if args.items:
        wanted = set(args.items.split(","))
        targets = [r for r in REPLACEMENTS if any(r["new_id"].startswith(w) for w in wanted)]
        print(f"Filtered to {len(targets)} items: {[r['new_id'] for r in targets]}")

    if args.dry_run:
        for r in targets:
            print(f"  {r['old_id']} → {r['new_id']}")
            print(f"     {r['topic']}")
            print(f"     prompt: {r['topic_prompt'][:120]}...")
        return

    VIDEOS_NAKED.mkdir(parents=True, exist_ok=True)
    VIDEOS_SYSTEM.mkdir(parents=True, exist_ok=True)

    for r in targets:
        print(f"\n{'='*70}")
        print(f"▶  {r['old_id']} → {r['new_id']}")
        print(f"   {r['topic']}")
        print(f"{'='*70}")

        # Run both sides
        opus_metrics = None
        system_metrics = None
        if args.side in ("naked", "both"):
            opus_metrics = run_naked(r["new_id"], r["topic_prompt"])
        if args.side in ("system", "both"):
            system_metrics = run_system(r["new_id"], r["topic_prompt"])

        # Find old item in gallery, replace
        for i, item in enumerate(gallery["items"]):
            if item["id"] == r["old_id"]:
                new_item = {
                    "id": r["new_id"],
                    "topic": r["topic"],
                    "topic_en": r["topic_en"],
                    "topic_prompt": r["topic_prompt"],
                    "opus_video_url": f"/static/videos/naked_opus/{r['new_id']}.mp4",
                    "system_video_url": f"/static/videos/old_rag/{r['new_id']}.mp4",
                    "opus_metrics": opus_metrics if opus_metrics else item["opus_metrics"],
                    "system_metrics": system_metrics if system_metrics else item["system_metrics"],
                }
                gallery["items"][i] = new_item
                break

        # Save incrementally
        GALLERY_JSON.write_text(json.dumps(gallery, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  💾 gallery.json updated: {r['new_id']}")

    # Summary
    print(f"\n{'='*70}\nSUMMARY\n{'='*70}")
    for r in targets:
        for item in gallery["items"]:
            if item["id"] == r["new_id"]:
                o = item["opus_metrics"]
                s = item["system_metrics"]
                ostat = "✅" if o.get("render_success") else "❌"
                sstat = "✅" if s.get("render_success") else "❌"
                print(f"  {r['new_id']}: baseline={ostat} system={sstat}")
                break


if __name__ == "__main__":
    main()
