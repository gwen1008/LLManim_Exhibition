"""
Code review for Q101~Q140 (gaps in Q101-Q150 session).
Output: runs/code_review_q101_q140.csv
"""
import csv, json, pathlib, sys, time

PROJECT_ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.utils.final_judge import FinalJudge

SOURCES = [
    {
        "test_cases": "evaluation/test_cases_q101_q150.json",
        "session_dir": "runs/20260507_132843",
        "ids": [f"Q{i}" for i in range(101, 141)],
    },
]

OUTPUT = PROJECT_ROOT / "runs" / "code_review_q101_q140.csv"
FIELDNAMES = [
    "Case ID", "Knowledge Point", "Difficulty",
    "FJ Math", "FJ Concept", "FJ Verdict", "FJ Veto Reason",
    "GT Match", "Issues Count", "Summary",
]

case_lookup = {}
for src in SOURCES:
    cases = json.loads((PROJECT_ROOT / src["test_cases"]).read_text())
    for c in cases:
        case_lookup[c["id"]] = c

judge = FinalJudge()
results = []
total = sum(len(s["ids"]) for s in SOURCES)
done = 0

for src in SOURCES:
    session_dir = PROJECT_ROOT / src["session_dir"]
    for cid in src["ids"]:
        done += 1
        case = case_lookup.get(cid)
        if not case:
            print(f"⚠️  [{done}/{total}] {cid}: test case not found")
            continue
        code_path = session_dir / cid / "code.py"
        if not code_path.exists():
            print(f"⚠️  [{done}/{total}] {cid}: code.py not found")
            continue

        code = code_path.read_text(encoding="utf-8")
        ground_truth = {"answer": case.get("answer", ""), "solution": case.get("solution", "")}

        print(f"🔍 [{done}/{total}] {cid} ...", end=" ", flush=True)
        t0 = time.time()
        try:
            result = judge._analyze_code(code, case.get("topic", ""), ground_truth=ground_truth)
            elapsed = round(time.time() - t0, 1)
            math_s = result.get("math_score")
            issues = result.get("issues", [])
            gt_match = result.get("ground_truth_match")

            if math_s is not None:
                verdict = "PASS" if int(math_s) >= 4 else "FAIL"
                veto = "" if verdict == "PASS" else "low_math_score"
            else:
                verdict, veto = "ERROR", "review_unavailable"

            print(f"Math={math_s} → {verdict} ({elapsed}s)")
            results.append({
                "Case ID": cid,
                "Knowledge Point": case.get("knowledge_point", ""),
                "Difficulty": case.get("difficulty", ""),
                "FJ Math": math_s if math_s is not None else "-",
                "FJ Concept": "-",
                "FJ Verdict": verdict,
                "FJ Veto Reason": veto,
                "GT Match": str(gt_match) if gt_match is not None else "-",
                "Issues Count": len(issues),
                "Summary": result.get("summary", "")[:200].replace("\n", " "),
            })
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({
                "Case ID": cid, "Knowledge Point": case.get("knowledge_point",""),
                "Difficulty": case.get("difficulty",""), "FJ Math": "-", "FJ Concept": "-",
                "FJ Verdict": "ERROR", "FJ Veto Reason": str(e)[:100],
                "GT Match": "-", "Issues Count": 0, "Summary": f"Exception: {e}",
            })

with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=FIELDNAMES)
    w.writeheader()
    w.writerows(results)

pass_c = sum(1 for r in results if r["FJ Verdict"] == "PASS")
fail_c = sum(1 for r in results if r["FJ Verdict"] == "FAIL")
err_c = sum(1 for r in results if r["FJ Verdict"] == "ERROR")
math_scores = [int(r["FJ Math"]) for r in results if r["FJ Math"] not in ("-", "")]
print(f"\n✅ 完成：{len(results)} 題 → {OUTPUT}")
print(f"PASS: {pass_c} | FAIL: {fail_c} | ERROR: {err_c}")
if math_scores:
    import statistics
    print(f"Math Score 平均: {statistics.mean(math_scores):.2f}")
