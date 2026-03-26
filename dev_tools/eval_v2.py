import os
import sys
import json
import subprocess
import time
import csv
import re
from datetime import datetime
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
STABLE_OUTPUTS = PROJECT_ROOT / "stable_outputs"
TEST_CASES_FILE = PROJECT_ROOT / "evaluation" / "test_cases.json"
REPORT_DIR = PROJECT_ROOT / "evaluation" / "reports"

class EMAEvaluator:
    def __init__(self, coder_choice="1"):
        self.coder_choice = coder_choice
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        
    def load_test_cases(self):
        with open(TEST_CASES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def run_case(self, case):
        topic = case["topic"]
        case_id = case["id"]
        
        print(f"\n🚀 [Running Case {case_id}]: {topic}")
        
        start_time = time.time()
        
        # Start main.py process
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        
        proc = subprocess.Popen(
            [sys.executable, "main.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env
        )
        
        full_output = []
        try:
            # Send Topic
            if proc.poll() is None:
                proc.stdin.write(topic + "\n")
                proc.stdin.flush()
            else:
                raise Exception("main.py closed unexpectedly before receiving topic.")

            # Small delay for the next prompt
            time.sleep(1) # Reduced delay
            
            # Send Coder Choice
            if proc.poll() is None:
                proc.stdin.write(self.coder_choice + "\n")
                proc.stdin.flush()
            else:
                # If it closed here, maybe it matched a template or crashed
                pass
            
            # Close stdin to allow process to proceed
            if proc.stdin:
                proc.stdin.close()
            
            # Read output in real-time
            while True:
                line = proc.stdout.readline()
                if not line and proc.poll() is not None:
                    break
                if line:
                    clean_line = line.strip()
                    full_output.append(clean_line)
                    if any(kw in clean_line for kw in ["🎬", "✍️", "🔄", "✨", "❌"]):
                        print(f"   {clean_line}")

        except Exception as e:
            print(f"❌ Error during execution: {e}")
            proc.kill()
            
        proc.wait(timeout=60)
        duration = round(time.time() - start_time, 2)
        combined_output = "\n".join(full_output)
        
        # If combined_output is empty or very short, something went wrong with the process start
        if len(combined_output) < 10:
            print(f"   ⚠️ [Critical] main.py produced almost no output. Check your environment or run 'python main.py' manually.")
            # Let's try to capture the return code
            return_code = proc.poll()
            if return_code != 0:
                print(f"   ⚠️ Process exited with return code: {return_code}")
        success_msg = any(kw in combined_output for kw in ["渲染成功", "Rendering Success"])
        
        # 1. Iterations
        iterations = 1
        iter_matches = re.findall(r"第 (\d+) / \d+ 次嘗試", combined_output)
        if iter_matches:
            iterations = max(int(m) for m in iter_matches)
            
        # 2. Token Breakdown
        prompt_tokens = 0
        comp_tokens = 0
        pt_match = re.search(r"Prompt: ([\d,]+)", combined_output)
        ct_match = re.search(r"Completion: ([\d,]+)", combined_output)
        if pt_match: prompt_tokens = int(pt_match.group(1).replace(",", ""))
        if ct_match: comp_tokens = int(ct_match.group(1).replace(",", ""))
        
        # 3. Cost
        cost = 0.0
        cost_match = re.search(r"Estimated Cost: \$([0-9.]+)", combined_output)
        if cost_match:
            cost = float(cost_match.group(1))

        # 4. Visual Defects
        defects_count = 0
        defect_matches = re.findall(r"Detected (\d+) defect\(s\)", combined_output)
        if defect_matches:
            defects_count = sum(int(m) for m in defect_matches)
            
        # 5. Video Verification
        video_found = False
        last_video_name = ""
        match = re.search(r"🎥\s+(.*\.mp4)", combined_output)
        if match:
            last_video_name = match.group(1).strip()
            if (STABLE_OUTPUTS / last_video_name).exists():
                video_found = True

        return {
            "id": case_id,
            "topic": topic,
            "status": "PASS" if (success_msg and video_found) else "FAIL",
            "iterations": iterations,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": comp_tokens,
            "cost_usd": cost,
            "vision_defects": defects_count,
            "duration": duration,
            "video_file": last_video_name if video_found else "N/A"
        }

    def run_benchmark(self):
        cases = self.load_test_cases()
        results = []
        
        print("="*60)
        print(f"📊 EMA Benchmarking v2.0 Started")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🤖 Coder Choice: {'Classic' if self.coder_choice == '1' else 'DSPy'}")
        print("="*60)
        
        for case in cases:
            res = self.run_case(case)
            results.append(res)
            
        self.save_reports(results)

    def save_reports(self, results):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # CSV Report
        csv_file = REPORT_DIR / f"benchmark_{timestamp}.csv"
        if results:
            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            
        # Summary
        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASS")
        avg_cost = sum(r["cost_usd"] for r in results) / total if total > 0 else 0
        avg_time = sum(r["duration"] for r in results) / total if total > 0 else 0
        avg_iters = sum(r["iterations"] for r in results) / total if total > 0 else 0
        total_tokens = sum(r["prompt_tokens"] + r["completion_tokens"] for r in results)
        
        print("\n" + "="*40)
        print("🏁 BENCHMARK SUMMARY")
        print("="*40)
        print(f"Total Cases:    {total}")
        print(f"Pass Rate:      {passed/total*100:.1f}% ({passed}/{total})")
        print(f"Avg Iterations: {avg_iters:.1f}")
        print(f"Avg Cost:       ${avg_cost:.4f} USD")
        print(f"Total Tokens:   {total_tokens:,}")
        print(f"Avg Time:       {avg_time:.1f}s")
        print(f"Report:         {csv_file.name}")
        print("="*40 + "\n")

if __name__ == "__main__":
    evaluator = EMAEvaluator(coder_choice="1")
    evaluator.run_benchmark()
