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
    """
    [VISUAL REASONING]
    1. Pedagogical Goal: Show how Taylor partial sums converge to cos(x),
       one term at a time, by overlaying successively higher-order polynomials
       on the true cosine curve.
    2. Layout Strategy: HEADER holds title + evolving Taylor formula; CONTENT
       holds shared axes with cos(x) and approximation curves; FOOTER holds a
       color legend.
    3. Anti-Overlap: Axes centered slightly low, title/formula at top edge,
       legend pinned to bottom edge (y above -2.5).
    4. Color Coding: cos true = WHITE, P0 = GREY, P2 = YELLOW, P4 = ORANGE,
       P6 = RED, so successive overlays read as "getting closer".
    """

    def construct(self):
        self._instrumentor = SceneInstrumentor(self, log_path='/Users/liaozhenting/Desktop/LLManim_Agent/scene_state_log.json')
        self._sm = SubtitleManager(self)
        self.set_subtitle = self._sm.show
        registry = {}

        title = Text("Taylor Series of cos(x)", font_size=34).to_edge(UP)
        registry["title"] = title

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=9,
            y_length=3.6,
        ).move_to(ORIGIN + DOWN * 0.3)
        registry["axes_main"] = axes

        def clamp(y):
            return max(-1.5, min(1.5, y))

        cos_curve = axes.plot(lambda x: np.cos(x), x_range=[-4, 4], color=WHITE)
        registry["cos_curve"] = cos_curve

        cos_label = MathTex(r"\cos(x)", font_size=30).next_to(
            axes.c2p(0, np.cos(0)), UP, buff=0.2
        )
        registry["cos_label"] = cos_label

        p0_curve = axes.plot(lambda x: 1.0, x_range=[-4, 4], color=GREY)
        registry["p0_curve"] = p0_curve

        p2_curve = axes.plot(
            lambda x: clamp(1 - x**2 / 2), x_range=[-4, 4], color=YELLOW
        )
        registry["p2_curve"] = p2_curve

        p4_curve = axes.plot(
            lambda x: clamp(1 - x**2 / 2 + x**4 / 24), x_range=[-4, 4], color=ORANGE
        )
        registry["p4_curve"] = p4_curve

        p6_curve = axes.plot(
            lambda x: clamp(1 - x**2 / 2 + x**4 / 24 - x**6 / 720),
            x_range=[-4, 4],
            color=RED,
        )
        registry["p6_curve"] = p6_curve

        formula = MathTex(r"\cos(x)", r"\approx", r"1", font_size=32).next_to(
            title, DOWN, buff=0.25
        )
        registry["formula"] = formula

        legend = Text(
            "grey:1   yellow:-x^2/2!   orange:+x^4/4!   red:-x^6/6!",
            font_size=20,
        ).move_to(np.array([0, -2.0, 0]))  # FOOTER zone, above subtitle exclusion
        registry["legend"] = legend

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N02_taylor_cosine_1780053619/media/audio/Explanation_of_the_T_3cc76c231b/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 10.13  # [audio-sync]
        # Step 1
        self.set_subtitle(
            "這是真實的餘弦曲線。我們的目標是用泰勒級數所建構的多項式，一項一項地逼近這條平滑的波。"
        , run_time=_audio_dur_0)
        anim_time_1 = _audio_dur_0
        self.play(
            LaggedStart(
                Write(title),
                Create(axes),
                Create(cos_curve),
                Write(cos_label),
                Write(formula),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N02_taylor_cosine_1780053619/media/audio/Explanation_of_the_T_3cc76c231b/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 9.34  # [audio-sync]
        # Step 2
        self.set_subtitle(
            "我們從常數項開始，也就是 1。這條水平線只在原點附近與餘弦吻合，因為函數在那裡等於 1。"
        , run_time=_audio_dur_1)
        anim_time_2 = _audio_dur_1
        origin_dot = Dot(axes.c2p(0, 1), color=GREY)
        self.play(
            LaggedStart(
                Create(p0_curve),
                FadeIn(legend),
                Flash(axes.c2p(0, 1), color=YELLOW),
                Indicate(formula.get_part_by_tex("1")),
                lag_ratio=0.25,
                run_time=anim_time_2,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N02_taylor_cosine_1780053619/media/audio/Explanation_of_the_T_3cc76c231b/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 8.57  # [audio-sync]
        # Step 3
        self.set_subtitle(
            "加入減去 x 平方除以 2 階乘，使直線向下彎曲，黃色拋物線現在沿著餘弦穿過中央的隆起。"
        , run_time=_audio_dur_2)
        anim_time_3 = _audio_dur_2
        formula_2 = MathTex(
            r"\cos(x)", r"\approx", r"1", r"-", r"\frac{x^2}{2!}", font_size=32
        ).next_to(title, DOWN, buff=0.25)
        self.play(
            LaggedStart(
                TransformMatchingTex(formula, formula_2),
                Create(p2_curve),
                FadeOut(p0_curve),
                Indicate(cos_curve),
                lag_ratio=0.25,
                run_time=anim_time_3,
            )
        )
        registry["formula"] = formula_2
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N02_taylor_cosine_1780053619/media/audio/Explanation_of_the_T_3cc76c231b/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 9.96  # [audio-sync]
        # Step 4
        self.set_subtitle(
            "再加上 x 的四次方除以 4 階乘，把尾端重新抬高，橘色曲線現在能在明顯更寬的區間內追蹤餘弦。"
        , run_time=_audio_dur_3)
        anim_time_4 = _audio_dur_3
        formula_3 = MathTex(
            r"\cos(x)",
            r"\approx",
            r"1",
            r"-",
            r"\frac{x^2}{2!}",
            r"+",
            r"\frac{x^4}{4!}",
            font_size=32,
        ).next_to(title, DOWN, buff=0.25)
        self.play(
            LaggedStart(
                TransformMatchingTex(formula_2, formula_3),
                Create(p4_curve),
                FadeOut(p2_curve),
                Indicate(cos_curve),
                lag_ratio=0.25,
                run_time=anim_time_4,
            )
        )
        registry["formula"] = formula_3
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N02_taylor_cosine_1780053619/media/audio/Explanation_of_the_T_3cc76c231b/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 11.42  # [audio-sync]
        # Step 5
        self.set_subtitle(
            "加上減去 x 的六次方除以 6 階乘，得到紅色曲線，它幾乎完美地貼合真實餘弦。每加入一項，吻合範圍就更往外延伸。"
        , run_time=_audio_dur_4)
        anim_time_5 = _audio_dur_4
        formula_4 = MathTex(
            r"\cos(x)",
            r"\approx",
            r"1",
            r"-",
            r"\frac{x^2}{2!}",
            r"+",
            r"\frac{x^4}{4!}",
            r"-",
            r"\frac{x^6}{6!}",
            font_size=32,
        ).next_to(title, DOWN, buff=0.25)
        sweep = SurroundingRectangle(axes, color=RED, buff=0.1)
        self.play(
            LaggedStart(
                TransformMatchingTex(formula_3, formula_4),
                Create(p6_curve),
                FadeOut(p4_curve),
                Create(sweep),
                Indicate(cos_label),
                lag_ratio=0.25,
                run_time=anim_time_5,
            )
        )
        registry["formula"] = formula_4
        self.wait(0.1)