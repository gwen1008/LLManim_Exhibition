from manim import *

# [VISUAL REASONING]
# L'Hôpital's rule is an iterative symbolic process. A single central equation
# is morphed in place three times via TransformMatchingTex so each differentiation
# visibly replaces the previous form. A recurring 0/0 indeterminate-form flag
# motivates each repetition. Only one main equation is visible at the equation
# anchor (y≈0.3); the step label sits above (y≈2.0) and the flag in the footer
# (y≈-2.2). Long MathTex is scaled to 0.9. The final clean substitution yields -1/6,
# highlighted by a green box.

class SubtitleManager:
    """Auto-injected by RefiningLoop.pre_render_patch. Prevents subtitle overlap and implements YT-style chunking."""
    MAX_WIDTH = 12.5

    def __init__(self, scene, font_size=28):
        self.scene = scene
        self.font_size = font_size
        self._current = None
        self._y = 3.5 * DOWN

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
        eq_center = np.array([0, 0.3, 0])

        title = Text("L'Hopital's Rule", color=WHITE, font_size=40).to_edge(UP, buff=0.5)

        eq0 = MathTex(r"\lim_{x \to 0} \frac{\sin x - x}{x^{3}}", color=WHITE).scale(0.9)
        eq0.move_to(eq_center)

        sub_check = MathTex(r"\frac{\sin 0 - 0}{0^{3}} = \frac{0}{0}", color=YELLOW).scale(0.9)
        sub_check.next_to(eq0, DOWN, buff=0.6)

        eq1 = MathTex(r"\lim_{x \to 0} \frac{\cos x - 1}{3x^{2}}", color=WHITE).scale(0.9)
        eq1.move_to(eq_center)

        eq2 = MathTex(r"\lim_{x \to 0} \frac{-\sin x}{6x}", color=WHITE).scale(0.9)
        eq2.move_to(eq_center)

        eq3 = MathTex(r"\lim_{x \to 0} \frac{-\cos x}{6}", color=WHITE).scale(0.9)
        eq3.move_to(eq_center)

        final = MathTex(r"\frac{-\cos 0}{6} = -\frac{1}{6}", color=GREEN).scale(0.9)
        final.move_to(eq_center)

        step_label = Text("Step 1: Check the form", color=BLUE, font_size=30)
        step_label.move_to(np.array([0, 2.0, 0]))

        flag = Text("Still 0/0 -> differentiate again", color=RED, font_size=28)
        flag.move_to(np.array([0, -2.2, 0]))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q05_complete_square_1780229122/media/audio/Using_L_Hôpital_s_ru_2518da042e/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 6.94  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 2.000)
        anim_time_1 = 2.000 * _scale_1
        self.play(Write(eq0), run_time=2.0)
        self.play(FadeIn(title), FadeIn(step_label), run_time=0.6)
        self.set_subtitle("我們要求這個極限，但代入 x 等於零會得到不定型 零分之零。", run_time=_audio_dur_0)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 - 0.6 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q05_complete_square_1780229122/media/audio/Using_L_Hôpital_s_ru_2518da042e/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 6.36  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 1.800)
        anim_time_2 = 1.800 * _scale_2
        self.play(Write(sub_check), run_time=1.8)
        self.play(Circumscribe(sub_check, color=YELLOW))
        self.set_subtitle("代入零確認了這一點：零分之零，所以直接代入在這裡行不通。", run_time=_audio_dur_1)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 - 1.0 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q05_complete_square_1780229122/media/audio/Using_L_Hôpital_s_ru_2518da042e/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 7.63  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.000)
        new_step_3 = Text("Step 2: Differentiate", color=BLUE, font_size=30).move_to(np.array([0, 2.0, 0]))
        anim_time_3 = 2.000 * _scale_3
        self.play(FadeOut(sub_check), Transform(step_label, new_step_3), run_time=0.6)
        self.play(TransformMatchingTex(eq0, eq1), run_time=2.0)
        self.play(Indicate(eq1, color=RED))
        self.set_subtitle("羅必達法則讓我們分別對分子分母微分，得到三x平方分之 cos x 減一。", run_time=_audio_dur_2)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 1.2 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q05_complete_square_1780229122/media/audio/Using_L_Hôpital_s_ru_2518da042e/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 5.09  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 1.200)
        anim_time_4 = 1.200 * _scale_4
        self.play(FadeIn(flag), run_time=1.2)
        self.set_subtitle("這仍然是零分之零，所以我們第二次應用這個法則。", run_time=_audio_dur_3)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q05_complete_square_1780229122/media/audio/Using_L_Hôpital_s_ru_2518da042e/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.41  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        anim_time_5 = 2.000 * _scale_5
        self.play(FadeOut(flag), run_time=0.5)
        self.play(TransformMatchingTex(eq1, eq2), run_time=2.0)
        self.play(Indicate(eq2, color=RED))
        self.set_subtitle("再次微分得到六x分之負 sin x，它仍然是不定型。", run_time=_audio_dur_4)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.0 + 0.1)
        self.wait(remaining_5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q05_complete_square_1780229122/media/audio/Using_L_Hôpital_s_ru_2518da042e/step_05.mp3")  # [auto-injected]
        _audio_dur_5 = 7.18  # [audio-sync]
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 2.000)
        new_step_6 = Text("Step 3: Substitute", color=BLUE, font_size=30).move_to(np.array([0, 2.0, 0]))
        anim_time_6 = 2.000 * _scale_6
        self.play(Transform(step_label, new_step_6), run_time=0.6)
        self.play(TransformMatchingTex(eq2, eq3), run_time=2.0)
        self.play(Indicate(eq3, color=RED))
        self.set_subtitle("再微分一次得到六分之負 cos x，此時分母不再是零。", run_time=_audio_dur_5)
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 - 1.2 + 0.1)
        self.wait(remaining_6)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q05_complete_square_1780229122/media/audio/Using_L_Hôpital_s_ru_2518da042e/step_06.mp3")  # [auto-injected]
        _audio_dur_6 = 7.37  # [audio-sync]
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 2.000)
        anim_time_7 = 2.000 * _scale_7
        self.play(TransformMatchingTex(eq3, final), run_time=2.0)
        answer_box = SurroundingRectangle(final, color=GREEN, buff=0.2)
        self.play(Create(answer_box), run_time=0.8)
        self.play(Circumscribe(final, color=GREEN))
        self.set_subtitle("現在代入零是安全的，cos 零等於一，所以極限等於負六分之一。", run_time=_audio_dur_6)
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 - 1.8 + 0.1)
        self.wait(remaining_7)