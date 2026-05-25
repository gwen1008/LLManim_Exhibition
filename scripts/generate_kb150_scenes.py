"""
For each seed JSON in knowledge_base/kb150_seeds/, ask LLM to generate a
self-contained Manim Scene that visualizes the solution. Validates output
(syntax, manim import discipline, RAG-friendly docstring) and writes to
knowledge_base/kb150/{slug}/{ClassName}.py.

Note: Generated Scenes are RAG fodder (code structure + docstring for retrieval),
NOT polished render-ready demos. Rendering them directly will often show layout
overlap because Gemini doesn't simulate the 2D canvas. The downstream Coder
agent adapts these patterns and its output goes through RefiningLoop +
Vision agent + pre_render_patch which fix layout. Do not judge KB quality by
rendering these files; judge by whether the Coder produces good videos when
this KB is active (RAG_COLLECTION=ManimKB150).

LLM: Google Gemini via google-generativeai SDK (uses GOOGLE_API_KEY from .env).
Bypasses agents/core/llm_client.LLMClient because that requires GROQ_API_KEY
to construct and routes 'coder' role to claude-code CLI subprocess (which is
macOS-pathed by default and won't work cleanly on Windows here).

Usage:
  python scripts/generate_kb150_scenes.py --dry-run        # print prompt sizes, no LLM
  python scripts/generate_kb150_scenes.py --limit 1        # smoke test on 1 seed
  python scripts/generate_kb150_scenes.py                  # full run (27 seeds)
"""
from __future__ import annotations
import argparse
import ast
import json
import os
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env")


SYSTEM_PROMPT = """You are an expert ManimCE v0.19.2 developer producing reference Scene examples for a RAG knowledge base. Each Scene visualizes the worked solution to one math problem step by step.

STRICT RULES:
1. Output ONLY valid Python code, no markdown fences (no ```python).
2. Must start with `from manim import *` — DO NOT use `from manimlib import *` (this project is ManimCE, not ManimGL).
3. Define exactly ONE Scene subclass with a CamelCase name reflecting the specific technique (e.g. ZeroPairIntegerAddition, DistributiveLawMultiplication, ScientificNotationCellLength).
4. The class MUST have a one-line docstring (>= 20 chars) describing what it visualizes. This docstring is the RAG retrieval anchor — phrase it so a teacher searching for similar problems would find it (mention operation type, key numbers, and technique).
5. Use Text() / MathTex() (NOT deprecated TextMobject / TexMobject).
6. Use .animate syntax: obj.animate.shift(UP). self.add() BEFORE self.play(..animate..).
7. Use VGroup + .arrange() for layout; avoid hard-coded coordinates where possible.
8. self.wait() duration must be > 0.
9. No Chinese characters in class names or variable names; Text(...) labels and # comments MAY contain Chinese.
10. Keep total animation time under ~30 seconds.
"""

USER_PROMPT_TEMPLATE = """Generate a Manim Scene that visualizes the solution to this question step by step.

【知識點】{knowledge}
【題目】{question}
【答案】{answer}

【詳解】
{explanation}

【引導策略】
{guidance}

Reference Scene style (study layout/animation patterns, do NOT copy verbatim):
```python
{reference_scene}
```

Return ONLY the complete Python file content for the new Scene — no commentary, no markdown fences."""


def extract_python(text: str) -> str:
    """Strip ```python ... ``` or ``` ... ``` fences if LLM added them."""
    m = re.search(r"```python\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"```\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()


def validate(code: str) -> tuple[bool, str, str | None]:
    """Return (ok, reason, class_name). class_name is None on failure."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, f"SyntaxError: {e}", None

    if "from manimlib" in code or "import manimlib" in code:
        return False, "forbidden import: manimlib (use manim, not manimgl)", None

    if not re.search(r"from\s+manim\s+import|^\s*import\s+manim\b", code, re.MULTILINE):
        return False, "missing `from manim import *`", None

    scene_class = None
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        for base in node.bases:
            base_name = getattr(base, "id", None) or getattr(base, "attr", None)
            if base_name == "Scene":
                scene_class = node
                break
        if scene_class:
            break

    if scene_class is None:
        return False, "no class extending Scene found", None

    docstring = ast.get_docstring(scene_class)
    if not docstring or len(docstring.strip()) < 20:
        return False, "Scene class missing docstring or too short (need >= 20 chars)", scene_class.name

    # Completeness check: construct() must exist and contain >=1 animation call.
    # Catches Gemini truncation (where AST still parses but the file ends mid-Scene).
    construct = next(
        (n for n in scene_class.body if isinstance(n, ast.FunctionDef) and n.name == "construct"),
        None,
    )
    if construct is None:
        return False, "Scene has no construct() method", scene_class.name
    animation_calls = sum(
        1 for n in ast.walk(construct)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr in {"play", "add", "wait"}
        and isinstance(n.func.value, ast.Name) and n.func.value.id == "self"
    )
    if animation_calls < 2:
        return False, f"construct() only has {animation_calls} self.play/add/wait call (likely truncated)", scene_class.name

    return True, "ok", scene_class.name


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seeds-dir", type=Path, default=Path("knowledge_base/kb150_seeds"))
    ap.add_argument("--out-dir", type=Path, default=Path("knowledge_base/kb150"))
    ap.add_argument(
        "--reference", type=Path,
        default=Path("knowledge_base/examples/arithmetic/VerticalAddition.py"),
        help="Existing Scene used as few-shot style reference.",
    )
    ap.add_argument("--limit", type=int, default=0, help="Process only first N seeds (0=all)")
    ap.add_argument("--dry-run", action="store_true", help="Print prompt sizes only, don't call LLM")
    ap.add_argument("--retries", type=int, default=1, help="Retries per seed after validation failure")
    ap.add_argument(
        "--only-ids", default="",
        help="Comma-separated question ids to process; skip all others. Use to "
             "incrementally generate new seeds without re-running the full batch.",
    )
    args = ap.parse_args()

    if not args.seeds_dir.exists():
        raise SystemExit(f"[ERR] Seeds dir not found: {args.seeds_dir}. Run extract_kb150_seeds.py first.")
    if not args.reference.exists():
        raise SystemExit(f"[ERR] Reference scene not found: {args.reference}")

    reference_scene = args.reference.read_text(encoding="utf-8")
    seeds = sorted(args.seeds_dir.glob("*.json"))
    if args.only_ids:
        only_set = {int(x) for x in args.only_ids.split(",") if x.strip()}
        seeds = [s for s in seeds
                 if json.loads(s.read_text(encoding="utf-8"))["id"] in only_set]
        print(f"[INFO] --only-ids filter: {len(seeds)} seeds match {sorted(only_set)}")
    if args.limit:
        seeds = seeds[:args.limit]
    print(f"[INFO] Processing {len(seeds)} seeds (dry_run={args.dry_run})")

    model = None
    if not args.dry_run:
        import google.generativeai as genai
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise SystemExit("[ERR] GOOGLE_API_KEY not set in .env or environment")
        genai.configure(api_key=api_key)
        # gemini-2.5-flash: fast + cheap + good for code. Override via env (e.g. gemini-2.5-pro for harder).
        model_name = os.environ.get("KB150_GEMINI_MODEL", "gemini-2.5-flash")
        # Loosen safety so math/code prompts don't get spuriously blocked.
        safety_settings = [
            {"category": c, "threshold": "BLOCK_NONE"}
            for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH",
                      "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]
        ]
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=SYSTEM_PROMPT,
            safety_settings=safety_settings,
            generation_config={"temperature": 0.3, "max_output_tokens": 16384},
        )
        print(f"[INFO] Using Gemini model: {model_name}")

    ok_count = 0
    fail_count = 0
    failures: list[str] = []

    for seed_path in seeds:
        seed = json.loads(seed_path.read_text(encoding="utf-8"))
        slug = seed["knowledge_slug"]
        qid = seed["id"]
        question_preview = seed["question"][:50].replace("\n", " ")
        print(f"\n--- [{slug}_{qid:03d}] {question_preview}... ---")

        user_prompt = USER_PROMPT_TEMPLATE.format(
            knowledge=seed["knowledge"],
            question=seed["question"],
            answer=seed["answer"],
            explanation=seed["explanation"],
            guidance=seed["guidance"],
            reference_scene=reference_scene,
        )

        if args.dry_run:
            print(f"  [DRY] system={len(SYSTEM_PROMPT)} chars, user={len(user_prompt)} chars")
            continue

        success = False
        current_user_prompt = user_prompt
        for attempt in range(args.retries + 1):
            try:
                resp = model.generate_content(current_user_prompt)
                raw = resp.text
                finish = "UNKNOWN"
                try:
                    finish = str(resp.candidates[0].finish_reason)
                except Exception:
                    pass
                if "MAX_TOKENS" in finish:
                    print(f"  [WARN] attempt {attempt+1} Gemini hit MAX_TOKENS — output may be truncated")
            except Exception as e:
                print(f"  [ERR] attempt {attempt+1} Gemini call failed: {e}")
                time.sleep(2)
                continue

            code = extract_python(raw)
            ok, reason, cls_name = validate(code)
            if ok:
                out_file = args.out_dir / slug / f"{cls_name}.py"
                out_file.parent.mkdir(parents=True, exist_ok=True)
                out_file.write_text(code, encoding="utf-8")
                print(f"  [OK]  -> {out_file}  (attempt {attempt+1}, class={cls_name})")
                ok_count += 1
                success = True
                break
            else:
                print(f"  [RETRY] attempt {attempt+1} validation failed: {reason}")
                current_user_prompt = (
                    user_prompt
                    + f"\n\nYour previous attempt failed validation: {reason}\n"
                    + "Please fix the issue and return the corrected complete file."
                )

        if not success:
            fail_count += 1
            failures.append(f"{slug}_{qid:03d}: {question_preview}")

    print(f"\n[SUMMARY] OK={ok_count}  FAIL={fail_count}")
    if failures:
        print("Failed seeds:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(2 if ok_count == 0 else 0)


if __name__ == "__main__":
    main()
