# [VISUAL REASONING]
# Anchor one equation at center and morph it through each transformation via ReplacementTransform.
# Step label sits above, explanation below, title at top. Final answer boxed in green.

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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/__frac_3__4___17702db6bd/step_00.mp3")  # [auto-injected] duration=7.94s
        _audio_dur_0 = 7.94  # [audio-sync] actual TTS duration
        # Step 1
        title = Text("Mixed Fraction Multiplication & Division", color=WHITE, font_size=34).to_edge(UP, buff=0.5)
        eq_original = MathTex(r"\left(-\frac{7}{18}\right) \times 2\frac{4}{7} \div \left(-1\frac{1}{3}\right)", color=WHITE).scale(0.9).move_to(ORIGIN)

        self.set_subtitle("我們從這個算式開始：負十八分之七乘以二又七分之四，再除以負一又三分之一。", run_time=_audio_dur_0)
        anim_time_1 = 2.5
        self.play(Write(title), run_time=0.8)
        self.play(Write(eq_original), run_time=2.5)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 - 0.8 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/__frac_3__4___17702db6bd/step_01.mp3")  # [auto-injected] duration=11.47s
        _audio_dur_1 = 11.47  # [audio-sync] actual TTS duration
        # Step 2
        step_label_1 = Text("Step 1: Convert mixed numbers to improper fractions", color=YELLOW, font_size=26).move_to([0, 1.8, 0])
        explain_1 = Text("2 4/7 = 18/7 and -1 1/3 = -4/3", color=WHITE, font_size=24).move_to([0, -2.3, 0])
        eq_improper = MathTex(r"\left(-\frac{7}{18}\right) \times \frac{18}{7} \div \left(-\frac{4}{3}\right)", color=WHITE).scale(0.9).move_to(ORIGIN)

        self.set_subtitle("首先，將每個帶分數化為假分數。二又七分之四等於十八分之七，負一又三分之一等於負三分之四。", run_time=_audio_dur_1)
        anim_time_2 = 4.0
        self.play(Circumscribe(eq_original, color=YELLOW), run_time=1.2)
        self.play(FadeIn(step_label_1), FadeIn(explain_1), run_time=0.5)
        self.play(ReplacementTransform(eq_original, eq_improper), run_time=2.3)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/__frac_3__4___17702db6bd/step_02.mp3")  # [auto-injected] duration=10.58s
        _audio_dur_2 = 10.58  # [audio-sync] actual TTS duration
        # Step 3
        step_label_2 = Text("Step 2: Convert division to multiplication by reciprocal", color=YELLOW, font_size=26).move_to([0, 1.8, 0])
        explain_2 = Text("Dividing by -4/3 is multiplying by -3/4", color=WHITE, font_size=24).move_to([0, -2.3, 0])
        eq_reciprocal = MathTex(r"\left(-\frac{7}{18}\right) \times \frac{18}{7} \times \left(-\frac{3}{4}\right)", color=WHITE).scale(0.9).move_to(ORIGIN)

        self.set_subtitle("接著，把除法改為乘以倒數。除以負三分之四等於乘以負四分之三。", run_time=_audio_dur_2)
        anim_time_3 = 4.0
        self.play(FadeOut(step_label_1), FadeOut(explain_1), run_time=0.5)
        self.play(Indicate(eq_improper, color=RED), run_time=1.0)
        self.play(FadeIn(step_label_2), FadeIn(explain_2), run_time=0.5)
        self.play(ReplacementTransform(eq_improper, eq_reciprocal), run_time=2.0)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/__frac_3__4___17702db6bd/step_03.mp3")  # [auto-injected] duration=7.37s
        _audio_dur_3 = 7.37  # [audio-sync] actual TTS duration
        # Step 4
        step_label_3 = Text("Step 3: Two negatives make a positive; cancel terms", color=YELLOW, font_size=26).move_to([0, 1.8, 0])
        explain_3 = Text("(-7/18) x (18/7) = -1", color=WHITE, font_size=24).move_to([0, -2.3, 0])
        eq_simplified = MathTex(r"(-1) \times \left(-\frac{3}{4}\right)", color=WHITE).scale(0.9).move_to(ORIGIN)

        self.set_subtitle("負負得正。前兩個分數相乘剛好消去，結果是負一。", run_time=_audio_dur_3)
        anim_time_4 = 4.0
        self.play(FadeOut(step_label_2), FadeOut(explain_2), run_time=0.5)
        self.play(Circumscribe(eq_reciprocal, color=BLUE), run_time=1.2)
        self.play(FadeIn(step_label_3), FadeIn(explain_3), run_time=0.5)
        self.play(ReplacementTransform(eq_reciprocal, eq_simplified), run_time=1.8)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/__frac_3__4___17702db6bd/step_04.mp3")  # [auto-injected] duration=6.48s
        _audio_dur_4 = 6.48  # [audio-sync] actual TTS duration
        # Step 5
        step_label_4 = Text("Step 4: Final result", color=YELLOW, font_size=26).move_to([0, 1.8, 0])
        explain_4 = Text("(-1) x (-3/4) = 3/4", color=WHITE, font_size=24).move_to([0, -2.3, 0])
        eq_final = MathTex(r"= \frac{3}{4}", color=GREEN).scale(0.9).move_to(ORIGIN)

        self.set_subtitle("最後，負一乘以負四分之三，得到正的答案：四分之三。", run_time=_audio_dur_4)
        anim_time_5 = 3.5
        self.play(FadeOut(step_label_3), FadeOut(explain_3), run_time=0.5)
        self.play(FadeIn(step_label_4), FadeIn(explain_4), run_time=0.5)
        self.play(ReplacementTransform(eq_simplified, eq_final), run_time=1.5)
        answer_box = SurroundingRectangle(eq_final, color=GREEN, buff=0.2)
        self.play(Create(answer_box), run_time=1.0)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.5)
        self.wait(max(0.1, remaining_5))