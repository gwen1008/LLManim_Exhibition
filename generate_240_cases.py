import os
import json
import asyncio
from openai import AsyncOpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 取代成你系統通常使用的 API KEY 變數名稱
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

OUTPUT_FILE = Path("evaluation/test_cases_random_240.json")

PHASES = {
    "小學數學 (Elementary Math)": 80,
    "國中數學 (Middle School Math)": 80,
    "高中數學 (High School Math)": 80
}

SYS_PROMPT = """
You are an expert K-12 mathematics educator.
Generate 5 completely random, unique, and specific educational animation topics suitable for Manim (a mathematical animation engine).
CRITICAL RULE: The topics MUST be strictly pure mathematics aimed at {phase} students. Do NOT include physics, chemistry, college-level calculus, advanced algorithms, linear algebra, graph theory, or stochastic processes. Keep it intuitive, visual, and strictly within the standard {phase} mathematics curriculum.
Do not repeat topics. Make them visual and engaging.

JSON FORMAT EXACTLY:
{{
  "cases": [
    {{
      "category": "{phase}",
      "topic": "Traditional Chinese description of the animation (e.g. 畫出 4x3 的長方形並用動畫計算面積為 12)",
      "topic_en": "English translation of the topic",
      "description": "Short internal description of what is being visualized"
    }}
  ]
}}
"""

async def generate_batch(batch_idx, phase):
    print(f"Generating {phase} batch {batch_idx} (5 cases)...")
    try:
        prompt = SYS_PROMPT.format(phase=phase)
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Generate 5 unique random Manim animation topics specifically for {phase}."}
            ],
            response_format={"type": "json_object"},
            temperature=1.2 # 高一點增加隨機性
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return data.get("cases", [])
    except Exception as e:
        print(f"Error in {phase} batch {batch_idx}: {e}")
        return []

async def main():
    print(f"🚀 準備生成 240 題純數學 Manim 挑戰題 (小學80、國中80、高中80)...")
    all_cases = []
    
    tasks = []
    for phase, count in PHASES.items():
        batches = count // 5
        for i in range(batches):
            tasks.append(generate_batch(i, phase))
            
    results = await asyncio.gather(*tasks)
    
    for batch_cases in results:
        all_cases.extend(batch_cases)

    # 重新編號 ID
    for idx, case in enumerate(all_cases):
        case["id"] = f"RND_{idx+1:03d}"

    # 寫檔
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_cases, f, ensure_ascii=False, indent=4)
        
    print(f"✅ 成功生成 {len(all_cases)} 題！並儲存至 {OUTPUT_FILE}")
    print(f"💡 之後你可以用這個指令跑測試：")
    print(f"python run_evaluation.py --test-cases {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
