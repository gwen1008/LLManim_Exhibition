from manim import *
import numpy as np

# [VISUAL REASONING]
# Build intuition by tracking one point's orbit under z->z^2+c, then generalize.
# Points whose orbits stay bounded form the Mandelbrot set; divergence speed colors the rest.
# Layout: title at top, formula below, complex plane centered slightly below origin,
# sample orbit traced on plane, then transform into final fractal approximation.

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

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q19_mandelbrot_1779989231/media/audio/Plotting_the_Mandelb_5bf722d504/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 5.50  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 2.000)
        title = Text("The Mandelbrot Set", color=WHITE, font_size=40).to_edge(UP, buff=0.5)
        formula = MathTex(r"z_{n+1} = z_n^2 + c,\quad z_0 = 0", color=YELLOW).next_to(title, DOWN, buff=0.3)
        registry["title"] = title
        registry["formula"] = formula

        self.add(title)
        self.set_subtitle("對於每個複數 c，我們從零開始迭代這個簡單的規則。", run_time=_audio_dur_0)
        anim_time_1 = 2.000 * _scale_1
        self.play(Write(formula), run_time=2.0)
        self.play(Circumscribe(formula, color=YELLOW), run_time=1.0)
        anim_time_1 += 1.0
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q19_mandelbrot_1779989231/media/audio/Plotting_the_Mandelb_5bf722d504/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 4.99  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.000)
        plane = Axes(
            x_range=[-2.2, 1.2, 1],
            y_range=[-1.3, 1.3, 1],
            x_length=6.8,
            y_length=3.6,
            axis_config={"color": GREY},
        ).move_to(ORIGIN + np.array([0, -0.5, 0]))
        registry["plane"] = plane

        c_dot = Dot(point=np.array([-0.84, 0.36, 0]) + np.array([0, -0.5, 0]), color=RED, radius=0.09)
        c_label = MathTex("c = -0.5 + 0.2i", color=RED).next_to(c_dot, UP, buff=0.2)
        registry["c_dot"] = c_dot
        registry["c_label"] = c_label

        self.set_subtitle("我們在複數平面上測試每個點 c，就像這個紅色的樣本點。", run_time=_audio_dur_1)
        anim_time_2 = 2.000 * _scale_2
        self.play(Create(plane), run_time=2.0)
        self.play(FadeIn(c_dot), Write(c_label), run_time=0.8)
        anim_time_2 += 0.8
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q19_mandelbrot_1779989231/media/audio/Plotting_the_Mandelb_5bf722d504/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 6.14  # [audio-sync]
        # Step 3
        offset = np.array([0, -0.5, 0])
        orbit_dot_1 = Dot(point=np.array([-0.84, 0.36, 0]) + offset, color=BLUE, radius=0.07)
        orbit_dot_2 = Dot(point=np.array([-0.42, 0.0, 0]) + offset, color=BLUE, radius=0.07)
        orbit_dot_3 = Dot(point=np.array([-0.55, 0.18, 0]) + offset, color=BLUE, radius=0.07)
        orbit_dot_4 = Dot(point=np.array([-0.48, 0.27, 0]) + offset, color=BLUE, radius=0.07)
        registry["orbit_dot_1"] = orbit_dot_1
        registry["orbit_dot_2"] = orbit_dot_2
        registry["orbit_dot_3"] = orbit_dot_3
        registry["orbit_dot_4"] = orbit_dot_4

        bounded_tag = Text("Bounded: c belongs to the set", color=GREEN, font_size=28).to_edge(DOWN, buff=1.8)
        registry["bounded_tag"] = bounded_tag

        self.set_subtitle("反覆應用這個規則會描繪出軌道；如果保持有界，c 就屬於這個集合。", run_time=_audio_dur_2)
        anim_time_3 = 0.0
        self.play(LaggedStart(
            FadeIn(orbit_dot_1),
            FadeIn(orbit_dot_2),
            FadeIn(orbit_dot_3),
            FadeIn(orbit_dot_4),
            lag_ratio=0.4,
        ), run_time=2.5)
        anim_time_3 += 2.5
        self.play(Write(bounded_tag), run_time=0.8)
        anim_time_3 += 0.8
        self.play(Indicate(orbit_dot_4, color=GREEN), run_time=0.8)
        anim_time_3 += 0.8
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q19_mandelbrot_1779989231/media/audio/Plotting_the_Mandelb_5bf722d504/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 5.98  # [audio-sync]
        # Step 4
        plane_group = VGroup(plane, c_dot, orbit_dot_1, orbit_dot_2, orbit_dot_3, orbit_dot_4)

        fractal_dots = VGroup()
        x_min, x_max = -2.2, 1.2
        y_min, y_max = -1.3, 1.3
        nx, ny = 80, 50
        max_iter = 30
        for i in range(nx):
            for j in range(ny):
                cx = x_min + (x_max - x_min) * i / (nx - 1)
                cy = y_min + (y_max - y_min) * j / (ny - 1)
                zx, zy = 0.0, 0.0
                k = 0
                while k < max_iter and zx * zx + zy * zy < 4.0:
                    zx, zy = zx * zx - zy * zy + cx, 2 * zx * zy + cy
                    k += 1
                if k >= max_iter:
                    color = BLACK
                else:
                    t = k / max_iter
                    if t < 0.33:
                        color = interpolate_color(RED, ORANGE, t / 0.33)
                    elif t < 0.66:
                        color = interpolate_color(ORANGE, YELLOW, (t - 0.33) / 0.33)
                    else:
                        color = interpolate_color(YELLOW, WHITE, (t - 0.66) / 0.34)
                pt = plane.c2p(cx, cy)
                d = Dot(point=pt, color=color, radius=0.045, stroke_width=0).set_fill(color, opacity=1.0)
                fractal_dots.add(d)

        fractal_image = fractal_dots
        registry["fractal_image"] = fractal_image

        self.set_subtitle("其他點則逃向無窮遠，我們用逃逸所需的迭代次數來著色它們。", run_time=_audio_dur_3)
        anim_time_4 = 0.0
        self.play(FadeOut(c_label), FadeOut(bounded_tag), run_time=0.6)
        anim_time_4 += 0.6
        self.play(ReplacementTransform(plane_group, fractal_image), run_time=2.5)
        anim_time_4 += 2.5
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q19_mandelbrot_1779989231/media/audio/Plotting_the_Mandelb_5bf722d504/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.38  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        legend = Text("Black = bounded   Warm colors = fast escape", color=WHITE, font_size=24).next_to(fractal_image, DOWN, buff=0.25)
        registry["legend"] = legend

        self.set_subtitle("黑色區域就是 Mandelbrot 集合；暖色標示出發散最快的點。", run_time=_audio_dur_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(Write(legend), run_time=2.0)
        self.play(Circumscribe(fractal_image, color=WHITE), run_time=1.2)
        anim_time_5 += 1.2
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)