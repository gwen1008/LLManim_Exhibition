
"""
Unified Entry Point for Arithmetic Animation Generation
Usage: python run_math.py [operation] [num1] [num2] [--interactive] [--render]

Supported operations:
  - add (Addition)
  - sub (Subtraction)
  - mul (Multiplication)
  - div (Division)
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import template modules
from templates import addition, subtraction, multiplication, division

# Try to import AudioEngine
try:
    from agents.audio_engine import AudioEngine
    AUDIO_ENGINE_AVAILABLE = True
except ImportError:
    AUDIO_ENGINE_AVAILABLE = False


def generate_math_video(operation, num1, num2, output_dir=None, interactive=False):
    """
    Generic pipeline: Narrative -> Audio -> Code -> (Render)
    """
    if output_dir is None:
        output_dir = Path("/tmp/math_output")
    output_dir.mkdir(exist_ok=True, parents=True)

    print("=" * 80)
    print(f"🎬 Generating {operation.upper()} Animation: {num1} vs {num2}")
    if interactive:
        print("   🌟 Interactive Mode Enabled")
    print("=" * 80)

    # 1. Dispatch Narrative Generation
    print("\n📝 Step 1: Generating Narrative...")
    
    if operation == "add":
        steps = addition.generate_addition_narrative(num1, num2, interactive)
        code_gen_func = addition.generate_vertical_addition_code
        scene_name = "VerticalAddition"
    elif operation == "sub":
        steps = subtraction.generate_subtraction_narrative(num1, num2, interactive)
        code_gen_func = subtraction.generate_vertical_subtraction_code
        scene_name = "VerticalSubtraction"
    elif operation == "mul":
        steps = multiplication.generate_multiplication_narrative(num1, num2, interactive)
        code_gen_func = multiplication.generate_vertical_multiplication_code
        scene_name = "VerticalMultiplication"
    elif operation == "div":
        steps = division.generate_division_narrative(num1, num2, interactive)
        code_gen_func = division.generate_long_division_code
        scene_name = "LongDivision"
    else:
        raise ValueError(f"Unknown operation: {operation}")

    print(f"   ✅ Generated {len(steps)} steps")

    # 2. Generate Audio
    print("\n🎙️ Step 2: Generating Audio...")
    global AUDIO_ENGINE_AVAILABLE
    audio_available = AUDIO_ENGINE_AVAILABLE
    
    if audio_available:
        try:
            audio_engine = AudioEngine(
                output_dir=str(output_dir / "audio"),
                topic=f"{operation}_{num1}_{num2}"
            )
            # AudioEngine updates steps in-place with duration and audio_path
            steps, final_audio_path = audio_engine.generate_narration(steps)
            print(f"   ✅ Audio generated successfully")
        except Exception as e:
            print(f"   ❌ AudioEngine failed: {e}")
            audio_available = False
    
    if not audio_available:
        print("   ⚠️ AudioEngine unavailable or failed. Using simulated durations.")
        for step in steps:
            # Estimate ~5 chars per second + base buffer
            step['duration'] = max(2.0, len(step.get('narrative', '')) / 5.0)

    total_duration = sum(s.get('duration', 0) for s in steps)
    print(f"   ✅ Total Duration: {total_duration:.2f}s")

    # 3. Generate Manim Code
    print("\n🎬 Step 3: Generating Manim Code...")
    code = code_gen_func(
        num1=num1, 
        num2=num2, 
        scene_name=scene_name,
        audio_steps=steps
    )
    
    code_path = output_dir / f"{operation}_{num1}_{num2}.py"
    with open(code_path, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"   ✅ Code saved to: {code_path}")
    
    return code_path, scene_name


def main():
    parser = argparse.ArgumentParser(description="Generate math animation with audio")
    parser.add_argument("operation", choices=["add", "sub", "mul", "div"], help="Operation type")
    parser.add_argument("num1", type=int, help="First number")
    parser.add_argument("num2", type=int, help="Second number")
    parser.add_argument("--output", type=str, default="stable_outputs_math", help="Output directory")
    parser.add_argument("--render", action="store_true", help="Render video after generation")
    parser.add_argument("--interactive", action="store_true", help="Enable interactive questions")
    
    args = parser.parse_args()
    
    code_path, scene_name = generate_math_video(
        args.operation, 
        args.num1, 
        args.num2, 
        output_dir=Path(args.output),
        interactive=args.interactive
    )
    
    if args.render:
        print("\n🎥 Rendering Video...")
        import subprocess
        subprocess.run(["manim", "-pql", str(code_path), scene_name], cwd=str(code_path.parent))

if __name__ == "__main__":
    main()
