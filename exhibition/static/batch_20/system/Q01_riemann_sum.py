from manim import *
from numpy import sin

# [VISUAL REASONING]
# A right-Riemann sum on sin(x) over [0, pi] converges to 2 as rectangle count
# doubles (4 -> 8 -> 16 -> 32). The graph stays centered; one n-label and one
# sum-label update in place via ReplacementTransform so only a single set of
# rectangles and a single numeric readout are ever visible, letting students
# watch both geometric tightening and monotone numeric convergence
# (1.8961 -> 1.9742 -> 1.9936 -> 1.9984 -> 2).

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

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q01_riemann_sum_1781442105/media/audio/Calculate_the_value__533949b815/step_00_3bb03124.mp3")  # [auto-injected]
        _audio_dur_0 = 6.89  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 2.000))
        title = MathTex(r"\int_0^{\pi} \sin(x)\, dx \approx 2", color=WHITE)
        title.to_edge(UP)
        registry["title"] = title

        axes = Axes(
            x_range=[0, 3.3, 0.7853981],
            y_range=[0, 1.2, 0.5],
            x_length=8.5,
            y_length=3.6,
            axis_config={"color": GREY, "include_tip": True},
        )
        axes.move_to(np.array([0, 0.1, 0]))
        registry["axes"] = axes

        anim_time_1 = 2.000 * _scale_1
        self.play(Create(axes), run_time=(2.0)*_scale_1)
        self.play(Write(title), run_time=(1.0)*_scale_1)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - (anim_time_1 + 2.0) + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q01_riemann_sum_1781442105/media/audio/Calculate_the_value__533949b815/step_01_4f0555d3.mp3")  # [auto-injected]
        _audio_dur_1 = 5.83  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 2.000))
        curve = axes.plot(lambda t: sin(t), x_range=[0, 3.14159, 0.05], color=TEAL)
        registry["curve"] = curve

        anim_time_2 = 2.000 * _scale_2
        self.play(Create(curve), run_time=(2.0)*_scale_2)
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q01_riemann_sum_1781442105/media/audio/Calculate_the_value__533949b815/step_02_b323ec26.mp3")  # [auto-injected]
        _audio_dur_2 = 8.35  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 2.000))
        rects_4 = axes.get_riemann_rectangles(
            curve,
            x_range=[0, 3.14159],
            dx=0.785398,
            input_sample_type="right",
            stroke_width=0.5,
            fill_opacity=0.6,
            color=[BLUE, YELLOW],
        )
        registry["rects_4"] = rects_4

        n_label = MathTex("n = 4", color=ORANGE)
        n_label.next_to(title, RIGHT, buff=0.6)
        registry["n_label"] = n_label

        sum_label = MathTex("S_4 = 1.8961", color=YELLOW)
        sum_label.move_to(np.array([0, -2.2, 0]))
        registry["sum_label"] = sum_label

        anim_time_3 = 2.000 * _scale_3
        self.play(Create(rects_4), run_time=(2.0)*_scale_3)
        self.play(FadeIn(n_label), FadeIn(sum_label), run_time=(0.8)*_scale_3)
        self.play(Indicate(sum_label, color=YELLOW), run_time=(1.0)*_scale_3)
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - (anim_time_3 + 1.8) + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q01_riemann_sum_1781442105/media/audio/Calculate_the_value__533949b815/step_03_b0abe004.mp3")  # [auto-injected]
        _audio_dur_3 = 7.85  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 2.000))
        rects_8 = axes.get_riemann_rectangles(
            curve,
            x_range=[0, 3.14159],
            dx=0.392699,
            input_sample_type="right",
            stroke_width=0.5,
            fill_opacity=0.6,
            color=[BLUE, YELLOW],
        )
        registry["rects_8"] = rects_8

        n_label_8 = MathTex("n = 8", color=ORANGE).next_to(title, RIGHT, buff=0.6)
        sum_label_8 = MathTex("S_8 = 1.9742", color=YELLOW).move_to(np.array([0, -2.2, 0]))

        anim_time_4 = 2.000 * _scale_4
        self.play(
            ReplacementTransform(rects_4, rects_8),
            ReplacementTransform(n_label, n_label_8),
            ReplacementTransform(sum_label, sum_label_8),
            run_time=(2.0)*_scale_4,
        )
        registry["n_label"] = n_label_8
        registry["sum_label"] = sum_label_8
        self.play(Indicate(n_label_8, color=ORANGE), run_time=(1.0)*_scale_4)
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - (anim_time_4 + 1.0) + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q01_riemann_sum_1781442105/media/audio/Calculate_the_value__533949b815/step_04_c19db3ea.mp3")  # [auto-injected]
        _audio_dur_4 = 12.00  # [audio-sync]
        # Step 5
        rects_16 = axes.get_riemann_rectangles(
            curve,
            x_range=[0, 3.14159],
            dx=0.196350,
            input_sample_type="right",
            stroke_width=0.5,
            fill_opacity=0.6,
            color=[BLUE, YELLOW],
        )
        registry["rects_16"] = rects_16

        rects_32 = axes.get_riemann_rectangles(
            curve,
            x_range=[0, 3.14159],
            dx=0.098175,
            input_sample_type="right",
            stroke_width=0.5,
            fill_opacity=0.6,
            color=[BLUE, YELLOW],
        )
        registry["rects_32"] = rects_32

        n_label_16 = MathTex("n = 16", color=ORANGE).next_to(title, RIGHT, buff=0.6)
        sum_label_16 = MathTex("S_{16} = 1.9936", color=YELLOW).move_to(np.array([0, -2.2, 0]))

        n_label_32 = MathTex("n = 32", color=ORANGE).next_to(title, RIGHT, buff=0.6)
        sum_label_32 = MathTex("S_{32} = 1.9984", color=YELLOW).move_to(np.array([0, -2.2, 0]))

        self.play(
            ReplacementTransform(rects_8, rects_16),
            ReplacementTransform(n_label_8, n_label_16),
            ReplacementTransform(sum_label_8, sum_label_16),
            run_time=1.5,
        )
        self.play(
            ReplacementTransform(rects_16, rects_32),
            ReplacementTransform(n_label_16, n_label_32),
            ReplacementTransform(sum_label_16, sum_label_32),
            run_time=1.5,
        )
        registry["n_label"] = n_label_32
        registry["sum_label"] = sum_label_32
        self.play(Indicate(sum_label_32, color=GREEN), run_time=1.0)
        remaining_5 = max(0.1, _audio_dur_4 - 4.0 + 0.1)
        self.wait(remaining_5)