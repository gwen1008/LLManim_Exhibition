from manim import *

# [VISUAL REASONING]
# Solve the system step-by-step with in-place equation morphing to avoid clutter,
# then confirm visually with a graph showing exactly two intersection points
# predicted by the positive discriminant. Algebra morphs at ORIGIN; FadeOut before
# the compact coordinate graph occupies CONTENT center for verification.

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
        stage = ORIGIN

        title = Text("Line and Circle Intersection", color=WHITE, font_size=36)
        title.to_edge(UP)

        eq_line = MathTex("y = x + 1", color=BLUE).move_to(stage + np.array([-2.5, 0.6, 0]))
        eq_circle = MathTex("x^2 + y^2 = 4", color=GREEN).move_to(stage + np.array([2.0, 0.6, 0]))
        eq_sub = MathTex("x^2 + (x+1)^2 = 4", color=WHITE).move_to(stage + np.array([0, 0, 0]))
        eq_quad = MathTex("2x^2 + 2x - 3 = 0", color=YELLOW).move_to(stage + np.array([0, 0, 0]))
        eq_disc = MathTex(r"\Delta = 2^2 - 4(2)(-3) = 28 > 0", color=ORANGE).move_to(stage + np.array([0, -1.0, 0]))
        two_points_text = Text("Two real solutions = two intersection points", color=WHITE, font_size=28).move_to(stage + np.array([0, -1.9, 0]))
        eq_solve = MathTex(r"x = (-1 \pm \sqrt{7})\,/\,2", color=YELLOW).move_to(stage + np.array([0, 0, 0]))
        coords_text = MathTex(r"(0.82,\,1.82)\quad (-1.82,\,-0.82)", color=WHITE).move_to(stage + np.array([0, -1.2, 0]))

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            axis_config={"color": GREY},
        ).move_to(ORIGIN)

        circle_graph = Circle(radius=1.667, color=GREEN).move_to(ORIGIN)
        line_graph = Line(start=[-2.5, -1.667, 0], end=[1.667, 2.5, 0], color=BLUE)

        dot1 = Dot(point=[0.686, 1.519, 0], color=RED, radius=0.09).move_to(np.array([0.686, 1.519, 0]))
        dot2 = Dot(point=[-1.519, -0.686, 0], color=RED, radius=0.09).move_to(np.array([-1.519, -0.686, 0]))

        label1 = MathTex(r"(0.82,\,1.82)", color=WHITE, font_size=28).next_to(dot1, UR, buff=0.1)
        label2 = MathTex(r"(-1.82,\,-0.82)", color=WHITE, font_size=28).next_to(dot2, DL, buff=0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H03_line_circle_1780229066/media/audio/Find_the_intersectio_479a284229/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 5.74  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 2.500)
        self.set_subtitle("我們要找直線與圓的共同點，所以先列出兩個方程式。", run_time=_audio_dur_0)
        anim_time_1 = 2.500 * _scale_1
        self.play(Write(title), run_time=1.0)
        self.play(LaggedStart(Write(eq_line), Write(eq_circle), lag_ratio=0.4), run_time=1.5)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H03_line_circle_1780229066/media/audio/Find_the_intersectio_479a284229/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 6.91  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.800)
        self.set_subtitle("把 y 等於 x 加一代入圓方程式，消去 y 得到只含 x 的式子。", run_time=_audio_dur_1)
        anim_time_2 = 2.800 * _scale_2
        self.play(Indicate(eq_circle, color=GREEN), run_time=0.8)
        self.play(Write(eq_sub), run_time=2.0)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H03_line_circle_1780229066/media/audio/Find_the_intersectio_479a284229/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 7.82  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.000)
        self.set_subtitle("展開並合併同類項，化簡成二次式 2x 平方加 2x 減 3 等於 0。", run_time=_audio_dur_2)
        anim_time_3 = 2.000 * _scale_3
        self.play(FadeOut(eq_line), FadeOut(eq_circle))
        self.play(TransformMatchingTex(eq_sub, eq_quad), run_time=2.0)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H03_line_circle_1780229066/media/audio/Find_the_intersectio_479a284229/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.79  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 3.000)
        self.set_subtitle("判別式等於二十八，是正的，所以直線與圓交於兩個點。", run_time=_audio_dur_3)
        anim_time_4 = 3.000 * _scale_4
        self.play(Write(eq_disc), run_time=2.0)
        self.play(Circumscribe(eq_disc, color=ORANGE), run_time=1.0)
        self.play(Write(two_points_text), run_time=1.0)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 - 1.0 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H03_line_circle_1780229066/media/audio/Find_the_intersectio_479a284229/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.82  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 3.000)
        self.set_subtitle("解這個二次式，得到 x 等於負一加減根號七，全部除以二。", run_time=_audio_dur_4)
        anim_time_5 = 3.000 * _scale_5
        self.play(FadeOut(eq_disc), FadeOut(two_points_text))
        self.play(TransformMatchingTex(eq_quad, eq_solve), run_time=2.0)
        self.play(Write(coords_text), run_time=1.0)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H03_line_circle_1780229066/media/audio/Find_the_intersectio_479a284229/step_05.mp3")  # [auto-injected]
        _audio_dur_5 = 5.33  # [audio-sync]
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 3.500)
        self.set_subtitle("把圓和直線畫出來，驗證我們剛剛求出的兩個交點。", run_time=_audio_dur_5)
        anim_time_6 = 3.500 * _scale_6
        self.play(FadeOut(eq_solve), FadeOut(coords_text))
        self.play(Create(axes), run_time=1.5)
        self.play(Create(circle_graph), run_time=1.0)
        self.play(Create(line_graph), run_time=1.0)
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 + 0.1)
        self.wait(remaining_6)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H03_line_circle_1780229066/media/audio/Find_the_intersectio_479a284229/step_06.mp3")  # [auto-injected]
        _audio_dur_6 = 5.88  # [audio-sync]
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 3.000)
        self.set_subtitle("兩個紅點標出直線與圓的交會處，正好對應我們算出的座標。", run_time=_audio_dur_6)
        anim_time_7 = 3.000 * _scale_7
        self.play(LaggedStart(GrowFromCenter(dot1), GrowFromCenter(dot2), lag_ratio=0.3), run_time=1.0)
        self.play(LaggedStart(Write(label1), Write(label2), lag_ratio=0.3), run_time=1.0)
        self.play(Indicate(dot1, color=RED), run_time=1.0)
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 + 0.1)
        self.wait(remaining_7)