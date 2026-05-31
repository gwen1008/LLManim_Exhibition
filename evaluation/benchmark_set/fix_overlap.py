"""偵測並修正每分鏡的 wait 時間，避免 audio 重疊。

對每分鏡：
1. 加總所有 self.play 的 run_time = actual_anim
2. 把 self.wait(max(0.1, _audio_dur_N - anim_time_{N+1})) 改成
   self.wait(max(0.1, _audio_dur_N - <actual_anim>))

確保 分鏡實際時長 = actual_anim + wait = _audio_dur_N，下段 audio 不會跟這段重疊。
"""
from __future__ import annotations
import re, argparse
from pathlib import Path

BASE = Path(__file__).parent


def fix_qid(qid: str, apply: bool) -> int:
    code = BASE / qid / "code.py"
    if not code.exists(): return 0
    src = code.read_text(encoding="utf-8")

    # 切分鏡
    matches = list(re.finditer(r'(        _audio_dur_(\d+) = ([\d.]+))', src))
    fixed = 0
    # 從後往前替換（避免 offset 變動）
    for i in range(len(matches) - 1, -1, -1):
        m = matches[i]
        n = int(m.group(2))
        scene_start = m.start()
        scene_end = matches[i+1].start() if i+1 < len(matches) else len(src)
        scene_body = src[scene_start:scene_end]

        # 先抽變數定義（anim_time_X = N.NN）
        local_vars = {}
        for vm in re.finditer(r'(\w+)\s*=\s*([\d.]+)\s*$', scene_body, re.MULTILINE):
            local_vars[vm.group(1)] = float(vm.group(2))

        # 算實際動畫時間（支援常數 + 變數）
        play_times = []
        for pm in re.finditer(r'self\.play\(.*?run_time\s*=\s*([\w.]+)', scene_body, re.DOTALL):
            val = pm.group(1)
            if val.replace(".", "").isdigit():
                play_times.append(float(val))
            elif val in local_vars:
                play_times.append(local_vars[val])
            else:
                play_times.append(1.0)  # 未知變數預設 1
        # 沒寫 run_time 的 play 預設 1.0
        all_plays = re.findall(r'self\.play\(', scene_body)
        plays_without_runtime = len(all_plays) - len(play_times)
        play_times.extend([1.0] * plays_without_runtime)
        actual_anim = sum(play_times)

        # 替換 wait 公式
        old_wait_re = re.compile(
            rf'self\.wait\(max\(0\.\d+,\s*_audio_dur_{n}\s*-\s*[^\)]+\)\)',
        )
        # 用實際動畫時間
        new_wait = f'self.wait(max(0.1, _audio_dur_{n} - {actual_anim:.2f}))'
        new_body, count = old_wait_re.subn(new_wait, scene_body)
        if count > 0:
            src = src[:scene_start] + new_body + src[scene_end:]
            fixed += 1

    if apply and fixed > 0:
        bak = code.with_suffix(".py.overlap-bak")
        if not bak.exists():
            bak.write_text(code.read_text(encoding="utf-8"), encoding="utf-8")
        code.write_text(src, encoding="utf-8")
    return fixed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qids", nargs="*")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if args.qids:
        qids = args.qids
    else:
        qids = sorted(d.name for d in BASE.iterdir() if d.is_dir() and d.name.startswith("Q"))

    total = 0
    for qid in qids:
        f = fix_qid(qid, args.apply)
        if f > 0:
            print(f"  {qid}: 修了 {f} 個分鏡的 wait")
            total += f

    print(f"\n總計 {total} 個分鏡 wait 修正")
    if not args.apply:
        print("Dry-run。--apply 寫檔。")


if __name__ == "__main__":
    main()
