from manim import *

# [VISUAL REASONING]
# Centered single-equation morph through 4 stages, with rotating step labels
# above and explanatory footer below. Title stays at top.

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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/__a_____b_____frac_2_77fb0ab732/step_00.mp3")  # [auto-injected] duration=10.01s
        _audio_dur_0 = 10.01  # [audio-sync] actual TTS duration
        # Step 1
        title = Text("Computing |a| - |b|", color=WHITE, font_size=40).to_edge(UP, buff=0.5)
        problem = MathTex(r"a = -3\tfrac{1}{5}, \quad b = 1\tfrac{3}{4}", color=YELLOW).move_to([0, 2.0, 0])
        anim_time_1 = 2.5
        self.play(Write(title), run_time=1.5)
        self.play(Write(problem), run_time=1.0)
        self.set_subtitle("我們要計算 a 的絕對值減去 b 的絕對值，其中 a 等於負三又五分之一，b 等於一又四分之三。", run_time=_audio_dur_0)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/__a_____b_____frac_2_77fb0ab732/step_01.mp3")  # [auto-injected] duration=10.80s
        _audio_dur_1 = 10.80  # [audio-sync] actual TTS duration
        # Step 2
        step_label_1 = Text("Step 1: Apply Absolute Value", color=BLUE, font_size=28).move_to([0, 1.0, 0])
        eq1 = MathTex(r"|-3\tfrac{1}{5}| - |1\tfrac{3}{4}| = 3\tfrac{1}{5} - 1\tfrac{3}{4}", color=WHITE).move_to(ORIGIN)
        explain_1 = Text("Absolute value removes the negative sign.", color=GREY_A, font_size=24).move_to([0, -2.2, 0])
        self.play(Circumscribe(problem, color=YELLOW), run_time=1.0)
        anim_time_2 = 3.0
        self.play(Write(step_label_1), run_time=0.8)
        self.play(Write(eq1), run_time=2.0)
        self.play(FadeIn(explain_1), run_time=0.6)
        self.set_subtitle("步驟一：取絕對值。絕對值會去掉負號，所以變成三又五分之一減去一又四分之三。", run_time=_audio_dur_1)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/__a_____b_____frac_2_77fb0ab732/step_02.mp3")  # [auto-injected] duration=11.16s
        _audio_dur_2 = 11.16  # [audio-sync] actual TTS duration
        # Step 3
        self.play(FadeOut(step_label_1), FadeOut(explain_1), run_time=0.4)
        step_label_2 = Text("Step 2: Convert to Improper Fractions", color=BLUE, font_size=28).move_to([0, 1.0, 0])
        eq2 = MathTex(r"3\tfrac{1}{5} - 1\tfrac{3}{4} = \frac{16}{5} - \frac{7}{4}", color=WHITE).move_to(ORIGIN)
        explain_2 = Text("3 1/5 = 16/5 and 1 3/4 = 7/4.", color=GREY_A, font_size=24).move_to([0, -2.2, 0])
        self.play(Indicate(eq1, color=RED), run_time=1.0)
        anim_time_3 = 3.0
        self.play(Write(step_label_2), run_time=0.8)
        self.play(ReplacementTransform(eq1, eq2), run_time=2.0)
        self.play(FadeIn(explain_2), run_time=0.6)
        self.set_subtitle("步驟二：將每個帶分數轉換為假分數。三又五分之一變成五分之十六，一又四分之三變成四分之七。", run_time=_audio_dur_2)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 1.4 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/__a_____b_____frac_2_77fb0ab732/step_03.mp3")  # [auto-injected] duration=11.02s
        _audio_dur_3 = 11.02  # [audio-sync] actual TTS duration
        # Step 4
        self.play(FadeOut(step_label_2), FadeOut(explain_2), run_time=0.4)
        step_label_3 = Text("Step 3: Common Denominator LCM(5,4)=20", color=BLUE, font_size=28).move_to([0, 1.0, 0])
        eq3 = MathTex(r"\frac{16}{5} - \frac{7}{4} = \frac{64}{20} - \frac{35}{20}", color=WHITE).move_to(ORIGIN)
        explain_3 = Text("Multiply by 4/4 and 5/5 to reach denominator 20.", color=GREY_A, font_size=24).move_to([0, -2.2, 0])
        self.play(Indicate(eq2, color=RED), run_time=1.0)
        anim_time_4 = 3.0
        self.play(Write(step_label_3), run_time=0.8)
        self.play(ReplacementTransform(eq2, eq3), run_time=2.0)
        self.play(FadeIn(explain_3), run_time=0.6)
        self.set_subtitle("步驟三：找出公分母。五和四的最小公倍數是二十，所以變成二十分之六十四減二十分之三十五。", run_time=_audio_dur_3)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 - 1.4 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/__a_____b_____frac_2_77fb0ab732/step_04.mp3")  # [auto-injected] duration=10.30s
        _audio_dur_4 = 10.30  # [audio-sync] actual TTS duration
        # Step 5
        self.play(FadeOut(step_label_3), FadeOut(explain_3), run_time=0.4)
        step_label_4 = Text("Step 4: Subtract Numerators", color=BLUE, font_size=28).move_to([0, 1.0, 0])
        eq4 = MathTex(r"\frac{64}{20} - \frac{35}{20} = \frac{29}{20}", color=GREEN).move_to(ORIGIN)
        explain_4 = Text("64 - 35 = 29, giving 29/20.", color=GREY_A, font_size=24).move_to([0, -2.2, 0])
        final_box = MathTex(r"|a| - |b| = \frac{29}{20} = 1\tfrac{9}{20}", color=YELLOW).move_to([0, -1.2, 0])
        self.play(Circumscribe(eq3, color=YELLOW), run_time=1.0)
        anim_time_5 = 4.0
        self.play(Write(step_label_4), run_time=0.8)
        self.play(ReplacementTransform(eq3, eq4), run_time=2.0)
        self.play(FadeIn(explain_4), run_time=0.5)
        self.play(Write(final_box), run_time=1.2)
        self.set_subtitle("步驟四：將分子相減。六十四減三十五等於二十九，所以最後答案是二十分之二十九。", run_time=_audio_dur_4)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))