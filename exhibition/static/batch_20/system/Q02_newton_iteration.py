# [VISUAL REASONING]
# Newton's method geometric visualization for √2.
# Axes centered, parabola f(x)=x²-2, iterative tangent construction.
# Title HEADER zone, formula FOOTER zone, all dots/tangents in CONTENT zone via axes.c2p.

from manim import *

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
        # Setup objects
        title = Text("牛頓法:逼近 √2", color=WHITE, font_size=34).to_edge(UP, buff=0.4)

        axes = Axes(
            x_range=[-0.5, 2.7, 0.5],
            y_range=[-2.5, 2.5, 1],
            x_length=7,
            y_length=4.5,
            axis_config={"color": GREY},
        ).move_to(ORIGIN + np.array([0, 0.2, 0]))

        parabola = axes.plot(lambda x: x**2 - 2, x_range=[-0.5, 2.5], color=BLUE)

        root_dot = Dot(point=axes.c2p(1.4142, 0), color=GREEN, radius=0.09)
        root_label = MathTex(r"\sqrt{2}", color=GREEN).next_to(root_dot, DOWN, buff=0.15)

        formula = MathTex(r"x_{n+1} = x_n - \frac{x_n^2 - 2}{2x_n}", color=YELLOW).to_edge(DOWN, buff=0.4)

        x0_dot = Dot(point=axes.c2p(2, 0), color=RED, radius=0.09)
        x0_label = MathTex(r"x_0=2", color=RED).next_to(x0_dot, UP, buff=0.15)

        tangent0 = Line(
            start=axes.c2p(1.0, -2),
            end=axes.c2p(2.2, 2.8),
            color=ORANGE,
        )

        x1_dot = Dot(point=axes.c2p(1.5, 0), color=RED, radius=0.09)
        x1_label = MathTex(r"x_1=1.5", color=RED).next_to(x1_dot, UP, buff=0.15)

        tangent1 = Line(
            start=axes.c2p(1.3, -0.35),
            end=axes.c2p(1.6, 0.55),
            color=ORANGE,
        )

        x2_dot = Dot(point=axes.c2p(1.4167, 0), color=RED, radius=0.09)
        x2_label = MathTex(r"x_2 \approx 1.4167", color=RED, font_size=32).next_to(x2_dot, UP, buff=0.25)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1779986373/media/audio/Using_the_Newton_ite_f2aba6e782/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 7.08  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 3.000)
        self.set_subtitle("為了求 √2,我們把 x² - 2 = 0 畫成這條拋物線。", run_time=_audio_dur_0)
        anim_time_1 = 3.000 * _scale_1
        self.play(
            LaggedStart(
                Write(title),
                Create(axes),
                Create(parabola),
                FadeIn(formula),
                lag_ratio=0.3,
            ),
            run_time=3.0,
        )
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1779986373/media/audio/Using_the_Newton_ite_f2aba6e782/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 6.70  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.000)
        self.set_subtitle("真正的根 √2 大約在 1.414 附近,這就是我們要逼近的目標。", run_time=_audio_dur_1)
        anim_time_2 = 2.000 * _scale_2
        self.play(FadeIn(root_dot), Write(root_label), run_time=1.5)
        self.play(Indicate(root_dot, color=GREEN), run_time=0.5)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1779986373/media/audio/Using_the_Newton_ite_f2aba6e782/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 5.93  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.800)
        self.set_subtitle("從初始猜測 x₀ = 2 開始,在曲線上該點畫出切線。", run_time=_audio_dur_2)
        anim_time_3 = 2.800 * _scale_3
        self.play(FadeIn(x0_dot), Write(x0_label), run_time=0.8)
        self.play(Create(tangent0), run_time=2.0)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1779986373/media/audio/Using_the_Newton_ite_f2aba6e782/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.38  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.300)
        self.set_subtitle("切線與 x 軸相交於 x₁ = 1.5,這就是改良後的估計值。", run_time=_audio_dur_3)
        anim_time_4 = 2.300 * _scale_4
        self.play(FadeIn(x1_dot), Write(x1_label), run_time=1.5)
        self.play(Circumscribe(x1_dot, color=YELLOW), run_time=0.8)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1779986373/media/audio/Using_the_Newton_ite_f2aba6e782/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 9.91  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 4.000)
        self.set_subtitle("再套用公式一次:下一條切線給出 x₂ ≈ 1.4167,已經非常接近 √2。", run_time=_audio_dur_4)
        anim_time_5 = 4.000 * _scale_5
        self.play(FadeOut(tangent0), FadeOut(x0_label), run_time=0.6)
        self.play(Indicate(formula, color=YELLOW), run_time=0.8)
        self.play(Create(tangent1), run_time=1.6)
        self.play(FadeIn(x2_dot), Write(x2_label), run_time=1.0)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)