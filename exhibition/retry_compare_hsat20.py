"""opus(餵錯誤 retry, 上限5) vs 本系統 的「重跑次數」對比 — 高中 20 題。

對每題跑 naked_opus_retry.py,記錄 opus「第幾次成功 / 5 次仍失敗」。
本系統端的 iteration 數從既有 paper run csv 撈(不重跑系統)。
輸出 retry_report.json,供網頁展示「opus 跑 N 次 vs 系統 1 次」。

用法:
  python exhibition/retry_compare_hsat20.py
  python exhibition/retry_compare_hsat20.py --items HSAT_115_1,HSAT_113_1
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
RUNNER = HERE / "naked_opus_retry.py"          # opus + 餵錯誤 retry
SYS_RUNNER = HERE / "full_system_runner.py"  # 本系統 FULL(完整 Planner,不簡化)
CASES = ROOT / "evaluation" / "test_cases_hsat20.json"
OUT_DIR = HERE / "static" / "retry_hsat20"
REPORT = OUT_DIR / "retry_report.json"


def _last_tag(lines, tag):
    v = [l for l in lines if l.startswith(f"[{tag}] ")]
    return v[-1][len(tag) + 3:].strip() if v else None


def run_system(t: dict) -> dict:
    """現在實跑本系統 lite runner,記錄 iteration / 成功與否 / 影片。"""
    tid = t["id"]
    task_id = f"sys_{tid}_{int(time.time())}"
    out_dir = HERE / "static" / "runs" / task_id
    out_dir.mkdir(parents=True, exist_ok=True)
    target_file = ROOT / f"test_script_{task_id}.py"

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["TASK_TARGET_FILE"] = str(target_file)

    print(f"  ▶ SYSTEM:     {tid}", flush=True)
    try:
        proc = subprocess.run(
            [sys.executable, str(SYS_RUNNER), task_id, str(out_dir)],
            input=t["topic"] + "\n",
            text=True, capture_output=True, env=env, timeout=1800,
        )
    except subprocess.TimeoutExpired:
        target_file.unlink(missing_ok=True)
        return {"sys_status": "TIMEOUT", "sys_iterations": None, "sys_video": None}

    lines = proc.stdout.splitlines()
    video = _last_tag(lines, "VIDEO")
    iters = _last_tag(lines, "SYS_ITERATIONS")
    best_effort = _last_tag(lines, "SYS_BEST_EFFORT") == "1"
    sys_ok = video is not None

    dest = OUT_DIR / tid
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "sys_stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (dest / "sys_stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    sys_video = None
    if sys_ok and (out_dir / "video.mp4").exists():
        import shutil
        shutil.copy(out_dir / "video.mp4", dest / "sys_video.mp4")
        sys_video = f"/static/retry_hsat20/{tid}/sys_video.mp4"

    target_file.unlink(missing_ok=True)
    return {
        "sys_status": "Success" if sys_ok else "Failed",
        "sys_iterations": int(iters) if iters and iters.isdigit() else None,
        "sys_best_effort": best_effort,
        "sys_video": sys_video,
    }


def run_one(t: dict) -> dict:
    tid = t["id"]
    task_id = f"retry_{tid}_{int(time.time())}"
    out_dir = HERE / "static" / "runs" / task_id
    out_dir.mkdir(parents=True, exist_ok=True)
    target_file = ROOT / f"test_script_{task_id}.py"

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["TASK_TARGET_FILE"] = str(target_file)
    env["NAKED_MAX_RETRIES"] = "5"

    print(f"  ▶ OPUS-RETRY: {tid}  ({t['knowledge_point']})", flush=True)
    t0 = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, str(RUNNER), task_id, str(out_dir)],
            input=t["topic"] + "\n",
            text=True, capture_output=True, env=env, timeout=1800,
        )
    except subprocess.TimeoutExpired:
        target_file.unlink(missing_ok=True)
        return {"id": tid, "opus_final": "TIMEOUT", "opus_attempts": None, "time_sec": 1800}
    dur = round(time.time() - t0, 1)

    lines = proc.stdout.splitlines()

    def last_tag(tag):
        v = [l for l in lines if l.startswith(f"[{tag}] ")]
        return v[-1][len(tag) + 3:].strip() if v else None

    final_tag = last_tag("FINAL")
    attempts = last_tag("ATTEMPTS")
    attempts = int(attempts) if attempts and attempts.isdigit() else None
    render_err = last_tag("RENDER_ERROR") or ""
    # 區分:runner 正常跑完(有 FINAL) vs subprocess 中途死掉(無 FINAL → CRASH)
    if final_tag:
        final = final_tag
    elif proc.returncode == 0:
        final = "OK"
    else:
        final = "CRASH"  # runner 自己異常退出,非 opus 內容問題

    # 保存影片 + 代碼 + log
    dest = OUT_DIR / tid
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (dest / "stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    src_code = out_dir / "opus_final_code.py"
    if src_code.exists():
        (dest / "opus_final_code.py").write_text(src_code.read_text(encoding="utf-8"), encoding="utf-8")
    video_path = None
    if final == "OK" and (out_dir / "video.mp4").exists():
        import shutil
        shutil.copy(out_dir / "video.mp4", dest / "video.mp4")
        video_path = f"/static/retry_hsat20/{tid}/video.mp4"

    target_file.unlink(missing_ok=True)
    return {
        "id": tid,
        "knowledge_point": t["knowledge_point"],
        "difficulty": t["difficulty"],
        "opus_final": final,
        "opus_attempts": attempts,
        "opus_video": video_path,
        "opus_last_error": render_err,
        "time_sec": dur,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", default="")
    ap.add_argument("--side", choices=["opus", "system", "both"], default="both",
                    help="只跑哪一邊(省 quota / 避免兩邊搶同一 Claude 訂閱)")
    args = ap.parse_args()

    cases = json.loads(CASES.read_text(encoding="utf-8"))
    if args.items:
        wanted = set(args.items.split(","))
        cases = [c for c in cases if c["id"] in wanted]

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 併入既有 report:重跑指定題時只更新那幾題,保留其餘
    existing = {}
    if REPORT.exists():
        for r in json.loads(REPORT.read_text(encoding="utf-8")):
            existing[r["id"]] = r

    print(f"\nopus(retry≤5) vs 本系統 · {len(cases)} 題 · side={args.side}\n" + "=" * 60)
    for i, t in enumerate(cases, 1):
        print(f"\n[{i}/{len(cases)}]")
        r = existing.get(t["id"], {"id": t["id"], "knowledge_point": t["knowledge_point"], "difficulty": t["difficulty"]})
        if args.side in ("opus", "both"):
            r.update(run_one(t))            # opus + 餵錯誤 retry
        if args.side in ("system", "both"):
            r.update(run_system(t))         # 本系統現在實跑
        existing[t["id"]] = r
        REPORT.write_text(json.dumps(list(existing.values()), ensure_ascii=False, indent=2), encoding="utf-8")

    results = list(existing.values())

    # 統計
    n = len(results)
    opus_ok = [r for r in results if r.get("opus_final") == "OK"]
    opus_att = [r["opus_attempts"] for r in opus_ok if r.get("opus_attempts")]
    opus_avg = round(sum(opus_att) / len(opus_att), 1) if opus_att else 0
    sys_ok = [r for r in results if r.get("sys_status") == "Success"]
    sys_iters = [r["sys_iterations"] for r in sys_ok if r.get("sys_iterations") is not None]
    sys_avg = round(sum(sys_iters) / len(sys_iters), 1) if sys_iters else 0

    print("\n" + "=" * 60)
    print(f"opus(retry≤5): {len(opus_ok)}/{n} 成功,成功題平均 {opus_avg} 次嘗試")
    print(f"本系統:        {len(sys_ok)}/{n} 成功,成功題平均 {sys_avg} 次迭代")
    print()
    print(f"{'ID':14s} {'opus':10s} {'opus次數':8s} {'系統':8s} {'系統iter':8s} {'難度'}")
    for r in results:
        att = f"第{r['opus_attempts']}次" if r.get("opus_attempts") else "-"
        ofin = "✅" if r.get("opus_final") == "OK" else "❌仍崩"
        sfin = "✅" if r.get("sys_status") == "Success" else "❌"
        si = r.get("sys_iterations")
        si = f"第{si}次" if si is not None else "-"
        be = "(勉強)" if r.get("sys_best_effort") else ""
        print(f"{r['id']:14s} {ofin:10s} {att:8s} {sfin:8s} {si:8s} D{r.get('difficulty','?')} {be}")
    print(f"\n📄 報告: {REPORT}")


if __name__ == "__main__":
    main()
