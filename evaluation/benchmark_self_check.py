"""File-level health check for evaluation/benchmark_set/<qid>/.

Pure file/ffprobe/PIL validation — does NOT call BJ or any LLM. Use this to
catch outlier drafts (zero-byte, ffprobe fails, extreme duration, broken first
frame) BEFORE wasting Opus quota on a self-sanity run.

Resolves the same video the runner would pick:
  1. benchmark_set/<qid>/benchmark.mp4   (final, preferred)
  2. benchmark_set/<qid>/raw/draft_v1.mp4 (draft fallback)

Checks per qid:
  - video file exists + non-empty
  - ffprobe returns a duration
  - duration ∈ [MIN_DUR, MAX_DUR]
  - PIL can load first frame via ffmpeg pipe (probe at t=0.5s)

Usage:
  python evaluation/benchmark_self_check.py
  python evaluation/benchmark_self_check.py --benchmark-dir evaluation/benchmark_set
  python evaluation/benchmark_self_check.py --min-dur 5 --max-dur 240

Exit code: 0 if all OK, 1 if any qid fails.

Optional BJ self-sanity mode (--bj-self):
  Runs BenchmarkJudge(draft_v1, draft_v1) for every qid. Expected final=100 for
  all 30. Any deviation reveals a system-level bug (anchor leakage, position
  swap, ffprobe edge). Uses --no-cache by default since self-vs-self keys collide.

  python evaluation/benchmark_self_check.py --bj-self
  python evaluation/benchmark_self_check.py --bj-self --qids Q024,Q050  # subset
"""
import argparse
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
BENCHMARK_DIR_DEFAULT = ROOT / "evaluation" / "benchmark_set"

MIN_DUR_DEFAULT = 10.0
MAX_DUR_DEFAULT = 180.0


def _resolve_video(bdir: Path):
    final = bdir / "benchmark.mp4"
    draft = bdir / "raw" / "draft_v1.mp4"
    if final.exists():
        return final, "final"
    if draft.exists():
        return draft, "draft"
    return None, "missing"


def _ffprobe_duration(path: Path):
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of",
             "default=noprint_wrappers=1:nokey=1", str(path)],
            stderr=subprocess.STDOUT, timeout=10,
        )
        return float(out.strip())
    except Exception as e:
        return f"ffprobe_failed: {e.__class__.__name__}"


def _first_frame_ok(path: Path) -> bool:
    """Pull a single frame at t=0.5s via ffmpeg, verify PIL can open it."""
    try:
        from PIL import Image
    except ImportError:
        return True  # PIL missing — skip this check, not the goal
    try:
        proc = subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", "0.5", "-i", str(path),
             "-vframes", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
            capture_output=True, timeout=15,
        )
        if proc.returncode != 0 or not proc.stdout:
            return False
        Image.open(io.BytesIO(proc.stdout)).verify()
        return True
    except Exception:
        return False


def check_qid(bdir: Path, min_dur: float, max_dur: float) -> dict:
    video, source = _resolve_video(bdir)
    row = {"qid": bdir.name, "source": source}

    if video is None:
        row["status"] = "missing"
        row["issues"] = ["no benchmark.mp4 and no raw/draft_v1.mp4"]
        return row

    row["video"] = str(video.relative_to(ROOT))
    size = video.stat().st_size
    row["size_bytes"] = size
    issues = []

    if size == 0:
        issues.append("zero-byte file")

    dur = _ffprobe_duration(video) if size > 0 else None
    row["duration_s"] = dur
    if isinstance(dur, str):
        issues.append(dur)
    elif dur is not None:
        if dur < min_dur:
            issues.append(f"duration {dur:.1f}s < min {min_dur}s")
        elif dur > max_dur:
            issues.append(f"duration {dur:.1f}s > max {max_dur}s")

    if size > 0 and not isinstance(dur, str):
        if not _first_frame_ok(video):
            issues.append("PIL cannot decode first frame")

    row["status"] = "ok" if not issues else "fail"
    row["issues"] = issues
    return row


def _bj_self_sanity(qid_dirs, passes: int = 2):
    """Run BJ(draft, draft) for each qid. Expected final=100 across the board."""
    from agents.utils.benchmark_judge import BenchmarkJudge
    from agents.core.llm_client import LLMClient

    bj = BenchmarkJudge(llm_client=LLMClient(), passes=passes)
    rows = []
    print(f"\n🧪 BJ self-sanity ({len(qid_dirs)} qids, passes={passes}, no-cache)\n")
    for d in qid_dirs:
        qid = d.name
        video, source = _resolve_video(d)
        if video is None:
            rows.append({"qid": qid, "status": "skip_no_video"})
            print(f"⏭️  [{qid}] no video → skip")
            continue
        code_path = d / "raw" / "draft_v1.py"
        code_str = code_path.read_text(encoding="utf-8") if code_path.exists() else None
        try:
            res = bj.judge(
                candidate_video=str(video),
                benchmark_video=str(video),
                question_topic=f"self-sanity {qid}",
                candidate_code=code_str,
                cache_path=None,  # disable: self-vs-self keys collide
                force=False,
            )
            status = res.get("status", "ok")
            final = res.get("final_100")
            rows.append({"qid": qid, "status": status, "final_100": final,
                         "modes": res.get("modes")})
            flag = "✓" if final == 100 else "✗"
            print(f"  {flag} [{qid}] status={status} final={final} modes={res.get('modes')}")
        except Exception as e:
            rows.append({"qid": qid, "status": "error", "error": str(e)})
            print(f"  ✗ [{qid}] error: {e}")

    n_total = len(rows)
    n_100 = sum(1 for r in rows if r.get("final_100") == 100)
    n_off = sum(1 for r in rows
                if r.get("status") == "ok" and r.get("final_100") != 100)
    n_err = sum(1 for r in rows if r.get("status") in ("error", "insufficient_passes"))
    print(f"\n📊 self-sanity result: {n_100}/{n_total} == 100  "
          f"(off={n_off}, errors={n_err})")
    if n_off or n_err:
        print("⚠️  any non-100 row is a system bug — investigate before A/B run.")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark-dir", default=str(BENCHMARK_DIR_DEFAULT))
    ap.add_argument("--min-dur", type=float, default=MIN_DUR_DEFAULT)
    ap.add_argument("--max-dur", type=float, default=MAX_DUR_DEFAULT)
    ap.add_argument("--json", action="store_true",
                    help="emit JSON to stdout instead of human-readable table")
    ap.add_argument("--bj-self", action="store_true",
                    help="run BJ(draft, draft) self-sanity (calls Opus; ~25s/qid)")
    ap.add_argument("--qids", default=None,
                    help="comma-separated qid filter (e.g. Q024,Q050)")
    ap.add_argument("--passes", type=int, default=2,
                    help="passes per qid in --bj-self (default 2)")
    args = ap.parse_args()

    root = Path(args.benchmark_dir)
    qid_dirs = sorted(p for p in root.iterdir()
                      if p.is_dir() and p.name.startswith("Q"))
    if args.qids:
        keep = {q.strip() for q in args.qids.split(",")}
        qid_dirs = [p for p in qid_dirs if p.name in keep]

    if args.bj_self:
        bj_rows = _bj_self_sanity(qid_dirs, passes=args.passes)
        out = ROOT / "evaluation" / "golden_set" / "bj_self_sanity_results.json"
        out.write_text(json.dumps(bj_rows, indent=2, ensure_ascii=False),
                       encoding="utf-8")
        print(f"💾 saved: {out.relative_to(ROOT)}")
        ok = all(r.get("final_100") == 100 for r in bj_rows if r.get("status") == "ok")
        sys.exit(0 if ok else 2)

    rows = [check_qid(d, args.min_dur, args.max_dur) for d in qid_dirs]

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        n_ok = sum(1 for r in rows if r["status"] == "ok")
        n_fail = sum(1 for r in rows if r["status"] == "fail")
        n_miss = sum(1 for r in rows if r["status"] == "missing")
        n_draft = sum(1 for r in rows if r.get("source") == "draft")
        n_final = sum(1 for r in rows if r.get("source") == "final")
        print(f"📋 benchmark_set self-check ({len(rows)} qids)")
        print(f"   OK={n_ok}  FAIL={n_fail}  MISSING={n_miss}  "
              f"(final={n_final}, draft={n_draft})\n")
        print(f"  {'qid':<6} {'source':<7} {'dur(s)':>8} {'size(MB)':>9}  status / issues")
        print("  " + "-" * 70)
        for r in rows:
            dur = r.get("duration_s")
            dur_s = f"{dur:.1f}" if isinstance(dur, (int, float)) else "—"
            size_mb = (r.get("size_bytes", 0) or 0) / 1e6
            tag = "✓" if r["status"] == "ok" else ("✗" if r["status"] == "fail" else "·")
            issues = "; ".join(r.get("issues", []))
            print(f"  {r['qid']:<6} {r.get('source','?'):<7} "
                  f"{dur_s:>8} {size_mb:>9.2f}  {tag} {issues}")

    sys.exit(0 if all(r["status"] == "ok" for r in rows) else 1)


if __name__ == "__main__":
    main()
