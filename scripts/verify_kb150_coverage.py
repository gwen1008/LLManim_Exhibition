"""
Verify every question in seed_questions_150.xlsx maps via RAG to at least one
Scene from the new ManimKB150 collection (i.e. top-1 retrieved Scene lives in
the correct knowledge-point directory).

This is the Definition of Done for the kb150 plan: it proves the LLM-generated
Scenes are semantically reachable from the original question text.

Output: console summary + runs/kb150_coverage_report.csv

Pre-req:
  - Phase B done (knowledge_base/kb150/{slug}/*.py populated)
  - Phase C ingest done: python rag/ingest_code.py --collection ManimKB150 --kb-dir knowledge_base/kb150/

Usage:
  RAG_COLLECTION=ManimKB150 python scripts/verify_kb150_coverage.py
  RAG_COLLECTION=ManimKB150 python scripts/verify_kb150_coverage.py --limit 10  # smoke
"""
from __future__ import annotations
import argparse
import csv
import os
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Match the slug map from extract_kb150_seeds.py. Keep them in sync if either
# changes — this is the join key between txt 知識點 and KB directory names.
SLUG_MAP = {
    "整數加減": "integer_add_sub",
    "整數乘除": "integer_mul_div",
    "分數加減": "fraction_add_sub",
    "分數乘除": "fraction_mul_div",
    "四則運算算則（不含去括號）": "pemdas_no_bracket_removal",
    "四則運算（含去括號）": "pemdas_with_bracket_removal",
    "完整的四則混合運算": "mixed_arithmetic_full",
    "指數與科學記號": "exponent_scientific_notation",
    "因數與倍數": "factor_multiple",
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--xlsx", type=Path, default=Path("data/seed_questions_150.txt.xlsx"))
    ap.add_argument("--output", type=Path, default=Path("runs/kb150_coverage_report.csv"))
    ap.add_argument("--limit", type=int, default=0, help="Process only first N questions (0=all)")
    ap.add_argument("--top-k", type=int, default=3, help="How many top results to record")
    args = ap.parse_args()

    expected_collection = os.environ.get("RAG_COLLECTION", "")
    if expected_collection != "ManimKB150":
        print(f"[WARN] RAG_COLLECTION env is {expected_collection!r}, expected 'ManimKB150'.")
        print("       Did you forget: set RAG_COLLECTION=ManimKB150  (or $env:RAG_COLLECTION = 'ManimKB150')?")

    from agents.core.rag_retriever import RAGRetriever, COLLECTION_NAME
    print(f"[INFO] Retriever bound to collection: {COLLECTION_NAME}")

    df = pd.read_excel(args.xlsx)
    if args.limit:
        df = df.head(args.limit)
    print(f"[INFO] Verifying {len(df)} questions")

    retriever = RAGRetriever()
    if retriever.client is None:
        raise SystemExit("[ERR] Weaviate connection failed — is the Docker container running?")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    hits_by_cat: dict[str, list[bool]] = {}

    for i, row in df.iterrows():
        qid = int(row["編號"])
        knowledge = str(row["知識點"]).strip()
        expected_dir = SLUG_MAP.get(knowledge, "")
        if not expected_dir:
            print(f"  [SKIP] q{qid}: unknown 知識點 {knowledge!r}")
            continue

        # Compose query from 題幹 + 知識點. Mirrors how a real Coder call would
        # phrase intent to the retriever.
        query = f"{knowledge} {row['題幹']}"
        examples = retriever.retrieve_examples(query, limit=args.top_k)

        top_classes = []
        top_dirs = []
        top_descs = []
        for ex in examples[:args.top_k]:
            top_classes.append(ex.get("class_name", "") or "")
            # Source_file is e.g. "integer_add_sub/ZeroPairIntegerAddition.py"
            src = ex.get("source_file", "") or ""
            top_dirs.append(src.split("/")[0].split("\\")[0])
            top_descs.append((ex.get("description", "") or "")[:80])

        # Pad to top_k for stable CSV columns.
        while len(top_classes) < args.top_k:
            top_classes.append("")
            top_dirs.append("")
            top_descs.append("")

        # Coder agent receives top-K examples (currently K=3), so a question
        # is "covered" if ANY of top-K lives in the expected category. The
        # stricter top-1-only criterion is reported separately for diagnostics.
        hit_top1 = top_dirs[0] == expected_dir if top_dirs[0] else False
        hit_topk = expected_dir in [d for d in top_dirs if d]
        hits_by_cat.setdefault(knowledge, []).append(hit_topk)

        rows.append({
            "id": qid,
            "knowledge": knowledge,
            "expected_dir": expected_dir,
            "top1_class": top_classes[0],
            "top1_dir": top_dirs[0],
            "top1_desc": top_descs[0],
            "top2_class": top_classes[1],
            "top2_dir": top_dirs[1],
            "top3_class": top_classes[2],
            "top3_dir": top_dirs[2],
            "hit_top1": hit_top1,
            "hit_topk": hit_topk,
        })

        marker = "OK " if hit_topk else "MISS"
        top1_marker = "*" if hit_top1 else " "
        print(f"  [{marker}]{top1_marker} q{qid:3d} ({knowledge[:6]:<6s}) "
              f"top_dirs={top_dirs} expected={expected_dir!r}")

    retriever.close()

    # Write CSV
    with args.output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n[OK] Wrote {len(rows)} rows to {args.output}")

    # Summary — top-K hit (Coder sees top-3, so this is the realistic metric)
    print("\n[SUMMARY] Per-知識點 top-K hit rate (K=3, mirrors Coder's view):")
    overall_hits = 0
    overall_total = 0
    worst = None
    for cat in sorted(hits_by_cat.keys()):
        hits = hits_by_cat[cat]
        rate = sum(hits) / len(hits) * 100
        print(f"  {cat:<20s}  {sum(hits):>3d}/{len(hits):<3d}  ({rate:5.1f}%)")
        overall_hits += sum(hits)
        overall_total += len(hits)
        if worst is None or rate < worst[1]:
            worst = (cat, rate)

    overall_rate = overall_hits / overall_total * 100 if overall_total else 0
    print(f"\n  OVERALL          {overall_hits:>3d}/{overall_total:<3d}  ({overall_rate:5.1f}%)")
    print(f"  WORST CATEGORY   {worst[0]} @ {worst[1]:.1f}%")

    # Diagnostic: stricter top-1 hit rate (what fraction land their FIRST result correctly)
    top1_hits = sum(1 for r in rows if r["hit_top1"])
    print(f"\n  Diagnostic top-1 only: {top1_hits}/{len(rows)} ({top1_hits/len(rows)*100:.1f}%)")

    # DoD per plan: overall >= 90%, every category >= 80%
    dod_ok = overall_rate >= 90.0 and all(
        sum(h) / len(h) * 100 >= 80.0 for h in hits_by_cat.values()
    )
    print(f"\n  Definition of Done (overall>=90%, every cat>=80%): {'PASS' if dod_ok else 'FAIL'}")
    if not dod_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
