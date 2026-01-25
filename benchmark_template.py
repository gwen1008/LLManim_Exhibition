import subprocess
import time
import csv
from datetime import datetime

# 📝 這就是所謂的 "10-20 個主題的 Python List"
# 我們希望這份清單能覆蓋不同類型的數學，測試系統是否會「偏科」
TEST_TOPICS = [
    # 1. 基礎運算
    "Calculate 15 + 27 step by step",
    "Show the multiplication of 12 and 12",
    
    # 2. 幾何圖形 (測試繪圖能力)
    "Visual proof of Pythagorean theorem",
    "Calculate the area of a circle with radius 5",
    "Show the angles of an equilateral triangle",
    
    # 3. 代數 (測試公式顯示)
    "Solve the quadratic equation x^2 - 5x + 6 = 0",
    "Expand (a + b)^2",
    
    # 4. 微積分/函數 (測試座標系)
    "Plot the function y = sin(x)",
    "Show the limit of 1/x as x approaches infinity",
    
    # 5. 複雜敘述 (測試理解力)
    "A train travels 60 miles in 2 hours. What is its speed?",
]

def run_benchmark():
    results = []
    print(f"🚀 開始執行批量測試 (共 {len(TEST_TOPICS)} 個主題)...\n")
    
    for i, topic in enumerate(TEST_TOPICS, 1):
        print(f"[{i}/{len(TEST_TOPICS)}] 正在測試: '{topic}' ...")
        start_time = time.time()
        
        # 呼叫主程式
        # 注意：我們使用 subprocess 來模擬在終端機輸入指令
        try:
            # 這裡假設您的 main.py 可以接收 stdin 輸入
            process = subprocess.run(
                ["python", "main.py"],
                input=f"{topic}\n",
                text=True,
                capture_output=True,
                timeout=300  # 每個任務限時 5 分鐘，避免卡死
            )
            
            duration = round(time.time() - start_time, 2)
            
            # 判斷成功與否 (根據 main.py 的輸出關鍵字)
            is_success = "Task Success" in process.stdout or "【任務成功】" in process.stdout
            status = "PASS" if is_success else "FAIL"
            
            error_msg = ""
            if not is_success:
                # 嘗試抓取最後幾行錯誤
                error_lines = [line for line in process.stdout.split('\n') if "Error" in line or "Exception" in line]
                error_msg = error_lines[-1] if error_lines else "Unknown Error"
                
            print(f"   -> 結果: {status} ({duration}s)")
            
            results.append({
                "topic": topic,
                "status": status,
                "duration": duration,
                "error": error_msg
            })
            
        except subprocess.TimeoutExpired:
            print("   -> 結果: TIMEOUT")
            results.append({"topic": topic, "status": "TIMEOUT", "duration": 300, "error": "Process Timed Out"})
            
    # 輸出報告
    save_report(results)

def save_report(results):
    filename = f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # 計算成功率
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    rate = (passed / total) * 100
    
    print(f"\n📊 測試完成！成功率: {rate:.1f}% ({passed}/{total})")
    print(f"📝 詳細報告已儲存至: {filename}")
    
    keys = results[0].keys()
    with open(filename, "w", newline="") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

if __name__ == "__main__":
    run_benchmark()
