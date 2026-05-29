# [VISUAL REASONING]
# Overlay successive Taylor polynomials on ln(1+x) to show convergence near 0
# and divergence outside |x|<1. Axes centered, equation banner above, title in header,
# convergence label in footer. Use axes.plot for proper coordinate mapping.

from manim import *
import math


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
        # Title
        title = Text("Taylor Series of ln(1+x)", color=WHITE, font_size=36)
        title.to_edge(UP)

        # Axes
        axes = Axes(
            x_range=[-1.8, 1.8, 0.5],
            y_range=[-2.5, 1.5, 1],
            x_length=7,
            y_length=4,
            axis_config={"color": GREY},
        ).move_to(np.array([0, -0.3, 0]))

        # Curves via axes.plot for correct coordinate mapping
        ln_curve = axes.plot(lambda x: math.log(1 + x), x_range=[-0.95, 1.7, 0.02], color=WHITE)
        poly1 = axes.plot(lambda x: x, x_range=[-1.7, 1.7, 0.02], color=BLUE)
        poly2 = axes.plot(lambda x: x - x**2 / 2, x_range=[-1.7, 1.7, 0.02], color=GREEN)
        poly3 = axes.plot(lambda x: x - x**2 / 2 + x**3 / 3, x_range=[-1.7, 1.7, 0.02], color=YELLOW)
        poly4 = axes.plot(
            lambda x: x - x**2 / 2 + x**3 / 3 - x**4 / 4,
            x_range=[-1.7, 1.7, 0.02],
            color=ORANGE,
        )

        # Equations banner
        eq1 = MathTex(r"\ln(1+x) \approx x", color=BLUE).move_to(np.array([0, 2.3, 0]))
        eq2 = MathTex(r"\ln(1+x) \approx x - \tfrac{x^2}{2}", color=GREEN).move_to(np.array([0, 2.3, 0]))
        eq3 = MathTex(
            r"\ln(1+x) \approx x - \tfrac{x^2}{2} + \tfrac{x^3}{3}", color=YELLOW
        ).move_to(np.array([0, 2.3, 0]))
        eq4 = MathTex(
            r"\ln(1+x) \approx x - \tfrac{x^2}{2} + \tfrac{x^3}{3} - \tfrac{x^4}{4}",
            color=ORANGE,
        ).move_to(np.array([0, 2.3, 0]))

        # Convergence boundaries (mapped through axes)
        bound_left = DashedLine(
            start=axes.c2p(-1, -2.0), end=axes.c2p(-1, 1.3), color=RED
        )
        bound_right = DashedLine(
            start=axes.c2p(1, -2.0), end=axes.c2p(1, 1.3), color=RED
        )
        roc_label = MathTex(r"|x| < 1", color=RED, font_size=36).move_to(np.array([0, -2.8, 0]))

        # Initial setup: title + axes
        self.play(Write(title), Create(axes), run_time=1.5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q20_taylor_log_1779989445/media/audio/Visualizing_the_Tayl_a0110213df/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 6.62  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 2.000)
        self.set_subtitle("這是 ln(1+x) 的真實曲線，我們要在零附近逼近的目標函數。", run_time=_audio_dur_0)
        anim_time_1 = 2.000 * _scale_1
        self.play(Create(ln_curve), run_time=anim_time_1)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q20_taylor_log_1779989445/media/audio/Visualizing_the_Tayl_a0110213df/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 5.66  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.600)
        self.set_subtitle("第一項泰勒展開就是 x，一條在原點與曲線相切的直線。", run_time=_audio_dur_1)
        anim_time_2 = 2.600 * _scale_2
        self.play(Write(eq1), Create(poly1), run_time=1.8)
        self.play(Circumscribe(eq1, color=YELLOW), run_time=0.8)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q20_taylor_log_1779989445/media/audio/Visualizing_the_Tayl_a0110213df/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 6.26  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.000)
        self.set_subtitle("加入負 x 平方除以二，使近似往下彎，更貼近曲線。", run_time=_audio_dur_2)
        anim_time_3 = 2.000 * _scale_3
        self.play(
            TransformMatchingTex(eq1, eq2),
            ReplacementTransform(poly1, poly2),
            run_time=anim_time_3,
        )
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q20_taylor_log_1779989445/media/audio/Visualizing_the_Tayl_a0110213df/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 7.54  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.500)
        self.set_subtitle("每加一項就讓零附近的擬合更緊，但在 x 等於正負一外面會發散。", run_time=_audio_dur_3)
        anim_time_4 = 2.500 * _scale_4
        self.play(
            TransformMatchingTex(eq2, eq3),
            ReplacementTransform(poly2, poly3),
            run_time=1.25,
        )
        self.play(
            TransformMatchingTex(eq3, eq4),
            ReplacementTransform(poly3, poly4),
            run_time=1.25,
        )
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q20_taylor_log_1779989445/media/audio/Visualizing_the_Tayl_a0110213df/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.94  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.800)
        self.set_subtitle("此級數只在絕對值 x 小於一時收斂，由這兩條紅色虛線標示。", run_time=_audio_dur_4)
        anim_time_5 = 2.800 * _scale_5
        self.play(
            Create(bound_left),
            Create(bound_right),
            Write(roc_label),
            run_time=2.0,
        )
        self.play(Indicate(roc_label, color=RED), run_time=0.8)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)