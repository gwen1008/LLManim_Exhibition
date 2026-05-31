from manim import *
import numpy as np

# [VISUAL REASONING]
# Left half shows Axes + circle + line + intersection dots; right half hosts a
# vertically-stacked algebra column. Each step fills one audio window with a
# single continuous LaggedStart, connecting the discriminant result to the two
# actual intersection points on the circle.

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
        self._instrumentor = SceneInstrumentor(self)
        self._sm = SubtitleManager(self)
        self.set_subtitle = self._sm.show
        graph_center = np.array([-3.3, 0.0, 0.0])
        algebra_center = np.array([3.0, 0.5, 0.0])

        title = Text("Line & Circle Intersection", font_size=38).to_edge(UP)

        axes_main = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4.5,
            y_length=4.5,
        ).move_to(graph_center)

        circle_main = Circle(radius=1.5, color=BLUE).move_to(graph_center)

        line_main = Line(
            start=[-5.55, -0.75, 0],
            end=[-1.05, 2.25, 0],
            color=YELLOW,
        )

        circle_eq_label = MathTex("x^2 + y^2 = 4", font_size=30).next_to(axes_main, DOWN)

        line_eq_label = MathTex("y = x + 1", color=YELLOW, font_size=30).move_to(algebra_center)
        substitution_eq = MathTex("x^2 + (x+1)^2 = 4", font_size=32).move_to(algebra_center)
        quadratic_eq = MathTex("2x^2 + 2x - 3 = 0", font_size=34).move_to(algebra_center)
        discriminant_eq = MathTex(r"\Delta = 2^2 - 4(2)(-3) = 28 > 0", font_size=30).move_to(algebra_center)
        solutions_eq = MathTex(r"x = (-1 \pm \sqrt{7}) / 2", font_size=32).move_to(algebra_center)
        coords_result = MathTex(r"(0.82,\, 1.82),\ (-1.82,\, -0.82)", color=GREEN, font_size=28).next_to(solutions_eq, DOWN)

        dot_A = Dot(point=[-2.68, 1.37, 0], color=RED, radius=0.08)
        dot_B = Dot(point=[-4.67, -0.62, 0], color=RED, radius=0.08)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H03_line_circle_1780237737/media/audio/Find_the_intersectio_a9ac15cb8e/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 8.76  # [audio-sync]
        # Step 1
        self.set_subtitle("我們想找出直線 y = x + 1 與半徑為 2 的圓的交點，先把兩條曲線畫在同一個座標平面上。", run_time=_audio_dur_0)
        anim_time_1 = _audio_dur_0
        self.play(
            LaggedStart(
                Write(title),
                Create(axes_main),
                Create(circle_main),
                Write(circle_eq_label),
                AnimationGroup(Create(line_main), Write(line_eq_label)),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H03_line_circle_1780237737/media/audio/Find_the_intersectio_a9ac15cb8e/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 10.78  # [audio-sync]
        # Step 2
        self.set_subtitle("由於 y = x + 1，把它代入圓方程式，用 x + 1 取代 y，將兩個條件合併成一個只含 x 的方程式。", run_time=_audio_dur_1)
        anim_time_2 = _audio_dur_1
        self.play(
            LaggedStart(
                FadeOut(line_eq_label),
                Write(substitution_eq),
                lag_ratio=0.25,
                run_time=anim_time_2,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H03_line_circle_1780237737/media/audio/Find_the_intersectio_a9ac15cb8e/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 10.39  # [audio-sync]
        # Step 3
        self.set_subtitle("展開並化簡平方項，方程式整理成 2x² + 2x − 3 = 0，這是一個標準的二次方程式。", run_time=_audio_dur_2)
        anim_time_3 = _audio_dur_2
        quad_rect = SurroundingRectangle(quadratic_eq, color=BLUE)
        self.play(
            LaggedStart(
                FadeOut(substitution_eq),
                Write(quadratic_eq),
                Create(quad_rect),
                lag_ratio=0.25,
                run_time=anim_time_3,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H03_line_circle_1780237737/media/audio/Find_the_intersectio_a9ac15cb8e/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 9.10  # [audio-sync]
        # Step 4
        self.set_subtitle("計算判別式得到二十八，是正數，所以直線恰好與圓相交於兩個相異的交點。", run_time=_audio_dur_3)
        anim_time_4 = _audio_dur_3
        self.play(
            LaggedStart(
                AnimationGroup(FadeOut(quadratic_eq), FadeOut(quad_rect)),
                Write(discriminant_eq),
                FadeIn(dot_A),
                FadeIn(dot_B),
                lag_ratio=0.25,
                run_time=anim_time_4,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H03_line_circle_1780237737/media/audio/Find_the_intersectio_a9ac15cb8e/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 9.89  # [audio-sync]
        # Step 5
        self.set_subtitle("解這個二次方程式得到 x = (−1 ± √7) / 2，求出在圓上標記出來的兩個交點座標。", run_time=_audio_dur_4)
        anim_time_5 = _audio_dur_4
        coords_rect = SurroundingRectangle(coords_result, color=GREEN)
        self.play(
            LaggedStart(
                FadeOut(discriminant_eq),
                Write(solutions_eq),
                Write(coords_result),
                AnimationGroup(Indicate(dot_A), Indicate(dot_B), Create(coords_rect)),
                lag_ratio=0.25,
                run_time=anim_time_5,
            )
        )
        self.wait(0.1)
