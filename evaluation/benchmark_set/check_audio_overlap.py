"""偵測 30 題 code.py 的音訊重疊問題。

每個分鏡 N：
- 預期 audio 長度: _audio_dur_N
- 動畫時間 (anim_time_{N+1} 變數值)
- 動畫實際時間 (所有 self.play 的 run_time 加總)
- wait 時間: max(0.1, _audio_dur_N - anim_time_{N+1})
- 分鏡實際時長 = 動畫實際時間 + wait 時間
- 重疊判定: 如果 分鏡實際時長 < _audio_dur_N，下個 add_sound 會跟這段重疊

輸出 markdown report
"""
from __future__ import annotations
import re, sys
from pathlib import Path

BASE = Path(__file__).parent

def analyze_qid(qid: str):
    code = BASE / qid / "code.py"
    if not code.exists():
        return None
    src = code.read_text(encoding="utf-8")

    # 抽 construct 函數內容
    construct_m = re.search(r'def construct\(self\):(.*?)(?=\n    def |\nclass |\Z)', src, re.DOTALL)
    if not construct_m:
        return None
    body = construct_m.group(1)

    # 切分鏡：每個 _audio_dur_N = X 開始
    scenes = []
    matches = list(re.finditer(r'        _audio_dur_(\d+) = ([\d.]+)', body))
    for i, m in enumerate(matches):
        n = int(m.group(1))
        audio_dur = float(m.group(2))
        scene_start = m.start()
        scene_end = matches[i+1].start() if i+1 < len(matches) else len(body)
        scene_body = body[scene_start:scene_end]

        # 抽 anim_time_{N+1} 賦值
        at_match = re.search(rf'anim_time_{n+1}\s*=\s*([\d.]+)', scene_body)
        anim_time_declared = float(at_match.group(1)) if at_match else None

        # 先抽變數定義
        local_vars = {}
        for vm in re.finditer(r'(\w+)\s*=\s*([\d.]+)\s*$', scene_body, re.MULTILINE):
            local_vars[vm.group(1)] = float(vm.group(2))

        # 算實際 self.play run_time 加總（支援變數）
        play_times = []
        for pm in re.finditer(r'self\.play\(.*?run_time\s*=\s*([\w.]+)', scene_body, re.DOTALL):
            val = pm.group(1)
            if val.replace(".", "").isdigit():
                play_times.append(float(val))
            elif val in local_vars:
                play_times.append(local_vars[val])
            else:
                play_times.append(1.0)
        all_plays = re.findall(r'self\.play\(', scene_body)
        plays_without_runtime = len(all_plays) - len(play_times)
        play_times.extend([1.0] * plays_without_runtime)
        actual_anim_time = sum(play_times)

        # 抽 wait 表達式裡的減項，直接算
        wait_match = re.search(
            rf'self\.wait\(max\(0\.\d+,\s*_audio_dur_{n}\s*-\s*([^\)]+)\)\)',
            scene_body,
        )
        if wait_match:
            sub_expr = wait_match.group(1).strip()
            if sub_expr.replace(".", "").isdigit():
                sub_val = float(sub_expr)
            elif sub_expr in local_vars:
                sub_val = local_vars[sub_expr]
            else:
                sub_val = 0
            wait_secs = max(0.1, audio_dur - sub_val)
        else:
            wait_secs = None

        # 分鏡實際時長 = 動畫實際 + wait
        actual_scene_dur = actual_anim_time + (wait_secs or 0)
        # 重疊量 = audio_dur - 分鏡實際時長（正值表示下段 audio 開始時這段還在播）
        overlap = audio_dur - actual_scene_dur

        scenes.append({
            "n": n,
            "audio_dur": audio_dur,
            "anim_time_declared": anim_time_declared,
            "actual_anim_time": actual_anim_time,
            "wait_secs": wait_secs,
            "actual_scene_dur": actual_scene_dur,
            "overlap": overlap,
        })

    return scenes


def main():
    qids = sys.argv[1:] if len(sys.argv) > 1 else sorted(
        d.name for d in BASE.iterdir() if d.is_dir() and d.name.startswith("Q")
    )

    print(f"{'QID':<6}{'N':<3}{'audio':<8}{'宣告':<8}{'實際':<8}{'wait':<8}{'分鏡實':<8}{'重疊':<8}{'狀態'}")
    print("-" * 70)

    bad_qids = []
    for qid in qids:
        scenes = analyze_qid(qid)
        if scenes is None: continue
        max_overlap = 0
        for s in scenes:
            ad = s["audio_dur"]
            atd = s["anim_time_declared"]
            atd_str = f"{atd:.1f}" if atd is not None else "?"
            aat = s["actual_anim_time"]
            ws = s["wait_secs"]
            ws_str = f"{ws:.1f}" if ws is not None else "?"
            asd = s["actual_scene_dur"]
            ov = s["overlap"]
            status = "🔴" if ov > 0.5 else ("⚠️" if ov > 0.1 else "✅")
            max_overlap = max(max_overlap, ov)
            print(f"{qid:<6}{s['n']:<3}{ad:<8.2f}{atd_str:<8}{aat:<8.1f}{ws_str:<8}{asd:<8.1f}{ov:<+8.1f}{status}")
        if max_overlap > 0.5:
            bad_qids.append((qid, max_overlap))
        print()

    if bad_qids:
        print("\n🔴 有顯著重疊的題目：")
        for qid, ov in bad_qids:
            print(f"  {qid}: max overlap = {ov:.1f}s")


if __name__ == "__main__":
    main()
