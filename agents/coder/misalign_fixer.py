"""
agents/coder/misalign_fixer.py

Tiered Defect Router (TDR) for MISALIGNED vision defects.

Classifies Vision Agent MISALIGNED defects into 3 tiers and applies
the cheapest effective fix at each tier:

  T1 (Parametric)  — Wrong numeric literal (e.g. buff=0.2 → buff=0)
                     Fix: deterministic AST rewrite, zero LLM cost.

  T2 (Relational)  — Wrong positioning method (e.g. next_to → move_to)
                     Fix: focused micro-prompt (~2K tokens vs ~20K full context).

  T3 (Structural)  — Incompatible coordinate systems or architecture
                     Fix: fall through to existing full-context LLM pipeline.

Integration: See agents/orchestrator/refining_loop.py → auto_fix_loop()
"""
import re
from typing import Optional

from .positioning_ast import find_positioning_calls, get_source_lines_around


# ─────────────────────────────────────────────────────────────────────────────
# Classification patterns
# ─────────────────────────────────────────────────────────────────────────────

# T1: Vision hints at changing a numeric value (buff, shift amount, etc.)
_T1_PATTERNS = [
    r'\bbuff\s*=\s*[\d.]+',                       # "use buff=0" / "buff=0.5"
    r'\bchange\s+[\d.]+\s+to\s+[\d.]+',           # "change 0.2 to 0"
    r'\bset\s+buff\s+to\s+[\d.]+',                # "set buff to 0"
    r'\breduce\s+(the\s+)?buff\b',                 # "reduce the buff"
    r'\bsmaller\s+buff\b',
    r'\bbuff\s*(value\s*)?to\s+0\b',              # "buff to 0"
    r'\bbuff\s*=\s*0\b',                           # explicit "buff=0"
    r'\bdecrease\s+(the\s+)?gap\b',
    r'\bremove\s+(the\s+)?gap\b',
]

# T2: Vision hints at changing the positioning method
_T2_PATTERNS = [
    r'\buse\s+(align_to|move_to|next_to|to_edge|to_corner|align_on_border)\b',
    r'\binstead\s+of\s+(shift|move_to|next_to|align_to)\b',
    r'\breplace\s+.*?\b(shift|move_to|next_to)\b',
    r'\balign\b.*(edge|corner|side)\b',
    r'\bsnap\b.*\bto\b',
    r'\bget_origin\b',          # "use axes.get_origin()"
    r'\bget_center\b.*\bof\b',  # "center of ..."
]


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def classify_misalignment(defect: dict, source_code: str) -> str:
    """
    Classify a single MISALIGNED defect as "T1", "T2", or "T3".

    Combines Vision suggested_fix text heuristics with AST verification:
    - T1 requires at least one positioning call with a non-zero buff= literal.
    - T2 requires a positioning call (any kind) to exist.
    - T3 is the fallback when code structure is the issue.
    """
    text = (defect.get("suggested_fix", "") + " " + defect.get("description", "")).strip()

    # --- T1 check ---
    for pat in _T1_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            calls = find_positioning_calls(source_code)
            # Cross-verify: there must be a buff= call to patch
            if any(c.buff_value is not None for c in calls):
                return "T1"
            # No buff= to patch, fall through to T2 check
            break

    # --- T2 check ---
    for pat in _T2_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return "T2"

    return "T3"


def fix_t1_parametric(defect: dict, source_code: str) -> Optional[str]:
    """
    Deterministic AST-guided fix for T1 parametric misalignment.

    Locates the single buff= kwarg in a positioning call and replaces its
    value based on the Vision Agent's suggestion.

    Safety rule: only modifies when there is EXACTLY ONE candidate call with
    a non-zero buff= literal. If 0 or 2+ candidates exist, returns None so
    the caller can escalate to T2.

    Returns:
        str: patched source code on success.
        None: cannot apply fix safely (ambiguous or no candidate).
    """
    calls = find_positioning_calls(source_code)
    candidates = [c for c in calls if c.buff_value is not None and c.buff_value > 0]

    if len(candidates) != 1:
        # Ambiguous — don't guess
        return None

    target = candidates[0]
    new_buff = _extract_target_buff(defect.get("suggested_fix", ""))

    # Patch the specific source line (1-indexed)
    lines = source_code.splitlines(keepends=True)
    idx = target.lineno - 1
    old_line = lines[idx]

    new_line = re.sub(
        r'\bbuff\s*=\s*[\d.]+',
        f'buff={new_buff}',
        old_line,
    )
    if new_line == old_line:
        return None  # Nothing changed (regex didn't match on that line)

    lines[idx] = new_line
    return "".join(lines)


def generate_micro_prompt(defect: dict, source_code: str) -> str:
    """
    Generate a focused ~2K token SEARCH/REPLACE prompt for T2 relational fixes.

    Instead of sending the full source + full script JSON (~20K tokens),
    this prompt only includes the relevant positioning code context.
    """
    calls = find_positioning_calls(source_code)
    if calls:
        # Use median positioning call as focal point for context window
        linenos = sorted(c.lineno for c in calls)
        focal = linenos[len(linenos) // 2]
        snippet = get_source_lines_around(source_code, focal, context=8)
    else:
        # Fallback: first 40 lines
        snippet = "\n".join(
            f"{i + 1:4d}: {line}"
            for i, line in enumerate(source_code.splitlines()[:40])
        )

    return (
        "A Manim animation has a VISUAL MISALIGNMENT defect found by a vision QA audit.\n"
        "Fix only the relevant positioning code.\n\n"
        f"DEFECT DESCRIPTION:\n  {defect.get('description', 'N/A')}\n\n"
        f"SUGGESTED FIX:\n  {defect.get('suggested_fix', 'N/A')}\n\n"
        "RELEVANT CODE CONTEXT (positioning calls and surroundings):\n"
        f"{snippet}\n\n"
        "Provide a SEARCH/REPLACE patch for the misaligned lines only.\n"
        "Do NOT rewrite the entire file or change unrelated logic.\n\n"
        "Output format (strict):\n"
        "<<<< SEARCH\n"
        "(exact lines from original code, preserving indentation)\n"
        "====\n"
        "(corrected replacement)\n"
        ">>>>"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

def _extract_target_buff(suggested_fix: str) -> float:
    """
    Parse Vision's suggested_fix text for an explicit target buff value.
    Falls back to 0.0 (touching/snapped) if no number is found.
    """
    # "buff=0", "buff = 0.0", "use buff=0.5"
    m = re.search(r'\bbuff\s*=\s*([\d.]+)', suggested_fix, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass

    # "change X to Y" → use Y
    m = re.search(r'\bchange\s+[\d.]+\s+to\s+([\d.]+)', suggested_fix, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass

    return 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Main router class
# ─────────────────────────────────────────────────────────────────────────────

class MisalignmentRouter:
    """
    Entry point for the Tiered Defect Router.

    Usage in refining_loop.py:

        router = MisalignmentRouter()

        # Try zero-cost T1 fix first
        patched = router.try_t1_fix(misaligned_defects, current_code)
        if patched:
            write(patched); continue  # skip LLM entirely

        # T1 failed → try lightweight T2 micro-prompt
        micro_prompt = router.get_t2_prompt(misaligned_defects, current_code)
        if micro_prompt:
            micro_fix_raw = llm.ask_for_fix(micro_prompt)  # ~2K tokens only
            micro_fix = LLMClient.extract_code(micro_fix_raw)
            patched = apply_patch_block(current_code, micro_fix)
            if patched: write(patched); continue

        # Fallthrough to full T3 pipeline (existing behavior, unchanged)
    """

    def try_t1_fix(
        self, misaligned_defects: list[dict], source_code: str
    ) -> Optional[str]:
        """
        Attempt a zero-cost T1 parametric fix on the first matching defect.

        Returns patched source code string, or None if T1 is not applicable.
        """
        for defect in misaligned_defects:
            if classify_misalignment(defect, source_code) == "T1":
                patched = fix_t1_parametric(defect, source_code)
                if patched:
                    return patched
        return None

    def get_t2_prompt(
        self, misaligned_defects: list[dict], source_code: str
    ) -> Optional[str]:
        """
        Generate a T2 micro-prompt for the first T1-or-T2 classified defect.

        Returns None only when all defects are T3 (structural), which means
        the caller should fall through to the full LLM pipeline.
        """
        for defect in misaligned_defects:
            tier = classify_misalignment(defect, source_code)
            if tier in ("T1", "T2"):
                # T2 prompt covers both genuinely T2 and T1-that-failed
                return generate_micro_prompt(defect, source_code)
        return None
