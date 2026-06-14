from manim import *

# [VISUAL REASONING]
# Left panel: circle x^2+y^2=4 and line y=x+1 on coordinate axes.
# Right panel: algebraic derivation morphing in-place.
# Intersection dots appear only after the roots are produced.

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

        title = Text("Line meets Circle", color=WHITE, font_size=36)
        title.to_edge(UP)
        registry["title"] = title

        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=4,
            y_length=4,
            axis_config={"color": GREY},
        )
        axes.move_to([-3.5, 0, 0])
        registry["axes"] = axes

        circle = Circle(radius=2, color=BLUE, stroke_width=4)
        circle.move_to(axes.get_origin())
        registry["circle"] = circle

        line = Line(start=[-6.3, -1.8, 0], end=[-2.3, 2.2, 0], color=YELLOW, stroke_width=4)
        registry["line"] = line

        dot1 = Dot(point=[-2.68, 1.82, 0], color=RED, radius=0.09)
        registry["dot1"] = dot1

        dot2 = Dot(point=[-5.32, -0.82, 0], color=RED, radius=0.09)
        registry["dot2"] = dot2

        label1 = MathTex(r"(0.82,\,1.82)", color=RED).scale(0.6)
        label1.next_to(dot1, UR, buff=0.1)
        registry["label1"] = label1

        label2 = MathTex(r"(-1.82,\,-0.82)", color=RED).scale(0.6)
        label2.next_to(dot2, DL, buff=0.1)
        registry["label2"] = label2

        eq_given = MathTex(r"x^2 + y^2 = 4, \quad y = x + 1", color=WHITE)
        eq_given.move_to([3.0, 1.6, 0])
        registry["eq_given"] = eq_given

        eq_sub = MathTex(r"2x^2 + 2x - 3 = 0", color=WHITE)
        eq_sub.move_to([3.0, 0.4, 0])
        registry["eq_sub"] = eq_sub

        eq_disc = MathTex(r"\Delta = 4 - 4(2)(-3) = 28 > 0", color=GREEN)
        eq_disc.move_to([3.0, 0.4, 0])
        registry["eq_disc"] = eq_disc

        # Avoid \frac entirely (repeatedly failed). Use inline parenthesised division.
        eq_roots = MathTex(r"x = (-1 \pm \sqrt{7}) \, / \, 2", color=YELLOW)
        eq_roots.move_to([3.0, -0.9, 0])
        registry["eq_roots"] = eq_roots

        self.add(title)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H03_line_circle_1781441087/media/audio/Find_the_intersectio_108f0da34f/step_00_835b5e3e.mp3")  # [auto-injected]
        _audio_dur_0 = 5.98  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 1.500))
        self.set_subtitle("我們想找直線 y 等於 x 加一 與半徑為二的圓相交的位置。", run_time=_audio_dur_0)
        anim_time_1 = 1.500 * _scale_1
        self.play(Create(axes), run_time=(1.5)*_scale_1)
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - anim_time_1 + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H03_line_circle_1781441087/media/audio/Find_the_intersectio_108f0da34f/step_01_d6da2ca7.mp3")  # [auto-injected]
        _audio_dur_1 = 4.87  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 3.000))
        self.set_subtitle("這裡把圓和直線一起畫在平面上。", run_time=_audio_dur_1)
        anim_time_2 = 3.000 * _scale_2
        self.play(Create(circle), run_time=(1.5)*_scale_2)
        self.play(Create(line), run_time=(1.5)*_scale_2)
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H03_line_circle_1781441087/media/audio/Find_the_intersectio_108f0da34f/step_02_b582d5bd.mp3")  # [auto-injected]
        _audio_dur_2 = 8.23  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 3.000))
        self.set_subtitle("把直線代入圓方程式，得到二次式 2x 平方加 2x 減 3 等於零。", run_time=_audio_dur_2)
        anim_time_3 = 3.000 * _scale_3
        self.play(Write(eq_given), run_time=(2.0)*_scale_3)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        self.play(Write(eq_sub), run_time=(1.0)*_scale_3)
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H03_line_circle_1781441087/media/audio/Find_the_intersectio_108f0da34f/step_03_7dde20f1.mp3")  # [auto-injected]
        _audio_dur_3 = 7.49  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 3.000))
        self.set_subtitle("判別式等於二十八，是正數，所以恰好有兩個交點。", run_time=_audio_dur_3)
        anim_time_4 = 3.000 * _scale_4
        self.play(ReplacementTransform(eq_sub, eq_disc), run_time=(2.0)*_scale_4)
        self.play(Indicate(eq_disc, color=GREEN), run_time=(1.0)*_scale_4)
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H03_line_circle_1781441087/media/audio/Find_the_intersectio_108f0da34f/step_04_56c50fce.mp3")  # [auto-injected]
        _audio_dur_4 = 8.30  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 4.000))
        self.set_subtitle("解得 x 等於負一加減根號七再除以二，標出兩個交點。", run_time=_audio_dur_4)
        anim_time_5 = 4.000 * _scale_5
        self.play(Write(eq_roots), run_time=(2.0)*_scale_5)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        self.play(
            LaggedStart(
                FadeIn(dot1), FadeIn(label1), FadeIn(dot2), FadeIn(label2),
                lag_ratio=0.2,
            ),
            run_time=(1.0)*_scale_5,
        )
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - anim_time_5 + 0.1))
        self.wait(remaining_5)