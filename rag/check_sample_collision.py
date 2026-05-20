"""Check experiment_sample_30.json for RAG collision.

For each of the 30 sample questions, query RAG and compute string similarity
between the top-1 retrieved example code and the question's expected solution.

If similarity > THRESHOLD, the question is at risk of being "open-book" for the
B group (optimized RAG) — i.e., RAG would essentially hand back the answer code,
contaminating the three-way comparison.

Read-only. Outputs a CSV report only.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from difflib import SequenceMatcher
from pathlib import Path

# Allow running from repo root: python rag/check_sample_collision.py
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from agents.core.rag_retriever import RAGRetriever  # noqa: E402


SIMILARITY_THRESHOLD = 0.70

# [W1.2] Map experiment JSON's Chinese knowledge_point → kb150 directory slug.
KNOWLEDGE_POINT_TO_SLUG = {
    "整數加減": "integer_add_sub",
    "整數乘除": "integer_mul_div",
    "分數加減": "fraction_add_sub",
    "分數乘除": "fraction_mul_div",
    "四則運算算則（不含去括號）": "pemdas_no_bracket_removal",
    "四則運算（含去括號）": "pemdas_with_bracket_removal",
    "完整的四則混合運算": "mixed_arithmetic_full",
    "因數與倍數": "factor_multiple",
    "指數與科學記號": "exponent_scientific_notation",
}


def code_similarity(a: str, b: str) -> float:
    """Normalized SequenceMatcher ratio on whitespace-collapsed code."""
    if not a or not b:
        return 0.0
    norm_a = " ".join(a.split())
    norm_b = " ".join(b.split())
    return SequenceMatcher(None, norm_a, norm_b).ratio()


def query_for_case(case: dict) -> str:
    """Build a retrieval query mirroring how main.py phrases it."""
    topic = case.get("topic", "")
    return topic.split("\n")[0][:200]


def slug_for_case(case: dict) -> str:
    """Resolve a case's knowledge_point (CN) to its kb150 directory slug."""
    return KNOWLEDGE_POINT_TO_SLUG.get(case.get("knowledge_point", ""), "")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sample",
        default=str(REPO_ROOT / "evaluation" / "experiment_sample_30.json"),
    )
    parser.add_argument(
        "--out",
        default=str(REPO_ROOT / "evaluation" / "sample_collision_report.csv"),
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=SIMILARITY_THRESHOLD,
        help="Similarity threshold above which a case is flagged as collision risk",
    )
    parser.add_argument(
        "--use-slug-filter",
        action="store_true",
        help="Pass each case's knowledge_slug to retrieve_examples() to test W1.2 filter",
    )
    args = parser.parse_args()

    with open(args.sample, encoding="utf-8") as f:
        cases = json.load(f)

    print(f"Loaded {len(cases)} cases from {args.sample}")
    print(f"RAG collection (env RAG_COLLECTION): {os.environ.get('RAG_COLLECTION', 'ManimGoldenPair')}")

    retriever = RAGRetriever()
    if retriever.client is None:
        print("❌ Weaviate not reachable. Aborting.")
        return 1

    rows = []
    flagged = []
    try:
        for case in cases:
            cid = case["id"]
            query = query_for_case(case)
            solution = case.get("solution", "") or ""
            slug = slug_for_case(case) if args.use_slug_filter else None
            print(f"\n--- {cid} ---  query: {query[:60]}" + (f" [slug={slug}]" if slug else ""))
            examples = retriever.retrieve_examples(query, limit=1, knowledge_slug=slug)
            if not examples:
                rows.append({
                    "case_id": cid,
                    "knowledge_point": case.get("knowledge_point", ""),
                    "difficulty": case.get("difficulty", ""),
                    "top1_score": "",
                    "top1_source": "",
                    "top1_desc": "",
                    "sim_vs_solution": "",
                    "flagged": "no_hit",
                })
                continue
            top1 = examples[0]
            sim = code_similarity(top1.get("code", ""), solution)
            flag = "COLLISION" if sim > args.threshold else ""
            if flag:
                flagged.append(cid)
            rows.append({
                "case_id": cid,
                "knowledge_point": case.get("knowledge_point", ""),
                "difficulty": case.get("difficulty", ""),
                "top1_score": f"{top1.get('score', 0):.3f}",
                "top1_source": top1.get("source_file", ""),
                "top1_desc": top1.get("description", "")[:80],
                "sim_vs_solution": f"{sim:.3f}",
                "flagged": flag,
            })
    finally:
        retriever.close()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Wrote: {out_path}")
    print(f"Total: {len(rows)}  Flagged (sim > {args.threshold}): {len(flagged)}")
    if flagged:
        print(f"Flagged case IDs: {', '.join(flagged)}")
        print("→ Consider swapping these in evaluation/experiment_sample_30.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
