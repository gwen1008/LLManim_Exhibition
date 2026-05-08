"""
CE Rules Ingestion Pipeline
============================
Section-level chunking of manim_ce_rules/*.md into ManimGoldenPair.
Each ## section becomes one chunk, with YAML frontmatter as semantic anchor.
"""
import re
import yaml
from pathlib import Path
from typing import List, Dict
import weaviate
from weaviate.classes.query import Filter

RULES_DIR = Path("knowledge_base/manim_ce_rules")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and return (meta, body)."""
    match = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    if match:
        try:
            meta = yaml.safe_load(match.group(1))
            return meta or {}, match.group(2)
        except Exception:
            pass
    return {}, text


def split_into_sections(body: str, filename: str, meta: dict) -> List[Dict]:
    """Split markdown body by ## headings into section-level chunks."""
    sections = re.split(r'\n(?=## )', body.strip())
    
    doc_description = meta.get("description", filename.replace(".md", "").replace("-", " "))
    doc_tags = meta.get("metadata", {}).get("tags", "") if isinstance(meta.get("metadata"), dict) else ""

    chunks = []
    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Extract section title
        title_match = re.match(r'^##\s+(.+)', section)
        section_title = title_match.group(1).strip() if title_match else meta.get("name", filename)

        # Skip sections that are nearly empty (< 3 lines)
        lines = [l for l in section.split('\n') if l.strip()]
        if len(lines) < 3:
            continue

        chunks.append({
            "class_name": f"{meta.get('name', filename)}::{section_title}",
            "code_content": section,
            "imports": "from manim import *",
            "complexity_score": section.count("```python"),  # code block count as proxy
            "manim_modules": doc_tags,
            "source_file": f"manim_ce_rules/{filename}",
            "source_library": "rules",
            "topic": meta.get("name", filename),
            "video_description": f"{doc_description} — {section_title}",
        })

    return chunks


def get_indexed_rule_sources(client) -> set:
    """Return set of already-indexed source_files for rules."""
    collection = client.collections.get("ManimGoldenPair")
    response = collection.query.fetch_objects(
        filters=Filter.by_property("source_library").equal("rules"),
        limit=500,
    )
    return {obj.properties.get("source_file", "") for obj in response.objects}


def run():
    client = weaviate.connect_to_local()
    try:
        print("🔍 Checking already-indexed rules...")
        indexed = get_indexed_rule_sources(client)
        print(f"   {len(indexed)} already indexed, will skip.")

        all_chunks = []
        for md_file in sorted(RULES_DIR.glob("*.md")):
            source_key = f"manim_ce_rules/{md_file.name}"
            if source_key in indexed:
                print(f"   ⏭️  Skip (already indexed): {md_file.name}")
                continue

            text = md_file.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(text)
            chunks = split_into_sections(body, md_file.name, meta)
            print(f"   📄 {md_file.name}: {len(chunks)} sections")
            all_chunks.extend(chunks)

        if not all_chunks:
            print("✅ Everything already indexed. Nothing to do.")
            return

        print(f"\n📤 Uploading {len(all_chunks)} rule chunks...")
        collection = client.collections.get("ManimGoldenPair")
        with collection.batch.dynamic() as batch:
            for chunk in all_chunks:
                batch.add_object(properties=chunk)

        print(f"✅ Uploaded {len(all_chunks)} CE Rules chunks to Weaviate")

    finally:
        client.close()


if __name__ == "__main__":
    print("🚀 Starting CE Rules Ingestion (append-only)...")
    run()
    print("🎉 CE Rules ingestion complete!")
