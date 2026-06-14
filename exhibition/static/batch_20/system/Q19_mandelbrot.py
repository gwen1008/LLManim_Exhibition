from manim import *
import numpy as np

# [VISUAL REASONING]
# The scene teaches the Mandelbrot test by first grounding the iteration z_{n+1}=z_n^2+c
# on a single point's orbit (bounded vs escaping), then generalizing to every point in the
# complex plane and mapping escape-speed to color, revealing the full fractal.
# Layout: NumberPlane is the central stage (shifted slightly down), the title sits in the
# top banner, and the iteration formula rests just beneath it. Orbit dots, the escape arrow,
# the final escape-time ImageMobject and a color reference bar are all rendered relative to
# the plane to keep everything inside y in [-2.0, 2.3] and clear of the subtitle band.

class SubtitleManager:
    """Auto-injected by RefiningLoop.pre_render_patch. Non-blocking subtitle (instant add/remove) —
    runs in parallel with animations and never stalls the main timeline.
    Does NOT use add_updater opacity tweening (broken on manim CE 0.19: VGroup.set_opacity(0)
    on a Text cannot be reversed inside an updater → subtitle stays invisible)."""
    MAX_WIDTH = 12.5
    Y_POSITION = 3.2 * DOWN

    def __init__(self, scene, font_size=28):
        self.scene = scene
        self.font_size = font_size
        self._current = None

    def show(self, text_str, run_time=1.0):
        # 瞬間顯示，不呼叫 scene.play/scene.wait → 不消耗時間軸（非阻塞）。
        # opacity 維持預設=1（絕不 set_opacity(0)），確保字幕一定可見。
        s = str(text_str).strip()
        if not s:
            return
        text_mob = Text(s, font_size=self.font_size, color=WHITE, weight="BOLD")
        bg = BackgroundRectangle(text_mob, color=BLACK, fill_opacity=0.75, buff=0.15)
        new_mob = VGroup(bg, text_mob).move_to(self.Y_POSITION)
        if new_mob.width > self.MAX_WIDTH:
            new_mob.scale_to_fit_width(self.MAX_WIDTH)
        if self._current is not None:
            self.scene.remove(self._current)
        self.scene.add(new_mob)
        self._current = new_mob

    def clear(self, run_time=0.0):
        if self._current is not None:
            self.scene.remove(self._current)
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

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q19_mandelbrot_1781379031/media/audio/Plot_the_Mandelbrot__f6982e2b18/step_00_030ac40b.mp3")  # [auto-injected]
        _audio_dur_0 = 6.24  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 2.000))
        title = Text("The Mandelbrot Set", color=WHITE, font_size=38)
        title.to_edge(UP, buff=0.4)
        registry["title"] = title

        plane = NumberPlane(
            x_range=[-2.5, 1, 0.5],
            y_range=[-1.25, 1.25, 0.5],
            background_line_style={"stroke_color": GREY, "stroke_opacity": 0.4},
        )
        plane.move_to(ORIGIN + np.array([0, -0.4, 0]))
        registry["plane"] = plane

        anim_time_1 = 2.000 * _scale_1
        self.play(Write(title), Create(plane), run_time=anim_time_1)
        self.set_subtitle("我們在複數平面上工作，每個點都代表一個候選值 c。", run_time=_audio_dur_0)
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - anim_time_1 + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q19_mandelbrot_1781379031/media/audio/Plot_the_Mandelbrot__f6982e2b18/step_01_cceff682.mp3")  # [auto-injected]
        _audio_dur_1 = 6.31  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 1.800))
        formula = MathTex(r"z_{n+1} = z_n^2 + c", color=YELLOW)
        formula.next_to(title, DOWN, buff=0.25)
        registry["formula"] = formula

        anim_time_2 = 1.800 * _scale_2
        self.play(Write(formula), run_time=anim_time_2)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        self.set_subtitle("對每個 c，我們重複套用這條規則：把 z 平方再加上 c。", run_time=_audio_dur_1)
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 - 1.0 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q19_mandelbrot_1781379031/media/audio/Plot_the_Mandelbrot__f6982e2b18/step_02_30b3efe9.mp3")  # [auto-injected]
        _audio_dur_2 = 6.62  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 2.000))
        c_dot_bounded = Dot(
            point=plane.c2p(-0.4, 0.1), color=GREEN, radius=0.09
        )
        registry["c_dot_bounded"] = c_dot_bounded

        c_label = MathTex(r"c = -0.4 + 0.1i", color=GREEN, font_size=30)
        c_label.next_to(c_dot_bounded, UP, buff=0.2)
        registry["c_label"] = c_label

        orbit_bounded = Dot(
            point=plane.c2p(-0.55, 0.2), color=TEAL, radius=0.06
        )
        registry["orbit_bounded"] = orbit_bounded

        orbit_pts = [
            plane.c2p(-0.4, 0.1),
            plane.c2p(-0.55, 0.2),
            plane.c2p(-0.32, -0.05),
            plane.c2p(-0.5, 0.15),
        ]
        orbit_dots = VGroup(
            *[Dot(point=p, color=TEAL, radius=0.05) for p in orbit_pts[1:]]
        )
        orbit_lines = VGroup(
            *[
                Line(orbit_pts[i], orbit_pts[i + 1], color=TEAL, stroke_width=2)
                for i in range(len(orbit_pts) - 1)
            ]
        )

        anim_time_3 = 2.000 * _scale_3
        self.play(
            FadeIn(c_dot_bounded),
            Write(c_label),
            Create(orbit_bounded),
            run_time=anim_time_3 * 0.5,
        )
        self.play(
            LaggedStart(
                *[Create(m) for m in [*orbit_lines, *orbit_dots]],
                lag_ratio=0.2,
            ),
            run_time=anim_time_3 * 0.5,
        )
        self.play(Indicate(c_dot_bounded, color=GREEN))
        self.set_subtitle("這個 c 的軌道始終被困在原點附近，所以 c 屬於這個集合。", run_time=_audio_dur_2)
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 - 1.0 + 0.1))
        self.wait(remaining_3)

        bounded_group = VGroup(
            c_dot_bounded, c_label, orbit_bounded, orbit_dots, orbit_lines
        )

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q19_mandelbrot_1781379031/media/audio/Plot_the_Mandelbrot__f6982e2b18/step_03_d668aa65.mp3")  # [auto-injected]
        _audio_dur_3 = 6.82  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 2.000))
        self.play(FadeOut(bounded_group), run_time=(0.6)*_scale_4)

        c_dot_escape = Dot(
            point=plane.c2p(0.5, 0.6), color=RED, radius=0.09
        )
        registry["c_dot_escape"] = c_dot_escape

        escape_arrow = Arrow(
            start=plane.c2p(0.5, 0.6),
            end=plane.c2p(2.2, 1.7),
            color=RED,
            buff=0.05,
        )
        registry["escape_arrow"] = escape_arrow

        escape_label = Text("diverges to infinity", color=RED, font_size=26)
        escape_label.next_to(escape_arrow, UP, buff=0.15)
        registry["escape_label"] = escape_label

        anim_time_4 = 2.000 * _scale_4
        self.play(FadeIn(c_dot_escape), run_time=(0.5)*_scale_4)
        self.play(Indicate(c_dot_escape, color=RED))
        self.play(GrowArrow(escape_arrow), run_time=anim_time_4 * 0.6)
        self.play(FadeIn(escape_label), run_time=anim_time_4 * 0.4)
        self.set_subtitle("另一個 c 越過半徑二，飛奔向無窮大，因此它落在集合之外。", run_time=_audio_dur_3)
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 - 1.6 + 0.1))
        self.wait(remaining_4)

        escape_group = VGroup(c_dot_escape, escape_arrow, escape_label)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q19_mandelbrot_1781379031/media/audio/Plot_the_Mandelbrot__f6982e2b18/step_04_e74d1694.mp3")  # [auto-injected]
        _audio_dur_4 = 6.14  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 2.500))
        self.play(FadeOut(escape_group), run_time=(0.6)*_scale_5)

        px_w, px_h = 600, 480
        x_min, x_max = -2.5, 1.0
        y_min, y_max = -1.25, 1.25
        max_iter = 50

        xs = np.linspace(x_min, x_max, px_w)
        ys = np.linspace(y_max, y_min, px_h)
        C = xs[np.newaxis, :] + 1j * ys[:, np.newaxis]
        Z = np.zeros_like(C)
        escape_count = np.zeros(C.shape, dtype=float)
        mask = np.ones(C.shape, dtype=bool)

        for i in range(max_iter):
            Z[mask] = Z[mask] * Z[mask] + C[mask]
            escaped = np.abs(Z) > 2.0
            newly = escaped & mask
            escape_count[newly] = i
            mask &= ~escaped

        escape_count[mask] = max_iter
        norm = escape_count / max_iter

        t = norm
        r = np.clip(9 * (1 - t) * t * t * t, 0, 1)
        g = np.clip(15 * (1 - t) * (1 - t) * t * t, 0, 1)
        b = np.clip(8.5 * (1 - t) * (1 - t) * (1 - t) * t, 0, 1)
        inside = norm >= 1.0
        r[inside] = 0.0
        g[inside] = 0.0
        b[inside] = 0.0

        rgb = np.stack([r, g, b], axis=-1)
        rgb_img = (rgb * 255).astype(np.uint8)

        mandelbrot_image = ImageMobject(rgb_img)
        mandelbrot_image.move_to(plane.get_center())
        mandelbrot_image.stretch_to_fit_width(plane.get_width())
        mandelbrot_image.stretch_to_fit_height(plane.get_height())
        registry["mandelbrot_image"] = mandelbrot_image

        colorbar = Rectangle(width=0.4, height=3.0, color=WHITE, fill_opacity=0.0)
        colorbar.to_edge(RIGHT, buff=0.4)
        bar_grad = Rectangle(
            width=0.4, height=3.0, stroke_width=0
        ).set_fill(opacity=1.0)
        bar_grad.set_color([BLACK, RED, YELLOW, WHITE])
        bar_grad.move_to(colorbar.get_center())
        registry["colorbar"] = colorbar

        colorbar_label = Text("escape speed", color=WHITE, font_size=24)
        colorbar_label.next_to(colorbar, UP, buff=0.2)
        registry["colorbar_label"] = colorbar_label

        anim_time_5 = 2.500 * _scale_5
        self.play(FadeIn(mandelbrot_image), run_time=anim_time_5)
        self.play(
            FadeIn(bar_grad),
            Create(colorbar),
            FadeIn(colorbar_label),
            run_time=(0.8)*_scale_5,
        )
        self.play(Circumscribe(colorbar, color=WHITE))
        self.set_subtitle("依逃逸速度為每個點上色，就揭示出完整的曼德博碎形。", run_time=_audio_dur_4)
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - anim_time_5 - 1.8 + 0.1))
        self.wait(remaining_5)