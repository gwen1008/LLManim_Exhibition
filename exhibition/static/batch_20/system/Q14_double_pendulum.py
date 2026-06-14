# [VISUAL REASONING]
# The double pendulum is integrated numerically with RK4 (dt=1/60s) because Manim
# cannot solve its nonlinear ODE symbolically. A single ValueTracker drives a global
# simulation clock; updaters on both arms and both bobs read the precomputed state
# each frame so the mechanical system literally swings. A TracedPath on the lower bob
# (YELLOW) accumulates the tangled, never-repeating chaotic curve. The pivot is fixed
# at [0,0.3,0] giving the arms full vertical room while keeping every bob above y=-1.7,
# safely clear of the subtitle zone. The footer caption delivers the takeaway about
# sensitive dependence on initial conditions.
from manim import *
import numpy as np


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
        L1, L2 = 1.0, 1.0
        m1, m2 = 1.0, 1.0
        g = 9.8
        dt = 1.0 / 60.0
        pivot_point = np.array([0.0, 0.3, 0.0])

        def derivs(state):
            t1, w1, t2, w2 = state
            delta = t2 - t1
            den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta) ** 2
            den2 = (L2 / L1) * den1
            dw1 = (
                m2 * L1 * w1 ** 2 * np.sin(delta) * np.cos(delta)
                + m2 * g * np.sin(t2) * np.cos(delta)
                + m2 * L2 * w2 ** 2 * np.sin(delta)
                - (m1 + m2) * g * np.sin(t1)
            ) / den1
            dw2 = (
                -m2 * L2 * w2 ** 2 * np.sin(delta) * np.cos(delta)
                + (m1 + m2)
                * (g * np.sin(t1) * np.cos(delta) - L1 * w1 ** 2 * np.sin(delta) - g * np.sin(t2))
            ) / den2
            return np.array([w1, dw1, w2, dw2])

        def rk4_step(state, h):
            k1 = derivs(state)
            k2 = derivs(state + 0.5 * h * k1)
            k3 = derivs(state + 0.5 * h * k2)
            k4 = derivs(state + h * k3)
            return state + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        theta0 = np.deg2rad(120.0)
        state = np.array([theta0, 0.0, theta0, 0.0])
        states = [state.copy()]
        total_frames = 600
        for _ in range(total_frames):
            state = rk4_step(state, dt)
            states.append(state.copy())

        def state_at(t):
            idx = int(t / dt)
            if idx >= len(states):
                idx = len(states) - 1
            return states[idx]

        def b1_pos(t):
            t1 = state_at(t)[0]
            return pivot_point + L1 * np.array([np.sin(t1), -np.cos(t1), 0.0])

        def b2_pos(t):
            s = state_at(t)
            t1, t2 = s[0], s[2]
            p1 = pivot_point + L1 * np.array([np.sin(t1), -np.cos(t1), 0.0])
            return p1 + L2 * np.array([np.sin(t2), -np.cos(t2), 0.0])

        time_tracker = ValueTracker(0.0)

        title = Text("The Double Pendulum: Deterministic Chaos", color=WHITE, font_size=34)
        title.to_edge(UP)

        pivot = Dot(point=pivot_point, color=GREY_B, radius=0.08)
        arm1 = Line(start=[0, 0.3, 0], end=[0.866, 0.8, 0], color=BLUE, stroke_width=6)
        bob1 = Dot(point=[0.866, 0.8, 0], color=BLUE, radius=0.12)
        arm2 = Line(start=[0.866, 0.8, 0], end=[1.732, 1.3, 0], color=TEAL, stroke_width=6)
        bob2 = Dot(point=[1.732, 1.3, 0], color=YELLOW, radius=0.12)
        angle_label = MathTex(r"\theta_1 = \theta_2 = 120^\circ", color=WHITE)
        angle_label.to_corner(UL, buff=0.6)
        caption = Text(
            "Tiny changes in start angle yield wildly different paths.",
            color=GREY_A,
            font_size=26,
        )
        caption.move_to([0, -2.6, 0])

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q14_double_pendulum_1781379586/media/audio/Visualize_the_chaoti_c0a717df99/step_00_e25fa6ce.mp3")  # [auto-injected]
        _audio_dur_0 = 6.19  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 2.500))
        self.set_subtitle("我們建立一個雙擺：兩根等長的擺臂由固定樞紐鉸接在一起。", run_time=_audio_dur_0)
        self.play(Write(title), run_time=(1.0)*_scale_1)
        self.play(FadeIn(pivot), Create(arm1), FadeIn(bob1), run_time=(1.5)*_scale_1)
        anim_time_1 = 2.500 * _scale_1
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - anim_time_1 + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q14_double_pendulum_1781379586/media/audio/Visualize_the_chaoti_c0a717df99/step_01_dfa1f57f.mp3")  # [auto-injected]
        _audio_dur_1 = 8.14  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 3.500))
        self.set_subtitle("兩根擺臂初始都傾斜到 120 度，幾乎水平，並完全靜止地被釋放。", run_time=_audio_dur_1)
        self.play(Create(arm2), FadeIn(bob2), run_time=(1.5)*_scale_2)
        self.play(Write(angle_label), run_time=(1.0)*_scale_2)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        anim_time_2 = 3.500 * _scale_2
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q14_double_pendulum_1781379586/media/audio/Visualize_the_chaoti_c0a717df99/step_02_75390115.mp3")  # [auto-injected]
        _audio_dur_2 = 6.10  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 5.000))
        self.set_subtitle("現在我們釋放系統，讓重力驅動它完整的非線性動力學。", run_time=_audio_dur_2)
        traced = TracedPath(bob2.get_center, stroke_color=YELLOW, stroke_width=2.5)
        self.add(traced)
        arm1.add_updater(
            lambda m: m.put_start_and_end_on(pivot_point, b1_pos(time_tracker.get_value()))
        )
        bob1.add_updater(lambda m: m.move_to(b1_pos(time_tracker.get_value())))
        arm2.add_updater(
            lambda m: m.put_start_and_end_on(
                b1_pos(time_tracker.get_value()), b2_pos(time_tracker.get_value())
            )
        )
        bob2.add_updater(lambda m: m.move_to(b2_pos(time_tracker.get_value())))
        self.play(Indicate(bob2, color=RED), run_time=(1.0)*_scale_3)
        self.play(time_tracker.animate.set_value(4.0), run_time=(4.0)*_scale_3, rate_func=linear)
        anim_time_3 = 5.000 * _scale_3
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q14_double_pendulum_1781379586/media/audio/Visualize_the_chaoti_c0a717df99/step_03_4dee319a.mp3")  # [auto-injected]
        _audio_dur_3 = 6.34  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 5.000))
        self.set_subtitle("下方擺錘描繪出一條糾纏的曲線，不斷迴圈交錯卻從不重複。", run_time=_audio_dur_3)
        self.play(time_tracker.animate.set_value(9.0), run_time=(5.0)*_scale_4, rate_func=linear)
        anim_time_4 = 5.000 * _scale_4
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q14_double_pendulum_1781379586/media/audio/Visualize_the_chaoti_c0a717df99/step_04_4bb42ec0.mp3")  # [auto-injected]
        _audio_dur_4 = 7.49  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 3.000))
        self.set_subtitle("這條不重複的路徑揭示了混沌：確定性規則卻產生完全不可預測的運動。", run_time=_audio_dur_4)
        for m in [arm1, bob1, arm2, bob2]:
            m.clear_updaters()
        self.play(Write(caption), run_time=(2.0)*_scale_5)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        anim_time_5 = 3.000 * _scale_5
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - anim_time_5 + 0.1))
        self.wait(remaining_5)