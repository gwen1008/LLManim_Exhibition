import asyncio
import json
import os
import sys
import uuid
from pathlib import Path
from typing import AsyncGenerator

# Windows cp950 terminals can't print UTF-8 emoji — reconfigure to avoid crash
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).parent
app = FastAPI()

_tasks: dict[str, dict] = {}


class AnimateRequest(BaseModel):
    topic: str


# (regex_string, stage, status)
_STAGE_PATTERNS = [
    ("RAG Retrieval 並行中|階段 1\\.8.*RAG",    "rag",     "running"),
    ("RAG Debug.*Total RAG context",             "rag",     "done"),
    ("階段 1: Director",                          "planner", "running"),
    ("Compression.*Planner|Blueprint.*已儲存|Planner.*fallback JSON", "planner", "done"),
    ("Audio Generation 並行中|階段 1\\.5.*Audio", "audio",   "running"),
    ("語音處理完成|語音生成發生錯誤",              "audio",   "done"),
    ("階段 2: Coder",                             "coder",   "running"),
    ("Coder.*T=0\\.3.*通過編譯|Coder.*T=0\\.3.*編譯失敗", "coder", "done"),
    ("階段 3: Review.*Fix",                       "render",  "running"),
]

import re as _re
_COMPILED = [(pat, _re.compile(pat), stage, status) for pat, stage, status in _STAGE_PATTERNS]
_VIDEO_RE = _re.compile(r"🎥\s+(\S+\.mp4)")
_ARCHIVE_DIR_RE = _re.compile(r"歸檔目錄:\s*(\S+)")
_JUDGE_SCORES_RE = _re.compile(
    r"FinalJudge\].*?math_correctness=(\S+).*?concept_alignment=(\S+).*?visual_clarity=(\S+)"
)
_JUDGE_TOTAL_RE = _re.compile(r"FinalJudge\].*?Weighted Total:\s*([\d.]+)")
_JUDGE_VERDICT_RE = _re.compile(r"FinalJudge\].*?Verdict:\s*(PASS|FAIL|ERROR)")


async def _run_pipeline(task_id: str, topic: str) -> None:
    task = _tasks[task_id]
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    proc = await asyncio.create_subprocess_exec(
        sys.executable, str(PROJECT_ROOT / "main.py"),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        env=env,
        cwd=str(PROJECT_ROOT),
    )
    proc.stdin.write((topic.strip() + "\n").encode())
    await proc.stdin.drain()
    proc.stdin.close()

    archive_dir = "stable_outputs"
    video_found = False
    judge_emitted = False
    judge_scores: dict = {}
    judge_total: float | None = None

    def _to_pct(v: str) -> float | None:
        try:
            return round(float(v) * 20, 2)  # 1-5 → 0-100
        except (ValueError, TypeError):
            return None

    async for raw in proc.stdout:
        line = raw.decode("utf-8", errors="replace").rstrip()
        print(line, flush=True)

        # detect archive dir
        m = _ARCHIVE_DIR_RE.search(line)
        if m:
            archive_dir = m.group(1)

        # detect video filename
        m = _VIDEO_RE.search(line)
        if m and not video_found:
            video_found = True
            video_path = f"{archive_dir}/{m.group(1)}"
            task["events"].append({"stage": "render", "status": "done", "video_path": video_path})

        # detect FinalJudge scores
        m = _JUDGE_SCORES_RE.search(line)
        if m:
            judge_scores = {
                "math_correctness":  _to_pct(m.group(1)) or 0.0,
                "concept_alignment": _to_pct(m.group(2)) or 0.0,
                "visual_clarity":    _to_pct(m.group(3)) or 0.0,
            }

        m = _JUDGE_TOTAL_RE.search(line)
        if m:
            judge_total = float(m.group(1))

        m = _JUDGE_VERDICT_RE.search(line)
        if m and not judge_emitted:
            judge_emitted = True
            verdict = "PASS" if m.group(1) == "PASS" else "FAIL"
            score = round(min(100.0, (judge_total / 5) * 100), 2) if judge_total else 0.0
            task["events"].append({
                "stage": "judge", "status": "done",
                "verdict": verdict, "score": score,
                "scores": judge_scores or {"math_correctness": 0.0, "visual_clarity": 0.0, "concept_alignment": 0.0},
            })

        # detect stage transitions
        for _, compiled, stage, status in _COMPILED:
            if compiled.search(line):
                task["events"].append({"stage": stage, "status": status})
                break

    await proc.wait()

    # fallback: pick the newest mp4 in archive_dir (sanitization differs between server/main)
    if not video_found:
        out_dir = PROJECT_ROOT / archive_dir
        if not out_dir.exists():
            out_dir = PROJECT_ROOT / "stable_outputs"
        if out_dir.exists():
            candidates = sorted(
                [f for f in out_dir.iterdir() if f.suffix == ".mp4"],
                key=lambda f: f.stat().st_mtime, reverse=True,
            )
            if candidates:
                video_path = f"{archive_dir}/{candidates[0].name}"
                task["events"].append({"stage": "render", "status": "done", "video_path": video_path})
                video_found = True

    if not video_found:
        task["events"].append({"stage": "render", "status": "error"})

    if not judge_emitted:
        task["events"].append({
            "stage": "judge", "status": "done",
            "verdict": "PASS" if video_found else "FAIL",
            "score": 0.0,
            "scores": {"math_correctness": 0.0, "visual_clarity": 0.0, "concept_alignment": 0.0},
        })
    task["done"] = True


async def _event_stream(task_id: str) -> AsyncGenerator[str, None]:
    if task_id not in _tasks:
        yield f"data: {json.dumps({'type': 'error'})}\n\n"
        return

    task = _tasks[task_id]
    sent = 0

    while True:
        events = task["events"]
        if sent < len(events):
            while sent < len(events):
                yield f"data: {json.dumps(events[sent])}\n\n"
                sent += 1
        elif task["done"]:
            break
        else:
            yield f"data: {json.dumps({'type': 'ping'})}\n\n"
            await asyncio.sleep(1)


@app.post("/animate")
async def start_animate(req: AnimateRequest):
    task_id = str(uuid.uuid4())
    _tasks[task_id] = {"topic": req.topic, "events": [], "done": False}
    asyncio.create_task(_run_pipeline(task_id, req.topic))
    return {"task_id": task_id}


@app.get("/animate/{task_id}/stream")
async def stream_events(task_id: str):
    return StreamingResponse(
        _event_stream(task_id),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/video/{path:path}")
async def serve_video(path: str):
    full = PROJECT_ROOT / path
    if not full.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(str(full), media_type="video/mp4")
