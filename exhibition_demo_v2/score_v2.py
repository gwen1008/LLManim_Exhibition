"""
Score all 20 v2 exhibition videos with FinalJudge.

Reads:
  exhibition_demo_v2/arm_A_system/Q*/{video.mp4, code.py}
  exhibition_demo_v2/arm_B_naked_opus/Q*/{scene.mp4, scene.py}

Writes (checkpoint after each judgment):
  exhibition_demo_v2/fj_scores.json
"""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from agents.core.llm_client import LLMClient
from agents.utils.final_judge import FinalJudge


def load_topics():
    return json.loads((ROOT / "exhibition_demo" / "topics.json").read_text(encoding="utf-8"))["topics"]


def find_video_and_code(arm_dir: Path, qid: str, arm: str):
    qdir = arm_dir / qid
    if arm == "system":
        return qdir / "video.mp4", qdir / "code.py"
    else:
        return qdir / "scene.mp4", qdir / "scene.py"


def main():
    topics = {t["id"]: t for t in load_topics()}
    out_path = ROOT / "exhibition_demo_v2" / "fj_scores.json"
    results = json.loads(out_path.read_text()) if out_path.exists() else {}

    llm = LLMClient()
    fj = FinalJudge(llm_client=llm)

    arms = {
        "system":     ROOT / "exhibition_demo_v2" / "arm_A_system",
        "naked_opus": ROOT / "exhibition_demo_v2" / "arm_B_naked_opus",
    }

    qids = sorted(topics.keys())
    total = len(qids) * len(arms)
    done = 0
    t_start = time.time()

    for qid in qids:
        topic_en = topics[qid]["en"]
        results.setdefault(qid, {})

        for arm_name, arm_dir in arms.items():
            done += 1
            if arm_name in results[qid] and results[qid][arm_name].get("weighted_total") is not None:
                print(f"[{done}/{total}] {qid} / {arm_name}  — cached, skip")
                continue

            video, code_file = find_video_and_code(arm_dir, qid, "system" if arm_name == "system" else "naked")
            if not video.exists():
                print(f"[{done}/{total}] {qid} / {arm_name}  — no video (render failed)")
                results[qid][arm_name] = {"weighted_total": None, "verdict": "NO_VIDEO"}
                out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
                continue

            code = code_file.read_text(encoding="utf-8", errors="replace") if code_file.exists() else ""
            print(f"\n[{done}/{total}] {qid} / {arm_name}  — judging {video.name} ({len(code)} chars code)")
            t0 = time.time()
            try:
                r = fj.judge(str(video), topic_en, code)
                elapsed = time.time() - t0
                results[qid][arm_name] = {
                    "weighted_total": r.get("weighted_total"),
                    "verdict": r.get("verdict"),
                    "scores": r.get("scores", {}),
                    "code_issues_count": len(r.get("code_issues", [])),
                    "elapsed_sec": round(elapsed, 1),
                }
                print(f"  → score={r.get('weighted_total')} verdict={r.get('verdict')} ({elapsed:.1f}s)")
            except Exception as e:
                results[qid][arm_name] = {"weighted_total": None, "verdict": "ERROR", "error": str(e)[:300]}
                print(f"  ✗ ERROR: {e}")

            out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))

    print(f"\n=== Done in {time.time() - t_start:.1f}s. Results in {out_path} ===")


if __name__ == "__main__":
    main()
