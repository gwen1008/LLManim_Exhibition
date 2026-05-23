"""Quick retrieval audit: simulate what variant-C RAG would fetch for the 30-question sample.

Static audit (no LLM judge, no code generation) — just runs the same hybrid
search the production RAGRetriever would do, and tabulates:

  - Top-3 hits per question (class_name + score + cross-knowledge flag)
  - Hit rate: top-1 in the *correct* knowledge_slug for the question's KP?
  - Score distribution (best / median / threshold-skipped count)
  - With and without `knowledge_slug` filter (the filter is what main.py
    actually uses when Planner emits a slug)

Usage:
  python rag/audit_retrieval_30.py --collection ManimKB150v2_rules
  python rag/audit_retrieval_30.py --collection ManimGoldenPair_KB150_v2  # for B comparison
  python rag/audit_retrieval_30.py --collection both  # run both side by side

Output:
  rag/retrieval_audit_30_<collection>.csv
  rag/retrieval_audit_30_<collection>.md   (summary)
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parents[1]
SAMPLE = REPO / "evaluation" / "experiment_sample_30.json"

import sys
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from agents.core.knowledge_slug_map import KP_TO_SLUG  # noqa: E402


def query_collection(client, collection_name: str, query: str, slug: str | None,
                     limit: int = 3, alpha: float = 0.5):
    """Replicate the production retrieval call from rag_retriever.py."""
    from weaviate.classes.query import MetadataQuery, Filter
    col = client.collections.get(collection_name)
    _f = Filter.by_property("source_library").equal("examples")
    if slug:
        _f = _f & Filter.by_property("knowledge_slug").equal(slug)
    resp = col.query.hybrid(
        query=query, limit=limit, alpha=alpha, filters=_f,
        return_metadata=MetadataQuery(score=True),
    )
    out = []
    for obj in resp.objects:
        out.append({
            "class_name": obj.properties.get("class_name", "?"),
            "source_file": obj.properties.get("source_file", "?"),
            "knowledge_slug": obj.properties.get("knowledge_slug", "?"),
            "score": float(obj.metadata.score),
        })
    return out


def audit_one_collection(collection: str):
    import weaviate
    client = weaviate.connect_to_local()

    # Confirm collection exists
    existing = [c.name for c in client.collections.list_all().values()]
    if collection not in existing:
        client.close()
        raise SystemExit(f"❌ collection '{collection}' not found. Available: {existing}")

    cases = json.loads(SAMPLE.read_text(encoding="utf-8"))
    rows = []
    SCORE_THRESHOLD = 0.4
    RELEVANCE_THRESHOLD = 0.65  # production gate from rag_retriever.py

    for c in cases:
        qid = c["id"]
        kp_zh = c.get("knowledge_point", "")
        slug = KP_TO_SLUG.get(kp_zh)
        query = c.get("topic", "").split("\n")[0]

        # Two retrieval modes:
        with_filter = query_collection(client, collection, query, slug, limit=3)
        no_filter = query_collection(client, collection, query, None, limit=3)

        # Did the top hit (no filter) come from the right knowledge area?
        top1_slug_nf = no_filter[0]["knowledge_slug"] if no_filter else None
        cross_kp = bool(no_filter) and slug is not None and top1_slug_nf != slug

        # Production gating: would the result be injected?
        best_score_filt = max((h["score"] for h in with_filter), default=0.0)
        injected_filt = best_score_filt >= RELEVANCE_THRESHOLD

        rows.append({
            "qid": qid,
            "kp_zh": kp_zh,
            "slug": slug or "(none)",
            "topic": query[:60],
            "filt_top1_class": with_filter[0]["class_name"] if with_filter else "(none)",
            "filt_top1_score": f"{with_filter[0]['score']:.3f}" if with_filter else "—",
            "filt_top1_slug": with_filter[0]["knowledge_slug"] if with_filter else "—",
            "filt_n_above_thresh": sum(1 for h in with_filter if h["score"] >= SCORE_THRESHOLD),
            "filt_injected": injected_filt,
            "nofilt_top1_class": no_filter[0]["class_name"] if no_filter else "(none)",
            "nofilt_top1_score": f"{no_filter[0]['score']:.3f}" if no_filter else "—",
            "nofilt_top1_slug": no_filter[0]["knowledge_slug"] if no_filter else "—",
            "cross_kp": cross_kp,
        })

    client.close()
    return rows


def write_csv(rows: list[dict], path: Path):
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def write_md(rows: list[dict], collection: str, path: Path):
    n = len(rows)
    n_injected = sum(1 for r in rows if r["filt_injected"])
    n_cross_kp_nofilt = sum(1 for r in rows if r["cross_kp"])
    n_slug_match_nofilt = sum(1 for r in rows if not r["cross_kp"] and r["slug"] != "(none)")

    lines = [
        f"# Retrieval Audit: `{collection}` × 30 questions",
        "",
        "Simulates production RAG retrieval (same hybrid alpha, same gates) for each",
        "of the 30 sample questions. No code generation, no LLM judge — just measures",
        "*what the system would fetch* before Coder runs.",
        "",
        "## Summary",
        "",
        f"- **Cases**: {n}",
        f"- **Production-gated injection** (filt mode, best ≥ 0.65): **{n_injected} / {n}** ({n_injected/n*100:.0f}%)",
        f"- **No-filter top-1 matched correct slug**: **{n_slug_match_nofilt} / {n}** ({n_slug_match_nofilt/n*100:.0f}%)",
        f"- **No-filter top-1 cross-KP (wrong knowledge)**: {n_cross_kp_nofilt} / {n}",
        "",
        "**Interpretation**:",
        "- *Production-gated*: in real run, only hits ≥ 0.65 get fed to Coder; below = no example injected.",
        "- *Slug match*: did the embedding pick the right knowledge domain without help? Tests semantic quality.",
        "- *Cross-KP*: how often the top hit was from a different knowledge area (bad signal if high).",
        "",
        "## Per-Case (with `knowledge_slug` filter — production path)",
        "",
        "| QID | KP | Top-1 (class) | Score | Inject? |",
        "|---|---|---|---:|:---:|",
    ]
    for r in rows:
        inj = "✅" if r["filt_injected"] else "🚫"
        lines.append(
            f"| {r['qid']} | {r['kp_zh'][:8]} | {r['filt_top1_class'][:36]} | {r['filt_top1_score']} | {inj} |"
        )

    lines += ["", "## Per-Case (no filter — would Planner-less code pick the right domain?)", "",
              "| QID | KP | Top-1 (class) | Top-1 slug | Score | Cross-KP? |",
              "|---|---|---|---|---:|:---:|"]
    for r in rows:
        x = "❌" if r["cross_kp"] else "✓"
        lines.append(
            f"| {r['qid']} | {r['kp_zh'][:8]} | {r['nofilt_top1_class'][:36]} | {r['nofilt_top1_slug'][:24]} | {r['nofilt_top1_score']} | {x} |"
        )

    # By knowledge group
    by_kp = defaultdict(list)
    for r in rows:
        by_kp[r["kp_zh"]].append(r)
    lines += ["", "## By Knowledge Point", "",
              "| KP | n | Filt-injected | NoFilt slug-match | NoFilt best score (avg) |",
              "|---|---:|---:|---:|---:|"]
    for kp, group in sorted(by_kp.items()):
        gn = len(group)
        inj = sum(1 for r in group if r["filt_injected"])
        slug_ok = sum(1 for r in group if not r["cross_kp"] and r["slug"] != "(none)")
        avg_score = sum(float(r["nofilt_top1_score"]) for r in group if r["nofilt_top1_score"] != "—") / gn
        lines.append(f"| {kp} | {gn} | {inj}/{gn} | {slug_ok}/{gn} | {avg_score:.3f} |")

    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--collection", required=True,
                   help="Weaviate collection (e.g. ManimKB150v2_rules) or 'both' for B+C comparison")
    args = p.parse_args()

    if args.collection == "both":
        collections = ["ManimGoldenPair_KB150_v2", "ManimKB150v2_rules"]
    else:
        collections = [args.collection]

    for col in collections:
        print(f"\n🔍 Auditing collection: {col}")
        rows = audit_one_collection(col)
        csv_path = REPO / "rag" / f"retrieval_audit_30_{col}.csv"
        md_path = REPO / "rag" / f"retrieval_audit_30_{col}.md"
        write_csv(rows, csv_path)
        write_md(rows, col, md_path)
        print(f"  ✅ {csv_path.relative_to(REPO)}")
        print(f"  ✅ {md_path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
