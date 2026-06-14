from manim import *
import numpy as np

# [VISUAL REASONING]
# A central Axes hosts the white target curve y=ln(1+x). Taylor polynomials P1..P5
# are drawn sequentially in a warm-to-cool ramp (RED->ORANGE->YELLOW->GREEN->BLUE),
# each clipped vertically to stay on screen. Earlier curves fade to opacity 0.25 so the
# family is seen converging. A header formula morphs as terms accumulate, and dashed
# purple walls at x=±1 anchor the radius of convergence to a concrete screen location.

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

        def clip(f):
            def g(x):
                y = f(x)
                if y > 3.0 or y < -3.0:
                    return np.nan
                return y
            return g

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q20_taylor_log_1781379961/media/audio/Visualize_the_Taylor_b6d53338a1/step_00_f66cd8ee.mp3")  # [auto-injected]
        _audio_dur_0 = 7.06  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 1.500))
        title = Text("Taylor Series of ln(1+x)", color=WHITE, font_size=36).to_edge(UP, buff=0.4)
        registry["title"] = title

        axes = Axes(
            x_range=[-1.5, 2.5, 1],
            y_range=[-3, 2, 1],
            x_length=9,
            y_length=5,
            axis_config={"color": GREY},
        ).move_to(ORIGIN)
        registry["axes"] = axes

        ln_curve = axes.plot(clip(lambda x: np.log(1 + x)), x_range=[-0.98, 2.4, 0.01], color=WHITE)
        registry["ln_curve"] = ln_curve

        ln_label = MathTex(r"y=\ln(1+x)", color=WHITE).next_to(axes, UR, buff=0.1)
        registry["ln_label"] = ln_label

        anim_time_1 = 1.500 * _scale_1
        self.play(Write(title), run_time=(0.8)*_scale_1)
        self.play(Create(axes), run_time=anim_time_1)
        self.play(Create(ln_curve), Write(ln_label), run_time=(1.5)*_scale_1)
        self.set_subtitle("我們先畫出真實曲線 y 等於 ln(1 加 x)，以白色作為我們的目標。", run_time=_audio_dur_0)
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - (0.8 + anim_time_1 + 1.5) + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q20_taylor_log_1781379961/media/audio/Visualize_the_Taylor_b6d53338a1/step_01_77b7dbe1.mp3")  # [auto-injected]
        _audio_dur_1 = 6.82  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 2.000))
        p1 = axes.plot(clip(lambda x: x), x_range=[-0.98, 1.8, 0.01], color=RED)
        registry["p1"] = p1

        series_label = MathTex(r"P_1 = x", color=RED).next_to(title, DOWN, buff=0.15)
        registry["series_label"] = series_label

        anim_time_2 = 2.000 * _scale_2
        self.play(Create(p1), Write(series_label), run_time=anim_time_2)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        self.set_subtitle("第一個泰勒項就是 x，一條直線，只在原點附近吻合曲線。", run_time=_audio_dur_1)
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - (anim_time_2 + 1.0) + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q20_taylor_log_1781379961/media/audio/Visualize_the_Taylor_b6d53338a1/step_02_c9bd3c65.mp3")  # [auto-injected]
        _audio_dur_2 = 8.54  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 2.000))
        p2 = axes.plot(clip(lambda x: x - x**2 / 2), x_range=[-0.98, 1.8, 0.01], color=ORANGE)
        registry["p2"] = p2

        series_label_2 = MathTex(r"P_2 = x - \frac{x^2}{2}", color=ORANGE).next_to(title, DOWN, buff=0.15)

        anim_time_3 = 2.000 * _scale_3
        self.play(Create(p2), run_time=anim_time_3)
        self.play(
            ReplacementTransform(series_label, series_label_2),
            p1.animate.set_opacity(0.25),
        )
        registry["series_label"] = series_label_2
        self.play(Circumscribe(series_label_2, color=ORANGE))
        self.set_subtitle("加上負 x 平方除以二，讓直線向下彎曲，在更大的範圍內貼近 ln(1 加 x)。", run_time=_audio_dur_2)
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - (anim_time_3 + 2.0) + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q20_taylor_log_1781379961/media/audio/Visualize_the_Taylor_b6d53338a1/step_03_67ce3a01.mp3")  # [auto-injected]
        _audio_dur_3 = 9.62  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 2.500))
        p3 = axes.plot(clip(lambda x: x - x**2 / 2 + x**3 / 3), x_range=[-0.98, 1.8, 0.01], color=YELLOW)
        registry["p3"] = p3
        p4 = axes.plot(clip(lambda x: x - x**2 / 2 + x**3 / 3 - x**4 / 4), x_range=[-0.98, 1.8, 0.01], color=GREEN)
        registry["p4"] = p4

        series_label_4 = MathTex(
            r"P_4 = x - \frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4}", color=GREEN
        ).next_to(title, DOWN, buff=0.15)

        anim_time_4 = 2.500 * _scale_4
        self.play(Succession(Create(p3), Create(p4)), run_time=anim_time_4)
        self.play(
            ReplacementTransform(registry["series_label"], series_label_4),
            p2.animate.set_opacity(0.25),
            p3.animate.set_opacity(0.25),
        )
        registry["series_label"] = series_label_4
        self.play(Indicate(series_label_4, color=GREEN))
        self.set_subtitle("每加一項，先是加 x 立方除以三，再減 x 四次方除以四，多項式就越來越貼近曲線。", run_time=_audio_dur_3)
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - (anim_time_4 + 2.0) + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q20_taylor_log_1781379961/media/audio/Visualize_the_Taylor_b6d53338a1/step_04_54b3ede3.mp3")  # [auto-injected]
        _audio_dur_4 = 7.82  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 2.000))
        p5 = axes.plot(
            clip(lambda x: x - x**2 / 2 + x**3 / 3 - x**4 / 4 + x**5 / 5),
            x_range=[-0.98, 1.8, 0.01],
            color=BLUE,
        )
        registry["p5"] = p5

        series_label_5 = MathTex(
            r"P_5 = x - \frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4} + \frac{x^5}{5}", color=BLUE
        ).next_to(title, DOWN, buff=0.15)

        anim_time_5 = 2.000 * _scale_5
        self.play(Create(p5), run_time=anim_time_5)
        self.play(
            ReplacementTransform(registry["series_label"], series_label_5),
            p4.animate.set_opacity(0.25),
        )
        registry["series_label"] = series_label_5
        self.play(Indicate(p5, color=BLUE))
        self.set_subtitle("到了第五項，藍色曲線在區間內幾乎完美地追隨 ln(1 加 x)。", run_time=_audio_dur_4)
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - (anim_time_5 + 2.0) + 0.1))
        self.wait(remaining_5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q20_taylor_log_1781379961/media/audio/Visualize_the_Taylor_b6d53338a1/step_05_e48b39e0.mp3")  # [auto-injected]
        _audio_dur_5 = 8.26  # [audio-sync]
        # Step 6
        _scale_6 = min(2.5, max(1.0, (_audio_dur_5 * 0.95) / 2.000))
        bound_right = DashedLine(
            start=axes.c2p(1, -2.5),
            end=axes.c2p(1, 1.8),
            color=PURPLE,
        )
        registry["bound_right"] = bound_right
        bound_left = DashedLine(
            start=axes.c2p(-1, -2.5),
            end=axes.c2p(-1, 1.8),
            color=PURPLE,
        )
        registry["bound_left"] = bound_left

        bound_label = MathTex(r"|x|<1", color=PURPLE).next_to(bound_right, UP, buff=0.15)
        registry["bound_label"] = bound_label

        anim_time_6 = 2.000 * _scale_6
        self.play(Create(bound_left), Create(bound_right), run_time=anim_time_6)
        self.play(Write(bound_label), run_time=(1.0)*_scale_6)
        self.play(Indicate(bound_right, color=PURPLE))
        self.set_subtitle("但超過 x 等於一之後，部分和開始發散，標示出級數發散的收斂半徑。", run_time=_audio_dur_5)
        remaining_6 = min(1.5, max(0.1, _audio_dur_5 - (anim_time_6 + 2.0) + 0.1))
        self.wait(remaining_6)