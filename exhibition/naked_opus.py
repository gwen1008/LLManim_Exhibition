"""Naked Opus runner — true zero-shot baseline.

跟 opus_only.py 的差別：
- ❌ 不跑 Translator
- ❌ 不跑 Planner（沒有 JSON 藍圖）
- ❌ 不用 OPUS_CODER_SYSTEM_PART（沒有 6 條 manim 規則）
- ❌ 不注入 audio
- ❌ 不用 SubtitleManager scaffolding
- ✅ 只給 Opus 最小可運行的 prompt：用戶原始 topic + 「寫一個 Manim 場景」

這才是 fair 的 zero-shot baseline，呈現 LLM 在「沒有系統工程」加持下的真實能力。
"""
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

TARGET_FILE = os.environ.get("TASK_TARGET_FILE", str(ROOT / "test_script.py"))
SCENE_NAME = "GeneratedScene"


NAKED_SYSTEM_PROMPT = """Write a complete ManimCE Python file that animates the given math topic.
Output only valid Python — no markdown, no explanations.
The scene class must be named `GeneratedScene(Scene)`."""


def _emit(tag: str, payload: str):
    print(f"[{tag}] {payload}", flush=True)


def main():
    topic = sys.stdin.readline().strip()
    task_id = sys.argv[1] if len(sys.argv) > 1 else "naked_task"
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "exhibition" / "static" / "runs" / task_id
    out_dir.mkdir(parents=True, exist_ok=True)

    _emit("LOG", f"Topic: {topic}")
    _emit("STAGE", "coder|20")

    from agents.core.llm_client import LLMClient
    llm = LLMClient()

    # 唯一一次 LLM 呼叫：給用戶原始 topic + 最小規則
    user_prompt = topic
    code_raw = llm.ask(NAKED_SYSTEM_PROMPT, user_prompt, role="coder")
    code = LLMClient.extract_code(code_raw)
    _emit("CODE", f"{len(code)}")
    _emit("STAGE", "coder_done|60")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(code)

    # 渲染（無 pre_render_patch、無 retry — 真的就是裸跑）
    _emit("STAGE", "render|65")
    from agents.orchestrator.refining_loop import RefiningLoop
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
