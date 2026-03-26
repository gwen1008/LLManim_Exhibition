import os
import json
import time
import subprocess
import argparse
from pathlib import Path
from agents.core.llm_client import LLMClient
from agents.coder.prompter import CoderPrompter

PROJECT_ROOT = Path(__file__).parent.resolve()
TEST_CASES_FILE = PROJECT_ROOT / "evaluation" / "test_cases.json"
RUNS_ROOT = PROJECT_ROOT / "runs"

def run_zero_shot_baseline(num_runs=3):
    print(f"🚀 Starting Zero-Shot Baseline Evaluation ({num_runs} runs per topic)")
    
    with open(TEST_CASES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        cases = data["cases"] if isinstance(data, dict) and "cases" in data else data
        
    session_dir = RUNS_ROOT / f"zero_shot_baseline_{int(time.time())}"
    session_dir.mkdir(parents=True, exist_ok=True)
    
    llm = LLMClient()
    results = []
    
    for run_idx in range(1, num_runs + 1):
        print(f"\n==================================================")
        print(f"🔄 Starting Run {run_idx}/{num_runs}")
        print(f"==================================================")
        
        for case in cases:
            case_id = case["id"]
            topic = case["topic"]
            print(f"\n🎬 [Run {run_idx}] Testing {case_id}: {topic}")
            
            start_time = time.time()
            
            # Construct a basic prompt
            system_prompt = (
                "You are an expert Manim developer. Write a complete, runnable Manim Python script "
                "for the given educational topic. \n"
                "- Define a single class named `GeneratedScene` inheriting from `Scene`.\n"
                "- Do not format output with anything other than a single Python markdown block.\n"
                "- Do not include explanations, just the code."
            )
            user_prompt = f"Topic to animate:\n{topic}"
            
            try:
                raw_response = llm.ask_for_fix(system_prompt, user_prompt, temperature=0.3)
                code = llm.extract_code(raw_response)
                
                # Post-process to ensure class name matches and imports exist
                import re
                code = re.sub(r'class\s+\w+\(Scene\):', f'class GeneratedScene(Scene):', code, count=1)
                
                if "from manim import" not in code:
                    code = "from manim import *\n" + code
                    
                # Calculate Lines of Code (LOC) excluding empty lines and pure comments
                loc = len([line for line in code.split('\n') if line.strip() and not line.strip().startswith('#')])
                
                # Use a combined directory name for the run
                case_dir = session_dir / f"run_{run_idx}" / case_id
                case_dir.mkdir(parents=True, exist_ok=True)
                code_path = case_dir / "code.py"
                
                with open(code_path, "w", encoding="utf-8") as f:
                    f.write(code)
                    
                # Try to compile
                compile_success = False
                error_type = "None"
                try:
                    compile(code, "<coder>", "exec")
                    compile_success = True
                except SyntaxError as e:
                    print(f"❌ Syntax Error: {e}")
                    error_type = "SyntaxError"
                    
                # Try to render
                render_success = False
                if compile_success:
                    print("⏳ Rendering...")
                    env = os.environ.copy()
                    env["PYTHONPATH"] = str(PROJECT_ROOT)
                    proc = subprocess.run(
                        ["manim", "-ql", str(code_path), "GeneratedScene"],
                        env=env,
                        cwd=str(case_dir),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=300 # 5 min timeout
                    )
                    if proc.returncode == 0:
                        render_success = True
                        print("✅ Render Success")
                    else:
                        print("❌ Render Failed")
                        stderr_output = proc.stderr.decode("utf-8", errors="ignore")
                        with open(case_dir / "error.log", "w") as f:
                            f.write(stderr_output)
                        
                        # Extract basic error type
                        error_match = re.search(r"(\w+Error):", stderr_output)
                        if error_match:
                            error_type = error_match.group(1)
                        elif "Traceback" in stderr_output:
                            error_type = "RuntimeError"
                        else:
                            error_type = "RenderError"
                            
                # Retrieve session stats
                cost_stats = llm.session_stats
                prompt_tokens = cost_stats.get("total_prompt_tokens", 0)
                comp_tokens = cost_stats.get("total_completion_tokens", 0)
                cost_usd = cost_stats.get("total_cost_usd", 0.0)
                
                duration = time.time() - start_time
                results.append({
                    "run": run_idx,
                    "id": case_id,
                    "topic": topic,
                    "compile_success": compile_success,
                    "render_success": render_success,
                    "error_type": error_type,
                    "duration_sec": round(duration, 2),
                    "prompt_tokens": prompt_tokens,
                    "comp_tokens": comp_tokens,
                    "total_tokens": prompt_tokens + comp_tokens,
                    "cost_usd": cost_usd,
                    "loc": loc
                })
                
                llm.reset_session_stats()
                
            except Exception as e:
                print(f"❌ Error during generation/execution: {e}")
                results.append({
                    "run": run_idx,
                    "id": case_id,
                    "topic": topic,
                    "compile_success": False,
                    "render_success": False,
                    "error_type": type(e).__name__,
                    "duration_sec": round(time.time() - start_time, 2),
                    "total_tokens": 0,
                    "cost_usd": 0.0,
                    "loc": 0
                })
            
    # Save report
    report_path = session_dir / "baseline_report.csv"
    import csv
    with open(report_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Run", "Case ID", "Topic", "Compile Success", "Render Success", "Error Type", "LOC", "Duration (s)", "Total Tokens", "Cost (USD)"])
        for r in results:
            writer.writerow([
                r["run"],
                r["id"], 
                r["topic"], 
                r["compile_success"], 
                r["render_success"], 
                r.get("error_type", "None"),
                r.get("loc", 0),
                r.get("duration_sec", "-"),
                r.get("total_tokens", "-"),
                r.get("cost_usd", "-")
            ])
            
    success_count = sum(1 for r in results if r["render_success"])
    total = len(results)
    print(f"\n🎉 Baseline Testing Complete! Overall Pass rate: {success_count}/{total} ({(success_count/total)*100:.1f}%)")
    print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run zero-shot baseline evaluation.")
    parser.add_argument("--runs", type=int, default=3, help="Number of times to run the full suite (default 3)")
    args = parser.parse_args()
    
    run_zero_shot_baseline(num_runs=args.runs)
