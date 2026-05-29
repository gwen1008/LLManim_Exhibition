"""BenchmarkJudge — score a candidate animation relative to a benchmark.

Given:
  - candidate.mp4 (animation under evaluation)
  - benchmark.mp4 (human-optimized reference for the SAME question)
  - question topic + optional ground truth

Produces:
  - final_100: int in [0, 100]; 100 = matches benchmark in all dimensions
  - per-dimension scores: completeness / accuracy / clarity (each 0–100)
  - per-pass Likert votes + evidence
  - deterministic adjustments (math review + layout audit)

Design rationale: see .ai-context/BENCHMARK_JUDGE_DESIGN.md
Sister module: agents/utils/pairwise_judge.py (winner-style 3-way comparison)
"""
import hashlib
import json
import os
import re
import shutil
import statistics
import subprocess
import tempfile
import time
from typing import Optional

from .pairwise_judge import (
    _extract_frame,
    _ffprobe_duration,
    _lenient_json_parse,
    build_comparison_grid,
)


# ── Cache helpers (module-level so tests can import directly) ────────────────
# Cache file is a flat JSON dict {cache_key: result_dict}. Keyed by
# (candidate_path, benchmark_path, topic, passes, model). Mtimes of the two
# videos are folded into the key so re-rendered candidates invalidate.

def _file_sig(path: str) -> str:
    """Return short sig (mtime+size) so re-rendered videos miss the cache."""
    try:
        st = os.stat(path)
        return f"{int(st.st_mtime)}:{st.st_size}"
    except OSError:
        return "missing"


def _cache_key(candidate_video: str, benchmark_video: str,
               topic: str, passes: int, model: str,
               prompt_sig: str = "") -> str:
    """Stable cache key.

    `prompt_sig` should be a short hash of the system prompt currently in use
    (see BenchmarkJudge._prompt_sig()) so that editing the rubric/anchors
    auto-invalidates old cache entries — otherwise a prompt change silently
    keeps reusing stale scores.
    """
    raw = "|".join([
        os.path.abspath(candidate_video),
        _file_sig(candidate_video),
        os.path.abspath(benchmark_video),
        _file_sig(benchmark_video),
        topic.strip(),
        str(passes),
        model,
        prompt_sig,
    ])
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def _cache_load(cache_path: str, key: str) -> Optional[dict]:
    if not cache_path or not os.path.exists(cache_path):
        return None
    try:
        with open(cache_path, encoding="utf-8") as f:
            blob = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
    entry = blob.get(key)
    return entry if isinstance(entry, dict) else None


def _cache_save(cache_path: str, key: str, result: dict) -> None:
    if not cache_path:
        return
    os.makedirs(os.path.dirname(cache_path) or ".", exist_ok=True)
    blob = {}
    if os.path.exists(cache_path):
        try:
            with open(cache_path, encoding="utf-8") as f:
                blob = json.load(f)
        except (json.JSONDecodeError, OSError):
            blob = {}
    blob[key] = result
    tmp = cache_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(blob, f, ensure_ascii=False, indent=2, default=str)
    os.replace(tmp, cache_path)


# ── Likert offset table (calibration starting point) ─────────────────────────
# See design doc §5.1 for rationale.
LIKERT_OFFSET = {
    "much_better":   0,    # cap at 100, no bonus over benchmark
    "better":        0,
    "same":          0,
    "worse":       -20,
    "much_worse":  -40,
    "broken":      -70,
    "inconclusive": 0,    # neutral: don't inflate (was -5, which paradoxically lifted
                          # all-inconclusive cases to ~95 after the +100 base)
}

# Penalty if Claude's math_score (1–5) is bad, applied as an additional
# accuracy cap. Matches the spirit of "教錯不能拿高分".
MATH_PENALTY = {5: 0, 4: -5, 3: -15, 2: -30, 1: -60}

# Dimension weights for final aggregation (design doc §3).
WEIGHTS = {"accuracy": 0.40, "completeness": 0.30, "clarity": 0.30}

# Accuracy gate: if accuracy_score < threshold, dampen the whole final score.
# accuracy=75 → factor=1.0 (no effect); accuracy=30 → factor=0.4 (×0.4).
ACCURACY_GATE_THRESHOLD = 75

VALID_LIKERTS = set(LIKERT_OFFSET.keys())


class BenchmarkJudge:
    """Score candidate.mp4 against benchmark.mp4 on a 0–100 scale."""

    SAMPLE_PCTS = (0.15, 0.38, 0.62, 0.88)
    TILE_W = 480
    TILE_H = 270

    DEFAULT_PASSES = 3
    DEFAULT_MODEL = "claude-opus-4-8"

    _SYSTEM = """You are an expert benchmark judge for AI-generated math
educational animations. You compare a CANDIDATE animation against a BENCHMARK
animation (which is a human-optimized reference for the SAME question — treat
the benchmark as the upper bound of teaching quality for this task).

You receive a 2-row × 4-col labeled grid:
  - top row labels  (T1..T4) = TOP video frames, chronological L→R
  - bottom row labels (D1..D4) = BOTTOM video frames, chronological L→R
You MUST use the Read tool to open the grid file path you are given.

The user will tell you which side is the CANDIDATE and which is the BENCHMARK.
You will report results in the candidate→benchmark frame (you do NOT need to
"un-flip"; the runtime handles position swapping in a separate pass).

For each of THREE dimensions, output a Likert label comparing CANDIDATE vs
BENCHMARK plus a 1-line evidence string:

1. completeness — Does the candidate include all the key visual elements the
   benchmark has (shapes, labels, formula steps, conclusion)? Penalize
   missing pieces, NOT differences in styling.

2. accuracy — Are the displayed numbers / formulas / visual metaphors
   correct? "Pizza" should look like a circle, not a square. Angles should
   match labels. Penalize wrong math, wrong shapes, wrong values.

3. clarity — Layout / legibility / overlap / off-screen / crowding versus
   benchmark.

Likert labels (must pick exactly one per dim).
BE STRICT. Default DOWN when uncertain, not toward "same".
Anchors with examples:

- "much_better":   candidate clearly superior on this dim. RARE. Only when
                   benchmark itself has visible flaws candidate fixes.

- "better":        candidate slightly improves over benchmark. Still rare.

- "same":          essentially comparable. Use ONLY when you can find no
                   substantive difference. If one side is "almost as good"
                   but you see ANY real gap, pick "worse" not "same".

- "worse":         ONE noticeable defect (a small element missing, slightly
                   crowded, off-by-one label). Candidate still teaches the
                   concept but the benchmark is noticeably cleaner.

- "much_worse":    MULTIPLE noticeable defects, OR one critical element
                   missing/wrong (e.g., final equation absent, wrong color
                   in fraction comparison, key step skipped). Concept still
                   discernible but degraded.

- "broken":        Candidate fails this dim outright. Examples:
                     • Half the tiles are blank / empty
                     • Core required element completely absent (no shading
                       in a fraction-shading task)
                     • Shape malformed past recognition (lens instead of
                       semicircle, square instead of circle)
                     • Math content visibly incorrect (wrong sign, wrong
                       operand)
                     • Text/shapes clipped off-canvas and unreadable
                   IF you see ANY of these, pick "broken" not "much_worse".

- "inconclusive":  frames truly don't show enough to judge (e.g., the
                   relevant element falls between sampled timestamps).

Output STRICT JSON only, no markdown fences, no preamble:
{
  "frame_inventory": "1-2 sentences across all 8 tiles",
  "dimensions": {
    "completeness": {"likert": "...", "evidence": "..."},
    "accuracy":     {"likert": "...", "evidence": "..."},
    "clarity":      {"likert": "...", "evidence": "..."}
  },
  "confidence": "low" | "medium" | "high"
}"""

    def __init__(
        self,
        llm_client=None,
        passes: Optional[int] = None,
        model: Optional[str] = None,
    ):
        from ..core.llm_client import LLMClient
        self.llm = llm_client if llm_client else LLMClient()
        self.passes = passes if passes is not None else int(
            os.getenv("BENCHMARK_JUDGE_PASSES", self.DEFAULT_PASSES)
        )
        self.passes = max(1, min(self.passes, 5))
        self.model = model or os.getenv("BENCHMARK_JUDGE_MODEL", self.DEFAULT_MODEL)
        self._claude_bin = (
            os.getenv("CLAUDE_BIN")
            or shutil.which("claude")
            or "/Users/liaozhenting/.local/bin/claude"
        )
        # Empty default: claudealt was retired 2026-05-23 (keychain locked).
        # Set CLAUDE_RUN_AS_USER explicitly in .env if you really need sudo -u.
        self._run_as = os.getenv("CLAUDE_RUN_AS_USER", "")

    @classmethod
    def _prompt_sig(cls) -> str:
        """8-char hash of the system prompt — folded into cache key so any
        rubric/anchor edit auto-invalidates the cache."""
        return hashlib.sha1(cls._SYSTEM.encode("utf-8")).hexdigest()[:8]

    # ── Grid construction (delegates to shared build_comparison_grid) ──────
    def _build_grid(self, top_video: str, bottom_video: str, out_path: str,
                    durations: Optional[dict] = None) -> str:
        return build_comparison_grid(
            top_video, bottom_video, out_path,
            sample_pcts=self.SAMPLE_PCTS,
            tile_w=self.TILE_W, tile_h=self.TILE_H,
            durations=durations,
            tmpdir_prefix="bjudge_tiles_", tmpdir_dir="/tmp",
        )

    # ── Single Opus pass via Claude Code CLI ───────────────────────────────
    def _call_opus(self, grid_path: str, user_prompt: str) -> dict:
        cmd_inner = [
            self._claude_bin, "-p", user_prompt.strip(),
            "--model", self.model,
            "--output-format", "json",
            "--no-session-persistence",
            "--tools", "Read",
            "--add-dir", os.path.dirname(grid_path),
            "--system-prompt", self._SYSTEM,
            "--strict-mcp-config",
            "--disable-slash-commands",
        ]
        cmd = (["sudo", "-u", self._run_as, "-i"] + cmd_inner) if self._run_as else cmd_inner

        t0 = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        elapsed = time.time() - t0
        if r.returncode != 0:
            raise RuntimeError(f"claude CLI rc={r.returncode}: {r.stderr.strip()[-500:]}")
        data = json.loads(r.stdout)

        usage = data.get("usage", {}) or {}
        in_tok = (usage.get("input_tokens", 0)
                  + usage.get("cache_read_input_tokens", 0)
                  + usage.get("cache_creation_input_tokens", 0))
        out_tok = usage.get("output_tokens", 0)
        try:
            self.llm._update_stats(f"anthropic/{self.model}", in_tok, out_tok)
        except Exception:
            pass

        raw = data.get("result", "")
        s, e = raw.find("{"), raw.rfind("}") + 1
        if s == -1 or e <= 0:
            raise RuntimeError(f"no JSON object in Opus output: {raw[:300]}")
        try:
            parsed = json.loads(raw[s:e])
        except json.JSONDecodeError:
            parsed = _lenient_json_parse(raw[s:e])
        parsed["_meta"] = {
            "elapsed_sec": round(elapsed, 2),
            "input_tokens": in_tok,
            "output_tokens": out_tok,
        }
        return parsed

    # ── Likert vote aggregation ────────────────────────────────────────────
    @staticmethod
    def _mode_likert(votes: list[str]) -> str:
        """Mode across passes. Tiebreak: pick the more pessimistic likert."""
        if not votes:
            return "inconclusive"
        # Filter valid only; exclude inconclusive from mode pool so it never wins
        # ties against real verdicts (it's a non-answer, not a midpoint).
        filt = [v for v in votes if v in VALID_LIKERTS and v != "inconclusive"]
        if not filt:
            return "inconclusive"
        counter = {}
        for v in filt:
            counter[v] = counter.get(v, 0) + 1
        max_count = max(counter.values())
        winners = [v for v, c in counter.items() if c == max_count]
        if len(winners) == 1:
            return winners[0]
        # Tiebreak: pick the worst (more conservative) outcome
        order = ["much_better", "better", "same", "worse", "much_worse", "broken"]
        for label in reversed(order):
            if label in winners:
                return label
        return winners[0]

    # ── Deterministic adjustments ──────────────────────────────────────────
    def _run_math_review(self, candidate_code: str, topic: str,
                         ground_truth: Optional[dict]) -> Optional[int]:
        """Use FinalJudge's Phase 1 prompt to score math_correctness 1–5."""
        if not candidate_code:
            return None
        try:
            from .final_judge import FinalJudge
            fj = FinalJudge(llm_client=self.llm)
            res = fj._analyze_code(candidate_code, topic, ground_truth=ground_truth)
            return res.get("math_score")
        except Exception as e:
            print(f"⚠️  [BenchmarkJudge] math review skipped: {e}")
            return None

    def _run_layout_audit(self, scene_state_log: Optional[str]) -> Optional[int]:
        """Use LayoutAuditor to get a 1–5 layout score."""
        if not scene_state_log or not os.path.exists(scene_state_log):
            return None
        try:
            from .layout_auditor import LayoutAuditor
            audit = LayoutAuditor().audit(scene_state_log)
            return audit.get("score_1_to_5")
        except Exception as e:
            print(f"⚠️  [BenchmarkJudge] layout audit skipped: {e}")
            return None

    # ── Score synthesis (pure Python, no LLM) ──────────────────────────────
    @staticmethod
    def _dim_score(likert_votes: list[str]) -> tuple[int, str]:
        """Return (per-dim 0–100 score, mode_likert)."""
        mode = BenchmarkJudge._mode_likert(likert_votes)
        offset = LIKERT_OFFSET.get(mode, -5)
        return max(0, min(100, 100 + offset)), mode

    @staticmethod
    def _layout_gap_to_clarity_penalty(
        cand_layout: Optional[int], bench_layout: Optional[int]
    ) -> int:
        """Negative gap (candidate worse) → negative penalty on clarity_score."""
        if cand_layout is None or bench_layout is None:
            return 0
        gap = cand_layout - bench_layout   # -4 .. +4
        return gap * 10                    # -40 .. +40 (cap below by 0)

    # ── Public entry point ─────────────────────────────────────────────────
    def judge(
        self,
        candidate_video: str,
        benchmark_video: str,
        question_topic: str,
        candidate_code: Optional[str] = None,
        candidate_state_log: Optional[str] = None,
        benchmark_state_log: Optional[str] = None,
        ground_truth: Optional[dict] = None,
        workdir: Optional[str] = None,
        cache_path: Optional[str] = None,
        force: bool = False,
        precomputed_math_score: Optional[int] = None,
    ) -> dict:
        """Score candidate against benchmark on 0–100 scale.

        Returns a dict (schema in design doc §6.2).

        Cache behaviour:
          - If `cache_path` is given and contains a hit for this
            (candidate, benchmark, topic, passes, model, prompt_sig) tuple,
            return it immediately (skips all Opus calls).
          - `force=True` bypasses lookup but still writes through on success.
          - Cache key folds in mtime+size of both videos AND a hash of the
            system prompt, so re-rendering a candidate OR editing the rubric
            auto-invalidates.

        Cost optimisation:
          - `precomputed_math_score` (1-5) lets caller supply a math_score
            already computed by FinalJudge in RefiningLoop, skipping the
            8-second extra Opus Phase-1 call. Falls back to running its own
            review if None.
        """
        for path, label in [(candidate_video, "candidate"), (benchmark_video, "benchmark")]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"{label} video not found: {path}")

        key = _cache_key(candidate_video, benchmark_video, question_topic,
                         self.passes, self.model, self._prompt_sig())
        if cache_path and not force:
            hit = _cache_load(cache_path, key)
            if hit is not None:
                print(f"💾 [BenchmarkJudge] cache HIT ({key}) — skipping {self.passes} passes")
                hit = dict(hit)
                hit["_cache"] = {"hit": True, "key": key, "path": cache_path}
                return hit

        workdir = workdir or tempfile.mkdtemp(prefix="bjudge_grids_", dir="/tmp")
        os.makedirs(workdir, exist_ok=True)
        try:
            os.chmod(workdir, 0o755)
        except OSError:
            pass

        # Cache video durations once per judge() (not once per pass).
        durations = {
            candidate_video: _ffprobe_duration(candidate_video),
            benchmark_video: _ffprobe_duration(benchmark_video),
        }

        print("\n" + "=" * 60)
        print(f"📐 [BenchmarkJudge] candidate vs benchmark | passes={self.passes}")
        print(f"   candidate:  {os.path.basename(candidate_video)}")
        print(f"   benchmark:  {os.path.basename(benchmark_video)}")
        print(f"   topic:      {question_topic[:60]}")
        print("=" * 60)

        # ── Pass loop with position swap ───────────────────────────────────
        # i even: candidate on TOP; i odd: candidate on BOTTOM.
        dim_votes = {"completeness": [], "accuracy": [], "clarity": []}
        # evidence_per_pass: [{"pass": 1, "tag": ..., "completeness": str, "accuracy": str, "clarity": str}, ...]
        # The pipe-joined `evidence` field is kept for back-compat.
        evidence_per_pass = []
        evidence  = {"completeness": [], "accuracy": [], "clarity": []}
        confidences = []
        passes_log = []

        for i in range(self.passes):
            cand_on_top = (i % 2 == 0)
            top_v, bot_v = (
                (candidate_video, benchmark_video) if cand_on_top
                else (benchmark_video, candidate_video)
            )
            tag = "cand@TOP" if cand_on_top else "cand@BOTTOM"
            grid_path = os.path.join(workdir, f"grid_pass{i+1}_{tag}.jpg")
            self._build_grid(top_v, bot_v, grid_path, durations=durations)

            cand_label = "TOP" if cand_on_top else "BOTTOM"
            bench_label = "BOTTOM" if cand_on_top else "TOP"
            user_prompt = (
                f"Task being taught: {question_topic}\n"
                f"In this grid: {cand_label} row = CANDIDATE, {bench_label} row = BENCHMARK.\n"
                f"Grid image path: {grid_path}\n"
                f"Use the Read tool on that path, then output the JSON per protocol."
            )

            print(f"\n→ Pass {i+1}/{self.passes} ({tag})")
            verdict = None
            last_err = None
            for attempt in range(2):
                try:
                    verdict = self._call_opus(grid_path, user_prompt)
                    break
                except Exception as e:
                    last_err = str(e)
                    print(f"   ⚠️ attempt {attempt+1} failed: {e}")
            if verdict is None:
                print(f"   ✗ pass failed after retry")
                passes_log.append({"pass": i+1, "tag": tag, "error": last_err})
                continue

            meta = verdict.pop("_meta", {})
            dims = verdict.get("dimensions", {}) or {}
            print(f"   ✓ {meta.get('elapsed_sec')}s | in={meta.get('input_tokens')} out={meta.get('output_tokens')}")
            pass_evidence = {"pass": i+1, "tag": tag}
            for dim in dim_votes:
                entry = dims.get(dim, {}) or {}
                l = str(entry.get("likert", "inconclusive")).strip().lower()
                if l not in VALID_LIKERTS:
                    l = "inconclusive"
                ev = str(entry.get("evidence", "")).strip()[:200]
                dim_votes[dim].append(l)
                evidence[dim].append(ev)
                pass_evidence[dim] = {"likert": l, "evidence": ev}
                print(f"     {dim:<13} likert={l}  evidence={ev[:60]}")
            evidence_per_pass.append(pass_evidence)
            confidences.append(verdict.get("confidence", "medium"))
            passes_log.append({
                "pass": i+1, "tag": tag, "raw": verdict, "meta": meta,
            })

        # ── #2: insufficient_passes guard ──────────────────────────────────
        # If majority of passes failed, do NOT synthesise a score — fewer than
        # half the planned votes makes the mode/tiebreak unreliable.
        n_ok = sum(1 for p in passes_log if "error" not in p)
        min_required = (self.passes + 1) // 2   # ceil(passes/2)
        if n_ok < min_required:
            print(f"\n⚠️  [BenchmarkJudge] only {n_ok}/{self.passes} passes succeeded "
                  f"(need ≥{min_required}) — returning insufficient_passes")
            insufficient = {
                "final_100":   None,
                "status":      "insufficient_passes",
                "scores":      None,
                "modes":       None,
                "likert_votes": dim_votes,
                "evidence":    {dim: " | ".join(ev) for dim, ev in evidence.items()},
                "evidence_per_pass": evidence_per_pass,
                "confidences": confidences,
                "passes":      passes_log,
                "n_successful_passes": n_ok,
                "candidate_video": candidate_video,
                "benchmark_video": benchmark_video,
            }
            if cache_path:
                # Do NOT write insufficient results to cache — we want a retry
                # to actually re-attempt rather than serve a sticky failure.
                insufficient["_cache"] = {"hit": False, "key": key, "path": cache_path,
                                          "written": False}
            return insufficient

        # ── Per-dim score (mode of likert votes) ───────────────────────────
        per_dim_scores = {}
        per_dim_modes = {}
        for dim, votes in dim_votes.items():
            score, mode = self._dim_score(votes)
            per_dim_scores[dim] = score
            per_dim_modes[dim] = mode

        # P1 guard: vision had no signal on accuracy (e.g. sampled frames missed
        # the key moments). Without this clamp, all-inconclusive votes ride
        # math_score=5 (penalty=0) to a free 100. Code review only checks code,
        # not whether the animation actually rendered the math.
        acc_votes = dim_votes.get("accuracy", [])
        inconclusive_ratio = (
            sum(1 for v in acc_votes if v == "inconclusive") / len(acc_votes)
            if acc_votes else 0.0
        )
        acc_insufficient_signal = inconclusive_ratio >= 0.8
        if acc_insufficient_signal:
            per_dim_scores["accuracy"] = min(per_dim_scores["accuracy"], 60)

        # ── Deterministic adjustments ──────────────────────────────────────
        # #1: skip the 8-second Opus Phase-1 if caller already has math_score
        # (e.g. RefiningLoop already ran FinalJudge on this candidate).
        if precomputed_math_score is not None:
            math_score = int(precomputed_math_score)
            print(f"   ↳ using precomputed math_score={math_score} (skipped Phase-1)")
        else:
            math_score = self._run_math_review(candidate_code, question_topic, ground_truth)
        cand_layout = self._run_layout_audit(candidate_state_log)
        bench_layout = self._run_layout_audit(benchmark_state_log)

        # Math penalty pushes accuracy down (additional cap)
        math_penalty = MATH_PENALTY.get(math_score, 0) if math_score is not None else 0
        if math_score is not None:
            new_accuracy = min(per_dim_scores["accuracy"], 100 + math_penalty)
            per_dim_scores["accuracy"] = max(0, new_accuracy)

        # Layout gap adjusts clarity
        layout_penalty = self._layout_gap_to_clarity_penalty(cand_layout, bench_layout)
        if layout_penalty:
            per_dim_scores["clarity"] = max(0, min(100,
                per_dim_scores["clarity"] + layout_penalty))

        # ── Final 100 with smooth accuracy gate ────────────────────────────
        weighted = sum(WEIGHTS[d] * per_dim_scores[d] for d in WEIGHTS)
        accuracy_factor = min(1.0, per_dim_scores["accuracy"] / ACCURACY_GATE_THRESHOLD)
        final_100 = round(weighted * accuracy_factor)
        final_100 = max(0, min(100, final_100))

        result = {
            "final_100": final_100,
            "status":    "ok",
            "scores": per_dim_scores,
            "modes": per_dim_modes,
            "likert_votes": dim_votes,
            "evidence": {dim: " | ".join(ev) for dim, ev in evidence.items()},
            "evidence_per_pass": evidence_per_pass,
            "deterministic": {
                "math_score":    math_score,
                "math_penalty":  math_penalty,
                "cand_layout":   cand_layout,
                "bench_layout":  bench_layout,
                "layout_gap_penalty": layout_penalty,
                "accuracy_factor": round(accuracy_factor, 3),
                "acc_inconclusive_ratio": round(inconclusive_ratio, 3),
                "acc_insufficient_signal": acc_insufficient_signal,
            },
            "confidences": confidences,
            "passes": passes_log,
            "n_successful_passes": len([p for p in passes_log if "error" not in p]),
            "candidate_video": candidate_video,
            "benchmark_video": benchmark_video,
        }

        print(f"\n{'='*60}")
        print(f"📐 [BenchmarkJudge] FINAL = {final_100}/100")
        for dim, w in WEIGHTS.items():
            print(f"   {dim:<13} {per_dim_scores[dim]:>3}  (mode={per_dim_modes[dim]}, weight={w})")
        if math_score is not None:
            print(f"   math_review:  {math_score}/5  → penalty {math_penalty}")
        if cand_layout is not None and bench_layout is not None:
            print(f"   layout gap:   cand={cand_layout} bench={bench_layout}  → clarity adj {layout_penalty:+d}")
        if acc_insufficient_signal:
            print(f"   ⚠️  acc insufficient signal: inconclusive_ratio={inconclusive_ratio:.0%} → acc clamped to ≤60")
        print(f"   accuracy_factor: {accuracy_factor:.2f}  (= min(1, acc/{ACCURACY_GATE_THRESHOLD}))")
        print(f"{'='*60}\n")

        if cache_path:
            try:
                _cache_save(cache_path, key, result)
                result["_cache"] = {"hit": False, "key": key, "path": cache_path}
            except OSError as e:
                print(f"⚠️  [BenchmarkJudge] cache save failed: {e}")

        return result
