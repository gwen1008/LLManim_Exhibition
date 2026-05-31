from manim import *

# [VISUAL REASONING]
# Dual-pane layout: left pane holds the cubic graph (axes, curve, extrema markers),
# right pane carries the symbolic derivative derivation as a single morphing equation.
# ReplacementTransform keeps only one derivative form visible at a time to avoid stacking,
# while horizontal tangents on the curve geometrically confirm the zero-slope extrema.

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

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_the_local_extre_8eabd02c29/step_00.mp3")  # [auto-injected] duration=4.34s
        _audio_dur_0 = 4.34  # [audio-sync] actual TTS duration
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.500)
        title = Text("f(x) = x³ - 6x² + 9x 的局部極值", color=WHITE, font_size=34)
        title.to_edge(UP)
        registry["title"] = title
        self.set_subtitle("我們想找出這個三次函數的局部最高點與最低點。", run_time=_audio_dur_0)
        anim_time_1 = 1.500 * _scale_1
        self.play(Write(title), run_time=anim_time_1)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_the_local_extre_8eabd02c29/step_01.mp3")  # [auto-injected] duration=4.49s
        _audio_dur_1 = 4.49  # [audio-sync] actual TTS duration
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 1.500)
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-2, 6, 2],
            x_length=5.0,
            y_length=4.0,
            axis_config={"color": GREY},
        )
        axes.move_to(np.array([-3.3, -0.3, 0]))
        registry["axes"] = axes
        self.set_subtitle("首先，畫出這個函數，讓我們能看見它的轉折點。", run_time=_audio_dur_1)
        anim_time_2 = 1.500 * _scale_2
        self.play(Create(axes), run_time=anim_time_2)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_the_local_extre_8eabd02c29/step_02.mp3")  # [auto-injected] duration=4.80s
        _audio_dur_2 = 4.80  # [audio-sync] actual TTS duration
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.000)
        curve = axes.plot(lambda x: x**3 - 6 * x**2 + 9 * x, x_range=[-0.5, 4.5], color=BLUE)
        registry["curve"] = curve
        self.set_subtitle("藍色曲線明顯先升到一個高峰，再下降到一個低谷。", run_time=_audio_dur_2)
        anim_time_3 = 2.000 * _scale_3
        self.play(Create(curve), run_time=anim_time_3)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_the_local_extre_8eabd02c29/step_03.mp3")  # [auto-injected] duration=4.99s
        _audio_dur_3 = 4.99  # [audio-sync] actual TTS duration
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 1.500)
        eq_deriv = MathTex("f'(x) = 3x^2 - 12x + 9", color=WHITE)
        eq_deriv.move_to(np.array([3.3, 1.2, 0]))
        registry["eq_deriv"] = eq_deriv
        self.set_subtitle("極值出現在斜率為零的地方，所以我們先求一階導數。", run_time=_audio_dur_3)
        anim_time_4 = 1.500 * _scale_4
        self.play(Write(eq_deriv), run_time=anim_time_4)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_the_local_extre_8eabd02c29/step_04.mp3")  # [auto-injected] duration=4.13s
        _audio_dur_4 = 4.13  # [audio-sync] actual TTS duration
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        eq_factored = MathTex("f'(x) = 3(x-1)(x-3)", color=WHITE)
        eq_factored.move_to(np.array([3.3, 1.2, 0]))
        registry["eq_factored"] = eq_factored
        self.set_subtitle("把導數因式分解，讓它的根一目了然。", run_time=_audio_dur_4)
        self.play(Indicate(eq_deriv, color=YELLOW))
        anim_time_5 = 2.000 * _scale_5
        self.play(ReplacementTransform(eq_deriv, eq_factored), run_time=anim_time_5)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(max(0.1, remaining_5))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_the_local_extre_8eabd02c29/step_05.mp3")  # [auto-injected] duration=5.66s
        _audio_dur_5 = 5.66  # [audio-sync] actual TTS duration
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 1.500)
        eq_roots = MathTex(r"x = 1 \quad or \quad x = 3", color=YELLOW)
        eq_roots.move_to(np.array([3.3, 0.2, 0]))
        registry["eq_roots"] = eq_roots
        self.set_subtitle("令它等於零，得到臨界點 x 等於一以及 x 等於三。", run_time=_audio_dur_5)
        anim_time_6 = 1.500 * _scale_6
        self.play(Write(eq_roots), run_time=anim_time_6)
        self.play(Circumscribe(eq_roots, color=YELLOW))
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 + 0.1)
        self.wait(max(0.1, remaining_6))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_the_local_extre_8eabd02c29/step_06.mp3")  # [auto-injected] duration=3.96s
        _audio_dur_6 = 3.96  # [audio-sync] actual TTS duration
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 1.500)
        eq_second = MathTex("f''(x) = 6x - 12", color=WHITE)
        eq_second.move_to(np.array([3.3, -0.9, 0]))
        registry["eq_second"] = eq_second
        self.set_subtitle("為了判斷它們的性質，我們計算二階導數。", run_time=_audio_dur_6)
        anim_time_7 = 1.500 * _scale_7
        self.play(Write(eq_second), run_time=anim_time_7)
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 + 0.1)
        self.wait(max(0.1, remaining_7))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_the_local_extre_8eabd02c29/step_07.mp3")  # [auto-injected] duration=6.22s
        _audio_dur_7 = 6.22  # [audio-sync] actual TTS duration
        # Step 8
        _scale_8 = max(1.0, (_audio_dur_7 * 0.7) / 1.500)
        eq_test_max = MathTex("f''(1) = -6 < 0 \\Rightarrow \max", color=GREEN, font_size=36)
        eq_test_max.move_to(np.array([3.3, -1.7, 0]))
        registry["eq_test_max"] = eq_test_max
        self.set_subtitle("在 x 等於一時為負六，凹口向下：這是局部最大值。", run_time=_audio_dur_7)
        anim_time_8 = 1.500 * _scale_8
        self.play(Write(eq_test_max), run_time=anim_time_8)
        remaining_8 = max(0.1, _audio_dur_7 - anim_time_8 + 0.1)
        self.wait(max(0.1, remaining_8))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_the_local_extre_8eabd02c29/step_08.mp3")  # [auto-injected] duration=6.10s
        _audio_dur_8 = 6.10  # [audio-sync] actual TTS duration
        # Step 9
        _scale_9 = max(1.0, (_audio_dur_8 * 0.7) / 1.500)
        eq_test_min = MathTex("f''(3) = +6 > 0 \\Rightarrow \min", color=RED, font_size=36)
        eq_test_min.move_to(np.array([3.3, -1.7, 0]))
        registry["eq_test_min"] = eq_test_min
        self.set_subtitle("在 x 等於三時為正六，凹口向上：這是局部最小值。", run_time=_audio_dur_8)
        self.play(FadeOut(eq_test_max))
        anim_time_9 = 1.500 * _scale_9
        self.play(Write(eq_test_min), run_time=anim_time_9)
        remaining_9 = max(0.1, _audio_dur_8 - anim_time_9 + 0.1)
        self.wait(max(0.1, remaining_9))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_the_local_extre_8eabd02c29/step_09.mp3")  # [auto-injected] duration=4.08s
        _audio_dur_9 = 4.08  # [audio-sync] actual TTS duration
        # Step 10
        _scale_10 = max(1.0, (_audio_dur_9 * 0.7) / 1.000)
        dot_max = Dot(color=GREEN, radius=0.09)
        dot_max.move_to(axes.coords_to_point(1, 4))
        registry["dot_max"] = dot_max
        label_max = MathTex("(1,4)", color=GREEN, font_size=30)
        label_max.next_to(dot_max, UP, buff=0.15)
        registry["label_max"] = label_max
        self.set_subtitle("在曲線上標出位於一逗號四的最大值點。", run_time=_audio_dur_9)
        anim_time_10 = 1.000 * _scale_10
        self.play(FadeIn(dot_max), run_time=anim_time_10)
        self.play(Indicate(dot_max, color=GREEN))
        remaining_10 = max(0.1, _audio_dur_9 - anim_time_10 + 0.1)
        self.wait(max(0.1, remaining_10))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_the_local_extre_8eabd02c29/step_10.mp3")  # [auto-injected] duration=5.26s
        _audio_dur_10 = 5.26  # [audio-sync] actual TTS duration
        # Step 11
        _scale_11 = max(1.0, (_audio_dur_10 * 0.7) / 1.500)
        tangent_max = Line(
            axes.coords_to_point(0, 4),
            axes.coords_to_point(2, 4),
            color=GREEN,
        )
        registry["tangent_max"] = tangent_max
        self.set_subtitle("它的切線是完全水平的，證實斜率為零。", run_time=_audio_dur_10)
        anim_time_11 = 1.500 * _scale_11
        self.play(Create(tangent_max), FadeIn(label_max), run_time=anim_time_11)
        remaining_11 = max(0.1, _audio_dur_10 - anim_time_11 + 0.1)
        self.wait(max(0.1, remaining_11))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_the_local_extre_8eabd02c29/step_11.mp3")  # [auto-injected] duration=5.40s
        _audio_dur_11 = 5.40  # [audio-sync] actual TTS duration
        # Step 12
        _scale_12 = max(1.0, (_audio_dur_11 * 0.7) / 1.500)
        dot_min = Dot(color=RED, radius=0.09)
        dot_min.move_to(axes.coords_to_point(3, 0))
        registry["dot_min"] = dot_min
        label_min = MathTex("(3,0)", color=RED, font_size=30)
        label_min.next_to(dot_min, DOWN, buff=0.15)
        registry["label_min"] = label_min
        tangent_min = Line(
            axes.coords_to_point(2, 0),
            axes.coords_to_point(4, 0),
            color=RED,
        )
        registry["tangent_min"] = tangent_min
        self.set_subtitle("最後，在三逗號零標出最小值，並畫出它自己的水平切線。", run_time=_audio_dur_11)
        self.play(FadeIn(dot_min), FadeIn(label_min))
        self.play(Indicate(dot_min, color=RED))
        anim_time_12 = 1.500 * _scale_12
        self.play(Create(tangent_min), run_time=anim_time_12)
        remaining_12 = max(0.1, _audio_dur_11 - anim_time_12 + 0.1)
        self.wait(max(0.1, remaining_12))