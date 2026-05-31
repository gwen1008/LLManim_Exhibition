"""掃 30 題 code.py 的 MathTex，跟 solution 比對找數學錯誤。

用 claudealt + Haiku 做語意比對：
- 抽 code.py 所有 MathTex 字串
- 抽 sample 的 solution（標準答案 + 計算步驟）
- 丟 Haiku 判斷算式是否對齊 solution

輸出 evaluation/benchmark_set/math_check_report.md
"""
from __future__ import annotations
import os, re, json, subprocess, sys
from pathlib import Path

BASE = Path(__file__).parent
SAMPLE = json.load(open(BASE.parent / "experiment_sample_30.json"))
SAMPLE_MAP = {c["id"]: c for c in SAMPLE}

MATHTEX_RE = re.compile(r'MathTex\(\s*r?["\'](.+?)["\']\s*[,)]', re.DOTALL)

SYSTEM_PROMPT = """你是數學動畫稽核員。任務：檢查 Manim 動畫的 MathTex 算式是否跟標準解題步驟一致。

我會給你：
- TOPIC: 原題目
- ANSWER: 標準答案
- SOLUTION: 解題步驟（每步該長怎樣）
- EQUATIONS: 動畫程式碼裡的 MathTex 字串（依出現順序）

你要判斷：
1. 每個 MathTex 是否「數學上正確」（左右兩邊真的相等）
2. 是否「跟 solution 對齊」（用到的步驟有沒有被改/漏）
3. **不需要 LaTeX 排版正確，只看數學邏輯**

輸出嚴格 JSON：
```json
{
  "verdict": "OK" 或 "ERROR",
  "errors": [
    {"idx": 0, "tex": "原 LaTeX", "issue": "為何錯", "should_be": "建議改成"},
    ...
  ],
  "summary": "一句話總結"
}
```

如果完全 OK，errors 為空陣列。
**不要輸出 JSON 以外的任何文字。**
"""


def extract_mathtex(code: str) -> list[str]:
    """從 code.py 抽 MathTex 字串。"""
    return MATHTEX_RE.findall(code)


def call_haiku(qid: str, sample: dict, equations: list[str]) -> dict:
    user_msg = f"""TOPIC: {sample['topic']}

ANSWER: {sample['answer']}

SOLUTION:
{sample['solution']}

EQUATIONS（共 {len(equations)} 個，依出現順序）：
"""
    for i, eq in enumerate(equations):
        user_msg += f"[{i}] {eq}\n"

    # claudealt retired 2026-05-23; run as current user. Override with
    # CLAUDE_RUN_AS_USER if you really need sudo -u.
    _run_as = os.getenv("CLAUDE_RUN_AS_USER", "")
    _claude_cmd = ["claude", "--model", "haiku",
                   "--append-system-prompt", SYSTEM_PROMPT,
                   "-p", user_msg]
    cmd = (["sudo", "-u", _run_as, "-i"] + _claude_cmd) if _run_as else _claude_cmd
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        return {"verdict": "FAIL", "errors": [], "summary": f"CLI 失敗: {result.stderr[:200]}"}

    out = result.stdout.strip()
    # 抽 JSON
    m = re.search(r'\{.*\}', out, re.DOTALL)
    if not m:
        return {"verdict": "FAIL", "errors": [], "summary": f"無法解析: {out[:200]}"}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError as e:
        return {"verdict": "FAIL", "errors": [], "summary": f"JSON parse 失敗: {e}"}


def main():
    qids = sys.argv[1:] if len(sys.argv) > 1 else sorted(
        d.name for d in BASE.iterdir() if d.is_dir() and d.name.startswith("Q")
    )

    all_results = []
    for qid in qids:
        code_path = BASE / qid / "code.py"
        if not code_path.exists():
            print(f"⏭  {qid}: code.py 不存在")
            continue
        if qid not in SAMPLE_MAP:
            print(f"⏭  {qid}: 不在 sample 裡")
            continue
        equations = extract_mathtex(code_path.read_text(encoding="utf-8"))
        if not equations:
            print(f"⏭  {qid}: 沒有 MathTex")
            continue
        print(f"▶ {qid}: 檢查 {len(equations)} 個算式...", flush=True)
        try:
            result = call_haiku(qid, SAMPLE_MAP[qid], equations)
        except Exception as e:
            result = {"verdict": "FAIL", "errors": [], "summary": str(e)}
        result["qid"] = qid
        result["equations"] = equations
        all_results.append(result)
        status = "✅" if result["verdict"] == "OK" else "🔴" if result["verdict"] == "ERROR" else "⚠️"
        print(f"  {status} {result['verdict']}: {result.get('summary','')[:80]}")

    # 寫 markdown report
    out = ["# Q030 數學算式檢查報告", ""]
    out.append(f"檢查 {len(all_results)} 題")
    ok_count = sum(1 for r in all_results if r["verdict"] == "OK")
    err_count = sum(1 for r in all_results if r["verdict"] == "ERROR")
    fail_count = sum(1 for r in all_results if r["verdict"] == "FAIL")
    out.append(f"- ✅ OK: {ok_count}")
    out.append(f"- 🔴 ERROR: {err_count}")
    out.append(f"- ⚠️ FAIL（檢查失敗）: {fail_count}")
    out.append("")
    out.append("---")
    out.append("")

    # 先列有問題的
    err_results = [r for r in all_results if r["verdict"] == "ERROR"]
    if err_results:
        out.append("## 🔴 有錯誤的題目")
        out.append("")
        for r in err_results:
            out.append(f"### {r['qid']} — {SAMPLE_MAP[r['qid']]['knowledge_point']}")
            out.append(f"**Summary**: {r.get('summary','')}")
            out.append("")
            for e in r.get("errors", []):
                idx = e.get("idx", "?")
                out.append(f"- **算式 [{idx}]**: `{e.get('tex','')}`")
                out.append(f"  - 問題: {e.get('issue','')}")
                out.append(f"  - 建議: `{e.get('should_be','')}`")
            out.append("")

    # 然後列 OK 的（只列題號）
    ok_results = [r for r in all_results if r["verdict"] == "OK"]
    if ok_results:
        out.append("## ✅ 通過檢查")
        out.append("")
        for r in ok_results:
            out.append(f"- {r['qid']} — {SAMPLE_MAP[r['qid']]['knowledge_point']}")
        out.append("")

    # FAIL 列出
    fail_results = [r for r in all_results if r["verdict"] == "FAIL"]
    if fail_results:
        out.append("## ⚠️ 檢查失敗（需人工確認）")
        out.append("")
        for r in fail_results:
            out.append(f"- {r['qid']}: {r.get('summary','')[:200]}")

    report = BASE / "math_check_report.md"
    report.write_text("\n".join(out), encoding="utf-8")
    print(f"\n報告寫入: {report}")
    print(f"✅ OK={ok_count}  🔴 ERROR={err_count}  ⚠️ FAIL={fail_count}")

    # 另存 raw JSON 方便後續處理
    json_path = BASE / "math_check_results.json"
    json.dump(all_results, open(json_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Raw JSON: {json_path}")


if __name__ == "__main__":
    main()
