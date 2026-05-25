"""Build self-contained HTML gallery for human review of kb150_v2 (or any KB).

Usage:
  python rag/build_review_gallery.py --kb-path knowledge_base/kb150_v2 \
      --videos-root runs/kb150_v2_review \
      --topics evaluation/kb150_v2_topics.json \
      --out runs/kb150_v2_review/index.html

Then open the produced HTML in browser:
  open runs/kb150_v2_review/index.html

Features:
  - One page, all scenes grouped by chapter
  - Video player + topic + method + new_topic + 5-rubric scoring
  - Auto-saves scores to localStorage (browser-local, persistent)
  - Export JSON button → save as evaluation/<kb-folder>_review_log.json
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def build_html(kb_path: Path, videos_root: Path, topics_path: Path, out_path: Path) -> None:
    topics = json.loads(topics_path.read_text(encoding="utf-8"))

    # Build flat list: [(chapter, scene_name, info, video_relpath_from_html, code_relpath)]
    out_dir = out_path.parent
    items = []
    for chapter, scenes in topics.items():
        if chapter.startswith("_"):
            continue
        for scene_name, info in scenes.items():
            mp4 = videos_root / chapter / f"{scene_name}.mp4"
            py = kb_path / chapter / f"{scene_name}.py"
            try:
                video_rel = mp4.relative_to(out_dir)
            except ValueError:
                video_rel = mp4
            try:
                code_rel = py.relative_to(out_dir)
            except ValueError:
                code_rel = py
            items.append({
                "chapter": chapter,
                "scene": scene_name,
                "key": f"{chapter}/{scene_name}",
                "method": info.get("method", ""),
                "topic": info.get("new_topic", ""),
                "notes": info.get("notes", ""),
                "video_url": str(video_rel),
                "code_url": str(code_rel),
                "video_exists": mp4.exists(),
            })

    items_json = json.dumps(items, ensure_ascii=False)
    kb_folder = kb_path.name

    html = HTML_TEMPLATE.replace("__ITEMS_JSON__", items_json).replace("__KB_NAME__", kb_folder)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"✅ Wrote {out_path}")
    print(f"   open {out_path}")


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>__KB_NAME__ Review Gallery</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: -apple-system, "PingFang TC", sans-serif; margin: 0; padding: 20px; background: #f7f7f9; color: #222; }
  header { position: sticky; top: 0; background: #fff; padding: 12px 20px; border-bottom: 1px solid #ddd; z-index: 100; margin: -20px -20px 20px; box-shadow: 0 2px 4px rgba(0,0,0,.05); }
  header h1 { margin: 0 0 8px; font-size: 18px; }
  .progress { font-size: 14px; color: #555; }
  .progress strong { color: #0a7; }
  .chapter { margin-bottom: 30px; }
  .chapter h2 { color: #555; font-size: 16px; border-bottom: 2px solid #e0e0e0; padding-bottom: 6px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 16px; }
  .card { background: #fff; border-radius: 8px; padding: 14px; box-shadow: 0 1px 3px rgba(0,0,0,.08); display: flex; flex-direction: column; }
  .card.done { border-left: 4px solid #0a7; }
  .card.low { border-left: 4px solid #e44; }
  .card-title { font-weight: 600; font-size: 14px; margin-bottom: 4px; word-break: break-all; }
  .card-meta { font-size: 12px; color: #888; margin-bottom: 8px; }
  .card video { width: 100%; max-height: 280px; background: #000; border-radius: 4px; }
  .topic-box { background: #f0f4f8; padding: 8px; border-radius: 4px; margin: 8px 0; font-size: 13px; line-height: 1.5; }
  .topic-box .method { color: #555; font-size: 11px; margin-bottom: 4px; }
  .rubric { display: flex; gap: 6px; margin: 8px 0; flex-wrap: wrap; }
  .rubric label { display: flex; align-items: center; gap: 4px; font-size: 12px; padding: 4px 8px; background: #eee; border-radius: 4px; cursor: pointer; user-select: none; }
  .rubric label.checked { background: #d4edda; }
  .rubric input { margin: 0; }
  .total { font-weight: 600; font-size: 13px; }
  .total.low { color: #e44; }
  .total.high { color: #0a7; }
  .note { width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px; font-family: inherit; font-size: 12px; resize: vertical; min-height: 40px; }
  .actions { margin: 8px 0; display: flex; gap: 8px; }
  .actions button { padding: 6px 12px; background: #2266dd; color: #fff; border: 0; border-radius: 4px; cursor: pointer; font-size: 13px; }
  .actions button:hover { background: #1a55cc; }
  .actions button.secondary { background: #888; }
  .missing { padding: 30px; text-align: center; color: #aaa; background: #fafafa; border-radius: 4px; }
  pre { background: #fafafa; padding: 8px; border-radius: 4px; font-size: 11px; overflow: auto; max-height: 100px; }
</style>
</head>
<body>
<header>
  <h1>📹 __KB_NAME__ Review Gallery</h1>
  <div class="progress">
    Progress: <strong id="reviewed-count">0</strong> / <span id="total-count">0</span>
    | Avg: <strong id="avg-score">—</strong> / 5
    | <span id="needs-rework">0</span> need rework (&lt;4/5)
  </div>
  <div class="actions">
    <button onclick="exportJSON()">📥 Export JSON</button>
    <button class="secondary" onclick="if(confirm('清空所有評分？')) clearAll()">🗑 Clear All</button>
    <button class="secondary" onclick="filterRework()">🔴 Show only &lt;4/5</button>
    <button class="secondary" onclick="showAll()">👁 Show all</button>
  </div>
</header>

<main id="main"></main>

<script>
const RUBRIC = ["clean", "steps", "visual", "latex", "pacing"];
const RUBRIC_LABEL = { clean: "畫面乾淨", steps: "步驟清楚", visual: "視覺對應", latex: "LaTeX 正確", pacing: "節奏合理" };
const ITEMS = __ITEMS_JSON__;
const STORAGE_KEY = "review_log_" + "__KB_NAME__";

function loadLog() { try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"); } catch { return {}; } }
function saveLog(log) { localStorage.setItem(STORAGE_KEY, JSON.stringify(log)); }

let log = loadLog();

function render() {
  const main = document.getElementById("main");
  const chapters = {};
  for (const item of ITEMS) {
    if (!chapters[item.chapter]) chapters[item.chapter] = [];
    chapters[item.chapter].push(item);
  }
  main.innerHTML = "";
  for (const [chap, list] of Object.entries(chapters)) {
    const sec = document.createElement("section");
    sec.className = "chapter";
    sec.innerHTML = `<h2>${chap} (${list.length})</h2><div class="grid"></div>`;
    const grid = sec.querySelector(".grid");
    for (const item of list) {
      grid.appendChild(buildCard(item));
    }
    main.appendChild(sec);
  }
  updateProgress();
}

function buildCard(item) {
  const card = document.createElement("div");
  card.className = "card";
  card.dataset.key = item.key;
  const entry = log[item.key] || { scores: {}, note: "" };
  const totalScore = RUBRIC.reduce((s, r) => s + (entry.scores[r] || 0), 0);
  const isReviewed = Object.keys(entry.scores).length === 5;
  if (isReviewed) card.classList.add(totalScore < 4 ? "low" : "done");

  const videoHTML = item.video_exists
    ? `<video src="${item.video_url}" controls preload="metadata"></video>`
    : `<div class="missing">⚠️ Video not found: ${item.video_url}</div>`;

  card.innerHTML = `
    <div class="card-title">${item.scene}</div>
    <div class="card-meta">${item.chapter}</div>
    ${videoHTML}
    <div class="topic-box">
      <div class="method">📐 ${item.method}</div>
      <div>${item.topic}</div>
    </div>
    <div class="rubric">
      ${RUBRIC.map(r => `
        <label class="${entry.scores[r] ? 'checked' : ''}">
          <input type="checkbox" data-rubric="${r}" ${entry.scores[r] ? "checked" : ""}>
          ${RUBRIC_LABEL[r]}
        </label>
      `).join("")}
    </div>
    <div class="total ${isReviewed ? (totalScore < 4 ? 'low' : 'high') : ''}">Total: ${totalScore}/5${isReviewed ? "" : " (未完成)"}</div>
    <textarea class="note" placeholder="筆記（選填）...">${entry.note || ""}</textarea>
  `;

  // bind events
  card.querySelectorAll('input[type=checkbox]').forEach(cb => {
    cb.addEventListener("change", () => {
      const r = cb.dataset.rubric;
      const cur = log[item.key] || { scores: {}, note: "" };
      cur.scores[r] = cb.checked ? 1 : 0;
      cur.total = RUBRIC.reduce((s, x) => s + (cur.scores[x] || 0), 0);
      log[item.key] = cur;
      saveLog(log);
      // refresh card visual
      const cardEl = cb.closest(".card");
      const reviewed = RUBRIC.every(x => x in cur.scores);
      cardEl.classList.toggle("done", reviewed && cur.total >= 4);
      cardEl.classList.toggle("low", reviewed && cur.total < 4);
      cb.closest("label").classList.toggle("checked", cb.checked);
      cardEl.querySelector(".total").textContent = `Total: ${cur.total}/5${reviewed ? "" : " (未完成)"}`;
      cardEl.querySelector(".total").className = `total ${reviewed ? (cur.total < 4 ? 'low' : 'high') : ''}`;
      updateProgress();
    });
  });
  card.querySelector("textarea").addEventListener("input", (e) => {
    const cur = log[item.key] || { scores: {}, note: "" };
    cur.note = e.target.value;
    log[item.key] = cur;
    saveLog(log);
  });
  return card;
}

function updateProgress() {
  const reviewed = Object.values(log).filter(e => Object.keys(e.scores || {}).length === 5);
  document.getElementById("reviewed-count").textContent = reviewed.length;
  document.getElementById("total-count").textContent = ITEMS.length;
  const avg = reviewed.length ? (reviewed.reduce((s, e) => s + (e.total || 0), 0) / reviewed.length).toFixed(2) : "—";
  document.getElementById("avg-score").textContent = avg;
  document.getElementById("needs-rework").textContent = reviewed.filter(e => (e.total || 0) < 4).length;
}

function exportJSON() {
  const blob = new Blob([JSON.stringify(log, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "__KB_NAME___review_log.json";
  a.click();
}
function clearAll() { log = {}; saveLog(log); render(); }
function filterRework() {
  document.querySelectorAll(".card").forEach(c => {
    c.style.display = c.classList.contains("low") ? "" : "none";
  });
}
function showAll() { document.querySelectorAll(".card").forEach(c => c.style.display = ""); }

render();
</script>
</body>
</html>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kb-path", type=Path, default=REPO / "knowledge_base" / "kb150_v2")
    p.add_argument("--videos-root", type=Path, default=None,
                   help="Default: runs/<kb-folder>_review")
    p.add_argument("--topics", type=Path, default=REPO / "evaluation" / "kb150_v2_topics.json")
    p.add_argument("--out", type=Path, default=None,
                   help="Default: <videos-root>/index.html")
    args = p.parse_args()

    kb_path = args.kb_path
    videos_root = args.videos_root or (REPO / "runs" / f"{kb_path.name}_review")
    out_path = args.out or (videos_root / "index.html")

    build_html(kb_path, videos_root, args.topics, out_path)


if __name__ == "__main__":
    main()
