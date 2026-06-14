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
    Y_POSITION = [0.0, -3.2, 0.0]

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


from manim import *
import numpy as np

# [VISUAL REASONING]
# A true 3D scene best conveys a saddle surface. We build ThreeDAxes and the
# parametric surface z = x^2 - y^2, mark the saddle point, then overlay two
# orthogonal cross-section parabolas to make the "up along x, down along y"
# property visceral, finishing with a camera orbit so viewers grasp the full
# geometry. Title is pinned in-frame so it stays upright during rotation.

class GeneratedScene(ThreeDScene):
    def construct(self):
        self._instrumentor = SceneInstrumentor(self, log_path='/Users/liaozhenting/Desktop/LLManim_Agent/scene_state_log.json')
        self._sm = SubtitleManager(self)
        self.set_subtitle = self._sm.show
        registry = {}

        title = Text("鞍面：z = x^2 - y^2", color=WHITE, font_size=36).to_edge(UP, buff=0.4)
        registry["title"] = title

        axes3d = ThreeDAxes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            z_range=[-4, 4, 2],
            axis_config={"color": GREY},
        )
        registry["axes3d"] = axes3d

        saddle_surface = Surface(
            lambda u, v: axes3d.c2p(u, v, u**2 - v**2),
            u_range=[-2, 2],
            v_range=[-2, 2],
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E],
            resolution=[32, 32],
        )
        registry["saddle_surface"] = saddle_surface

        saddle_point = Dot3D(point=axes3d.c2p(0, 0, 0), color=RED, radius=0.12)
        registry["saddle_point"] = saddle_point

        curve_x = ParametricFunction(
            lambda t: axes3d.c2p(t, 0, t**2),
            t_range=[-2, 2],
            color=YELLOW,
            stroke_width=6,
        )
        registry["curve_x"] = curve_x

        curve_y = ParametricFunction(
            lambda t: axes3d.c2p(0, t, -t**2),
            t_range=[-2, 2],
            color=GREEN,
            stroke_width=6,
        )
        registry["curve_y"] = curve_y

        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.add_fixed_in_frame_mobjects(title)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q17_saddle_3d_1781378825/media/audio/In_3D_space__plot_th_fe11bed353/step_00_547d72f8.mp3")  # [auto-injected]
        _audio_dur_0 = 5.14  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 2.000))
        self.set_subtitle("我們先建立一個三維座標系，用來放置我們的鞍面。", run_time=_audio_dur_0)
        self.play(Write(title), Create(axes3d), run_time=(2.0)*_scale_1)
        anim_time_1 = 2.000 * _scale_1
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - anim_time_1 + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q17_saddle_3d_1781378825/media/audio/In_3D_space__plot_th_fe11bed353/step_01_c1077e72.mp3")  # [auto-injected]
        _audio_dur_1 = 7.13  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 3.000))
        self.set_subtitle("現在我們畫出 z 等於 x 平方減 y 平方，它的圖形形成一個馬鞍的形狀。", run_time=_audio_dur_1)
        self.play(Create(saddle_surface), run_time=(3.0)*_scale_2)
        anim_time_2 = 3.000 * _scale_2
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q17_saddle_3d_1781378825/media/audio/In_3D_space__plot_th_fe11bed353/step_02_33e6f0a1.mp3")  # [auto-injected]
        _audio_dur_2 = 6.91  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 3.500))
        self.set_subtitle("沿著 x 方向切開，得到 z 等於 x 平方，是一條向上彎曲的拋物線。", run_time=_audio_dur_2)
        self.play(Create(curve_x), run_time=(2.5)*_scale_3)
        self.play(Indicate(curve_x, color=YELLOW))
        anim_time_3 = 3.500 * _scale_3
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q17_saddle_3d_1781378825/media/audio/In_3D_space__plot_th_fe11bed353/step_03_aeb36568.mp3")  # [auto-injected]
        _audio_dur_3 = 7.92  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 3.500))
        self.set_subtitle("沿著 y 方向切開，得到 z 等於負 y 平方，反而是一條向下彎曲的拋物線。", run_time=_audio_dur_3)
        self.play(Create(curve_y), run_time=(2.5)*_scale_4)
        self.play(Indicate(curve_y, color=GREEN))
        anim_time_4 = 3.500 * _scale_4
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q17_saddle_3d_1781378825/media/audio/In_3D_space__plot_th_fe11bed353/step_04_24d526c6.mp3")  # [auto-injected]
        _audio_dur_4 = 7.87  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 2.500))
        self.set_subtitle("在原點處，一個方向凹向上，另一個方向凹向下，所以這個紅點就是鞍點。", run_time=_audio_dur_4)
        self.play(Create(saddle_point), run_time=(1.5)*_scale_5)
        self.play(Indicate(saddle_point, color=RED))
        self.begin_ambient_camera_rotation(rate=0.3)
        anim_time_5 = 2.500 * _scale_5
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - anim_time_5 + 0.1))
        self.wait(remaining_5)
        self.stop_ambient_camera_rotation()
        self.wait(3)  # [Auto-injected by Shift-Left Repair]