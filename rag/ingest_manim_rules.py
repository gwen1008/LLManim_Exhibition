"""
Manim Skill Rules Ingestion Pipeline
=====================================
從 adithya-s-k/manim_skill 的 rules/*.md 抓取 Manim CE best practices
並 ingest 進 Weaviate ManimGoldenPair collection。

用法:
    python rag/ingest_manim_rules.py
    python rag/ingest_manim_rules.py --dry-run   # 只 fetch，不寫 Weaviate
    python rag/ingest_manim_rules.py --save-local # 同時存到 knowledge_base/manim_ce_rules/
"""

import argparse
import re
import sys
from pathlib import Path

import httpx
import weaviate

# ── 來源設定 ──────────────────────────────────────────────────────────────────
RULES = [
    "3d", "animation-groups", "animations", "axes", "camera",
    # "cli" removed: pure bash CLI flags, not Python API, noise for code generation
    "colors", "config", "creation-animations", "graphing", "grouping",
    "latex", "lines", "mobjects", "positioning", "scenes", "shapes",
    "styling", "text-animations", "text", "timing", "transform-animations",
    "updaters",
]

RAW_BASE = (
    "https://raw.githubusercontent.com/adithya-s-k/manim_skill/main"
    "/skills/manimce-best-practices/rules"
)

LOCAL_CACHE_DIR = Path("knowledge_base/manim_ce_rules")


# ── Fetch ─────────────────────────────────────────────────────────────────────

def fetch_rules(save_local: bool = False, from_local: bool = False) -> list[dict]:
    """Fetch all rule markdown files and return list of dicts ready for Weaviate."""
    chunks = []

    if from_local:
        # Read from local knowledge_base/manim_ce_rules/ instead of GitHub
        for rule in RULES:
            path = LOCAL_CACHE_DIR / f"{rule}.md"
            if not path.exists():
                print(f"  local {rule}.md ... SKIP (not found)")
                continue
            content = path.read_text(encoding="utf-8").strip()
            if not content:
                print(f"  local {rule}.md ... SKIP (empty)")
                continue
            sections = _split_by_h2(content, rule)
            chunks.extend(sections)
            print(f"  local {rule}.md ... OK ({len(sections)} chunks)")
        print(f"\n  總計: {len(chunks)} chunks from local files")
        return chunks

    if save_local:
        LOCAL_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    with httpx.Client(timeout=30, follow_redirects=True) as client:
        for rule in RULES:
            url = f"{RAW_BASE}/{rule}.md"
            print(f"  fetch {rule}.md ... ", end="", flush=True)
            resp = client.get(url)
            if resp.status_code != 200:
                print(f"SKIP (HTTP {resp.status_code})")
                continue

            content = resp.text.strip()
            if not content:
                print("SKIP (empty)")
                continue

            if save_local:
                (LOCAL_CACHE_DIR / f"{rule}.md").write_text(content, encoding="utf-8")

            # 把 markdown 拆成 h2 sections，每個 section 一個 chunk
            sections = _split_by_h2(content, rule)
            chunks.extend(sections)
            print(f"OK ({len(sections)} chunks)")

    print(f"\n  總計: {len(chunks)} chunks from {len(RULES)} rule files")
    return chunks


def _split_by_h2(content: str, rule_name: str) -> list[dict]:
    """把一份 md 按 ## 標題切成多個 chunk，每個 chunk 保留標題。"""
    # 先整份作為 fallback chunk
    parts = re.split(r"(?m)^(## .+)$", content)

    if len(parts) <= 1:
        # 沒有 h2 標題，整份當一個 chunk
        return [_make_chunk(rule_name, content, f"manim_ce_rules/{rule_name}")]

    chunks = []
    # parts: [preamble, heading1, body1, heading2, body2, ...]
    preamble = parts[0].strip()
    if preamble:
        chunks.append(_make_chunk(rule_name, preamble, f"manim_ce_rules/{rule_name}/preamble"))

    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        section_text = f"{heading}\n\n{body}".strip()
        slug = re.sub(r"[^a-z0-9]+", "-", heading.lstrip("# ").lower()).strip("-")
        chunks.append(_make_chunk(rule_name, section_text, f"manim_ce_rules/{rule_name}/{slug}"))

    return chunks


def _make_chunk(rule_name: str, text: str, source_file: str) -> dict:
    return {
        "code_content": text,           # 被 text2vec 向量化的主欄位
        "imports": "",                   # 不適用
        "complexity_score": 0,
        "manim_modules": rule_name,      # 用 rule 名稱標記模組域
        "source_file": source_file,
        "topic": f"best_practices/{rule_name}",
        "video_description": f"Manim CE best practice: {rule_name}",
    }


# ── Weaviate upload ───────────────────────────────────────────────────────────

def upload(chunks: list[dict]) -> None:
    client = weaviate.connect_to_local()
    try:
        collection = client.collections.get("ManimGoldenPair")
        with collection.batch.dynamic() as batch:
            for chunk in chunks:
                batch.add_object(properties=chunk)
        print(f"  Weaviate: uploaded {len(chunks)} objects into ManimGoldenPair")
    finally:
        client.close()


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Ingest manim_skill rules into Weaviate")
    parser.add_argument("--dry-run", action="store_true", help="Fetch only, skip Weaviate write")
    parser.add_argument("--save-local", action="store_true", help="Also save .md to knowledge_base/manim_ce_rules/")
    parser.add_argument("--from-local", action="store_true", help="Read from local knowledge_base/manim_ce_rules/ instead of GitHub")
    args = parser.parse_args()

    if args.from_local:
        print("Reading manim_skill rules from local files...")
    else:
        print("Fetching manim_skill rules from GitHub...")
    chunks = fetch_rules(save_local=args.save_local, from_local=args.from_local)

    if not chunks:
        print("No chunks fetched, abort.")
        sys.exit(1)

    if args.dry_run:
        print("\n[dry-run] Skipping Weaviate upload.")
        print("Sample chunk:")
        c = chunks[0]
        print(f"  topic: {c['topic']}")
        print(f"  source_file: {c['source_file']}")
        print(f"  content[:200]: {c['code_content'][:200]}")
        return

    print("\nUploading to Weaviate...")
    upload(chunks)
    print("\nDone.")


if __name__ == "__main__":
    main()