# [VISUAL REASONING]
# Riemann sum convergence for ∫₀^π sin(x)dx using midpoint rectangles.
# ValueTracker drives n from 4→32 with always_redraw rectangles, n_readout, and area_readout.
# Static axes + curve + title frame the scene; final step reveals true value = 2.

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
        # Static objects
        title_text = MathTex(r"\int_0^{\pi} \sin(x)\,dx \;\approx\; \sum_{i=1}^{n} f(x_i^*)\,\Delta x").to_edge(UP, buff=0.4)

        axes_main = Axes(
            x_range=[0, 3.3, 1],
            y_range=[0, 1.2, 0.5],
            x_length=9,
            y_length=3.6,
            axis_config={"include_numbers": True},
        ).move_to(ORIGIN + 0.2 * DOWN)

        sine_curve = axes_main.plot(lambda t: np.sin(t), x_range=[0, PI, 0.01], color=BLUE)
        curve_label = MathTex(r"f(x)=\sin(x)").next_to(sine_curve, UP, buff=0.1)

        # ValueTracker for n
        n_tracker = ValueTracker(4)

        def _build_rects():
            n = int(n_tracker.get_value())
            dx = PI / n
            rects = VGroup()
            for i in range(n):
                xm = i * dx + dx / 2
                h = np.sin(xm)
                bl = axes_main.c2p(i * dx, 0)
                tr = axes_main.c2p((i + 1) * dx, h)
                width = tr[0] - bl[0]
                height = tr[1] - bl[1]
                r = Rectangle(
                    width=width,
                    height=height,
                    fill_color=YELLOW,
                    fill_opacity=0.5,
                    stroke_width=1,
                    stroke_color=YELLOW_E,
                ).move_to([(bl[0] + tr[0]) / 2, (bl[1] + tr[1]) / 2, 0])
                rects.add(r)
            return rects

        def _compute_area():
            n = int(n_tracker.get_value())
            dx = PI / n
            return sum(np.sin(i * dx + dx / 2) * dx for i in range(n))

        riemann_rects = always_redraw(_build_rects)

        n_label = MathTex("n = ")
        n_value = Integer(4)
        n_readout = VGroup(n_label, n_value).arrange(RIGHT, buff=0.1).move_to(3.5 * LEFT + 2.4 * DOWN)
        n_value.add_updater(lambda m: m.set_value(int(n_tracker.get_value())))

        area_label = MathTex(r"S_n \approx")
        area_value = DecimalNumber(0.0, num_decimal_places=4)
        area_readout = VGroup(area_label, area_value).arrange(RIGHT, buff=0.1).move_to(1.5 * RIGHT + 2.4 * DOWN)
        area_value.add_updater(lambda m: m.set_value(_compute_area()))
        true_value_box = MathTex(r"True value = 2").move_to(4.5 * RIGHT + 2.4 * DOWN)

        # Subtitle Step 1
        self.set_subtitle("我們要計算正弦函數從零到 π 的面積。黎曼的想法：把區域切成細長矩形，再加總面積。")

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/e8e61d1b/media/audio/Using_the_rectangle__eec1b53f6c/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 9.62  # [audio-sync]
        # Step 1
        shaded_hint = axes_main.get_area(sine_curve, x_range=[0, PI], color=BLUE, opacity=0.15)
        anim_time_1 = _audio_dur_0
        self.play(
            LaggedStart(
                Write(title_text),
                Create(axes_main),
                Create(sine_curve),
                Write(curve_label),
                FadeIn(shaded_hint),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1)

        # Subtitle Step 2
        self.set_subtitle("先從四個中點矩形開始。每個寬度是 Δx 等於 π 除以 n，高度等於 f 在該區間中點的函數值。", run_time=_audio_dur_0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/e8e61d1b/media/audio/Using_the_rectangle__eec1b53f6c/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 10.49  # [audio-sync]
        # Step 2
        self.add(riemann_rects)
        midpoint_dot = Dot(
            axes_main.c2p(PI / 4 / 2 + 0, np.sin(PI / 4 / 2)),
            color=RED,
        )
        first_dx = PI / 4
        brace = Brace(
            Line(axes_main.c2p(0, 0), axes_main.c2p(first_dx, 0)),
            DOWN,
            buff=0.05,
        )
        brace_label = brace.get_tex(r"\Delta x")

        anim_time_2 = _audio_dur_1
        self.play(
            LaggedStart(
                FadeOut(shaded_hint),
                FadeIn(riemann_rects),
                FadeIn(n_readout),
                FadeIn(area_readout),
                Indicate(midpoint_dot),
                AnimationGroup(GrowFromCenter(brace), Write(brace_label)),
                lag_ratio=0.25,
                run_time=anim_time_2,
            )
        )
        self.wait(0.1)

        # Subtitle Step 3
        self.set_subtitle("看看細分分割時會發生什麼。矩形數量從四，平滑增加到八、十六，一路到三十二。", run_time=_audio_dur_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/e8e61d1b/media/audio/Using_the_rectangle__eec1b53f6c/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 9.94  # [audio-sync]
        # Step 3
        anim_time_3 = _audio_dur_2
        self.play(
            n_tracker.animate.set_value(32),
            FadeOut(brace),
            FadeOut(brace_label),
            FadeOut(midpoint_dot),
            run_time=anim_time_3,
            rate_func=smooth,
        )
        self.wait(0.1)

        # Subtitle Step 4
        self.set_subtitle("階梯與曲線之間的誤差幾乎消失。黎曼和收斂到真實積分值，正好等於二。", run_time=_audio_dur_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/e8e61d1b/media/audio/Using_the_rectangle__eec1b53f6c/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 9.55  # [audio-sync]
        # Step 4
        arrow = DashedVMobject(
            Line(area_readout.get_right(), true_value_box.get_left(), color=GREEN)
        )
        integral_part = title_text

        anim_time_4 = _audio_dur_3
        self.play(
            LaggedStart(
                FadeIn(true_value_box),
                Indicate(area_readout, color=GREEN),
                Create(arrow),
                Indicate(integral_part),
                Flash(riemann_rects.get_center(), color=YELLOW, flash_radius=0.5),
                lag_ratio=0.25,
                run_time=anim_time_4,
            )
        )
        self.wait(0.1)