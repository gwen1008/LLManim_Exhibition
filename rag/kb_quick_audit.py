"""KB Quick Audit — pure retrieval diagnostics, NO LLM calls.

Use this to quantify a RAG collection's health BEFORE running the full
LLM-as-Judge audit (rag/retrieval_audit_50.py) or any 30-question A/B.

Per collection, reports:
  - Total object count (examples / rules, by source_library)
  - Per-knowledge_slug example coverage (how many slugs, count distribution)
  - For each test query: top-K hit, best_score, slug_match (retrieved.slug == expected.slug)
  - Aggregates: best_score distribution (min/p25/median/p75/max),
                below-relevance-threshold rate (best < 0.65),
                slug match rate (when expected_slug is known),
                cross-knowledge contamination rate

Usage:
  # Default: KB150_v2 against experiment_sample_30
  python rag/kb_quick_audit.py

  # Compare two collections side-by-side
  python rag/kb_quick_audit.py \\
      --collections ManimGoldenPair_KB150,ManimGoldenPair_KB150_v2 \\
      --sample evaluation/experiment_sample_30.json

  # Custom limit + knowledge_slug filter pass-through
  python rag/kb_quick_audit.py --limit 5 --with-slug

Output:
  - stdout summary table
  - rag/kb_quick_audit_<timestamp>.json   (full raw)
  - rag/kb_quick_audit_<timestamp>.md     (human readable)

Exit code: 0 if audit completes; non-zero only on connection failure.
"""
from __future__ import annotations

import argparse
import datetime
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import os

SAMPLE_DEFAULT = ROOT / "evaluation" / "experiment_sample_30.json"


def _connect():
    """Local-only connection; bypass the wrapper so we can switch collections
    per query without recreating the client."""
    import weaviate
    try:
        client = weaviate.connect_to_local(host="localhost", port=8080)
        if not client.is_live():
            print("❌ Weaviate not live on localhost:8080")
            sys.exit(2)
        return client
    except Exception as e:
        print(f"❌ Weaviate connect failed: {e}")
        sys.exit(2)


def _collection_inventory(client, name: str) -> dict:
    """Total objects per source_library + slug coverage."""
    from weaviate.classes.query import Filter
    coll = client.collections.get(name)
    inv = {"name": name, "total": 0, "by_source": {}, "by_slug_examples": {}}
    try:
        # Aggregate count via iterator (no aggregate API uniformly available)
        for obj in coll.iterator(return_properties=["source_library", "knowledge_slug"]):
            inv["total"] += 1
            src = obj.properties.get("source_library", "<none>")
            inv["by_source"][src] = inv["by_source"].get(src, 0) + 1
            if src == "examples":
                slug = obj.properties.get("knowledge_slug") or "<none>"
                inv["by_slug_examples"][slug] = inv["by_slug_examples"].get(slug, 0) + 1
    except Exception as e:
        inv["error"] = str(e)
    return inv


def _retrieve(client, collection_name: str, query: str, limit: int,
              knowledge_slug: str | None = None) -> list[dict]:
    """Direct hybrid retrieval — mirrors RAGRetriever.retrieve_examples but
    WITHOUT the RELEVANCE_THRESHOLD cutoff so we can see what would have hit."""
    from weaviate.classes.query import Filter, MetadataQuery
    coll = client.collections.get(collection_name)
    f = Filter.by_property("source_library").equal("examples")
    if knowledge_slug:
        f = f & Filter.by_property("knowledge_slug").equal(knowledge_slug)
    resp = coll.query.hybrid(
        query=query, limit=limit, alpha=0.5, filters=f,
        return_metadata=MetadataQuery(score=True),
    )
    return [{
        "score":     o.metadata.score,
        "slug":      o.properties.get("knowledge_slug"),
        "class":     o.properties.get("class_name"),
        "desc":      (o.properties.get("video_description") or "")[:80],
    } for o in resp.objects]


def audit_collection(client, name: str, sample: list[dict], limit: int,
                     pass_slug: bool) -> dict:
    print(f"\n🔍 auditing collection: {name}")
    inv = _collection_inventory(client, name)
    print(f"   inventory: total={inv['total']} by_source={inv['by_source']} "
          f"#slugs(examples)={len(inv.get('by_slug_examples', {}))}")

    rows = []
    for q in sample:
        qid = q["id"]
        query = q.get("topic") or q.get("question") or ""
        expected_slug = q.get("knowledge_slug")
        slug_for_filter = expected_slug if pass_slug else None
        try:
            hits = _retrieve(client, name, query, limit, slug_for_filter)
        except Exception as e:
            rows.append({"qid": qid, "error": str(e)})
            continue

        best = max((h["score"] for h in hits), default=0.0)
        top_slug = hits[0]["slug"] if hits else None
        slug_match = (expected_slug is not None
                      and top_slug is not None
                      and top_slug == expected_slug)
        rows.append({
            "qid": qid,
            "query":          query[:60],
            "expected_slug":  expected_slug,
            "n_hits":         len(hits),
            "best_score":     round(best, 3),
            "top_slug":       top_slug,
            "slug_match":     slug_match if expected_slug else None,
            "hits":           hits,
        })

    return {"name": name, "inventory": inv, "rows": rows}


def _summary(report: dict, relevance_threshold: float = 0.65) -> dict:
    rows = report["rows"]
    valid = [r for r in rows if "error" not in r]
    scores = [r["best_score"] for r in valid if r["best_score"] > 0]
    below = sum(1 for s in scores if s < relevance_threshold)

    matched = [r for r in valid if r["slug_match"] is True]
    mismatched = [r for r in valid if r["slug_match"] is False]
    no_label = [r for r in valid if r["slug_match"] is None]

    def _quant(xs):
        if not xs:
            return None
        xs = sorted(xs)
        n = len(xs)
        return {
            "n":      n,
            "min":    round(xs[0], 3),
            "p25":    round(xs[n // 4], 3),
            "median": round(statistics.median(xs), 3),
            "p75":    round(xs[(3 * n) // 4], 3),
            "max":    round(xs[-1], 3),
            "mean":   round(statistics.mean(xs), 3),
        }

    return {
        "name":               report["name"],
        "n_queries":          len(rows),
        "n_errors":           len(rows) - len(valid),
        "score_distribution": _quant(scores),
        "below_threshold":    {"count": below, "ratio": round(below / max(1, len(scores)), 3)},
        "slug_match": {
            "n_labeled":   len(matched) + len(mismatched),
            "n_matched":   len(matched),
            "n_mismatch":  len(mismatched),
            "match_rate":  (round(len(matched) / max(1, len(matched) + len(mismatched)), 3)
                            if (matched or mismatched) else None),
        },
        "n_no_slug_label":    len(no_label),
    }


def _print_summary(summary: dict):
    name = summary["name"]
    sd = summary["score_distribution"]
    sm = summary["slug_match"]
    bt = summary["below_threshold"]
    print(f"\n📊 [{name}] summary")
    print(f"   queries: {summary['n_queries']} ({summary['n_errors']} errors)")
    if sd:
        print(f"   best_score: min={sd['min']} p25={sd['p25']} median={sd['median']} "
              f"p75={sd['p75']} max={sd['max']} mean={sd['mean']}")
    print(f"   below relevance threshold (<0.65): "
          f"{bt['count']}/{sd['n'] if sd else 0} ({bt['ratio']*100:.1f}%)")
    if sm["n_labeled"]:
        print(f"   slug match: {sm['n_matched']}/{sm['n_labeled']} "
              f"({(sm['match_rate'] or 0)*100:.1f}%) — mismatch={sm['n_mismatch']}")
    else:
        print(f"   slug match: no expected_slug labels in sample (skipped)")


def _write_outputs(reports: list[dict], summaries: list[dict], out_dir: Path, stamp: str):
    json_path = out_dir / f"kb_quick_audit_{stamp}.json"
    md_path = out_dir / f"kb_quick_audit_{stamp}.md"
    json_path.write_text(json.dumps({
        "stamp":     stamp,
        "summaries": summaries,
        "reports":   reports,
    }, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    lines = [f"# KB Quick Audit — {stamp}\n"]
    for s in summaries:
        lines.append(f"## {s['name']}\n")
        sd = s.get("score_distribution") or {}
        sm = s.get("slug_match") or {}
        bt = s.get("below_threshold") or {}
        lines.append(f"- queries: {s['n_queries']} ({s['n_errors']} errors)")
        if sd:
            lines.append(f"- best_score: min={sd['min']} median={sd['median']} "
                         f"max={sd['max']} mean={sd['mean']}")
        lines.append(f"- below relevance threshold (<0.65): "
                     f"{bt.get('count',0)} ({bt.get('ratio',0)*100:.1f}%)")
        if sm.get("n_labeled"):
            lines.append(f"- slug match: {sm['n_matched']}/{sm['n_labeled']} "
                         f"({(sm['match_rate'] or 0)*100:.1f}%)")
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n💾 json: {json_path.relative_to(ROOT)}")
    print(f"📄 md:   {md_path.relative_to(ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collections",
                    default=os.getenv("RAG_COLLECTION", "ManimGoldenPair_KB150_v2"),
                    help="comma-separated collection names to audit")
    ap.add_argument("--sample", default=str(SAMPLE_DEFAULT))
    ap.add_argument("--limit", type=int, default=2,
                    help="top-K to retrieve (default 2, mirrors production)")
    ap.add_argument("--with-slug", action="store_true",
                    help="pass expected knowledge_slug as filter "
                         "(mirrors production W1.2 path)")
    ap.add_argument("--out-dir", default=str(ROOT / "rag"))
    args = ap.parse_args()

    sample_path = Path(args.sample)
    if not sample_path.exists():
        print(f"❌ sample not found: {sample_path}")
        sys.exit(1)
    sample = json.loads(sample_path.read_text(encoding="utf-8"))
    print(f"📋 sample: {len(sample)} queries from {sample_path.name}")

    collections = [c.strip() for c in args.collections.split(",") if c.strip()]
    client = _connect()
    try:
        reports = []
        summaries = []
        for c in collections:
            rep = audit_collection(client, c, sample, args.limit, args.with_slug)
            reports.append(rep)
            summ = _summary(rep)
            summaries.append(summ)
            _print_summary(summ)

        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        _write_outputs(reports, summaries, Path(args.out_dir), stamp)
    finally:
        client.close()


if __name__ == "__main__":
    main()
