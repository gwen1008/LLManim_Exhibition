# [VISUAL REASONING]
# Single-anchor in-place transformation of the expression through PEMDAS steps.
# Each step shows a label, transforms the equation, and displays a footer explanation.
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
        # Object creation
        title = Text("Order of Operations", color=WHITE, font_size=38).to_edge(UP, buff=0.5)
        eq0 = MathTex(r"38 - 48 \div (-6 - 2) \times 3", color=WHITE).move_to(ORIGIN)
        eq1 = MathTex(r"38 - 48 \div (-8) \times 3", color=WHITE).move_to(ORIGIN)
        eq2 = MathTex(r"38 - (-6) \times 3", color=WHITE).move_to(ORIGIN)
        eq3 = MathTex(r"38 - (-18)", color=WHITE).move_to(ORIGIN)
        eq4 = MathTex(r"38 + 18 = 56", color=YELLOW).move_to(ORIGIN)
        step_label1 = Text("Step 1: Brackets first", color=BLUE, font_size=28).move_to(ORIGIN + np.array([0, 1.5, 0]))
        step_label2 = Text("Step 2: Division (left to right)", color=BLUE, font_size=28).move_to(ORIGIN + np.array([0, 1.5, 0]))
        step_label3 = Text("Step 3: Multiplication", color=BLUE, font_size=28).move_to(ORIGIN + np.array([0, 1.5, 0]))
        step_label4 = Text("Step 4: Subtraction", color=BLUE, font_size=28).move_to(ORIGIN + np.array([0, 1.5, 0]))
        footer1 = Text("-6 - 2 = -8", color=GREEN, font_size=28).move_to(ORIGIN + np.array([0, -2.3, 0]))
        footer2 = Text("48 ÷ (-8) = -6", color=GREEN, font_size=28).move_to(ORIGIN + np.array([0, -2.3, 0]))
        footer3 = Text("(-6) × 3 = -18", color=GREEN, font_size=28).move_to(ORIGIN + np.array([0, -2.3, 0]))
        footer4 = Text("Subtracting a negative = adding a positive", color=GREEN, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__e2cdcbba22/step_00.mp3")  # [auto-injected] duration=7.44s
        _audio_dur_0 = 7.44  # [audio-sync] actual TTS duration
        self.set_subtitle("我們要計算 38 - 48 ÷ 括號內 -6 - 2，再 × 3。", run_time=_audio_dur_0)
        # Step 1
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__e2cdcbba22/step_01.mp3")  # [auto-injected] duration=6.24s
        self.wait(max(0.1, _audio_dur_0 - 1.50))
        _audio_dur_1 = 6.24  # [audio-sync] actual TTS duration
        self.set_subtitle("這是我們的原始算式，讓我們仔細應用運算順序。", run_time=_audio_dur_1)
        # Step 2
        anim_time_2 = 2.0
        self.play(Write(eq0), run_time=2.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__e2cdcbba22/step_02.mp3")  # [auto-injected] duration=8.18s
        self.wait(max(0.1, _audio_dur_1 - 2.00))
        _audio_dur_2 = 8.18  # [audio-sync] actual TTS duration
        self.set_subtitle("步驟 1：括號優先。計算 -6 - 2 = -8。", run_time=_audio_dur_2)
        # Step 3
        self.play(Circumscribe(eq0, color=YELLOW))
        anim_time_3 = 1.0 + 1.2
        self.play(Write(step_label1), run_time=1.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__e2cdcbba22/step_03.mp3")  # [auto-injected] duration=8.02s
        self.wait(max(0.1, _audio_dur_2 - 2.00))
        _audio_dur_3 = 8.02  # [audio-sync] actual TTS duration
        self.set_subtitle("括號變成 -8，算式變為 38 - 48 ÷ -8 × 3。", run_time=_audio_dur_3)
        # Step 4
        anim_time_4 = 1.8 + 0.8
        self.play(ReplacementTransform(eq0, eq1), run_time=1.8)
        self.play(Write(footer1), run_time=0.8)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__e2cdcbba22/step_04.mp3")  # [auto-injected] duration=10.44s
        self.wait(max(0.1, _audio_dur_3 - 2.60))
        _audio_dur_4 = 10.44  # [audio-sync] actual TTS duration
        self.set_subtitle("步驟 2：乘除由左至右。先除：48 ÷ -8 = -6。", run_time=_audio_dur_4)
        # Step 5
        self.play(FadeOut(step_label1), FadeOut(footer1))
        self.play(Indicate(eq1, color=RED))
        anim_time_5 = 1.2
        self.play(Write(step_label2), run_time=1.2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__e2cdcbba22/step_05.mp3")  # [auto-injected] duration=5.18s
        self.wait(max(0.1, _audio_dur_4 - 3.20))
        _audio_dur_5 = 5.18  # [audio-sync] actual TTS duration
        self.set_subtitle("算式簡化為 38 - -6 × 3。", run_time=_audio_dur_5)
        # Step 6
        anim_time_6 = 1.8 + 0.8
        self.play(ReplacementTransform(eq1, eq2), run_time=1.8)
        self.play(Write(footer2), run_time=0.8)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__e2cdcbba22/step_06.mp3")  # [auto-injected] duration=6.89s
        self.wait(max(0.1, _audio_dur_5 - 2.60))
        _audio_dur_6 = 6.89  # [audio-sync] actual TTS duration
        self.set_subtitle("步驟 3：進行乘法。-6 × 3 = -18。", run_time=_audio_dur_6)
        # Step 7
        self.play(FadeOut(step_label2), FadeOut(footer2))
        self.play(Indicate(eq2, color=RED))
        anim_time_7 = 1.2
        self.play(Write(step_label3), run_time=1.2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__e2cdcbba22/step_07.mp3")  # [auto-injected] duration=4.27s
        self.wait(max(0.1, _audio_dur_6 - 3.20))
        _audio_dur_7 = 4.27  # [audio-sync] actual TTS duration
        self.set_subtitle("算式現在變成 38 - -18。", run_time=_audio_dur_7)
        # Step 8
        anim_time_8 = 1.8 + 0.8
        self.play(ReplacementTransform(eq2, eq3), run_time=1.8)
        self.play(Write(footer3), run_time=0.8)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__e2cdcbba22/step_08.mp3")  # [auto-injected] duration=9.48s
        self.wait(max(0.1, _audio_dur_7 - 2.60))
        _audio_dur_8 = 9.48  # [audio-sync] actual TTS duration
        self.set_subtitle("步驟 4：減去負數等於加上正數，所以 38 + 18 = 56。", run_time=_audio_dur_8)
        # Step 9
        self.play(FadeOut(step_label3), FadeOut(footer3))
        self.play(Circumscribe(eq3, color=YELLOW))
        anim_time_9 = 1.2
        self.play(Write(step_label4), run_time=1.2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__e2cdcbba22/step_09.mp3")  # [auto-injected] duration=3.12s
        self.wait(max(0.1, _audio_dur_8 - 3.20))
        _audio_dur_9 = 3.12  # [audio-sync] actual TTS duration
        self.set_subtitle("最終答案是 56。", run_time=_audio_dur_9)
        # Step 10
        anim_time_10 = 1.8 + 0.6
        self.play(ReplacementTransform(eq3, eq4), run_time=1.8)
        self.play(Write(footer4), run_time=0.6)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__e2cdcbba22/step_10.mp3")  # [auto-injected] duration=4.32s
        self.wait(max(0.1, _audio_dur_9 - 2.40))
        _audio_dur_10 = 4.32  # [audio-sync] actual TTS duration
        self.set_subtitle("這就是我們漂亮的計算結果：56。", run_time=_audio_dur_10)
        # Step 11
        self.play(FadeOut(step_label4), FadeOut(footer4))
        final_box = SurroundingRectangle(eq4, color=YELLOW, buff=0.2)
        anim_time_11 = 1.5
        self.play(Create(final_box), run_time=1.5)
        self.wait(max(0.1, _audio_dur_10 - 2.50))
