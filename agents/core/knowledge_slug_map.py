"""Single source of truth: Chinese 知識點 → ASCII slug.

Used by RAG ingest, retrieval audits, and KB150 seed extraction. Keys must
match exactly the 知識點 strings in evaluation source JSON/xlsx. Verified
against data/_xlsx_inspect.json on 2026-05-17.

Previously duplicated in three places (rag/audit_retrieval_30.py,
rag/check_sample_collision.py, scripts/extract_kb150_seeds.py) — drift
between them caused silent slug-match misses.
"""

KP_TO_SLUG: dict[str, str] = {
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
