from manim import *
import numpy as np

# [VISUAL REASONING]
# De Casteljau is a recursive linear-interpolation scaffold. We display four control
# points and their dashed control polygon (BLUE), then build each interpolation layer
# at the sample t=0.4: level-1 (GREEN), level-2 (ORANGE), collapsing into one curve
# point (YELLOW). Finally we sweep t from 0 to 1 to trace the full cubic Bezier curve.
# Colors encode the recursion hierarchy for pedagogical clarity (Mayer's signaling).


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
        title = Text("De Casteljau: Cubic Bezier Curve", color=WHITE, font_size=36).to_edge(UP)

        P0 = Dot(point=[-5, -1.5, 0], color=BLUE, radius=0.1)
        P1 = Dot(point=[-2, 2, 0], color=BLUE, radius=0.1)
        P2 = Dot(point=[2, 2, 0], color=BLUE, radius=0.1)
        P3 = Dot(point=[5, -1.5, 0], color=BLUE, radius=0.1)

        labelP0 = MathTex("P_0", color=BLUE).next_to(P0, DOWN, buff=0.2)
        labelP1 = MathTex("P_1", color=BLUE).next_to(P1, UP, buff=0.2)
        labelP2 = MathTex("P_2", color=BLUE).next_to(P2, UP, buff=0.2)
        labelP3 = MathTex("P_3", color=BLUE).next_to(P3, DOWN, buff=0.2)

        poly01 = DashedLine(start=[-5, -1.5, 0], end=[-2, 2, 0], color=BLUE)
        poly12 = DashedLine(start=[-2, 2, 0], end=[2, 2, 0], color=BLUE)
        poly23 = DashedLine(start=[2, 2, 0], end=[5, -1.5, 0], color=BLUE)

        lineQ0 = Line(start=[-3.8, -0.1, 0], end=[-0.4, 2, 0], color=GREEN)
        lineQ1 = Line(start=[-0.4, 2, 0], end=[3.2, 0.6, 0], color=GREEN)
        Q0 = Dot(point=[-3.8, -0.1, 0], color=GREEN, radius=0.08)
        Q1 = Dot(point=[-0.4, 2, 0], color=GREEN, radius=0.08)
        Q2 = Dot(point=[3.2, 0.6, 0], color=GREEN, radius=0.08)

        lineR = Line(start=[-2.44, 0.74, 0], end=[1.04, 1.44, 0], color=ORANGE)
        R0 = Dot(point=[-2.44, 0.74, 0], color=ORANGE, radius=0.08)
        R1 = Dot(point=[1.04, 1.44, 0], color=ORANGE, radius=0.08)

        curvePoint = Dot(point=[-1.048, 1.02, 0], color=YELLOW, radius=0.1)

        bezierCurve = CubicBezier(
            np.array([-5, -1.5, 0]),
            np.array([-2, 2, 0]),
            np.array([2, 2, 0]),
            np.array([5, -1.5, 0]),
        )
        bezierCurve.set_color(YELLOW)

        self.play(Write(title), run_time=1.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N01_bezier_curve_1780053079/media/audio/Using_the_de_Castelj_af8830b653/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 6.26  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 3.000)
        self.set_subtitle("我們從四個控制點開始，它們的虛線多邊形大致勾勒出我們想建構的曲線。", run_time=_audio_dur_0)
        anim_time_1 = 3.000 * _scale_1
        self.play(
            LaggedStart(
                FadeIn(P0), FadeIn(P1), FadeIn(P2), FadeIn(P3),
                Write(labelP0), Write(labelP1), Write(labelP2), Write(labelP3),
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )
        self.play(
            LaggedStart(
                Create(poly01), Create(poly12), Create(poly23),
                lag_ratio=0.2,
            ),
            run_time=2.0,
        )
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N01_bezier_curve_1780053079/media/audio/Using_the_de_Castelj_af8830b653/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 8.04  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 3.000)
        self.set_subtitle("在 t 等於 0.4 時，沿每條邊插值得到三個綠色點，這是第一層遞迴。", run_time=_audio_dur_1)
        anim_time_2 = 3.000 * _scale_2
        self.play(Indicate(poly01, color=GREEN), run_time=0.7)
        self.play(
            LaggedStart(Create(Q0), Create(Q1), Create(Q2), lag_ratio=0.15),
            run_time=1.0,
        )
        self.play(
            LaggedStart(Create(lineQ0), Create(lineQ1), lag_ratio=0.2),
            run_time=1.3,
        )
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N01_bezier_curve_1780053079/media/audio/Using_the_de_Castelj_af8830b653/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 7.22  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.700)
        self.set_subtitle("在兩條綠色線段上重複插值，產生兩個橘色點與一條新的連接線段。", run_time=_audio_dur_2)
        anim_time_3 = 2.700 * _scale_3
        self.play(Indicate(lineQ0, color=ORANGE), run_time=0.7)
        self.play(
            LaggedStart(Create(R0), Create(R1), lag_ratio=0.15),
            run_time=1.0,
        )
        self.play(Create(lineR), run_time=1.0)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N01_bezier_curve_1780053079/media/audio/Using_the_de_Castelj_af8830b653/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 7.20  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.000)
        self.set_subtitle("在橘色線段上做最後一次插值，將一切收斂成位於曲線上的單一黃色點。", run_time=_audio_dur_3)
        anim_time_4 = 2.000 * _scale_4
        self.play(Create(curvePoint), run_time=1.0)
        self.play(Circumscribe(curvePoint, color=YELLOW), run_time=1.0)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N01_bezier_curve_1780053079/media/audio/Using_the_de_Castelj_af8830b653/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 8.33  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 4.000)
        self.set_subtitle("讓 t 從 0 掃到 1，這個遞迴在每一處重複，移動的點便描繪出完整平滑的三次貝茲曲線。", run_time=_audio_dur_4)
        anim_time_5 = 4.000 * _scale_5
        self.play(
            FadeOut(Q0), FadeOut(Q1), FadeOut(Q2),
            FadeOut(R0), FadeOut(R1),
            FadeOut(lineQ0), FadeOut(lineQ1), FadeOut(lineR),
            run_time=0.8,
        )
        t_tracker = ValueTracker(0.0)
        curvePoint.add_updater(
            lambda m: m.move_to(bezierCurve.point_from_proportion(t_tracker.get_value()))
        )
        self.play(
            Create(bezierCurve),
            t_tracker.animate.set_value(1.0),
            run_time=4.0,
            rate_func=linear,
        )
        curvePoint.clear_updaters()
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)