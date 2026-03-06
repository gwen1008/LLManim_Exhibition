import os
import json
import re
from pathlib import Path

# Configuration
SESSION_ID = "20260220_021530"
PROJECT_ROOT = Path(".").resolve()
SESSION_DIR = PROJECT_ROOT / "runs" / SESSION_ID
BENCHMARK_ROOT = PROJECT_ROOT / "benchmarks"
TEST_CASES_FILE = PROJECT_ROOT / "evaluation" / "test_cases.json"

def recover():
    if not SESSION_DIR.exists():
        print("Session directory not found.")
        return

    with open(TEST_CASES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        cases = data["cases"] if isinstance(data, dict) and "cases" in data else data

    results = []
    
    # Scan session directory for completed cases
    for case in cases:
        case_id = case["id"]
        case_path = SESSION_DIR / case_id
        
        if case_path.exists() and (case_path / "video.mp4").exists():
            # Try to parse metrics from log if it exists
            metrics = {"iterations": "-", "defects": "-", "tokens": "-", "cost": "-", "duration": "-"}
            log_path = case_path / "thought_trace.log"
            if log_path.exists():
                content = log_path.read_text(encoding="utf-8")
                
                iter_matches = re.findall(r"第 (\d+) / \d+ 次嘗試", content)
                if iter_matches: metrics["iterations"] = max(int(m) for m in iter_matches)
                
                pt_match = re.search(r"Prompt: ([\d,]+)", content)
                ct_match = re.search(r"Completion: ([\d,]+)", content)
                if pt_match and ct_match:
                    p = int(pt_match.group(1).replace(",", ""))
                    c = int(ct_match.group(1).replace(",", ""))
                    metrics["tokens"] = f"{p+c} ({p}/{c})"
                
                cost_match = re.search(r"Estimated Cost: \$([0-9.]+)", content)
                if cost_match: metrics["cost"] = f"${float(cost_match.group(1)):.4f}"
                
                defect_matches = re.findall(r"Detected (\d+) defect\(s\)", content)
                if defect_matches: metrics["defects"] = sum(int(m) for m in defect_matches)

            # Find Benchmark 
            old_video_rel = "N/A"
            for b_dir in BENCHMARK_ROOT.iterdir():
                if b_dir.is_dir() and b_dir.name.startswith(case_id):
                    old_video_rel = f"../../benchmarks/{b_dir.name}/result.mp4"
                    break

            results.append({
                "id": case_id,
                "topic": case["topic"],
                "new_video": f"{case_id}/video.mp4",
                "old_video": old_video_rel,
                "trace_link": f"{case_id}/thought_trace.log",
                "metrics": metrics,
                "status": "Success"
            })

    # Use the same HTML generation logic from run_evaluation
    generate_html(SESSION_DIR, results)
    print(f"✅ Recovered {len(results)} cases. Report generated at {SESSION_DIR}/comparison.html")

def generate_html(session_dir, results):
    html = """
    <html><head><title>RECOVERED: A/B Comparison & Analytics</title>
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
        .trace-link { display: block; margin-top: 25px; padding: 10px; background: #1976D2; color: white; text-decoration: none; border-radius: 6px; font-size: 0.85em; text-align: center; }
    </style></head>
    <body>
        <h1 style="text-align:center;">🩹 RECOVERED Report: Session """ + SESSION_ID + """</h1>
        <div class="content">
    """
    for r in results:
        m = r['metrics']
        html += f"""
        <div class="row">
            <div class="info">
                <div class="badge">{r['id']}</div>
                <h3>{r['topic']}</h3>
                <div class="metrics-table">
                    <div class="metrics-row"><span>Iterations:</span> <span class="metrics-val">{m['iterations']}</span></div>
                    <div class="metrics-row"><span>Defects:</span> <span class="metrics-val">{m['defects']}</span></div>
                    <div class="metrics-row"><span>Tokens:</span> <span class="metrics-val">{m['tokens']}</span></div>
                    <div class="metrics-row"><span>Cost:</span> <span class="metrics-val">{m['cost']}</span></div>
                </div>
                <a href="{r['trace_link']}" class="trace-link" target="_blank">🔍 View Trace</a>
            </div>
            <div class="video-box">
                <span class="label">◀️ OLD Bench</span>
                {f'<video controls src="{r["old_video"]}"></video>' if r["old_video"] != "N/A" else "N/A"}
            </div>
            <div class="video-box">
                <span class="label">NEW Run ▶️</span>
                <video controls src="{r['new_video']}"></video>
            </div>
        </div>
        """
    html += "</div></body></html>"
    with open(session_dir / "comparison.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    recover()
