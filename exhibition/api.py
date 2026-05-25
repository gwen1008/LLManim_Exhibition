import asyncio
import json
import sys
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

HERE = Path(__file__).parent
ROOT = HERE.parent
STATIC_DIR = HERE / "static"
DIST_DIR = HERE / "frontend" / "dist"
RUNS_DIR = STATIC_DIR / "runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="LLManim Exhibition API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ── In-memory task store ──────────────────────────────────────────────

tasks: dict[str, dict] = {}

_STAGE_PERCENT: dict[str, int] = {
    "translate": 5,
    "rag": 10,
    "planner": 15,
    "planner_done": 30,
    "rag_done": 32,
    "coder": 35,
    "coder_done": 55,
    "refining": 60,
    "refining_done": 80,
    "judge": 85,
    "render": 65,
    "done": 100,
    "failed": 100,
}

_STAGE_LABEL: dict[str, str] = {
    "translate": "翻譯主題中",
    "rag": "RAG 搜尋中",
    "planner": "Planner 規劃中",
    "planner_done": "Planner 完成",
    "rag_done": "RAG 完成",
    "coder": "Coder 生成中",
    "coder_done": "Coder 完成",
    "refining": "Reflexion 修正中",
    "refining_done": "修正完成",
    "judge": "FinalJudge 評分中",
    "render": "渲染中",
    "done": "完成",
    "failed": "生成失敗",
}


def _parse_line(line: str, task: dict):
    """Parse structured marker lines from runner subprocess stdout."""
    line = line.strip()
    if not line:
        return

    task["logs"].append(line)

    if line.startswith("[STAGE] "):
        payload = line[8:]
        parts = payload.split("|")
        key = parts[0]
        pct = int(parts[1]) if len(parts) > 1 else _STAGE_PERCENT.get(key, task["progress"]["percent"])
        label = _STAGE_LABEL.get(key, key)
        task["progress"] = {"stage": label, "percent": pct}
        if key == "done":
            task["status"] = "done"
        elif key == "failed":
            task["status"] = "failed"
        else:
            task["status"] = "running"

    elif line.startswith("[PLANNER_JSON] "):
        try:
            task["artifacts"]["planner_json"] = json.loads(line[15:])
        except Exception:
            pass

    elif line.startswith("[CODE] "):
        task["artifacts"]["code_chars"] = line[7:]

    elif line.startswith("[VIDEO] "):
        task["artifacts"]["video_url"] = line[8:]

    elif line.startswith("[VISION_VERDICT] "):
        try:
            task["artifacts"]["vision_verdict"] = json.loads(line[17:])
        except Exception:
            pass

    elif line.startswith("[BJ_SCORE] "):
        try:
            task["artifacts"]["bj_score"] = float(line[11:])
        except Exception:
            pass

    elif line.startswith("[ERROR] "):
        task["error"] = line[8:]

    elif line.startswith("[RENDER_ERROR] "):
        task["error"] = line[15:]
        task["artifacts"]["render_error"] = line[15:]


async def _run_task(task_id: str, topic: str, mode: str):
    import os
    import time
    task = tasks[task_id]
    out_dir = RUNS_DIR / task_id

    runner_script = str(HERE / ("opus_only.py" if mode == "opus_only" else "full_system_runner.py"))

    proc_env = os.environ.copy()
    proc_env["PYTHONUTF8"] = "1"
    proc_env["PYTHONIOENCODING"] = "utf-8"
    # Pass unique target file per task to avoid race condition when both runners run concurrently
    proc_env["TASK_TARGET_FILE"] = str(ROOT / f"test_script_{task_id}.py")

    proc = await asyncio.create_subprocess_exec(
        sys.executable, runner_script, task_id, str(out_dir),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=proc_env,
    )

    proc.stdin.write((topic + "\n").encode())
    await proc.stdin.drain()
    proc.stdin.close()

    stderr_chunks: list[bytes] = []

    async def read_stdout():
        while True:
            try:
                raw = await asyncio.wait_for(proc.stdout.readline(), timeout=30)
            except asyncio.TimeoutError:
                continue
            if not raw:
                break
            _parse_line(raw.decode(errors="replace"), task)

    async def read_stderr():
        while True:
            try:
                raw = await asyncio.wait_for(proc.stderr.readline(), timeout=30)
            except asyncio.TimeoutError:
                continue
            if not raw:
                break
            stderr_chunks.append(raw)

    await asyncio.gather(read_stdout(), read_stderr())
    await proc.wait()

    if proc.returncode != 0 and task["status"] not in ("done", "failed"):
        stderr_out = b"".join(stderr_chunks).decode(errors="replace")[-800:]
        task["error"] = stderr_out or f"Process exited with code {proc.returncode}"
        task["status"] = "failed"
        task["progress"] = {"stage": "生成失敗", "percent": 100}

    task["duration_sec"] = round(time.time() - task["_start"], 1)

    # Clean up the per-task target file
    target_file = ROOT / f"test_script_{task_id}.py"
    try:
        target_file.unlink(missing_ok=True)
    except Exception:
        pass


# ── API routes ────────────────────────────────────────────────────────

@app.get("/api/gallery")
async def get_gallery():
    return json.loads((STATIC_DIR / "data" / "gallery.json").read_text(encoding="utf-8"))


@app.get("/api/stats")
async def get_stats():
    return json.loads((STATIC_DIR / "data" / "stats.json").read_text(encoding="utf-8"))


class GenerateRequest(BaseModel):
    topic: str
    mode: str = "full_system"


@app.post("/api/generate", status_code=200)
async def post_generate(req: GenerateRequest):
    import time
    if req.mode not in ("opus_only", "full_system"):
        raise HTTPException(status_code=400, detail="mode must be opus_only or full_system")
    if req.topic == "__probe__":
        return {"task_id": "__probe__"}

    task_id = str(uuid.uuid4())[:8]
    tasks[task_id] = {
        "status": "queued",
        "progress": {"stage": "排隊中", "percent": 0},
        "artifacts": {},
        "logs": [],
        "error": None,
        "duration_sec": 0,
        "_start": time.time(),
    }
    asyncio.create_task(_run_task(task_id, req.topic, req.mode))
    return {"task_id": task_id}


@app.get("/api/task/{task_id}")
async def get_task(task_id: str):
    import time
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    elapsed = task["duration_sec"] if task["status"] in ("done", "failed") else round(time.time() - task["_start"], 1)
    return {
        "status": task["status"],
        "progress": task["progress"],
        "artifacts": {k: v for k, v in task["artifacts"].items() if k != "code_chars"},
        "duration_sec": elapsed,
        "error": task["error"],
        "logs": task["logs"][-30:],
    }


# ── SPA fallback ──────────────────────────────────────────────────────

if DIST_DIR.exists():
    _assets = DIST_DIR / "assets"
    if _assets.exists():
        app.mount("/assets", StaticFiles(directory=str(_assets)), name="assets")

    @app.get("/favicon.svg")
    async def favicon():
        return FileResponse(str(DIST_DIR / "favicon.svg"))

    @app.get("/icons.svg")
    async def icons():
        return FileResponse(str(DIST_DIR / "icons.svg"))

    @app.get("/{full_path:path}")
    async def spa(full_path: str):
        candidate = DIST_DIR / full_path
        if candidate.exists() and candidate.is_file():
            return FileResponse(str(candidate))
        return FileResponse(str(DIST_DIR / "index.html"))
