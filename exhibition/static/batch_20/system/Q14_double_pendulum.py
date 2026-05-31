# [VISUAL REASONING]
# Build a double pendulum centered on screen with pivot at (0, 1.5).
# Title at top, governing equations top-right, caption at bottom.
# Use ValueTracker + always_redraw for arm/bob updaters driven by RK4-integrated angles.
# TracedPath on bob2 reveals chaotic trajectory. Audio durations gate each step.

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
        # ---------- Physics helpers ----------
        G = 9.8
        L1 = 1.0
        L2 = 1.0
        M1 = 1.0
        M2 = 1.0
        PIVOT = np.array([0.0, 1.5, 0.0])

        def derivs(state):
            th1, w1, th2, w2 = state
            d = th2 - th1
            denom1 = (M1 + M2) * L1 - M2 * L1 * np.cos(d) * np.cos(d)
            a1 = (M2 * L1 * w1 * w1 * np.sin(d) * np.cos(d)
                  + M2 * G * np.sin(th2) * np.cos(d)
                  + M2 * L2 * w2 * w2 * np.sin(d)
                  - (M1 + M2) * G * np.sin(th1)) / denom1
            denom2 = (L2 / L1) * denom1
            a2 = (-M2 * L2 * w2 * w2 * np.sin(d) * np.cos(d)
                  + (M1 + M2) * G * np.sin(th1) * np.cos(d)
                  - (M1 + M2) * L1 * w1 * w1 * np.sin(d)
                  - (M1 + M2) * G * np.sin(th2)) / denom2
            return np.array([w1, a1, w2, a2])

        def rk4_step(state, dt):
            k1 = derivs(state)
            k2 = derivs(state + dt * k1 / 2)
            k3 = derivs(state + dt * k2 / 2)
            k4 = derivs(state + dt * k3)
            return state + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6

        # Pre-simulate full trajectory keyed by simulation time
        sim_dt = 0.005
        sim_total = 12.0
        n_steps = int(sim_total / sim_dt) + 2
        state = np.array([2.0, 0.0, 2.0, 0.0])
        traj_th1 = np.zeros(n_steps)
        traj_th2 = np.zeros(n_steps)
        traj_th1[0], traj_th2[0] = state[0], state[2]
        for i in range(1, n_steps):
            state = rk4_step(state, sim_dt)
            traj_th1[i] = state[0]
            traj_th2[i] = state[2]

        sim_time = ValueTracker(0.0)

        def get_angles():
            t = sim_time.get_value()
            idx = int(t / sim_dt)
            idx = max(0, min(idx, n_steps - 1))
            return traj_th1[idx], traj_th2[idx]

        def bob1_pos():
            th1, _ = get_angles()
            return PIVOT + np.array([L1 * np.sin(th1), -L1 * np.cos(th1), 0.0])

        def bob2_pos():
            th1, th2 = get_angles()
            p1 = PIVOT + np.array([L1 * np.sin(th1), -L1 * np.cos(th1), 0.0])
            return p1 + np.array([L2 * np.sin(th2), -L2 * np.cos(th2), 0.0])

        # ---------- Objects ----------
        title = Text("Double Pendulum: Chaotic Motion", color=WHITE, font_size=36).to_edge(UP, buff=0.5)

        pivot = Dot(point=PIVOT, color=WHITE, radius=0.08)

        arm1 = always_redraw(lambda: Line(PIVOT, bob1_pos(), color=BLUE, stroke_width=4))
        bob1 = always_redraw(lambda: Dot(point=bob1_pos(), color=BLUE, radius=0.14))
        arm2 = always_redraw(lambda: Line(bob1_pos(), bob2_pos(), color=RED, stroke_width=4))
        bob2 = always_redraw(lambda: Dot(point=bob2_pos(), color=RED, radius=0.14))

        equations = MathTex(r"\ddot{\theta_1},\ \ddot{\theta_2} = f(\theta_1,\theta_2,\dot{\theta_1},\dot{\theta_2})", color=WHITE).scale(0.55).to_corner(UR, buff=0.5)

        caption = Text("Tiny changes in initial angles produce vastly different paths.", color=YELLOW, font_size=24).move_to([0, -2.3, 0])

        # Static initial visuals for steps 1-2 (before simulation animates)
        arm1_static = Line(PIVOT, bob1_pos(), color=BLUE, stroke_width=4)
        bob1_static = Dot(point=bob1_pos(), color=BLUE, radius=0.14)
        arm2_static = Line(bob1_pos(), bob2_pos(), color=RED, stroke_width=4)
        bob2_static = Dot(point=bob2_pos(), color=RED, radius=0.14)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q14_double_pendulum_1779988291/media/audio/Visualizing_the_chao_42417e892d/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 6.17  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 3.000)
        self.set_subtitle("我們建構一個雙擺：兩根剛性擺臂在關節處連接，懸掛於固定的樞軸上。", run_time=_audio_dur_0)
        anim_time_1 = 3.000 * _scale_1
        self.play(Write(title), run_time=1.0)
        self.play(
            LaggedStart(
                Create(pivot),
                Create(arm1_static),
                Create(bob1_static),
                Create(arm2_static),
                Create(bob2_static),
                lag_ratio=0.25,
            ),
            run_time=2.0,
        )
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q14_double_pendulum_1779988291/media/audio/Visualizing_the_chao_42417e892d/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 7.10  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.500)
        self.set_subtitle("它的運動由耦合的非線性微分方程描述 — 沒有封閉形式的解。", run_time=_audio_dur_1)
        anim_time_2 = 2.500 * _scale_2
        self.play(Write(equations), run_time=2.0)
        self.play(Circumscribe(equations, color=YELLOW), run_time=0.5)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q14_double_pendulum_1779988291/media/audio/Visualizing_the_chao_42417e892d/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 6.91  # [audio-sync]
        # Step 3 — swap static visuals for live updaters and run simulation
        self.set_subtitle("讓系統從靜止釋放，由物理接管，以數值方法積分運動方程。", run_time=_audio_dur_2)
        self.remove(arm1_static, bob1_static, arm2_static, bob2_static)
        self.add(arm1, bob1, arm2, bob2)
        anim_time_3 = 3.5
        self.play(Indicate(bob2, color=RED), run_time=0.5)
        self.play(sim_time.animate.set_value(3.0), run_time=3.0, rate_func=linear)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q14_double_pendulum_1779988291/media/audio/Visualizing_the_chao_42417e892d/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 5.98  # [audio-sync]
        # Step 4 — trace path
        self.set_subtitle("現在我們追蹤第二根擺臂的尖端 — 看著路徑扭轉，永不重複。", run_time=_audio_dur_3)
        trace = TracedPath(bob2.get_center, stroke_color=YELLOW, stroke_width=2)
        self.add(trace)
        anim_time_4 = 8.0
        self.play(sim_time.animate.set_value(11.0), run_time=8.0, rate_func=linear)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q14_double_pendulum_1779988291/media/audio/Visualizing_the_chao_42417e892d/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.41  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.500)
        self.set_subtitle("這就是確定性混沌：簡單的規則產生實際上無法預測的運動。", run_time=_audio_dur_4)
        anim_time_5 = 2.500 * _scale_5
        self.play(Write(caption), run_time=2.0)
        self.play(Circumscribe(caption, color=YELLOW), run_time=0.5)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)