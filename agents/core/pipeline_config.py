"""
Pipeline configuration dataclass.
All magic numbers and runtime constants live here.
Override at startup via env vars or by mutating the singleton `CFG`.
"""
from dataclasses import dataclass, field
import os
import time


class StageTimer:
    """Context manager for timing pipeline stages.

    Prints elapsed time on exit and optionally accumulates into a stats dict.

    Usage:
        # Basic — just print
        with StageTimer("Planner"):
            ...

        # With stats accumulation
        with StageTimer("Planner", llm.session_stats, "time_planner_sec"):
            ...

        # Read elapsed mid-flight
        with StageTimer("Render") as t:
            render()
            print(f"so far: {t.elapsed:.1f}s")
    """

    def __init__(self, name: str, stats: dict = None, stats_key: str = None, silent: bool = False):
        self.name = name
        self.stats = stats
        self.stats_key = stats_key
        self.silent = silent
        self._start: float = 0.0
        self.elapsed: float = 0.0

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, *_):
        self.elapsed = time.time() - self._start
        if not self.silent:
            print(f"⏱  [{self.name}] {self.elapsed:.1f}s")
        if self.stats is not None and self.stats_key:
            self.stats[self.stats_key] += self.elapsed


@dataclass
class PipelineConfig:
    # ── Render settings ───────────────────────────────────────────────
    fps_preview: int = 8          # Low-fps preview for Vision QA (speed >> quality)
    fps_final: int = 15           # Final high-quality render after preview passes
    render_timeout_sec: int = 120 # Hard kill for runaway Manim processes

    # ── RefiningLoop budgets ───────────────────────────────────────────
    max_refine_attempts: int = 5  # Hard cap on main render+fix iterations
    visual_attempts_limit: int = 3
    linter_retry_budget: int = 3  # Extra retries for linter-only failures
    tdr_t1_cap: int = 3           # Zero-cost T1 TDR re-renders
    tdr_t2_cap: int = 2           # Cheap micro-prompt T2 fixes

    # ── Vision confidence gradient ─────────────────────────────────────
    vision_conf_accept: int = 4   # confidence_score >= this → immediate accept
    vision_conf_soft_fail: int = 3 # confidence_score == this and budget remains → soft-fail

    # ── SubtitleManager ───────────────────────────────────────────────
    subtitle_max_width: float = 12.5
    subtitle_font_size: int = 28
    subtitle_y_offset: float = 3.2  # Distance from bottom (DOWN direction)

    # ── LLM models ────────────────────────────────────────────────────
    model_planner: str = field(
        default_factory=lambda: os.getenv("PLANNER_MODEL", "deepseek-v4-flash")
    )
    model_coder: str = field(
        default_factory=lambda: os.getenv("DEEPSEEK_MODEL_CODER", "deepseek-v4-flash")
    )
    model_vision: str = field(
        default_factory=lambda: os.getenv("VISION_MODEL", "google/gemini-2.0-flash-001")
    )
    model_tier3: str = "deepseek-v4-flash"  # DeepSeek-V4 thinking mode


# Global singleton — import and use directly:
#   from agents.core.pipeline_config import CFG
#   print(CFG.fps_preview)
CFG = PipelineConfig()