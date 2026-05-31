from manim import *

# [VISUAL REASONING]
# Overlaying successive Fourier partial sums on a single shared axis against the
# fixed gray square wave makes convergence and the Gibbs overshoot self-evident.
# Warm-to-cool colors (red->orange->yellow->green->teal) encode increasing harmonic
# order; previous sums fade to 0.35 opacity so the newest full-opacity curve stands out.

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
        registry = {}

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_Fourier_se_1f06ada7f3/step_00.mp3")  # [auto-injected] duration=5.47s
        _audio_dur_0 = 5.47  # [audio-sync] actual TTS duration
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.500)
        title = Text("Fourier Series: Square Wave", color=WHITE, font_size=36).to_edge(UP)
        registry["title"] = title

        axes = Axes(
            x_range=[-6.3, 6.3, 1.5707963],
            y_range=[-1.5, 1.5, 0.5],
            x_length=11.0,
            y_length=3.6,
            axis_config={"color": GREY},
        ).move_to(np.array([0, -0.3, 0]))
        registry["axes"] = axes

        self.set_subtitle("我們從目標出發：一個週期為 2π、振幅為 1 的方波。", run_time=_audio_dur_0)
        anim_time_1 = 1.500 * _scale_1
        self.play(Create(axes), run_time=anim_time_1)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_Fourier_se_1f06ada7f3/step_01.mp3")  # [auto-injected] duration=5.74s
        _audio_dur_1 = 5.74  # [audio-sync] actual TTS duration
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.500)
        square_wave = axes.plot(
            lambda x: 1 if (x % (2 * PI)) < PI else -1,
            color=GREY_B,
            stroke_width=4,
            use_smoothing=False,
            discontinuities=[k * PI for k in range(-3, 4)],
        )
        registry["square_wave"] = square_wave

        harm_label = Text("Target square wave", color=GREY_B, font_size=28).move_to(
            np.array([0, -2.2, 0])
        )
        registry["harm_label"] = harm_label

        self.set_subtitle("這條灰色曲線在每個半週期都在 +1 與 -1 之間急遽跳變。", run_time=_audio_dur_1)
        anim_time_2 = 2.500 * _scale_2
        self.play(
            Create(square_wave),
            Write(title),
            FadeIn(harm_label),
            run_time=anim_time_2,
        )
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_Fourier_se_1f06ada7f3/step_02.mp3")  # [auto-injected] duration=7.20s
        _audio_dur_2 = 7.20  # [audio-sync] actual TTS duration
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.500)
        formula = MathTex(
            r"f(x)=\frac{4}{\pi}\sum_{k=1}^{\infty}\frac{\sin((2k-1)x)}{2k-1}",
            color=WHITE,
        ).move_to(np.array([0, 2.2, 0]))
        registry["formula"] = formula

        self.set_subtitle("傅立葉的想法：用正弦波組合出這個形狀，只取奇次諧波並乘上 4/π。", run_time=_audio_dur_2)
        anim_time_3 = 2.500 * _scale_3
        self.play(Write(formula), run_time=anim_time_3)
        self.play(Circumscribe(formula, color=YELLOW))
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_Fourier_se_1f06ada7f3/step_03.mp3")  # [auto-injected] duration=6.72s
        _audio_dur_3 = 6.72  # [audio-sync] actual TTS duration
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.000)
        harm1 = axes.plot(lambda x: (4 / PI) * np.sin(x), color=RED, stroke_width=4)
        registry["harm1"] = harm1

        new_label_4 = Text("n = 1", color=GREY_B, font_size=28).move_to(
            np.array([0, -2.2, 0])
        )
        self.set_subtitle("第一個諧波，4/π sin x，是一條平滑的單峰曲線，粗略地描繪出方波。", run_time=_audio_dur_3)
        anim_time_4 = 2.000 * _scale_4
        self.play(
            Create(harm1),
            Transform(harm_label, new_label_4),
            run_time=anim_time_4,
        )
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_Fourier_se_1f06ada7f3/step_04.mp3")  # [auto-injected] duration=5.95s
        _audio_dur_4 = 5.95  # [audio-sync] actual TTS duration
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        sum3 = axes.plot(
            lambda x: (4 / PI) * (np.sin(x) + np.sin(3 * x) / 3),
            color=ORANGE,
            stroke_width=4,
        )
        registry["sum3"] = sum3

        new_label_5 = Text("n = 3", color=GREY_B, font_size=28).move_to(
            np.array([0, -2.2, 0])
        )
        self.set_subtitle("加入第三諧波後，頂部被壓平，曲線更貼近方波的邊緣。", run_time=_audio_dur_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(
            harm1.animate.set_opacity(0.35),
            Create(sum3),
            Transform(harm_label, new_label_5),
            run_time=anim_time_5,
        )
        self.play(Indicate(sum3, color=ORANGE))
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_5))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_Fourier_se_1f06ada7f3/step_05.mp3")  # [auto-injected] duration=6.24s
        _audio_dur_5 = 6.24  # [audio-sync] actual TTS duration
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 2.500)
        sum5 = axes.plot(
            lambda x: (4 / PI) * (np.sin(x) + np.sin(3 * x) / 3 + np.sin(5 * x) / 5),
            color=YELLOW,
            stroke_width=4,
        )
        registry["sum5"] = sum5

        sum7 = axes.plot(
            lambda x: (4 / PI)
            * (np.sin(x) + np.sin(3 * x) / 3 + np.sin(5 * x) / 5 + np.sin(7 * x) / 7),
            color=GREEN,
            stroke_width=4,
        )
        registry["sum7"] = sum7

        new_label_6 = Text("n = 7", color=GREY_B, font_size=28).move_to(
            np.array([0, -2.2, 0])
        )
        self.set_subtitle("第五與第七諧波讓邊角更加銳利，緊緊貼合平坦的高原。", run_time=_audio_dur_5)
        anim_time_6 = 2.500 * _scale_6
        self.play(
            sum3.animate.set_opacity(0.35),
            FadeIn(sum5),
            run_time=0.6,
        )
        self.play(
            sum5.animate.set_opacity(0.35),
            Create(sum7),
            Transform(harm_label, new_label_6),
            run_time=anim_time_6 - 0.6,
        )
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 + 0.1)
        self.wait(max(0.1, remaining_6))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_Fourier_se_1f06ada7f3/step_06.mp3")  # [auto-injected] duration=6.67s
        _audio_dur_6 = 6.67  # [audio-sync] actual TTS duration
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 2.500)
        sum9 = axes.plot(
            lambda x: (4 / PI)
            * (
                np.sin(x)
                + np.sin(3 * x) / 3
                + np.sin(5 * x) / 5
                + np.sin(7 * x) / 7
                + np.sin(9 * x) / 9
            ),
            color=TEAL,
            stroke_width=4,
        )
        registry["sum9"] = sum9

        new_label_7 = Text("n = 9", color=GREY_B, font_size=28).move_to(
            np.array([0, -2.2, 0])
        )
        self.set_subtitle("到了九個諧波，逼近已經非常出色，但每個跳變處仍頑強地殘留一個過衝。", run_time=_audio_dur_6)
        anim_time_7 = 2.500 * _scale_7
        self.play(FadeOut(sum5), run_time=0.5)
        self.play(
            sum7.animate.set_opacity(0.35),
            Create(sum9),
            Transform(harm_label, new_label_7),
            run_time=anim_time_7 - 0.5,
        )
        self.play(Indicate(sum9, color=TEAL))
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_7))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_Fourier_se_1f06ada7f3/step_07.mp3")  # [auto-injected] duration=6.67s
        _audio_dur_7 = 6.67  # [audio-sync] actual TTS duration
        # Step 8
        _scale_8 = max(1.0, (_audio_dur_7 * 0.7) / 2.000)
        gibbs_marker = Dot(
            point=axes.c2p(PI, 1.1), color=WHITE, radius=0.07
        )
        registry["gibbs_marker"] = gibbs_marker

        self.set_subtitle("這個在不連續點附近持續存在的尖峰就是吉布斯現象，它永遠不會完全消失。", run_time=_audio_dur_7)
        anim_time_8 = 2.000 * _scale_8
        self.play(FadeIn(gibbs_marker), run_time=anim_time_8)
        self.play(Circumscribe(gibbs_marker, color=WHITE))
        remaining_8 = max(0.1, _audio_dur_7 - anim_time_8 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_8))