import asyncio
import json
import os
import sys
import uuid
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STABLE_OUTPUTS = Path("stable_outputs")
STABLE_OUTPUTS.mkdir(exist_ok=True)

# in-memory task store: task_id -> dict
tasks: dict[str, dict] = {}

STAGE_PATTERNS = [
    ("[階段 1.8: RAG Retrieval 並行中]", "rag", "running"),
    ("[階段 1: Director]", "planner", "running"),
    ("[Planner Compliance]", "planner", "done"),
    ("[階段 1.5: Audio Generation 並行中]", "audio", "running"),
    ("語音處理完成", "audio", "done"),
    ("[階段 2: Coder]", "coder", "running"),
    ("[Coder] T=0.3 通過編譯檢查", "coder", "done"),
    ("[階段 3: Review & Fix]", "render", "running"),
    ("[階段 4: FinalJudge]", "judge", "running"),
    ("[FinalJudge] 評分失敗", "judge", "error"),
]


def _parse_stage(line: str) -> tuple[str, str] | None:
    for pattern, stage, status in STAGE_PATTERNS:
        if pattern in line:
            return stage, status
    return None


def _load_meta(task_id: str) -> dict | None:
    path = STABLE_OUTPUTS / f"{task_id}_meta.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


def _save_meta(task_id: str, data: dict) -> None:
    path = STABLE_OUTPUTS / f"{task_id}_meta.json"
    with open(path, "w") as f:
        json.dump(data, f)


async def _run_pipeline(task_id: str, topic: str) -> None:
    task = tasks[task_id]
    task["status"] = "running"

    proc = await asyncio.create_subprocess_exec(
        sys.executable, "main.py",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        cwd=str(Path(__file__).parent),
    )

    proc.stdin.write((topic + "\n").encode())
    await proc.stdin.drain()
    proc.stdin.close()
    await proc.stdin.wait_closed()

    async def read_stdout():
        while True:
            try:
                line_bytes = await asyncio.wait_for(proc.stdout.readline(), timeout=15)
            except asyncio.TimeoutError:
                task["events"].append({"type": "ping"})
                continue
            if not line_bytes:
                break
            line = line_bytes.decode(errors="replace").rstrip()
            result = _parse_stage(line)
            if result:
                stage, status = result
                task["events"].append({"stage": stage, "status": status})

    await read_stdout()
    await proc.wait()

    # load judge scores from cost_report.json
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in topic)
    video_path = None
    for f in STABLE_OUTPUTS.iterdir():
        if f.suffix == ".mp4" and safe_name[:20] in f.name:
            video_path = f.name
            break

    cost_report_path = STABLE_OUTPUTS / "cost_report.json"
    judge_data = {}
    if cost_report_path.exists():
        with open(cost_report_path) as f:
            cr = json.load(f)
        fj = cr.get("final_judge", {})
        judge_data = {
            "verdict": fj.get("verdict", "UNKNOWN"),
            "score": fj.get("weighted_total", 0.0),
            "scores": fj.get("scores", {}),
        }

    task["status"] = "done" if proc.returncode == 0 else "error"
    task["video_path"] = video_path
    task["judge"] = judge_data
    task["events"].append({
        "stage": "judge",
        "status": "done",
        **judge_data,
    })

    _save_meta(task_id, {
        "task_id": task_id,
        "topic": topic,
        "status": task["status"],
        "video_path": video_path,
        "judge": judge_data,
    })


class AnimateRequest(BaseModel):
    topic: str


@app.post("/animate")
async def start_animate(req: AnimateRequest):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "task_id": task_id,
        "topic": req.topic,
        "status": "pending",
        "events": [],
        "video_path": None,
        "judge": {},
    }
    asyncio.create_task(_run_pipeline(task_id, req.topic))
    return {"task_id": task_id}


async def _event_generator(task_id: str) -> AsyncGenerator[dict, None]:
    if task_id not in tasks:
        meta = _load_meta(task_id)
        if meta:
            tasks[task_id] = {**meta, "events": []}
        else:
            yield {"data": json.dumps({"error": "task not found"})}
            return

    task = tasks[task_id]
    sent = 0

    while True:
        events = task["events"]
        while sent < len(events):
            yield {"data": json.dumps(events[sent])}
            sent += 1

        if task["status"] in ("done", "error"):
            break

        await asyncio.sleep(1)


@app.get("/animate/{task_id}/stream")
async def stream_events(task_id: str):
    return EventSourceResponse(_event_generator(task_id))


@app.get("/animate/{task_id}/result")
async def get_result(task_id: str):
    task = tasks.get(task_id)
    if not task:
        meta = _load_meta(task_id)
        if not meta:
            raise HTTPException(status_code=404, detail="task not found")
        return meta
    return {
        "task_id": task_id,
        "status": task["status"],
        "video_path": task["video_path"],
        "judge": task["judge"],
    }


@app.get("/video/{filename}")
async def serve_video(filename: str):
    path = STABLE_OUTPUTS / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="video not found")
    return FileResponse(str(path), media_type="video/mp4")


# SPA fallback — serve static assets and index.html for all non-API routes
FRONTEND_DIST = Path("frontend/dist")

@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    candidate = FRONTEND_DIST / full_path
    if candidate.exists() and candidate.is_file():
        return FileResponse(str(candidate))
    index = FRONTEND_DIST / "index.html"
    if index.exists():
        return HTMLResponse(index.read_text(encoding="utf-8"))
    raise HTTPException(status_code=404, detail="frontend not built yet")
