"""只跑 naked_opus 驗證 20 題高中學測題的 render 成功率。

不跑 system，純粹確認 opus 裸跑在學測題上崩幾題、錯幾題。
結果寫 naked_hsat20_report.json + 印表格。

用法:
  python exhibition/verify_naked_hsat20.py            # 全 20 題
  python exhibition/verify_naked_hsat20.py --items HSAT_115_1,HSAT_113_1
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
RUNNER = HERE / "naked_opus.py"
CASES = ROOT / "evaluation" / "test_cases_hsat20.json"
OUT_DIR = HERE / "static" / "naked_hsat20"
REPORT = OUT_DIR / "report.json"


def run_one(t: dict) -> dict:
    tid = t["id"]
    task_id = f"naked_{tid}_{int(time.time())}"
    out_dir = HERE / "static" / "runs" / task_id
    out_dir.mkdir(parents=True, exist_ok=True)
    target_file = ROOT / f"test_script_{task_id}.py"

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["TASK_TARGET_FILE"] = str(target_file)

    print(f"  ▶ NAKED: {tid}  ({t['knowledge_point']})", flush=True)
    t0 = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, str(RUNNER), task_id, str(out_dir)],
            input=t["topic"] + "\n",
            text=True, capture_output=True, env=env, timeout=900,
        )
    except subprocess.TimeoutExpired:
        target_file.unlink(missing_ok=True)
        return {"id": tid, "render": "TIMEOUT", "time_sec": 900, "error": "900s timeout"}
    dur = round(time.time() - t0, 1)

    lines = proc.stdout.splitlines()
    video_line = next((l for l in lines if l.startswith("[VIDEO] ")), None)
    render_ok = video_line is not None
    render_err_line = next((l for l in lines if l.startswith("[RENDER_ERROR] ")), None)

    dest = OUT_DIR / tid
    dest.mkdir(parents=True, exist_ok=True)

    # 保存 opus 生的代碼（render 前 runner 已寫進 target_file）+ 完整 stdout/stderr 供判讀
    if target_file.exists():
        (dest / "opus_code.py").write_text(
            target_file.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8"
        )
    (dest / "stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (dest / "stderr.txt").write_text(proc.stderr or "", encoding="utf-8")

    video_path = None
    if render_ok:
        src = Path(video_line[len("[VIDEO] "):].strip())
        if src.exists():
            import shutil
            shutil.copy(src, dest / "video.mp4")
            video_path = f"/static/naked_hsat20/{tid}/video.mp4"

    err = ""
    if not render_ok:
        err = render_err_line[len("[RENDER_ERROR] "):].strip() if render_err_line else (proc.stderr[-600:] if proc.stderr else "(no error captured)")

    target_file.unlink(missing_ok=True)
    return {
        "id": tid,
        "knowledge_point": t["knowledge_point"],
        "difficulty": t["difficulty"],
        "render": "OK" if render_ok else "FAIL",
        "time_sec": dur,
        "exit_code": proc.returncode,
        "video_path": video_path,
        "error": err,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", default="", help="逗號分隔的 id 子集")
    args = ap.parse_args()

    cases = json.loads(CASES.read_text(encoding="utf-8"))
    if args.items:
        wanted = set(args.items.split(","))
        cases = [c for c in cases if c["id"] in wanted]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n只跑 naked_opus 驗證 {len(cases)} 題高中學測\n" + "=" * 50)
    results = []
    for i, t in enumerate(cases, 1):
        print(f"\n[{i}/{len(cases)}]")
        results.append(run_one(t))
        REPORT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = sum(1 for r in results if r["render"] == "OK")
    fail = len(results) - ok
    print("\n" + "=" * 50)
    print(f"naked render: {ok} OK / {fail} FAIL  (共 {len(results)})\n")
    print(f"{'ID':14s} {'render':7s} {'time':6s} {'KP'}")
    for r in results:
        print(f"{r['id']:14s} {r['render']:7s} {r['time_sec']:>5}s  {r.get('knowledge_point','')}")
    print(f"\n📄 詳細報告: {REPORT}")


if __name__ == "__main__":
    main()
