#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLManim Agent 批量測試腳本 (Benchmark Script)
讓效能可被量化：執行後產出 benchmark_result.csv，可直接用 Excel 查看成功率。
"""

import subprocess
import sys
import os
import time
import csv
from datetime import datetime

# ---------------------------------------------------------------------------
# 📝 測試集 (Benchmark Set)：10–20 個主題，覆蓋不同數學類型
# ---------------------------------------------------------------------------
BENCHMARK_TOPICS = [
    # 幾何
    "畢氏定理",
    "圓面積公式",
    "正三角形內角",
    # 微積分／極限
    "微積分極限",
    "導數的定義",
    "基本積分",
    # 數列
    "費氏數列",
    "等差數列求和",
    # 代數
    "一元二次方程公式解",
    "二項式展開 (a+b)^2",
    # 函數／圖形
    "正弦函數 y=sin(x)",
    "指數函數 y=2^x",
    # 機率／其他
    "擲硬幣機率",
    "分數的加減",
]

# 輸出路徑（DoD：可直接用 Excel 開啟）
OUTPUT_CSV = "benchmark_result.csv"
OUTPUT_MD = "benchmark_result.md"

# 單一主題最長執行時間（秒），逾時視為 FAIL
PER_TOPIC_TIMEOUT = 600  # 10 分鐘

# 錯誤訊息最長字元（避免 CSV 單格過大）
ERROR_LOG_MAX = 500


def _project_root():
    return os.path.dirname(os.path.abspath(__file__))


def _run_one(topic: str) -> dict:
    """
    用 subprocess 呼叫 main.py，傳入主題、計時、擷取 stdout/stderr。
    回傳 {"topic", "status", "duration", "error"}。
    """
    root = _project_root()
    main_py = os.path.join(root, "main.py")
    env = os.environ.copy()
    env["BENCHMARK"] = "1"  # 不自動播放影片

    start = time.time()
    err_log = ""

    try:
        proc = subprocess.run(
            [sys.executable, main_py],
            cwd=root,
            input=f"{topic}\n",
            text=True,
            capture_output=True,
            timeout=PER_TOPIC_TIMEOUT,
            env=env,
        )
        duration = round(time.time() - start, 2)
        out, err = proc.stdout or "", proc.stderr or ""

        # 成功條件：main.py 印出 【任務成功】
        if "【任務成功】" in out:
            status = "PASS"
        else:
            status = "FAIL"
            # 擷取錯誤：stderr + stdout 中含 Error/Exception/遺憾/Traceback/❌ 的行
            parts = []
            if err.strip():
                parts.append(err.strip())
            for line in out.splitlines():
                s = line.strip()
                if any(k in s for k in ("Error", "Exception", "遺憾", "Traceback", "❌", "error：")):
                    parts.append(s)
            err_log = " | ".join(parts)[:ERROR_LOG_MAX]

        return {
            "topic": topic,
            "status": status,
            "duration": duration,
            "error": err_log,
        }

    except subprocess.TimeoutExpired:
        duration = round(time.time() - start, 2)
        return {
            "topic": topic,
            "status": "TIMEOUT",
            "duration": duration,
            "error": f"逾時 ({PER_TOPIC_TIMEOUT} 秒)",
        }
    except Exception as e:
        duration = round(time.time() - start, 2)
        return {
            "topic": topic,
            "status": "FAIL",
            "duration": duration,
            "error": str(e)[:ERROR_LOG_MAX],
        }


def _write_csv(results: list, path: str) -> None:
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    timeout = sum(1 for r in results if r["status"] == "TIMEOUT")
    rate = (passed / total * 100) if total else 0
    rate_str = f"{rate:.1f}% ({passed}/{total})"

    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["主題", "狀態", "耗時(秒)", "錯誤訊息"])
        for r in results:
            w.writerow([r["topic"], r["status"], r["duration"], r["error"]])
        w.writerow([])
        w.writerow(["【摘要】", "", "", ""])
        w.writerow(["總計", total, "", ""])
        w.writerow(["通過", passed, "", ""])
        w.writerow(["失敗", failed, "", ""])
        w.writerow(["超時", timeout, "", ""])
        w.writerow(["成功率", rate_str, "", ""])


def _write_md(results: list, path: str) -> None:
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    rate = (passed / total * 100) if total else 0

    with open(path, "w", encoding="utf-8") as f:
        f.write("# LLManim Agent Benchmark 報告\n\n")
        f.write(f"**執行時間：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 成功率\n\n")
        f.write(f"**{rate:.1f}%** ({passed}/{total})\n\n")
        f.write("## 明細\n\n")
        f.write("| 主題 | 狀態 | 耗時(秒) | 錯誤訊息 |\n")
        f.write("|------|------|----------|----------|\n")
        for r in results:
            err = (r["error"] or "").replace("|", "\\|").replace("\n", " ")
            f.write(f"| {r['topic']} | {r['status']} | {r['duration']} | {err} |\n")
        f.write("\n")


def run_benchmark():
    root = _project_root()
    os.chdir(root)

    total = len(BENCHMARK_TOPICS)
    print("\n" + "=" * 60)
    print("  LLManim Agent 批量測試 (Benchmark)")
    print("=" * 60)
    print(f"  測試主題數：{total}")
    print(f"  單題逾時：{PER_TOPIC_TIMEOUT} 秒")
    print(f"  輸出：{OUTPUT_CSV}、{OUTPUT_MD}")
    print("=" * 60 + "\n")

    results = []

    for i, topic in enumerate(BENCHMARK_TOPICS, 1):
        print(f"[{i}/{total}] 測試：{topic} ... ", end="", flush=True)
        r = _run_one(topic)
        results.append(r)
        print(f"{r['status']} ({r['duration']}s)")

    # 產出報告
    csv_path = os.path.join(root, OUTPUT_CSV)
    md_path = os.path.join(root, OUTPUT_MD)
    _write_csv(results, csv_path)
    _write_md(results, md_path)

    passed = sum(1 for r in results if r["status"] == "PASS")
    rate = (passed / total * 100) if total else 0

    print("\n" + "=" * 60)
    print(f"  成功率：{rate:.1f}% ({passed}/{total})")
    print("=" * 60)
    print(f"  CSV：{csv_path}")
    print(f"  MD ：{md_path}")
    print("  可直接用 Excel 開啟 CSV 查看。\n")


if __name__ == "__main__":
    run_benchmark()
