"""
Parse seed_questions_150.xlsx -> group by 知識點 -> emit seed JSONs for Phase B.

Each seed JSON carries the raw teaching material (題幹 + 詳解 + 引導策略)
that the LLM in Phase B will condense into a Manim Scene.

Selection rule (deliberately code, not hard-coded ids, so it survives source
updates): per 知識點, sort by 難度 desc, then 編號 asc, take top N (default 3).
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import pandas as pd

import sys
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from agents.core.knowledge_slug_map import KP_TO_SLUG as SLUG_MAP  # noqa: E402

REQUIRED_COLUMNS = ["編號", "題幹", "知識點", "難度", "詳解", "引導策略"]


def load_xlsx(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit(f"[ERR] xlsx missing required columns: {missing}\n   actual: {list(df.columns)}")
    return df


def normalize_row(row: pd.Series) -> dict:
    """Coerce row to typed dict; treat NaN as empty string."""
    def _s(v) -> str:
        if pd.isna(v):
            return ""
        return str(v).strip()

    try:
        qid = int(row["編號"])
    except (ValueError, TypeError):
        qid = -1
    try:
        difficulty = int(row["難度"])
    except (ValueError, TypeError):
        difficulty = 0

    knowledge = _s(row["知識點"])
    return {
        "id": qid,
        "knowledge": knowledge,
        "knowledge_slug": SLUG_MAP.get(knowledge, ""),
        "difficulty": difficulty,
        "question": _s(row["題幹"]),
        "answer": _s(row.get("正確答案", "")),
        "explanation": _s(row["詳解"]),
        "guidance": _s(row["引導策略"]),
    }


def select_seeds(normalized: list[dict], per_category: int) -> dict[str, list[dict]]:
    by_cat: dict[str, list[dict]] = {}
    for q in normalized:
        by_cat.setdefault(q["knowledge"], []).append(q)
    seeds = {}
    for cat, items in by_cat.items():
        items.sort(key=lambda x: (-x["difficulty"], x["id"]))
        seeds[cat] = items[:per_category]
    return seeds


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--input", type=Path, default=Path("data/seed_questions_150.txt.xlsx"),
        help="Path to the source xlsx (12 columns, 159 rows expected).",
    )
    ap.add_argument(
        "--out-dir", type=Path, default=Path("knowledge_base/kb150_seeds"),
        help="Directory for seed JSON output.",
    )
    ap.add_argument(
        "--per-category", type=int, default=3,
        help="How many seed questions to take per 知識點.",
    )
    ap.add_argument(
        "--extra-ids", default="",
        help="Comma-separated question ids to ALWAYS include, on top of per-category "
             "selection (e.g. --extra-ids 38,98 for plugging known coverage gaps).",
    )
    args = ap.parse_args()

    if not args.input.exists():
        raise SystemExit(f"[ERR] Input not found: {args.input}")

    df = load_xlsx(args.input)
    normalized = [normalize_row(df.iloc[i]) for i in range(len(df))]
    print(f"[OK] Parsed {len(normalized)} rows from {args.input}")

    unmapped = sorted({q["knowledge"] for q in normalized if not q["knowledge_slug"]})
    if unmapped:
        print(f"[ERR] {len(unmapped)} 知識點 not in SLUG_MAP -- add them and re-run:")
        for k in unmapped:
            print(f"      {k!r}")
        raise SystemExit(1)

    seeds = select_seeds(normalized, args.per_category)

    # Plug in --extra-ids (always include, regardless of difficulty sort).
    extra_ids = {int(x) for x in args.extra_ids.split(",") if x.strip()}
    if extra_ids:
        by_id = {q["id"]: q for q in normalized}
        for eid in extra_ids:
            q = by_id.get(eid)
            if q is None:
                print(f"[WARN] --extra-ids {eid} not found in source, skipping")
                continue
            existing_ids = {s["id"] for s in seeds[q["knowledge"]]}
            if eid not in existing_ids:
                seeds[q["knowledge"]].append(q)
                print(f"[ADD] extra seed id={eid} -> {q['knowledge']}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    total_written = 0
    print("\n📊 Per-category selection (sorted by difficulty desc, id asc):")
    for cat in sorted(seeds.keys()):
        cat_items = seeds[cat]
        total_in_source = sum(1 for q in normalized if q["knowledge"] == cat)
        ids = [q["id"] for q in cat_items]
        diffs = [q["difficulty"] for q in cat_items]
        print(f"   {cat:<20s}  picked {len(cat_items)} / {total_in_source:>3d}"
              f"  ids={ids}  diff={diffs}")
        for seed in cat_items:
            slug = seed["knowledge_slug"]
            fname = args.out_dir / f"{slug}_{seed['id']:03d}.json"
            fname.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding="utf-8")
            total_written += 1

    print(f"\n[OK] Wrote {total_written} seed JSONs to {args.out_dir}")


if __name__ == "__main__":
    main()
