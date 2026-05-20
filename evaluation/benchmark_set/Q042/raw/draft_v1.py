# [VISUAL REASONING]
# Central focus equation morphing through stages: 24×(-5) → -(24×5) → -(120) → -120
# Title at top, sign rule reminder above equation, final answer boxed in green.
# Uses ReplacementTransform for smooth morphs; Circumscribe/Indicate for emphasis.

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
        title = Text("Multiplying Signed Numbers: 24 × (-5)", color=WHITE, font_size=36).to_edge(UP, buff=0.5)
        sign_rule = MathTex("(+)\\times(-) = (-)", color=YELLOW).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq_start = MathTex("24 \\times (-5)", color=WHITE).move_to(ORIGIN)
        eq_split = MathTex("-\\,(24 \\times 5)", color=WHITE).move_to(ORIGIN)
        eq_mult = MathTex("-\\,(120)", color=WHITE).move_to(ORIGIN)
        eq_final = MathTex("-120", color=GREEN).move_to(ORIGIN)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__46b29b0cb3/step_00.mp3")  # [auto-injected] duration=4.58s
        _audio_dur_0 = 4.58  # [audio-sync] actual TTS duration
        # Step 1
        self.set_subtitle("我們要計算 24 乘以負 5。", run_time=_audio_dur_0)
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__46b29b0cb3/step_01.mp3")  # [auto-injected] duration=4.42s
        _audio_dur_1 = 4.42  # [audio-sync] actual TTS duration
        # Step 2
        self.set_subtitle("這是我們的算式：24 乘以負 5。", run_time=_audio_dur_1)
        anim_time_2 = 1.5
        self.play(Write(eq_start), run_time=1.5)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__46b29b0cb3/step_02.mp3")  # [auto-injected] duration=5.50s
        _audio_dur_2 = 5.50  # [audio-sync] actual TTS duration
        # Step 3
        self.set_subtitle("正數乘以負數等於負數，所以我們把負號提出來。", run_time=_audio_dur_2)
        anim_time_3 = 1.5
        self.play(Write(sign_rule), run_time=1.5)
        self.play(Circumscribe(sign_rule, color=YELLOW))
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__46b29b0cb3/step_03.mp3")  # [auto-injected] duration=4.37s
        _audio_dur_3 = 4.37  # [audio-sync] actual TTS duration
        # Step 4
        self.set_subtitle("改寫之後，得到負的 24 乘以 5。", run_time=_audio_dur_3)
        anim_time_4 = 1.5
        self.play(ReplacementTransform(eq_start, eq_split), run_time=1.5)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__46b29b0cb3/step_04.mp3")  # [auto-injected] duration=6.62s
        _audio_dur_4 = 6.62  # [audio-sync] actual TTS duration
        # Step 5
        self.set_subtitle("因為 24 乘以 5 等於 120，所以答案是負 120。", run_time=_audio_dur_4)
        anim_time_5 = 1.5
        self.play(
            ReplacementTransform(eq_split, eq_mult),
            FadeOut(sign_rule),
            run_time=1.5
        )
        self.play(Indicate(eq_mult, color=RED))
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__46b29b0cb3/step_05.mp3")  # [auto-injected] duration=5.59s
        _audio_dur_5 = 5.59  # [audio-sync] actual TTS duration
        # Step 6
        self.set_subtitle("因此，24 乘以負 5 等於負 120。", run_time=_audio_dur_5)
        anim_time_6 = 1.5
        self.play(ReplacementTransform(eq_mult, eq_final), run_time=1.5)
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__46b29b0cb3/step_06.mp3")  # [auto-injected] duration=3.82s
        _audio_dur_6 = 3.82  # [audio-sync] actual TTS duration
        # Step 7
        self.set_subtitle("我們的最終答案是負 120。", run_time=_audio_dur_6)
        answer_box = SurroundingRectangle(eq_final, color=GREEN)
        anim_time_7 = 1.2
        self.play(Create(answer_box), run_time=1.2)
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 + 0.5)
        self.wait(max(0.1, remaining_7))