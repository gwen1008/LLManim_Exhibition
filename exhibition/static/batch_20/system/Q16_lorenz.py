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


# [VISUAL REASONING]
# 3D scene showing the Lorenz attractor. Title appears top, equations + params fixed
# in upper-left (fixed_in_frame), 3D axes centered, then numerically integrated
# trajectory traced while camera ambient-rotates to reveal the butterfly.

from manim import *
import numpy as np

class GeneratedScene(ThreeDScene):
    def set_subtitle(self, text, **kwargs):
        pass  # Overridden by system SubtitleManager

    def construct(self):
        self._instrumentor = SceneInstrumentor(self, log_path='/Users/liaozhenting/Desktop/LLManim_Agent/scene_state_log.json')
        # Camera setup
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        registry = {}

        # Build objects from blueprint
        title = Text("The Lorenz Attractor", color=WHITE, font_size=38).to_edge(UP, buff=0.4)
        registry["title"] = title

        axes_3d = ThreeDAxes(
            x_range=[-30, 30, 10],
            y_range=[-30, 30, 10],
            z_range=[0, 55, 10],
            x_length=5,
            y_length=5,
            z_length=4,
        ).move_to(ORIGIN)
        registry["axes_3d"] = axes_3d

        _eq1 = MathTex(r"\dot{x} = \sigma(y-x)", color=WHITE)
        _eq2 = MathTex(r"\dot{y} = x(\rho-z)-y", color=WHITE)
        _eq3 = MathTex(r"\dot{z} = xy - \beta z", color=WHITE)
        lorenz_eqs = VGroup(_eq1, _eq2, _eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL, buff=0.5)
        registry["lorenz_eqs"] = lorenz_eqs

        params = MathTex(
            r"\sigma=10,\ \rho=28,\ \beta=\tfrac{8}{3}",
            color=YELLOW,
        ).next_to(lorenz_eqs, DOWN, buff=0.3)
        registry["params"] = params

        # Numerically integrate Lorenz ODEs (RK4)
        sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0

        def lorenz(state):
            x, y, z = state
            return np.array([
                sigma * (y - x),
                x * (rho - z) - y,
                x * y - beta * z,
            ])

        dt = 0.01
        T = 40.0
        n_steps = int(T / dt)
        state = np.array([1.0, 1.0, 1.0])
        points = [state.copy()]
        for _ in range(n_steps):
            k1 = lorenz(state)
            k2 = lorenz(state + 0.5 * dt * k1)
            k3 = lorenz(state + 0.5 * dt * k2)
            k4 = lorenz(state + dt * k3)
            state = state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
            points.append(state.copy())
        points = np.array(points)

        # Subsample for performance
        sampled = points[::8]
        curve_points = [axes_3d.c2p(p[0], p[1], p[2]) for p in sampled]

        trajectory = VMobject(stroke_width=1.5)
        trajectory.set_points_smoothly(curve_points)
        trajectory.set_color_by_gradient(BLUE, RED)
        registry["trajectory"] = trajectory

        start_dot = Dot3D(point=axes_3d.c2p(1, 1, 1), color=YELLOW, radius=0.08)
        registry["start_dot"] = start_dot

        # Fix equations & title in frame so they don't rotate
        self.add_fixed_in_frame_mobjects(title, lorenz_eqs, params)
        title.to_edge(UP, buff=0.4).shift(DOWN * 1.8).shift(DOWN * 1.8).shift(DOWN * 1.8).shift(DOWN * 1.8)
        lorenz_eqs.to_corner(UL, buff=0.5)
        params.next_to(lorenz_eqs, DOWN, buff=0.3)
        self.remove(title, lorenz_eqs, params)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q16_lorenz_1779988635/media/audio/Plot_the_trajectory__5cd5d22b08/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 6.74  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 2.000)
        self.set_subtitle("勞侖次系統用三條耦合的非線性微分方程描述大氣對流。", run_time=_audio_dur_0)
        anim_time_1 = 2.000 * _scale_1
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=anim_time_1)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q16_lorenz_1779988635/media/audio/Plot_the_trajectory__5cd5d22b08/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 5.54  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.500)
        self.set_subtitle("這三條方程式描述 x、y、z 隨時間的演化。", run_time=_audio_dur_1)
        anim_time_2 = 2.500 * _scale_2
        self.add_fixed_in_frame_mobjects(lorenz_eqs)
        self.play(Write(lorenz_eqs), run_time=anim_time_2)
        self.play(Circumscribe(lorenz_eqs, color=YELLOW), run_time=1.0)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 - 1.0 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q16_lorenz_1779988635/media/audio/Plot_the_trajectory__5cd5d22b08/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 8.66  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 1.500)
        self.set_subtitle("採用經典參數 σ=10、ρ=28、β=8/3,系統會產生混沌行為。", run_time=_audio_dur_2)
        anim_time_3 = 1.500 * _scale_3
        self.add_fixed_in_frame_mobjects(params)
        self.play(Write(params), run_time=anim_time_3)
        self.play(Indicate(params, color=YELLOW), run_time=1.0)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 1.0 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q16_lorenz_1779988635/media/audio/Plot_the_trajectory__5cd5d22b08/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.96  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.000)
        self.set_subtitle("從初始點 (1,1,1) 出發,我們對系統做數值積分。", run_time=_audio_dur_3)
        anim_time_4 = 2.000 * _scale_4
        self.play(Create(axes_3d), run_time=anim_time_4)
        self.play(FadeIn(start_dot, scale=0.5), run_time=0.8)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 - 0.8 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q16_lorenz_1779988635/media/audio/Plot_the_trajectory__5cd5d22b08/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.53  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 8.000)
        self.set_subtitle("軌跡永不重複,在兩個吸子之間穿梭,形成標誌性的蝴蝶形狀。", run_time=_audio_dur_4)
        anim_time_5 = 8.000 * _scale_5
        self.begin_ambient_camera_rotation(rate=0.2)
        self.play(Create(trajectory), run_time=anim_time_5, rate_func=linear)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)
        self.stop_ambient_camera_rotation()
        self.wait(3)  # [Auto-injected by Shift-Left Repair]