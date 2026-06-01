"""
PairwiseJudge — Compare a candidate animation against a benchmark animation.

Uses Claude Opus 4.7 via the Claude Code CLI (subscription quota), which can
Read local image files. We build a 2-row labeled comparison grid (top row =
candidate, bottom row = benchmark) and ask Opus to judge across three
dimensions, with self-consistency over multiple passes and position swapping
to neutralize position bias.

Designed for the RAG-150 three-way experiment (A vs C, B vs C). The "C"
(benchmark) side is always the reference; the candidate side rotates.
"""
import os
import re
import json
import shutil
import subprocess
import tempfile
import time
from typing import Optional


def _lenient_json_parse(text: str) -> dict:
    """Parse JSON tolerantly: handles trailing commas + // comments."""
    text = re.sub(r",(\s*[}\]])", r"\1", text)        # trailing commas
    text = re.sub(r"//[^\n]*", "", text)              # line comments
    return json.loads(text)


def _ffprobe_duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, timeout=10
    ).stdout.strip()
    return float(out)


def _extract_frame(video: str, ts: float, out_path: str, w: int, h: int) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-ss", f"{ts:.2f}", "-i", video,
         "-frames:v", "1", "-vf", f"scale={w}:{h}", out_path],
        capture_output=True, timeout=20
    )


def build_comparison_grid(
    top_video: str,
    bottom_video: str,
    out_path: str,
    sample_pcts=(0.15, 0.38, 0.62, 0.88),
    tile_w: int = 480,
    tile_h: int = 270,
    durations: Optional[dict] = None,
    tmpdir_prefix: str = "judge_tiles_",
    tmpdir_dir: Optional[str] = None,
) -> str:
    """Build a 2×N labeled comparison grid (top = T1..TN, bottom = D1..DN).

    Shared by PairwiseJudge and BenchmarkJudge. `durations` is an optional
    {video_path: duration_sec} cache so callers can avoid double ffprobe across
    multiple passes on the same pair. Writes JPEG to out_path with mode 0o644
    so a different-user subprocess (e.g. `sudo -u claudealt` Opus CLI) can Read it.
    """
    from PIL import Image, ImageDraw, ImageFont

    durations = durations or {}
    dur_t = durations.get(top_video) or _ffprobe_duration(top_video)
    dur_b = durations.get(bottom_video) or _ffprobe_duration(bottom_video)
    ts_t = [dur_t * p for p in sample_pcts]
    ts_b = [dur_b * p for p in sample_pcts]

    mk_kwargs = {"prefix": tmpdir_prefix}
    if tmpdir_dir is not None:
        mk_kwargs["dir"] = tmpdir_dir
    tmpdir = tempfile.mkdtemp(**mk_kwargs)
    try:
        tiles = []
        for i, ts in enumerate(ts_t):
            p = os.path.join(tmpdir, f"t{i}.jpg")
            _extract_frame(top_video, ts, p, tile_w, tile_h)
            tiles.append((f"T{i+1}", p))
        for i, ts in enumerate(ts_b):
            p = os.path.join(tmpdir, f"d{i}.jpg")
            _extract_frame(bottom_video, ts, p, tile_w, tile_h)
            tiles.append((f"D{i+1}", p))

        cols = len(sample_pcts)
        rows = 2
        canvas = Image.new("RGB", (cols * tile_w, rows * tile_h), "black")
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        except Exception:
            font = ImageFont.load_default()
        draw = ImageDraw.Draw(canvas)
        for idx, (label, path) in enumerate(tiles):
            if not os.path.exists(path):
                continue
            tile = Image.open(path).convert("RGB")
            x = (idx % cols) * tile_w
            y = (idx // cols) * tile_h
            canvas.paste(tile, (x, y))
            draw.rectangle((x + 5, y + 5, x + 85, y + 52), fill=(0, 0, 0))
            draw.text((x + 14, y + 9), label, fill="yellow", font=font)
        canvas.save(out_path, "JPEG", quality=88)
        try:
            os.chmod(out_path, 0o644)
        except OSError:
            pass
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    return out_path


class PairwiseJudge:
    # 4 frames per side at 15/38/62/88% of duration
    SAMPLE_PCTS = (0.15, 0.38, 0.62, 0.88)
    TILE_W = 480
    TILE_H = 270

    DEFAULT_PASSES = 3
    DEFAULT_MODEL = "claude-opus-4-8"

    _SYSTEM = """You are an expert judge for AI-generated math educational animations.
You compare TWO candidate animations attempting the SAME math task, given only
static sampled frames. Be epistemically careful: frames cannot reveal animation
pacing, narration, or transitions — say so when relevant.

You MUST use the Read tool to open the provided comparison-grid image file.

The grid is 2 rows × 4 columns:
- TOP row labeled (T1, T2, T3, T4)    = "TOP" candidate, chronological left→right
- BOTTOM row labeled (D1, D2, D3, D4) = "BOTTOM" candidate (D = down), chronological left→right

Each tile has its label in a yellow box at the top-left corner.

Compare across THREE dimensions. For each, choose winner ∈ {TOP, BOTTOM, tie}:

1. math_correctness — Are the displayed numbers, signs, intermediate steps,
   and final answer mathematically correct? Use the [GROUND TRUTH] block if
   provided to verify. Penalize wrong values, missing steps, or misleading math.

2. visual_clarity — Layout quality, no overlap, no off-screen elements,
   text readable at a glance. Penalize crowding, occlusion, off-canvas content.

3. concept_alignment — Does the visual help a learner understand the task?
   Reward clear visual metaphors and canonical step ordering. Penalize
   confusing or non-canonical presentations.

Then pick overall_winner (default to the dimension consensus; "tie" if mixed).

Output ONLY a single JSON object, no preamble, no markdown fence:
{
  "frame_inventory_TOP":    "1-2 sentences on what T1..T4 show overall",
  "frame_inventory_BOTTOM": "1-2 sentences on what D1..D4 show overall",
  "dimensions": {
    "math_correctness":  {"winner": "TOP" | "BOTTOM" | "tie", "reason": "..."},
    "visual_clarity":    {"winner": "TOP" | "BOTTOM" | "tie", "reason": "..."},
    "concept_alignment": {"winner": "TOP" | "BOTTOM" | "tie", "reason": "..."}
  },
  "overall_winner": "TOP" | "BOTTOM" | "tie",
  "confidence": "low" | "medium" | "high",
  "notes": "anything frames alone cannot determine"
}"""

    def __init__(self, llm_client=None,
                 passes: Optional[int] = None,
                 model: Optional[str] = None):
        from ..core.llm_client import LLMClient
        self.llm = llm_client if llm_client else LLMClient()
        self.passes = passes if passes is not None else int(os.getenv("PAIRWISE_JUDGE_PASSES", self.DEFAULT_PASSES))
        self.passes = max(1, min(self.passes, 5))
        self.model = model or os.getenv("PAIRWISE_JUDGE_MODEL", self.DEFAULT_MODEL)
        self._claude_bin = (
            os.getenv("CLAUDE_BIN") or shutil.which("claude") or "/Users/liaozhenting/.local/bin/claude"
        )
        # Empty default: claudealt was retired 2026-05-23 (keychain locked).
        self._run_as = os.getenv("CLAUDE_RUN_AS_USER", "")

    # ──────────────────────────────────────────────────────────────────────
    # Grid construction (delegates to module-level build_comparison_grid)
    # ──────────────────────────────────────────────────────────────────────
    def _build_grid(self, top_video: str, bottom_video: str, out_path: str) -> str:
        return build_comparison_grid(
            top_video, bottom_video, out_path,
            sample_pcts=self.SAMPLE_PCTS,
            tile_w=self.TILE_W, tile_h=self.TILE_H,
            tmpdir_prefix="pwj_",
        )

    # ──────────────────────────────────────────────────────────────────────
    # Single judgement call (CLI subprocess)
    # ──────────────────────────────────────────────────────────────────────
    def _call_opus_read(self, grid_path: str, user_prompt: str) -> dict:
        """One Opus pass via Claude Code CLI. Returns parsed JSON dict."""
        cmd_inner = [
            self._claude_bin, "-p", user_prompt.strip(),
            "--model", self.model,
            "--output-format", "json",
            "--effort", "medium",
            "--no-session-persistence",
            "--tools", "Read",
            "--add-dir", os.path.dirname(grid_path),
            "--system-prompt", self._SYSTEM,
            "--strict-mcp-config",
            "--disable-slash-commands",
        ]
        cmd = (["sudo", "-u", self._run_as, "-i"] + cmd_inner) if self._run_as else cmd_inner

        start = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        elapsed = time.time() - start
        if r.returncode != 0:
            raise RuntimeError(f"claude CLI failed: {r.stderr.strip()[-500:]}")
        data = json.loads(r.stdout)

        usage = data.get("usage", {})
        c_read = usage.get("cache_read_input_tokens", 0)
        c_create = usage.get("cache_creation_input_tokens", 0)
        in_tok = usage.get("input_tokens", 0) + c_read + c_create
        out_tok = usage.get("output_tokens", 0)
        self.llm._update_stats(f"anthropic/{self.model}", in_tok, out_tok)

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
            "num_turns": data.get("num_turns"),
            "input_tokens": in_tok,
            "cache_read": c_read,
            "output_tokens": out_tok,
        }
        return parsed

    # ──────────────────────────────────────────────────────────────────────
    # Vote aggregation across passes
    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def _flip_winner(w: str, candidate_on_top: bool) -> str:
        """Convert TOP/BOTTOM verdict back to candidate/benchmark space."""
        if w == "tie":
            return "tie"
        if candidate_on_top:
            return "candidate" if w == "TOP" else "benchmark"
        return "candidate" if w == "BOTTOM" else "benchmark"

    @staticmethod
    def _majority(votes: list[str]) -> str:
        votes = [v for v in votes if v]
        if not votes:
            return "tie"
        counts = {v: votes.count(v) for v in set(votes)}
        top = max(counts.values())
        winners = [k for k, v in counts.items() if v == top]
        if len(winners) == 1:
            return winners[0]
        # Tie in vote count between candidate and benchmark → "tie"
        if "candidate" in winners and "benchmark" in winners:
            return "tie"
        return winners[0]

    # ──────────────────────────────────────────────────────────────────────
    # Public entry
    # ──────────────────────────────────────────────────────────────────────
    def compare(self, candidate_video: str, benchmark_video: str,
                task_context: str = "",
                ground_truth: dict | None = None,
                workdir: str | None = None) -> dict:
        """
        Compare candidate vs benchmark.

        Args:
            candidate_video: path to .mp4 under evaluation (A or B variant)
            benchmark_video: path to the C-group reference .mp4
            task_context:    one-line task description (Planner topic or question text)
            ground_truth:    optional {"answer": "...", "solution": "..."}
            workdir:         where to write grid images (default: temp dir)

        Returns:
            dict with:
              winner ∈ {candidate, benchmark, tie}
              dim_winners: {math_correctness, visual_clarity, concept_alignment}
              confidence_summary: mean confidence
              passes: list of per-pass raw verdicts (after un-flipping to candidate/benchmark)
              tokens: aggregated token usage
        """
        if not os.path.exists(candidate_video):
            raise FileNotFoundError(f"candidate_video not found: {candidate_video}")
        if not os.path.exists(benchmark_video):
            raise FileNotFoundError(f"benchmark_video not found: {benchmark_video}")

        # Write grid images under /tmp (world-readable) so the Opus subprocess
        # running as a different user via `sudo -u claudealt` can Read them.
        # mkdtemp default location is /var/folders/...T/ with mode 0o700 which
        # blocks cross-user access (EACCES). See agents/utils/final_judge.py
        # for the same fix.
        workdir = workdir or tempfile.mkdtemp(prefix="pwj_grids_", dir="/tmp")
        os.makedirs(workdir, exist_ok=True)
        os.chmod(workdir, 0o755)

        print("\n" + "=" * 50)
        print(f"⚖️  [PairwiseJudge] candidate vs benchmark | passes={self.passes} | model={self.model}")
        print(f"   candidate:  {os.path.basename(candidate_video)}")
        print(f"   benchmark:  {os.path.basename(benchmark_video)}")
        print("=" * 50)

        # GROUND TRUTH block
        gt_block = ""
        if ground_truth:
            ans = ground_truth.get("answer") or ""
            sol = ground_truth.get("solution") or ""
            if ans or sol:
                gt_block = "\n**[GROUND TRUTH]**\n"
                if ans:
                    gt_block += f"Correct answer: {ans}\n"
                if sol:
                    gt_block += f"Solution steps:\n{str(sol)[:800]}\n"

        # Schedule passes with alternating positions to neutralize bias.
        # Pass i: candidate on TOP if i even, on BOTTOM if i odd.
        passes_log = []
        dim_votes = {"math_correctness": [], "visual_clarity": [], "concept_alignment": []}
        overall_votes = []
        confidences = []

        for i in range(self.passes):
            candidate_on_top = (i % 2 == 0)
            top_video, bottom_video = (
                (candidate_video, benchmark_video) if candidate_on_top
                else (benchmark_video, candidate_video)
            )
            position_tag = "cand@TOP" if candidate_on_top else "cand@BOTTOM"
            grid_path = os.path.join(workdir, f"grid_pass{i+1}_{position_tag}.jpg")
            self._build_grid(top_video, bottom_video, grid_path)

            user_prompt = (
                f"Task being animated: {task_context}\n{gt_block}\n"
                f"Read the image at {grid_path} and produce the comparison JSON "
                f"per the protocol. Be specific about which frame(s) support each claim."
            )

            print(f"\n→ Pass {i+1}/{self.passes} ({position_tag})")
            verdict = None
            last_err = None
            for attempt in range(2):
                try:
                    verdict = self._call_opus_read(grid_path, user_prompt)
                    break
                except Exception as e:
                    last_err = str(e)
                    print(f"   ⚠️ attempt {attempt+1} failed: {e}")
            if verdict is None:
                print(f"   ✗ pass failed after retry")
                passes_log.append({"pass": i + 1, "position": position_tag, "error": last_err})
                continue

            meta = verdict.pop("_meta", {})
            print(f"   ✓ {meta.get('elapsed_sec')}s | "
                  f"in={meta.get('input_tokens')} cache={meta.get('cache_read')} out={meta.get('output_tokens')} | "
                  f"overall(raw)={verdict.get('overall_winner')}")

            # Un-flip winners back into candidate/benchmark space
            flipped = {"pass": i + 1, "position": position_tag, "meta": meta, "raw": verdict}
            for dim in dim_votes:
                w = (verdict.get("dimensions") or {}).get(dim, {}).get("winner", "tie")
                flipped_w = self._flip_winner(w, candidate_on_top)
                dim_votes[dim].append(flipped_w)
                flipped.setdefault("dim_winners", {})[dim] = flipped_w
            overall_w = self._flip_winner(verdict.get("overall_winner", "tie"), candidate_on_top)
            overall_votes.append(overall_w)
            flipped["overall_winner"] = overall_w
            confidences.append(verdict.get("confidence", "medium"))
            passes_log.append(flipped)

        # Aggregate
        result = {
            "winner": self._majority(overall_votes),
            "dim_winners": {dim: self._majority(votes) for dim, votes in dim_votes.items()},
            "vote_breakdown": {
                "overall": overall_votes,
                **{dim: votes for dim, votes in dim_votes.items()},
            },
            "confidences": confidences,
            "passes": passes_log,
            "n_successful_passes": len([p for p in passes_log if "error" not in p]),
            "candidate_video": candidate_video,
            "benchmark_video": benchmark_video,
        }

        # Summary print
        print(f"\n{'=' * 50}")
        print(f"⚖️  [PairwiseJudge] FINAL  → winner: {result['winner']}")
        for dim, w in result["dim_winners"].items():
            print(f"   {dim:>20}: {w}  (votes: {dim_votes[dim]})")
        print(f"   overall votes: {overall_votes}")
        print(f"   passes succeeded: {result['n_successful_passes']}/{self.passes}")
        print(f"{'=' * 50}\n")

        return result
