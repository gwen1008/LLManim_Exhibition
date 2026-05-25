"""Scan all 30 benchmark_set/*/code.py and extract set_subtitle(...) narration strings.

Outputs a markdown report so user can review which lines need 拼字→阿拉伯 conversion.
Does NOT modify any code.
"""
from __future__ import annotations
import re
from pathlib import Path

BASE = Path(__file__).parent

# Match: self.set_subtitle("...") OR self.set_subtitle('...')  with possible run_time kwarg
PATTERN = re.compile(
    r'self\.set_subtitle\(\s*(["\'])(.*?)\1',
    re.DOTALL,
)

# Heuristic: chinese 拼字數字 patterns worth flagging
CHINESE_NUM = re.compile(r'[負正零一二兩三四五六七八九十百千萬億分之又]')
CHINESE_ORD = re.compile(r'第[一二三四五六七八九十]+(步|個)')
SCIENTIFIC = re.compile(r'十的(負)?[一二三四五六七八九十]+次方')

def scan_one(qid: str, path: Path) -> list[dict]:
    src = path.read_text(encoding="utf-8")
    results = []
    for m in PATTERN.finditer(src):
        line_no = src[:m.start()].count("\n") + 1
        text = m.group(2)
        flags = []
        if CHINESE_NUM.search(text):
            flags.append("中文數字")
        if CHINESE_ORD.search(text):
            flags.append("中文序數")
        if SCIENTIFIC.search(text):
            flags.append("中文科學記號")
        results.append({
            "qid": qid,
            "line": line_no,
            "text": text,
            "flags": flags,
        })
    return results

def main():
    all_results = []
    qids = sorted(d.name for d in BASE.iterdir() if d.is_dir() and d.name.startswith("Q"))
    for qid in qids:
        code = BASE / qid / "code.py"
        if not code.exists():
            continue
        all_results.extend(scan_one(qid, code))

    # Markdown report
    out = ["# Benchmark Set 字幕掃描 report", ""]
    out.append(f"共 {len(qids)} 題、{len(all_results)} 條字幕")
    out.append("")
    flagged = [r for r in all_results if r["flags"]]
    out.append(f"**需要改的字幕**（含中文數字/序數/科學記號）: {len(flagged)} 條")
    out.append("")

    current_qid = None
    for r in all_results:
        if r["qid"] != current_qid:
            current_qid = r["qid"]
            out.append(f"\n## {current_qid}")
            out.append("")
        flag_str = f" `[{', '.join(r['flags'])}]`" if r["flags"] else ""
        out.append(f"- L{r['line']}{flag_str}")
        out.append(f"  > {r['text']}")

    report_path = BASE / "subtitle_scan_report.md"
    report_path.write_text("\n".join(out), encoding="utf-8")
    print(f"Report written: {report_path}")
    print(f"Total subtitles: {len(all_results)}, flagged: {len(flagged)}")

if __name__ == "__main__":
    main()
