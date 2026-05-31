# [VISUAL REASONING]
# Sequential equation morphing for nested arithmetic, with step labels (upper)
# and explanations (lower) guiding each transformation toward the final answer 36.

from manim import *

class SubtitleManager:
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
        parts = self._re.split(r'([，。！？,\.!?]+)', str(text))
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
        self.set_subtitle("我們要計算 24 - (-3) × [12 - (-4) × 3] ÷ 6。", run_time=_audio_dur_0)
        # Step 1
        title = Text("Order of Operations with Brackets", color=YELLOW, font_size=36).to_edge(UP, buff=0.5)
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_01.mp3")  # [auto-injected] duration=6.24s
        self.wait(max(0.1, _audio_dur_0 - 1.50))
        _audio_dur_1 = 6.24  # [audio-sync] actual TTS duration
        self.set_subtitle("這個算式含有中括號與小括號，要由內向外、先乘除後加減。", run_time=_audio_dur_1)
        # Step 2
        eq_original = MathTex(r"24 - (-3) \times [\,12 - (-4)\times 3\,] \div 6", color=WHITE).scale(0.9).move_to(ORIGIN)
        anim_time_2 = 2.0
        self.play(Write(eq_original), run_time=2.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_02.mp3")  # [auto-injected] duration=5.78s
        self.wait(max(0.1, _audio_dur_1 - 2.00))
        _audio_dur_2 = 5.78  # [audio-sync] actual TTS duration
        self.set_subtitle("第 1 步：先處理中括號內的乘法。", run_time=_audio_dur_2)
        # Step 3
        step_label_1 = Text("Step 1: Inner multiplication", color=BLUE, font_size=28).move_to([0, 1.8, 0])
        anim_time_3 = 1.0
        self.play(Circumscribe(eq_original, color=YELLOW))
        self.play(Write(step_label_1), run_time=1.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_03.mp3")  # [auto-injected] duration=3.62s
        self.wait(max(0.1, _audio_dur_2 - 2.00))
        _audio_dur_3 = 3.62  # [audio-sync] actual TTS duration
        self.set_subtitle("(-4) × 3 = -12，把中括號裡的乘法替換掉。", run_time=_audio_dur_3)
        # Step 4
        explain_1 = MathTex(r"(-4)\times 3 = -12", color=WHITE).move_to([0, -2.3, 0])
        anim_time_4 = 1.5
        self.play(Write(explain_1), run_time=1.5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_04.mp3")  # [auto-injected] duration=3.72s
        self.wait(max(0.1, _audio_dur_3 - 1.50))
        _audio_dur_4 = 3.72  # [audio-sync] actual TTS duration
        self.set_subtitle("原式變成 24 - (-3) × [12 - (-12)] ÷ 6。", run_time=_audio_dur_4)
        # Step 5
        eq_step1 = MathTex(r"24 - (-3) \times [\,12 - (-12)\,] \div 6", color=WHITE).scale(0.9).move_to(ORIGIN)
        anim_time_5 = 2.0
        self.play(ReplacementTransform(eq_original, eq_step1), run_time=2.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_05.mp3")  # [auto-injected] duration=6.14s
        self.wait(max(0.1, _audio_dur_4 - 2.00))
        _audio_dur_5 = 6.14  # [audio-sync] actual TTS duration
        self.set_subtitle("第 2 步：計算中括號內的減法。", run_time=_audio_dur_5)
        # Step 6
        step_label_2 = Text("Step 2: Subtract inside brackets", color=BLUE, font_size=28).move_to([0, 1.8, 0])
        anim_time_6 = 1.0
        self.play(FadeOut(step_label_1), FadeOut(explain_1))
        self.play(Indicate(eq_step1, color=YELLOW))
        self.play(Write(step_label_2), run_time=1.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_06.mp3")  # [auto-injected] duration=4.75s
        self.wait(max(0.1, _audio_dur_5 - 3.00))
        _audio_dur_6 = 4.75  # [audio-sync] actual TTS duration
        self.set_subtitle("12 - (-12) = 12 + 12 = 24，減去負數等於加上正數。", run_time=_audio_dur_6)
        # Step 7
        explain_2 = MathTex(r"12 - (-12) = 12 + 12 = 24", color=WHITE).move_to([0, -2.3, 0])
        anim_time_7 = 1.5
        self.play(Write(explain_2), run_time=1.5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_07.mp3")  # [auto-injected] duration=3.19s
        self.wait(max(0.1, _audio_dur_6 - 1.50))
        _audio_dur_7 = 3.19  # [audio-sync] actual TTS duration
        self.set_subtitle("中括號簡化為 24，原式變成 24 - (-3) × 24 ÷ 6。", run_time=_audio_dur_7)
        # Step 8
        eq_step2 = MathTex(r"24 - (-3) \times 24 \div 6", color=WHITE).scale(0.9).move_to(ORIGIN)
        anim_time_8 = 2.0
        self.play(ReplacementTransform(eq_step1, eq_step2), run_time=2.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_08.mp3")  # [auto-injected] duration=7.34s
        self.wait(max(0.1, _audio_dur_7 - 2.00))
        _audio_dur_8 = 7.34  # [audio-sync] actual TTS duration
        self.set_subtitle("第 3 步：乘除由左至右，先算乘法。", run_time=_audio_dur_8)
        # Step 9
        step_label_3 = Text("Step 3: Multiply left to right", color=BLUE, font_size=28).move_to([0, 1.8, 0])
        anim_time_9 = 1.0
        self.play(FadeOut(step_label_2), FadeOut(explain_2))
        self.play(Write(step_label_3), run_time=1.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_09.mp3")  # [auto-injected] duration=4.58s
        self.wait(max(0.1, _audio_dur_8 - 2.00))
        _audio_dur_9 = 4.58  # [audio-sync] actual TTS duration
        self.set_subtitle("(-3) × 24 = -72。", run_time=_audio_dur_9)
        # Step 10
        explain_3 = MathTex(r"(-3)\times 24 = -72", color=WHITE).move_to([0, -2.3, 0])
        anim_time_10 = 1.5
        self.play(Write(explain_3), run_time=1.5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_10.mp3")  # [auto-injected] duration=5.26s
        self.wait(max(0.1, _audio_dur_9 - 1.50))
        _audio_dur_10 = 5.26  # [audio-sync] actual TTS duration
        self.set_subtitle("原式變成 24 - (-72) ÷ 6。", run_time=_audio_dur_10)
        # Step 11
        eq_step3 = MathTex(r"24 - (-72) \div 6", color=WHITE).scale(0.9).move_to(ORIGIN)
        anim_time_11 = 2.0
        self.play(ReplacementTransform(eq_step2, eq_step3), run_time=2.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_11.mp3")  # [auto-injected] duration=7.99s
        self.wait(max(0.1, _audio_dur_10 - 2.00))
        _audio_dur_11 = 7.99  # [audio-sync] actual TTS duration
        self.set_subtitle("第 4 步：接著計算除法。", run_time=_audio_dur_11)
        # Step 12
        step_label_4 = Text("Step 4: Then divide", color=BLUE, font_size=28).move_to([0, 1.8, 0])
        anim_time_12 = 1.0
        self.play(FadeOut(step_label_3), FadeOut(explain_3))
        self.play(Write(step_label_4), run_time=1.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_12.mp3")  # [auto-injected] duration=2.62s
        self.wait(max(0.1, _audio_dur_11 - 2.00))
        _audio_dur_12 = 2.62  # [audio-sync] actual TTS duration
        self.set_subtitle("-72 ÷ 6 = -12。", run_time=_audio_dur_12)
        # Step 13
        explain_4 = MathTex(r"-72 \div 6 = -12", color=WHITE).move_to([0, -2.3, 0])
        anim_time_13 = 1.5
        self.play(Write(explain_4), run_time=1.5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_13.mp3")  # [auto-injected] duration=3.98s
        self.wait(max(0.1, _audio_dur_12 - 1.50))
        _audio_dur_13 = 3.98  # [audio-sync] actual TTS duration
        self.set_subtitle("原式簡化為 24 - (-12)。", run_time=_audio_dur_13)
        # Step 14
        eq_step4 = MathTex(r"24 - (-12)", color=WHITE).scale(0.9).move_to(ORIGIN)
        anim_time_14 = 2.0
        self.play(ReplacementTransform(eq_step3, eq_step4), run_time=2.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_14.mp3")  # [auto-injected] duration=6.48s
        self.wait(max(0.1, _audio_dur_13 - 2.00))
        _audio_dur_14 = 6.48  # [audio-sync] actual TTS duration
        self.set_subtitle("第 5 步：減去一個負數等於加上正數。", run_time=_audio_dur_14)
        # Step 15
        step_label_5 = Text("Step 5: Subtract a negative = add", color=BLUE, font_size=28).move_to([0, 1.8, 0])
        anim_time_15 = 1.0
        self.play(FadeOut(step_label_4), FadeOut(explain_4))
        self.play(Indicate(eq_step4, color=GREEN))
        self.play(Write(step_label_5), run_time=1.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_15.mp3")  # [auto-injected] duration=5.71s
        self.wait(max(0.1, _audio_dur_14 - 3.00))
        _audio_dur_15 = 5.71  # [audio-sync] actual TTS duration
        self.set_subtitle("24 - (-12) = 24 + 12 = 36。", run_time=_audio_dur_15)
        # Step 16
        explain_5 = MathTex(r"24 - (-12) = 24 + 12 = 36", color=GREEN).move_to([0, -2.3, 0])
        anim_time_16 = 1.5
        self.play(Write(explain_5), run_time=1.5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_16.mp3")  # [auto-injected] duration=3.02s
        self.wait(max(0.1, _audio_dur_15 - 1.50))
        _audio_dur_16 = 3.02  # [audio-sync] actual TTS duration
        self.set_subtitle("最終答案是 36。", run_time=_audio_dur_16)
        # Step 17
        eq_final = MathTex(r"= 36", color=GREEN).scale(0.9).move_to(ORIGIN)
        anim_time_17 = 2.0
        self.play(ReplacementTransform(eq_step4, eq_final), run_time=2.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__74ffaddc9c/step_17.mp3")  # [auto-injected] duration=4.66s
        self.wait(max(0.1, _audio_dur_16 - 2.00))
        _audio_dur_17 = 4.66  # [audio-sync] actual TTS duration
        self.set_subtitle("因此這道題的答案是 36。", run_time=_audio_dur_17)
        # Step 18
        final_box = SurroundingRectangle(eq_final, color=GREEN)
        anim_time_18 = 1.5
        self.play(Create(final_box), run_time=1.5)
        self.wait(max(0.1, _audio_dur_17 - 1.50))
