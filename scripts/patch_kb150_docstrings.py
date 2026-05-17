"""
Patch every Scene docstring in knowledge_base/kb150/ to prepend the knowledge
category. This boosts RAG retrieval relevance: Gemini's auto-generated
docstrings emphasized specific techniques (grouping, distributive) but rarely
the broad category, so queries containing 知識點 didn't match the right scene
strongly enough.

After running, re-ingest:
  python rag/ingest_code.py --collection ManimKB150 --kb-dir knowledge_base/kb150/
"""
from __future__ import annotations
import re
from pathlib import Path

# Bilingual prefix so queries in both Chinese 知識點 and English Manim vocabulary hit.
PREFIX = {
    "integer_add_sub":              "Integer addition subtraction 整數加減: ",
    "integer_mul_div":              "Integer multiplication division 整數乘除: ",
    "fraction_add_sub":             "Fraction addition subtraction 分數加減: ",
    "fraction_mul_div":             "Fraction multiplication division 分數乘除: ",
    "pemdas_no_bracket_removal":    "PEMDAS order of operations without bracket removal 四則運算算則 不含去括號: ",
    "pemdas_with_bracket_removal":  "PEMDAS with bracket removal distributive 四則運算 含去括號: ",
    "mixed_arithmetic_full":        "Complete mixed arithmetic 完整的四則混合運算: ",
    "exponent_scientific_notation": "Exponent scientific notation 指數與科學記號: ",
    "factor_multiple":              "Factor multiple GCD LCM 因數與倍數: ",
}

DOCSTRING_RE = re.compile(
    r'(class\s+\w+\s*\(\s*Scene\s*\)\s*:\s*\n\s*)("""|\'\'\')(.*?)(\2)',
    re.DOTALL,
)


def patch_file(path: Path, prefix: str) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    m = DOCSTRING_RE.search(text)
    if not m:
        return False, "no class+docstring matched"
    doc_body = m.group(3).strip()
    # Skip if already patched (idempotent).
    if doc_body.startswith(prefix.strip()):
        return False, "already patched"
    new_body = f"\n    {prefix}{doc_body}\n    "
    new_text = text[:m.start(3)] + new_body + text[m.end(3):]
    path.write_text(new_text, encoding="utf-8")
    return True, "patched"


def main() -> None:
    kb_dir = Path("knowledge_base/kb150")
    patched = 0
    skipped = 0
    failed = 0
    for slug_dir in sorted(kb_dir.iterdir()):
        if not slug_dir.is_dir():
            continue
        slug = slug_dir.name
        prefix = PREFIX.get(slug)
        if not prefix:
            print(f"[WARN] no prefix for slug {slug!r}, skipping dir")
            continue
        for f in sorted(slug_dir.glob("*.py")):
            ok, reason = patch_file(f, prefix)
            tag = "OK " if ok else ("--" if reason == "already patched" else "ERR")
            print(f"  [{tag}] {slug}/{f.name}  ({reason})")
            if ok:
                patched += 1
            elif reason == "already patched":
                skipped += 1
            else:
                failed += 1
    print(f"\n[SUMMARY] patched={patched}  skipped={skipped}  failed={failed}")


if __name__ == "__main__":
    main()
