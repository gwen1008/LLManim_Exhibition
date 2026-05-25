"""Audit kb150 Manim Scene templates for code quality issues.

Read-only AST + regex checks. Outputs CSV report.

Rules:
  A_FADEOUT_GAP      : self.play(Write/Create/...) 次數 - FadeOut/Uncreate 次數 > 1
                       → 物件可能殘留畫面造成擁擠
  B_ADD_NO_REMOVE    : self.add(...) 後找不到對應的 remove/FadeOut
  C_DEPRECATED_API   : 過時 API 殘留（ShowCreation, TextMobject, get_graph 等）
  D_OVERLAP_RISK     : Mobject 構建數 > 5 且檔內無 VGroup/arrange/next_to 任一
  E_LATEX_UNICODE    : MathTex/Tex 內嵌中日韓字元（會觸發 LaTeX Unicode error）
  F_FRAC_INDEX_RISK  : `\\frac{...}` 後緊接 `[數字]` 索引（不穩定，剛才已踩雷）

Usage:
  python rag/audit_kb150_quality.py
  python rag/audit_kb150_quality.py --kb-path knowledge_base/kb150 --out evaluation/kb150_audit.csv
"""

from __future__ import annotations

import argparse
import ast
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

DEPRECATED_APIS = [
    "ShowCreation",
    "TextMobject",
    "TexMobject",
    "get_graph",
    "GraphScene",
    "ContinualAnimation",
    "SmallDot",  # not deprecated but often misused; keep optional
]

CREATE_LIKE = {"Write", "Create", "FadeIn", "GrowFromCenter", "GrowFromEdge",
               "GrowArrow", "DrawBorderThenFill", "ShowIncreasingSubsets",
               "AddTextLetterByLetter"}
REMOVE_LIKE = {"FadeOut", "Uncreate", "ShrinkToCenter", "Unwrite"}
# Transform-like 動作會「替換」物件（舊物件自動移除、新物件出現），不算淨增加。
# 從 CREATE_LIKE 移出來避免 A_FADEOUT_GAP 偽陽性。
TRANSFORM_LIKE = {"Transform", "TransformMatchingTex",
                  "TransformMatchingShapes", "ReplacementTransform"}

LATEX_FN_NAMES = {"MathTex", "Tex"}

CJK_PATTERN = re.compile(r"[　-〿぀-ゟ゠-ヿ一-鿿가-힯]")
FRAC_INDEX_PATTERN = re.compile(r"\\frac\{[^}]*\}\{[^}]*\}[^)\n]*?\)\s*\[\d")


def _walk_calls(tree):
    """Yield ast.Call nodes."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            yield node


def _call_name(call: ast.Call) -> str:
    """Best-effort extract callable name from ast.Call."""
    f = call.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return ""


def _string_args(call: ast.Call):
    """Yield string constants among positional args."""
    for arg in call.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            yield arg.value


def audit_file(path: Path) -> list[dict]:
    """Return list of finding dicts for the file."""
    src = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [{"file": str(path), "rule": "SYNTAX_ERROR", "line": e.lineno or 0, "detail": str(e)}]

    findings: list[dict] = []
    create_calls = 0
    remove_calls = 0
    add_lines: list[int] = []
    mobject_constructions = 0
    has_layout_helper = False

    for call in _walk_calls(tree):
        name = _call_name(call)

        # Rule A/B counters
        if name in CREATE_LIKE:
            create_calls += 1
        elif name in REMOVE_LIKE:
            remove_calls += 1
        elif name == "add":
            # heuristic: self.add(...) — record line for rule B
            if isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name) and call.func.value.id == "self":
                add_lines.append(call.lineno)

        # Rule C deprecated API
        if name in DEPRECATED_APIS:
            findings.append({"file": str(path), "rule": "C_DEPRECATED_API",
                             "line": call.lineno, "detail": f"call to deprecated `{name}`"})

        # Rule D heuristic counters
        if name in {"MathTex", "Tex", "Text", "Line", "Arrow", "Circle", "Square",
                    "Polygon", "Rectangle", "Dot", "Triangle"}:
            mobject_constructions += 1
        if name in {"VGroup", "arrange", "next_to", "arrange_in_grid"}:
            has_layout_helper = True

        # Rule E: LaTeX Unicode
        if name in LATEX_FN_NAMES:
            for s in _string_args(call):
                if CJK_PATTERN.search(s):
                    findings.append({"file": str(path), "rule": "E_LATEX_UNICODE",
                                     "line": call.lineno,
                                     "detail": f"{name}(...) contains CJK char: {CJK_PATTERN.search(s).group()!r}"})
                    break

    # Rule A
    gap = create_calls - remove_calls
    if gap > 1:
        findings.append({"file": str(path), "rule": "A_FADEOUT_GAP",
                         "line": 0,
                         "detail": f"create-like={create_calls}, remove-like={remove_calls}, gap={gap}"})

    # Rule B
    if add_lines:
        # find any remove/FadeOut in the file referring to add'd Mobjects is hard;
        # weak heuristic: if file has zero FadeOut/Uncreate at all, flag every self.add
        if remove_calls == 0:
            for ln in add_lines:
                findings.append({"file": str(path), "rule": "B_ADD_NO_REMOVE",
                                 "line": ln,
                                 "detail": "self.add(...) used but file has 0 FadeOut/Uncreate"})

    # Rule D
    if mobject_constructions > 5 and not has_layout_helper:
        findings.append({"file": str(path), "rule": "D_OVERLAP_RISK",
                         "line": 0,
                         "detail": f"mobjects={mobject_constructions} but no VGroup/arrange/next_to"})

    # Rule F: brittle frac index (regex over source text, AST-bypassing)
    for m in FRAC_INDEX_PATTERN.finditer(src):
        line = src[:m.start()].count("\n") + 1
        findings.append({"file": str(path), "rule": "F_FRAC_INDEX_RISK",
                         "line": line,
                         "detail": "MathTex with \\frac{}{} followed by [int] index — unstable"})

    return findings


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--kb-path", default=str(REPO_ROOT / "knowledge_base" / "kb150"))
    p.add_argument("--out", default=str(REPO_ROOT / "evaluation" / "kb150_audit.csv"))
    args = p.parse_args()

    kb_root = Path(args.kb_path)
    files = sorted(kb_root.rglob("*.py"))
    print(f"Scanning {len(files)} files under {kb_root}")

    all_findings: list[dict] = []
    for f in files:
        findings = audit_file(f)
        if findings:
            # shorten file path for readability (only if under REPO_ROOT)
            for fd in findings:
                p = Path(fd["file"])
                try:
                    fd["file"] = str(p.relative_to(REPO_ROOT))
                except ValueError:
                    fd["file"] = str(p)
            all_findings.extend(findings)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["file", "rule", "line", "detail"]
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(all_findings)

    # Summary
    from collections import Counter
    rule_counts = Counter(f["rule"] for f in all_findings)
    file_counts = Counter(f["file"] for f in all_findings)

    print(f"\n✅ Wrote: {out_path}")
    print(f"Total findings: {len(all_findings)}")
    print(f"Files with issues: {len(file_counts)} / {len(files)}")
    print("\nBy rule:")
    for rule, n in sorted(rule_counts.items(), key=lambda x: -x[1]):
        print(f"  {rule}: {n}")
    print("\nTop 10 files by issue count:")
    for fname, n in file_counts.most_common(10):
        print(f"  {n:>3}  {fname}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
