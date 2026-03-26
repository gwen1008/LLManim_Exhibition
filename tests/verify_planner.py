import sys
import os

# Ensure the current directory is in the python path
sys.path.append(os.getcwd())

from agents.planner.planner import Planner

def test_planner_text():
    print("Testing Planner with Text Prompt (Enhanced Style)...")
    planner = Planner()
    topic = "Explain the concept of specific gravity using a visual analogy"
    try:
        plan = planner.plan_script_from_prompt(topic)
        print("\n[SUCCESS] Plan Generated:\n")
        print(plan[:500] + "...\n(truncated)")
        
        if "Visual Elements" in planner.system_prompt:
            print("[CHECK] System Prompt contains 'Visual Elements': YES")
        else:
            print("[CHECK] System Prompt contains 'Visual Elements': NO")
            
    except Exception as e:
        print(f"\n[FAILURE] Error: {e}")

if __name__ == "__main__":
    test_planner_text()
