# [VISUAL REASONING]
# One fixed axes + sin curve stage stays throughout. Midpoint Riemann rectangle
# groups (n=4,8,16,32) are swapped in-place via ReplacementTransform while a single
# sum readout morphs toward 2, visually demonstrating convergence of the Riemann sum
# to the exact integral value of 2.

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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q01_riemann_sum_1781377994/media/audio/Calculate_the_value__533949b815/step_00_fd4fb78f.mp3")  # [auto-injected]
        _audio_dur_0 = 6.17  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 2.000))
        title = MathTex(r"\int_0^{\pi} \sin(x)\, dx = 2", color=WHITE).to_edge(UP)
        anim_time_1 = 2.000 * _scale_1
        self.play(Write(title), run_time=anim_time_1)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - anim_time_1 - 1.0 + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q01_riemann_sum_1781377994/media/audio/Calculate_the_value__533949b815/step_01_dcce0e87.mp3")  # [auto-injected]
        _audio_dur_1 = 4.90  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 2.000))
        axes = Axes(
            x_range=[0, 3.2, 0.7853981],
            y_range=[0, 1.2, 0.5],
            x_length=8,
            y_length=3.5,
            axis_config={"color": GREY},
        ).move_to(np.array([0, -0.6, 0]))
        sin_curve = axes.plot(lambda x: np.sin(x), x_range=[0, PI], color=BLUE)
        anim_time_2 = 2.000 * _scale_2
        self.play(Create(axes), run_time=(1.0)*_scale_2)
        self.play(Create(sin_curve), run_time=(1.0)*_scale_2)
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q01_riemann_sum_1781377994/media/audio/Calculate_the_value__533949b815/step_02_2e327d4b.mp3")  # [auto-injected]
        _audio_dur_2 = 7.18  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 2.000))
        rects_4 = axes.get_riemann_rectangles(
            sin_curve, x_range=[0, PI], dx=PI / 4,
            input_sample_type="center", color=GREEN,
            fill_opacity=0.5, stroke_width=1,
        )
        sum_4 = MathTex(r"n=4:\ S \approx 2.052", color=YELLOW)
        sum_4.move_to(axes.get_center() + np.array([0, 2.2, 0]))
        anim_time_3 = 2.000 * _scale_3
        self.play(Create(rects_4), Write(sum_4), run_time=anim_time_3)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 - 1.0 + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q01_riemann_sum_1781377994/media/audio/Calculate_the_value__533949b815/step_03_521d733b.mp3")  # [auto-injected]
        _audio_dur_3 = 7.34  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 2.000))
        rects_8 = axes.get_riemann_rectangles(
            sin_curve, x_range=[0, PI], dx=PI / 8,
            input_sample_type="center", color=GREEN,
            fill_opacity=0.5, stroke_width=1,
        )
        sum_8 = MathTex(r"n=8:\ S \approx 2.013", color=YELLOW).move_to(sum_4)
        anim_time_4 = 2.000 * _scale_4
        self.play(
            ReplacementTransform(rects_4, rects_8),
            ReplacementTransform(sum_4, sum_8),
            run_time=anim_time_4,
        )
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q01_riemann_sum_1781377994/media/audio/Calculate_the_value__533949b815/step_04_0787056f.mp3")  # [auto-injected]
        _audio_dur_4 = 7.34  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 2.000))
        rects_16 = axes.get_riemann_rectangles(
            sin_curve, x_range=[0, PI], dx=PI / 16,
            input_sample_type="center", color=GREEN,
            fill_opacity=0.5, stroke_width=1,
        )
        sum_16 = MathTex(r"n=16:\ S \approx 2.003", color=YELLOW).move_to(sum_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(
            ReplacementTransform(rects_8, rects_16),
            ReplacementTransform(sum_8, sum_16),
            run_time=anim_time_5,
        )
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - anim_time_5 + 0.1))
        self.wait(remaining_5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q01_riemann_sum_1781377994/media/audio/Calculate_the_value__533949b815/step_05_8e535482.mp3")  # [auto-injected]
        _audio_dur_5 = 8.21  # [audio-sync]
        # Step 6
        _scale_6 = min(2.5, max(1.0, (_audio_dur_5 * 0.95) / 2.000))
        rects_32 = axes.get_riemann_rectangles(
            sin_curve, x_range=[0, PI], dx=PI / 32,
            input_sample_type="center", color=TEAL,
            fill_opacity=0.5, stroke_width=1,
        )
        sum_32 = MathTex(r"n=32:\ S \approx 2.0008", color=GREEN).move_to(sum_4)
        anim_time_6 = 2.000 * _scale_6
        self.play(
            ReplacementTransform(rects_16, rects_32),
            ReplacementTransform(sum_16, sum_32),
            run_time=anim_time_6,
        )
        self.play(Circumscribe(sum_32, color=GREEN))
        remaining_6 = min(1.5, max(0.1, _audio_dur_5 - anim_time_6 - 1.0 + 0.1))
        self.wait(remaining_6)