"""
Opus-only runner: Planner → single Coder call → single render.
No RAG, no VisionQA, no Reflexion.
Prints structured markers:  [STAGE] label|percent  [VIDEO] url  [PLANNER_JSON] {...}  [CODE] N
"""
import concurrent.futures
import json
import os
import re
import shutil
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
    task_id = sys.argv[1] if len(sys.argv) > 1 else "opus_task"
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "exhibition" / "static" / "runs" / task_id
    out_dir.mkdir(parents=True, exist_ok=True)

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

    # ── Planner ────────────────────────────────────────────────────────
    _emit("STAGE", "planner|15")
    from agents.planner.planner import Planner
    try:
        script_json_str, _ = Planner(llm_client=llm).plan_script_from_prompt(topic_en)
    except Exception as e:
        _emit("ERROR", f"Planner: {e}")
        sys.exit(1)

    clean = re.sub(r"<[^>]+>.*?</[^>]+>", "", script_json_str, flags=re.DOTALL).strip()
    try:
        script_obj = json.loads(clean)
    except Exception:
        i = clean.find("{")
        script_obj = json.loads(clean[i: clean.rfind("}") + 1]) if i >= 0 else {"title": topic_en}
    _emit("PLANNER_JSON", json.dumps(script_obj, ensure_ascii=False))
    _emit("STAGE", "planner_done|30")

    # ── Audio (parallel with Coder) ────────────────────────────────────
    sequence_data = script_obj.get("sequence") or script_obj.get("scenes") or []
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def _audio_task():
        if not sequence_data:
            return None, None
        try:
            from agents.utils.audio_engine import AudioEngine
            eng = AudioEngine(output_dir=str(out_dir / "media" / "audio"), topic=topic_en)
            return eng.generate_narration(sequence_data)
        except Exception as e:
            _emit("LOG", f"AudioEngine skipped: {e}")
            return None, None

    audio_future = executor.submit(_audio_task)

    # ── Single Coder (no RAG) ─────────────────────────────────────────
    _emit("STAGE", "coder|35")
    from agents.coder.prompter import CoderPrompter
    sys_p, usr_p = CoderPrompter().generate_initial_prompt(
        script_json=script_json_str,
        target_scene=SCENE_NAME,
        rag_context="",
    )
    code_raw = llm.ask(sys_p, usr_p, role="coder")
    code = LLMClient.extract_code(code_raw)
    _emit("CODE", f"{len(code)}")
    _emit("STAGE", "coder_done|60")

    # ── Inject audio ──────────────────────────────────────────────────
    try:
        updated_sequence, final_audio_path = audio_future.result(timeout=90)
    except Exception:
        updated_sequence, final_audio_path = None, None
        _emit("LOG", "Audio skipped (timeout or error)")
    executor.shutdown(wait=False)
    if updated_sequence is not None:
        try:
            from exhibition.audio_inject import inject_audio_sync
            code = inject_audio_sync(code, updated_sequence, final_audio_path)
            _emit("LOG", "Audio injection complete")
        except Exception as e:
            _emit("LOG", f"Audio injection skipped: {e}")

    # Apply zero-cost deterministic patches
    from agents.orchestrator.refining_loop import RefiningLoop
    code = RefiningLoop.pre_render_patch(code)

    # Replace any remaining undefined _audio_dur_N variables
    code = re.sub(r'\b_audio_dur_\d+\b', '2.0', code)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(code)

    # ── Single render (no Reflexion) ──────────────────────────────────
    _emit("STAGE", "render|65")
    render_result = RefiningLoop.run_manim_task(TARGET_FILE, SCENE_NAME)
    render_ok = render_result[0]
    render_err = render_result[1] if len(render_result) > 1 else ""

    if render_ok:
        script_stem = Path(TARGET_FILE).stem
        media_mp4 = ROOT / "media" / "videos" / script_stem / "480p15" / f"{SCENE_NAME}.mp4"
        dest = out_dir / "video.mp4"
        if media_mp4.exists():
            shutil.copy2(str(media_mp4), str(dest))
        _emit("VIDEO", f"/static/runs/{task_id}/video.mp4")
        _emit("STAGE", "done|100")
        sys.exit(0)
    else:
        err_lines = [l for l in str(render_err).splitlines() if "Error" in l or "error" in l]
        short_err = err_lines[-1].strip() if err_lines else str(render_err)[:200]
        _emit("RENDER_ERROR", short_err)
        _emit("STAGE", "failed|100")
        sys.exit(1)


if __name__ == "__main__":
    main()
