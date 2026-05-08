"""
Merge multiple evaluation session summary.csv files into one.
Usage: python merge_sessions.py
"""
import csv, io, pathlib

SESSIONS = [
    "runs/merged_q01_q100/summary.csv",
    "runs/20260507_132843/summary.csv",
]
OUTPUT = "runs/merged_q01_q150_combined.csv"

def read_csv(path):
    text = pathlib.Path(path).read_text(encoding="utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))

rows_all = []
all_fields = []

for path in SESSIONS:
    rows = read_csv(path)
    if rows:
        for f in rows[0].keys():
            if f not in all_fields:
                all_fields.append(f)
        rows_all.extend(r for r in rows if r.get("Case ID", "").startswith("Q"))

# Sort by Case ID (Q01 < Q02 ... < Q021 ... < ELEM_01 ...)
def sort_key(r):
    cid = r.get("Case ID", "")
    prefix_order = {"Q": 0, "E": 1, "M": 2, "H": 3}
    p = prefix_order.get(cid[0].upper(), 9) if cid else 9
    num = ""
    for c in cid[1:]:
        if c.isdigit():
            num += c
        else:
            break
    return (p, int(num) if num else 0, cid)

rows_all.sort(key=sort_key)

with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=all_fields, extrasaction="ignore")
    writer.writeheader()
    for r in rows_all:
        writer.writerow({k: r.get(k, "") for k in all_fields})

print(f"✅ 合併完成：{len(rows_all)} 題 → {OUTPUT}")

# Quick stats
statuses = {}
for r in rows_all:
    s = r.get("Status", "?")
    statuses[s] = statuses.get(s, 0) + 1
print("狀態分佈:", statuses)
