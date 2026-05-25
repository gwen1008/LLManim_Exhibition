#!/usr/bin/env python3
"""
更新 evaluation/benchmark_set/meta.json 的單題狀態。

用法：
    python evaluation/benchmark_set/mark_done.py Q028 done
    python evaluation/benchmark_set/mark_done.py Q029 draft --note "缺第三步"
    python evaluation/benchmark_set/mark_done.py Q039 reviewing
    python evaluation/benchmark_set/mark_done.py --list
    python evaluation/benchmark_set/mark_done.py --stats

status 可選: pending | draft | reviewing | done
done 會自動填 benchmark_mp4=QXXX/benchmark.mp4 並檢查檔案存在。
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

META = Path(__file__).parent / "meta.json"
VALID = {"pending", "draft", "reviewing", "done"}


def load():
    return json.loads(META.read_text(encoding="utf-8"))


def save(m):
    m["pending"] = sum(1 for c in m["cases"] if c["status"] == "pending")
    m["in_progress"] = sum(1 for c in m["cases"] if c["status"] in ("draft", "reviewing"))
    m["done"] = sum(1 for c in m["cases"] if c["status"] == "done")
    META.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cmd_list(m):
    for c in m["cases"]:
        mark = {"pending": "⚪", "draft": "🟡", "reviewing": "🟠", "done": "✅"}[c["status"]]
        print(f"{mark} {c['id']}  d{c['difficulty']}  {c['knowledge_point']:<20} {c['status']}")


def cmd_stats(m):
    print(f"total={m['total']}  done={m['done']}  in_progress={m['in_progress']}  pending={m['pending']}")
    print(f"完成度: {100 * m['done'] / m['total']:.1f}%")


def cmd_update(m, qid, status, note):
    case = next((c for c in m["cases"] if c["id"] == qid), None)
    if not case:
        sys.exit(f"❌ 找不到 {qid}")
    if status not in VALID:
        sys.exit(f"❌ status 必須是 {VALID}")

    qdir = Path(__file__).parent / qid
    if status == "done":
        bm = qdir / "benchmark.mp4"
        if not bm.exists():
            sys.exit(f"❌ {bm} 不存在，不能標 done。先重渲。")
        case["benchmark_mp4"] = f"{qid}/benchmark.mp4"
        code = qdir / "code.py"
        if code.exists():
            case["code_py"] = f"{qid}/code.py"
            case["render_cmd"] = f"manim -ql evaluation/benchmark_set/{qid}/code.py GeneratedScene"
    elif status == "draft":
        code = qdir / "code.py"
        if code.exists():
            case["code_py"] = f"{qid}/code.py"
            case["render_cmd"] = f"manim -ql evaluation/benchmark_set/{qid}/code.py GeneratedScene"

    case["status"] = status
    if note:
        case["notes"] = note
    case["last_updated"] = date.today().isoformat()
    save(m)
    print(f"✅ {qid} → {status}  (done={m['done']}/{m['total']})")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("qid", nargs="?", help="題目 ID, e.g. Q028")
    p.add_argument("status", nargs="?", choices=sorted(VALID))
    p.add_argument("--note", "-n", default=None)
    p.add_argument("--list", "-l", action="store_true")
    p.add_argument("--stats", "-s", action="store_true")
    args = p.parse_args()

    m = load()
    if args.list:
        cmd_list(m)
    elif args.stats:
        cmd_stats(m)
    elif args.qid and args.status:
        cmd_update(m, args.qid, args.status, args.note)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
