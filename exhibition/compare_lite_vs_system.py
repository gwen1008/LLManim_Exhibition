"""Lite vs System 兩版公平對比 — 重新出題。

同題、同 prompt，分別跑：
  - full_system_runner.py        → SYSTEM (主 Planner)
  - full_system_lite_runner.py   → LITE   (PlannerLite + lite directive)

兩 runner 介面一致：  runner.py <task_id> <out_dir>   stdin 餵 topic。

Output:
  exhibition/static/compare_new/system/{id}.mp4 + {id}.py
  exhibition/static/compare_new/lite/{id}.mp4   + {id}.py
  exhibition/static/compare_new/results.json
  → 再跑 build_lite_vs_system_page.py 生對比頁

用法：
  python exhibition/compare_lite_vs_system.py            # 跑全部新題（兩版）
  python exhibition/compare_lite_vs_system.py --items N01_bezier_curve,N03_gradient_descent
  python exhibition/compare_lite_vs_system.py --variant lite   # 只跑某一版
  python exhibition/compare_lite_vs_system.py --force          # 無視快取重跑
"""
from __future__ import annotations

import argparse
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
RUNS_DIR = HERE / "static" / "runs"
OUT_BASE = HERE / "static" / "compare_new"
RESULTS = OUT_BASE / "results.json"

SYSTEM_RUNNER = HERE / "full_system_runner.py"
LITE_RUNNER = HERE / "full_system_lite_runner.py"

# ── 新出的題目（刻意避開 batch_20 的 5 題，涵蓋 4 種生成挑戰）──────────
#   prompt 用中文，跟正式 pipeline 一樣走 AcademicTranslator。
TOPICS = [
    {
        "id": "N01_bezier_curve",
        "topic": "Bézier 曲線",
        "prompt": "用 de Casteljau 演算法說明三次貝茲曲線：給定四個控制點，隨著參數 t 從 0 到 1 連續移動，遞迴線性內插畫出曲線。",
        "challenge": "連續參數動畫（ValueTracker 沿 t 掃）",
    },
    {
        "id": "N02_taylor_cosine",
        "topic": "cos(x) 泰勒展開",
        "prompt": "說明餘弦函數的泰勒級數逼近：從常數項開始，逐項加入 -x²/2!、+x⁴/4!，每加一項曲線就更貼近真正的 cos(x)。",
        "challenge": "離散疊加步驟（逐項加入）",
    },
    {
        "id": "N03_gradient_descent",
        "topic": "梯度下降",
        "prompt": "在二維損失曲面的等高線圖上，示範梯度下降：從一個起始點出發，沿負梯度方向逐步迭代，軌跡螺旋收斂到最低點。",
        "challenge": "迭代收斂 + 多物件追蹤（dead air 高風險）",
    },
    {
        "id": "N04_dft_phasors",
        "topic": "傅立葉相量合成方波",
        "prompt": "用旋轉相量說明傅立葉級數如何合成方波：多個不同頻率與半徑的旋轉向量首尾相接，末端軌跡隨時間描繪出方波。",
        "challenge": "多旋轉體並行 + 連續時間",
    },
]

RUNNERS = {"system": SYSTEM_RUNNER, "lite": LITE_RUNNER}


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
        return 0, 0, 0, 0
    src = py.read_text(encoding="utf-8", errors="ignore")
    lines = src.count("\n")
    plays = len(re.findall(r"self\.play\(", src))
    subs = len(re.findall(r"set_subtitle\(", src))
    lagged = len(re.findall(r"LaggedStart\(", src))
    return lines, plays, subs, lagged


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

    print(f"  ▶ {variant.upper():<6}: {tid}", end="", flush=True)
    t0 = time.time()
    proc = subprocess.run(
        [sys.executable, str(runner), task_id, str(out_dir)],
        input=t["prompt"] + "\n",
        text=True, capture_output=True, env=env, timeout=900,
    )
    dur = time.time() - t0

    render_ok = any(l.startswith("[VIDEO] ") for l in proc.stdout.splitlines())
    bj = next((l.split("] ", 1)[1] for l in proc.stdout.splitlines()
               if l.startswith("[BJ_SCORE] ")), None)

    # preserve source
    if target_file.exists():
        shutil.copy2(str(target_file), str(out_dir / "source.py"))
    target_file.unlink(missing_ok=True)

    dest_dir = OUT_BASE / variant
    dest_dir.mkdir(parents=True, exist_ok=True)
    if render_ok and (out_dir / "video.mp4").exists():
        shutil.copy2(str(out_dir / "video.mp4"), str(dest_dir / f"{tid}.mp4"))
    if (out_dir / "source.py").exists():
        shutil.copy2(str(out_dir / "source.py"), str(dest_dir / f"{tid}.py"))

    vid_dur, vid_kb = _probe(dest_dir / f"{tid}.mp4") if render_ok else (None, None)
    lines, plays, subs, lagged = _code_stats(dest_dir / f"{tid}.py")

    stderr_tail = ""
    if not render_ok and proc.stderr:
        stderr_tail = "\n".join(proc.stderr.splitlines()[-12:])[-600:]

    mark = "✅" if render_ok else "❌"
    print(f"  {mark} {dur:.0f}s · video {vid_dur}s · {lines}行 · {plays}play/{lagged}lagged · {subs}旁白")

    return {
        "render": render_ok,
        "gen_time_sec": round(dur, 1),
        "video_dur_sec": vid_dur,
        "video_kb": vid_kb,
        "code_lines": lines,
        "animations": plays,
        "lagged_starts": lagged,
        "subtitles": subs,
        "bj_score": bj,
        "stderr_tail": stderr_tail,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", help="逗號分隔的 topic id，預設全部")
    ap.add_argument("--variant", choices=["system", "lite", "both"], default="both")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    by_id = {t["id"]: t for t in TOPICS}
    targets = [by_id[i] for i in args.items.split(",") if i in by_id] if args.items else TOPICS
    variants = ["system", "lite"] if args.variant == "both" else [args.variant]

    OUT_BASE.mkdir(parents=True, exist_ok=True)
    done = json.loads(RESULTS.read_text(encoding="utf-8")) if RESULTS.exists() else {}

    print(f"題目: {[t['id'] for t in targets]}")
    print(f"版本: {variants}\n")

    t_global = time.time()
    for i, t in enumerate(targets, 1):
        tid = t["id"]
        print(f"[{i}/{len(targets)}] {tid}  ·  {t['topic']}  ({t['challenge']})")
        slot = done.setdefault(tid, {"topic": t["topic"], "prompt": t["prompt"],
                                     "challenge": t["challenge"]})
        for v in variants:
            if v in slot and slot[v].get("render") and not args.force:
                print(f"  ⏭️  {v} cached")
                continue
            slot[v] = run_one(v, t)
            RESULTS.write_text(json.dumps(done, ensure_ascii=False, indent=2), encoding="utf-8")

    elapsed = time.time() - t_global
    print(f"\n{'='*78}")
    print(f"DONE in {elapsed/60:.1f} min")
    print(f"{'='*78}")
    print(f"  {'ID':<20} {'ver':<7} {'render':<7} {'vid':<8} {'lines':<6} {'play/lag':<9} {'subs'}")
    print(f"  {'-'*72}")
    for tid, slot in done.items():
        for v in ("system", "lite"):
            d = slot.get(v)
            if not d:
                continue
            r = "✅" if d["render"] else "❌"
            vd = f"{d.get('video_dur_sec')}s" if d.get("video_dur_sec") else "—"
            pl = f"{d.get('animations')}/{d.get('lagged_starts')}"
            print(f"  {tid:<20} {v:<7} {r:<7} {vd:<8} {str(d.get('code_lines')):<6} {pl:<9} {d.get('subtitles')}")

    print(f"\nResults: {RESULTS}")
    print(f"Next:    python exhibition/build_lite_vs_system_page.py")


if __name__ == "__main__":
    main()
