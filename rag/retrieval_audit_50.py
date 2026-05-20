"""
RAG Retrieval Audit (LLM-as-Judge) — Q1-Q50 across A (Old) vs B (KB150).

實驗目的：純測 retrieval 命中率，不跑 Coder/Render。
- 每題分別從 ManimGoldenPair_Old / ManimGoldenPair_KB150 各撈 2 個 example (limit=2)。
- 4 個範例 shuffle 後盲測丟給 Claude Opus (subscription) 評 1-5 分。
- 統計 A vs B 的 top-1 / top-2 平均分、winner 分布、按知識點分群。

跟 production retrieval 設定一致：limit=2、用 test_cases JSON 的 topic 中文題幹當 query。
"""

from __future__ import annotations

import csv
import importlib
import io
import json
import os
import random
import statistics
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                              errors="replace", line_buffering=True)

from agents.core.llm_client import LLMClient, LLMError  # noqa: E402
import agents.core.rag_retriever as rr_mod  # noqa: E402


# ─── Config ────────────────────────────────────────────────────────────────

REPO = Path(__file__).parent.parent
TEST_FILES = [
    REPO / "evaluation" / "test_cases_q20_xlsx.json",      # Q01-Q20
    REPO / "evaluation" / "test_cases_q21_q100.json",      # Q021-Q050 (取前 30)
]

COLLECTIONS = {
    "A": "ManimGoldenPair_Old",
    "B": "ManimGoldenPair_KB150",
}

LIMIT = 2  # 跟 production 一致
SEED = 42  # shuffle 確定性
RATE_DELAY = 0.5  # 每題之間 sleep，避 Claude CLI throttle

OUT_CSV = REPO / "rag" / "retrieval_audit_50.csv"
OUT_JSON = REPO / "rag" / "retrieval_audit_50_summary.json"


# ─── Judge prompts ─────────────────────────────────────────────────────────

JUDGE_SYSTEM = """You are an expert evaluating retrieval quality for a Manim math animation generator.

Given a math problem (Chinese, junior-high level) and 4 candidate Manim code examples,
rate EACH candidate 1-5 on how useful it is as reference for the Coder LLM that needs
to write a Manim animation for this specific problem.

Scoring scale:
5 = Perfect match. Same problem type & operation. Coder can adapt structure directly.
4 = Strong match. Same knowledge domain (e.g. both integer arithmetic). Patterns reusable.
3 = Partial match. Related concept but different operation (e.g. multiplication vs addition).
2 = Weak match. Some shared elements (uses MathTex) but topic mostly unrelated.
1 = Irrelevant. Completely different topic (e.g. geometry example for arithmetic problem).

Focus on: math topic match, visual strategy applicability.
Do NOT score based on: code style, length, formatting.

Output ONLY a JSON object, no markdown fence, no prose:
{"scores": {"E1": <int>, "E2": <int>, "E3": <int>, "E4": <int>},
 "best": "E?",
 "rationale": "<1-2 sentences explaining your top pick>"}
"""


def build_user_prompt(topic: str, kp: str, candidates: list[dict]) -> str:
    """candidates: list of {'label': 'E1', 'description': '...'}"""
    cand_block = "\n".join(
        f"[{c['label']}] {c['description']}"
        for c in candidates
    )
    return f"""Problem: {topic}
Knowledge Point: {kp}

Candidates (described by their video_description field):
{cand_block}

Rate each candidate 1-5 per the scoring scale. Output JSON only."""


# ─── Load test cases ───────────────────────────────────────────────────────

def load_cases() -> list[dict]:
    """Load Q01-Q20 + Q021-Q050 = 50 cases."""
    all_cases = []
    for f in TEST_FILES:
        with open(f, encoding="utf-8") as fh:
            all_cases.extend(json.load(fh))

    # Q01-Q20 (q20_xlsx) and Q021-Q050 (q21_q100 first 30)
    target_ids = {f"Q{i:02d}" for i in range(1, 21)} | {f"Q{i:03d}" for i in range(21, 51)}
    cases = [c for c in all_cases if c["id"] in target_ids]
    assert len(cases) == 50, f"Expected 50 cases, got {len(cases)}: {[c['id'] for c in cases]}"
    cases.sort(key=lambda c: (len(c["id"]), c["id"]))
    return cases


# ─── Retrieval (切 collection) ─────────────────────────────────────────────

def retrieve_for(collection: str, query: str, limit: int = LIMIT) -> list[dict]:
    """Switch RAG_COLLECTION via env + reload module so module-level COLLECTION_NAME re-reads."""
    os.environ["RAG_COLLECTION"] = collection
    importlib.reload(rr_mod)
    rag = rr_mod.RAGRetriever()
    try:
        results = rag.retrieve_examples(query, limit=limit)
    finally:
        rag.close()
    return results


# ─── Judge ─────────────────────────────────────────────────────────────────

def parse_judge_output(raw: str) -> dict | None:
    """Best-effort JSON extraction from LLM output."""
    raw = raw.strip()
    # strip code fence if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw
        if raw.endswith("```"):
            raw = raw.rsplit("```", 1)[0]
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start < 0 or end <= start:
        return None
    try:
        return json.loads(raw[start:end])
    except json.JSONDecodeError:
        return None


def judge_case(llm: LLMClient, topic: str, kp: str, candidates: list[dict]) -> dict | None:
    user = build_user_prompt(topic, kp, candidates)
    try:
        raw = llm._call_claude_code(JUDGE_SYSTEM, user)
    except (LLMError, Exception) as e:
        print(f"  ⚠️  Judge call failed: {e}")
        return None
    return parse_judge_output(raw)


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    random.seed(SEED)
    cases = load_cases()
    print(f"Loaded {len(cases)} cases (Q01-Q020 + Q021-Q050).\n")

    llm = LLMClient()

    rows = []  # csv rows
    raw_results = []  # for json dump

    for idx, case in enumerate(cases, 1):
        cid = case["id"]
        topic = case["topic"]
        kp = case.get("knowledge_point", "?")

        print(f"[{idx:>2}/{len(cases)}] {cid} ({kp})")

        # 撈兩組
        try:
            res_A = retrieve_for(COLLECTIONS["A"], topic)
            res_B = retrieve_for(COLLECTIONS["B"], topic)
        except Exception as e:
            print(f"  ❌ Retrieve failed: {e}")
            continue

        # 建 candidates 並 shuffle
        # 每筆: {'source': 'A_top1'/'A_top2'/'B_top1'/'B_top2', 'description': ..., 'score': ...}
        candidates = []
        for rank, r in enumerate(res_A[:2]):
            candidates.append({
                "source": f"A_top{rank+1}",
                "description": r.get("description", "(no description)"),
                "rag_score": r.get("score", 0.0),
            })
        for rank, r in enumerate(res_B[:2]):
            candidates.append({
                "source": f"B_top{rank+1}",
                "description": r.get("description", "(no description)"),
                "rag_score": r.get("score", 0.0),
            })

        # 不足 4 個 (某 collection 撈不到 2 個)，跳過 judge 但記錄
        if len(candidates) < 2:
            print(f"  ⚠️  撈到太少範例 ({len(candidates)})，跳過")
            continue

        # 打亂 + 重新貼 E1-E4 標籤
        random.shuffle(candidates)
        for i, c in enumerate(candidates):
            c["label"] = f"E{i+1}"

        # judge
        judge_out = judge_case(llm, topic, kp, candidates)
        if judge_out is None or "scores" not in judge_out:
            print(f"  ⚠️  judge 失敗或格式錯，跳過")
            continue

        # 把 E1-E4 score 對回原始 source
        per_source_score = {}
        for c in candidates:
            s = judge_out["scores"].get(c["label"])
            if s is not None:
                per_source_score[c["source"]] = int(s)

        # 整理本題結果
        row = {
            "case_id": cid,
            "knowledge_point": kp,
            "difficulty": case.get("difficulty", ""),
            "A_top1_score": per_source_score.get("A_top1", ""),
            "A_top2_score": per_source_score.get("A_top2", ""),
            "B_top1_score": per_source_score.get("B_top1", ""),
            "B_top2_score": per_source_score.get("B_top2", ""),
            "best_label": judge_out.get("best", ""),
            "best_source": next((c["source"] for c in candidates if c["label"] == judge_out.get("best", "")), ""),
            "rationale": judge_out.get("rationale", ""),
        }
        rows.append(row)

        raw_results.append({
            "case_id": cid,
            "knowledge_point": kp,
            "topic": topic,
            "candidates": [
                {"source": c["source"], "label": c["label"],
                 "description": c["description"], "rag_score": c["rag_score"]}
                for c in candidates
            ],
            "judge_scores": judge_out.get("scores", {}),
            "judge_best": judge_out.get("best", ""),
            "judge_rationale": judge_out.get("rationale", ""),
            "per_source_score": per_source_score,
        })

        # quick log
        a1 = per_source_score.get("A_top1", "?")
        a2 = per_source_score.get("A_top2", "?")
        b1 = per_source_score.get("B_top1", "?")
        b2 = per_source_score.get("B_top2", "?")
        print(f"  A: top1={a1} top2={a2}  |  B: top1={b1} top2={b2}  |  best={row['best_source']}")

        time.sleep(RATE_DELAY)

    # ── 寫 CSV ──
    OUT_CSV.parent.mkdir(exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n✅ CSV: {OUT_CSV} ({len(rows)} rows)")

    # ── 統計 ──
    print("\n" + "=" * 80)
    print(f"📊 Retrieval Audit Summary ({len(rows)} 題)")
    print("=" * 80)

    def avg(vals): return statistics.mean(vals) if vals else 0
    def med(vals): return statistics.median(vals) if vals else 0

    a_t1 = [r["A_top1_score"] for r in rows if isinstance(r["A_top1_score"], int)]
    a_t2 = [r["A_top2_score"] for r in rows if isinstance(r["A_top2_score"], int)]
    b_t1 = [r["B_top1_score"] for r in rows if isinstance(r["B_top1_score"], int)]
    b_t2 = [r["B_top2_score"] for r in rows if isinstance(r["B_top2_score"], int)]
    a_t12 = [(r["A_top1_score"] + r["A_top2_score"]) / 2 for r in rows
             if isinstance(r["A_top1_score"], int) and isinstance(r["A_top2_score"], int)]
    b_t12 = [(r["B_top1_score"] + r["B_top2_score"]) / 2 for r in rows
             if isinstance(r["B_top1_score"], int) and isinstance(r["B_top2_score"], int)]

    print(f"\n{'指標':<28}{'A (Old)':<14}{'B (KB150)':<14}{'Δ':<10}")
    print("-" * 70)
    print(f"{'Top-1 mean':<28}{avg(a_t1):<14.2f}{avg(b_t1):<14.2f}{avg(b_t1)-avg(a_t1):<+10.2f}")
    print(f"{'Top-1 median':<28}{med(a_t1):<14.1f}{med(b_t1):<14.1f}")
    print(f"{'Top-2 mean':<28}{avg(a_t2):<14.2f}{avg(b_t2):<14.2f}{avg(b_t2)-avg(a_t2):<+10.2f}")
    print(f"{'Top-1+Top-2 avg':<28}{avg(a_t12):<14.2f}{avg(b_t12):<14.2f}{avg(b_t12)-avg(a_t12):<+10.2f}")

    a_perf = sum(1 for s in a_t1 if s == 5)
    b_perf = sum(1 for s in b_t1 if s == 5)
    a_bad = sum(1 for s in a_t1 if s <= 2)
    b_bad = sum(1 for s in b_t1 if s <= 2)
    print(f"\n{'Top-1=5 (完美對題)':<28}{a_perf}/{len(a_t1)} ({a_perf*100/len(a_t1):.0f}%)"
          f"{'':<3}{b_perf}/{len(b_t1)} ({b_perf*100/len(b_t1):.0f}%)")
    print(f"{'Top-1≤2 (不相關)':<28}{a_bad}/{len(a_t1)} ({a_bad*100/len(a_t1):.0f}%)"
          f"{'':<3}{b_bad}/{len(b_t1)} ({b_bad*100/len(b_t1):.0f}%)")

    # Winner（A top-1 vs B top-1）
    a_win = b_win = tie = 0
    for r in rows:
        if not (isinstance(r["A_top1_score"], int) and isinstance(r["B_top1_score"], int)):
            continue
        if r["A_top1_score"] > r["B_top1_score"]: a_win += 1
        elif r["A_top1_score"] < r["B_top1_score"]: b_win += 1
        else: tie += 1
    print(f"\n{'Winner (Top-1 對比)':<28}A 贏 {a_win}{' '*3}B 贏 {b_win}{' '*3}平手 {tie}")

    # judge_best 來源分布
    best_src_dist = {"A_top1": 0, "A_top2": 0, "B_top1": 0, "B_top2": 0}
    for r in rows:
        s = r["best_source"]
        if s in best_src_dist: best_src_dist[s] += 1
    print(f"\nJudge 認定 best 來源分布: {best_src_dist}")
    a_best = best_src_dist["A_top1"] + best_src_dist["A_top2"]
    b_best = best_src_dist["B_top1"] + best_src_dist["B_top2"]
    print(f"  A 組總 best: {a_best}/{len(rows)} | B 組總 best: {b_best}/{len(rows)}")

    # 按知識點
    print("\n" + "-" * 70)
    print("📚 按知識點分群（Top-1 mean）")
    print("-" * 70)
    print(f"{'KP':<24}{'n':<4}{'A T1':<10}{'B T1':<10}{'Δ':<10}{'判定':<10}")
    kp_groups = {}
    for r in rows:
        kp_groups.setdefault(r["knowledge_point"], []).append(r)
    for kp, group in sorted(kp_groups.items(), key=lambda x: -len(x[1])):
        a_kp = [g["A_top1_score"] for g in group if isinstance(g["A_top1_score"], int)]
        b_kp = [g["B_top1_score"] for g in group if isinstance(g["B_top1_score"], int)]
        if not (a_kp and b_kp): continue
        am, bm = avg(a_kp), avg(b_kp)
        delta = bm - am
        verdict = "✅ B 贏" if delta > 0.3 else ("❌ B 輸" if delta < -0.3 else "🟰 持平")
        print(f"{kp:<24}{len(group):<4}{am:<10.2f}{bm:<10.2f}{delta:<+10.2f}{verdict:<10}")

    # ── 寫 JSON ──
    summary = {
        "n_cases": len(rows),
        "config": {"limit": LIMIT, "seed": SEED, "collections": COLLECTIONS},
        "aggregates": {
            "A_top1_mean": avg(a_t1), "A_top1_median": med(a_t1),
            "B_top1_mean": avg(b_t1), "B_top1_median": med(b_t1),
            "A_top2_mean": avg(a_t2), "B_top2_mean": avg(b_t2),
            "A_top1_perfect": a_perf, "B_top1_perfect": b_perf,
            "A_top1_irrelevant": a_bad, "B_top1_irrelevant": b_bad,
            "winner_A": a_win, "winner_B": b_win, "tie": tie,
            "best_source_distribution": best_src_dist,
        },
        "per_case": raw_results,
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\n✅ JSON: {OUT_JSON}")
    print(f"✅ 完成 ({len(rows)}/{len(cases)} 題)")


if __name__ == "__main__":
    main()
