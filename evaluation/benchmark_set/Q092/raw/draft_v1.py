# [VISUAL REASONING]
# Visualize the decimal-point shift to derive the exponent, then symbolically sum a+n.
# Sequential in-place transforms keep cognitive load low.
# Uses ReplacementTransform for equation evolution, cleanup before next, Circumscribe highlights.

from manim import *

class SubtitleManager:
    """Auto-injected by RefiningLoop.pre_render_patch. Prevents subtitle overlap and implements YT-style chunking."""
    MAX_WIDTH = 12.5

    def __init__(self, scene, font_size=28):
        self.scene = scene
        self.font_size = font_size
        self._current = None
        self._y = 3.2 * DOWN

    def show(self, text_str, run_time=1.0):
        import re
        FADE_IN = 0.10
        FADE_BETWEEN = 0.08

        # Break text into chunks by punctuation (keeping the punctuation)
        parts = re.split(r'([，。！？,\.!?]+)', str(text_str))
        sentences = []
        for i in range(0, len(parts)-1, 2):
            sentences.append((parts[i] + parts[i+1]).strip())
        if len(parts) % 2 == 1 and parts[-1].strip():
            sentences.append(parts[-1].strip())

        # 過濾空字串，確保 is_last 判斷正確
        sentences = [s for s in sentences if s]
        if not sentences:
            return

        total_len = sum(len(s) for s in sentences)
        n = len(sentences)

        # run_time = 字幕總存活時間（= TTS 時長），字幕要撐滿這段時間
        time_cursor = 0.0

        for idx, s in enumerate(sentences):

            text_mob = Text(s, font_size=self.font_size, color=WHITE, weight="BOLD")
            bg = BackgroundRectangle(text_mob, color=BLACK, fill_opacity=0.75, buff=0.15)
            new_mob = VGroup(bg, text_mob).move_to(self._y)
            if new_mob.width > self.MAX_WIDTH:
                new_mob.scale_to_fit_width(self.MAX_WIDTH)

            is_last = (idx == n - 1)

            if self._current is None:
                self.scene.play(FadeIn(new_mob), run_time=FADE_IN)
                time_cursor += FADE_IN
            else:
                self.scene.play(
                    FadeOut(self._current, run_time=FADE_BETWEEN / 2),
                    FadeIn(new_mob, run_time=FADE_BETWEEN / 2),
                )
                time_cursor += FADE_BETWEEN

            self._current = new_mob

            if not is_last:
                # 按字數比例分配時間給非最後一句
                chunk_ratio = len(s) / max(1, total_len)
                hold = run_time * chunk_ratio - (FADE_IN if idx == 0 else FADE_BETWEEN)
                if hold > 0:
                    self.scene.wait(hold)
                    time_cursor += hold
            else:
                # 最後一句：把剩餘時間全用掉，確保字幕撐到 TTS 結束
                remaining = run_time - time_cursor
                if remaining > 0:
                    self.scene.wait(remaining)

    def clear(self, run_time=0.5):
        if self._current is not None:
            anim_time = min(0.2, run_time)
            self.scene.play(FadeOut(self._current), run_time=anim_time)
            if run_time > anim_time:
                self.scene.wait(run_time - anim_time)
            self._current = None


class SceneInstrumentor:
    """Auto-injected by RefiningLoop.pre_render_patch to quantitatively track object overlap."""
    def __init__(self, scene, log_path="scene_state_log.json"):
        import json
        self._scene = scene
        self._log_path = log_path
        self._log = []
        self._step = 0
        self._original_play = scene.play
        scene.play = self._instrumented_play

    def _instrumented_play(self, *anims, **kwargs):
        result = self._original_play(*anims, **kwargs)
        self._step += 1
        snapshot = {"step": self._step, "mobjects": []}

        for mob in getattr(self._scene, "mobjects", []):
            # Manim v0.20.0: __getattr__ wraps deprecated getters, making hasattr() unreliable.
            # get_fill_opacity() may raise AttributeError or return None on internal mobjects.
            # Use try/except + (val or 0) to handle both cases robustly.
            try:
                opacity = (mob.get_fill_opacity() or 0) + (mob.get_stroke_opacity() or 0)
            except Exception:
                opacity = 1.0  # assume visible if opacity cannot be determined
                 
            if opacity <= 0.01 or type(mob).__name__ == "BackgroundRectangle":
                continue
            try:
                w, h = mob.width, mob.height
                if w * h < 0.05: continue
                c = mob.get_center().tolist()
                snapshot["mobjects"].append({
                    "type": type(mob).__name__, "width": round(w, 3), "height": round(h, 3),
                    "center": [round(c[0], 3), round(c[1], 3), round(c[2], 3)], "area": round(w * h, 3)
                })
            except Exception: pass
            
        snapshot["n_mobjects_visible"] = len(snapshot["mobjects"])
        oc = 0
        mobs = snapshot["mobjects"]
        for i in range(len(mobs)):
            for j in range(i + 1, len(mobs)):
                m1, m2 = mobs[i], mobs[j]
                ho = (abs(m1["center"][0] - m2["center"][0]) * 2 < (m1["width"] + m2["width"]))
                vo = (abs(m1["center"][1] - m2["center"][1]) * 2 < (m1["height"] + m2["height"]))
                if ho and vo: oc += 1
                
        snapshot["overlap_pairs"] = oc
        snapshot["total_screen_coverage"] = sum(m["area"] for m in mobs)
        self._log.append(snapshot)
        
        try:
            import json
            with open(self._log_path, "w", encoding="utf-8") as f:
                json.dump({
                    "max_simultaneous_objects": max((s["n_mobjects_visible"] for s in self._log), default=0),
                    "max_overlap_pairs": max((s["overlap_pairs"] for s in self._log), default=0),
                    "steps_with_overlap": sum(1 for s in self._log if s["overlap_pairs"] > 0),
                    "peak_screen_coverage": max((s["total_screen_coverage"] for s in self._log), default=0),
                    "timeline": self._log
                }, f, indent=2)
        except Exception: pass
        return result


class GeneratedScene(Scene):
    def construct(self):
        self._instrumentor = SceneInstrumentor(self, log_path='/Users/liaozhenting/Desktop/LLManim_Agent/scene_state_log.json')
        self._sm = SubtitleManager(self)
        self.set_subtitle = self._sm.show
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/_3_5_be751d9880/step_00.mp3")  # [auto-injected] duration=7.97s
        _audio_dur_0 = 7.97  # [audio-sync] actual TTS duration
        # Step 1
        title = Text("Scientific Notation: Find a + n", color=WHITE, font_size=38).to_edge(UP, buff=0.6)
        self.set_subtitle("我們要將 0.0000025 寫成科學記號，並求出 a 加 n 的值。", run_time=_audio_dur_0)
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/_3_5_be751d9880/step_01.mp3")  # [auto-injected] duration=6.29s
        _audio_dur_1 = 6.29  # [audio-sync] actual TTS duration
        # Step 2
        format_hint = MathTex(r"a \times 10^n, \; 1 \le a < 10", color=BLUE).move_to(ORIGIN + np.array([0, -2.2, 0]))
        self.set_subtitle("科學記號的形式是 a 乘以 10 的 n 次方，其中 a 介於 1 到 10 之間。", run_time=_audio_dur_1)
        anim_time_2 = 1.5
        self.play(Write(format_hint), run_time=1.5)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/_3_5_be751d9880/step_02.mp3")  # [auto-injected] duration=9.94s
        _audio_dur_2 = 9.94  # [audio-sync] actual TTS duration
        # Step 3
        step_label = Text("Step 1: Original number", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq_original = MathTex("0.0000025", color=WHITE).move_to(ORIGIN)
        self.set_subtitle("從 0.0000025 開始，將小數點向右移動 6 位變成 2.5。", run_time=_audio_dur_2)
        anim_time_3 = 1.5
        self.play(Write(step_label), Write(eq_original), run_time=1.5)
        self.play(Circumscribe(eq_original, color=YELLOW))
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/_3_5_be751d9880/step_03.mp3")  # [auto-injected] duration=13.08s
        _audio_dur_3 = 13.08  # [audio-sync] actual TTS duration
        # Step 4
        eq_shifted = MathTex(r"0.0000025 = 2.5 \times 10^{-6}", color=WHITE).move_to(ORIGIN)
        self.set_subtitle("向右移動 6 位代表乘以 10 的負 6 次方，所以 0.0000025 等於 2.5 乘以 10 的負 6 次方。", run_time=_audio_dur_3)
        anim_time_4 = 2.0
        self.play(ReplacementTransform(eq_original, eq_shifted), run_time=2.0)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/_3_5_be751d9880/step_04.mp3")  # [auto-injected] duration=9.82s
        _audio_dur_4 = 9.82  # [audio-sync] actual TTS duration
        # Step 5
        eq_sum = MathTex(r"a + n = 2.5 + (-6) = -3.5", color=WHITE).move_to(ORIGIN)
        self.set_subtitle("比較後得到 a 等於 2.5，n 等於負 6，相加得到 a 加 n 等於負 3.5。", run_time=_audio_dur_4)
        anim_time_5 = 2.0
        self.play(FadeOut(format_hint), ReplacementTransform(eq_shifted, eq_sum), run_time=2.0)
        self.play(Circumscribe(eq_sum, color=GREEN))
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))