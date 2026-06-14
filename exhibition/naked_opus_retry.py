"""Naked Opus + naive retry runner — 記錄「opus 重跑幾次才成功」。

跟 naked_opus.py 的差別：
- ✅ 保留同樣的最小 zero-shot prompt（無 Planner/RAG/lint/audio）
- ✅ 加「餵錯誤 retry」迴圈：render 失敗就把 error 餵回 opus 叫它修，上限 5 次
- ✅ emit [ATTEMPTS] N 與 [FINAL] OK/FAIL，供統計「第幾次才成功 / N 次仍失敗」

設計目的：跟本系統 RefiningLoop（同樣 5 次上限、會看錯誤修）對齊條件，
讓對比落在「即使給 opus 同樣的 retry 能力，它仍要 N 次（或仍崩），
而系統靠 Planner+RAG+lint 一次就過」。這是公平且誠實的對照。
"""
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

TARGET_FILE = os.environ.get("TASK_TARGET_FILE", str(ROOT / "test_script.py"))
SCENE_NAME = "GeneratedScene"
MAX_RETRIES = int(os.environ.get("NAKED_MAX_RETRIES", "5"))

NAKED_SYSTEM_PROMPT = """Write a complete ManimCE Python file that animates the given math topic.
Output only valid Python — no markdown, no explanations.
The scene class must be named `GeneratedScene(Scene)`."""

# retry 時的修正 prompt：只給「上次代碼 + render 錯誤」，不給任何 manim know-how
FIX_SYSTEM_PROMPT = """The ManimCE code you wrote failed to render. Fix it.
Output only the complete corrected Python file — no markdown, no explanations.
The scene class must be named `GeneratedScene(Scene)`."""


def _emit(tag: str, payload: str):
    print(f"[{tag}] {payload}", flush=True)


def main():
    topic = sys.stdin.readline().strip()
    task_id = sys.argv[1] if len(sys.argv) > 1 else "naked_retry_task"
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "exhibition" / "static" / "runs" / task_id
    out_dir.mkdir(parents=True, exist_ok=True)

    _emit("LOG", f"Topic: {topic}")

    from agents.core.llm_client import LLMClient
    from agents.orchestrator.refining_loop import RefiningLoop
    llm = LLMClient()

    code = ""
    last_err = ""
    success_attempt = None  # 第幾次成功（1-based），None = 全失敗

    for attempt in range(1, MAX_RETRIES + 1):
        _emit("STAGE", f"attempt_{attempt}|{int(attempt / MAX_RETRIES * 90)}")
        _emit("LOG", f"=== Attempt {attempt}/{MAX_RETRIES} ===")

        if attempt == 1:
            code_raw = llm.ask(NAKED_SYSTEM_PROMPT, topic, role="coder")
        else:
            # 餵：原題 + 上次代碼 + render 錯誤，叫 opus 自己修（無任何系統 know-how）
            fix_user = (
                f"Math topic: {topic}\n\n"
                f"--- Your previous code ---\n{code}\n\n"
                f"--- Render error ---\n{last_err[:1500]}\n\n"
                f"Fix the code so it renders successfully."
            )
            code_raw = llm.ask(FIX_SYSTEM_PROMPT, fix_user, role="coder")

        code = LLMClient.extract_code(code_raw)
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(code)

        try:
            # run_manim_task 回傳不一致:成功 (True, stdout, dur)、失敗 (False, err)
            result = RefiningLoop.run_manim_task(TARGET_FILE, SCENE_NAME)
            render_ok = result[0]
            render_err = result[1] if len(result) > 1 else ""
        except Exception as e:
            render_ok, render_err = False, f"render_task crashed: {type(e).__name__}: {e}"
        if render_ok:
            success_attempt = attempt
            _emit("LOG", f"✅ Attempt {attempt} render OK")
            break

        err_lines = [l for l in str(render_err).splitlines() if "Error" in l or "error" in l]
        last_err = str(render_err)
        short_err = err_lines[-1].strip() if err_lines else str(render_err)[:200]
        _emit("LOG", f"❌ Attempt {attempt} failed: {short_err}")

    # 保存最後一版代碼供診斷
    (out_dir / "opus_final_code.py").write_text(code, encoding="utf-8")

    if success_attempt is not None:
        script_stem = Path(TARGET_FILE).stem
        media_mp4 = ROOT / "media" / "videos" / script_stem / "480p15" / f"{SCENE_NAME}.mp4"
        if media_mp4.exists():
            shutil.copy2(str(media_mp4), str(out_dir / "video.mp4"))
            _emit("VIDEO", f"/static/runs/{task_id}/video.mp4")
        _emit("ATTEMPTS", str(success_attempt))
        _emit("FINAL", "OK")
        _emit("STAGE", "done|100")
        sys.exit(0)
    else:
        _emit("RENDER_ERROR", (last_err[:200] if last_err else "unknown"))
        _emit("ATTEMPTS", str(MAX_RETRIES))
        _emit("FINAL", "FAIL")
        _emit("STAGE", "failed|100")
        sys.exit(1)


if __name__ == "__main__":
    main()
