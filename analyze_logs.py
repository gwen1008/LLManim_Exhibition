import os
import re
from pathlib import Path
from collections import Counter

# Configuration
SESSION_ID = "20260219_201106"
PROJECT_ROOT = Path(".").resolve()
SESSION_DIR = PROJECT_ROOT / "runs" / SESSION_ID

def analyze():
    if not SESSION_DIR.exists():
        print(f"❌ Session directory {SESSION_ID} not found.")
        return

    report = []
    error_counts = Counter()
    defect_counts = Counter()
    
    print(f"🔍 Analyzing logs in {SESSION_DIR}...\n")
    
    # Iterate through all case folders
    for case_dir in sorted(SESSION_DIR.iterdir()):
        if not case_dir.is_dir(): continue
        
        case_id = case_dir.name
        log_path = case_dir / "thought_trace.log"
        
        if not log_path.exists():
            report.append(f"⚠️ [{case_id}] Log file missing.")
            continue
            
        content = log_path.read_text(encoding="utf-8")
        
        # 1. Check Execution Errors (Tracebacks)
        tracebacks = re.findall(r"Traceback \(most recent call last\).*?(\w+Error: .*?)\n", content, re.DOTALL)
        last_error = tracebacks[-1].strip() if tracebacks else "None"
        
        if last_error != "None":
            # Clean up error message (take the last line usually)
            last_error = last_error.split('\n')[-1]
            error_counts[last_error] += 1

        # 2. Check Vision Defects
        defects = re.findall(r"\[([A-Z_]+)\]", content)
        # Filter only known defect codes
        valid_codes = {"OVERLAP", "MISALIGNED", "LOW_CONTRAST", "CLUTTER", "TINY_TEXT", "HALLUCINATION"}
        case_defects = [d for d in defects if d in valid_codes]
        defect_counts.update(case_defects)
        
        # 3. Check Iterations
        iterations = 0
        iter_matches = re.findall(r"第 (\d+) / \d+ 次嘗試", content)
        if iter_matches: 
            iterations = max(int(m) for m in iter_matches)
        
        # Summary for this case
        status_icon = "✅" if last_error == "None" and iterations < 3 else "⚠️"
        if iterations >= 5: status_icon = "❌"
        
        report.append(f"{status_icon} [{case_id}] Iters: {iterations} | Error: {last_error} | Defects: {', '.join(set(case_defects))}")

    # Print Final Report
    print("="*60)
    print("📋  FULL DIAGNOSTIC REPORT")
    print("="*60)
    for line in report:
        print(line)
    
    print("\n" + "="*60)
    print("📉  TOP ERROR TYPES (Code/Runtime)")
    print("="*60)
    for err, count in error_counts.most_common(5):
        print(f"{count}x : {err}")

    print("\n" + "="*60)
    print("👁️  TOP VISUAL DEFECTS (Vision Agent)")
    print("="*60)
    for defect, count in defect_counts.most_common(5):
        print(f"{count}x : {defect}")

if __name__ == "__main__":
    analyze()
