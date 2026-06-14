"""Lite vs System 兩欄對比頁（讀 compare_new/results.json）。

Output: exhibition/static/compare_new/compare.html
URL:    http://localhost:8000/static/compare_new/compare.html
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE / "static" / "compare_new"
RESULTS = BASE / "results.json"
OUT = BASE / "compare.html"


HTML = """<!doctype html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Planner Lite vs System · 生成對比</title>
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
  .legend .sys  {{ color: #6ee7b7; }}
  .legend .lite {{ color: #c4b5fd; }}
  .grid {{
    display: grid; grid-template-columns: 1fr; gap: 28px;
    padding: 24px; max-width: 1500px; margin: 0 auto;
  }}
  .card {{
    background: #0f172a; border: 1px solid #1e293b; border-radius: 14px;
    overflow: hidden;
  }}
  .card-head {{ padding: 14px 18px; border-bottom: 1px solid #1e293b; }}
  .card-head .id {{ color: #6366f1; font-family: ui-monospace, monospace; font-size: 12px; }}
  .card-head h3 {{ margin: 0 0 4px; font-size: 17px; color: #e2e8f0; }}
  .card-head .prompt {{ font-size: 11px; color: #64748b; margin-top: 4px; }}
  .card-head .challenge {{ font-size: 11px; color: #818cf8; margin-top: 4px; }}
  .videos {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: #1e293b; }}
  @media (max-width: 900px) {{ .videos {{ grid-template-columns: 1fr; }} }}
  .col {{ background: #000; position: relative; display: flex; flex-direction: column; }}
  .col-label {{
    position: absolute; top: 8px; left: 10px;
    background: rgba(0,0,0,0.7); padding: 3px 10px; border-radius: 4px;
    font-size: 11px; font-weight: 700; backdrop-filter: blur(4px); z-index: 1;
  }}
  .col-label.sys  {{ color: #6ee7b7; }}
  .col-label.lite {{ color: #c4b5fd; }}
  .col video {{ width: 100%; height: auto; aspect-ratio: 16/9; object-fit: contain; display: block; }}
  .col .nomedia {{ aspect-ratio: 16/9; display: flex; align-items: center; justify-content: center; color: #475569; font-size: 12px; }}
  .col .stats {{ padding: 8px 12px; font-size: 11px; color: #94a3b8; font-family: ui-monospace, monospace; border-top: 1px solid #1e293b; background: #0f172a; }}
  .col .stats .ok {{ color: #34d399; }}
  .col .stats .fail {{ color: #f87171; }}
</style>
</head>
<body>
<header>
  <h1>Planner Lite vs System · 生成對比</h1>
  <p>{n} 題重新出題 · 同題同 prompt 兩版各跑一次完整 pipeline</p>
  <div class="legend">
    <span><span class="sys">●</span> <b>SYSTEM</b> 主 Planner + 完整 pipeline</span>
    <span><span class="lite">●</span> <b>LITE</b> Planner Lite + LaggedStart 填滿 audio</span>
  </div>
</header>
<div class="grid">
{cards}
</div>
</body>
</html>"""


CARD = """<div class="card">
  <div class="card-head">
    <h3>{topic}</h3>
    <div class="id">{id}</div>
    <div class="prompt">📝 {prompt}</div>
    <div class="challenge">🎯 考驗：{challenge}</div>
  </div>
  <div class="videos">
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


def _stats(d: dict | None) -> str:
    if not d:
        return "—"
    mark = '<span class="ok">✅</span>' if d.get("render") else '<span class="fail">❌</span>'
    dur = f"<b>{d['video_dur_sec']}</b>s" if d.get("video_dur_sec") else "—"
    parts = [
        mark, dur,
        f"{d.get('code_lines')}行" if d.get("code_lines") else "—",
        f"{d.get('animations')}play" if d.get("animations") else "—",
        f"{d.get('lagged_starts')}lagged" if d.get("lagged_starts") else "0lagged",
        f"{d.get('subtitles')}旁白" if d.get("subtitles") else "—",
    ]
    if d.get("bj_score"):
        parts.append(f"BJ {d['bj_score']}")
    return " · ".join(parts)


def main():
    data = json.loads(RESULTS.read_text(encoding="utf-8")) if RESULTS.exists() else {}
    cards = []
    for tid, slot in data.items():
        sysd, lited = slot.get("system"), slot.get("lite")
        sys_v = BASE / "system" / f"{tid}.mp4"
        lite_v = BASE / "lite" / f"{tid}.mp4"
        cards.append(CARD.format(
            id=tid,
            topic=slot.get("topic", tid),
            prompt=slot.get("prompt", ""),
            challenge=slot.get("challenge", ""),
            sys_status="✅" if (sysd and sysd.get("render")) else "❌",
            lite_status="✅" if (lited and lited.get("render")) else "❌",
            sys_media=VIDEO.format(src=f"system/{tid}.mp4") if sys_v.exists() else NOMEDIA,
            lite_media=VIDEO.format(src=f"lite/{tid}.mp4") if lite_v.exists() else NOMEDIA,
            sys_stats=_stats(sysd),
            lite_stats=_stats(lited),
        ))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(HTML.format(n=len(data), cards="\n".join(cards)), encoding="utf-8")
    print(f"✅ {OUT}")
    print(f"   open: http://localhost:8000/static/compare_new/compare.html")


if __name__ == "__main__":
    main()
