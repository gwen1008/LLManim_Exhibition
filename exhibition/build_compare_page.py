"""Generate a simple side-by-side comparison HTML for the 20-topic batch.

Output: exhibition/static/batch_20/index.html
View at: http://localhost:8000/static/batch_20/index.html
"""
from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
BATCH = HERE / "static" / "batch_20"
RESULTS_CSV = BATCH / "results.csv"
OUT_HTML = BATCH / "index.html"


HTML_TEMPLATE = """<!doctype html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>20 題對比 · Naked Opus vs Full System</title>
<style>
  :root {{
    color-scheme: dark;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", "Microsoft JhengHei", sans-serif;
    background: #020617;
    color: #f8fafc;
    line-height: 1.55;
  }}
  header {{
    padding: 32px 24px 20px;
    text-align: center;
    border-bottom: 1px solid #1e293b;
    background: radial-gradient(ellipse at top, rgba(99,102,241,0.12), transparent 65%);
  }}
  header h1 {{ margin: 0 0 8px; font-size: 28px; letter-spacing: -0.01em; }}
  header p  {{ margin: 0; color: #94a3b8; font-size: 14px; }}
  .stats {{
    display: inline-flex; gap: 20px; margin-top: 14px;
    font-family: ui-monospace, "Fira Code", monospace; font-size: 13px;
  }}
  .stats b {{ color: #34d399; font-weight: 700; }}
  .filter-bar {{
    display: flex; gap: 8px; justify-content: center; padding: 16px;
    border-bottom: 1px solid #1e293b; background: rgba(15,23,42,0.6); position: sticky; top: 0; z-index: 10;
    backdrop-filter: blur(8px);
  }}
  .filter-bar button {{
    background: #1e293b; color: #cbd5e1; border: 1px solid #334155;
    padding: 6px 14px; border-radius: 999px; cursor: pointer; font-size: 13px;
    font-family: inherit; transition: all 0.15s;
  }}
  .filter-bar button:hover {{ background: #334155; color: #fff; }}
  .filter-bar button.active {{ background: #4f46e5; color: #fff; border-color: #6366f1; }}
  .grid {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 24px;
    max-width: 1600px;
    margin: 0 auto;
  }}
  @media (min-width: 900px) {{
    .grid {{ grid-template-columns: repeat(2, 1fr); }}
  }}
  .card {{
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 14px;
    overflow: hidden;
    transition: border-color 0.15s, transform 0.15s;
  }}
  .card:hover {{ border-color: #334155; }}
  .card.naked-fail {{ border-left: 4px solid #f43f5e; }}
  .card.both-ok {{ border-left: 4px solid #64748b; }}
  .card-head {{
    display: flex; justify-content: space-between; align-items: baseline;
    padding: 14px 18px; border-bottom: 1px solid #1e293b;
  }}
  .card-head .id {{ color: #6366f1; font-family: ui-monospace, monospace; font-size: 12px; }}
  .card-head h3 {{ margin: 0 0 4px; font-size: 16px; color: #e2e8f0; }}
  .card-head .meta {{ font-size: 11px; color: #64748b; font-family: ui-monospace, monospace; }}
  .videos {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: #1e293b;
  }}
  .video-cell {{ background: #000; position: relative; }}
  .video-cell video {{ width: 100%; height: auto; display: block; aspect-ratio: 16/9; object-fit: contain; }}
  .video-cell .label {{
    position: absolute; top: 6px; left: 8px;
    background: rgba(0,0,0,0.7); color: #fff; padding: 2px 8px;
    border-radius: 4px; font-size: 11px; font-weight: 600;
    backdrop-filter: blur(4px);
  }}
  .video-cell.naked .label {{ color: #fda4af; }}
  .video-cell.system .label {{ color: #6ee7b7; }}
  .video-cell .placeholder {{
    aspect-ratio: 16/9; display: flex; flex-direction: column;
    align-items: center; justify-content: center; gap: 8px;
    color: #94a3b8; font-size: 13px;
  }}
  .video-cell .placeholder .icon {{ font-size: 28px; opacity: 0.6; }}
  .stats-row {{
    display: grid; grid-template-columns: 1fr 1fr; padding: 10px 14px;
    border-top: 1px solid #1e293b; font-size: 12px; color: #94a3b8;
    font-family: ui-monospace, monospace; gap: 8px;
  }}
  .stats-row .col {{ display: flex; gap: 12px; }}
  .stats-row .col span {{ display: inline-flex; gap: 4px; }}
  .stats-row .ok {{ color: #34d399; }}
  .stats-row .fail {{ color: #f87171; }}
  .stats-row b {{ color: #e2e8f0; font-weight: 600; }}
  .prompt {{
    padding: 10px 18px 14px; font-size: 12px; color: #64748b;
    border-top: 1px solid #1e293b; max-height: 4em; overflow: hidden;
    text-overflow: ellipsis;
  }}
  .prompt::before {{ content: "📝 "; opacity: 0.6; }}
  details {{ padding: 0; }}
  details summary {{
    list-style: none; cursor: pointer; padding: 6px 18px;
    font-size: 11px; color: #6366f1; border-top: 1px solid #1e293b;
  }}
  details summary::-webkit-details-marker {{ display: none; }}
  details[open] summary {{ color: #818cf8; }}
  details code {{
    display: block; padding: 8px 18px 14px; font-size: 11px;
    color: #94a3b8; white-space: pre-wrap; word-break: break-word;
    font-family: ui-monospace, "Fira Code", monospace;
  }}
</style>
</head>
<body>
<header>
  <h1>20 題對比實驗 · <span style="color:#fda4af">Naked Opus</span> vs <span style="color:#6ee7b7">本系統</span></h1>
  <p>同一題目，左 = Opus zero-shot 直出，右 = Multi-Agent Pipeline</p>
  <div class="stats">
    <span>Naked 成功 <b>{naked_ok}/{total}</b></span>
    <span>本系統成功 <b>{sys_ok}/{total}</b></span>
    <span>平均時長 <b>{avg_naked}s</b> vs <b>{avg_sys}s</b></span>
  </div>
</header>

<div class="filter-bar">
  <button class="active" data-filter="all">全部 ({total})</button>
  <button data-filter="naked-fail">Naked Crash ({naked_fail})</button>
  <button data-filter="both-ok">兩邊都成功 ({both_ok})</button>
</div>

<div class="grid">
{cards}
</div>

<script>
const buttons = document.querySelectorAll('.filter-bar button');
const cards = document.querySelectorAll('.card');
buttons.forEach(b => {{
  b.addEventListener('click', () => {{
    buttons.forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    const f = b.dataset.filter;
    cards.forEach(c => {{
      if (f === 'all') c.style.display = '';
      else c.style.display = c.classList.contains(f) ? '' : 'none';
    }});
  }});
}});
</script>
</body>
</html>"""


CARD_TEMPLATE = """<div class="card {extra_class}">
  <div class="card-head">
    <div>
      <h3>{topic}</h3>
      <div class="id">{id}</div>
    </div>
    <div class="meta">{n_lines} → {s_lines} 行</div>
  </div>
  <div class="videos">
    <div class="video-cell naked">
      <span class="label">NAKED · {naked_status}</span>
      {naked_video}
    </div>
    <div class="video-cell system">
      <span class="label">SYSTEM · {sys_status}</span>
      {sys_video}
    </div>
  </div>
  <div class="stats-row">
    <div class="col">
      <span class="{naked_class}">{naked_emoji}</span>
      <span><b>{naked_dur}</b>s</span>
      <span>{n_lines}行</span>
      <span>{n_plays}動畫</span>
    </div>
    <div class="col">
      <span class="ok">✅</span>
      <span><b>{sys_dur}</b>s</span>
      <span>{s_lines}行</span>
      <span>{s_plays}動畫</span>
      <span>{s_subs}旁白</span>
    </div>
  </div>
  <div class="prompt">{prompt}</div>
</div>"""


VIDEO_HTML = '<video src="{src}" controls preload="metadata" playsinline></video>'
PLACEHOLDER_HTML = '<div class="placeholder"><div class="icon">❌</div><div>Render Failed</div></div>'


def main():
    rows = list(csv.DictReader(open(RESULTS_CSV, encoding="utf-8")))
    naked_ok = sum(1 for r in rows if r["naked_render"] == "True")
    sys_ok = sum(1 for r in rows if r["sys_render"] == "True")
    naked_durs = [float(r["naked_video_sec"]) for r in rows if r["naked_video_sec"]]
    sys_durs = [float(r["sys_video_sec"]) for r in rows if r["sys_video_sec"]]
    naked_fail = sum(1 for r in rows if r["naked_render"] != "True")
    both_ok = sum(1 for r in rows if r["naked_render"] == "True" and r["sys_render"] == "True")

    cards = []
    for r in rows:
        naked_render = r["naked_render"] == "True"
        sys_render = r["sys_render"] == "True"
        extra_class = "naked-fail" if not naked_render else ("both-ok" if sys_render else "")

        naked_video = (
            VIDEO_HTML.format(src=f"naked/{r['id']}.mp4")
            if naked_render else PLACEHOLDER_HTML
        )
        sys_video = (
            VIDEO_HTML.format(src=f"system/{r['id']}.mp4")
            if sys_render else PLACEHOLDER_HTML
        )

        cards.append(CARD_TEMPLATE.format(
            id=r["id"],
            topic=r["topic"],
            naked_status="✅" if naked_render else "❌",
            sys_status="✅" if sys_render else "❌",
            naked_video=naked_video,
            sys_video=sys_video,
            naked_class="ok" if naked_render else "fail",
            naked_emoji="✅" if naked_render else "❌",
            naked_dur=r.get("naked_video_sec") or "—",
            sys_dur=r.get("sys_video_sec") or "—",
            n_lines=r.get("naked_lines") or "—",
            s_lines=r.get("sys_lines") or "—",
            n_plays=r.get("naked_render") and "?" or "—",  # not in CSV by default
            s_plays=r.get("sys_animations") or "—",
            s_subs=r.get("sys_subtitles") or "—",
            prompt=r["prompt"],
            extra_class=extra_class,
        ))

    html = HTML_TEMPLATE.format(
        total=len(rows),
        naked_ok=naked_ok,
        sys_ok=sys_ok,
        naked_fail=naked_fail,
        both_ok=both_ok,
        avg_naked=f"{sum(naked_durs)/len(naked_durs):.1f}" if naked_durs else "—",
        avg_sys=f"{sum(sys_durs)/len(sys_durs):.1f}" if sys_durs else "—",
        cards="\n".join(cards),
    )

    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"✅ {OUT_HTML}")
    print(f"   open: http://localhost:8000/static/batch_20/index.html")


if __name__ == "__main__":
    main()
