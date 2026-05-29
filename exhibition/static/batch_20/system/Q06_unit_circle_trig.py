# [VISUAL REASONING]
# Split-screen: unit circle (left) + sine plot (right), linked by dashed projector.
# ValueTracker drives theta; updaters sync moving_dot, radius_line, projector_line, trace_dot.
# TracedPath on trace_dot draws the sine curve as theta sweeps 0 -> 2π.

from manim import *
import numpy as np

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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q06_unit_circle_trig_1779987057/media/audio/Visualization_of_a_p_b5e5dd440b/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 5.30  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 2.000)
        title = Text("Unit Circle and the Sine Function", color=WHITE, font_size=34)
        title.move_to(ORIGIN + np.array([0, 3.2, 0]))

        circle_center = np.array([-3.8, 0, 0])
        unit_circle = Circle(radius=1.3, color=BLUE).move_to(circle_center)
        circle_axes = Axes(
            x_range=[-1.6, 1.6, 1],
            y_range=[-1.6, 1.6, 1],
            x_length=3.2,
            y_length=3.2,
            axis_config={"color": GREY, "include_ticks": False},
        ).move_to(circle_center)

        sine_axes = Axes(
            x_range=[0, 6.5, 1.5708],
            y_range=[-1.5, 1.5, 1],
            x_length=6.0,
            y_length=3.0,
            axis_config={"color": GREY},
        ).move_to(ORIGIN + np.array([2.7, 0, 0]))

        sine_label = MathTex(r"y=\sin(\theta)", color=YELLOW)
        sine_label.move_to(ORIGIN + np.array([5.3, 1.8, 0]))

        self.set_subtitle("我們從左側的單位圓和右側空白的正弦座標軸開始。", run_time=_audio_dur_0)
        anim_time_1 = 2.000 * _scale_1
        self.play(Write(title), run_time=1.0)
        self.play(
            LaggedStart(
                Create(circle_axes),
                Create(unit_circle),
                Create(sine_axes),
                lag_ratio=0.2,
            ),
            run_time=2.0,
        )
        remaining_1 = max(0.1, _audio_dur_0 - (1.0 + anim_time_1) + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q06_unit_circle_trig_1779987057/media/audio/Visualization_of_a_p_b5e5dd440b/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 6.91  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 1.800)
        theta = ValueTracker(0.0)
        R = 1.3

        def dot_pos():
            t = theta.get_value()
            return circle_center + R * np.array([np.cos(t), np.sin(t), 0])

        moving_dot = Dot(color=RED, radius=0.09).move_to(dot_pos())
        moving_dot.add_updater(lambda m: m.move_to(dot_pos()))

        radius_line = always_redraw(
            lambda: Line(circle_center, dot_pos(), color=GREEN)
        )

        self.set_subtitle("在圓上放一個點，並以從正 x 軸出發的半徑線標示角度 θ。", run_time=_audio_dur_1)
        anim_time_2 = 1.800 * _scale_2
        self.play(Create(radius_line), FadeIn(moving_dot), run_time=anim_time_2)
        self.play(Circumscribe(moving_dot, color=YELLOW), run_time=1.0)
        remaining_2 = max(0.1, _audio_dur_1 - (anim_time_2 + 1.0) + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q06_unit_circle_trig_1779987057/media/audio/Visualization_of_a_p_b5e5dd440b/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 5.76  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 1.500)
        def trace_pos():
            t = theta.get_value()
            return sine_axes.c2p(t, np.sin(t))

        projector_line = always_redraw(
            lambda: DashedLine(dot_pos(), trace_pos(), color=YELLOW)
        )
        trace_dot = Dot(color=YELLOW, radius=0.08).move_to(trace_pos())
        trace_dot.add_updater(lambda m: m.move_to(trace_pos()))

        self.set_subtitle("虛線將該點的高度水平投影到右側的正弦座標軸上。", run_time=_audio_dur_2)
        anim_time_3 = 1.500 * _scale_3
        self.play(Create(projector_line), FadeIn(trace_dot), run_time=anim_time_3)
        self.play(Indicate(projector_line, color=YELLOW), run_time=1.0)
        remaining_3 = max(0.1, _audio_dur_2 - (anim_time_3 + 1.0) + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q06_unit_circle_trig_1779987057/media/audio/Visualization_of_a_p_b5e5dd440b/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.41  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 6.000)
        traced = TracedPath(trace_dot.get_center, stroke_color=YELLOW, stroke_width=4)
        self.add(traced)

        self.set_subtitle("當 θ 增加時，點逆時針旋轉，其高度便描繪出正弦曲線。", run_time=_audio_dur_3)
        anim_time_4 = 6.000 * _scale_4
        self.play(Write(sine_label), run_time=1.0)
        self.play(
            theta.animate.set_value(2 * PI),
            run_time=anim_time_4,
            rate_func=linear,
        )
        remaining_4 = max(0.1, _audio_dur_3 - (1.0 + anim_time_4) + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q06_unit_circle_trig_1779987057/media/audio/Visualization_of_a_p_b5e5dd440b/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 5.45  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        footer = Text(
            "The y-coordinate of the rotating point IS sin(theta).",
            color=WHITE,
            font_size=26,
        ).move_to(ORIGIN + np.array([0, -2.3, 0]))

        self.set_subtitle("一圈旋轉之後，描繪出的曲線完成了一個正弦週期。", run_time=_audio_dur_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(FadeIn(footer), Indicate(footer, color=YELLOW), run_time=anim_time_5)
        self.play(Circumscribe(sine_label, color=YELLOW), run_time=1.0)
        remaining_5 = max(0.1, _audio_dur_4 - (anim_time_5 + 1.0) + 0.1)
        self.wait(remaining_5)