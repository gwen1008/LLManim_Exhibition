from manim import *
import numpy as np

# [VISUAL REASONING]
# A linear constant-coefficient IVP taught as a clean symbolic chain:
# ODE -> characteristic -> factor -> roots -> general -> system -> constants -> particular,
# using in-place TransformMatchingTex morphs at a central anchor to avoid overflow.
# A step label banner updates each step; the final plot anchors the algebra to
# physical exponential-decay behavior. Cleanup keeps only the current equation,
# step label, and helper visible at any time.

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
        eq_center = np.array([0.0, 0.3, 0.0])

        title = Text("Solving a Second-Order IVP", color=WHITE, font_size=36)
        title.to_edge(UP, buff=0.4)

        step_label = Text("Step 1: The ODE and conditions", color=TEAL, font_size=26)
        step_label.next_to(title, DOWN, buff=0.3)

        ode = MathTex("y'' + 3y' + 2y = 0", color=WHITE).move_to(eq_center)
        init_conds = MathTex(r"y(0)=1,\quad y'(0)=0", color=YELLOW).next_to(ode, DOWN, buff=0.5)
        char_eq = MathTex("r^2 + 3r + 2 = 0", color=WHITE).move_to(eq_center)
        factored = MathTex("(r+1)(r+2) = 0", color=WHITE).move_to(eq_center)
        roots = MathTex(r"r = -1, \quad r = -2", color=GREEN).move_to(eq_center)
        general = MathTex("y(t) = C_1 e^{-t} + C_2 e^{-2t}", color=WHITE).move_to(eq_center)
        system = VGroup(
            MathTex(r"C_1 + C_2 = 1", color=YELLOW),
            MathTex(r"-C_1 - 2C_2 = 0", color=YELLOW),
        ).arrange(DOWN, buff=0.3).scale(0.9).move_to(eq_center)
        constants = MathTex("C_1 = 2, \\quad C_2 = -1", color=GREEN).move_to(eq_center)
        particular = MathTex("y(t) = 2e^{-t} - e^{-2t}", color=WHITE).move_to(eq_center + np.array([0, 1.5, 0]))

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.2, 0.5],
            x_length=7,
            y_length=3,
            axis_config={"color": GREY},
        ).move_to(eq_center + np.array([0, -0.8, 0]))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Solve_the_initial_va_a837cccf5a/step_00.mp3")  # [auto-injected] duration=6.10s
        _audio_dur_0 = 6.10  # [audio-sync] actual TTS duration
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.500)
        anim_time_1 = 1.500 * _scale_1
        self.set_subtitle("我們從這個線性常微分方程與兩個初始條件開始，它們能確定唯一解。", run_time=_audio_dur_0)
        self.play(FadeIn(title), FadeIn(step_label))
        self.play(Write(ode), run_time=anim_time_1)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Solve_the_initial_va_a837cccf5a/step_01.mp3")  # [auto-injected] duration=7.08s
        _audio_dur_1 = 7.08  # [audio-sync] actual TTS duration
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 1.500)
        anim_time_2 = 1.500 * _scale_2
        self.set_subtitle("條件 y(0)=1 與 y'(0)=0 稍後將用來確定常數。", run_time=_audio_dur_1)
        self.play(Write(init_conds), run_time=anim_time_2)
        self.play(Indicate(init_conds, color=YELLOW))
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 - 0.6 + 0.1)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Solve_the_initial_va_a837cccf5a/step_02.mp3")  # [auto-injected] duration=5.83s
        _audio_dur_2 = 5.83  # [audio-sync] actual TTS duration
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 1.800)
        anim_time_3 = 1.800 * _scale_3
        self.set_subtitle("假設指數型解，會將常微分方程轉換成它的特徵方程。", run_time=_audio_dur_2)
        new_label_3 = Text("Step 2: Characteristic equation", color=TEAL, font_size=26).next_to(title, DOWN, buff=0.3)
        self.play(FadeOut(init_conds), Transform(step_label, new_label_3))
        self.play(TransformMatchingTex(ode, char_eq), run_time=anim_time_3)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 0.5 + 0.1)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Solve_the_initial_va_a837cccf5a/step_03.mp3")  # [auto-injected] duration=4.20s
        _audio_dur_3 = 4.20  # [audio-sync] actual TTS duration
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 1.800)
        anim_time_4 = 1.800 * _scale_4
        self.set_subtitle("我們將二次式因式分解，直接揭示它的根。", run_time=_audio_dur_3)
        new_label_4 = Text("Step 3: Factor", color=TEAL, font_size=26).next_to(title, DOWN, buff=0.3)
        self.play(Transform(step_label, new_label_4))
        self.play(TransformMatchingTex(char_eq, factored), run_time=anim_time_4)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 - 0.5 + 0.1)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Solve_the_initial_va_a837cccf5a/step_04.mp3")  # [auto-injected] duration=6.53s
        _audio_dur_4 = 6.53  # [audio-sync] actual TTS duration
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 1.800)
        anim_time_5 = 1.800 * _scale_5
        self.set_subtitle("令每個因式為零，得到兩個相異實根，負一與負二。", run_time=_audio_dur_4)
        new_label_5 = Text("Step 4: Roots", color=TEAL, font_size=26).next_to(title, DOWN, buff=0.3)
        self.play(Transform(step_label, new_label_5))
        self.play(TransformMatchingTex(factored, roots), run_time=anim_time_5)
        self.play(Circumscribe(roots, color=GREEN))
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.5 + 0.1)
        self.wait(max(0.1, remaining_5))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Solve_the_initial_va_a837cccf5a/step_05.mp3")  # [auto-injected] duration=6.14s
        _audio_dur_5 = 6.14  # [audio-sync] actual TTS duration
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 1.800)
        anim_time_6 = 1.800 * _scale_6
        self.set_subtitle("相異實根產生的通解，是兩個衰減指數項的和。", run_time=_audio_dur_5)
        new_label_6 = Text("Step 5: General solution", color=TEAL, font_size=26).next_to(title, DOWN, buff=0.3)
        self.play(Transform(step_label, new_label_6))
        self.play(TransformMatchingTex(roots, general), run_time=anim_time_6)
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 - 0.5 + 0.1)
        self.wait(max(0.1, remaining_6))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Solve_the_initial_va_a837cccf5a/step_06.mp3")  # [auto-injected] duration=5.76s
        _audio_dur_6 = 5.76  # [audio-sync] actual TTS duration
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 1.800)
        anim_time_7 = 1.800 * _scale_7
        self.set_subtitle("套用兩個初始條件，得到關於兩個常數的簡單線性方程組。", run_time=_audio_dur_6)
        new_label_7 = Text("Steps 6-7: Apply conditions", color=TEAL, font_size=26).next_to(title, DOWN, buff=0.3)
        self.play(Transform(step_label, new_label_7))
        self.play(ReplacementTransform(general, system), run_time=anim_time_7)
        self.play(Indicate(system, color=YELLOW))
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 - 0.6 + 0.1)
        self.wait(max(0.1, remaining_7))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Solve_the_initial_va_a837cccf5a/step_07.mp3")  # [auto-injected] duration=5.54s
        _audio_dur_7 = 5.54  # [audio-sync] actual TTS duration
        # Step 8
        _scale_8 = max(1.0, (_audio_dur_7 * 0.7) / 1.800)
        anim_time_8 = 1.800 * _scale_8
        self.set_subtitle("解這個方程組得到 C1 等於二，C2 等於負一。", run_time=_audio_dur_7)
        new_label_8 = Text("Step 8: Solve the system", color=TEAL, font_size=26).next_to(title, DOWN, buff=0.3)
        self.play(Transform(step_label, new_label_8))
        self.play(ReplacementTransform(system, constants), run_time=anim_time_8)
        self.play(Circumscribe(constants, color=GREEN))
        remaining_8 = max(0.1, _audio_dur_7 - anim_time_8 - 1.5 + 0.1)
        self.wait(max(0.1, remaining_8))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Solve_the_initial_va_a837cccf5a/step_08.mp3")  # [auto-injected] duration=4.94s
        _audio_dur_8 = 4.94  # [audio-sync] actual TTS duration
        # Step 9
        _scale_9 = max(1.0, (_audio_dur_8 * 0.7) / 1.800)
        anim_time_9 = 1.800 * _scale_9
        self.set_subtitle("將常數代回，得到唯一的特解。", run_time=_audio_dur_8)
        new_label_9 = Text("Step 9: Particular solution", color=TEAL, font_size=26).next_to(title, DOWN, buff=0.3)
        self.play(Transform(step_label, new_label_9))
        self.play(TransformMatchingTex(constants, particular), run_time=anim_time_9)
        remaining_9 = max(0.1, _audio_dur_8 - anim_time_9 - 0.5 + 0.1)
        self.wait(max(0.1, remaining_9))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Solve_the_initial_va_a837cccf5a/step_09.mp3")  # [auto-injected] duration=5.90s
        _audio_dur_9 = 5.90  # [audio-sync] actual TTS duration
        # Step 10
        _scale_10 = max(1.0, (_audio_dur_9 * 0.7) / 2.500)
        anim_time_10 = 2.500 * _scale_10
        self.set_subtitle("最後，繪出解的圖形，顯示它從一開始，平滑地衰減到零。", run_time=_audio_dur_9)
        new_label_10 = Text("Step 10: Visualize the decay", color=TEAL, font_size=26).next_to(title, DOWN, buff=0.3)
        self.play(Transform(step_label, new_label_10))
        curve = axes.plot(lambda t: 2 * np.exp(-t) - np.exp(-2 * t), x_range=[0, 5], color=BLUE)
        self.play(Create(axes), run_time=1.0)
        self.play(Create(curve), run_time=anim_time_10)
        remaining_10 = max(0.1, _audio_dur_9 - anim_time_10 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_10))