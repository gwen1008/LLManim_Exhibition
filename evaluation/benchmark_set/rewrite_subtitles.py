"""批次轉寫 set_subtitle 中文數字 → 阿拉伯數字，產 diff 預覽。

規則（用戶 2026-05-21 鎖定）：
- 整數/負數：負七 → -7、二十 → 20
- 真分數：七分之三 → 3/7（注意分母在前的中文 → 分子在前的阿拉伯）
- 帶分數：二又七分之四 → 2 4/7（空格分隔）
- 小數：零點五 → 0.5
- 百分比：百分之二十五 → 25%
- 運算：乘以→×、除以→÷、加→+、減→-、等於→=
- 指數：十的負三次方 → 10⁻³、二的五次方 → 2⁵
- 序數：第一步 → 第 1 步（保留中文「第…步/個/項」框架，只換數字）
- 數學名詞：最大公因數 GCD、最小公倍數 LCM（保留中文，不動）

用法：
  python evaluation/benchmark_set/rewrite_subtitles.py          # 只產 diff，不寫檔
  python evaluation/benchmark_set/rewrite_subtitles.py --apply  # 套用 + 備份原檔到 .bak
  python evaluation/benchmark_set/rewrite_subtitles.py Q024     # 只處理單題
"""
from __future__ import annotations
import re
import sys
import argparse
import difflib
from pathlib import Path

BASE = Path(__file__).parent

# ---------- 中文數字 → int ----------
CN_DIGITS = {"零":0,"一":1,"二":2,"兩":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}
CN_UNITS = {"十":10,"百":100,"千":1000,"萬":10000,"億":100000000}

def cn_to_int(s: str) -> int | None:
    """Parse Chinese numeral string to int. Returns None if not parseable."""
    if not s:
        return None
    # 純數字字串
    if s.isdigit():
        return int(s)

    result = 0
    current = 0
    for ch in s:
        if ch in CN_DIGITS:
            current = CN_DIGITS[ch]
        elif ch in CN_UNITS:
            unit = CN_UNITS[ch]
            if current == 0:
                current = 1
            if unit >= 10000:
                result = (result + current) * unit
                current = 0
            else:
                result += current * unit
                current = 0
        else:
            return None
    result += current
    return result

# 中文數字字元集（用於 regex）
CN_NUM_CHARS = "零一二兩三四五六七八九十百千萬億"
CN_NUM = f"[{CN_NUM_CHARS}]+"

# ---------- 上標表 ----------
SUPERSCRIPT = str.maketrans({
    "0":"⁰","1":"¹","2":"²","3":"³","4":"⁴",
    "5":"⁵","6":"⁶","7":"⁷","8":"⁸","9":"⁹","-":"⁻",
})

def to_superscript(n: int) -> str:
    return str(n).translate(SUPERSCRIPT)

# ---------- 轉寫規則 ----------
# 注意順序：最具體的先 match，避免被簡單規則吃掉

def rewrite(text: str) -> str:
    s = text

    # 1. 指數：負 N 次方 / N 次方  →  10⁻³ 形式
    # 「十的負三次方」 / 「十的三次方」
    def repl_pow_neg(m):
        base = cn_to_int(m.group(1))
        exp = cn_to_int(m.group(2))
        if base is None or exp is None: return m.group(0)
        return f"{base}{to_superscript(-exp)}"
    s = re.sub(rf"({CN_NUM})的負({CN_NUM})次方", repl_pow_neg, s)

    def repl_pow(m):
        base = cn_to_int(m.group(1))
        exp = cn_to_int(m.group(2))
        if base is None or exp is None: return m.group(0)
        return f"{base}{to_superscript(exp)}"
    s = re.sub(rf"({CN_NUM})的({CN_NUM})次方", repl_pow, s)

    # 2. 帶分數（負）N 又 M 分之 K  →  -N K/M
    def repl_mixed_neg(m):
        whole = cn_to_int(m.group(1))
        denom = cn_to_int(m.group(2))
        numer = cn_to_int(m.group(3))
        if None in (whole, denom, numer): return m.group(0)
        return f"-{whole} {numer}/{denom}"
    s = re.sub(rf"負({CN_NUM})又({CN_NUM})分之({CN_NUM})", repl_mixed_neg, s)

    def repl_mixed(m):
        whole = cn_to_int(m.group(1))
        denom = cn_to_int(m.group(2))
        numer = cn_to_int(m.group(3))
        if None in (whole, denom, numer): return m.group(0)
        return f"{whole} {numer}/{denom}"
    s = re.sub(rf"({CN_NUM})又({CN_NUM})分之({CN_NUM})", repl_mixed, s)

    # 3. 真分數（負）M 分之 K  →  -K/M
    def repl_frac_neg(m):
        denom = cn_to_int(m.group(1))
        numer = cn_to_int(m.group(2))
        if None in (denom, numer): return m.group(0)
        return f"-{numer}/{denom}"
    s = re.sub(rf"負({CN_NUM})分之({CN_NUM})", repl_frac_neg, s)

    def repl_frac(m):
        denom = cn_to_int(m.group(1))
        numer = cn_to_int(m.group(2))
        if None in (denom, numer): return m.group(0)
        return f"{numer}/{denom}"
    s = re.sub(rf"({CN_NUM})分之({CN_NUM})", repl_frac, s)

    # 4. 百分比：百分之 N → N%
    def repl_pct(m):
        n = cn_to_int(m.group(1))
        if n is None: return m.group(0)
        return f"{n}%"
    s = re.sub(rf"百分之({CN_NUM})", repl_pct, s)

    # 5. 小數：N 點 M[M...]  →  N.MMM
    def repl_decimal_neg(m):
        whole = cn_to_int(m.group(1))
        if whole is None: return m.group(0)
        frac_digits = "".join(str(CN_DIGITS[c]) for c in m.group(2) if c in CN_DIGITS)
        if not frac_digits: return m.group(0)
        return f"-{whole}.{frac_digits}"
    s = re.sub(rf"負({CN_NUM})點([{CN_NUM_CHARS}]+)", repl_decimal_neg, s)

    def repl_decimal(m):
        whole = cn_to_int(m.group(1))
        if whole is None: return m.group(0)
        frac_digits = "".join(str(CN_DIGITS[c]) for c in m.group(2) if c in CN_DIGITS)
        if not frac_digits: return m.group(0)
        return f"{whole}.{frac_digits}"
    s = re.sub(rf"({CN_NUM})點([{CN_NUM_CHARS}]+)", repl_decimal, s)

    # 6. 序數：第 N 步 / 第 N 個 / 第 N 項 → 第 1 步 / 第 1 個 / 第 1 項
    def repl_ord(m):
        n = cn_to_int(m.group(1))
        if n is None: return m.group(0)
        return f"第 {n} {m.group(2)}"
    s = re.sub(rf"第({CN_NUM})(步|個|項|題|次|組|行|列|位)", repl_ord, s)

    # 6b. 步驟一/二/三 → 步驟 1/2/3
    def repl_step(m):
        n = cn_to_int(m.group(1))
        if n is None: return m.group(0)
        return f"步驟 {n}"
    s = re.sub(rf"步驟({CN_NUM})", repl_step, s)

    # 7a. 負數：負 + 阿拉伯數字 → -N（先處理已混合形式）
    s = re.sub(r"負\s*(\d+(?:\.\d+)?)", r"-\1", s)

    # 7b. 負數：負 + 中文數字 → -N
    def repl_neg(m):
        n = cn_to_int(m.group(1))
        if n is None: return m.group(0)
        return f"-{n}"
    s = re.sub(rf"負({CN_NUM})", repl_neg, s)

    # 8. 純中文整數 → 阿拉伯
    # 8a. 預先保護成語/連寫詞：用 placeholder 暫時隔離
    PROTECTED = ["兩兩", "單一", "兩數", "兩者", "兩邊", "兩端", "兩側", "一邊", "一些",
                 "一樣", "一起", "一下", "一直", "一定", "一律", "一旁", "一致",
                 "一連串", "一系列", "一般", "一向", "一切", "一概"]
    placeholders = {}
    for i, w in enumerate(PROTECTED):
        if w in s:
            ph = f"\x00P{i}\x00"
            placeholders[ph] = w
            s = s.replace(w, ph)

    def repl_int(m):
        n = cn_to_int(m.group(1))
        if n is None: return m.group(0)
        return str(n)
    # 中文數字後不能緊接這些字（會變量詞/連寫詞）
    s = re.sub(
        rf"({CN_NUM})(?![個些樣起下直定邊則者項步次題組行列位律旁致般向切概])",
        repl_int,
        s,
    )

    # 還原 placeholder
    for ph, w in placeholders.items():
        s = s.replace(ph, w)

    # 9-pre. 運算符單字（在數字/符號之間）：乘/除/加/減 → ×/÷/+/-
    # 避開「相乘/相加/相減/乘法/除法/加法/減法/乘除」這類複合詞
    s = re.sub(r"(?<![相乘除加減])乘(?![以法除])(?=\s*[\d\-])", " × ", s)
    s = re.sub(r"(?<![相乘除加減])除(?![以法])(?=\s*[\d\-])", " ÷ ", s)

    # 9. 運算符（前後加空格，避免緊貼漢字視覺糟）
    s = s.replace("乘以", " × ")
    s = s.replace("除以", " ÷ ")
    s = re.sub(r"(?<=[\d\)])加(?=[\d\(\-])", " + ", s)
    s = re.sub(r"(?<=[\d\)])減(?=[\d\(\-])", " - ", s)
    s = s.replace("等於", " = ")

    # 10. 清掉多餘空白：「  」→「 」、句尾標點前空白、中文標點後不留空格
    s = re.sub(r" +", " ", s)
    s = re.sub(r" ([，。：；！？])", r"\1", s)
    s = re.sub(r"([，。：；！？]) ", r"\1", s)  # 中文標點後直接接運算符（不留空格）
    s = re.sub(r"([（(]) ", r"\1", s)
    s = re.sub(r" ([)）])", r"\1", s)
    s = s.strip()

    return s

# ---------- diff 顯示 ----------
def colorize(line: str) -> str:
    if line.startswith("+"):
        return f"\033[32m{line}\033[0m"
    if line.startswith("-"):
        return f"\033[31m{line}\033[0m"
    return line

SUBTITLE_RE = re.compile(r'(self\.set_subtitle\(\s*["\'])(.*?)(["\'])', re.DOTALL)

def process_file(path: Path) -> tuple[str, str, int]:
    """Return (original, rewritten, count_changed)."""
    src = path.read_text(encoding="utf-8")
    count = 0
    def repl(m):
        nonlocal count
        new = rewrite(m.group(2))
        if new != m.group(2):
            count += 1
        return m.group(1) + new + m.group(3)
    new_src = SUBTITLE_RE.sub(repl, src)
    return src, new_src, count

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qids", nargs="*", help="QID list (default: all)")
    ap.add_argument("--apply", action="store_true", help="實際寫檔（會備份 .bak）")
    ap.add_argument("--show-unchanged", action="store_true", help="也顯示沒變的題目")
    args = ap.parse_args()

    if args.qids:
        targets = [BASE / q for q in args.qids]
    else:
        targets = sorted(d for d in BASE.iterdir() if d.is_dir() and d.name.startswith("Q"))

    total_changes = 0
    for qd in targets:
        code = qd / "code.py"
        if not code.exists(): continue
        orig, new, count = process_file(code)
        if count == 0:
            if args.show_unchanged:
                print(f"\n--- {qd.name} (無變更) ---")
            continue
        total_changes += count
        print(f"\n=== {qd.name} ({count} 條字幕變更) ===")
        diff = difflib.unified_diff(
            orig.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=f"{qd.name}/code.py",
            tofile=f"{qd.name}/code.py (new)",
            n=0,
        )
        for line in diff:
            print(colorize(line.rstrip()))

        if args.apply:
            bak = code.with_suffix(".py.bak")
            if not bak.exists():
                bak.write_text(orig, encoding="utf-8")
            code.write_text(new, encoding="utf-8")
            print(f"  ✓ 已寫入 {code}（備份 {bak}）")

    print(f"\n=== 總計：{total_changes} 條字幕需要改 ===")
    if not args.apply:
        print("這是 dry-run。確認 OK 後加 --apply 實際寫檔。")

if __name__ == "__main__":
    main()
