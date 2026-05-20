# [VISUAL REASONING]
# Sequential equation morphing for nested arithmetic, with step labels (upper)
# and explanations (lower) guiding each transformation toward the final answer 36.

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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_00.mp3")  # [auto-injected] duration=5.64s
        _audio_dur_0 = 5.64  # [audio-sync] actual TTS duration
        # Step 1
        title = Text("Order of Operations with Brackets", color=YELLOW, font_size=36).to_edge(UP, buff=0.5)
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_01.mp3")  # [auto-injected] duration=6.24s
        _audio_dur_1 = 6.24  # [audio-sync] actual TTS duration
        # Step 2
        eq_original = MathTex(r"-(-3) \times [\,12 - (-4)\times 3\,] \div 6", color=WHITE).scale(0.9).move_to(ORIGIN)
        anim_time_2 = 2.0
        self.play(Write(eq_original), run_time=2.0)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_02.mp3")  # [auto-injected] duration=5.78s
        _audio_dur_2 = 5.78  # [audio-sync] actual TTS duration
        # Step 3
        step_label_1 = Text("Step 1: Inner multiplication", color=BLUE, font_size=28).move_to([0, 1.8, 0])
        anim_time_3 = 1.0
        self.play(Circumscribe(eq_original, color=YELLOW))
        self.play(Write(step_label_1), run_time=1.0)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_03.mp3")  # [auto-injected] duration=3.62s
        _audio_dur_3 = 3.62  # [audio-sync] actual TTS duration
        # Step 4
        explain_1 = MathTex(r"(-4)\times 3 = -12", color=WHITE).move_to([0, -2.3, 0])
        anim_time_4 = 1.5
        self.play(Write(explain_1), run_time=1.5)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_04.mp3")  # [auto-injected] duration=3.72s
        _audio_dur_4 = 3.72  # [audio-sync] actual TTS duration
        # Step 5
        eq_step1 = MathTex(r"-(-3) \times [\,12 - (-12)\,] \div 6", color=WHITE).scale(0.9).move_to(ORIGIN)
        anim_time_5 = 2.0
        self.play(ReplacementTransform(eq_original, eq_step1), run_time=2.0)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_05.mp3")  # [auto-injected] duration=6.14s
        _audio_dur_5 = 6.14  # [audio-sync] actual TTS duration
        # Step 6
        step_label_2 = Text("Step 2: Subtract inside brackets", color=BLUE, font_size=28).move_to([0, 1.8, 0])
        anim_time_6 = 1.0
        self.play(FadeOut(step_label_1), FadeOut(explain_1))
        self.play(Indicate(eq_step1, color=YELLOW))
        self.play(Write(step_label_2), run_time=1.0)
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_06.mp3")  # [auto-injected] duration=4.75s
        _audio_dur_6 = 4.75  # [audio-sync] actual TTS duration
        # Step 7
        explain_2 = MathTex(r"12 - (-12) = 12 + 12 = 24", color=WHITE).move_to([0, -2.3, 0])
        anim_time_7 = 1.5
        self.play(Write(explain_2), run_time=1.5)
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_07.mp3")  # [auto-injected] duration=3.19s
        _audio_dur_7 = 3.19  # [audio-sync] actual TTS duration
        # Step 8
        eq_step2 = MathTex(r"-(-3) \times 24 \div 6", color=WHITE).scale(0.9).move_to(ORIGIN)
        anim_time_8 = 2.0
        self.play(ReplacementTransform(eq_step1, eq_step2), run_time=2.0)
        remaining_8 = max(0.1, _audio_dur_7 - anim_time_8 + 0.5)
        self.wait(max(0.1, remaining_8))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_08.mp3")  # [auto-injected] duration=7.34s
        _audio_dur_8 = 7.34  # [audio-sync] actual TTS duration
        # Step 9
        step_label_3 = Text("Step 3: Multiply left to right", color=BLUE, font_size=28).move_to([0, 1.8, 0])
        anim_time_9 = 1.0
        self.play(FadeOut(step_label_2), FadeOut(explain_2))
        self.play(Write(step_label_3), run_time=1.0)
        remaining_9 = max(0.1, _audio_dur_8 - anim_time_9 + 0.5)
        self.wait(max(0.1, remaining_9))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_09.mp3")  # [auto-injected] duration=4.58s
        _audio_dur_9 = 4.58  # [audio-sync] actual TTS duration
        # Step 10
        explain_3 = MathTex(r"(-3)\times 24 = -72", color=WHITE).move_to([0, -2.3, 0])
        anim_time_10 = 1.5
        self.play(Write(explain_3), run_time=1.5)
        remaining_10 = max(0.1, _audio_dur_9 - anim_time_10 + 0.5)
        self.wait(max(0.1, remaining_10))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_10.mp3")  # [auto-injected] duration=5.26s
        _audio_dur_10 = 5.26  # [audio-sync] actual TTS duration
        # Step 11
        eq_step3 = MathTex(r"-(-72) \div 6", color=WHITE).scale(0.9).move_to(ORIGIN)
        anim_time_11 = 2.0
        self.play(ReplacementTransform(eq_step2, eq_step3), run_time=2.0)
        remaining_11 = max(0.1, _audio_dur_10 - anim_time_11 + 0.5)
        self.wait(max(0.1, remaining_11))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_11.mp3")  # [auto-injected] duration=7.99s
        _audio_dur_11 = 7.99  # [audio-sync] actual TTS duration
        # Step 12
        step_label_4 = Text("Step 4: Then divide", color=BLUE, font_size=28).move_to([0, 1.8, 0])
        anim_time_12 = 1.0
        self.play(FadeOut(step_label_3), FadeOut(explain_3))
        self.play(Write(step_label_4), run_time=1.0)
        remaining_12 = max(0.1, _audio_dur_11 - anim_time_12 + 0.5)
        self.wait(max(0.1, remaining_12))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_12.mp3")  # [auto-injected] duration=2.62s
        _audio_dur_12 = 2.62  # [audio-sync] actual TTS duration
        # Step 13
        explain_4 = MathTex(r"-72 \div 6 = -12", color=WHITE).move_to([0, -2.3, 0])
        anim_time_13 = 1.5
        self.play(Write(explain_4), run_time=1.5)
        remaining_13 = max(0.1, _audio_dur_12 - anim_time_13 + 0.5)
        self.wait(max(0.1, remaining_13))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_13.mp3")  # [auto-injected] duration=3.98s
        _audio_dur_13 = 3.98  # [audio-sync] actual TTS duration
        # Step 14
        eq_step4 = MathTex(r"-(-12)", color=WHITE).scale(0.9).move_to(ORIGIN)
        anim_time_14 = 2.0
        self.play(ReplacementTransform(eq_step3, eq_step4), run_time=2.0)
        remaining_14 = max(0.1, _audio_dur_13 - anim_time_14 + 0.5)
        self.wait(max(0.1, remaining_14))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_14.mp3")  # [auto-injected] duration=6.48s
        _audio_dur_14 = 6.48  # [audio-sync] actual TTS duration
        # Step 15
        step_label_5 = Text("Step 5: Subtract a negative = add", color=BLUE, font_size=28).move_to([0, 1.8, 0])
        anim_time_15 = 1.0
        self.play(FadeOut(step_label_4), FadeOut(explain_4))
        self.play(Indicate(eq_step4, color=GREEN))
        self.play(Write(step_label_5), run_time=1.0)
        remaining_15 = max(0.1, _audio_dur_14 - anim_time_15 + 0.5)
        self.wait(max(0.1, remaining_15))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_15.mp3")  # [auto-injected] duration=5.71s
        _audio_dur_15 = 5.71  # [audio-sync] actual TTS duration
        # Step 16
        explain_5 = MathTex(r"-(-12) = 24 + 12 = 36", color=GREEN).move_to([0, -2.3, 0])
        anim_time_16 = 1.5
        self.play(Write(explain_5), run_time=1.5)
        remaining_16 = max(0.1, _audio_dur_15 - anim_time_16 + 0.5)
        self.wait(max(0.1, remaining_16))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_16.mp3")  # [auto-injected] duration=3.02s
        _audio_dur_16 = 3.02  # [audio-sync] actual TTS duration
        # Step 17
        eq_final = MathTex(r"= 36", color=GREEN).scale(0.9).move_to(ORIGIN)
        anim_time_17 = 2.0
        self.play(ReplacementTransform(eq_step4, eq_final), run_time=2.0)
        remaining_17 = max(0.1, _audio_dur_16 - anim_time_17 + 0.5)
        self.wait(max(0.1, remaining_17))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_17.mp3")  # [auto-injected] duration=4.66s
        _audio_dur_17 = 4.66  # [audio-sync] actual TTS duration
        # Step 18
        final_box = SurroundingRectangle(eq_final, color=GREEN)
        anim_time_18 = 1.5
        self.play(Create(final_box), run_time=1.5)
        remaining_18 = max(0.1, _audio_dur_17 - anim_time_18 + 0.5)
        self.wait(max(0.1, remaining_18))