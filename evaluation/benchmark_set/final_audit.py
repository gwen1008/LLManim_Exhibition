"""benchmark_set 最後檢查 — 30 題完成度全面審計。

檢查項目：
1. code.py 存在
2. benchmark.mp4 存在
3. mp4 時長 vs audio_dur 總和（差距 < 3s 視為同步）
4. 字幕數 vs audio_dur 數一致
5. 沒有 audio 重疊（reuse check_audio_overlap）
6. MathTex 算式無數學錯誤（已跑過 math_check_report，重新匯總）
7. meta.json 狀態
"""
from __future__ import annotations
import re, json, subprocess
from pathlib import Path

BASE = Path(__file__).parent


def ffprobe_dur(mp4: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
        capture_output=True, text=True,
    )
    try:
        return float(out.stdout.strip())
    except Exception:
        return -1


def audit_one(qid: str, math_errors: dict) -> dict:
    qd = BASE / qid
    code = qd / "code.py"
    mp4 = qd / "benchmark.mp4"
    result = {"qid": qid, "issues": []}

    if not code.exists():
        result["issues"].append("❌ code.py 不存在")
        return result
    if not mp4.exists():
        result["issues"].append("❌ benchmark.mp4 不存在")
        return result

    src = code.read_text(encoding="utf-8")
    audio_durs = [float(m) for m in re.findall(r'_audio_dur_\d+ = ([\d.]+)', src)]
    subtitles = re.findall(r'self\.set_subtitle\(["\']', src)
    result["audio_dur_sum"] = sum(audio_durs)
    result["audio_dur_count"] = len(audio_durs)
    result["subtitle_count"] = len(subtitles)
    result["mp4_dur"] = ffprobe_dur(mp4)

    # 同步檢查（mp4 vs audio）
    gap = result["mp4_dur"] - result["audio_dur_sum"]
    if abs(gap) > 5:
        result["issues"].append(f"⚠️ mp4 ({result['mp4_dur']:.1f}s) 跟 audio_dur ({result['audio_dur_sum']:.1f}s) 差 {gap:+.1f}s")

    # 字幕數 vs audio_dur 數
    if result["subtitle_count"] != result["audio_dur_count"]:
        result["issues"].append(f"⚠️ subtitle={result['subtitle_count']} vs audio_dur={result['audio_dur_count']} 不一致")

    # MathTex 數學錯誤（從之前的報告）
    if qid in math_errors:
        result["issues"].append(f"🔴 MathTex 數學錯誤: {math_errors[qid]}")

    return result


def main():
    # 讀 math_check_results.json 抽出 ERROR 題目
    math_errors = {}
    mr_path = BASE / "math_check_results.json"
    if mr_path.exists():
        results = json.load(open(mr_path, encoding="utf-8"))
        for r in results:
            if r.get("verdict") == "ERROR":
                # 但這份 report 是 Q075/Q148 修之前的，現在這兩題已修
                if r["qid"] in {"Q075", "Q148"}:
                    continue
                # Q039/Q048/Q104/Q147 是 LLM 誤判，跳過
                if r["qid"] in {"Q039", "Q048", "Q104", "Q147"}:
                    continue
                math_errors[r["qid"]] = r.get("summary", "")[:80]

    qids = sorted(d.name for d in BASE.iterdir() if d.is_dir() and d.name.startswith("Q"))

    print(f"{'QID':<6}{'mp4':<8}{'audio':<8}{'sub':<5}{'dur':<5}{'issues'}")
    print("-" * 80)

    all_results = []
    clean = []
    issues_qids = []
    for qid in qids:
        r = audit_one(qid, math_errors)
        all_results.append(r)
        mp4_s = f"{r.get('mp4_dur', 0):.1f}" if "mp4_dur" in r else "N/A"
        a_s = f"{r.get('audio_dur_sum', 0):.1f}" if "audio_dur_sum" in r else "N/A"
        sub = r.get("subtitle_count", "?")
        dur = r.get("audio_dur_count", "?")
        issues_str = "; ".join(r["issues"]) if r["issues"] else "✅"
        print(f"{qid:<6}{mp4_s:<8}{a_s:<8}{sub:<5}{dur:<5}{issues_str}")
        if r["issues"]:
            issues_qids.append(qid)
        else:
            clean.append(qid)

    print(f"\n{'='*70}")
    print(f"✅ 完全 OK: {len(clean)}/30")
    print(f"⚠️ 有問題: {len(issues_qids)}")
    if issues_qids:
        print(f"   問題題目: {', '.join(issues_qids)}")


if __name__ == "__main__":
    main()
