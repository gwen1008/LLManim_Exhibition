"""Full-system Lite runner — uses PlannerLite for aesthetic-first generation.

Same pipeline as full_system_runner.py BUT:
  - Uses PlannerLite (relaxed constraints)
  - All other agents unchanged (Coder, AudioEngine, RefiningLoop, FinalJudge)

Goal: see if loosening the Planner gives us better-looking videos.
"""
import concurrent.futures
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

TARGET_FILE = os.environ.get("TASK_TARGET_FILE", str(ROOT / "test_script.py"))
SCENE_NAME = "GeneratedScene"


def _emit(tag: str, payload: str):
    print(f"[{tag}] {payload}", flush=True)


def main():
    topic = sys.stdin.readline().strip()
    task_id = sys.argv[1] if len(sys.argv) > 1 else "lite_task"
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "exhibition" / "static" / "runs" / task_id
    out_dir.mkdir(parents=True, exist_ok=True)

    os.environ["EVAL_OUTPUT_DIR"] = str(out_dir)

    from agents.core.llm_client import LLMClient
    llm = LLMClient()

    # ── Translate ──────────────────────────────────────────────────────
    _emit("STAGE", "translate|5")
    try:
        from agents.orchestrator.translator import AcademicTranslator
        topic_en = AcademicTranslator(llm_client=llm).translate_to_english(topic)
    except Exception:
        topic_en = topic
    _emit("LOG", f"Topic: {topic_en}")

    # ── RAG (parallel) ────────────────────────────────────────────────
    _emit("STAGE", "rag|10")
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

    def _rag():
        try:
            from agents.core.rag_retriever import RAGRetriever
            r = RAGRetriever()
            ctx = r.format_for_prompt(r.retrieve_examples(topic_en, limit=2) + r.retrieve_rules(topic_en, limit=2))
            r.close()
            return ctx
        except Exception:
            return ""

    rag_future = executor.submit(_rag)

    # ── Planner Lite ───────────────────────────────────────────────────
    _emit("STAGE", "planner|15")
    from agents.planner.planner_lite import PlannerLite
    try:
        script_json_str, _ = PlannerLite(llm_client=llm).plan_script_from_prompt(topic_en)
    except Exception as e:
        _emit("ERROR", f"PlannerLite: {e}")
        sys.exit(1)

    clean = re.sub(r"<[^>]+>.*?</[^>]+>", "", script_json_str, flags=re.DOTALL).strip()
    try:
        script_obj = json.loads(clean)
    except Exception:
        i = clean.find("{")
        script_obj = json.loads(clean[i: clean.rfind("}") + 1]) if i >= 0 else {"title": topic_en}
    _emit("PLANNER_JSON", json.dumps(script_obj, ensure_ascii=False))
    _emit("STAGE", "planner_done|25")

    rag_ctx = rag_future.result()
    _emit("STAGE", "rag_done|28")

    # ── Audio (parallel with Coder) ────────────────────────────────────
    sequence_data = script_obj.get("sequence") or script_obj.get("scenes") or []

    def _audio_task():
        if not sequence_data:
            return None, None
        try:
            from agents.utils.audio_engine import AudioEngine
            audio_engine = AudioEngine(
                output_dir=str(out_dir / "media" / "audio"),
                topic=topic_en,
            )
            return audio_engine.generate_narration(sequence_data)
        except Exception as e:
            _emit("LOG", f"AudioEngine skipped: {e}")
            return None, None

    audio_future = executor.submit(_audio_task)

    # ── Coder (with Lite directive appended to user prompt) ──────────
    _emit("STAGE", "coder|35")
    from agents.coder.prompter import CoderPrompter
    sys_p, usr_p = CoderPrompter().generate_initial_prompt(
        script_json=script_json_str,
        target_scene=SCENE_NAME,
        rag_context=rag_ctx,
    )
    # Lite directive: override default "animate-then-wait" pattern with density
    lite_directive = """

═══════════════════════════════════════════════════════════════════
🎬 LITE MODE — OVERRIDES (READ FIRST, THIS TAKES PRECEDENCE)
═══════════════════════════════════════════════════════════════════
⚠️ This run uses Planner Lite. THREE rules in the system prompt above are
OVERRIDDEN (system prompt rules NOT marked here remain in force):

  OVERRIDE #1 — Audio sync pattern (replaces "AUDIO SYNCHRONIZATION" example):
    OLD: anim_time = 1.5; play(...); wait(_audio_dur_N - 1.5)
    NEW: play(..., run_time=_audio_dur_N); wait(0.1)

  OVERRIDE #2 — Step internal grouping (replaces "ANIMATION RHYTHM RULES"
                guidance about separating logical steps into multiple play calls):
    Within ONE step, even if the `details` field describes multiple distinct
    logical actions (e.g. "draw axes, write label, fill area"), wrap them ALL
    in ONE LaggedStart inside a SINGLE self.play() so the entire step fills
    one `_audio_dur_N` window with continuous animation.

  OVERRIDE #3 — lag_ratio range:
    Use lag_ratio in [0.15, 0.35] (a bit wider than the default 0.1-0.2).

CANONICAL PATTERN — copy this structure for every step:

    # Step N
    anim_time_N = _audio_dur_N    # use full audio duration, no shortening
    self.play(
        LaggedStart(
            <anim_a>, <anim_b>, <anim_c>, <anim_d>,
            lag_ratio=0.25,
            run_time=anim_time_N,
        )
    )
    self.wait(0.1)   # minimal padding only

CONTINUOUS-DYNAMICS PATTERN (when `details` mentions smooth change of a
parameter, e.g. "rectangles subdividing from 4 to 32"):

    # Step N — single continuous transition
    n_tracker = ValueTracker(4)

    def _build_rects():
        n = int(n_tracker.get_value())
        # YOU must implement the construction logic inline here.
        # Do NOT call an undefined helper like make_rectangles().
        dx = PI / n
        return VGroup(*[
            Rectangle(width=dx, height=np.sin(i*dx),
                      fill_color=BLUE, fill_opacity=0.5, stroke_width=1)
                .move_to(axes.c2p(i*dx + dx/2, np.sin(i*dx)/2))
            for i in range(n)
        ])

    rects = always_redraw(_build_rects)
    self.add(rects)
    self.play(n_tracker.animate.set_value(32), run_time=_audio_dur_N)
    self.wait(0.1)

NOTES on parsing `details`:
  - If details lists time slices like "(a) 0.8s, (b) 0.5s, (c) 2s", those
    numbers are RELATIVE RATIOS — actual run_time is anchored to _audio_dur_N
    and LaggedStart distributes timing internally via lag_ratio.
  - If details says "rich label sequence", choose 3-5 visual events that
    illustrate the step's narrative.

SubtitleManager and Step formatting (`# Step N` comment) remain MANDATORY
exactly as in the system prompt above.
"""
    first_code = llm.ask(sys_p, usr_p + lite_directive, role="coder")
    first_code = LLMClient.extract_code(first_code)
    _emit("CODE", f"{len(first_code)}")
    _emit("STAGE", "coder_done|50")

    # ── Inject audio ─────────────────────────────────────────────────
    try:
        updated_sequence, final_audio_path = audio_future.result(timeout=90)
    except Exception:
        updated_sequence, final_audio_path = None, None
        _emit("LOG", "Audio skipped (timeout or error)")
    executor.shutdown(wait=False)
    if updated_sequence is not None:
        try:
            from exhibition.audio_inject import inject_audio_sync
            first_code = inject_audio_sync(first_code, updated_sequence, final_audio_path)
            _emit("LOG", "Audio injection complete")
        except Exception as e:
            _emit("LOG", f"Audio injection skipped: {e}")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(first_code)

    # ── Reflexion ────────────────────────────────────────────────────
    _emit("STAGE", "refining|55")
    from agents.orchestrator.refining_loop_types import run_fix_loop
    try:
        loop_result = run_fix_loop(
            TARGET_FILE, SCENE_NAME, topic_en, script_json_str,
            llm_client=llm, backup_filename_prefix=topic,
        )
    except Exception as e:
        _emit("ERROR", f"RefiningLoop: {e}")
        sys.exit(1)

    video_path = loop_result.video_path
    _counters = getattr(loop_result, "counters_final", {}) or {}
    _emit("SYS_ITERATIONS", str(_counters.get("main_i", "")))
    _emit("SYS_BEST_EFFORT", "1" if getattr(loop_result, "is_best_effort", False) else "0")
    _emit("STAGE", f"refining_done|80")

    # ── FinalJudge ───────────────────────────────────────────────────
    bj_score = None
    vision_verdict = None
    if video_path and os.path.exists(str(video_path)):
        _emit("STAGE", "judge|85")
        try:
            from agents.utils.final_judge import FinalJudge
            with open(TARGET_FILE, encoding="utf-8") as f:
                final_code = f.read()
            fj_result = FinalJudge(llm_client=llm).judge(str(video_path), script_json_str, final_code)
            bj_score = fj_result.get("weighted_total")
            verdict = fj_result.get("verdict", "UNKNOWN")
            vision_verdict = {"verdict": verdict, "issues": fj_result.get("code_issues", [])}
            _emit("VISION_VERDICT", json.dumps(vision_verdict))
            _emit("BJ_SCORE", str(bj_score))
        except Exception as e:
            _emit("LOG", f"FinalJudge skipped: {e}")

    if video_path and os.path.exists(str(video_path)):
        import shutil
        dest = out_dir / "video.mp4"
        shutil.copy2(str(video_path), str(dest))
        _emit("VIDEO", f"/static/runs/{task_id}/video.mp4")
        _emit("STAGE", "done|100")
        sys.exit(0)
    else:
        _emit("STAGE", "failed|100")
        sys.exit(1)


if __name__ == "__main__":
    main()
