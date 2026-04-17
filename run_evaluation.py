import os
import signal
import argparse
import json
import subprocess
import shutil
import sys
import re
import csv
import time
import tempfile
import threading
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime

# 配置
PROJECT_ROOT = Path(".").resolve()
TEST_CASES_FILE = PROJECT_ROOT / "evaluation" / "test_cases.json"
BENCHMARK_ROOT = PROJECT_ROOT / "benchmarks"
RUNS_ROOT = PROJECT_ROOT / "runs"

try:
    from agents.utils.telemetry import compute_iou_summary
except Exception:
    compute_iou_summary = None


def run_pattern_checks(code: str, case: dict) -> dict:
    """對生成代碼跑 required/disallowed pattern 驗證，計算 pattern_rate 與 animation_score。"""
    required = case.get("required_patterns", [])
    disallowed = case.get("disallowed_patterns", [])
    min_anim = case.get("min_animation_count", 1)

    matched, missing = [], []
    for pattern in required:
        (matched if re.search(pattern, code, re.MULTILINE) else missing).append(pattern)

    violations = [p for p in disallowed if re.search(p, code, re.MULTILINE)]

    pattern_rate = round(len(matched) / len(required), 3) if required else 1.0
    anim_count = len(re.findall(r'self\.play\(', code))
    anim_score = round(min(anim_count / max(min_anim, 1), 1.0), 3)

    return {
        "pattern_rate": pattern_rate,
        "matched_patterns": matched,
        "missing_patterns": missing,
        "disallowed_violations": violations,
        "animation_count": anim_count,
        "animation_score": anim_score,
    }


def compute_quality_score(render_ok: bool, vision_ok: bool, pattern_rate: float, anim_score: float) -> float:
    """複合評分 = 0.4*render + 0.3*vision + 0.2*pattern + 0.1*animation"""
    return round(
        0.4 * float(render_ok)
        + 0.3 * float(vision_ok)
        + 0.2 * pattern_rate
        + 0.1 * anim_score,
        3
    )


def parse_error_types(stdout: str) -> str:
    """從 stdout 提取錯誤類型分佈，回傳 pipe-separated string。"""
    checks = [
        ("SYNTAX",          r"SyntaxError|Syntax Error"),
        ("IMPORT_ERROR",    r"ImportError|ModuleNotFoundError"),
        ("CLASS_NOT_FOUND", r"CLASS_NOT_FOUND|is not in the script"),
        ("TIMEOUT",         r"timed out after 120"),
        ("LINTER",          r"Static Analysis Failed|靜態審查失敗"),
        ("VISION_FAIL",     r"Visual Check Failed|視覺審查失敗"),
        ("LATEX_ERROR",     r"latex error converting|LaTeX Compiler Output"),
    ]
    found = [label for label, pattern in checks if re.search(pattern, stdout)]
    return "|".join(found) if found else "NONE"


def run_single_case(case: dict, session_dir: Path, project_root: Path, benchmark_root: Path) -> dict:
    """
    Run one evaluation case in isolation.
    Uses a per-case tmpdir as EVAL_OUTPUT_DIR so parallel workers never conflict.
    Returns a result dict (same shape as the serial loop produces).
    """
    case_id = case["id"]
    topic = case["topic"]
    start_time = time.time()

    with tempfile.TemporaryDirectory(prefix=f"llmanim_eval_{case_id}_") as tmp_out:
        env = os.environ.copy()
        env["EVAL_OUTPUT_DIR"] = tmp_out

        try:
            proc = subprocess.Popen(
                [sys.executable, "main.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(project_root),
                preexec_fn=os.setsid,
                env=env,
            )
            try:
                stdout, stderr = proc.communicate(input=f"{topic}\n1\n", timeout=900)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except ProcessLookupError:
                    proc.kill()
                stdout, stderr = proc.communicate()
                print(f"⏰ [TIMEOUT] Task {case_id} exceeded 15-minute limit.")

                timeout_duration = round(time.time() - start_time, 2)
                timeout_cost = {}
                cost_json_timeout = Path(tmp_out) / "cost_report.json"
                timeout_case_dir = session_dir / case_id
                timeout_case_dir.mkdir(exist_ok=True)

                # 保留 thought_trace.log 讓事後診斷 TIMEOUT 原因
                with open(timeout_case_dir / "thought_trace.log", "w", encoding="utf-8") as f:
                    f.write("=== STDOUT ===\n")
                    f.write(stdout or "")
                    f.write("\n\n=== STDERR ===\n")
                    f.write(stderr or "")

                if cost_json_timeout.exists():
                    with open(cost_json_timeout) as f:
                        timeout_cost = json.load(f)
                    shutil.copy2(cost_json_timeout, timeout_case_dir / "cost_report.json")

                return {
                    "id": case_id, "topic": topic,
                    "category": case.get("category", "-"),
                    "status": "TIMEOUT",
                    "error": "Task exceeded 15-minute hard limit (900s).",
                    "metrics": {
                        "duration": f"{timeout_duration}s",
                        "cost": f"${timeout_cost.get('total_cost_usd', 0.0):.4f}",
                        "raw": {
                            "prompt_tokens": timeout_cost.get("total_prompt_tokens", 0),
                            "comp_tokens": timeout_cost.get("total_completion_tokens", 0),
                            "cost": timeout_cost.get("total_cost_usd", 0.0),
                            "num_calls": len(timeout_cost.get("calls", []))
                        }
                    }
                }

            # Archive outputs to session_dir
            case_dir = session_dir / case_id
            case_dir.mkdir(exist_ok=True)

            trace_path = case_dir / "thought_trace.log"
            with open(trace_path, "w", encoding="utf-8") as f:
                f.write("=== STDOUT ===\n")
                f.write(stdout)
                f.write("\n\n=== STDERR ===\n")
                f.write(stderr)

            reasoning_blocks = re.findall(r'={10,}.*?={10,}', stdout, re.DOTALL)
            if reasoning_blocks:
                with open(case_dir / "reasoning_summary.md", "w", encoding="utf-8") as f:
                    f.write("# 🧠 Thinking Summary\n\n")
                    for block in reasoning_blocks:
                        f.write(f"```text\n{block}\n```\n\n")

            tmp_path = Path(tmp_out)
            py_files = list(tmp_path.glob("*.py"))
            # mp4 may be at root (stable_outputs mode) or under media/videos/... (EVAL_OUTPUT_DIR mode)
            mp4_files = list(tmp_path.glob("*.mp4")) or list(tmp_path.rglob("*.mp4"))

            if not py_files or not mp4_files:
                raise FileNotFoundError(f"Task {case_id} finished but no .py or .mp4 in tmp output dir.")

            latest_py = sorted(py_files, key=os.path.getmtime)[-1]
            latest_mp4 = sorted(mp4_files, key=os.path.getmtime)[-1]

            shutil.copy2(latest_py, case_dir / "code.py")
            shutil.copy2(latest_mp4, case_dir / "video.mp4")

            with open(latest_py, encoding="utf-8") as pyf:
                py_content = pyf.read()
            code_lines = py_content.count("\n") + 1

            pattern_result = run_pattern_checks(py_content, case)
            vision_ok = bool(re.search(r"視覺審查通過|Vision.*PASS", stdout))
            quality_score = compute_quality_score(
                render_ok=True, vision_ok=vision_ok,
                pattern_rate=pattern_result["pattern_rate"],
                anim_score=pattern_result["animation_score"],
            )
            error_types = parse_error_types(stdout)

            video_duration_sec = 0.0
            try:
                ffprobe_result = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=noprint_wrappers=1:nokey=1", str(case_dir / "video.mp4")],
                    capture_output=True, text=True, timeout=10
                )
                video_duration_sec = round(float(ffprobe_result.stdout.strip()), 2)
            except Exception:
                pass

            exit_code = proc.returncode

            cost_json_path = tmp_path / "cost_report.json"
            cost_stats = {}
            if cost_json_path.exists():
                shutil.copy2(cost_json_path, case_dir / "cost_report.json")
                with open(cost_json_path) as f:
                    cost_stats = json.load(f)

            scene_log_path = project_root / "scene_state_log.json"
            instrumentor_stats = {}
            iou_summary = {}
            if scene_log_path.exists():
                shutil.copy2(scene_log_path, case_dir / "scene_state_log.json")
                with open(scene_log_path) as f:
                    instrumentor_stats = json.load(f)
                if compute_iou_summary is not None:
                    try:
                        iou_summary = compute_iou_summary(instrumentor_stats)
                    except Exception:
                        iou_summary = {}

            iterations = 1
            iter_matches = re.findall(r"第 (\d+) / \d+ 次嘗試", stdout)
            if iter_matches:
                iterations = max(int(m) for m in iter_matches)

            prompt_tokens = cost_stats.get("total_prompt_tokens", 0)
            comp_tokens = cost_stats.get("total_completion_tokens", 0)
            cost = cost_stats.get("total_cost_usd", 0.0)
            num_calls = len(cost_stats.get("calls", []))

            defects_count = 0
            defect_matches = re.findall(r"Detected (\d+) defect\(s\)", stdout)
            if defect_matches:
                defects_count = sum(int(m) for m in defect_matches)

            duration = round(time.time() - start_time, 2)

            old_video_rel = "N/A"
            if benchmark_root.exists():
                for b_dir in benchmark_root.iterdir():
                    if b_dir.is_dir() and b_dir.name.startswith(case_id):
                        old_video_rel = f"../../benchmarks/{b_dir.name}/result.mp4"
                        break

            print(f"✅ [{case_id}] Completed in {duration}s (Price: ${cost:.4f})")
            return {
                "id": case_id, "topic": topic,
                "category": case.get("category", "-"),
                "new_video": f"{case_id}/video.mp4",
                "old_video": old_video_rel,
                "trace_link": f"{case_id}/thought_trace.log",
                "metrics": {
                    "iterations": iterations,
                    "defects": defects_count,
                    "tokens": f"{prompt_tokens + comp_tokens} ({prompt_tokens}/{comp_tokens})",
                    "cost": f"${cost:.4f}",
                    "duration": f"{duration}s",
                    "code_lines": code_lines,
                    "video_duration_sec": video_duration_sec,
                    "exit_code": exit_code,
                    "raw": {"prompt_tokens": prompt_tokens, "comp_tokens": comp_tokens,
                            "cost": cost, "num_calls": num_calls},
                    "planner_sec": f"{cost_stats.get('time_planner_sec', 0.0):.2f}",
                    "coder_sec": f"{cost_stats.get('time_coder_sec', 0.0):.2f}",
                    "render_sec": f"{cost_stats.get('time_render_sec', 0.0):.2f}",
                    "vision_sec": f"{cost_stats.get('time_vision_sec', 0.0):.2f}",
                    "rag_sec": f"{cost_stats.get('time_rag_sec', 0.0):.2f}",
                    "max_simultaneous_objects": instrumentor_stats.get("max_simultaneous_objects", "-"),
                    "max_overlap_pairs": instrumentor_stats.get("max_overlap_pairs", "-"),
                    "steps_with_overlap": instrumentor_stats.get("steps_with_overlap", "-"),
                    "iou_overlap_pairs_max": iou_summary.get("iou_overlap_pairs_max", "-"),
                    "steps_with_iou_overlap": iou_summary.get("steps_with_iou_overlap", "-"),
                    "worst_overlap_step_pct": iou_summary.get("worst_overlap_step_pct", "-"),
                    "fj_weighted":       cost_stats.get("final_judge", {}).get("weighted_total", "-"),
                    "fj_math":           cost_stats.get("final_judge", {}).get("scores", {}).get("math_correctness", "-"),
                    "fj_concept":        cost_stats.get("final_judge", {}).get("scores", {}).get("concept_alignment", "-"),
                    "fj_visual":         cost_stats.get("final_judge", {}).get("scores", {}).get("visual_clarity", "-"),
                    "quality_score": quality_score,
                    "pattern_rate": pattern_result["pattern_rate"],
                    "animation_count": pattern_result["animation_count"],
                    "missing_patterns": "|".join(pattern_result["missing_patterns"]),
                    "disallowed_violations": "|".join(pattern_result["disallowed_violations"]),
                    "error_types": error_types,
                },
                "status": "Success"
            }

        except Exception as e:
            print(f"❌ [{case_id}] Failed: {e}")
            return {"id": case_id, "topic": topic, "category": case.get("category", "-"),
                    "status": "Failed", "error": str(e)}


def run_compare():
    """掃描所有 runs/*/summary.csv，輸出跨 session 的 FinalJudge 趨勢表。"""
    sessions = sorted([
        d for d in RUNS_ROOT.iterdir()
        if d.is_dir() and (d / "summary.csv").exists()
    ])[-8:]  # 只保留最近 8 個 session
    if not sessions:
        print("❌ No completed sessions found in runs/")
        return

    rows = []
    all_case_ids = set()
    for s in sessions:
        csv_path = s / "summary.csv"
        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            cases = list(reader)

        n_total = len(cases)
        n_success = sum(1 for c in cases if c.get("Status") == "Success")

        fj_weighted_vals = []
        fj_math_vals = []
        fj_concept_vals = []
        fj_visual_vals = []
        fj_cost_vals = []

        per_case = {}
        for c in cases:
            cid = c.get("Case ID", "")
            all_case_ids.add(cid)
            weighted = c.get("FJ Weighted", "-")
            math_s = c.get("FJ Math", "-")
            concept_s = c.get("FJ Concept", "-")
            visual_s = c.get("FJ Visual", "-")
            per_case[cid] = {
                "weighted": weighted,
                "math": math_s,
            }
            # Extract FinalJudge-specific cost from cost_report.json
            cost_path = s / cid / "cost_report.json"
            if cost_path.exists():
                try:
                    with open(cost_path, encoding="utf-8") as _cf:
                        _cdata = json.load(_cf)
                    fj_models = {"anthropic/claude-sonnet-4.6", "anthropic/claude-sonnet-4.5"}
                    _fj_c = sum(
                        call.get("cost", 0)
                        for call in _cdata.get("calls", [])
                        if call.get("model", "") in fj_models
                        or (call.get("model", "") == "gpt-4o-mini" and
                            _cdata.get("final_judge"))
                    )
                    if _fj_c > 0:
                        fj_cost_vals.append(_fj_c)
                except Exception:
                    pass
            try:
                fj_weighted_vals.append(float(weighted))
            except (ValueError, TypeError):
                pass
            try:
                fj_math_vals.append(float(math_s))
            except (ValueError, TypeError):
                pass
            try:
                fj_concept_vals.append(float(concept_s))
            except (ValueError, TypeError):
                pass
            try:
                fj_visual_vals.append(float(visual_s))
            except (ValueError, TypeError):
                pass

        def avg(lst):
            return f"{sum(lst)/len(lst):.2f}" if lst else "-"

        def total_cost(lst):
            return f"${sum(lst):.4f}" if lst else "-"

        rows.append({
            "session": s.name,
            "n_total": n_total,
            "n_success": n_success,
            "avg_weighted": avg(fj_weighted_vals),
            "avg_math": avg(fj_math_vals),
            "avg_concept": avg(fj_concept_vals),
            "avg_visual": avg(fj_visual_vals),
            "fj_cost": total_cost(fj_cost_vals),
            "per_case": per_case,
        })

    # ── 總覽表 ──────────────────────────────────────────────────────────────
    print("\n" + "═" * 90)
    print("  LLManim FinalJudge 跨 Session 趨勢")
    print("═" * 90)
    hdr = f"{'Session':<26} {'Cases':>6} {'Weighted':>10} {'Math':>6} {'Concept':>8} {'Visual':>7} {'FJ Cost':>9}"
    print(hdr)
    print("─" * 80)
    for r in rows:
        trend = ""
        if len(rows) > 1:
            idx = rows.index(r)
            if idx > 0:
                prev_w = rows[idx - 1]["avg_weighted"]
                curr_w = r["avg_weighted"]
                try:
                    delta = float(curr_w) - float(prev_w)
                    trend = f" {'▲' if delta > 0 else '▼' if delta < 0 else '─'}{abs(delta):.2f}"
                except (ValueError, TypeError):
                    pass
        cases_str = f"{r['n_success']}/{r['n_total']}"
        print(f"{r['session']:<26} {cases_str:>6}   {r['avg_weighted']:>6}{trend:<8} {r['avg_math']:>6} {r['avg_concept']:>8} {r['avg_visual']:>7} {r['fj_cost']:>9}")

    print("─" * 70)

    # ── Per-case 歷史追蹤（只顯示至少有一個 session 有 FJ 資料的 case）──────────────────────
    tracked_cases = sorted(
        cid for cid in all_case_ids
        if any(
            r["per_case"].get(cid, {}).get("weighted", "-") not in ("-", "")
            for r in rows
        )
    )
    print(f"\n{'Per-Case FinalJudge 歷史 (weighted / math / verdict)'}")
    print("─" * 90)
    case_col_w = 10
    header = f"{'Case':<{case_col_w}}"
    for r in rows:
        header += f"  {r['session'][:18]:<20}"
    print(header)
    print("─" * 90)
    for cid in tracked_cases:
        line = f"{cid:<{case_col_w}}"
        for r in rows:
            pc = r["per_case"].get(cid)
            if pc:
                w = pc["weighted"]
                m = pc["math"]
                line += f"  w={w:>4} m={m:>4}        "
            else:
                line += f"  {'—':<20}"
        print(line)
    print("═" * 90 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Run LLManim Agent Evaluation")
    parser.add_argument("--test-cases", type=str, default=str(TEST_CASES_FILE), help="Path to the test cases JSON file")
    parser.add_argument("--resume", type=str, help="Path to an existing session directory to resume from (e.g., runs/20260321_020857)")
    parser.add_argument("--case", type=str, help="Optional: Run only a specific Case ID")
    parser.add_argument("--cases", type=str, help="Optional: Run only a comma-separated list of Case IDs")
    parser.add_argument("--workers", type=int, default=1,
                        help="Number of parallel workers (default: 1 = serial). "
                             "Each worker uses an isolated tmpdir so stable_outputs never conflict.")
    parser.add_argument("--compare", action="store_true",
                        help="Compare FinalJudge scores across all sessions in runs/")
    args = parser.parse_args()

    if args.compare:
        run_compare()
        return

    if args.case and args.cases:
        parser.error("Use either --case or --cases, not both.")

    target_id = args.case
    target_ids = None
    if args.cases:
        target_ids = {c.strip() for c in args.cases.split(",") if c.strip()}
        if not target_ids:
            parser.error("--cases was provided but no valid Case IDs were found.")
    test_cases_path = Path(args.test_cases)

    if args.resume:
        session_dir = Path(args.resume)
        if not session_dir.exists():
            print(f"❌ Error: Resume directory {session_dir} does not exist.")
            return
        print(f"🔄 Resuming Evaluation Session from: {session_dir}")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = RUNS_ROOT / timestamp
        session_dir.mkdir(parents=True, exist_ok=True)
        print(f"🚀 Starting New Evaluation Session: {timestamp}")

    print(f"📂 Results will be stored in: {session_dir}")

    # 讀取測試案例
    with open(test_cases_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        cases = data["cases"] if isinstance(data, dict) and "cases" in data else data

    results = []
    completed_cases = set()

    # 嘗試讀取舊的 summary.csv 來續傳
    summary_csv = session_dir / "summary.csv"
    if args.resume and summary_csv.exists():
        with open(summary_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                case_id = row["Case ID"]
                status = row["Status"]
                
                # 所有已跑過的題目都跳過（不管成功或失敗），保留真實成功率
                completed_cases.add(case_id)
                
                if status != "Success":
                    # Failed/TIMEOUT 直接保留舊紀錄，不重跑
                    results.append({
                        "id": case_id,
                        "topic": row["Topic"],
                        "category": row.get("Category", "-"),
                        "status": status,
                        "error": "Previous run failed/timeout (preserved)"
                    })
                    continue
                
                m = {
                    "iterations": row.get("Iterations", "-"),
                    "defects": row.get("Defects", "-"),
                    "tokens": row.get("Total Tokens", "-"),
                    "cost": row.get("Cost USD", "-"),
                    "duration": row.get("Duration Sec", "-"),
                    "code_lines": row.get("Code Lines", "-"),
                    "video_duration_sec": row.get("Video Duration Sec", "-"),
                    "exit_code": row.get("Exit Code", "-"),
                    "planner_sec": row.get("Planner Sec", "-"),
                    "coder_sec": row.get("Coder Sec", "-"),
                    "render_sec": row.get("Render Sec", "-"),
                    "vision_sec": row.get("Vision Sec", "-"),
                    "raw": {}
                }
                
                case_dir = session_dir / case_id
                cost_json = case_dir / "cost_report.json"
                if cost_json.exists():
                    with open(cost_json, "r", encoding="utf-8") as cf:
                        cdata = json.load(cf)
                        m["raw"]["prompt_tokens"] = cdata.get("total_prompt_tokens", 0)
                        m["raw"]["comp_tokens"] = cdata.get("total_completion_tokens", 0)
                        m["raw"]["cost"] = cdata.get("total_cost_usd", 0.0)
                        m["raw"]["num_calls"] = len(cdata.get("calls", []))
                
                # Try to load previous run's instrumentor log
                m["max_simultaneous_objects"] = row.get("Max Objects", "-")
                m["max_overlap_pairs"] = row.get("Max Overlap Pairs", "-")
                m["steps_with_overlap"] = row.get("Steps with Overlap", "-")
                
                old_v = "N/A"
                if BENCHMARK_ROOT.exists():
                    for b_dir in BENCHMARK_ROOT.iterdir():
                        if b_dir.is_dir() and b_dir.name.startswith(case_id):
                            old_v = f"../../benchmarks/{b_dir.name}/result.mp4"
                            break

                results.append({
                    "id": case_id,
                    "topic": row["Topic"],
                    "category": row.get("Category", "-"),
                    "status": status,
                    "new_video": f"{case_id}/video.mp4",
                    "old_video": old_v,
                    "trace_link": f"{case_id}/thought_trace.log",
                    "metrics": m
                })
        print(f"✅ Found {len(completed_cases)} successfully completed cases from previous run. Skipping them.")

    pending_cases = [
        c for c in cases
        if (
            (not target_id or c["id"] == target_id)
            and (target_ids is None or c["id"] in target_ids)
            and c["id"] not in completed_cases
        )
    ]
    for cid in completed_cases:
        print(f"⏭️ Skipping Task [{cid}]: Already completed.")

    workers = args.workers
    save_lock = threading.Lock()

    def _save_incremental():
        try:
            generate_summary_csv(session_dir, results)
            generate_comparison_html(session_dir, results)
            generate_cost_dashboard(session_dir, results)
        except Exception as report_e:
            print(f"⚠️ Error generating incremental reports: {report_e}")

    def _on_done(result: dict):
        with save_lock:
            results.append(result)
            _save_incremental()

    if workers <= 1:
        for case in pending_cases:
            print(f"\n🎬 Running Task [{case['id']}]: {case['topic'][:30]}...")
            result = run_single_case(case, session_dir, PROJECT_ROOT, BENCHMARK_ROOT)
            _on_done(result)
    else:
        print(f"⚡ Parallel mode: {workers} workers")
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(run_single_case, case, session_dir, PROJECT_ROOT, BENCHMARK_ROOT): case["id"]
                for case in pending_cases
            }
            for future in as_completed(futures):
                case_id = futures[future]
                try:
                    result = future.result()
                except Exception as e:
                    result = {"id": case_id, "topic": "", "category": "-",
                              "status": "Failed", "error": str(e)}
                _on_done(result)


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
        writer.writerow([
            "Case ID", "Topic", "Category", "Status",
            "FJ Weighted", "FJ Math", "FJ Concept", "FJ Visual",
            "Quality Score", "Pattern Rate", "Animation Count", "Missing Patterns", "Disallowed Violations", "Error Types",
            "Iterations", "Defects", "Max Objects", "Max Overlap Pairs", "Steps with Overlap",
            "Max IoU Overlap Pairs", "Steps with IoU Overlap", "Worst Overlap Step Pct",
            "Total Tokens", "Cost USD", "Duration Sec", "Code Lines", "Video Duration Sec",
            "Exit Code", "Planner Sec", "Coder Sec", "Render Sec", "Vision Sec"
        ])
        for r in results:
            m = r.get("metrics", {})
            writer.writerow([
                r["id"],
                r["topic"],
                r.get("category", "-"),
                r["status"],
                m.get("fj_weighted", "-"),
                m.get("fj_math", "-"),
                m.get("fj_concept", "-"),
                m.get("fj_visual", "-"),
                m.get("quality_score", "-"),
                m.get("pattern_rate", "-"),
                m.get("animation_count", "-"),
                m.get("missing_patterns", "-"),
                m.get("disallowed_violations", "-"),
                m.get("error_types", "-"),
                m.get("iterations", "-"),
                m.get("defects", "-"),
                m.get("max_simultaneous_objects", "-"),
                m.get("max_overlap_pairs", "-"),
                m.get("steps_with_overlap", "-"),
                m.get("iou_overlap_pairs_max", "-"),
                m.get("steps_with_iou_overlap", "-"),
                m.get("worst_overlap_step_pct", "-"),
                m.get("tokens", "-"),
                m.get("cost", "-"),
                m.get("duration", "-"),
                m.get("code_lines", "-"),
                m.get("video_duration_sec", "-"),
                m.get("exit_code", "-"),
                m.get("planner_sec", "-"),
                m.get("coder_sec", "-"),
                m.get("render_sec", "-"),
                m.get("vision_sec", "-"),
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
                    <div class="metrics-row"><span>⭐ Quality Score:</span> <span class="metrics-val">{m.get('quality_score', '-')}</span></div>
                    <div class="metrics-row"><span>Pattern Rate:</span> <span class="metrics-val">{m.get('pattern_rate', '-')}</span></div>
                    <div class="metrics-row"><span>Animation Count:</span> <span class="metrics-val">{m.get('animation_count', '-')}</span></div>
                    <div class="metrics-row"><span>Error Types:</span> <span class="metrics-val">{m.get('error_types', '-')}</span></div>
                    <div class="metrics-row"><span>Iteration Count:</span> <span class="metrics-val">{m.get('iterations', '-')}</span></div>
                    <div class="metrics-row"><span>Visual Defects (LLM):</span> <span class="metrics-val">{m.get('defects', '-')}</span></div>
                    <div class="metrics-row"><span>Max Simul. Objects:</span> <span class="metrics-val">{m.get('max_simultaneous_objects', '-')}</span></div>
                    <div class="metrics-row"><span>Steps w/ Overlap:</span> <span class="metrics-val">{m.get('steps_with_overlap', '-')}</span></div>
                    <div class="metrics-row"><span>Max IoU Pairs:</span> <span class="metrics-val">{m.get('iou_overlap_pairs_max', '-')}</span></div>
                    <div class="metrics-row"><span>Total Tokens:</span> <span class="metrics-val">{m.get('tokens', '-')}</span></div>
                    <div class="metrics-row"><span>Est. Cost (USD):</span> <span class="metrics-val">{m.get('cost', '-')}</span></div>
                    <div class="metrics-row"><span>Total Time:</span> <span class="metrics-val">{m.get('duration', '-')}</span></div>
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
