"""Build run_evaluation.py test_cases JSON from kb150_v2_topics.json.

Usage:
  python rag/build_kb150_v2_cases.py            # build both pilot + full
  python rag/build_kb150_v2_cases.py --pilot    # only pilot 3 cases

Outputs:
  evaluation/kb150_pilot_cases.json     (3 題, Step 2 試水溫)
  evaluation/kb150_full_cases.json      (29 題, Step 2.5 全量)

Pilot 選題策略（覆蓋三種風險情境）：
  1. 簡單+完整 docstring : FractionMultiplicationCancellation
  2. v1 渲染失敗者       : FractionExpressionSimplification
  3. 結構性題型         : GCDLCMExponents
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "evaluation" / "kb150_v2_topics.json"
OUT_PILOT = REPO / "evaluation" / "kb150_pilot_cases.json"
OUT_FULL = REPO / "evaluation" / "kb150_full_cases.json"

PILOT_NAMES = {
    "FractionMultiplicationCancellation",
    "FractionExpressionSimplification",
    "GCDLCMExponents",
}

# 章節 → benchmark category 對應（給 difficulty/category 用）
CHAPTER_CATEGORY = {
    "exponent_scientific_notation": "指數與科學記號",
    "factor_multiple": "因數與倍數",
    "fraction_add_sub": "分數加減",
    "fraction_mul_div": "分數乘除",
    "integer_add_sub": "整數加減",
    "integer_mul_div": "整數乘除",
    "mixed_arithmetic_full": "完整的四則混合運算",
    "pemdas_no_bracket_removal": "四則運算算則（不含去括號）",
    "pemdas_with_bracket_removal": "四則運算（含去括號）",
}


def to_case(scene_name: str, chapter: str, info: dict) -> dict:
    """Convert one v2 topic entry to a test_cases.json record."""
    case_id = f"KB150V2_{scene_name}"
    return {
        "id": case_id,
        "category": CHAPTER_CATEGORY.get(chapter, chapter),
        "difficulty": 3,
        "topic": info["new_topic"],
        "answer": None,
        "question_type": "計算題",
        "solution": f"教學手法：{info['method']}\n備註：{info.get('notes', '')}",
        "required_patterns": ["MathTex|Tex|Text", "self\\.play\\("],
        "disallowed_patterns": ["ShowCreation", "TextMobject", "TexMobject"],
        "min_animation_count": 3,
        "_kb150v2_meta": {
            "scene_name": scene_name,
            "chapter": chapter,
            "method": info["method"],
            "original_v1": info.get("original_v1", ""),
        },
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pilot", action="store_true", help="Only build pilot 3 cases")
    args = p.parse_args()

    v2 = json.loads(SRC.read_text(encoding="utf-8"))

    pilot_cases: list[dict] = []
    full_cases: list[dict] = []

    for chapter, scenes in v2.items():
        if chapter.startswith("_"):
            continue
        for name, info in scenes.items():
            case = to_case(name, chapter, info)
            full_cases.append(case)
            if name in PILOT_NAMES:
                pilot_cases.append(case)

    assert len(pilot_cases) == 3, f"Expected 3 pilot cases, got {len(pilot_cases)}: {[c['id'] for c in pilot_cases]}"
    assert len(full_cases) == 29, f"Expected 29 full cases, got {len(full_cases)}"

    OUT_PILOT.write_text(json.dumps(pilot_cases, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Wrote {OUT_PILOT.relative_to(REPO)} ({len(pilot_cases)} cases)")
    for c in pilot_cases:
        print(f"   - {c['id']}: {c['topic'][:60]}")

    if not args.pilot:
        OUT_FULL.write_text(json.dumps(full_cases, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"✅ Wrote {OUT_FULL.relative_to(REPO)} ({len(full_cases)} cases)")


if __name__ == "__main__":
    main()
