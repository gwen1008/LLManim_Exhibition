"""批次修 30 題的時序 bug：
- 把每個分鏡的 set_subtitle 從 play 之前移到 play 之後
- run_time 改為 max(0.5, _audio_dur_N - anim_time_{N+1})
- 刪除 remaining_X = ... 跟 self.wait(remaining_X) 兩行

用法:
  python evaluation/benchmark_set/fix_timing.py             # dry-run（只報告每題能修幾個）
  python evaluation/benchmark_set/fix_timing.py --apply     # 實際寫檔（備份 .py.timing-bak）
  python evaluation/benchmark_set/fix_timing.py Q024 --apply  # 單題
"""
from __future__ import annotations
import re, sys, argparse
from pathlib import Path

BASE = Path(__file__).parent

def fix_one(src: str, max_n: int = 20) -> tuple[str, int, list[int]]:
    """嘗試修每個 _audio_dur_N（N=0..max_n）。回傳 (new_src, fixed_count, skipped_n)。"""
    fixed = 0
    skipped = []
    for n in range(max_n):
        # Pattern A: 完整三段（含 # Step comment 可選）
        # _audio_dur_N = ...
        # (# Step X)?
        # self.set_subtitle(..., run_time=_audio_dur_N)
        # <中間動畫>
        # remaining_{N+1} = max(0.1, _audio_dur_N - anim_time_{N+1} + 0.5)
        # self.wait(max(0.1, remaining_{N+1}))
        # 把 set_subtitle 從 audio_dur 後到 remaining 之前任意位置抓出
        # 用兩個 pattern：先找 audio_dur ~ remaining 區塊，再從區塊內找 set_subtitle
        block_pattern = re.compile(
            rf'(        _audio_dur_{n} = [\d.]+  # \[audio-sync\] actual TTS duration\n)'
            rf'(.*?)'
            rf'(        remaining_{n+1} = max\(0\.1, _audio_dur_{n} - anim_time_{n+1}[\s\d.+\-]*\)\n'
            rf'        self\.wait\(max\(0\.1, remaining_{n+1}\)\)\n?)',
            re.DOTALL,
        )
        m = block_pattern.search(src)
        if not m:
            if re.search(rf'_audio_dur_{n} = ', src):
                skipped.append(n)
            continue

        audio_line = m.group(1)
        middle = m.group(2)

        # 從 middle 把 set_subtitle 那行抽出來
        sub_pattern = re.compile(
            rf'(        self\.set_subtitle\((.*?), run_time=_audio_dur_{n}\)\n)',
            re.DOTALL,
        )
        sm = sub_pattern.search(middle)
        if not sm:
            # 沒 set_subtitle，跳過（不是時序問題）
            continue

        subtitle_arg = sm.group(2)
        # 從 middle 移除原 set_subtitle 行
        middle_without_sub = middle[:sm.start()] + middle[sm.end():]

        new_block = (
            audio_line
            + middle_without_sub
            + f'        self.set_subtitle({subtitle_arg}, run_time=max(0.5, _audio_dur_{n} - anim_time_{n+1}))\n'
        )

        src = src[:m.start()] + new_block + src[m.end():]
        fixed += 1

    return src, fixed, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qids", nargs="*")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if args.qids:
        targets = [BASE / q for q in args.qids]
    else:
        targets = sorted(d for d in BASE.iterdir() if d.is_dir() and d.name.startswith("Q"))

    total_fixed = 0
    total_skipped = 0
    results = []
    for qd in targets:
        code = qd / "code.py"
        if not code.exists(): continue
        src = code.read_text(encoding="utf-8")
        # 先看 audio_dur 數量（上限給 max_n）
        all_durs = sorted(set(int(m) for m in re.findall(r'_audio_dur_(\d+)', src)))
        max_n = (max(all_durs) + 1) if all_durs else 0

        new_src, fixed, skipped = fix_one(src, max_n=max_n)
        results.append((qd.name, fixed, len(all_durs), skipped))
        total_fixed += fixed
        total_skipped += len(skipped)

        if args.apply and fixed > 0:
            bak = code.with_suffix(".py.timing-bak")
            if not bak.exists():
                bak.write_text(src, encoding="utf-8")
            code.write_text(new_src, encoding="utf-8")

    # 報告
    print(f"{'QID':<8}{'修了':<6}{'分鏡總數':<10}{'跳過':<10}{'狀態'}")
    print("-" * 60)
    for qid, fixed, total, skipped in results:
        status = "✅" if not skipped and fixed > 0 else ("⏭" if fixed == 0 else "⚠")
        skip_str = ",".join(map(str, skipped)) if skipped else "-"
        print(f"{qid:<8}{fixed:<6}{total:<10}{skip_str:<10}{status}")

    print(f"\n總計：修了 {total_fixed} 個分鏡，跳過 {total_skipped} 個（pattern 不符）")
    if not args.apply:
        print("這是 dry-run。確認 OK 後加 --apply 寫檔。")


if __name__ == "__main__":
    main()
