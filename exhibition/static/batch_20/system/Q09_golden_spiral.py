# [VISUAL REASONING]
# A concrete construction of the Golden Spiral: six Fibonacci-sized squares are
# laid out in the classic spiral tiling using ABSOLUTE coordinates (no move_to on
# squares/arcs). Each square's side length is labeled with MathTex placed at its
# given centroid offset. Finally one tangent-continuous quarter-arc is drawn per
# square (smallest to largest) so the golden spiral emerges continuously from the
# squares the viewer just saw. Arc endpoints chain exactly via the given
# start_angle/angle values.

from manim import *
import numpy


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

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q09_golden_spiral_1781378111/media/audio/Draw_a_golden_spiral_bab1eef485/step_00_529da97b.mp3")  # [auto-injected]
        _audio_dur_0 = 6.29  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 1.500))
        title = Text("The Golden Spiral", color=WHITE, font_size=40).to_edge(UP, buff=0.3)
        registry["title"] = title
        anim_time_1 = 1.500 * _scale_1
        self.play(Write(title), run_time=anim_time_1)
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - anim_time_1 + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q09_golden_spiral_1781378111/media/audio/Draw_a_golden_spiral_bab1eef485/step_01_4c202375.mp3")  # [auto-injected]
        _audio_dur_1 = 5.83  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 1.500))
        fib_seq = MathTex(r"1,\ 1,\ 2,\ 3,\ 5,\ 8", color=GOLD, font_size=36)
        fib_seq.move_to(ORIGIN + numpy.array([0, 2.7, 0]))
        registry["fib_seq"] = fib_seq
        anim_time_2 = 1.500 * _scale_2
        self.play(Write(fib_seq), run_time=anim_time_2)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 - 1.0 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q09_golden_spiral_1781378111/media/audio/Draw_a_golden_spiral_bab1eef485/step_02_3836a6e6.mp3")  # [auto-injected]
        _audio_dur_2 = 6.02  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 2.500))
        sq1 = Polygon(
            [1.25, -1, 0], [1.75, -1, 0], [1.75, -0.5, 0], [1.25, -0.5, 0],
            color=BLUE_D, fill_opacity=0.15, stroke_width=3
        )
        sq2 = Polygon(
            [0.75, -1, 0], [1.25, -1, 0], [1.25, -0.5, 0], [0.75, -0.5, 0],
            color=BLUE_D, fill_opacity=0.15, stroke_width=3
        )
        sq3 = Polygon(
            [0.75, -2, 0], [1.75, -2, 0], [1.75, -1, 0], [0.75, -1, 0],
            color=TEAL, fill_opacity=0.15, stroke_width=3
        )
        lbl1 = MathTex("1", color=WHITE, font_size=22).move_to(ORIGIN + numpy.array([1.5, -0.75, 0]))
        lbl2 = MathTex("1", color=WHITE, font_size=22).move_to(ORIGIN + numpy.array([1.0, -0.75, 0]))
        lbl3 = MathTex("2", color=WHITE, font_size=26).move_to(ORIGIN + numpy.array([1.25, -1.5, 0]))
        registry.update({"sq1": sq1, "sq2": sq2, "sq3": sq3, "lbl1": lbl1, "lbl2": lbl2, "lbl3": lbl3})
        anim_time_3 = 2.500 * _scale_3
        self.play(
            LaggedStart(
                AnimationGroup(Create(sq1), Write(lbl1)),
                AnimationGroup(Create(sq2), Write(lbl2)),
                AnimationGroup(Create(sq3), Write(lbl3)),
                lag_ratio=0.2,
            ),
            run_time=anim_time_3,
        )
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q09_golden_spiral_1781378111/media/audio/Draw_a_golden_spiral_bab1eef485/step_03_831f9cc0.mp3")  # [auto-injected]
        _audio_dur_3 = 6.70  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 3.000))
        sq4 = Polygon(
            [1.75, -2, 0], [3.25, -2, 0], [3.25, -0.5, 0], [1.75, -0.5, 0],
            color=TEAL, fill_opacity=0.15, stroke_width=3
        )
        sq5 = Polygon(
            [0.75, -0.5, 0], [3.25, -0.5, 0], [3.25, 2, 0], [0.75, 2, 0],
            color=GREEN, fill_opacity=0.12, stroke_width=3
        )
        sq6 = Polygon(
            [-3.25, -2, 0], [0.75, -2, 0], [0.75, 2, 0], [-3.25, 2, 0],
            color=GREEN, fill_opacity=0.12, stroke_width=3
        )
        lbl4 = MathTex("3", color=WHITE, font_size=30).move_to(ORIGIN + numpy.array([2.5, -1.25, 0]))
        lbl5 = MathTex("5", color=WHITE, font_size=34).move_to(ORIGIN + numpy.array([2.0, 0.75, 0]))
        lbl6 = MathTex("8", color=WHITE, font_size=38).move_to(ORIGIN + numpy.array([-1.25, 0, 0]))
        registry.update({"sq4": sq4, "sq5": sq5, "sq6": sq6, "lbl4": lbl4, "lbl5": lbl5, "lbl6": lbl6})
        anim_time_4 = 3.000 * _scale_4
        self.play(
            LaggedStart(
                AnimationGroup(Create(sq4), Write(lbl4)),
                AnimationGroup(Create(sq5), Write(lbl5)),
                AnimationGroup(Create(sq6), Write(lbl6)),
                lag_ratio=0.2,
            ),
            run_time=anim_time_4,
        )
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q09_golden_spiral_1781378111/media/audio/Draw_a_golden_spiral_bab1eef485/step_04_ae6d4954.mp3")  # [auto-injected]
        _audio_dur_4 = 7.25  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 4.000))
        arc1 = Arc(radius=0.5, arc_center=[1.75, -0.5, 0], start_angle=180 * DEGREES, angle=90 * DEGREES, color=GOLD, stroke_width=6)
        arc2 = Arc(radius=0.5, arc_center=[1.25, -1, 0], start_angle=180 * DEGREES, angle=-90 * DEGREES, color=GOLD, stroke_width=6)
        arc3 = Arc(radius=1.0, arc_center=[1.75, -1, 0], start_angle=270 * DEGREES, angle=-90 * DEGREES, color=GOLD, stroke_width=6)
        arc4 = Arc(radius=1.5, arc_center=[1.75, -0.5, 0], start_angle=0 * DEGREES, angle=-90 * DEGREES, color=GOLD, stroke_width=6)
        arc5 = Arc(radius=2.5, arc_center=[0.75, -0.5, 0], start_angle=90 * DEGREES, angle=-90 * DEGREES, color=GOLD, stroke_width=6)
        arc6 = Arc(radius=4.0, arc_center=[0.75, -2, 0], start_angle=90 * DEGREES, angle=90 * DEGREES, color=GOLD, stroke_width=6)
        registry.update({"arc1": arc1, "arc2": arc2, "arc3": arc3, "arc4": arc4, "arc5": arc5, "arc6": arc6})
        anim_time_5 = 4.000 * _scale_5
        self.play(
            Succession(
                Create(arc1),
                Create(arc2),
                Create(arc3),
                Create(arc4),
                Create(arc5),
                Create(arc6),
            ),
            run_time=anim_time_5,
        )
        self.play(Circumscribe(arc6, color=YELLOW))
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - anim_time_5 - 1.0 + 0.1))
        self.wait(remaining_5)