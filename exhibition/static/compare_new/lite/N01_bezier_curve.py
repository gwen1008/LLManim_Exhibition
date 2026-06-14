from manim import *
import numpy as np

# [VISUAL REASONING]
# De Casteljau is recursive interpolation collapsing to one point. A single
# t_tracker (ValueTracker) drives every intermediate point via always_redraw
# lerps of the layer below, giving continuous recursion without jump cuts.
# Layer 0: P0..P3 fixed. Layer 1 (blue): A,B,C. Layer 2 (green): D,E.
# Layer 3 (yellow): segment DE with red curve point F that traces the Bezier.

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
        P0 = np.array([-5.0, -1.5, 0])
        P1 = np.array([-3.0, 1.6, 0])
        P2 = np.array([2.5, 1.8, 0])
        P3 = np.array([5.0, -1.0, 0])

        def lerp(a, b, t):
            return a + (b - a) * t

        t_tracker = ValueTracker(0.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N01_bezier_curve_1780053268/media/audio/Using_the_de_Castelj_8f7e2e3aa8/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 9.41  # [audio-sync]
        # Step 1
        title = Text("De Casteljau Algorithm: Cubic Bezier", font_size=34).to_edge(UP)

        dot_P0 = Dot(point=P0, radius=0.09, color=WHITE)
        dot_P1 = Dot(point=P1, radius=0.09, color=WHITE)
        dot_P2 = Dot(point=P2, radius=0.09, color=WHITE)
        dot_P3 = Dot(point=P3, radius=0.09, color=WHITE)

        lbl_P0 = MathTex("P_0", font_size=30).next_to(dot_P0, DOWN, buff=0.15)
        lbl_P1 = MathTex("P_1", font_size=30).next_to(dot_P1, UP, buff=0.15)
        lbl_P2 = MathTex("P_2", font_size=30).next_to(dot_P2, UP, buff=0.15)
        lbl_P3 = MathTex("P_3", font_size=30).next_to(dot_P3, DOWN, buff=0.15)

        control_polygon = VGroup(
            Line(P0, P1, color=GREY),
            Line(P1, P2, color=GREY),
            Line(P2, P3, color=GREY),
        )

        self.set_subtitle("我們從四個控制點 P0 到 P3 開始，依序連接它們，形成決定三次貝茲曲線形狀的控制多邊形。", run_time=_audio_dur_0)
        anim_time_1 = _audio_dur_0
        self.play(
            LaggedStart(
                Write(title),
                AnimationGroup(FadeIn(dot_P0), Write(lbl_P0)),
                AnimationGroup(FadeIn(dot_P1), Write(lbl_P1)),
                AnimationGroup(FadeIn(dot_P2), Write(lbl_P2)),
                AnimationGroup(FadeIn(dot_P3), Write(lbl_P3)),
                Create(control_polygon),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N01_bezier_curve_1780053268/media/audio/Using_the_de_Castelj_8f7e2e3aa8/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 9.82  # [audio-sync]
        # Step 2
        def get_A():
            return lerp(P0, P1, t_tracker.get_value())

        def get_B():
            return lerp(P1, P2, t_tracker.get_value())

        def get_C():
            return lerp(P2, P3, t_tracker.get_value())

        layer1_lines = always_redraw(lambda: VGroup(
            Line(P0, P1, color=BLUE),
            Line(P1, P2, color=BLUE),
            Line(P2, P3, color=BLUE),
        ))
        dot_A = always_redraw(lambda: Dot(point=get_A(), radius=0.08, color=BLUE))
        dot_B = always_redraw(lambda: Dot(point=get_B(), radius=0.08, color=BLUE))
        dot_C = always_redraw(lambda: Dot(point=get_C(), radius=0.08, color=BLUE))

        lbl_A = MathTex("A", font_size=28, color=BLUE)
        lbl_A.add_updater(lambda m: m.next_to(get_A(), LEFT, buff=0.12))
        lbl_B = MathTex("B", font_size=28, color=BLUE)
        lbl_B.add_updater(lambda m: m.next_to(get_B(), UP, buff=0.12))
        lbl_C = MathTex("C", font_size=28, color=BLUE)
        lbl_C.add_updater(lambda m: m.next_to(get_C(), RIGHT, buff=0.12))

        t_readout = VGroup(
            MathTex("t = ", font_size=36),
            DecimalNumber(0, num_decimal_places=2, font_size=36),
        ).arrange(RIGHT, buff=0.1).move_to([0, -2.0, 0])
        t_readout[1].add_updater(lambda m: m.set_value(t_tracker.get_value()))

        self.set_subtitle("對於固定的 t，我們沿著每條多邊形邊做線性內插，產生三個新的點 A、B 和 C，它們會隨 t 改變而滑動。", run_time=_audio_dur_1)
        anim_time_2 = _audio_dur_1
        self.play(
            LaggedStart(
                Create(layer1_lines),
                AnimationGroup(FadeIn(dot_A), FadeIn(dot_B), FadeIn(dot_C)),
                FadeIn(t_readout),
                AnimationGroup(Write(lbl_A), Write(lbl_B), Write(lbl_C)),
                t_tracker.animate.set_value(0.4),
                lag_ratio=0.25,
                run_time=anim_time_2,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N01_bezier_curve_1780053268/media/audio/Using_the_de_Castelj_8f7e2e3aa8/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 9.74  # [audio-sync]
        # Step 3
        def get_D():
            return lerp(get_A(), get_B(), t_tracker.get_value())

        def get_E():
            return lerp(get_B(), get_C(), t_tracker.get_value())

        def get_F():
            return lerp(get_D(), get_E(), t_tracker.get_value())

        layer2_lines = always_redraw(lambda: VGroup(
            Line(get_A(), get_B(), color=GREEN),
            Line(get_B(), get_C(), color=GREEN),
        ))
        dot_D = always_redraw(lambda: Dot(point=get_D(), radius=0.08, color=GREEN))
        dot_E = always_redraw(lambda: Dot(point=get_E(), radius=0.08, color=GREEN))
        lbl_D = MathTex("D", font_size=28, color=GREEN)
        lbl_D.add_updater(lambda m: m.next_to(get_D(), LEFT, buff=0.12))
        lbl_E = MathTex("E", font_size=28, color=GREEN)
        lbl_E.add_updater(lambda m: m.next_to(get_E(), RIGHT, buff=0.12))

        layer3_segment = always_redraw(lambda: Line(get_D(), get_E(), color=YELLOW))
        curve_point = always_redraw(lambda: Dot(point=get_F(), radius=0.11, color=RED))
        lbl_F = MathTex("B(t)", font_size=28, color=RED)
        lbl_F.add_updater(lambda m: m.next_to(get_F(), UP, buff=0.15))

        self.set_subtitle("我們進行遞迴：沿著 A-B 與 B-C 內插得到 D 和 E，再沿 D-E 做最後一次內插，得到曲線上的單一點。", run_time=_audio_dur_2)
        anim_time_3 = _audio_dur_2
        self.play(
            LaggedStart(
                Create(layer2_lines),
                AnimationGroup(FadeIn(dot_D), FadeIn(dot_E)),
                AnimationGroup(Write(lbl_D), Write(lbl_E)),
                Create(layer3_segment),
                FadeIn(curve_point),
                Write(lbl_F),
                lag_ratio=0.25,
                run_time=anim_time_3,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N01_bezier_curve_1780053268/media/audio/Using_the_de_Castelj_8f7e2e3aa8/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 9.79  # [audio-sync]
        # Step 4
        def bezier(t):
            return ((1 - t) ** 3) * P0 + 3 * ((1 - t) ** 2) * t * P1 \
                + 3 * (1 - t) * (t ** 2) * P2 + (t ** 3) * P3

        bezier_curve = TracedPath(curve_point.get_center, stroke_color=RED, stroke_width=4)
        self.add(bezier_curve)

        self.set_subtitle("現在讓 t 從零連續掃到一；遞迴構造平滑移動，紅色的點便描繪出整條貝茲曲線。", run_time=_audio_dur_3)
        anim_time_4 = _audio_dur_3
        self.play(
            t_tracker.animate.set_value(1.0),
            run_time=anim_time_4,
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N01_bezier_curve_1780053268/media/audio/Using_the_de_Castelj_8f7e2e3aa8/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 8.71  # [audio-sync]
        # Step 5
        static_curve = ParametricFunction(bezier, t_range=[0, 1, 0.01], color=RED)
        self.remove(bezier_curve)
        self.add(static_curve)

        formula = MathTex(
            "B(t)=(1-t)^3P_0+3(1-t)^2tP_1+3(1-t)t^2P_2+t^3P_3",
            font_size=30,
        ).move_to([0, -2.3, 0])

        self.set_subtitle("把遞迴用代數方式收合，便得到伯恩斯坦形式，顯示曲線是四個控制點在所有 t 上的加權混合。", run_time=_audio_dur_4)
        anim_time_5 = _audio_dur_4
        self.play(
            LaggedStart(
                FadeOut(layer1_lines, dot_A, dot_B, dot_C, lbl_A, lbl_B, lbl_C),
                FadeOut(layer2_lines, dot_D, dot_E, lbl_D, lbl_E),
                FadeOut(layer3_segment, t_readout),
                Write(formula),
                Indicate(formula, color=YELLOW),
                lag_ratio=0.25,
                run_time=anim_time_5,
            )
        )
        self.wait(0.1)