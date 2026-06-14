from manim import *

# [VISUAL REASONING]
# The unit circle anchors the abstract equation sin(theta)=1/2 to a concrete
# vertical height. The y-coordinate of the two intersection points explains
# why 30 degrees and 150 degrees share the same sine value, then periodicity
# extends this to the general solution.
# Layout: title on top (HEADER), unit circle centered (CONTENT),
# equations in the bottom footer band (FOOTER, y about -2.3).


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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H02_sin_equation_1780228795/media/audio/Solve_the_trigonomet_3071f57192/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 5.50  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 4.500)
        title = Text("求解 sin(θ) = 1/2", color=WHITE, font_size=36)
        title.to_edge(UP)

        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            axis_config={"color": GREY},
        )
        axes.move_to(ORIGIN)

        unit_circle = Circle(radius=2, color=BLUE, fill_opacity=0.0)
        unit_circle.move_to(ORIGIN)

        self.set_subtitle("我們想找出所有正弦值等於二分之一的角度，因此使用單位圓。", run_time=_audio_dur_0)
        self.play(Write(title), run_time=(1.0)*_scale_1)
        anim_time_1 = 4.500 * _scale_1
        self.play(Create(axes), run_time=1.5)
        self.play(Create(unit_circle), run_time=2.0)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H02_sin_equation_1780228795/media/audio/Solve_the_trigonomet_3071f57192/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 5.90  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 3.800)
        sine_line = DashedLine(start=[-2.5, 1.0, 0], end=[2.5, 1.0, 0], color=YELLOW)
        sine_label = MathTex(r"y=\tfrac{1}{2}", color=YELLOW)
        sine_label.move_to(sine_line.get_center() + np.array([2.0, 0.4, 0]))

        self.set_subtitle("因為正弦就是圓上的高度，我們在 y 等於二分之一處畫一條水平線。", run_time=_audio_dur_1)
        self.play(Create(sine_line), run_time=(2.0)*_scale_2)
        self.play(Write(sine_label), run_time=(0.8)*_scale_2)
        self.play(Indicate(sine_label, color=YELLOW))
        anim_time_2 = 3.800 * _scale_2
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H02_sin_equation_1780228795/media/audio/Solve_the_trigonomet_3071f57192/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 5.98  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.500)
        dot_30 = Dot(point=[1.732, 1.0, 0], color=GREEN, radius=0.09)
        dot_150 = Dot(point=[-1.732, 1.0, 0], color=ORANGE, radius=0.09)

        self.set_subtitle("這條線與圓相交於兩點，分別落在第一象限與第二象限。", run_time=_audio_dur_2)
        self.play(
            LaggedStart(
                FadeIn(dot_30, scale=0.5),
                FadeIn(dot_150, scale=0.5),
                lag_ratio=0.2,
            ),
            run_time=(1.5)*_scale_3,
        )
        self.play(Circumscribe(dot_30, color=GREEN))
        anim_time_3 = 2.500 * _scale_3
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H02_sin_equation_1780228795/media/audio/Solve_the_trigonomet_3071f57192/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.02  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 5.000)
        radius_30 = Line(start=[0, 0, 0], end=[1.732, 1.0, 0], color=GREEN)
        radius_150 = Line(start=[0, 0, 0], end=[-1.732, 1.0, 0], color=ORANGE)
        label_30 = MathTex(r"30^{\circ}", color=GREEN).next_to(dot_30, UR, buff=0.15)
        label_150 = MathTex(r"150^{\circ}", color=ORANGE).next_to(dot_150, UL, buff=0.15)
        principal_eq = MathTex(
            r"\theta = 30^{\circ} \;or\; 150^{\circ}", color=WHITE
        )
        principal_eq.move_to([0, -2.3, 0])

        self.set_subtitle("讀取這兩條半徑，它們對應到三十度與一百五十度。", run_time=_audio_dur_3)
        self.play(
            LaggedStart(
                Create(radius_30),
                Create(radius_150),
                lag_ratio=0.2,
            ),
            run_time=(2.0)*_scale_4,
        )
        self.play(
            LaggedStart(
                Write(label_30),
                Write(label_150),
                lag_ratio=0.2,
            ),
            run_time=(1.0)*_scale_4,
        )
        self.play(Write(principal_eq), run_time=(1.0)*_scale_4)
        self.play(Indicate(label_150, color=ORANGE))
        anim_time_4 = 5.000 * _scale_4
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H02_sin_equation_1780228795/media/audio/Solve_the_trigonomet_3071f57192/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 8.18  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 3.500)
        general_eq = MathTex(
            r"\theta = 30^{\circ} + 360^{\circ}k \;or\; 150^{\circ} + 360^{\circ}k",
            color=WHITE,
        )
        general_eq.move_to([0, -2.3, 0])

        self.set_subtitle("由於正弦每旋轉一整圈就重複一次，我們加上三百六十度乘以任意整數 k，得到通解。", run_time=_audio_dur_4)
        self.play(ReplacementTransform(principal_eq, general_eq), run_time=(2.5)*_scale_5)
        self.play(Indicate(general_eq, color=RED))
        anim_time_5 = 3.500 * _scale_5
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)