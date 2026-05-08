"""
Merge code_review_q01_q83.csv 的 FJ Math/Verdict/GT Match 回填到 merged_q01_q150_combined.csv。
"""
import csv, io, pathlib

MAIN = "runs/merged_q01_q150_combined.csv"
REVIEWS = ["runs/code_review_q01_q83.csv", "runs/code_review_q101_q140.csv"]
OUTPUT = "runs/merged_q01_q150_with_review.csv"

def read(path):
    return list(csv.DictReader(io.StringIO(pathlib.Path(path).read_text(encoding="utf-8-sig"))))

main_rows = read(MAIN)
review = {}
for p in REVIEWS:
    for r in read(p):
        review[r["Case ID"]] = r

# 用主表欄位（保留所有原始欄位）
fields = list(main_rows[0].keys())

filled = 0
for r in main_rows:
    cid = r["Case ID"]

    # 舊版 (Q084~Q100): FJ Weighted 是 'PASS'/'FAIL' 字串 → 回填到 FJ Verdict
    fw = r.get("FJ Weighted", "")
    if fw in ("PASS", "FAIL") and not r.get("FJ Verdict"):
        r["FJ Verdict"] = fw

    rv = review.get(cid)
    if not rv:
        continue
    # 只填空值，不覆蓋已有的 FJ
    if not r.get("FJ Math") or r["FJ Math"] in ("-", ""):
        r["FJ Math"] = rv["FJ Math"]
        r["FJ Verdict"] = rv["FJ Verdict"]
        r["FJ Veto Reason"] = rv["FJ Veto Reason"]
        r["FJ GT Match"] = rv["GT Match"]
        filled += 1

with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(main_rows)

# 統計
fj_rows = [r for r in main_rows if r.get("FJ Math") and r["FJ Math"] not in ("-", "")]
print(f"✅ 合併完成 → {OUTPUT}")
print(f"   總題數: {len(main_rows)}")
print(f"   回填題數: {filled}")
print(f"   現在有 FJ Math 的題目: {len(fj_rows)} / {len(main_rows)}")

# Verdict 分布
verdicts = {}
for r in fj_rows:
    v = r.get("FJ Verdict", "")
    verdicts[v] = verdicts.get(v, 0) + 1
print(f"   Verdict 分布: {verdicts}")
