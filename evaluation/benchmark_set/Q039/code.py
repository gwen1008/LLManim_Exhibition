# [VISUAL REASONING]
# Pairing trick: group (99-198) and (299-398), each equals -99, sum to -198.
# Layout: title top, expression center, results below, final answer at bottom.

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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__42b179feb9/step_00.mp3")  # [auto-injected] duration=12.26s
        _audio_dur_0 = 12.26  # [audio-sync] actual TTS duration
        self.set_subtitle("我們要計算 99 - 198 + 299 - 398。從左到右算很麻煩，讓我們找找結構。", run_time=_audio_dur_0)
        # Step 1
        title = Text("Smart Grouping: 99 - 198 + 299 - 398", color=WHITE, font_size=38).to_edge(UP, buff=0.5)
        expr_full = MathTex("99 - 198 + 299 - 398", color=WHITE).move_to(ORIGIN + np.array([0, 0.8, 0]))
        anim_time_1 = 3.0
        self.play(Write(title), run_time=1.5)
        self.play(Write(expr_full), run_time=1.5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__42b179feb9/step_01.mp3")  # [auto-injected] duration=6.41s
        self.wait(max(0.1, _audio_dur_0 - 3.00))
        _audio_dur_1 = 6.41  # [audio-sync] actual TTS duration
        self.set_subtitle("注意相鄰的數字很接近。我們把它們兩兩配對。", run_time=_audio_dur_1)
        # Step 2
        group_expr = MathTex("(99 - 198) + (299 - 398)", color=WHITE).move_to(ORIGIN + np.array([0, 0.8, 0]))
        anim_time_2 = 3.0
        self.play(Indicate(expr_full, color=YELLOW), run_time=1.0)
        self.play(TransformMatchingTex(expr_full, group_expr), run_time=2.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__42b179feb9/step_02.mp3")  # [auto-injected] duration=13.54s
        self.wait(max(0.1, _audio_dur_1 - 3.00))
        _audio_dur_2 = 13.54  # [audio-sync] actual TTS duration
        self.set_subtitle("第 1 組 99 - 198 = -99。第 2 組 299 - 398 = -99。", run_time=_audio_dur_2)
        # Step 3
        left_result = MathTex("-99", color=BLUE).move_to(ORIGIN + np.array([-2.0, -0.6, 0]))
        right_result = MathTex("-99", color=GREEN).move_to(ORIGIN + np.array([2.0, -0.6, 0]))
        anim_time_3 = 4.0
        self.play(Circumscribe(group_expr, color=BLUE), run_time=1.5)
        self.play(Write(left_result), Write(right_result), run_time=2.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__42b179feb9/step_03.mp3")  # [auto-injected] duration=3.43s
        self.wait(max(0.1, _audio_dur_2 - 3.50))
        _audio_dur_3 = 3.43  # [audio-sync] actual TTS duration
        self.set_subtitle("現在我們把兩個結果相加。", run_time=_audio_dur_3)
        # Step 4
        sum_expr = MathTex("(-99) + (-99)", color=YELLOW).move_to(ORIGIN + np.array([0, -0.6, 0]))
        anim_time_4 = 3.0
        self.play(FadeOut(group_expr), run_time=0.5)
        self.play(TransformMatchingTex(VGroup(left_result, right_result).copy(), sum_expr), FadeOut(left_result), FadeOut(right_result), run_time=2.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__42b179feb9/step_04.mp3")  # [auto-injected] duration=7.87s
        self.wait(max(0.1, _audio_dur_3 - 2.50))
        _audio_dur_4 = 7.87  # [audio-sync] actual TTS duration
        self.set_subtitle("-99 + -99 = -198。這就是答案。", run_time=_audio_dur_4)
        # Step 5
        final_answer = MathTex("= -198", color=YELLOW).move_to(ORIGIN + np.array([0, -1.5, 0]))
        answer_box = SurroundingRectangle(final_answer, color=YELLOW, buff=0.2)
        hint_text = Text("Tip: Pair adjacent terms to simplify!", color=GREY, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))
        anim_time_5 = 4.0
        self.play(Write(final_answer), run_time=1.5)
        self.play(Create(answer_box), run_time=1.0)
        self.play(Circumscribe(final_answer, color=YELLOW), run_time=1.0)
        self.play(FadeIn(hint_text), run_time=0.5)
        self.wait(max(0.1, _audio_dur_4 - 4.00))
