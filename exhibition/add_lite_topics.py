"""補跑 batch_20 三方比較的「全新題」三版全跑（naked / system / lite）。

每題跑三個 runner，歸位到 static/batch_20/{naked,system,lite}/{id}.mp4 + .py，
ffprobe 量時長，把 naked/system stats 寫進 results.csv（新增列），
lite stats 寫進 lite_results.json，最後重生 lite_compare.html。

三 runner 介面一致：  runner.py <task_id> <out_dir>   stdin 餵 topic，印 [VIDEO]。

用法：
  python exhibition/add_lite_topics.py                          # 全部 NEW_TOPICS 三版
  python exhibition/add_lite_topics.py --items H01_complete_square
  python exhibition/add_lite_topics.py --variant lite           # 只跑某版
  python exhibition/add_lite_topics.py --force                  # 無視快取重跑
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
BATCH = HERE / "static" / "batch_20"
RUNS_DIR = HERE / "static" / "runs"
LITE_JSON = BATCH / "lite_results.json"
RESULTS_CSV = BATCH / "results.csv"

RUNNERS = {
    "naked": HERE / "naked_opus.py",
    "system": HERE / "full_system_runner.py",
    "lite": HERE / "full_system_lite_runner.py",
}

# 全新高中數學解題題（id H 前綴，避開 batch_20 的 Q）
NEW_TOPICS = [
    {
        "id": "H01_complete_square",
        "topic": "配方法解二次方程",
        "prompt": "用配方法解一元二次方程 x²-6x+5=0：先將方程配成完全平方 (x-3)²=4，再開根號求出兩根 x=1 與 x=5。請同步畫出對應的拋物線 y=x²-6x+5，標出頂點 (3,-4) 與兩個 x 軸交點。",
    },
    {
        "id": "H02_sin_equation",
        "topic": "三角方程 sinθ=1/2",
        "prompt": "解三角方程 sinθ=1/2。在單位圓上找出第一象限與第二象限的兩個基本解 θ=30° 與 θ=150°，並說明因為正弦函數的週期性，通解為 θ=30°+360°k 與 θ=150°+360°k。請同步顯示單位圓上的點與 sinθ 曲線。",
    },
    {
        "id": "H03_line_circle",
        "topic": "直線與圓相交",
        "prompt": "求直線 y=x+1 與圓 x²+y²=4 的交點。將直線代入圓方程得到 2x²+2x-3=0，用判別式判斷有兩個交點，解出交點座標。請畫出圓與直線，標出兩個交點。",
    },
]

# results.csv 欄位順序（沿用既有 schema）
CSV_FIELDS = [
    "id", "topic", "prompt",
    "naked_render", "naked_time_sec", "naked_lines", "naked_video_sec", "naked_video_kb",
    "sys_render", "sys_time_sec", "sys_lines", "sys_video_sec", "sys_video_kb",
    "sys_subtitles", "sys_animations",
]


def _probe(p: Path):
    if not p.exists():
        return None, None
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


def _code_stats(py: Path):
    if not py.exists():
        return 0, 0, 0
    src = py.read_text(encoding="utf-8", errors="ignore")
    lines = src.count("\n")
    plays = len(re.findall(r"self\.play\(", src))
    subs = len(re.findall(r"set_subtitle\(", src))
    return lines, plays, subs


def run_one(variant: str, t: dict) -> dict:
    tid = t["id"]
    runner = RUNNERS[variant]
    task_id = f"{variant}_{tid}_{int(time.time())}"
    out_dir = RUNS_DIR / task_id
    out_dir.mkdir(parents=True, exist_ok=True)
    target_file = ROOT / f"test_script_{task_id}.py"

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["TASK_TARGET_FILE"] = str(target_file)

    print(f"  ▶ {variant.upper():<6}: {tid}", flush=True)
    t0 = time.time()
    proc = subprocess.run(
        [sys.executable, str(runner), task_id, str(out_dir)],
        input=t["prompt"] + "\n",
        text=True, capture_output=True, env=env, timeout=900,
    )
    dur = time.time() - t0

    render_ok = any(l.startswith("[VIDEO] ") for l in proc.stdout.splitlines())

    dest_dir = BATCH / variant
    dest_dir.mkdir(parents=True, exist_ok=True)
    if target_file.exists():
        shutil.copy2(str(target_file), str(dest_dir / f"{tid}.py"))
    target_file.unlink(missing_ok=True)
    if render_ok and (out_dir / "video.mp4").exists():
        shutil.copy2(str(out_dir / "video.mp4"), str(dest_dir / f"{tid}.mp4"))

    vid_dur, vid_kb = _probe(dest_dir / f"{tid}.mp4") if render_ok else (None, None)
    lines, plays, subs = _code_stats(dest_dir / f"{tid}.py")

    stderr_tail = ""
    if not render_ok and proc.stderr:
        stderr_tail = "\n".join(proc.stderr.splitlines()[-12:])[-600:]

    mark = "✅" if render_ok else "❌"
    print(f"    {mark} {dur:.0f}s · video {vid_dur}s · {lines}行 · {plays}動畫 · {subs}旁白")
    if not render_ok and stderr_tail:
        print(f"    stderr: {stderr_tail[:300]}")

    return {
        "render": render_ok, "gen_time_sec": round(dur, 1),
        "video_dur_sec": vid_dur, "video_kb": vid_kb,
        "code_lines": lines, "animations": plays, "subtitles": subs,
        "stderr_tail": stderr_tail,
    }


def _load_csv() -> dict:
    if not RESULTS_CSV.exists():
        return {}
    return {r["id"]: r for r in csv.DictReader(open(RESULTS_CSV, encoding="utf-8"))}


def _write_csv(rows: dict):
    # 保留既有所有欄位（results.csv 原本有更多欄；只更新/新增我們關心的）
    existing_fields = []
    if RESULTS_CSV.exists():
        with open(RESULTS_CSV, encoding="utf-8") as f:
            existing_fields = next(csv.reader(f))
    fields = existing_fields or CSV_FIELDS
    with open(RESULTS_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows.values():
            w.writerow(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", help="逗號分隔 id，預設全部 NEW_TOPICS")
    ap.add_argument("--variant", choices=["naked", "system", "lite", "all"], default="all")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    by_id = {t["id"]: t for t in NEW_TOPICS}
    targets = [by_id[i] for i in args.items.split(",") if i in by_id] if args.items else NEW_TOPICS
    variants = ["naked", "system", "lite"] if args.variant == "all" else [args.variant]

    csv_rows = _load_csv()
    lite = json.loads(LITE_JSON.read_text(encoding="utf-8")) if LITE_JSON.exists() else {}

    print(f"補題: {[t['id'] for t in targets]}  版本: {variants}\n")
    t_global = time.time()

    for i, t in enumerate(targets, 1):
        tid = t["id"]
        print(f"[{i}/{len(targets)}] {tid}  ·  {t['topic']}")
        # 確保 csv 有此題的基本列
        row = csv_rows.setdefault(tid, {"id": tid, "topic": t["topic"], "prompt": t["prompt"]})
        row["topic"], row["prompt"] = t["topic"], t["prompt"]

        for v in variants:
            cached = (
                (v == "lite" and tid in lite and lite[tid].get("render"))
                or (v == "naked" and row.get("naked_render") == "True")
                or (v == "system" and row.get("sys_render") == "True")
            )
            if cached and not args.force:
                print(f"  ⏭️  {v} cached")
                continue

            res = run_one(v, t)

            if v == "naked":
                row.update({
                    "naked_render": str(res["render"]),
                    "naked_time_sec": res["gen_time_sec"],
                    "naked_lines": res["code_lines"],
                    "naked_video_sec": res["video_dur_sec"] or "",
                    "naked_video_kb": res["video_kb"] or "",
                })
                _write_csv(csv_rows)
            elif v == "system":
                row.update({
                    "sys_render": str(res["render"]),
                    "sys_time_sec": res["gen_time_sec"],
                    "sys_lines": res["code_lines"],
                    "sys_video_sec": res["video_dur_sec"] or "",
                    "sys_video_kb": res["video_kb"] or "",
                    "sys_subtitles": res["subtitles"],
                    "sys_animations": res["animations"],
                })
                _write_csv(csv_rows)
            else:  # lite
                res.update({
                    "topic": t["topic"],
                    "naked_render": row.get("naked_render", ""),
                    "naked_video_sec": row.get("naked_video_sec", ""),
                    "sys_render": row.get("sys_render", ""),
                    "sys_video_sec": row.get("sys_video_sec", ""),
                    "sys_lines": row.get("sys_lines", ""),
                    "sys_subs": row.get("sys_subtitles", ""),
                })
                lite[tid] = res
                LITE_JSON.write_text(json.dumps(lite, ensure_ascii=False, indent=2), encoding="utf-8")

    elapsed = time.time() - t_global
    print(f"\n{'='*60}\nDONE in {elapsed/60:.1f} min")
    print(f"更新 {RESULTS_CSV}\n更新 {LITE_JSON}")
    print("重生頁面: python exhibition/build_lite_compare_page.py")


if __name__ == "__main__":
    main()
