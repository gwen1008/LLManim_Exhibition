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
    # [VISUAL REASONING]
    # 1. Pedagogical Goal: Show Taylor series of cos(x) converging via successive polynomial approximations.
    # 2. Layout Strategy: Title in HEADER, shared Axes in CONTENT, evolving formula in FOOTER (y approx -2.3).
    # 3. Anti-Overlap: Tight y_range [-1.5,1.5], curves clipped to x in [-3.5,3.5]; formulas use ReplacementTransform to avoid stacking.
    # 4. Color Code: cos=GREY reference, p0=RED, p2=ORANGE, p4=GREEN for intuitive legend reading.
    def construct(self):
        self._instrumentor = SceneInstrumentor(self, log_path='/Users/liaozhenting/Desktop/LLManim_Agent/scene_state_log.json')
        self._sm = SubtitleManager(self)
        self.set_subtitle = self._sm.show
        title = Text("Taylor Series of cos(x)", color=WHITE, font_size=36)
        title.to_edge(UP)

        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-1.5, 1.5, 1],
            axis_config={"color": GREY},
        )
        axes.move_to(ORIGIN)

        cos_curve = axes.plot(lambda x: np.cos(x), x_range=[-3.5, 3.5], color=GREY)
        approx_p0 = axes.plot(lambda x: 1, x_range=[-3.5, 3.5], color=RED)
        approx_p2 = axes.plot(lambda x: 1 - x**2 / 2, x_range=[-3.5, 3.5], color=ORANGE)
        approx_p4 = axes.plot(lambda x: 1 - x**2 / 2 + x**4 / 24, x_range=[-3.5, 3.5], color=GREEN)

        formula_p0 = MathTex(r"\cos(x) \approx 1", color=RED).move_to([0, -2.3, 0])
        formula_p2 = MathTex(r"\cos(x) \approx 1 - \frac{x^2}{2!}", color=ORANGE).move_to([0, -2.3, 0])
        formula_p4 = MathTex(r"\cos(x) \approx 1 - \frac{x^2}{2!} + \frac{x^4}{4!}", color=GREEN).move_to([0, -2.3, 0])

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N02_taylor_cosine_1780053485/media/audio/Explanation_of_the_T_3cc76c231b/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 5.90  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.500)
        self.set_subtitle("這是真正的餘弦曲線，是每個近似都試圖貼合的目標。", run_time=_audio_dur_0)
        anim_time_1 = 1.500 * _scale_1
        self.play(Create(axes), run_time=1.5)
        self.play(Write(title), run_time=1.0)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 - 1.0 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N02_taylor_cosine_1780053485/media/audio/Explanation_of_the_T_3cc76c231b/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 5.26  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.000)
        self.set_subtitle("我們以灰色畫出實際的 cos(x)，作為想要重現的參考。", run_time=_audio_dur_1)
        anim_time_2 = 2.000 * _scale_2
        self.play(Create(cos_curve), run_time=2.0)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N02_taylor_cosine_1780053485/media/audio/Explanation_of_the_T_3cc76c231b/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 6.07  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 1.500)
        self.set_subtitle("先從常數項一開始，一條只在零附近貼合餘弦的水平線。", run_time=_audio_dur_2)
        anim_time_3 = 1.500 * _scale_3
        self.play(Create(approx_p0), Write(formula_p0), run_time=1.5)
        self.play(Circumscribe(formula_p0, color=YELLOW))
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 1.0 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N02_taylor_cosine_1780053485/media/audio/Explanation_of_the_T_3cc76c231b/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.94  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.000)
        self.set_subtitle("加上負 x 平方除以二階乘，曲線向下彎曲，從中間緊貼餘弦。", run_time=_audio_dur_3)
        anim_time_4 = 2.000 * _scale_4
        self.play(
            ReplacementTransform(approx_p0, approx_p2),
            ReplacementTransform(formula_p0, formula_p2),
            run_time=2.0,
        )
        self.play(Indicate(approx_p2, color=ORANGE))
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 - 1.0 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N02_taylor_cosine_1780053485/media/audio/Explanation_of_the_T_3cc76c231b/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 8.11  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        self.set_subtitle("加上 x 四次方除以四階乘修正了尾端，綠色曲線更廣地追蹤餘弦。", run_time=_audio_dur_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(
            ReplacementTransform(approx_p2, approx_p4),
            ReplacementTransform(formula_p2, formula_p4),
            run_time=2.0,
        )
        self.play(Indicate(approx_p4, color=GREEN))
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.0 + 0.1)
        self.wait(remaining_5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N02_taylor_cosine_1780053485/media/audio/Explanation_of_the_T_3cc76c231b/step_05.mp3")  # [auto-injected]
        _audio_dur_5 = 6.29  # [audio-sync]
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 2.000)
        self.set_subtitle("每增加一項就拓寬貼合範圍，因此級數穩定地處處收斂於餘弦。", run_time=_audio_dur_5)
        anim_time_6 = 2.000 * _scale_6
        self.play(Indicate(cos_curve), run_time=2.0)
        self.play(Circumscribe(approx_p4, color=YELLOW))
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 - 1.0 + 0.1)
        self.wait(remaining_6)