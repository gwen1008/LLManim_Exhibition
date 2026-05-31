#!/usr/bin/env python3
"""Generate one poster frame per gallery video using ffmpeg.

Reads exhibition/static/data/gallery.json, extracts the mid-duration frame
per video, writes to exhibition/static/thumbs/{arm}/{id}.jpg.

Run from project root:
    python3 exhibition/build_thumbnails.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GALLERY_JSON = ROOT / "static" / "data" / "gallery.json"
VIDEOS_ROOT = ROOT / "static"
THUMBS_ROOT = ROOT / "static" / "thumbs"

POSTER_PCT = 0.50
JPEG_QUALITY = "3"  # 2-5 = high quality, 31 = worst
WIDTH = "480"  # downscale, keeps aspect


def extract_frame(video_path: Path, t_sec: float, out_path: Path) -> bool:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        f"{t_sec:.2f}",
        "-i",
        str(video_path),
        "-vframes",
        "1",
        "-q:v",
        JPEG_QUALITY,
        "-vf",
        f"scale={WIDTH}:-2",
        str(out_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"  ffmpeg failed: {proc.stderr[-300:]}", file=sys.stderr)
        return False
    return True


def process_video(arm: str, video_id: str, video_url: str, duration: float) -> int:
    rel = video_url.lstrip("/")
    rel = rel.removeprefix("static/")
    video_path = VIDEOS_ROOT / rel
    if not video_path.exists():
        print(f"  ! missing video: {video_path}")
        return 0
    if duration <= 0:
        print(f"  ! invalid duration: {duration}")
        return 0
    out_path = THUMBS_ROOT / arm / f"{video_id}.jpg"
    t = duration * POSTER_PCT
    return 1 if extract_frame(video_path, t, out_path) else 0


def main() -> int:
    if not shutil.which("ffmpeg"):
        print("ERROR: ffmpeg not found in PATH", file=sys.stderr)
        return 1
    if not GALLERY_JSON.exists():
        print(f"ERROR: {GALLERY_JSON} not found", file=sys.stderr)
        return 1

    data = json.loads(GALLERY_JSON.read_text())
    items = data.get("items", [])
    print(f"Processing {len(items)} items → {THUMBS_ROOT}")
    total = 0
    for item in items:
        vid = item["id"]
        print(f"[{vid}]")
        for arm, url_key, metrics_key in (
            ("opus", "opus_video_url", "opus_metrics"),
            ("system", "system_video_url", "system_metrics"),
        ):
            m = item.get(metrics_key, {})
            if not m.get("render_success"):
                continue
            dur = m.get("video_duration_sec") or 0
            total += process_video(arm, vid, item[url_key], float(dur))
    print(f"\nDone. {total} thumbnails written to {THUMBS_ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
