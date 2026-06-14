from manim import *

# [VISUAL REASONING]
# A persistent polar grid (NumberPlane) sits at ORIGIN so every rose r = sin(kθ)
# is drawn in the same frame of reference. ParametricFunction curves are traced
# with Create(...) to simulate a moving pen sweeping θ from 0 to 2π. Formula and
# petal-count labels in the footer use ReplacementTransform to update in-place,
# reinforcing the odd-vs-even rule (odd k → k petals, even k → 2k petals).
# All curve points stay within y in [-2, 2], safely above the subtitle zone.


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
        self.camera.background_color = "#1e1e1e"

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V01_rose_curve_1781430342/media/audio/Visualize_the_polar__a8744d6610/step_00_e0161ac9.mp3")  # [auto-injected]
        _audio_dur_0 = 6.62  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 2.000))
        title = Text("Polar Rose: r = sin(kθ)", color=WHITE, font_size=38).to_edge(UP)

        polar_plane = NumberPlane(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            background_line_style={"stroke_color": GREY, "stroke_opacity": 0.4},
        ).move_to(ORIGIN)

        anim_time_1 = 2.000 * _scale_1
        self.play(Create(polar_plane), run_time=(2.0)*_scale_1)
        self.play(Write(title), run_time=(1.0)*_scale_1)
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - anim_time_1 - 1.0 + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V01_rose_curve_1781430342/media/audio/Visualize_the_polar__a8744d6610/step_01_2b2b07e1.mp3")  # [auto-injected]
        _audio_dur_1 = 7.78  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 4.000))
        formula_label = MathTex(r"r = \sin(2\theta)", color=YELLOW, font_size=36).move_to(
            np.array([-3.0, -2.3, 0])
        )
        petal_label = MathTex(
            r"k=2\ (even)\Rightarrow 4\ petals", color=PINK, font_size=32
        ).move_to(np.array([2.5, -2.3, 0]))

        curve_k2 = ParametricFunction(
            lambda t: [np.sin(2 * t) * np.cos(t) * 2, np.sin(2 * t) * np.sin(t) * 2, 0],
            t_range=[0, 6.2832, 0.01],
            color=PINK,
        ).move_to(ORIGIN)

        self.play(Write(formula_label), Write(petal_label), run_time=(1.0)*_scale_2)
        anim_time_2 = 4.000 * _scale_2
        self.play(Create(curve_k2), run_time=(4.0)*_scale_2, rate_func=linear)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 - 1.0 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V01_rose_curve_1781430342/media/audio/Visualize_the_polar__a8744d6610/step_02_0ec23f64.mp3")  # [auto-injected]
        _audio_dur_2 = 6.00  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 4.000))
        curve_k3 = ParametricFunction(
            lambda t: [np.sin(3 * t) * np.cos(t) * 2, np.sin(3 * t) * np.sin(t) * 2, 0],
            t_range=[0, 6.2832, 0.01],
            color=TEAL,
        ).move_to(ORIGIN)

        new_formula_3 = MathTex(r"r = \sin(3\theta)", color=YELLOW, font_size=36).move_to(
            formula_label.get_center()
        )
        new_petal_3 = MathTex(
            r"k=3\ (odd)\Rightarrow 3\ petals", color=TEAL, font_size=32
        ).move_to(petal_label.get_center())

        self.play(FadeOut(curve_k2), run_time=(0.5)*_scale_3)
        self.play(
            ReplacementTransform(formula_label, new_formula_3),
            ReplacementTransform(petal_label, new_petal_3),
            run_time=(0.8)*_scale_3,
        )
        formula_label = new_formula_3
        petal_label = new_petal_3

        anim_time_3 = 4.000 * _scale_3
        self.play(Create(curve_k3), run_time=(4.0)*_scale_3, rate_func=linear)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 - 1.3 + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V01_rose_curve_1781430342/media/audio/Visualize_the_polar__a8744d6610/step_03_c320aa02.mp3")  # [auto-injected]
        _audio_dur_3 = 7.49  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 4.500))
        curve_k4 = ParametricFunction(
            lambda t: [np.sin(4 * t) * np.cos(t) * 2, np.sin(4 * t) * np.sin(t) * 2, 0],
            t_range=[0, 6.2832, 0.01],
            color=ORANGE,
        ).move_to(ORIGIN)

        new_formula_4 = MathTex(r"r = \sin(4\theta)", color=YELLOW, font_size=36).move_to(
            formula_label.get_center()
        )
        new_petal_4 = MathTex(
            r"k=4\ (even)\Rightarrow 8\ petals", color=ORANGE, font_size=32
        ).move_to(petal_label.get_center())

        self.play(FadeOut(curve_k3), run_time=(0.5)*_scale_4)
        self.play(
            ReplacementTransform(formula_label, new_formula_4),
            ReplacementTransform(petal_label, new_petal_4),
            run_time=(0.8)*_scale_4,
        )
        formula_label = new_formula_4
        petal_label = new_petal_4

        anim_time_4 = 4.500 * _scale_4
        self.play(Create(curve_k4), run_time=(4.5)*_scale_4, rate_func=linear)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 - 1.3 + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V01_rose_curve_1781430342/media/audio/Visualize_the_polar__a8744d6610/step_04_6890c6b3.mp3")  # [auto-injected]
        _audio_dur_4 = 7.97  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 4.500))
        curve_k5 = ParametricFunction(
            lambda t: [np.sin(5 * t) * np.cos(t) * 2, np.sin(5 * t) * np.sin(t) * 2, 0],
            t_range=[0, 6.2832, 0.01],
            color=PURPLE,
        ).move_to(ORIGIN)

        new_formula_5 = MathTex(r"r = \sin(5\theta)", color=YELLOW, font_size=36).move_to(
            formula_label.get_center()
        )
        new_petal_5 = MathTex(
            r"k=5\ (odd)\Rightarrow 5\ petals", color=PURPLE, font_size=32
        ).move_to(petal_label.get_center())

        self.play(FadeOut(curve_k4), run_time=(0.5)*_scale_5)
        self.play(
            ReplacementTransform(formula_label, new_formula_5),
            ReplacementTransform(petal_label, new_petal_5),
            run_time=(0.8)*_scale_5,
        )
        formula_label = new_formula_5
        petal_label = new_petal_5

        anim_time_5 = 4.500 * _scale_5
        self.play(Create(curve_k5), run_time=(4.5)*_scale_5, rate_func=linear)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - anim_time_5 - 1.3 + 0.1))
        self.wait(remaining_5)