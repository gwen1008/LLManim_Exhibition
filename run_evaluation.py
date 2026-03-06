import os
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
    # 建立這次跑的 Session 資料夾
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = RUNS_ROOT / timestamp
    session_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 Starting Evaluation Session: {timestamp}")
    print(f"📂 Results will be stored in: {session_dir}")

    # 讀取測試案例
    with open(TEST_CASES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        cases = data["cases"] if isinstance(data, dict) and "cases" in data else data

    # 為了比較，我們需要紀錄結果
    results = []

    # 支持命令行過濾 Case ID
    target_id = sys.argv[1] if len(sys.argv) > 1 else None

    for case in cases:
        case_id = case["id"]
        if target_id and case_id != target_id:
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
                cwd=str(PROJECT_ROOT)
            )
            
            # [HOTFIX] Add 15-minute timeout (900 seconds)
            try:
                # 輸入 topic 並選擇 Coder (假設 Coder 選擇是 1)
                stdout, stderr = proc.communicate(input=f"{topic}\n1\n", timeout=900)
            except subprocess.TimeoutExpired:
                proc.kill()
                stdout, stderr = proc.communicate() # Capture what we can
                print(f"⏰ [TIMEOUT] Task {case_id} exceeded 15-minute limit. Force killing...")
                results.append({
                    "id": case_id,
                    "topic": topic,
                    "status": "TIMEOUT",
                    "error": "Task exceeded 15-minute hard limit (900s)."
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
            
            # === [New] Parse Analytics from cost_report.json ===
            cost_json_path = stable_out_dir / "cost_report.json"
            cost_stats = {}
            if cost_json_path.exists():
                shutil.copy2(cost_json_path, case_dir / "cost_report.json")
                with open(cost_json_path, "r", encoding="utf-8") as f:
                    cost_stats = json.load(f)

            iterations = 1
            iter_matches = re.findall(r"第 (\d+) / \d+ 次嘗試", stdout)
            if iter_matches: iterations = max(int(m) for m in iter_matches)
            
            prompt_tokens = cost_stats.get("total_prompt_tokens", 0)
            comp_tokens = cost_stats.get("total_completion_tokens", 0)
            cost = cost_stats.get("total_cost_usd", 0.0)
            num_calls = len(cost_stats.get("calls", []))

            defects_count = 0
            defect_matches = re.findall(r"Detected (\d+) defect\(s\)", stdout)
            if defect_matches: defects_count = sum(int(m) for m in defect_matches)

            duration = round(time.time() - start_time, 2)
            
            # 找 Benchmark 裡的舊版做對比
            old_video_rel = "N/A"

            for b_dir in BENCHMARK_ROOT.iterdir():
                if b_dir.is_dir() and b_dir.name.startswith(case_id):
                    old_video_rel = f"../../benchmarks/{b_dir.name}/result.mp4"
                    break
            
            results.append({
                "id": case_id,
                "topic": topic,
                "new_video": f"{case_id}/video.mp4",
                "old_video": old_video_rel,
                "trace_link": f"{case_id}/thought_trace.log",
                "metrics": {
                    "iterations": iterations,
                    "defects": defects_count,
                    "tokens": f"{prompt_tokens + comp_tokens} ({prompt_tokens}/{comp_tokens})",
                    "cost": f"${cost:.4f}",
                    "duration": f"{duration}s",
                    "raw": {
                        "prompt_tokens": prompt_tokens,
                        "comp_tokens": comp_tokens,
                        "cost": cost,
                        "num_calls": num_calls
                    }
                },
                "status": "Success"
            })
            print(f"✅ [{case_id}] Completed in {duration}s (Price: ${cost:.4f})")
            
        except Exception as e:
            print(f"❌ [{case_id}] Failed: {e}")
            results.append({"id": case_id, "topic": topic, "status": "Failed", "error": str(e)})

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
        writer.writerow(["Case ID", "Topic", "Status", "Iterations", "Defects", "Total Tokens", "Cost USD", "Duration Sec"])
        for r in results:
            m = r.get("metrics", {})
            writer.writerow([
                r["id"], 
                r["topic"], 
                r["status"], 
                m.get("iterations", "-"),
                m.get("defects", "-"),
                m.get("tokens", "-"),
                m.get("cost", "-"),
                m.get("duration", "-")
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
                    <div class="metrics-row"><span>Iteration Count:</span> <span class="metrics-val">{m['iterations']}</span></div>
                    <div class="metrics-row"><span>Visual Defects:</span> <span class="metrics-val">{m['defects']}</span></div>
                    <div class="metrics-row"><span>Total Tokens:</span> <span class="metrics-val">{m['tokens']}</span></div>
                    <div class="metrics-row"><span>Est. Cost (USD):</span> <span class="metrics-val">{m['cost']}</span></div>
                    <div class="metrics-row"><span>Total Time:</span> <span class="metrics-val">{m['duration']}</span></div>
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
