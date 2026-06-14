"""從 retry_report.json 生成「opus retry vs 本系統」對比網頁。

正式腳本(取代學測當初的 inline python),內建踩過的雷修正:
  - MathJax CDN(題目 $...$ LaTeX 渲染)
  - HTML escape(題目裡的 < > 不會被當標籤吃掉)
  - 統計數據從 report 即時算(不寫死)
  - badge 顏色按 opus_attempts / sys_iterations 自動判定
  - 崩題(任一邊失敗)排最前面當 killer card

用法:
  python exhibition/build_retry_page.py --variant cap20
  python exhibition/build_retry_page.py --variant hsat20
"""
import argparse
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

META = {
    "cap20": {
        "dir": "retry_cap20",
        "title": "國中會考 20 題 · 同樣 retry 能力,差距有多大?",
        "kp_field": "knowledge_point",
    },
    "hsat20": {
        "dir": "retry_hsat20",
        "title": "高中學測 20 題 · 同樣 retry 能力,差距有多大?",
        "kp_field": "knowledge_point",
    },
}

CSS = """:root{color-scheme:dark} *{box-sizing:border-box}
body{margin:0;font-family:ui-sans-serif,system-ui,"Microsoft JhengHei",sans-serif;background:#020617;color:#f8fafc;line-height:1.5}
header{padding:32px 24px;text-align:center;border-bottom:1px solid #1e293b;background:radial-gradient(ellipse at top,rgba(99,102,241,.12),transparent 65%)}
header h1{margin:0 0 6px;font-size:26px} header p{margin:0;color:#94a3b8;font-size:14px}
.stats{display:flex;gap:28px;justify-content:center;margin-top:18px;flex-wrap:wrap}
.stat{text-align:center} .stat b{display:block;font-size:30px;font-family:ui-monospace,monospace}
.stat .o{color:#fda4af} .stat .s{color:#6ee7b7} .stat small{color:#64748b;font-size:12px}
.grid{display:grid;gap:22px;padding:24px;max-width:1500px;margin:0 auto}
@media(min-width:1000px){.grid{grid-template-columns:repeat(2,1fr)}}
.card{background:#0f172a;border:1px solid #1e293b;border-radius:14px;overflow:hidden}
.card.killer{border-left:4px solid #f43f5e}
.head{padding:12px 16px;border-bottom:1px solid #1e293b;font-size:12px;color:#94a3b8;font-family:ui-monospace,monospace}
.head .id{color:#818cf8;font-weight:700}
.topic{padding:10px 16px;font-size:13px;color:#cbd5e1;border-bottom:1px solid #1e293b;max-height:60px;overflow:hidden}
.videos{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#1e293b}
.cell{background:#000;position:relative}
.cell video{width:100%;aspect-ratio:16/9;object-fit:contain;display:block}
.label{padding:8px 10px;font-size:11px;font-weight:600;background:#0f172a;display:flex;justify-content:space-between;align-items:center;gap:6px}
.cell.opus .label{color:#fda4af} .cell.sys .label{color:#6ee7b7}
.badge{font-size:10px;padding:2px 7px;border-radius:999px;white-space:nowrap}
.badge.good{background:rgba(16,185,129,.2);color:#6ee7b7}
.badge.warn{background:rgba(245,158,11,.2);color:#fcd34d}
.badge.bad{background:rgba(244,63,94,.2);color:#fda4af}
.crash{display:flex;flex-direction:column;align-items:center;justify-content:center;aspect-ratio:16/9;color:#f43f5e;font-weight:700;font-size:14px;text-align:center;background:repeating-linear-gradient(45deg,#1a0a0e,#1a0a0e 10px,#0f0608 10px,#0f0608 20px)}
.crash small{color:#9f6068;font-weight:400;font-size:11px;margin-top:4px}"""

MATHJAX = """<script>
window.MathJax={tex:{inlineMath:[['$','$'],['\\\\(','\\\\)']],displayMath:[['$$','$$'],['\\\\[','\\\\]']]},svg:{fontCache:'global'}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" id="MathJax-script" async></script>"""


def esc(s: str) -> str:
    """HTML escape，但保留 $...$ 給 MathJax(只轉 < > &，避免題目裡的不等式被當標籤)。"""
    return html.escape(str(s), quote=False)


def opus_badge(r: dict) -> str:
    """opus 端 badge：依 attempts 與 final 判色。"""
    if r.get("opus_final") != "OK":
        return '<span class="badge bad">5 次仍失敗 ❌</span>'
    a = r.get("opus_attempts")
    if a == 1:
        return '<span class="badge good">一次到位 ✨</span>'
    if a and a <= 2:
        return f'<span class="badge warn">第 {a} 次成功</span>'
    return f'<span class="badge warn">第 {a} 次成功</span>'


def sys_badge(r: dict) -> str:
    if r.get("sys_status") != "Success":
        return '<span class="badge bad">5 次仍失敗 ❌</span>'
    it = r.get("sys_iterations")
    if it in (0, 1):
        return '<span class="badge good">一次到位 ✨</span>'
    return f'<span class="badge warn">第 {it} 次</span>'


def cell(side: str, r: dict, base_id: str) -> str:
    """生一格影片或崩格。side = 'opus' | 'sys'."""
    if side == "opus":
        label = "Opus 裸跑 + retry≤5"
        ok = r.get("opus_final") == "OK"
        vid = f"{base_id}/video.mp4"
        badge = opus_badge(r)
    else:
        label = "本系統(Planner+RAG+lint)"
        ok = r.get("sys_status") == "Success"
        vid = f"{base_id}/sys_video.mp4"
        badge = sys_badge(r)

    inner = (
        f'<video src="{vid}" controls preload="metadata" playsinline></video>'
        if ok else
        '<div class="crash">⚠️ 渲染失敗<br><small>5 次 retry 仍無法產出</small></div>'
    )
    return f'<div class="cell {side}"><div class="label">{label} {badge}</div>{inner}</div>'


def card(r: dict, kp_field: str) -> str:
    opus_fail = r.get("opus_final") != "OK"
    sys_fail = r.get("sys_status") != "Success"
    killer = "killer" if (opus_fail or sys_fail) else ""
    kp = esc(r.get(kp_field, ""))
    diff = r.get("difficulty", "?")
    topic = esc(r.get("topic", ""))  # topic 可能不在 report，後面 merge 補
    return f"""<div class="card {killer}">
  <div class="head"><div><span class="id">{r['id']}</span> · D{diff} · {kp}</div></div>
  <div class="topic">{topic}</div>
  <div class="videos">
    {cell('opus', r, r['id'])}
    {cell('sys', r, r['id'])}
  </div>
</div>"""


def build(variant: str):
    m = META[variant]
    out_dir = HERE / "static" / m["dir"]
    report = json.loads((out_dir / "retry_report.json").read_text(encoding="utf-8"))

    # 補 topic：report 沒存 topic，從題庫 merge
    cases_path = HERE.parent / "evaluation" / f"test_cases_{variant}.json"
    if cases_path.exists():
        topics = {c["id"]: c["topic"] for c in json.loads(cases_path.read_text(encoding="utf-8"))}
        for r in report:
            r.setdefault("topic", topics.get(r["id"], ""))

    # 統計
    n = len(report)
    opus_ok = [r for r in report if r.get("opus_final") == "OK"]
    sys_ok = [r for r in report if r.get("sys_status") == "Success"]
    opus_att = [r["opus_attempts"] for r in opus_ok if r.get("opus_attempts")]
    sys_it = [r["sys_iterations"] for r in sys_ok if r.get("sys_iterations") is not None]
    opus_avg = round(sum(opus_att) / len(opus_att), 2) if opus_att else 0
    sys_avg = round(sum(sys_it) / len(sys_it), 2) if sys_it else 0
    sys_oneshot = sum(1 for r in sys_ok if r.get("sys_iterations") in (0, 1))

    # 排序：崩題(killer)排最前，其餘照原序
    def is_killer(r):
        return r.get("opus_final") != "OK" or r.get("sys_status") != "Success"
    ordered = sorted(report, key=lambda r: (not is_killer(r),))

    cards = "\n".join(card(r, m["kp_field"]) for r in ordered)

    stats = f"""<div class="stat"><b><span class="o">{len(opus_ok)}</span> / <span class="s">{len(sys_ok)}</span></b><small>render 成功數 (opus / 系統，共 {n} 題)</small></div>
<div class="stat"><b><span class="o">{opus_avg}</span> → <span class="s">{sys_avg}</span></b><small>平均嘗試次數 (opus → 系統)</small></div>
<div class="stat"><b class="s">{sys_oneshot}<small style="font-size:14px"> / {n}</small></b><small>本系統一次到位</small></div>"""

    doc = f"""<!doctype html><html lang="zh-TW"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{m['title']}</title>
<style>
{CSS}
</style>
{MATHJAX}
</head><body>
<header>
<h1>{m['title']}</h1>
<p>左:Opus 裸跑,失敗就餵錯誤重跑(上限 5 次) ｜ 右:本系統完整 pipeline</p>
<div class="stats">
{stats}
</div>
</header>
<div class="grid">
{cards}
</div>
</body></html>"""

    out_path = out_dir / "index.html"
    out_path.write_text(doc, encoding="utf-8")
    print(f"✅ 生成 {out_path}")
    print(f"   opus {len(opus_ok)}/{n} (avg {opus_avg}) | 系統 {len(sys_ok)}/{n} (avg {sys_avg}) | 一次到位 {sys_oneshot}")
    killers = [r['id'] for r in ordered if is_killer(r)]
    if killers:
        print(f"   崩題(killer card): {killers}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=list(META.keys()), default="cap20")
    args = ap.parse_args()
    build(args.variant)
