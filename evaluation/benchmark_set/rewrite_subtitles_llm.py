"""用 Claude Code 訂閱（claudealt + Haiku）批次重寫字幕。

流程：
  1. 抽 30 題 code.py 的 set_subtitle(...) 字串
  2. 分批（每批 ~30 條）餵 claudealt Haiku，要求嚴格 JSON 輸出
  3. 跟原文 diff 預覽
  4. --apply 套用（備份 .py.llm-bak）

用法：
  python evaluation/benchmark_set/rewrite_subtitles_llm.py             # dry-run
  python evaluation/benchmark_set/rewrite_subtitles_llm.py Q024 Q070   # 指定題目
  python evaluation/benchmark_set/rewrite_subtitles_llm.py --apply
"""
from __future__ import annotations
import re, json, sys, subprocess, argparse, difflib, tempfile, os
from pathlib import Path

BASE = Path(__file__).parent
SUBTITLE_RE = re.compile(r'(self\.set_subtitle\(\s*)(["\'])(.*?)\2', re.DOTALL)

SYSTEM_PROMPT = """你是一個字幕格式化工具。把中文數學旁白裡的「中文數字、運算詞」改成「阿拉伯數字、Unicode 符號」，保持其餘中文不動。

### 嚴格規則（依此優先順序套用）

1. **整數/負數**：
   - 「負七」→ `-7`、「二十」→ `20`、「一百」→ `100`
   - 「負 5」（已混合）→ `-5`

2. **真分數**：「七分之三」→ `3/7`（注意：中文「分母在前，分子在後」要對調）
   - 「負十八分之七」→ `-7/18`

3. **帶分數**：「二又七分之四」→ `2 4/7`（空格分隔，不加 +）
   - 「負一又三分之一」→ `-1 1/3`

4. **小數**：「零點五」→ `0.5`、「負三點二」→ `-3.2`

5. **百分比**：「百分之二十五」→ `25%`

6. **指數（次方用 Unicode 上標）**：
   - 「十的負三次方」→ `10⁻³`
   - 「二的五次方」→ `2⁵`
   - 「3.2 乘以 10 的負 6 次方」→ `3.2 × 10⁻⁶`
   - 上標表：⁰¹²³⁴⁵⁶⁷⁸⁹⁻

7. **運算符號（前後加空格）**：
   - 「乘以」/「乘」（數字之間）→ ` × `
   - 「除以」/「除」（數字之間）→ ` ÷ `
   - 「加」（數字之間）→ ` + `
   - 「減」（數字之間）→ ` - `
   - 「等於」→ ` = `

8. **序數（保留中文框架，只換數字）**：
   - 「第一步」→ `第 1 步`
   - 「第二組」→ `第 2 組`
   - 「步驟一」→ `步驟 1`
   - 「步驟二」→ `步驟 2`

9. **保留中文（不要轉的詞）**：
   - 成語/連寫：兩兩、單一、兩數、兩者、兩邊、一些、一樣、一起、一下、一直、一定、一律、一概、一切、一向
   - 量詞：「一個分數」「兩個負數」「四則運算」「一項」保留
   - 數學名詞：GCD、LCM、最大公因數、最小公倍數、絕對值、倒數、係數、分母、分子 全保留
   - 描述語：「負號獲勝」「負負得正」「正負相消」 全保留中文

10. **格式收尾**：
    - 多餘空白合併為單一空格
    - 中文標點（，。：；！？）後不留空白
    - 句首/句尾去除多餘空白

### 輸出格式

我會給你 JSON 輸入，每條有 `id` 和 `text`。你只回傳 JSON，**沒有任何前後說明**：
```json
[{"id":1,"out":"..."},{"id":2,"out":"..."}]
```

### Few-shot 範例

輸入：
```json
[
  {"id":1,"text":"我們從這個算式開始：負十八分之七乘以二又七分之四，再除以負一又三分之一。"},
  {"id":2,"text":"第一步：減去一個負數等於加上正數，所以減負十八變成加十八。"},
  {"id":3,"text":"步驟一：括號優先。計算負 6 減 2，等於負 8。"},
  {"id":4,"text":"向右移動 6 位代表乘以 10 的負 6 次方，所以 0.0000025 等於 2.5 乘以 10 的負 6 次方。"},
  {"id":5,"text":"把它們兩兩配對。第一組 99 減 198 等於負 99。"},
  {"id":6,"text":"負負得正。前兩個分數相乘剛好消去，結果是負一。"}
]
```

輸出：
```json
[
  {"id":1,"out":"我們從這個算式開始：-7/18 × 2 4/7，再 ÷ -1 1/3。"},
  {"id":2,"out":"第 1 步：減去一個負數 = 加上正數，所以減 -18 變成加 18。"},
  {"id":3,"out":"步驟 1：括號優先。計算 -6 - 2 = -8。"},
  {"id":4,"out":"向右移動 6 位代表 × 10⁻⁶，所以 0.0000025 = 2.5 × 10⁻⁶。"},
  {"id":5,"out":"把它們兩兩配對。第 1 組 99 - 198 = -99。"},
  {"id":6,"out":"負負得正。前兩個分數相乘剛好消去，結果是 -1。"}
]
```

注意：
- 範例 5「兩兩」保留、「兩個分數」中的「兩個」也保留
- 範例 6「負負得正」「相乘」全保留中文
- 所有運算符前後都有空格

現在等我給你輸入。"""


def extract_subtitles(qids: list[str] | None = None) -> list[dict]:
    """從 code.py 抽所有 set_subtitle 字串。"""
    if qids:
        targets = [BASE / q for q in qids]
    else:
        targets = sorted(d for d in BASE.iterdir() if d.is_dir() and d.name.startswith("Q"))
    items = []
    for qd in targets:
        code = qd / "code.py"
        if not code.exists(): continue
        src = code.read_text(encoding="utf-8")
        for m in SUBTITLE_RE.finditer(src):
            line_no = src[:m.start()].count("\n") + 1
            items.append({
                "qid": qd.name,
                "line": line_no,
                "quote": m.group(2),     # 引號型別 " 或 '
                "text": m.group(3),
                "match_start": m.start(),
                "match_end": m.end(),
            })
    return items


def call_claudealt_haiku(batch: list[dict]) -> list[dict]:
    """送一批字幕給 claudealt Haiku，回傳 LLM 改寫結果。"""
    payload = [{"id": i, "text": it["text"]} for i, it in enumerate(batch)]
    user_msg = f"輸入：\n```json\n{json.dumps(payload, ensure_ascii=False)}\n```\n\n請只回 JSON，不要其他文字。"

    # claudealt retired 2026-05-23; run as current user. Override with
    # CLAUDE_RUN_AS_USER if you really need sudo -u.
    _run_as = os.getenv("CLAUDE_RUN_AS_USER", "")
    _claude_cmd = ["claude", "--model", "haiku",
                   "--append-system-prompt", SYSTEM_PROMPT,
                   "-p", user_msg]
    cmd = (["sudo", "-u", _run_as, "-i"] + _claude_cmd) if _run_as else _claude_cmd
    print(f"  → 呼叫 Haiku（batch size={len(batch)}）...", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if result.returncode != 0:
        raise RuntimeError(f"claude CLI 失敗: {result.stderr[:500]}")

    out = result.stdout.strip()
    # 抽 JSON（可能被 ```json fence 包起來）
    m = re.search(r'\[\s*\{.*?\}\s*\]', out, re.DOTALL)
    if not m:
        raise RuntimeError(f"找不到 JSON：{out[:500]}")
    try:
        parsed = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON parse 失敗：{e}\n原文：{m.group(0)[:500]}")
    return parsed


def colorize(line: str) -> str:
    if line.startswith("+"): return f"\033[32m{line}\033[0m"
    if line.startswith("-"): return f"\033[31m{line}\033[0m"
    return line


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qids", nargs="*", help="只處理這些 QID（預設全 30 題）")
    ap.add_argument("--apply", action="store_true", help="實際寫檔（會備份 .py.llm-bak）")
    ap.add_argument("--batch-size", type=int, default=30, help="每批字幕數（預設 30）")
    ap.add_argument("--out-json", default=None, help="把 LLM 結果存到 JSON 檔（後續可重用）")
    ap.add_argument("--from-json", default=None, help="從先前存的 JSON 讀，跳過 LLM 呼叫")
    args = ap.parse_args()

    items = extract_subtitles(args.qids if args.qids else None)
    print(f"抽到 {len(items)} 條字幕（{len(set(i['qid'] for i in items))} 題）")

    if args.from_json:
        results = json.load(open(args.from_json, encoding="utf-8"))
        assert len(results) == len(items), f"JSON {len(results)} 條但抽到 {len(items)} 條，不匹配"
        for it, r in zip(items, results):
            it["new"] = r["out"]
    else:
        bs = args.batch_size
        for start in range(0, len(items), bs):
            batch = items[start:start+bs]
            try:
                parsed = call_claudealt_haiku(batch)
            except Exception as e:
                print(f"  ❌ batch {start//bs+1} 失敗: {e}")
                for it in batch:
                    it["new"] = it["text"]  # fallback
                continue
            by_id = {r["id"]: r["out"] for r in parsed}
            for i, it in enumerate(batch):
                it["new"] = by_id.get(i, it["text"])
            print(f"  ✓ batch {start//bs+1}: {len(parsed)} 條改寫完成")

        if args.out_json:
            json.dump(
                [{"qid": it["qid"], "line": it["line"], "text": it["text"], "out": it["new"]} for it in items],
                open(args.out_json, "w", encoding="utf-8"),
                ensure_ascii=False, indent=2,
            )
            print(f"  ✓ LLM 結果存到 {args.out_json}")

    # 印 diff（按題分組）
    by_qid = {}
    for it in items:
        by_qid.setdefault(it["qid"], []).append(it)

    changed_count = 0
    for qid, group in sorted(by_qid.items()):
        deltas = [it for it in group if it.get("new", it["text"]) != it["text"]]
        if not deltas: continue
        changed_count += len(deltas)
        print(f"\n=== {qid} ({len(deltas)} 條變更) ===")
        for it in deltas:
            print(colorize(f"- L{it['line']}: {it['text']}"))
            print(colorize(f"+ L{it['line']}: {it['new']}"))

    print(f"\n=== 總計：{changed_count} 條字幕變更 ===")

    if args.apply:
        # 套用：每題從後往前替換，避免位移
        for qid, group in by_qid.items():
            code = BASE / qid / "code.py"
            src = code.read_text(encoding="utf-8")
            # 重新掃一遍（不靠 match_start，避免之前修改的副作用）
            # 改為：依 text 字面 replace（set_subtitle 字串通常唯一）
            new_src = src
            for it in group:
                if it["text"] == it.get("new", it["text"]): continue
                old = f'self.set_subtitle({it["quote"]}{it["text"]}{it["quote"]}'
                new = f'self.set_subtitle({it["quote"]}{it["new"]}{it["quote"]}'
                if old in new_src:
                    new_src = new_src.replace(old, new, 1)
                else:
                    print(f"  ⚠ {qid} L{it['line']} 找不到原字串，跳過")
            if new_src != src:
                bak = code.with_suffix(".py.llm-bak")
                if not bak.exists():
                    bak.write_text(src, encoding="utf-8")
                code.write_text(new_src, encoding="utf-8")
                print(f"  ✓ {qid}/code.py 已寫入（備份 {bak.name}）")
    else:
        print("這是 dry-run。確認 OK 後加 --apply 實際寫檔。")
        print("建議：先加 --out-json results.json 把 LLM 結果存下來，下次可用 --from-json 跳過呼叫。")


if __name__ == "__main__":
    main()
