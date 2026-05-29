# [VISUAL REASONING]
# Show convergence by progressively transforming a sine curve into higher-order
# partial sums on shared axes, with the target square wave as a constant reference.
# Title at HEADER, Axes at CONTENT center, formula at FOOTER below axes.

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
        # Setup: title and axes (always visible)
        title = Text("Fourier Series: Approximating a Square Wave",
                     color=WHITE, font_size=34).to_edge(UP, buff=0.4)

        axes = Axes(
            x_range=[-6.5, 6.5, 1.5708],
            y_range=[-1.6, 1.6, 1],
            x_length=11,
            y_length=4,
            axis_config={"color": GREY},
        ).move_to(ORIGIN + np.array([0, 0.2, 0]))

        self.add(title, axes)

        # Curves (parametric in plot space, then shifted to axes)
        square_wave = ParametricFunction(
            lambda t: [t, 1.2 if (t % 6.2832) < 3.1416 else -1.2, 0],
            t_range=[-6.28, 6.28, 0.005],
            color=GREY,
            stroke_width=3,
        ).move_to(axes.get_center())

        curve_s1 = ParametricFunction(
            lambda t: [t, (4 / 3.14159) * 1.2 * math.sin(t), 0],
            t_range=[-6.28, 6.28, 0.02],
            color=YELLOW,
            stroke_width=4,
        ).move_to(axes.get_center())

        curve_s3 = ParametricFunction(
            lambda t: [t, (4 / 3.14159) * 1.2 * (math.sin(t) + math.sin(3 * t) / 3), 0],
            t_range=[-6.28, 6.28, 0.02],
            color=ORANGE,
            stroke_width=4,
        ).move_to(axes.get_center())

        curve_s5 = ParametricFunction(
            lambda t: [t, (4 / 3.14159) * 1.2 * (math.sin(t) + math.sin(3 * t) / 3 + math.sin(5 * t) / 5), 0],
            t_range=[-6.28, 6.28, 0.02],
            color=RED,
            stroke_width=4,
        ).move_to(axes.get_center())

        curve_s9 = ParametricFunction(
            lambda t: [t, (4 / 3.14159) * 1.2 * (
                math.sin(t) + math.sin(3 * t) / 3 + math.sin(5 * t) / 5
                + math.sin(7 * t) / 7 + math.sin(9 * t) / 9), 0],
            t_range=[-6.28, 6.28, 0.02],
            color=GREEN,
            stroke_width=4,
        ).move_to(axes.get_center())

        formula_s1 = MathTex(r"S_1(x)=\tfrac{4}{\pi}\sin x", color=YELLOW).move_to([0, -2.3, 0])
        formula_s3 = MathTex(r"S_3(x)=\tfrac{4}{\pi}\left(\sin x+\tfrac{\sin 3x}{3}\right)", color=ORANGE).move_to([0, -2.3, 0])
        formula_s5 = MathTex(r"S_5(x)=\tfrac{4}{\pi}\left(\sin x+\tfrac{\sin 3x}{3}+\tfrac{\sin 5x}{5}\right)", color=RED).move_to([0, -2.3, 0])
        formula_s9 = MathTex(r"S_9(x)=\tfrac{4}{\pi}\sum_{k=1,3,5,7,9}\tfrac{\sin kx}{k}", color=GREEN).move_to([0, -2.3, 0])

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q12_fourier_square_1779987975/media/audio/Approximate_a_square_f5ca0c69d6/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 5.93  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 2.500)
        self.set_subtitle("這是我們的目標:一個只用正弦函數來重建的方波。", run_time=_audio_dur_0)
        anim_time_1 = 2.500 * _scale_1
        self.play(Create(square_wave), run_time=2.5)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q12_fourier_square_1779987975/media/audio/Approximate_a_square_f5ca0c69d6/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 5.83  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.000)
        self.set_subtitle("先從第一諧波開始:單一正弦波已經抓到基本形狀。", run_time=_audio_dur_1)
        anim_time_2 = 2.000 * _scale_2
        self.play(Create(curve_s1), Write(formula_s1), run_time=2.0)
        self.play(Circumscribe(formula_s1, color=YELLOW), run_time=1.2)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 - 1.2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q12_fourier_square_1779987975/media/audio/Approximate_a_square_f5ca0c69d6/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 5.18  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.500)
        self.set_subtitle("加入第三諧波後,波峰變平、邊緣更陡峭。", run_time=_audio_dur_2)
        anim_time_3 = 2.500 * _scale_3
        self.play(
            ReplacementTransform(curve_s1, curve_s3),
            TransformMatchingTex(formula_s1, formula_s3),
            run_time=2.5,
        )
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q12_fourier_square_1779987975/media/audio/Approximate_a_square_f5ca0c69d6/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 5.88  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.500)
        self.set_subtitle("再納入第五諧波,逼近方波的程度更上一層樓。", run_time=_audio_dur_3)
        anim_time_4 = 2.500 * _scale_4
        self.play(
            ReplacementTransform(curve_s3, curve_s5),
            TransformMatchingTex(formula_s3, formula_s5),
            run_time=2.5,
        )
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q12_fourier_square_1779987975/media/audio/Approximate_a_square_f5ca0c69d6/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 7.18  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 3.000)
        self.set_subtitle("把奇數諧波加到第九階,總和幾乎貼合方波,展示傅立葉收斂。", run_time=_audio_dur_4)
        anim_time_5 = 3.000 * _scale_5
        self.play(
            ReplacementTransform(curve_s5, curve_s9),
            TransformMatchingTex(formula_s5, formula_s9),
            run_time=3.0,
        )
        self.play(Indicate(curve_s9, color=GREEN), run_time=1.2)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.2 + 0.1)
        self.wait(remaining_5)