from manim import *
import math
import numpy as np

# [VISUAL REASONING]
# Single coordinate system showing sin(x) on [0, pi].
# ValueTracker n_tracker drives midpoint Riemann rectangles via always_redraw.
# Sum readout and n readout update live. Final result reveals exact value = 2.

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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q01_riemann_sum_1779992973/media/audio/Calculate_the_value__0a659d9c83/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 8.71  # [audio-sync]
        # Step 1
        self.set_subtitle("我們要計算 sin(x) 從 0 到 π 的定積分，幾何上就是這段區間內正弦曲線下方的面積。", run_time=_audio_dur_0)

        title = Text("Riemann Sum Approximation of ∫₀^π sin(x) dx", font_size=32).to_edge(UP, buff=0.4)

        axes_main = Axes(
            x_range=[0, 3.3, 0.5],
            y_range=[0, 1.2, 0.5],
            x_length=9,
            y_length=3.8,
            axis_config={"include_numbers": False},
        ).move_to(ORIGIN)

        x_label_0 = MathTex("0", font_size=28).next_to(axes_main, DOWN, buff=0.05, aligned_edge=LEFT)
        x_label_pi = MathTex("\\pi", font_size=28).next_to(axes_main, DOWN, buff=0.05, aligned_edge=RIGHT)

        sine_curve = ParametricFunction(
            lambda t: axes_main.c2p(t, math.sin(t)),
            t_range=[0, 3.14159, 0.01],
            color=BLUE,
        )

        curve_label = MathTex("f(x)=\\sin(x)", font_size=32, color=BLUE).next_to(
            axes_main, UP, buff=0.1, aligned_edge=RIGHT
        )

        integral_expr = MathTex("\\int_{0}^{\\pi} \\sin(x)\\,dx", font_size=36).to_corner(DL, buff=0.5)

        anim_time_1 = _audio_dur_0
        self.play(
            LaggedStart(
                Write(title),
                Create(axes_main),
                FadeIn(x_label_0, x_label_pi),
                Create(sine_curve),
                Write(curve_label),
                Write(integral_expr),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q01_riemann_sum_1779992973/media/audio/Calculate_the_value__0a659d9c83/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 8.88  # [audio-sync]
        # Step 2
        self.set_subtitle("我們把區間分成 n 個矩形，每個寬度為 π/n，並使用中點法決定矩形高度。", run_time=_audio_dur_1)

        n_tracker = ValueTracker(4)

        def _build_rects():
            n = int(n_tracker.get_value())
            n = max(1, n)
            dx = math.pi / n
            rects = VGroup()
            for i in range(n):
                xm = (i + 0.5) * dx
                h = math.sin(xm)
                p0 = axes_main.c2p(i * dx, 0)
                p1 = axes_main.c2p((i + 1) * dx, h)
                w = p1[0] - p0[0]
                hp = p1[1] - p0[1]
                r = Rectangle(
                    width=w,
                    height=hp,
                    fill_color=GREEN,
                    fill_opacity=0.5,
                    stroke_color=GREEN,
                    stroke_width=1.5,
                ).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0])
                rects.add(r)
            return rects

        riemann_rects = always_redraw(_build_rects)

        def _sum_value():
            n = max(1, int(n_tracker.get_value()))
            dx = math.pi / n
            s = sum(math.sin((i + 0.5) * dx) for i in range(n)) * dx
            return s

        # Discrete readouts updated via Transform between steps (no updater+become).
        def _make_n_readout(n_val):
            return MathTex(f"n = {n_val}", font_size=32, color=YELLOW).to_corner(DR, buff=0.5)

        def _make_sum_readout(n_val, anchor):
            return MathTex(f"S_n \\approx {_sum_value_for(n_val):.2f}", font_size=32, color=YELLOW).next_to(anchor, UP, buff=0.15)

        def _sum_value_for(n):
            n = max(1, int(n))
            dx = math.pi / n
            return sum(math.sin((i + 0.5) * dx) for i in range(n)) * dx

        n_readout = _make_n_readout(4)
        sum_readout = _make_sum_readout(4, n_readout)

        anim_time_2 = _audio_dur_1
        self.play(
            LaggedStart(
                FadeIn(riemann_rects),
                Write(n_readout),
                Write(sum_readout),
                Indicate(curve_label, scale_factor=1.1),
                lag_ratio=0.25,
                run_time=anim_time_2,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q01_riemann_sum_1779992973/media/audio/Calculate_the_value__0a659d9c83/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 8.62  # [audio-sync]
        # Step 3
        self.set_subtitle("當 n 越來越大，矩形變得更細，更貼近曲線，黎曼和也穩定趨近真正的面積。", run_time=_audio_dur_2)

        anim_time_3 = _audio_dur_2
        step_rt = anim_time_3 / 3.0
        for n_val in (12, 24, 48):
            new_n = _make_n_readout(n_val)
            new_s = _make_sum_readout(n_val, new_n)
            self.play(
                n_tracker.animate.set_value(n_val),
                Transform(n_readout, new_n),
                Transform(sum_readout, new_s),
                run_time=step_rt,
            )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q01_riemann_sum_1779992973/media/audio/Calculate_the_value__0a659d9c83/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 9.70  # [audio-sync]
        # Step 4
        self.set_subtitle("當 n 趨近無限大時,黎曼和恰好收斂到反導數的計算結果,積分值等於二。", run_time=_audio_dur_3)

        final_result = MathTex(
            "\\int_{0}^{\\pi}\\sin(x)\\,dx = 2", font_size=44, color=GOLD
        ).move_to(ORIGIN)

        shaded_area = axes_main.get_area(sine_curve, x_range=[0, 3.14159], color=GOLD, opacity=0.4)

        highlight_box = SurroundingRectangle(final_result, color=GOLD, buff=0.2)

        anim_time_4 = _audio_dur_3
        self.play(
            LaggedStart(
                FadeOut(riemann_rects, n_readout, sum_readout, curve_label, integral_expr),
                Indicate(sine_curve, color=GOLD, scale_factor=1.05),
                FadeIn(shaded_area),
                Write(final_result),
                Create(highlight_box),
                lag_ratio=0.25,
                run_time=anim_time_4,
            )
        )
        self.wait(0.1)