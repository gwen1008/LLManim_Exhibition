# [VISUAL REASONING]
# Anchor iteration formula in a visible orbit on the complex plane, then generalize
# to the full colored Mandelbrot set so learners connect escape-speed to fractal coloring.

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
        # ---- Build objects from blueprint ----
        title = Text("The Mandelbrot Set", font_size=38, color="#FFD700").move_to([0, 3.0, 0])

        plane_axes = Axes(
            x_range=[-2.2, 1.2, 1],
            y_range=[-1.4, 1.4, 1],
            x_length=5.5,
            y_length=4.4,
            tips=False,
        ).move_to([-3.3, -0.2, 0])

        re_label = MathTex(r"Re(c)", font_size=24).next_to(plane_axes, DOWN, buff=0.15)
        im_label = MathTex(r"Im(c)", font_size=24).next_to(plane_axes, LEFT, buff=0.15)

        formula_main = MathTex(r"z_{n+1} = z_n^2 + c", font_size=44, color="#00E5FF").move_to([3.2, 1.6, 0])
        init_cond = MathTex(r"z_0 = 0,\quad c \in \mathbb{C}", font_size=30).move_to([3.2, 0.8, 0])

        # Sample point c = -0.5 + 0.5i mapped via axes
        c_val = complex(-0.5, 0.5)
        c_point = plane_axes.c2p(c_val.real, c_val.imag)
        c_dot = Dot(point=c_point, radius=0.09, color="#FF4081")
        c_label = MathTex("c = -0.5 + 0.5i", font_size=26, color="#FF4081").next_to(c_dot, UP, buff=0.15)

        # Orbit computation: z_{n+1} = z_n^2 + c
        orbit_pts = []
        z = complex(0, 0)
        for _ in range(9):
            orbit_pts.append(z)
            z = z * z + c_val
            if abs(z) > 4:
                break

        orbit_dots = VGroup(*[
            Dot(point=plane_axes.c2p(p.real, p.imag), radius=0.06, color="#FFFFFF")
            for p in orbit_pts
        ])
        orbit_lines = VGroup(*[
            Line(
                plane_axes.c2p(orbit_pts[i].real, orbit_pts[i].imag),
                plane_axes.c2p(orbit_pts[i + 1].real, orbit_pts[i + 1].imag),
                stroke_width=2,
                color="#FFEB3B",
            )
            for i in range(len(orbit_pts) - 1)
        ])
        orbit_group = VGroup(orbit_lines, orbit_dots)

        # Escape circle |z|=2 on axes — radius scaled to axes units
        unit_x = np.linalg.norm(plane_axes.c2p(1, 0) - plane_axes.c2p(0, 0))
        escape_circle = Circle(radius=2 * unit_x, color="#FF9800", stroke_width=2.5).move_to(plane_axes.c2p(0, 0))

        escape_rule = MathTex(r"|z_n| > 2 \;\Rightarrow\; diverges", font_size=30, color="#FF9800").move_to([3.2, 0.0, 0])
        color_rule = Text("Color = iterations until escape", font_size=24, color="#B0E57C").move_to([3.2, -0.8, 0])

        # Legend bar with gradient
        legend_bar = Rectangle(width=3.0, height=0.35, stroke_width=1.5).move_to([3.2, -1.5, 0])
        legend_bar.set_fill(color=[BLUE, GREEN, YELLOW, ORANGE, RED], opacity=1.0)
        legend_fast = Text("fast escape", font_size=18).next_to(legend_bar, LEFT, buff=0.15)
        legend_slow = Text("bounded", font_size=18).next_to(legend_bar, RIGHT, buff=0.15)

        # Mandelbrot field — sample grid
        def mandel_iters(c, max_iter=40):
            z = 0 + 0j
            for i in range(max_iter):
                z = z * z + c
                if abs(z) > 2:
                    return i
            return -1

        def color_from_iter(i, max_iter=40):
            if i < 0:
                return "#000000"
            t = i / max_iter
            cmap = [BLUE_E, BLUE, TEAL, GREEN, YELLOW, ORANGE, RED]
            idx = min(int(t * (len(cmap) - 1)), len(cmap) - 2)
            frac = t * (len(cmap) - 1) - idx
            return interpolate_color(cmap[idx], cmap[idx + 1], frac)

        nx, ny = 110, 70
        x_vals = np.linspace(-2.2, 1.2, nx)
        y_vals = np.linspace(-1.4, 1.4, ny)
        cell_w = (plane_axes.c2p(x_vals[1], 0) - plane_axes.c2p(x_vals[0], 0))[0]
        cell_h = abs((plane_axes.c2p(0, y_vals[1]) - plane_axes.c2p(0, y_vals[0]))[1])
        squares = []
        # Order left-to-right for sweep
        for xi, xv in enumerate(x_vals):
            for yi, yv in enumerate(y_vals):
                it = mandel_iters(complex(xv, yv))
                col = color_from_iter(it)
                sq = Square(side_length=max(cell_w, cell_h) * 1.05, stroke_width=0)
                sq.set_fill(col, opacity=1.0)
                sq.move_to(plane_axes.c2p(xv, yv))
                squares.append(sq)
        mandelbrot_field = VGroup(*squares)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q19_mandelbrot_1779993420/media/audio/Plotting_the_Mandelb_5bf722d504/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 8.28  # [audio-sync]
        # Step 1
        self.set_subtitle("我們探索曼德博集合，從 z 等於零開始，迭代 z 平方加上 c 於複數平面上。", run_time=_audio_dur_0)
        anim_time_1 = _audio_dur_0
        self.play(
            LaggedStart(
                Write(title),
                Create(plane_axes),
                AnimationGroup(Write(re_label), Write(im_label)),
                Write(formula_main),
                Write(init_cond),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q19_mandelbrot_1779993420/media/audio/Plotting_the_Mandelb_5bf722d504/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 10.10  # [audio-sync]
        # Step 2
        self.set_subtitle("選取樣本點 c 等於負二分之一加二分之一 i，追蹤軌道 z₀、z₁、z₂ 觀察其走向。", run_time=_audio_dur_1)
        anim_time_2 = _audio_dur_1
        self.play(
            LaggedStart(
                AnimationGroup(FadeIn(c_dot), Write(c_label)),
                Create(orbit_lines),
                LaggedStart(*[FadeIn(d, scale=0.5) for d in orbit_dots], lag_ratio=0.3),
                Indicate(orbit_dots[-1], color=YELLOW, scale_factor=1.6),
                lag_ratio=0.25,
                run_time=anim_time_2,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q19_mandelbrot_1779993420/media/audio/Plotting_the_Mandelb_5bf722d504/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 8.90  # [audio-sync]
        # Step 3
        self.set_subtitle("若軌道的模長超過二，序列就會發散到無窮；否則點 c 屬於曼德博集合。", run_time=_audio_dur_2)
        anim_time_3 = _audio_dur_2
        self.play(
            LaggedStart(
                Create(escape_circle),
                Write(escape_rule),
                Indicate(orbit_dots[-1], color="#FF9800", scale_factor=1.5),
                Write(color_rule),
                lag_ratio=0.25,
                run_time=anim_time_3,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q19_mandelbrot_1779993420/media/audio/Plotting_the_Mandelb_5bf722d504/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 8.30  # [audio-sync]
        # Step 4
        self.set_subtitle("對每一點重複此測試並以逃逸速度上色，便能揭示出標誌性的曼德博碎形。", run_time=_audio_dur_3)
        anim_time_4 = _audio_dur_3
        self.play(
            LaggedStart(
                AnimationGroup(
                    FadeOut(c_dot),
                    FadeOut(c_label),
                    FadeOut(orbit_group),
                    FadeOut(escape_circle),
                ),
                LaggedStart(*[FadeIn(sq) for sq in squares], lag_ratio=0.002),
                AnimationGroup(Create(legend_bar), Write(legend_fast), Write(legend_slow)),
                lag_ratio=0.2,
                run_time=anim_time_4,
            )
        )
        self.wait(0.1)