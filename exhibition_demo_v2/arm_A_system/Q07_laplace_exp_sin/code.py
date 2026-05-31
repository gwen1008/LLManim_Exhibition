from manim import *

# [VISUAL REASONING]
# Laplace shifting is a substitution rule, so the clearest pedagogy is a single
# in-place equation that transforms s -> s-a, anchored by a persistent theorem
# callout in the footer that justifies the move. We keep ONE equation anchor at
# ORIGIN and use ReplacementTransform to morph between derivation steps, avoiding
# stacking/overflow. Circumscribe (yellow) introduces the base formula and
# Indicate (red) signals the s -> s-a substitution.

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
        registry = {}

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_Laplace__a20ec2c4c7/step_00.mp3")  # [auto-injected] duration=4.87s
        _audio_dur_0 = 4.87  # [audio-sync] actual TTS duration
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.500)
        title = Text("Laplace Transform of e^{at} sin(bt)", color=WHITE, font_size=34)
        title.to_edge(UP)
        registry["title"] = title
        anim_time_1 = 1.500 * _scale_1
        self.play(Write(title), run_time=anim_time_1)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_Laplace__a20ec2c4c7/step_01.mp3")  # [auto-injected] duration=6.74s
        _audio_dur_1 = 6.74  # [audio-sync] actual TTS duration
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.000)
        eq_base = MathTex(r"\mathcal{L}\{\sin(bt)\} = \frac{b}{s^2 + b^2}", color=WHITE)
        eq_base.move_to(ORIGIN)
        registry["eq_base"] = eq_base
        anim_time_2 = 2.000 * _scale_2
        self.play(Write(eq_base), run_time=anim_time_2)
        self.play(Circumscribe(eq_base, color=YELLOW))
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_Laplace__a20ec2c4c7/step_02.mp3")  # [auto-injected] duration=6.24s
        _audio_dur_2 = 6.24  # [audio-sync] actual TTS duration
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 1.500)
        rule_text = MathTex(r"e^{at} f(t) \;\longrightarrow\; F(s-a)", color=TEAL)
        rule_text.move_to([0, -2.2, 0])
        registry["rule_text"] = rule_text
        rule_box = SurroundingRectangle(rule_text, color=TEAL, buff=0.2)
        registry["rule_box"] = rule_box
        anim_time_3 = 1.500 * _scale_3
        self.play(Write(rule_text), Create(rule_box), run_time=anim_time_3)
        self.play(Indicate(rule_text, color=TEAL))
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_Laplace__a20ec2c4c7/step_03.mp3")  # [auto-injected] duration=4.66s
        _audio_dur_3 = 4.66  # [audio-sync] actual TTS duration
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.000)
        eq_shifted = MathTex(r"\frac{b}{(s-a)^2 + b^2}", color=WHITE)
        eq_shifted.move_to(ORIGIN)
        registry["eq_shifted"] = eq_shifted
        anim_time_4 = 2.000 * _scale_4
        self.play(ReplacementTransform(eq_base, eq_shifted), run_time=anim_time_4)
        self.play(Indicate(eq_shifted, color=RED))
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_Laplace__a20ec2c4c7/step_04.mp3")  # [auto-injected] duration=5.95s
        _audio_dur_4 = 5.95  # [audio-sync] actual TTS duration
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        eq_final = MathTex(r"\mathcal{L}\{e^{at}\sin(bt)\} = \frac{b}{(s-a)^2 + b^2}", color=YELLOW)
        eq_final.move_to(ORIGIN)
        if eq_final.width > 10:
            eq_final.scale(0.9)
        registry["eq_final"] = eq_final
        anim_time_5 = 2.000 * _scale_5
        self.play(ReplacementTransform(eq_shifted, eq_final), run_time=anim_time_5)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(max(0.1, remaining_5))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_Laplace__a20ec2c4c7/step_05.mp3")  # [auto-injected] duration=4.34s
        _audio_dur_5 = 4.34  # [audio-sync] actual TTS duration
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 1.500)
        answer_box = SurroundingRectangle(eq_final, color=YELLOW, buff=0.2)
        registry["answer_box"] = answer_box
        anim_time_6 = 1.500 * _scale_6
        self.play(Create(answer_box), run_time=anim_time_6)
        self.play(Indicate(eq_final, color=YELLOW))
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_6))