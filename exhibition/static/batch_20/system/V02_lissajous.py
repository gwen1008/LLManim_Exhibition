# [VISUAL REASONING]
# A fixed centered coordinate system lets viewers directly compare how the frequency
# ratio a:b reshapes the closed Lissajous curve. The equation and ratio label live in
# the header zone while the curve is traced at the ORIGIN. Each new case fades out the
# previous curve and ReplacementTransforms the ratio label in place to avoid clutter.

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
        registry = {}

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V02_lissajous_1781401976/media/audio/Visualize_the_Lissaj_1bbe06b86f/step_00_5c42f40a.mp3")  # [auto-injected]
        _audio_dur_0 = 8.06  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 2.000))
        title = Text("Lissajous Figures", color=WHITE, font_size=36)
        title.to_edge(UP, buff=0.4)
        registry["title"] = title

        param_eq = MathTex(r"x=\sin(a t),\quad y=\sin(b t+\tfrac{\pi}{2})", color=WHITE)
        param_eq.next_to(title, DOWN, buff=0.25)
        registry["param_eq"] = param_eq

        anim_time_1 = 2.000 * _scale_1
        self.play(Write(title), run_time=(0.8)*_scale_1)
        self.play(Write(param_eq), run_time=(2.0)*_scale_1)
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - (anim_time_1 + 0.8) + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V02_lissajous_1781401976/media/audio/Visualize_the_Lissaj_1bbe06b86f/step_01_1a8e87df.mp3")  # [auto-injected]
        _audio_dur_1 = 6.38  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 1.500))
        axes = Axes(
            x_range=[-1.2, 1.2, 0.5],
            y_range=[-1.2, 1.2, 0.5],
            x_length=4.2,
            y_length=4.2,
            axis_config={"color": GREY},
        )
        axes.move_to(ORIGIN + np.array([0, -0.4, 0]))
        registry["axes"] = axes

        ratio_label = MathTex("a:b = 1:2", color=YELLOW)
        ratio_label.next_to(axes, RIGHT, buff=0.5)
        registry["ratio_label"] = ratio_label

        anim_time_2 = 1.500 * _scale_2
        self.play(Create(axes), run_time=(1.5)*_scale_2)
        self.play(Write(ratio_label), run_time=(0.8)*_scale_2)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - (anim_time_2 + 0.8 + 1.0) + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V02_lissajous_1781401976/media/audio/Visualize_the_Lissaj_1bbe06b86f/step_02_3406d75a.mp3")  # [auto-injected]
        _audio_dur_2 = 7.25  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 4.000))
        curve_12 = ParametricFunction(
            lambda t: axes.c2p(np.sin(1 * t), np.sin(2 * t + PI / 2)),
            t_range=[0, 6.2832, 0.01],
            color=BLUE,
        )
        curve_12.move_to(axes.get_center())
        registry["curve_12"] = curve_12

        anim_time_3 = 4.000 * _scale_3
        self.play(Create(curve_12), run_time=(4.0)*_scale_3, rate_func=linear)
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V02_lissajous_1781401976/media/audio/Visualize_the_Lissaj_1bbe06b86f/step_03_e18971ed.mp3")  # [auto-injected]
        _audio_dur_3 = 7.54  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 4.000))
        ratio_label_23 = MathTex("a:b = 2:3", color=YELLOW)
        ratio_label_23.next_to(axes, RIGHT, buff=0.5)
        registry["ratio_label_23"] = ratio_label_23

        curve_23 = ParametricFunction(
            lambda t: axes.c2p(np.sin(2 * t), np.sin(3 * t + PI / 2)),
            t_range=[0, 6.2832, 0.01],
            color=GREEN,
        )
        curve_23.move_to(axes.get_center())
        registry["curve_23"] = curve_23

        anim_time_4 = 4.000 * _scale_4
        self.play(
            FadeOut(registry["curve_12"]),
            ReplacementTransform(registry["ratio_label"], ratio_label_23),
            run_time=(1.0)*_scale_4,
        )
        self.play(Indicate(ratio_label_23, color=RED))
        self.play(Create(curve_23), run_time=(4.0)*_scale_4, rate_func=linear)
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - (anim_time_4 + 1.0 + 1.0) + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V02_lissajous_1781401976/media/audio/Visualize_the_Lissaj_1bbe06b86f/step_04_8dfdc2ae.mp3")  # [auto-injected]
        _audio_dur_4 = 8.69  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 4.000))
        ratio_label_34 = MathTex("a:b = 3:4", color=YELLOW)
        ratio_label_34.next_to(axes, RIGHT, buff=0.5)
        registry["ratio_label_34"] = ratio_label_34

        curve_34 = ParametricFunction(
            lambda t: axes.c2p(np.sin(3 * t), np.sin(4 * t + PI / 2)),
            t_range=[0, 6.2832, 0.01],
            color=ORANGE,
        )
        curve_34.move_to(axes.get_center())
        registry["curve_34"] = curve_34

        anim_time_5 = 4.000 * _scale_5
        self.play(
            FadeOut(registry["curve_23"]),
            ReplacementTransform(ratio_label_23, ratio_label_34),
            run_time=(1.0)*_scale_5,
        )
        self.play(Indicate(ratio_label_34, color=RED))
        self.play(Create(curve_34), run_time=(4.0)*_scale_5, rate_func=linear)
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - (anim_time_5 + 1.0 + 1.0) + 0.1))
        self.wait(remaining_5)