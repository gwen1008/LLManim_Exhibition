"""
Mock API server for frontend development.
Simulates the full pipeline event stream without running main.py.

Usage:
    uvicorn mock_api:app --port 8000 --reload
"""
import asyncio
import json
import uuid
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_EVENTS = [
    (1.0, {"stage": "rag",     "status": "running"}),
    (2.0, {"stage": "rag",     "status": "done"}),
    (3.0, {"stage": "planner", "status": "running"}),
    (5.0, {"stage": "planner", "status": "done"}),
    (5.5, {"stage": "audio",   "status": "running"}),
    (5.5, {"stage": "coder",   "status": "running"}),
    (7.0, {"stage": "audio",   "status": "done"}),
    (8.0, {"stage": "coder",   "status": "done"}),
    (8.5, {"stage": "render",  "status": "running"}),
    (11.0, {"stage": "render", "status": "done"}),
    (11.5, {"stage": "judge",  "status": "running"}),
    (14.0, {
        "stage": "judge", "status": "done",
        "verdict": "PASS", "score": 0.87,
        "scores": {
            "math_correctness": 0.92,
            "visual_clarity": 0.81,
            "concept_alignment": 0.88,
        },
        "video_path": "mock_video.mp4",
    }),
]

mock_tasks: dict[str, dict] = {}


async def _mock_stream(task_id: str) -> AsyncGenerator[dict, None]:
    start = asyncio.get_event_loop().time()
    idx = 0
    while idx < len(MOCK_EVENTS):
        t, event = MOCK_EVENTS[idx]
        now = asyncio.get_event_loop().time() - start
        if now >= t:
            yield {"data": json.dumps(event)}
            idx += 1
        else:
            await asyncio.sleep(0.2)


from pydantic import BaseModel

class AnimateRequest(BaseModel):
    topic: str


@app.post("/animate")
async def start_animate(req: AnimateRequest):
    task_id = str(uuid.uuid4())
    mock_tasks[task_id] = {"topic": req.topic}
    return {"task_id": task_id}


@app.get("/animate/{task_id}/stream")
async def stream_events(task_id: str):
    return EventSourceResponse(_mock_stream(task_id))


@app.get("/animate/{task_id}/result")
async def get_result(task_id: str):
    return {
        "task_id": task_id,
        "status": "done",
        "video_path": "mock_video.mp4",
        "judge": {
            "verdict": "PASS",
            "score": 0.87,
            "scores": {
                "math_correctness": 0.92,
                "visual_clarity": 0.81,
                "concept_alignment": 0.88,
            },
        },
    }


@app.get("/video/{filename}")
async def serve_video(filename: str):
    # return a placeholder 404 in mock mode
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="mock: no real video")
