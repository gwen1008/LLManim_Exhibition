from manim import *
import numpy as np

# [VISUAL REASONING]
# 2D x-z projection of the Lorenz attractor with RK4 integration.
# Left column: equations + parameters + initial condition.
# Right column: axes with progressively drawn butterfly trajectory + leading dot.
# Final caption emphasizes deterministic chaos.

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
        # --- Pre-compute Lorenz trajectory via RK4 ---
        sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0

        def lorenz(state):
            x, y, z = state
            return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])

        dt = 0.01
        n_steps = 4000
        traj = np.zeros((n_steps + 1, 3))
        traj[0] = np.array([0.1, 0.0, 0.0])
        for i in range(n_steps):
            s = traj[i]
            k1 = lorenz(s)
            k2 = lorenz(s + 0.5 * dt * k1)
            k3 = lorenz(s + 0.5 * dt * k2)
            k4 = lorenz(s + dt * k3)
            traj[i + 1] = s + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        # --- Build registry ---
        title = Text("The Lorenz Attractor", font_size=40, weight=BOLD).move_to([0, 3.0, 0])

        eq_system = VGroup(
            MathTex(r"\dot{x} = \sigma(y-x)", font_size=34),
            MathTex(r"\dot{y} = x(\rho-z)-y", font_size=34),
            MathTex(r"\dot{z} = xy - \beta z", font_size=34),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-4.0, 1.2, 0])

        params = MathTex(r"\sigma=10,\ \rho=28,\ \beta=\tfrac{8}{3}", font_size=32).move_to([-4.0, -0.6, 0])

        init_cond = MathTex(r"(x_0,y_0,z_0)=(0.1,\,0,\,0)", font_size=28).move_to([-4.0, -1.6, 0])

        axes_xz = Axes(
            x_range=[-25, 25, 10],
            y_range=[0, 50, 10],
            x_length=5.6,
            y_length=4.2,
        ).move_to([2.8, 0.0, 0])

        axis_label_x = MathTex("x", font_size=28).move_to([5.7, -2.1, 0])
        axis_label_z = MathTex("z", font_size=28).move_to([2.8, 2.3, 0])

        # Build trajectory VMobject from integrated points
        pts = [axes_xz.c2p(traj[i, 0], traj[i, 2]) for i in range(n_steps + 1)]
        trajectory_curve = VMobject(color=BLUE, stroke_width=2)
        trajectory_curve.set_points_smoothly(pts[::4])

        leading_dot = Dot(radius=0.08, color=YELLOW).move_to(pts[0])

        wing_label_left = Text("Wing A", font_size=22, color=GRAY).move_to([1.4, 0.6, 0])
        wing_label_right = Text("Wing B", font_size=22, color=GRAY).move_to([4.2, 0.6, 0])

        caption_chaos = Text(
            "Deterministic chaos: bounded yet non-periodic",
            font_size=24,
            color=GOLD,
        ).move_to([0, -2.5, 0])

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q16_lorenz_1779993703/media/audio/Plot_the_trajectory__5cd5d22b08/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 10.56  # [audio-sync]
        # Step 1
        self.set_subtitle("勞侖次系統是三個耦合的非線性常微分方程，源自1963年大氣對流的簡化模型。", run_time=_audio_dur_0)
        anim_time_1 = _audio_dur_0
        self.play(
            LaggedStart(
                Write(title),
                Write(eq_system),
                Indicate(eq_system, color=YELLOW),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q16_lorenz_1779993703/media/audio/Plot_the_trajectory__5cd5d22b08/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 11.64  # [audio-sync]
        # Step 2
        self.set_subtitle("使用經典混沌參數 σ=10、ρ=28、β=8/3，從靠近原點的微小擾動出發。", run_time=_audio_dur_1)
        anim_time_2 = _audio_dur_1
        self.play(
            LaggedStart(
                Write(params),
                Indicate(params, color=YELLOW),
                Write(init_cond),
                Create(axes_xz),
                AnimationGroup(Write(axis_label_x), Write(axis_label_z)),
                lag_ratio=0.25,
                run_time=anim_time_2,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q16_lorenz_1779993703/media/audio/Plot_the_trajectory__5cd5d22b08/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 11.69  # [audio-sync]
        # Step 3
        self.set_subtitle("數值積分後在三維空間描繪軌跡，投影到 x-z 平面，著名的蝴蝶剪影逐漸浮現。", run_time=_audio_dur_2)
        anim_time_3 = _audio_dur_2
        self.play(
            LaggedStart(
                FadeIn(leading_dot),
                AnimationGroup(
                    Create(trajectory_curve),
                    MoveAlongPath(leading_dot, trajectory_curve),
                ),
                lag_ratio=0.25,
                run_time=anim_time_3,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q16_lorenz_1779993703/media/audio/Plot_the_trajectory__5cd5d22b08/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 12.31  # [audio-sync]
        # Step 4
        self.set_subtitle("軌跡繞著兩個不穩定平衡點運行，在兩翼之間不可預測地切換，這正是決定性混沌的標誌。", run_time=_audio_dur_3)
        anim_time_4 = _audio_dur_3
        self.play(
            LaggedStart(
                FadeIn(wing_label_left),
                FadeIn(wing_label_right),
                Indicate(wing_label_left, color=YELLOW),
                Indicate(wing_label_right, color=YELLOW),
                Write(caption_chaos),
                Flash(leading_dot, color=YELLOW, flash_radius=0.4),
                lag_ratio=0.25,
                run_time=anim_time_4,
            )
        )
        self.wait(0.1)