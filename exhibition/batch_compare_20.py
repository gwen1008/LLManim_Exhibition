"""Batch compare 20 topics: naked Opus vs full system.

For each topic:
1. Run naked_opus.py → save video + source to batch_20/naked/{id}/
2. Run full_system_runner.py → save video + source to batch_20/system/{id}/
3. Append metrics to batch_20_results.csv (incremental — supports resume)

Run from project root:
    .venv/bin/python exhibition/batch_compare_20.py [--items Q01,Q02] [--side naked|system|both]
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
BATCH_DIR = HERE / "static" / "batch_20"
RESULTS_CSV = BATCH_DIR / "results.csv"

NAKED_RUNNER = HERE / "naked_opus.py"
SYSTEM_RUNNER = HERE / "full_system_runner.py"


# 20 topics — mix of easy/medium/hard for naked Opus
TOPICS = [
    # === Easy: 標準 Manim 視覺化（naked 應該都能做）===
    {"id": "Q01_riemann_sum", "topic": "Riemann 和逼近積分",
     "prompt": "計算定積分 ∫₀^π sin(x) dx 的值。請用 Riemann 和（將區間分成多個矩形）的方式視覺化近似過程。"},
    {"id": "Q02_newton_iteration", "topic": "Newton 迭代法求 √2",
     "prompt": "用 Newton 迭代法求 √2 的近似值（即求解方程 x² − 2 = 0）。請視覺化每一步切線如何逐漸逼近真正的根。"},
    {"id": "Q03_taylor_sine", "topic": "Taylor 級數逼近 sin(x)",
     "prompt": "用 Taylor 級數逼近 sin(x) 在原點附近的值。請視覺化展示加入越多項時多項式如何越來越貼近真正的 sin(x) 曲線。"},
    {"id": "Q04_pythagorean", "topic": "畢氏定理面積證明",
     "prompt": "用面積方法證明畢氏定理：建立一個直角三角形，在三邊外側分別建構正方形，視覺化展示兩股的正方形面積總和等於斜邊正方形的面積。"},
    {"id": "Q05_complete_square", "topic": "二次函數配方法",
     "prompt": "示範如何將二次函數 y = x² − 6x + 5 透過配方法化為頂點式 (x−3)² − 4，並視覺化拋物線頂點的平移與對稱軸位置。"},

    # === Medium: 多元素 + 精度要求 ===
    {"id": "Q06_unit_circle_trig", "topic": "單位圓正弦餘弦動畫",
     "prompt": "視覺化單位圓上的點如何旋轉並對應到正弦與餘弦函數：左側顯示單位圓上一個點繞圓旋轉，右側同步畫出 sin(θ) 曲線。"},
    {"id": "Q07_unit_roots", "topic": "z⁸ = 1 單位根",
     "prompt": "視覺化複數方程 z⁸ = 1 的所有解（8 次單位根）。請在複數平面上畫出單位圓，標出 8 個解，並從原點畫向量連到每個解。"},
    {"id": "Q08_slope_field", "topic": "斜率場與解曲線",
     "prompt": "解一階微分方程 dy/dx = x − y。請用斜率場視覺化方程的方向場，並從兩個不同初始點畫出對應的解曲線。"},
    {"id": "Q09_golden_spiral", "topic": "黃金螺旋",
     "prompt": "繪製黃金螺旋。請用費氏數列邊長 (1, 1, 2, 3, 5, 8) 依序排列六個正方形，並在每個正方形內畫一條四分之一圓弧連成螺旋。"},
    {"id": "Q10_sierpinski", "topic": "Sierpinski 三角形（4 層遞迴）",
     "prompt": "繪製 Sierpinski 三角形。請從一個大的等邊三角形開始，每一輪將每個三角形分成四個並移除中間那個，重複這個遞迴過程四次。"},
    {"id": "Q11_eigenvectors", "topic": "2×2 矩陣特徵向量",
     "prompt": "視覺化矩陣 A = [[3, 1], [0, 2]] 的線性變換：在 2D 平面上展示單位向量如何被變換，並標出特徵向量（不被旋轉只被縮放的方向）。"},
    {"id": "Q12_fourier_square", "topic": "Fourier 級數逼近方波",
     "prompt": "用 Fourier 級數逼近方波。請依序疊加奇數項（1 次、3 次、5 次諧波）正弦函數，視覺化展示越多項時級數越接近方波形狀。"},

    # === Hard: 動態系統 / 3D / 雙圖同步 / 高複雜度 ===
    {"id": "Q13_pendulum_phase", "topic": "單擺：時域 vs 相位空間",
     "prompt": "視覺化單擺運動。請左右並排兩張圖：左圖顯示擺角 θ 隨時間 t 的變化，右圖顯示相位空間（θ 對 dθ/dt 的橢圓軌跡），兩圖同步演化。"},
    {"id": "Q14_double_pendulum", "topic": "雙擺混沌軌跡",
     "prompt": "視覺化雙擺系統的混沌運動。請畫出兩個連接的擺臂，模擬其動態並描繪第二個擺末端的運動軌跡曲線。"},
    {"id": "Q15_wave_equation", "topic": "1D 波動方程動畫",
     "prompt": "視覺化 1D 波動方程的解 u(x, t) = sin(x − ct)：固定一個區間，動畫展示波形隨時間向右傳播。"},
    {"id": "Q16_lorenz", "topic": "Lorenz 吸引子（3D 蝴蝶曲線）",
     "prompt": "繪製 Lorenz 吸引子的軌跡。請解 Lorenz 系統並在 3D 空間中描繪解曲線形成的蝴蝶形狀（σ=10, ρ=28, β=8/3）。"},
    {"id": "Q17_saddle_3d", "topic": "馬鞍面 z = x² − y²",
     "prompt": "在 3D 空間中繪製馬鞍面 z = x² − y²。請展示其鞍點特性：沿 x 方向向上彎、沿 y 方向向下彎，並讓鏡頭旋轉觀察。"},
    {"id": "Q18_galton_board", "topic": "Galton 板（常態分佈）",
     "prompt": "用 Galton 板模擬常態分佈：許多小球從頂部落下，經過多層釘子隨機左右偏移，最後底部累積成鐘形分佈。"},
    {"id": "Q19_mandelbrot", "topic": "Mandelbrot 集合",
     "prompt": "繪製 Mandelbrot 集合：在複數平面上對每個點 c 計算迭代 zₙ₊₁ = zₙ² + c 是否發散，用顏色標示發散速度。"},
    {"id": "Q20_taylor_log", "topic": "Taylor 級數逼近 ln(1+x)",
     "prompt": "視覺化 ln(1+x) 的 Taylor 級數逼近。請依序加入更多項（x、−x²/2、+x³/3...），展示多項式逐漸貼近 ln(1+x) 並標示收斂半徑 |x| < 1。"},
]


CSV_FIELDS = [
    "id", "topic", "prompt",
    "naked_render", "naked_time_sec", "naked_lines", "naked_video_sec", "naked_video_kb",
    "sys_render", "sys_time_sec", "sys_lines", "sys_video_sec", "sys_video_kb",
    "sys_subtitles", "sys_animations",
]


def _run_subprocess(runner: Path, task_id: str, out_dir: Path, topic_prompt: str) -> tuple[subprocess.CompletedProcess, float]:
    out_dir.mkdir(parents=True, exist_ok=True)
    target_file = ROOT / f"test_script_{task_id}.py"

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["TASK_TARGET_FILE"] = str(target_file)

    t0 = time.time()
    proc = subprocess.run(
        [sys.executable, str(runner), task_id, str(out_dir)],
        input=topic_prompt + "\n",
        text=True,
        capture_output=True,
        env=env,
        timeout=900,
    )
    dur = time.time() - t0

    # Preserve source.py
    try:
        if target_file.exists():
            shutil.copy2(str(target_file), str(out_dir / "source.py"))
        target_file.unlink(missing_ok=True)
    except Exception:
        pass

    return proc, dur


def _probe(path: Path) -> tuple[float | None, int | None]:
    """Return (duration_sec, file_size_kb)."""
    if not path.exists():
        return None, None
    size_kb = round(path.stat().st_size / 1024)
    try:
        ff = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=duration", "-of", "json", str(path)],
            capture_output=True, text=True, timeout=30,
        )
        dur = round(float(json.loads(ff.stdout)["streams"][0]["duration"]), 2)
        return dur, size_kb
    except Exception:
        return None, size_kb


def _count_source(out_dir: Path) -> tuple[int, int, int]:
    """Return (lines, animations, subtitles) from source.py."""
    p = out_dir / "source.py"
    if not p.exists():
        return 0, 0, 0
    src = p.read_text(encoding="utf-8", errors="ignore")
    import re
    lines = src.count("\n")
    plays = len(re.findall(r"self\.play\(", src))
    subs = len(re.findall(r"set_subtitle\(", src))
    return lines, plays, subs


def run_naked(topic_id: str, topic_prompt: str) -> dict:
    task_id = f"batch_naked_{topic_id}_{int(time.time())}"
    out_dir = RUNS_DIR / task_id
    print(f"  ▶ NAKED: {topic_id}", end="", flush=True)

    proc, dur = _run_subprocess(NAKED_RUNNER, task_id, out_dir, topic_prompt)

    render_success = any(l.startswith("[VIDEO] ") for l in proc.stdout.splitlines())

    # Copy video to canonical batch dir
    canonical_video = BATCH_DIR / "naked" / f"{topic_id}.mp4"
    canonical_source = BATCH_DIR / "naked" / f"{topic_id}.py"
    canonical_video.parent.mkdir(parents=True, exist_ok=True)

    if render_success:
        src_v = out_dir / "video.mp4"
        if src_v.exists():
            shutil.copy2(str(src_v), str(canonical_video))
    src_py = out_dir / "source.py"
    if src_py.exists():
        shutil.copy2(str(src_py), str(canonical_source))

    vid_dur, vid_kb = _probe(canonical_video) if render_success else (None, None)
    lines, _, _ = _count_source(out_dir)

    print(f"  {('✅' if render_success else '❌')} {dur:.0f}s")
    return {
        "render": render_success,
        "time_sec": round(dur, 1),
        "lines": lines,
        "video_sec": vid_dur,
        "video_kb": vid_kb,
    }


def run_system(topic_id: str, topic_prompt: str) -> dict:
    task_id = f"batch_sys_{topic_id}_{int(time.time())}"
    out_dir = RUNS_DIR / task_id
    print(f"  ▶ SYSTEM: {topic_id}", end="", flush=True)

    proc, dur = _run_subprocess(SYSTEM_RUNNER, task_id, out_dir, topic_prompt)

    render_success = any(l.startswith("[VIDEO] ") for l in proc.stdout.splitlines())

    canonical_video = BATCH_DIR / "system" / f"{topic_id}.mp4"
    canonical_source = BATCH_DIR / "system" / f"{topic_id}.py"
    canonical_video.parent.mkdir(parents=True, exist_ok=True)

    if render_success:
        src_v = out_dir / "video.mp4"
        if src_v.exists():
            shutil.copy2(str(src_v), str(canonical_video))
    src_py = out_dir / "source.py"
    if src_py.exists():
        shutil.copy2(str(src_py), str(canonical_source))

    vid_dur, vid_kb = _probe(canonical_video) if render_success else (None, None)
    lines, plays, subs = _count_source(out_dir)

    print(f"  {('✅' if render_success else '❌')} {dur:.0f}s")
    return {
        "render": render_success,
        "time_sec": round(dur, 1),
        "lines": lines,
        "video_sec": vid_dur,
        "video_kb": vid_kb,
        "subtitles": subs,
        "animations": plays,
    }


def load_done() -> dict:
    if not RESULTS_CSV.exists():
        return {}
    with open(RESULTS_CSV, encoding="utf-8") as f:
        return {row["id"]: row for row in csv.DictReader(f)}


def write_row(row: dict):
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    file_exists = RESULTS_CSV.exists()
    with open(RESULTS_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if not file_exists:
            w.writeheader()
        w.writerow(row)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", help="Comma-separated topic prefix (e.g. Q01,Q02). Default: all 20")
    ap.add_argument("--side", choices=["naked", "system", "both"], default="both")
    ap.add_argument("--force", action="store_true", help="Re-run even if already in CSV")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    targets = TOPICS
    if args.items:
        wanted = set(args.items.split(","))
        targets = [t for t in TOPICS if any(t["id"].startswith(w) for w in wanted)]
        print(f"Filtered to {len(targets)} items")

    if args.dry_run:
        for t in targets:
            print(f"  {t['id']}: {t['topic']}")
            print(f"     prompt: {t['prompt'][:80]}...")
        return

    done = load_done()
    print(f"Already done: {len(done)} (resume mode)")

    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    t_global = time.time()

    for i, t in enumerate(targets, 1):
        print(f"\n[{i}/{len(targets)}] {t['id']}: {t['topic']}")
        if t["id"] in done and not args.force:
            print(f"  ⏭️  already done, skip (use --force to re-run)")
            continue

        naked = None
        system = None
        if args.side in ("naked", "both"):
            naked = run_naked(t["id"], t["prompt"])
        if args.side in ("system", "both"):
            system = run_system(t["id"], t["prompt"])

        row = {
            "id": t["id"],
            "topic": t["topic"],
            "prompt": t["prompt"],
            "naked_render": naked["render"] if naked else "",
            "naked_time_sec": naked["time_sec"] if naked else "",
            "naked_lines": naked["lines"] if naked else "",
            "naked_video_sec": naked["video_sec"] if naked else "",
            "naked_video_kb": naked["video_kb"] if naked else "",
            "sys_render": system["render"] if system else "",
            "sys_time_sec": system["time_sec"] if system else "",
            "sys_lines": system["lines"] if system else "",
            "sys_video_sec": system["video_sec"] if system else "",
            "sys_video_kb": system["video_kb"] if system else "",
            "sys_subtitles": system["subtitles"] if system else "",
            "sys_animations": system["animations"] if system else "",
        }
        write_row(row)
        print(f"  💾 row written")

    # Summary
    elapsed = time.time() - t_global
    print(f"\n{'='*70}")
    print(f"BATCH COMPLETE in {elapsed/60:.1f} min")
    print(f"{'='*70}")
    done_after = load_done()
    naked_ok = sum(1 for r in done_after.values() if r.get("naked_render") == "True")
    sys_ok = sum(1 for r in done_after.values() if r.get("sys_render") == "True")
    print(f"Naked render success: {naked_ok}/{len(done_after)}")
    print(f"System render success: {sys_ok}/{len(done_after)}")
    print(f"CSV: {RESULTS_CSV}")
    print(f"Videos: {BATCH_DIR}/{{naked,system}}/")


if __name__ == "__main__":
    main()
