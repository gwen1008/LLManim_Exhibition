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


# [VISUAL REASONING]
# Lorenz attractor traced as a single continuous gradient curve in a ThreeDScene.
# Equations and parameters are pinned as camera-fixed overlays. A red dot marks the
# start near origin; the trajectory grows revealing the double-wing butterfly, then a
# slow camera rotation exposes the full 3D structure of deterministic chaos.

from manim import *
import numpy as np


def lorenz_points():
    sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
    dt = 0.005
    steps = 4000
    scale = 0.12
    z_shift = 25.0 * scale
    x, y, z = 0.1, 0.0, 0.0
    pts = []
    for _ in range(steps):
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        x += dx * dt
        y += dy * dt
        z += dz * dt
        pts.append([x * scale, y * scale, z * scale - z_shift])
    return [np.array(p, dtype=float) for p in pts]


class GeneratedScene(ThreeDScene):
    def construct(self):
        self._instrumentor = SceneInstrumentor(self, log_path='/Users/liaozhenting/Desktop/LLManim_Agent/scene_state_log.json')
        self._sm = SubtitleManager(self)
        self.set_subtitle = self._sm.show
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        axes3d = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"color": GREY},
        )

        title = Text("勞侖次吸子", color=WHITE, font_size=40)
        title.to_edge(UP, buff=0.4)

        eq_x = MathTex(r"\dot{x} = \sigma(y - x)", color=BLUE)
        eq_x.to_corner(UL, buff=0.6)

        eq_y = MathTex(r"\dot{y} = x(\rho - z) - y", color=TEAL)
        eq_y.next_to(eq_x, DOWN, buff=0.3)

        eq_z = MathTex(r"\dot{z} = xy - \beta z", color=YELLOW)
        eq_z.next_to(eq_y, DOWN, buff=0.3)

        params = MathTex(r"\sigma=10,\ \rho=28,\ \beta=\tfrac{8}{3}", color=WHITE, font_size=32)
        params.next_to(eq_z, DOWN, buff=0.4)

        raw_points = lorenz_points()

        lorenz_curve = VMobject()
        lorenz_curve.set_points_smoothly(raw_points)
        lorenz_curve.set_color_by_gradient(BLUE, TEAL, YELLOW)
        lorenz_curve.set_stroke(width=2)

        start_dot = Dot3D(point=raw_points[0], color=RED, radius=0.08)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q16_lorenz_1781378425/media/audio/Plot_the_trajectory__4c48905cfe/step_00_ff1d1aa8.mp3")  # [auto-injected]
        _audio_dur_0 = 6.48  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 2.000))
        self.add_fixed_in_frame_mobjects(title, eq_x, eq_y, eq_z)
        anim_time_1 = 2.000 * _scale_1
        self.play(Write(eq_x), run_time=anim_time_1)
        self.play(
            LaggedStart(Write(eq_y), Write(eq_z), Write(title), lag_ratio=0.3),
            run_time=(1.5) * _scale_1,
        )
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - (anim_time_1 + 1.5) + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q16_lorenz_1781378425/media/audio/Plot_the_trajectory__4c48905cfe/step_01_9d05911d.mp3")  # [auto-injected]
        _audio_dur_1 = 8.57  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 2.000))
        self.add_fixed_in_frame_mobjects(params)
        anim_time_2 = 2.000 * _scale_2
        self.play(
            Write(params),
            Create(axes3d),
            run_time=anim_time_2,
        )
        self.wait(0.5)
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - (anim_time_2 + 1.0) + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q16_lorenz_1781378425/media/audio/Plot_the_trajectory__4c48905cfe/step_02_37794b6d.mp3")  # [auto-injected]
        _audio_dur_2 = 4.90  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 1.500))
        anim_time_3 = 1.500 * _scale_3
        self.play(Create(start_dot), run_time=anim_time_3)
        self.play(Indicate(start_dot, color=RED), run_time=(1.0) * _scale_3)
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - (anim_time_3 + 1.0) + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q16_lorenz_1781378425/media/audio/Plot_the_trajectory__4c48905cfe/step_03_654725fd.mp3")  # [auto-injected]
        _audio_dur_3 = 7.10  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 8.000))
        anim_time_4 = 8.000 * _scale_4
        self.play(Create(lorenz_curve, rate_func=linear), run_time=anim_time_4)
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q16_lorenz_1781378425/media/audio/Plot_the_trajectory__4c48905cfe/step_04_7d604d2f.mp3")  # [auto-injected]
        _audio_dur_4 = 6.43  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 5.000))
        self.play(FadeOut(start_dot), run_time=(0.5) * _scale_5)
        anim_time_5 = 5.000 * _scale_5
        self.move_camera(theta=-45 * DEGREES + 2 * PI, run_time=anim_time_5, rate_func=linear)
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - (anim_time_5 + 0.5) + 0.1))
        self.wait(remaining_5)