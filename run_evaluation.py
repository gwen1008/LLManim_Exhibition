import os
import signal
import argparse
import json
import subprocess
import shutil
import sys
import re
import csv
import time
from pathlib import Path
from datetime import datetime

# 配置
PROJECT_ROOT = Path(".").resolve()
TEST_CASES_FILE = PROJECT_ROOT / "evaluation" / "test_cases.json"
BENCHMARK_ROOT = PROJECT_ROOT / "benchmarks"
RUNS_ROOT = PROJECT_ROOT / "runs"

def main():
    parser = argparse.ArgumentParser(description="Run LLManim Agent Evaluation")
    parser.add_argument("--test-cases", type=str, default=str(TEST_CASES_FILE), help="Path to the test cases JSON file")
    parser.add_argument("--resume", type=str, help="Path to an existing session directory to resume from (e.g., runs/20260321_020857)")
    parser.add_argument("--case", type=str, help="Optional: Run only a specific Case ID")
    args = parser.parse_args()

    target_id = args.case
    test_cases_path = Path(args.test_cases)

    if args.resume:
        session_dir = Path(args.resume)
        if not session_dir.exists():
            print(f"❌ Error: Resume directory {session_dir} does not exist.")
            return
        print(f"🔄 Resuming Evaluation Session from: {session_dir}")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = RUNS_ROOT / timestamp
        session_dir.mkdir(parents=True, exist_ok=True)
        print(f"🚀 Starting New Evaluation Session: {timestamp}")

    print(f"📂 Results will be stored in: {session_dir}")

    # 讀取測試案例
    with open(test_cases_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        cases = data["cases"] if isinstance(data, dict) and "cases" in data else data

    results = []
    completed_cases = set()

    # 嘗試讀取舊的 summary.csv 來續傳
    summary_csv = session_dir / "summary.csv"
    if args.resume and summary_csv.exists():
        with open(summary_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                case_id = row["Case ID"]
                status = row["Status"]
                
                # 所有已跑過的題目都跳過（不管成功或失敗），保留真實成功率
                completed_cases.add(case_id)
                
                if status != "Success":
                    # Failed/TIMEOUT 直接保留舊紀錄，不重跑
                    results.append({
                        "id": case_id,
                        "topic": row["Topic"],
                        "category": row.get("Category", "-"),
                        "status": status,
                        "error": "Previous run failed/timeout (preserved)"
                    })
                    continue
                
                m = {
                    "iterations": row.get("Iterations", "-"),
                    "defects": row.get("Defects", "-"),
                    "tokens": row.get("Total Tokens", "-"),
                    "cost": row.get("Cost USD", "-"),
                    "duration": row.get("Duration Sec", "-"),
                    "code_lines": row.get("Code Lines", "-"),
                    "video_duration_sec": row.get("Video Duration Sec", "-"),
                    "exit_code": row.get("Exit Code", "-"),
                    "planner_sec": row.get("Planner Sec", "-"),
                    "coder_sec": row.get("Coder Sec", "-"),
                    "render_sec": row.get("Render Sec", "-"),
                    "vision_sec": row.get("Vision Sec", "-"),
                    "raw": {}
                }
                
                case_dir = session_dir / case_id
                cost_json = case_dir / "cost_report.json"
                if cost_json.exists():
                    with open(cost_json, "r", encoding="utf-8") as cf:
                        cdata = json.load(cf)
                        m["raw"]["prompt_tokens"] = cdata.get("total_prompt_tokens", 0)
                        m["raw"]["comp_tokens"] = cdata.get("total_completion_tokens", 0)
                        m["raw"]["cost"] = cdata.get("total_cost_usd", 0.0)
                        m["raw"]["num_calls"] = len(cdata.get("calls", []))
                
                # Try to load previous run's instrumentor log
                m["max_simultaneous_objects"] = row.get("Max Objects", "-")
                m["max_overlap_pairs"] = row.get("Max Overlap Pairs", "-")
                m["steps_with_overlap"] = row.get("Steps with Overlap", "-")
                
                old_v = "N/A"
                if BENCHMARK_ROOT.exists():
                    for b_dir in BENCHMARK_ROOT.iterdir():
                        if b_dir.is_dir() and b_dir.name.startswith(case_id):
                            old_v = f"../../benchmarks/{b_dir.name}/result.mp4"
                            break

                results.append({
                    "id": case_id,
                    "topic": row["Topic"],
                    "category": row.get("Category", "-"),
                    "status": status,
                    "new_video": f"{case_id}/video.mp4",
                    "old_video": old_v,
                    "trace_link": f"{case_id}/thought_trace.log",
                    "metrics": m
                })
        print(f"✅ Found {len(completed_cases)} successfully completed cases from previous run. Skipping them.")

    for case in cases:
        case_id = case["id"]
        if target_id and case_id != target_id:
            continue
            
        if case_id in completed_cases:
            print(f"⏭️ Skipping Task [{case_id}]: Already completed.")
            continue
            
        topic = case["topic"]
        print(f"\n🎬 Running Task [{case_id}]: {topic[:30]}...")
        
        start_time = time.time()
        
        # === [Fix] Clear stable_outputs before each run to avoid inheriting old results ===
        stable_out_dir = PROJECT_ROOT / "stable_outputs"
        if stable_out_dir.exists():
            shutil.rmtree(stable_out_dir)
        stable_out_dir.mkdir(exist_ok=True)

        # 執行 main.py (模擬手動輸入)
        # 我們直接帶入 topic 和 Coder 選項 (1: Classic)
        try:
            # 這裡我們調用 main.py 並捕捉輸出
            proc = subprocess.Popen(
                [sys.executable, "main.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(PROJECT_ROOT),
                preexec_fn=os.setsid  # [Fix] Create process group for clean kill
            )
            
            # [HOTFIX] Add 15-minute timeout (900 seconds)
            try:
                # 輸入 topic 並選擇 Coder (假設 Coder 選擇是 1)
                stdout, stderr = proc.communicate(input=f"{topic}\n1\n", timeout=900)
            except subprocess.TimeoutExpired:
                # [Fix] Kill entire process group (including manim subprocesses)
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except ProcessLookupError:
                    proc.kill()
                stdout, stderr = proc.communicate() # Capture what we can
                print(f"⏰ [TIMEOUT] Task {case_id} exceeded 15-minute limit. Force killing...")
                
                # [Fix] Save partial cost data for TIMEOUT tasks
                timeout_duration = round(time.time() - start_time, 2)
                timeout_cost = {}
                cost_json_timeout = stable_out_dir / "cost_report.json"
                if cost_json_timeout.exists():
                    with open(cost_json_timeout, "r", encoding="utf-8") as f:
                        timeout_cost = json.load(f)
                    case_dir_t = session_dir / case_id
                    case_dir_t.mkdir(exist_ok=True)
                    shutil.copy2(cost_json_timeout, case_dir_t / "cost_report.json")
                
                results.append({
                    "id": case_id,
                    "topic": topic,
                    "category": case.get("category", "-"),
                    "status": "TIMEOUT",
                    "error": "Task exceeded 15-minute hard limit (900s).",
                    "metrics": {
                        "duration": f"{timeout_duration}s",
                        "cost": f"${timeout_cost.get('total_cost_usd', 0.0):.4f}",
                        "raw": {
                            "prompt_tokens": timeout_cost.get("total_prompt_tokens", 0),
                            "comp_tokens": timeout_cost.get("total_completion_tokens", 0),
                            "cost": timeout_cost.get("total_cost_usd", 0.0),
                            "num_calls": len(timeout_cost.get("calls", []))
                        }
                    }
                })
                continue
            
            # 創建存放在本次 session 的位址
            case_dir = session_dir / case_id
            case_dir.mkdir(exist_ok=True)

            # === [New] Capture thinking process ===
            trace_path = case_dir / "thought_trace.log"
            with open(trace_path, "w", encoding="utf-8") as f:
                f.write("=== STDOUT ===\n")
                f.write(stdout)
                f.write("\n\n=== STDERR ===\n")
                f.write(stderr)
            
            # Extract cleaner reasoning blocks
            reasoning_blocks = re.findall(r'={10,}.*?={10,}', stdout, re.DOTALL)
            if reasoning_blocks:
                with open(case_dir / "reasoning_summary.md", "w", encoding="utf-8") as f:
                    f.write("# 🧠 Thinking Summary\n\n")
                    for block in reasoning_blocks:
                        f.write(f"```text\n{block}\n```\n\n")
                        
            # 從 stable_outputs 抓剛剛生成的最新檔案
            # 確保檔案存在才進行拷貝
            py_files = list(stable_out_dir.glob("*.py"))
            mp4_files = list(stable_out_dir.glob("*.mp4"))

            if not py_files or not mp4_files:
                raise FileNotFoundError(f"Task {case_id} finished but no .py or .mp4 files were found in stable_outputs.")

            latest_py = sorted(py_files, key=os.path.getmtime)[-1]
            latest_mp4 = sorted(mp4_files, key=os.path.getmtime)[-1]
            
            shutil.copy2(latest_py, case_dir / "code.py")
            shutil.copy2(latest_mp4, case_dir / "video.mp4")
            
            # [New] Collect code lines count
            with open(latest_py, "r", encoding="utf-8") as pyf:
                code_lines = len(pyf.readlines())
            
            # [New] Collect video duration via ffprobe
            video_duration_sec = 0.0
            try:
                ffprobe_result = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=noprint_wrappers=1:nokey=1", str(latest_mp4)],
                    capture_output=True, text=True, timeout=10
                )
                video_duration_sec = round(float(ffprobe_result.stdout.strip()), 2)
            except Exception:
                video_duration_sec = 0.0
            
            # [New] Capture exit code
            exit_code = proc.returncode
            
            # === [New] Parse Analytics from cost_report.json ===
            cost_json_path = stable_out_dir / "cost_report.json"
            cost_stats = {}
            if cost_json_path.exists():
                shutil.copy2(cost_json_path, case_dir / "cost_report.json")
                with open(cost_json_path, "r", encoding="utf-8") as f:
                    cost_stats = json.load(f)

            # [New] Parse SceneInstrumentor log
            scene_log_path = BENCHMARK_ROOT.parent / "scene_state_log.json"
            instrumentor_stats = {}
            if scene_log_path.exists():
                shutil.copy2(scene_log_path, case_dir / "scene_state_log.json")
                with open(scene_log_path, "r", encoding="utf-8") as f:
                    instrumentor_stats = json.load(f)

            iterations = 1
            iter_matches = re.findall(r"第 (\d+) / \d+ 次嘗試", stdout)
            if iter_matches: iterations = max(int(m) for m in iter_matches)
            
            prompt_tokens = cost_stats.get("total_prompt_tokens", 0)
            comp_tokens = cost_stats.get("total_completion_tokens", 0)
            cost = cost_stats.get("total_cost_usd", 0.0)
            num_calls = len(cost_stats.get("calls", []))

            time_planner_sec = cost_stats.get("time_planner_sec", 0.0)
            time_coder_sec = cost_stats.get("time_coder_sec", 0.0)
            time_render_sec = cost_stats.get("time_render_sec", 0.0)
            time_vision_sec = cost_stats.get("time_vision_sec", 0.0)

            defects_count = 0
            defect_matches = re.findall(r"Detected (\d+) defect\(s\)", stdout)
            if defect_matches: defects_count = sum(int(m) for m in defect_matches)

            duration = round(time.time() - start_time, 2)
            
            # 找 Benchmark 裡的舊版做對比
            old_video_rel = "N/A"

            if BENCHMARK_ROOT.exists():
                for b_dir in BENCHMARK_ROOT.iterdir():
                    if b_dir.is_dir() and b_dir.name.startswith(case_id):
                        old_video_rel = f"../../benchmarks/{b_dir.name}/result.mp4"
                        break
            
            results.append({
                "id": case_id,
                "topic": topic,
                "category": case.get("category", "-"),
                "new_video": f"{case_id}/video.mp4",
                "old_video": old_video_rel,
                "trace_link": f"{case_id}/thought_trace.log",
                "metrics": {
                    "iterations": iterations,
                    "defects": defects_count,
                    "tokens": f"{prompt_tokens + comp_tokens} ({prompt_tokens}/{comp_tokens})",
                    "cost": f"${cost:.4f}",
                    "duration": f"{duration}s",
                    "code_lines": code_lines,
                    "video_duration_sec": video_duration_sec,
                    "exit_code": exit_code,
                    "raw": {
                        "prompt_tokens": prompt_tokens,
                        "comp_tokens": comp_tokens,
                        "cost": cost,
                        "num_calls": num_calls
                    },
                    "planner_sec": f"{time_planner_sec:.2f}",
                    "coder_sec": f"{time_coder_sec:.2f}",
                    "render_sec": f"{time_render_sec:.2f}",
                    "vision_sec": f"{time_vision_sec:.2f}",
                    "max_simultaneous_objects": instrumentor_stats.get("max_simultaneous_objects", "-"),
                    "max_overlap_pairs": instrumentor_stats.get("max_overlap_pairs", "-"),
                    "steps_with_overlap": instrumentor_stats.get("steps_with_overlap", "-")
                },
                "status": "Success"
            })
            print(f"✅ [{case_id}] Completed in {duration}s (Price: ${cost:.4f})")
            
        except Exception as e:
            print(f"❌ [{case_id}] Failed: {e}")
            results.append({"id": case_id, "topic": topic, "category": case.get("category", "-"), "status": "Failed", "error": str(e)})

        # [New] Incremental saving just in case the script crashes completely
        try:
            generate_summary_csv(session_dir, results)
            generate_comparison_html(session_dir, results)
            generate_cost_dashboard(session_dir, results)
        except Exception as report_e:
            print(f"⚠️ Error generating reports for {case_id}: {report_e}")

    # 生成報告
    generate_summary_csv(session_dir, results)
    generate_comparison_html(session_dir, results)
    generate_cost_dashboard(session_dir, results)
    print(f"\n✨ Session Finalized!")
    print(f"📊 CSV Summary: {session_dir}/summary.csv")
    print(f"💻 HTML Gallery: {session_dir}/comparison.html")
    print(f"💰 Cost Dashboard: {session_dir}/cost_dashboard.md")

def generate_cost_dashboard(session_dir, results):
    import datetime
    md_path = session_dir / "cost_dashboard.md"
    
    total_calls = 0
    total_pt = 0
    total_ct = 0
    total_cost_usd = 0.0
    
    md_lines = [
        f"# LLManim Agent Cost Tracking Dashboard",
        f"**Generated**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Session**: `{session_dir.name}`",
        f"",
        f"| 關卡 (Task) | 狀態 | 模型呼叫次數 | Prompt Tokens | Completion Tokens | 總花費 (USD) | 台幣預估 (TWD) |",
        f"|---|---|---|---|---|---|---|"
    ]
    
    for r in results:
        status = r.get("status", "Unknown")
        # [Fix 5] Include ALL tasks — previously only Success was included, hiding true cost
        if "metrics" in r and status == "Success":
            raw = r["metrics"].get("raw", {})
            calls = raw.get("num_calls", 0)
            pt = raw.get("prompt_tokens", 0)
            ct = raw.get("comp_tokens", 0)
            cost = raw.get("cost", 0.0)
            
            total_calls += calls
            total_pt += pt
            total_ct += ct
            total_cost_usd += cost
            
            twd = cost * 32.5  # Approximate exchange rate
            status_badge = "✅ Success"
            md_lines.append(
                f"| `{r['id']}` | {status_badge} | {calls} | {pt:,} | {ct:,} | ${cost:.4f} | NT${twd:.2f} |"
            )
        else:
            # Failed/TIMEOUT tasks: show dashes for token/cost but still list them
            status_badge = f"❌ {status}"
            md_lines.append(
                f"| `{r['id']}` | {status_badge} | — | — | — | — | — |"
            )
        
    md_lines.append(f"| **總計 (Total)** | | **{total_calls}** | **{total_pt:,}** | **{total_ct:,}** | **${total_cost_usd:.4f}** | **NT${total_cost_usd * 32.5:.2f}** |")
    md_lines.append("")
    md_lines.append(f"> Note: TWD calculation assumes USD/TWD rate of 32.5")
    md_lines.append(f"> ⚠️ Failed tasks have no token data recorded (see Fix 5 in implementation plan for full cost tracking).")
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))


def generate_summary_csv(session_dir, results):
    csv_path = session_dir / "summary.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Case ID", "Topic", "Category", "Status", "Iterations", "Defects", "Max Objects", "Max Overlap Pairs", "Steps with Overlap", "Total Tokens", "Cost USD", "Duration Sec", "Code Lines", "Video Duration Sec", "Exit Code", "Planner Sec", "Coder Sec", "Render Sec", "Vision Sec"])
        for r in results:
            m = r.get("metrics", {})
            writer.writerow([
                r["id"], 
                r["topic"], 
                r.get("category", "-"),
                r["status"], 
                m.get("iterations", "-"),
                m.get("defects", "-"),
                m.get("max_simultaneous_objects", "-"),
                m.get("max_overlap_pairs", "-"),
                m.get("steps_with_overlap", "-"),
                m.get("tokens", "-"),
                m.get("cost", "-"),
                m.get("duration", "-"),
                m.get("code_lines", "-"),
                m.get("video_duration_sec", "-"),
                m.get("exit_code", "-"),
                m.get("planner_sec", "-"),
                m.get("coder_sec", "-"),
                m.get("render_sec", "-"),
                m.get("vision_sec", "-")
            ])

def generate_comparison_html(session_dir, results):
    html = """
    <html><head><title>A/B Comparison & Analytics</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0a0a; color: #eee; padding: 20px; }
        .row { display: flex; align-items: stretch; margin-bottom: 60px; border-bottom: 2px solid #222; padding-bottom: 40px; background: #111; border-radius: 12px; padding: 20px; }
        .info { width: 320px; padding-right: 30px; border-right: 1px solid #333; }
        .video-box { flex: 1; text-align: center; padding: 0 15px; }
        video { width: 100%; border: 3px solid #333; border-radius: 12px; background: #000; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h3 { color: #fff; margin-top: 15px; font-size: 1.1em; line-height: 1.4; }
        .label { font-weight: bold; color: #888; margin-bottom: 12px; display: block; text-transform: uppercase; letter-spacing: 1px; font-size: 0.8em; }
        .badge { display: inline-block; background: #2e7d32; padding: 4px 12px; border-radius: 20px; font-size: 0.75em; font-weight: bold; margin-bottom: 10px; }
        .metrics-table { font-size: 0.8em; color: #aaa; margin-top: 20px; border-top: 1px solid #333; padding-top: 15px; }
        .metrics-row { display: flex; justify-content: space-between; margin-bottom: 6px; }
        .metrics-val { color: #4CAF50; font-weight: bold; }
        .trace-link { 
            display: block; 
            margin-top: 25px; 
            padding: 10px; 
            background: #1976D2; 
            color: white; 
            text-decoration: none; 
            border-radius: 6px;
            font-size: 0.85em;
            text-align: center;
            transition: 0.2s;
        }
        .trace-link:hover { background: #1E88E5; transform: scale(1.02); }
    </style></head>
    <body>
        <h1 style="text-align:center; font-size:2.5em; margin-bottom:10px;">📊 LLManim Analytics Dashboard</h1>
        <p style="text-align:center; color:#888; margin-bottom:50px;">Session ID: """ + session_dir.name + """</p>
    """
    
    for r in results:
        if r.get("status") != "Success" or "metrics" not in r:
            continue
        m = r['metrics']
        
        html += f"""
        <div class="row">
            <div class="info">
                <div class="badge">{r['id']}</div>
                <h3>{r['topic']}</h3>
                
                <div class="metrics-table">
                    <div class="metrics-row"><span>Iteration Count:</span> <span class="metrics-val">{m.get('iterations', '-')}</span></div>
                    <div class="metrics-row"><span>Visual Defects (LLM):</span> <span class="metrics-val">{m.get('defects', '-')}</span></div>
                    <div class="metrics-row"><span>Max Simul. Objects:</span> <span class="metrics-val">{m.get('max_simultaneous_objects', '-')}</span></div>
                    <div class="metrics-row"><span>Steps w/ Overlap:</span> <span class="metrics-val">{m.get('steps_with_overlap', '-')}</span></div>
                    <div class="metrics-row"><span>Total Tokens:</span> <span class="metrics-val">{m.get('tokens', '-')}</span></div>
                    <div class="metrics-row"><span>Est. Cost (USD):</span> <span class="metrics-val">{m.get('cost', '-')}</span></div>
                    <div class="metrics-row"><span>Total Time:</span> <span class="metrics-val">{m.get('duration', '-')}</span></div>
                </div>

                <a href="{r['trace_link']}" class="trace-link" target="_blank">🔍 Full Reasoning Trace</a>
            </div>
            <div class="video-box">
                <span class="label">◀️ OLD Bench</span>
                {f'<video controls src="{r["old_video"]}"></video>' if r["old_video"] != "N/A" else '<div style="height:250px; background:#000; display:flex; align-items:center; justify-content:center; color:#333; border-radius:12px;">NO PREVIOUS</div>'}
            </div>
            <div class="video-box">
                <span class="label">NEW Run ▶️</span>
                <video controls src="{r['new_video']}"></video>
            </div>
        </div>
        """
        
    html += "</body></html>"
    with open(session_dir / "comparison.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
