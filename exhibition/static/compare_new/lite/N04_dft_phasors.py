from manim import *
import numpy as np

# [VISUAL REASONING]
# 1. Goal: Show how rotating phasors (odd harmonics) synthesize a square wave.
# 2. Layout: Left pane = chained rotating phasors around a fixed origin;
#    Right pane = Axes tracing the partial Fourier sum vs the ideal square wave.
# 3. Mechanism: A single ValueTracker 't' (phase angle) drives every phasor via
#    always_redraw, and the trace is plotted as the partial sum up to current t.
#    Each step adds one harmonic (k=1,2,3) and re-sweeps a full period.

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
        origin = np.array([-3.5, 0.3, 0])
        amps = [4 / PI, 4 / (3 * PI), 4 / (5 * PI)]
        freqs = [1, 3, 5]
        pcolors = ["#f2c14e", "#e07a5f", "#81b29a"]
        psw = [5, 4, 3]

        t = ValueTracker(0)
        state = {"n": 1}

        def chain_point(theta, n):
            p = origin.copy()
            for k in range(n):
                ang = freqs[k] * theta
                p = p + amps[k] * np.array([np.cos(ang), np.sin(ang), 0])
            return p

        def partial_sum(x, n):
            return sum(amps[k] * np.sin(freqs[k] * x) for k in range(n))

        # Header title
        title_main = Text("Fourier Series: Phasors Build a Square Wave", font_size=34).to_edge(UP)

        # Right pane axes
        wave_axes = Axes(
            x_range=[0, 6.28, 1.57],
            y_range=[-1.6, 1.6, 0.8],
            x_length=5.2,
            y_length=3.0,
        ).move_to([2.8, 0.3, 0])

        # Guide circle for dominant phasor
        phasor_circle_guide = Circle(
            radius=1.27, color="#3b6ea5", stroke_width=1.5, stroke_opacity=0.4
        ).move_to(origin)

        # Phasors via always_redraw
        def make_phasor(k):
            return always_redraw(
                lambda: Arrow(
                    chain_point(t.get_value(), k),
                    chain_point(t.get_value(), k + 1),
                    buff=0,
                    color=pcolors[k],
                    stroke_width=psw[k],
                    max_tip_length_to_length_ratio=0.3,
                )
            )

        phasor_vector_1 = make_phasor(0)
        phasor_vector_2 = make_phasor(1)
        phasor_vector_3 = make_phasor(2)

        endpoint_dot = always_redraw(
            lambda: Dot(chain_point(t.get_value(), state["n"]), radius=0.07, color="#ffffff")
        )

        wave_trace = always_redraw(
            lambda: wave_axes.plot(
                lambda x: partial_sum(x, state["n"]),
                x_range=[0, max(0.05, t.get_value()), 0.02],
                color="#f2c14e",
                stroke_width=4,
            )
        )

        link_dashed = always_redraw(
            lambda: DashedLine(
                chain_point(t.get_value(), state["n"]),
                wave_axes.c2p(t.get_value(), partial_sum(t.get_value(), state["n"])),
                color="#888888",
                stroke_width=2,
            )
        )

        target_square_wave = wave_axes.plot(
            lambda x: 1.0 if np.sin(x) >= 0 else -1.0,
            x_range=[0, 6.28, 0.01],
            color="#cccccc",
            stroke_width=2,
            use_smoothing=False,
        ).set_stroke(opacity=0.55)

        formula_label = MathTex(
            r"f(t)=\frac{4}{\pi}\sum_{k=1}^{\infty}\frac{\sin((2k-1)t)}{2k-1}",
            font_size=30,
        ).move_to([0, -2.0, 0])

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N04_dft_phasors_1780054523/media/audio/Using_rotating_phaso_250974fb82/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 10.85  # [audio-sync]
        # Step 1
        self.set_subtitle("我們從一個以基頻旋轉的向量，也就是相量開始；它的垂直投影單獨描出一條純正弦波。", run_time=_audio_dur_0)
        state["n"] = 1
        t.set_value(0)
        self.add(phasor_vector_1, endpoint_dot, wave_trace)
        anim_time_1 = _audio_dur_0
        self.play(
            LaggedStart(
                Write(title_main),
                Create(wave_axes),
                FadeIn(phasor_circle_guide),
                t.animate.set_value(TAU),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N04_dft_phasors_1780054523/media/audio/Using_rotating_phaso_250974fb82/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 10.63  # [audio-sync]
        # Step 2
        self.set_subtitle("現在在第一個相量的尖端接上第二個較小的相量，以三倍的速度旋轉；鏈狀尖端開始把波峰壓平。", run_time=_audio_dur_1)
        state["n"] = 2
        t.set_value(0)
        self.add(phasor_vector_2, link_dashed)
        anim_time_2 = _audio_dur_1
        self.play(
            LaggedStart(
                GrowArrow(Arrow(chain_point(0, 1), chain_point(0, 2), buff=0, color=pcolors[1], stroke_width=psw[1])),
                FadeIn(link_dashed),
                t.animate.set_value(TAU),
                lag_ratio=0.25,
                run_time=anim_time_2,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N04_dft_phasors_1780054523/media/audio/Using_rotating_phaso_250974fb82/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 10.54  # [audio-sync]
        # Step 3
        self.set_subtitle("加入第三個以五倍頻率旋轉的相量，整條向量鏈描繪出更銳利的邊緣，逐漸逼近方波平坦的高原。", run_time=_audio_dur_2)
        state["n"] = 3
        t.set_value(0)
        self.add(phasor_vector_3)
        anim_time_3 = _audio_dur_2
        self.play(
            LaggedStart(
                GrowArrow(Arrow(chain_point(0, 2), chain_point(0, 3), buff=0, color=pcolors[2], stroke_width=psw[2])),
                Indicate(endpoint_dot, color="#ffffff"),
                t.animate.set_value(TAU),
                lag_ratio=0.25,
                run_time=anim_time_3,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N04_dft_phasors_1780054523/media/audio/Using_rotating_phaso_250974fb82/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 9.67  # [audio-sync]
        # Step 4
        self.set_subtitle("疊上理想的方波，可以看到相量之和緊緊貼合它；每多一個諧波都抑制漣漪並讓轉角更方正。", run_time=_audio_dur_3)
        state["n"] = 3
        t.set_value(0)
        anim_time_4 = _audio_dur_3
        self.play(
            LaggedStart(
                Create(target_square_wave),
                t.animate.set_value(TAU),
                Indicate(target_square_wave, color="#f2c14e"),
                lag_ratio=0.25,
                run_time=anim_time_4,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N04_dft_phasors_1780054523/media/audio/Using_rotating_phaso_250974fb82/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 11.16  # [audio-sync]
        # Step 5
        self.set_subtitle("這就是傅立葉合成的核心：無窮多個奇次諧波的旋轉相量相加，正如公式所宣告，精確重建出方波。", run_time=_audio_dur_4)
        state["n"] = 3
        t.set_value(0)
        formula_rect = SurroundingRectangle(formula_label, color="#f2c14e")
        anim_time_5 = _audio_dur_4
        self.play(
            LaggedStart(
                Write(formula_label),
                Create(formula_rect),
                t.animate.set_value(TAU),
                FadeIn(target_square_wave.copy().set_stroke(opacity=0.9)),
                lag_ratio=0.25,
                run_time=anim_time_5,
            )
        )
        self.wait(0.1)