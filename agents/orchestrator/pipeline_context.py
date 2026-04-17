"""
PipelineContext: Single source of truth for auto_fix_loop counter state.

Phase 2 of the RefiningLoop decomposition RFC. Centralizes the 10+ local
counter variables that were previously scattered across auto_fix_loop, making
budget semantics explicit and testable without restructuring the main loop.

Counter semantics (preserved exactly from original auto_fix_loop):
- visual_attempts   : increments on Vision FAIL or low-confidence, NOT on Render FAIL
- linter_only_retries: independent budget; does NOT consume main_i
- consecutive_timeouts: resets to 0 after any successful render
- main_i            : only increments on non-linter-only failures
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PipelineContext:
    """
    Holds all mutable loop state for auto_fix_loop.

    Instantiate once at the top of auto_fix_loop, then pass to _fill_diagnostics
    instead of reading individual variables.
    """

    # ── Budget counters (hard caps enforced by charge_* methods) ──────────
    visual_attempts: int = 0
    linter_only_retries: int = 0
    consecutive_timeouts: int = 0
    tdr_t1_attempts: int = 0
    tdr_t2_attempts: int = 0
    main_i: int = 0           # i in original code
    total_loops: int = 0      # safety cap counter

    # ── Hard limits (mirror CFG values set at construction time) ──────────
    max_attempts: int = 5
    visual_attempts_limit: int = 3    # CFG.visual_attempts_limit
    linter_retry_budget: int = 3      # CFG.linter_retry_budget
    tdr_t1_cap: int = 2               # CFG.tdr_t1_cap
    tdr_t2_cap: int = 2               # CFG.tdr_t2_cap

    # ── Control flags ────────────────────────────────────────────────────
    is_linter_only_failure: bool = False
    patch_mode: bool = False
    syntax_rollback: bool = False

    # ── Diagnostic state ─────────────────────────────────────────────────
    reflection_memory: list[Any] = field(default_factory=list)
    failed_code_snapshots: list[tuple[int, str, str]] = field(default_factory=list)
    last_error_message: str = ""
    last_render_hash: str | None = None
    last_successful_video_path: str | None = None

    # ── Budget helpers (preserve original counter semantics exactly) ──────

    def charge_visual(self) -> bool:
        """Increment visual_attempts. Returns True if limit now reached."""
        self.visual_attempts += 1
        return self.visual_attempts >= self.visual_attempts_limit

    def charge_linter(self) -> bool:
        """Increment linter_only_retries. Returns True if budget exhausted."""
        self.linter_only_retries += 1
        return self.linter_only_retries >= self.linter_retry_budget

    def charge_timeout(self) -> bool:
        """Increment consecutive_timeouts. Returns True if >= 3."""
        self.consecutive_timeouts += 1
        return self.consecutive_timeouts >= 3

    def reset_timeout(self) -> None:
        self.consecutive_timeouts = 0

    def advance_main(self) -> None:
        """Increment main_i (non-linter-only path)."""
        self.main_i += 1

    def advance_linter_or_main(self) -> None:
        """
        Mirrors the original counter logic at line 1804:
            if is_linter_only_failure and linter_only_retries < LINTER_RETRY_BUDGET:
                linter_only_retries += 1
            else:
                i += 1
        """
        if self.is_linter_only_failure and self.linter_only_retries < self.linter_retry_budget:
            self.linter_only_retries += 1
        else:
            self.main_i += 1

    # ── Loop termination conditions ───────────────────────────────────────

    def should_continue(self) -> bool:
        """Mirrors: while i < max_attempts and total_loops < max_attempts + LINTER_RETRY_BUDGET"""
        return (
            self.main_i < self.max_attempts
            and self.total_loops < self.max_attempts + self.linter_retry_budget
        )

    def visual_budget_exhausted(self) -> bool:
        return self.visual_attempts >= self.visual_attempts_limit

    def linter_budget_exhausted(self) -> bool:
        return self.linter_only_retries >= self.linter_retry_budget

    def to_diagnostics_dict(self, is_best_effort: bool, failure_reason: str) -> dict:
        return {
            "visual_attempts": self.visual_attempts,
            "linter_only_retries": self.linter_only_retries,
            "consecutive_timeouts": self.consecutive_timeouts,
            "main_i": self.main_i,
            "is_best_effort": is_best_effort,
            "failure_reason": failure_reason,
            "reflection_memory": list(self.reflection_memory),
            "failed_code_snapshots": list(self.failed_code_snapshots),
        }
