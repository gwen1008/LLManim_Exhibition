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
        # [VISUAL REASONING]
        # Goal: Show how odd-harmonic rotating phasors (epicycles) chained tip-to-tail
        #       synthesize a square wave traced on the right-side axes.
        # Layout: phasor chain centered at (-4,0), wave axes near (2.2,0),
        #         a dashed tracer line links the moving phasor tip to the pen on the axes.
        # Technique: ValueTracker(t) drives rotation; always_redraw rebuilds phasors,
        #            circles, tip dot, pen, and tracer each frame; TracedPath draws the wave.

        center = np.array([-4.0, 0.0, 0.0])
        harmonics = [(1, 1.27, BLUE), (3, 0.42, GREEN), (5, 0.25, YELLOW)]

        t = ValueTracker(0.0)
        n_active = ValueTracker(0)

        def get_points():
            n = int(round(n_active.get_value()))
            pts = [center.copy()]
            p = center.copy()
            tv = t.get_value()
            for i in range(n):
                k, r, _c = harmonics[i]
                p = p + r * np.array([np.cos(k * tv), np.sin(k * tv), 0.0])
                pts.append(p.copy())
            return pts

        title = Text(
            "Fourier Series: Phasors Building a Square Wave",
            color=WHITE,
            font_size=34,
        ).to_edge(UP)

        formula = MathTex(
            r"f(t)=\frac{4}{\pi}\left(\sin t+\tfrac{1}{3}\sin 3t+\tfrac{1}{5}\sin 5t+\cdots\right)",
            color=WHITE,
        ).scale(0.8)
        formula.move_to([0, -2.5, 0])

        wave_axes = Axes(
            x_range=[0, 6, 1],
            y_range=[-1.6, 1.6, 1],
            x_length=6,
            y_length=3.2,
            axis_config={"color": GREY},
        ).move_to([2.2, 0, 0])

        def make_circle(i):
            def f():
                n = int(round(n_active.get_value()))
                if i >= n:
                    return VGroup()
                pts = get_points()
                k, r, c = harmonics[i]
                return Circle(radius=r, color=c, stroke_width=2).move_to(pts[i])
            return always_redraw(f)

        def make_vec(i):
            def f():
                n = int(round(n_active.get_value()))
                if i >= n:
                    return VGroup()
                pts = get_points()
                c = harmonics[i][2]
                return Arrow(
                    pts[i],
                    pts[i + 1],
                    buff=0,
                    color=c,
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.25,
                )
            return always_redraw(f)

        circle1 = make_circle(0)
        circle2 = make_circle(1)
        circle3 = make_circle(2)
        vec1 = make_vec(0)
        vec2 = make_vec(1)
        vec3 = make_vec(2)

        tip_dot = always_redraw(lambda: Dot(get_points()[-1], color=RED, radius=0.07))
        wave_dot = always_redraw(
            lambda: Dot(
                wave_axes.c2p(t.get_value(), get_points()[-1][1]),
                color=RED,
                radius=0.05,
            )
        )
        tracer_line = always_redraw(
            lambda: DashedLine(
                get_points()[-1],
                wave_axes.c2p(t.get_value(), get_points()[-1][1]),
                color=RED,
                stroke_width=2,
            )
        )

        def indicate(mob, color):
            mob.suspend_updating()
            self.play(Indicate(mob, color=color))
            mob.resume_updating()

        trace = None

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N04_dft_phasors_1780054220/media/audio/Using_rotating_phaso_250974fb82/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 6.17  # [audio-sync]
        # Step 1
        self.set_subtitle("方波可以由一系列奇次諧波的正弦波疊加而成，振幅依序縮小。", run_time=_audio_dur_0)
        self.play(Write(title), run_time=1.0)
        self.play(Write(formula), run_time=2.0)
        self.play(Circumscribe(formula, color=YELLOW), run_time=1.5)
        remaining_1 = max(0.1, _audio_dur_0 - 4.5 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N04_dft_phasors_1780054220/media/audio/Using_rotating_phaso_250974fb82/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 6.62  # [audio-sync]
        # Step 2
        self.set_subtitle("第一個旋轉相量以基頻轉動，它的高度描繪出一條單純的正弦波。", run_time=_audio_dur_1)
        n_active.set_value(1)
        t.set_value(0)
        self.add(tip_dot, wave_dot)
        self.play(Create(wave_axes), run_time=1.0)
        self.play(Create(circle1), Create(vec1), run_time=1.0)
        self.add(tracer_line)
        indicate(vec1, BLUE)
        trace = TracedPath(wave_dot.get_center, stroke_color=BLUE, stroke_width=3)
        self.add(trace)
        self.play(t.animate.set_value(6), run_time=3.0, rate_func=linear)
        remaining_2 = max(0.1, _audio_dur_1 - 6.0 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N04_dft_phasors_1780054220/media/audio/Using_rotating_phaso_250974fb82/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 5.59  # [audio-sync]
        # Step 3
        self.set_subtitle("我們在第一個相量的頂端接上第二個相量，轉速是它的三倍。", run_time=_audio_dur_2)
        self.remove(trace)
        n_active.set_value(2)
        t.set_value(0)
        self.play(Create(circle2), Create(vec2), run_time=1.0)
        indicate(vec2, GREEN)
        trace = TracedPath(wave_dot.get_center, stroke_color=GREEN, stroke_width=3)
        self.add(trace)
        self.play(t.animate.set_value(6), run_time=3.0, rate_func=linear)
        remaining_3 = max(0.1, _audio_dur_2 - 5.0 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N04_dft_phasors_1780054220/media/audio/Using_rotating_phaso_250974fb82/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.77  # [audio-sync]
        # Step 4
        self.set_subtitle("加入第五諧波的相量讓轉角更加銳利，使軌跡更接近真正的方波。", run_time=_audio_dur_3)
        self.remove(trace)
        n_active.set_value(3)
        t.set_value(0)
        self.play(Create(circle3), Create(vec3), run_time=1.0)
        indicate(vec3, YELLOW)
        trace = TracedPath(wave_dot.get_center, stroke_color=YELLOW, stroke_width=3)
        self.add(trace)
        self.play(t.animate.set_value(6), run_time=3.5, rate_func=linear)
        remaining_4 = max(0.1, _audio_dur_3 - 5.5 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N04_dft_phasors_1780054220/media/audio/Using_rotating_phaso_250974fb82/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.72  # [audio-sync]
        # Step 5
        self.set_subtitle("更多的諧波讓邊緣更清晰，揭示旋轉向量如何合成出方波。", run_time=_audio_dur_4)
        self.remove(trace)
        t.set_value(0)
        trace = TracedPath(wave_dot.get_center, stroke_color=RED, stroke_width=3)
        self.add(trace)
        indicate(tip_dot, RED)
        self.play(t.animate.set_value(6), run_time=2.5, rate_func=linear)
        self.play(Circumscribe(wave_axes, color=RED), run_time=1.5)
        remaining_5 = max(0.1, _audio_dur_4 - 5.0 + 0.1)
        self.wait(remaining_5)