# [VISUAL REASONING]
# Teach distributive law by visually factoring common 75, collapsing bracket, then computing product.
# In-place ReplacementTransform morphing keeps focus on a single equation at center.

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
        title = Text("Distributive Law in Action", color=WHITE, font_size=40).move_to(ORIGIN + np.array([0, 3.2, 0]))
        step_label = Text("Step 1: Spot the common factor 75", color=TEAL, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        step_label_2 = Text("Step 2: Factor out 75", color=TEAL, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        step_label_3 = Text("Step 3: Add inside the bracket", color=TEAL, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        step_label_4 = Text("Step 4: Multiply for the final answer", color=TEAL, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))

        eq_0 = MathTex("75 \\times (-38) + 75 \\times (-62)", color=WHITE).move_to(ORIGIN + np.array([0, 0.3, 0]))
        eq_1 = MathTex("75 \\times \\left[(-38) + (-62)\\right]", color=WHITE).move_to(ORIGIN + np.array([0, 0.3, 0]))
        eq_2 = MathTex("75 \\times (-100)", color=WHITE).move_to(ORIGIN + np.array([0, 0.3, 0]))
        eq_3 = MathTex("-7500", color=YELLOW).move_to(ORIGIN + np.array([0, 0.3, 0]))

        explain_1 = Text("Both terms share the factor 75.", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))
        explain_2 = Text("Factor 75 out using a x b + a x c = a x (b + c).", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))
        explain_3 = Text("Add the two negatives: -38 + -62 = -100.", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))
        explain_4 = Text("Positive times negative gives a negative product.", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__c672ea68c1/step_00.mp3")  # [auto-injected] duration=7.01s
        _audio_dur_0 = 7.01  # [audio-sync] actual TTS duration
        # Step 1
        self.set_subtitle("我們要計算 75 乘以負 38 加上 75 乘以負 62。", run_time=_audio_dur_0)
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__c672ea68c1/step_01.mp3")  # [auto-injected] duration=4.34s
        _audio_dur_1 = 4.34  # [audio-sync] actual TTS duration
        # Step 2
        self.set_subtitle("注意這兩項都有共同的因數 75。", run_time=_audio_dur_1)
        anim_time_2 = 2.5
        self.play(Write(eq_0), run_time=2.0)
        self.play(FadeIn(step_label), FadeIn(explain_1), run_time=0.5)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__c672ea68c1/step_02.mp3")  # [auto-injected] duration=5.16s
        _audio_dur_2 = 5.16  # [audio-sync] actual TTS duration
        # Step 3
        self.set_subtitle("利用分配律，我們把 75 提取出來。", run_time=_audio_dur_2)
        anim_time_3 = 3.0
        self.play(FadeOut(step_label), FadeOut(explain_1), run_time=0.4)
        self.play(Circumscribe(eq_0, color=YELLOW), run_time=1.0)
        self.play(ReplacementTransform(eq_0, eq_1), run_time=1.2)
        self.play(FadeIn(step_label_2), FadeIn(explain_2), run_time=0.4)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__c672ea68c1/step_03.mp3")  # [auto-injected] duration=4.70s
        _audio_dur_3 = 4.70  # [audio-sync] actual TTS duration
        # Step 4
        self.set_subtitle("括號裡，兩個負數相加得到負一百。", run_time=_audio_dur_3)
        anim_time_4 = 3.0
        self.play(FadeOut(step_label_2), FadeOut(explain_2), run_time=0.4)
        self.play(Indicate(eq_1, color=RED), run_time=1.0)
        self.play(ReplacementTransform(eq_1, eq_2), run_time=1.2)
        self.play(FadeIn(step_label_3), FadeIn(explain_3), run_time=0.4)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate_the_value__c672ea68c1/step_04.mp3")  # [auto-injected] duration=6.10s
        _audio_dur_4 = 6.10  # [audio-sync] actual TTS duration
        # Step 5
        self.set_subtitle("最後，75 乘以負 100 等於負 7500。", run_time=_audio_dur_4)
        anim_time_5 = 3.0
        self.play(FadeOut(step_label_3), FadeOut(explain_3), run_time=0.4)
        self.play(Circumscribe(eq_2, color=YELLOW), run_time=1.0)
        self.play(ReplacementTransform(eq_2, eq_3), run_time=1.2)
        self.play(FadeIn(step_label_4), FadeIn(explain_4), run_time=0.4)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.5)
        self.wait(max(0.1, remaining_5))