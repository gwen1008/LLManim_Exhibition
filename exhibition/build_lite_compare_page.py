"""Generate 3-column comparison page: naked / system / lite.

Output: exhibition/static/batch_20/lite_compare.html
URL:    http://localhost:8000/static/batch_20/lite_compare.html
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BATCH = HERE / "static" / "batch_20"
LITE_JSON = BATCH / "lite_results.json"
RESULTS_CSV = BATCH / "results.csv"
OUT = BATCH / "lite_compare.html"


HTML = """<!doctype html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Planner Lite 3-Way 對比 · Naked / System / Lite</title>
<style>
  :root {{ color-scheme: dark; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; font-family: ui-sans-serif, system-ui, -apple-system,
      "Microsoft JhengHei", sans-serif;
    background: #020617; color: #f8fafc; line-height: 1.55;
  }}
  header {{
    padding: 32px 24px 20px; text-align: center;
    border-bottom: 1px solid #1e293b;
    background: radial-gradient(ellipse at top, rgba(99,102,241,0.12), transparent 65%);
  }}
  header h1 {{ margin: 0 0 8px; font-size: 26px; }}
  header p {{ margin: 0; color: #94a3b8; font-size: 14px; }}
  .legend {{
    display: inline-flex; gap: 24px; margin-top: 18px; font-size: 13px;
    font-family: ui-monospace, monospace;
  }}
  .legend b {{ font-weight: 700; }}
  .legend .naked {{ color: #fda4af; }}
  .legend .sys {{ color: #6ee7b7; }}
  .legend .lite {{ color: #c4b5fd; }}
  .grid {{
    display: grid; grid-template-columns: 1fr; gap: 28px;
    padding: 24px; max-width: 1800px; margin: 0 auto;
  }}
  .card {{
    background: #0f172a; border: 1px solid #1e293b; border-radius: 14px;
    overflow: hidden;
  }}
  .card-head {{
    padding: 14px 18px; border-bottom: 1px solid #1e293b;
    display: flex; justify-content: space-between; align-items: baseline;
  }}
  .card-head .id {{ color: #6366f1; font-family: ui-monospace, monospace; font-size: 12px; }}
  .card-head h3 {{ margin: 0 0 4px; font-size: 17px; color: #e2e8f0; }}
  .card-head .topic-prompt {{ font-size: 11px; color: #64748b; margin-top: 4px; }}
  .videos {{
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px;
    background: #1e293b;
  }}
  @media (max-width: 1000px) {{
    .videos {{ grid-template-columns: 1fr; }}
  }}
  .col {{
    background: #000; position: relative;
    display: flex; flex-direction: column;
  }}
  .col-label {{
    position: absolute; top: 8px; left: 10px;
    background: rgba(0,0,0,0.7); color: #fff; padding: 3px 10px;
    border-radius: 4px; font-size: 11px; font-weight: 700;
    backdrop-filter: blur(4px); z-index: 1;
  }}
  .col-label.naked {{ color: #fda4af; }}
  .col-label.sys   {{ color: #6ee7b7; }}
  .col-label.lite  {{ color: #c4b5fd; }}
  .col video {{ width: 100%; height: auto; aspect-ratio: 16/9; object-fit: contain; display: block; }}
  .col .nomedia {{
    aspect-ratio: 16/9; display: flex; align-items: center; justify-content: center;
    color: #475569; font-size: 12px;
  }}
  .col .stats {{
    padding: 8px 12px; font-size: 11px; color: #94a3b8;
    font-family: ui-monospace, monospace; border-top: 1px solid #1e293b;
    background: #0f172a;
  }}
  .col .stats b {{ color: #e2e8f0; }}
  .col .stats .ok {{ color: #34d399; }}
  .col .stats .fail {{ color: #f87171; }}
</style>
</head>
<body>
<header>
  <h1>Planner Lite 3-Way 對比</h1>
  <p>5 題視覺對比：Naked / 原系統 / Lite（Lite 重點：填滿 audio，無 dead air）</p>
  <div class="legend">
    <span><span class="naked">●</span> <b>NAKED</b> Opus zero-shot 直出（無 audio）</span>
    <span><span class="sys">●</span> <b>SYSTEM</b> 主 Planner + 完整 pipeline</span>
    <span><span class="lite">●</span> <b>LITE</b> Planner Lite + 動畫密度填滿 audio</span>
  </div>
</header>
<div class="grid">
{cards}
</div>
</body>
</html>"""


CARD = """<div class="card">
  <div class="card-head">
    <div>
      <h3>{topic}</h3>
      <div class="id">{id}</div>
      <div class="topic-prompt">📝 {prompt}</div>
    </div>
  </div>
  <div class="videos">
    <div class="col">
      <span class="col-label naked">NAKED · {naked_status}</span>
      {naked_media}
      <div class="stats">{naked_stats}</div>
    </div>
    <div class="col">
      <span class="col-label sys">SYSTEM · {sys_status}</span>
      {sys_media}
      <div class="stats">{sys_stats}</div>
    </div>
    <div class="col">
      <span class="col-label lite">LITE · {lite_status}</span>
      {lite_media}
      <div class="stats">{lite_stats}</div>
    </div>
  </div>
</div>"""


VIDEO = '<video src="{src}" controls preload="metadata" playsinline></video>'
NOMEDIA = '<div class="nomedia">no video</div>'


def main():
    rows = list(csv.DictReader(open(RESULTS_CSV, encoding="utf-8")))
    by_id = {r["id"]: r for r in rows}
    lite = json.loads(LITE_JSON.read_text(encoding="utf-8")) if LITE_JSON.exists() else {}

    cards = []
    for tid in lite.keys():
        r = by_id.get(tid)
        if not r:
            continue
        l = lite[tid]

        # Videos
        naked_path = BATCH / "naked" / f"{tid}.mp4"
        sys_path = BATCH / "system" / f"{tid}.mp4"
        lite_path = BATCH / "lite" / f"{tid}.mp4"

        def media(rel, exists):
            return VIDEO.format(src=rel) if exists else NOMEDIA

        # Stats lines
        def stats(render, dur, lines, plays, subs):
            mark = '<span class="ok">✅</span>' if render else '<span class="fail">❌</span>'
            d = f"<b>{dur}</b>s" if dur not in (None, "", "-") else "—"
            ll = f"{lines}行" if lines else "—"
            pp = f"{plays}動畫" if plays else "—"
            ss = f"{subs}旁白" if subs else "—"
            return f"{mark} {d} · {ll} · {pp} · {ss}"

        naked_ok = r["naked_render"] == "True"
        sys_ok = r["sys_render"] == "True"
        lite_ok = l["render"]

        cards.append(CARD.format(
            id=tid,
            topic=r["topic"],
            prompt=r["prompt"],
            naked_status="✅" if naked_ok else "❌",
            sys_status="✅" if sys_ok else "❌",
            lite_status="✅" if lite_ok else "❌",
            naked_media=media(f"naked/{tid}.mp4", naked_path.exists()),
            sys_media=media(f"system/{tid}.mp4", sys_path.exists()),
            lite_media=media(f"lite/{tid}.mp4", lite_path.exists()),
            naked_stats=stats(naked_ok, r.get("naked_video_sec"), r.get("naked_lines"), "", "0"),
            sys_stats=stats(sys_ok, r.get("sys_video_sec"), r.get("sys_lines"), r.get("sys_animations"), r.get("sys_subtitles")),
            lite_stats=stats(lite_ok, l.get("video_dur_sec"), l.get("code_lines"), l.get("animations"), l.get("subtitles")),
        ))

    OUT.write_text(HTML.format(cards="\n".join(cards)), encoding="utf-8")
    print(f"✅ {OUT}")
    print(f"   open: http://localhost:8000/static/batch_20/lite_compare.html")


if __name__ == "__main__":
    main()
