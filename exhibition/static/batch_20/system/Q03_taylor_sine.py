# [VISUAL REASONING]
# A persistent white sin(x) curve serves as the ground truth on axes spanning [-pi, pi].
# Each Taylor partial sum (T1=BLUE, T2=GREEN, T3=YELLOW, T4=RED) is drawn in layers,
# with a single footer polynomial label updated via ReplacementTransform so only one
# expression shows at a time. Signal actions (Indicate/Circumscribe) emphasize each new
# approximation, illustrating progressive convergence toward sin(x).

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
        title = Text("Taylor Series of sin(x)", color=WHITE, font_size=36)
        title.to_edge(UP)

        axes = Axes(
            x_range=[-3.15, 3.15, 1.57],
            y_range=[-3, 3, 1],
            x_length=9,
            y_length=5,
            axis_config={"color": GREY},
        )
        axes.move_to(ORIGIN)

        sin_curve = ParametricFunction(
            lambda t: axes.c2p(t, np.sin(t)),
            t_range=[-3.14159, 3.14159, 0.05],
            color=WHITE,
        )
        sin_label = MathTex("\\sin(x)", color=WHITE).next_to(axes, UR, buff=0.1)

        curve_t1 = ParametricFunction(
            lambda t: axes.c2p(t, t),
            t_range=[-3.14159, 3.14159, 0.05],
            color=BLUE,
        )
        curve_t2 = ParametricFunction(
            lambda t: axes.c2p(t, t - t**3 / 6),
            t_range=[-3.14159, 3.14159, 0.05],
            color=GREEN,
        )
        curve_t3 = ParametricFunction(
            lambda t: axes.c2p(t, t - t**3 / 6 + t**5 / 120),
            t_range=[-3.14159, 3.14159, 0.05],
            color=YELLOW,
        )
        curve_t4 = ParametricFunction(
            lambda t: axes.c2p(t, t - t**3 / 6 + t**5 / 120 - t**7 / 5040),
            t_range=[-3.14159, 3.14159, 0.05],
            color=RED,
        )

        label_t1 = MathTex("P_1(x) = x", color=BLUE).move_to([0, -2.3, 0])
        label_t2 = MathTex("P_2(x) = x - \\dfrac{x^3}{3!}", color=GREEN).move_to([0, -2.3, 0])
        label_t3 = MathTex("P_3(x) = x - \\dfrac{x^3}{3!} + \\dfrac{x^5}{5!}", color=YELLOW).move_to([0, -2.3, 0])
        label_t4 = MathTex("P_4(x) = x - \\dfrac{x^3}{3!} + \\dfrac{x^5}{5!} - \\dfrac{x^7}{7!}", color=RED).move_to([0, -2.3, 0])

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q03_taylor_sine_1781379187/media/audio/Visualize_the_Taylor_ae6682017f/step_00_7975a1d6.mp3")  # [auto-injected]
        _audio_dur_0 = 7.10  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 3.500))
        self.set_subtitle("這是從負 pi 到正 pi 區間上真正的正弦曲線，是我們要逼近的目標。", run_time=_audio_dur_0)
        anim_time_1 = 3.500 * _scale_1
        self.play(Write(title), run_time=(1.0)*_scale_1)
        self.play(Create(axes), run_time=(1.0)*_scale_1)
        self.play(Create(sin_curve), Write(sin_label), run_time=(2.5)*_scale_1)
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - anim_time_1 + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q03_taylor_sine_1781379187/media/audio/Visualize_the_Taylor_ae6682017f/step_01_38584ca3.mp3")  # [auto-injected]
        _audio_dur_1 = 7.94  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 2.500))
        self.set_subtitle("第一項就是 x，在原點附近完美貼合 sin(x)，但很快就發散。", run_time=_audio_dur_1)
        anim_time_2 = 2.500 * _scale_2
        self.play(Create(curve_t1), FadeIn(label_t1), run_time=(2.0)*_scale_2)
        self.play(Indicate(curve_t1, color=BLUE), run_time=(0.5)*_scale_2)
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q03_taylor_sine_1781379187/media/audio/Visualize_the_Taylor_ae6682017f/step_02_9b5b3a71.mp3")  # [auto-injected]
        _audio_dur_2 = 7.94  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 2.500))
        self.set_subtitle("減去 x 的三次方除以三階乘，曲線向下彎曲，更遠地貼合正弦波。", run_time=_audio_dur_2)
        anim_time_3 = 2.500 * _scale_3
        self.play(Create(curve_t2), ReplacementTransform(label_t1, label_t2), run_time=(2.0)*_scale_3)
        self.play(Indicate(curve_t2, color=GREEN), run_time=(0.5)*_scale_3)
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q03_taylor_sine_1781379187/media/audio/Visualize_the_Taylor_ae6682017f/step_03_1642feaa.mp3")  # [auto-injected]
        _audio_dur_3 = 8.95  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 2.500))
        self.set_subtitle("加上 x 的五次方除以五階乘，把尾端拉回，幾乎追蹤 sin(x) 到邊緣。", run_time=_audio_dur_3)
        anim_time_4 = 2.500 * _scale_4
        self.play(Create(curve_t3), ReplacementTransform(label_t2, label_t3), run_time=(2.0)*_scale_4)
        self.play(Indicate(curve_t3, color=YELLOW), run_time=(0.5)*_scale_4)
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q03_taylor_sine_1781379187/media/audio/Visualize_the_Taylor_ae6682017f/step_04_ceeeb7ed.mp3")  # [auto-injected]
        _audio_dur_4 = 9.41  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 3.000))
        self.set_subtitle("加入 x 的七次方項後，多項式在整個區間都與 sin(x) 重疊，展現快速收斂。", run_time=_audio_dur_4)
        anim_time_5 = 3.000 * _scale_5
        self.play(Create(curve_t4), ReplacementTransform(label_t3, label_t4), run_time=(2.0)*_scale_5)
        self.play(Circumscribe(curve_t4, color=RED), run_time=(1.0)*_scale_5)
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - anim_time_5 + 0.1))
        self.wait(remaining_5)