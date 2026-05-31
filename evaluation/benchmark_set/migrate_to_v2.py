"""把 30 題 code.py 遷移到 SubtitleManagerV2（非阻塞字幕）。

步驟：
1. 整段替換 SubtitleManager class（用 v2 實作，名稱保留 SubtitleManager）
2. 重排每分鏡時序：
   - 移除 set_subtitle 在 play 前的位置
   - 在 audio_dur_N = X 之後插 set_subtitle(text, run_time=_audio_dur_N)
   - 保留原本 self.play(...) 不變
   - 移除舊的 remaining_X / self.wait(remaining_X)
   - 在 play 之後插 self.wait(_audio_dur_N - anim_time_{N+1})
3. 備份原檔到 .py.v2-bak

用法：
  python evaluation/benchmark_set/migrate_to_v2.py             # dry-run
  python evaluation/benchmark_set/migrate_to_v2.py --apply
  python evaluation/benchmark_set/migrate_to_v2.py Q024 --apply
"""
from __future__ import annotations
import re, argparse
from pathlib import Path

BASE = Path(__file__).parent

# 新版 SubtitleManager（從 subtitle_manager_v2.py 抄，名稱改回 SubtitleManager）
NEW_SUBMGR = '''class SubtitleManager:
    """Non-blocking subtitle: shows in parallel with animation via add_updater."""
    MAX_WIDTH = 12.5
    Y_POSITION = 3.2 * DOWN
    FADE_DURATION = 0.15

    def __init__(self, scene, font_size=28):
        import re
        self.scene = scene
        self.font_size = font_size
        self._re = re
        self._active_drivers = []

    def _split_sentences(self, text):
        parts = self._re.split(r'([，。！？,\\.!?]+)', str(text))
        sentences = []
        for i in range(0, len(parts) - 1, 2):
            sentences.append((parts[i] + parts[i + 1]).strip())
        if len(parts) % 2 == 1 and parts[-1].strip():
            sentences.append(parts[-1].strip())
        return [s for s in sentences if s]

    def _make_mob(self, text):
        text_mob = Text(text, font_size=self.font_size, color=WHITE, weight="BOLD")
        bg = BackgroundRectangle(text_mob, color=BLACK, fill_opacity=0.75, buff=0.15)
        mob = VGroup(bg, text_mob).move_to(self.Y_POSITION)
        if mob.width > self.MAX_WIDTH:
            mob.scale_to_fit_width(self.MAX_WIDTH)
        return mob

    def show(self, text_str, run_time=1.0):
        """Non-blocking subtitle display for run_time seconds."""
        self._clear_active()
        sentences = self._split_sentences(text_str)
        if not sentences:
            return
        total_chars = sum(len(s) for s in sentences)

        intervals = []
        cursor = 0.0
        for s in sentences:
            seg = run_time * (len(s) / max(1, total_chars))
            intervals.append((cursor, cursor + seg))
            cursor += seg

        mobs = []
        for s, _ in zip(sentences, intervals):
            m = self._make_mob(s)
            m.set_opacity(0)
            self.scene.add(m)
            mobs.append(m)

        driver = Dot(radius=0.001).set_opacity(0).move_to(LEFT * 100)
        driver._sm_elapsed = 0.0
        driver._sm_run_time = run_time
        driver._sm_mobs = mobs
        driver._sm_intervals = intervals
        driver._sm_fade = self.FADE_DURATION
        driver._sm_scene = self.scene

        def _sub_updater(mob, dt):
            mob._sm_elapsed += dt
            t = mob._sm_elapsed
            for i, (start, end) in enumerate(mob._sm_intervals):
                tm = mob._sm_mobs[i]
                fd = mob._sm_fade
                if t < start:
                    op = 0.0
                elif t < start + fd:
                    op = (t - start) / fd
                elif t < end - fd:
                    op = 1.0
                elif t < end:
                    op = (end - t) / fd
                else:
                    op = 0.0
                tm.set_opacity(max(0.0, min(1.0, op)))
            if t >= mob._sm_run_time + 0.05:
                mob.clear_updaters()
                for tm in mob._sm_mobs:
                    if tm in mob._sm_scene.mobjects:
                        mob._sm_scene.remove(tm)
                if mob in mob._sm_scene.mobjects:
                    mob._sm_scene.remove(mob)

        driver.add_updater(_sub_updater)
        self.scene.add(driver)
        self._active_drivers.append(driver)

    def _clear_active(self):
        for d in list(self._active_drivers):
            try:
                d.clear_updaters()
                for m in getattr(d, "_sm_mobs", []):
                    if m in self.scene.mobjects:
                        self.scene.remove(m)
                if d in self.scene.mobjects:
                    self.scene.remove(d)
            except Exception:
                pass
        self._active_drivers.clear()

    def clear(self, run_time=0.0):
        self._clear_active()
'''


def replace_submgr(src: str) -> tuple[str, bool]:
    """整段替換 SubtitleManager class（從 `class SubtitleManager:` 到下個 `class ` 之前）。"""
    pattern = re.compile(
        r'class SubtitleManager:.*?(?=\nclass )',
        re.DOTALL,
    )
    new_src, count = pattern.subn(NEW_SUBMGR, src)
    return new_src, count > 0


def fix_scene_timing(src: str, max_n: int = 25) -> tuple[str, int]:
    """對每個分鏡 N 做時序修正：
    - 把 set_subtitle 從原位置移到 _audio_dur_N = X 那行的下一行
    - 把 self.play 後的 remaining_{N+1}/wait 改成 self.wait(audio_dur - anim_time)
    """
    fixed_count = 0
    for n in range(max_n):
        # 找這個分鏡的範圍：_audio_dur_N 到 (下個 _audio_dur 或檔尾)
        block_re = re.compile(
            rf'(        _audio_dur_{n} = [\d.]+  # \[audio-sync\] actual TTS duration\n)'
            rf'(.*?)'
            rf'(?=        _audio_dur_{n+1} = |\Z)',
            re.DOTALL,
        )
        m = block_re.search(src)
        if not m:
            continue
        audio_dur_line = m.group(1)
        block_body = m.group(2)

        # 抽出 set_subtitle(...) 字串本體
        # run_time 可能是 _audio_dur_N 或 max(0.5, ...)，所以要平衡括號
        sub_re = re.compile(
            rf'        self\.set_subtitle\((.*?), run_time=(?:_audio_dur_{n}|max\([^)]+\))\)\n?',
            re.DOTALL,
        )
        sub_match = sub_re.search(block_body)
        if not sub_match:
            continue
        subtitle_arg = sub_match.group(1)
        # 移除原 set_subtitle 行
        block_body = sub_re.sub('', block_body, count=1)

        # 移除舊的 remaining/wait pair
        remaining_re = re.compile(
            rf'        remaining_{n+1} = max\(0\.1, _audio_dur_{n} - anim_time_{n+1}[^)]*\)\n'
            rf'        self\.wait\(max\(0\.1, remaining_{n+1}\)\)\n?',
        )
        block_body = remaining_re.sub('', block_body)

        # 移除舊的 max(0.5, _audio_dur - anim_time) 補時間 wait（我們會重新加）
        old_wait_re = re.compile(
            rf'        self\.wait\(max\(0\.5, _audio_dur_{n} - anim_time_{n+1}\)\)\n',
        )
        block_body = old_wait_re.sub('', block_body)

        # 找 anim_time_{N+1}（如果有）
        at_match = re.search(rf'anim_time_{n+1} = ([\d.]+)', block_body)
        if at_match:
            anim_time_var = f'anim_time_{n+1}'
        else:
            anim_time_var = '0'  # 沒 anim_time 就當 0

        # 新版分鏡：
        # _audio_dur_N = X
        # self.set_subtitle(text, run_time=_audio_dur_N)
        # <原本的物件創建 + play>
        # self.wait(max(0.1, _audio_dur_N - anim_time_{N+1}))
        new_block_body = (
            f'        self.set_subtitle({subtitle_arg}, run_time=_audio_dur_{n})\n'
            + block_body.rstrip('\n')
            + '\n'
            + f'        self.wait(max(0.1, _audio_dur_{n} - {anim_time_var}))\n'
        )

        new_section = audio_dur_line + new_block_body
        src = src[:m.start()] + new_section + src[m.end():]
        fixed_count += 1

    return src, fixed_count


def process_file(path: Path) -> tuple[str, str, int, bool]:
    src = path.read_text(encoding="utf-8")
    new_src, replaced = replace_submgr(src)
    new_src, fixed = fix_scene_timing(new_src)
    return src, new_src, fixed, replaced


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qids", nargs="*")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if args.qids:
        targets = [BASE / q for q in args.qids]
    else:
        targets = sorted(d for d in BASE.iterdir() if d.is_dir() and d.name.startswith("Q"))

    print(f"{'QID':<8}{'SubMgr 替換':<14}{'分鏡修':<10}")
    print("-" * 40)
    total_fixed = 0
    for qd in targets:
        code = qd / "code.py"
        if not code.exists(): continue
        orig, new, fixed, replaced = process_file(code)
        total_fixed += fixed
        rep_str = "✅" if replaced else "❌"
        print(f"{qd.name:<8}{rep_str:<14}{fixed:<10}")

        if args.apply:
            bak = code.with_suffix(".py.v2-bak")
            if not bak.exists():
                bak.write_text(orig, encoding="utf-8")
            code.write_text(new, encoding="utf-8")

    print(f"\n總計：{total_fixed} 個分鏡修正")
    if args.apply:
        print("✓ 已寫入（備份在 .py.v2-bak）")
    else:
        print("Dry-run。確認 OK 後加 --apply。")


if __name__ == "__main__":
    main()
