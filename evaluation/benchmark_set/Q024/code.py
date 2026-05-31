# [VISUAL REASONING]
# Anchor one equation at center and morph it through each transformation via ReplacementTransform.
# Step label sits above, explanation below, title at top. Final answer boxed in green.

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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/evaluation/benchmark_set/Q024/raw/tts_regen/step_00.mp3")  # [regen] duration=7.75s
        _audio_dur_0 = 7.75  # [audio-sync] actual TTS duration
        self.set_subtitle("我們從這個算式開始：-7/18 × 2 4/7，再 ÷ -1 1/3。", run_time=_audio_dur_0)
        # Step 1
        title = Text("Mixed Fraction Multiplication & Division", color=WHITE, font_size=34).to_edge(UP, buff=0.5)
        eq_original = MathTex(r"\left(-\frac{7}{18}\right) \times 2\frac{4}{7} \div \left(-1\frac{1}{3}\right)", color=WHITE).scale(0.9).move_to(ORIGIN)

        anim_time_1 = 2.5
        self.play(Write(title), run_time=0.8)
        self.play(Write(eq_original), run_time=2.5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/evaluation/benchmark_set/Q024/raw/tts_regen/step_01.mp3")  # [regen] duration=10.97s
        self.wait(max(0.1, _audio_dur_0 - 3.30))
        _audio_dur_1 = 10.97  # [audio-sync] actual TTS duration
        self.set_subtitle("首先，將每個帶分數化為假分數。2 4/7 = 7/18，-1 1/3 = -4/3。", run_time=_audio_dur_1)
        # Step 2
        step_label_1 = Text("Step 1: Convert mixed numbers to improper fractions", color=YELLOW, font_size=26).move_to([0, 1.8, 0])
        explain_1 = Text("2 4/7 = 18/7 and -1 1/3 = -4/3", color=WHITE, font_size=24).move_to([0, -2.3, 0])
        eq_improper = MathTex(r"\left(-\frac{7}{18}\right) \times \frac{18}{7} \div \left(-\frac{4}{3}\right)", color=WHITE).scale(0.9).move_to(ORIGIN)

        anim_time_2 = 4.0
        self.play(Circumscribe(eq_original, color=YELLOW), run_time=1.2)
        self.play(FadeIn(step_label_1), FadeIn(explain_1), run_time=0.5)
        self.play(ReplacementTransform(eq_original, eq_improper), run_time=2.3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/evaluation/benchmark_set/Q024/raw/tts_regen/step_02.mp3")  # [regen] duration=8.28s
        self.wait(max(0.1, _audio_dur_1 - 4.00))
        _audio_dur_2 = 8.28  # [audio-sync] actual TTS duration
        self.set_subtitle("接著，把除法改為乘以倒數。÷ -4/3 = × -3/4。", run_time=_audio_dur_2)
        # Step 3
        step_label_2 = Text("Step 2: Convert division to multiplication by reciprocal", color=YELLOW, font_size=26).move_to([0, 1.8, 0])
        explain_2 = Text("Dividing by -4/3 is multiplying by -3/4", color=WHITE, font_size=24).move_to([0, -2.3, 0])
        eq_reciprocal = MathTex(r"\left(-\frac{7}{18}\right) \times \frac{18}{7} \times \left(-\frac{3}{4}\right)", color=WHITE).scale(0.9).move_to(ORIGIN)

        anim_time_3 = 4.0
        self.play(FadeOut(step_label_1), FadeOut(explain_1), run_time=0.5)
        self.play(Indicate(eq_improper, color=RED), run_time=1.0)
        self.play(FadeIn(step_label_2), FadeIn(explain_2), run_time=0.5)
        self.play(ReplacementTransform(eq_improper, eq_reciprocal), run_time=2.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/evaluation/benchmark_set/Q024/raw/tts_regen/step_03.mp3")  # [regen] duration=6.65s
        self.wait(max(0.1, _audio_dur_2 - 4.00))
        _audio_dur_3 = 6.65  # [audio-sync] actual TTS duration
        self.set_subtitle("負負得正。前兩個分數相乘剛好消去，結果是 -1。", run_time=_audio_dur_3)
        # Step 4
        step_label_3 = Text("Step 3: Two negatives make a positive; cancel terms", color=YELLOW, font_size=26).move_to([0, 1.8, 0])
        explain_3 = Text("(-7/18) x (18/7) = -1", color=WHITE, font_size=24).move_to([0, -2.3, 0])
        eq_simplified = MathTex(r"(-1) \times \left(-\frac{3}{4}\right)", color=WHITE).scale(0.9).move_to(ORIGIN)

        anim_time_4 = 4.0
        self.play(FadeOut(step_label_2), FadeOut(explain_2), run_time=0.5)
        self.play(Circumscribe(eq_reciprocal, color=BLUE), run_time=1.2)
        self.play(FadeIn(step_label_3), FadeIn(explain_3), run_time=0.5)
        self.play(ReplacementTransform(eq_reciprocal, eq_simplified), run_time=1.8)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/evaluation/benchmark_set/Q024/raw/tts_regen/step_04.mp3")  # [regen] duration=6.46s
        self.wait(max(0.1, _audio_dur_3 - 4.00))
        _audio_dur_4 = 6.46  # [audio-sync] actual TTS duration
        self.set_subtitle("最後，-1 × -3/4，得到正的答案：3/4。", run_time=_audio_dur_4)
        # Step 5
        step_label_4 = Text("Step 4: Final result", color=YELLOW, font_size=26).move_to([0, 1.8, 0])
        explain_4 = Text("(-1) x (-3/4) = 3/4", color=WHITE, font_size=24).move_to([0, -2.3, 0])
        eq_final = MathTex(r"= \frac{3}{4}", color=GREEN).scale(0.9).move_to(ORIGIN)

        anim_time_5 = 3.5
        self.play(FadeOut(step_label_3), FadeOut(explain_3), run_time=0.5)
        self.play(FadeIn(step_label_4), FadeIn(explain_4), run_time=0.5)
        self.play(ReplacementTransform(eq_simplified, eq_final), run_time=1.5)
        answer_box = SurroundingRectangle(eq_final, color=GREEN, buff=0.2)
        self.play(Create(answer_box), run_time=1.0)
        self.wait(max(0.1, _audio_dur_4 - 3.50))
