"""
Structured result types for RefiningLoop.auto_fix_loop().

Phase 1 (Design C): Thin adapter over the existing monolithic method.
- FixLoopResult: typed return value replacing `str | False`
- run_fix_loop(): adapter function that callers should use instead of
  RefiningLoop.auto_fix_loop() directly

Usage:
    from agents.orchestrator.refining_loop_types import run_fix_loop

    result = run_fix_loop(
        file_path, scene_name, user_topic, script_json,
        llm_client=llm, backup_filename_prefix=session_dir,
    )
    if result.video_path:
        ...  # success or best-effort
    print(result.failure_reason, result.counters_final)
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FailureReason(str, Enum):
    SUCCESS = "success"
    VISUAL_BUDGET_EXCEEDED = "visual_budget_exceeded"   # visual_attempts >= limit
    LINTER_BUDGET_EXCEEDED = "linter_budget_exceeded"   # linter_only_retries >= budget
    MAX_ITERATIONS = "max_iterations"                   # i >= max_attempts (hard cap: 5)
    LLM_FATAL = "llm_fatal"                             # unrecoverable LLMError
    ALL_SC_WORKERS_FAILED = "all_sc_workers_failed"     # candidates list empty
    VIDEO_NOT_FOUND = "video_not_found"                 # render succeeded but output file missing
    TEMPLATE_OVERRIDE_ACTIVATED = "template_override_activated"  # consecutive_timeouts >= 1
    UNKNOWN = "unknown"


@dataclass
class FixLoopResult:
    """
    Structured return value for run_fix_loop().

    Quick path:  check `video_path` (None = complete failure).
    Diagnostic:  check `failure_reason`, `counters_final`, `iterations`.
    """

    # ── Quick path ─────────────────────────────────────────────────────
    video_path: str | None
    """Absolute path to the final .mp4, or None if all attempts failed."""

    is_best_effort: bool
    """True = loop exhausted budget but archived last successful render as fallback.
    Vision PASS was NOT achieved. Video exists but quality may be suboptimal."""

    # ── Result summary ──────────────────────────────────────────────────
    failure_reason: FailureReason
    total_wall_time: float

    # ── Counter snapshot at loop exit ───────────────────────────────────
    # Counter semantics match auto_fix_loop exactly:
    #   visual    – increments on Vision FAIL/low-confidence, NOT on Render FAIL
    #   linter    – independent budget, does NOT consume visual
    #   timeouts  – consecutive render timeouts (reset to 0 after any successful render)
    #   main_i    – main iteration index (linter-only retries do NOT increment this)
    counters_final: dict[str, int] = field(default_factory=dict)
    """Keys: "visual", "linter", "timeouts", "main_i"."""

    # ── Diagnostic path ─────────────────────────────────────────────────
    reflection_memory: list[Any] = field(default_factory=list)
    failed_code_snapshots: list[tuple[int, str, str]] = field(default_factory=list)
    """List of (attempt_num, failure_type, code) tuples, max 5 entries."""


def run_fix_loop(
    file_path: str,
    scene_name: str,
    user_topic: str,
    script_json: str,
    *,
    llm_client=None,
    max_attempts: int = 5,
    backup_filename_prefix: str | None = None,
) -> FixLoopResult:
    """
    Thin adapter over RefiningLoop.auto_fix_loop().

    Does NOT change any business logic — only wraps the result into FixLoopResult.
    The underlying method is called with a `_diagnostics` dict to capture counter
    state without modifying the main loop structure.
    """
    from agents.orchestrator.refining_loop import RefiningLoop

    _diagnostics: dict[str, Any] = {}
    _start = time.time()

    raw_result = RefiningLoop.auto_fix_loop(
        file_path=file_path,
        scene_name=scene_name,
        user_topic=user_topic,
        script_json=script_json,
        llm_client=llm_client,
        max_attempts=max_attempts,
        backup_filename_prefix=backup_filename_prefix,
        _diagnostics=_diagnostics,
    )

    wall_time = round(time.time() - _start, 2)

    # Interpret raw result
    if raw_result and isinstance(raw_result, str):
        video_path = raw_result
        is_best_effort = _diagnostics.get("is_best_effort", False)
        failure_reason = FailureReason(_diagnostics.get("failure_reason", "max_iterations" if is_best_effort else "success"))
    else:
        video_path = None
        is_best_effort = False
        failure_reason = FailureReason(_diagnostics.get("failure_reason", "unknown"))

    # If template override was activated (consecutive_timeouts >= 1), note it
    # This is informational — the loop may still have succeeded.
    _timeouts = _diagnostics.get("consecutive_timeouts", 0)
    if _timeouts >= 1 and failure_reason == FailureReason.SUCCESS:
        # Loop succeeded but went through template override — record in counters
        pass  # failure_reason stays SUCCESS; counters_final will show timeouts

    return FixLoopResult(
        video_path=video_path,
        is_best_effort=is_best_effort,
        failure_reason=failure_reason,
        total_wall_time=wall_time,
        counters_final={
            "visual": _diagnostics.get("visual_attempts", 0),
            "linter": _diagnostics.get("linter_only_retries", 0),
            "timeouts": _diagnostics.get("consecutive_timeouts", 0),
            "main_i": _diagnostics.get("main_i", 0),
        },
        reflection_memory=_diagnostics.get("reflection_memory", []),
        failed_code_snapshots=_diagnostics.get("failed_code_snapshots", []),
    )
