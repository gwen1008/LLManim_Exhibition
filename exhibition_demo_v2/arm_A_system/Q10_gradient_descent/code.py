from manim import *

# [VISUAL REASONING]
# Gradient descent is shown by overlaying the iterate trajectory on the level sets
# it descends. Elongated ellipses (x^2+2y^2=c) plus a visible zigzag explain why the
# steeper y-direction converges faster than x. A faint NumberPlane keeps dots and
# arrows readable; gradient formula sits top, convergence note bottom.

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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_gradient_d_2fb906c3d9/step_00.mp3")  # [auto-injected] duration=6.26s
        _audio_dur_0 = 6.26  # [audio-sync] actual TTS duration
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.500)
        title = Text("Gradient Descent on f(x,y)=x^2+2y^2", color=WHITE, font_size=34)
        title.to_edge(UP)
        anim_time_1 = 1.500 * _scale_1
        self.play(Write(title), run_time=anim_time_1)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_gradient_d_2fb906c3d9/step_01.mp3")  # [auto-injected] duration=4.58s
        _audio_dur_1 = 4.58  # [audio-sync] actual TTS duration
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 1.500)
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_color": GREY, "stroke_opacity": 0.3},
        )
        plane.move_to(ORIGIN)
        anim_time_2 = 1.500 * _scale_2
        self.play(Create(plane), run_time=anim_time_2)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_gradient_d_2fb906c3d9/step_02.mp3")  # [auto-injected] duration=6.79s
        _audio_dur_2 = 6.79  # [audio-sync] actual TTS duration
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.000)
        ellipse1 = Ellipse(width=4.0, height=2.83, color=TEAL, fill_opacity=0.0).move_to(ORIGIN)
        ellipse2 = Ellipse(width=5.66, height=4.0, color=BLUE, fill_opacity=0.0).move_to(ORIGIN)
        ellipse3 = Ellipse(width=6.93, height=4.9, color=PURPLE, fill_opacity=0.0).move_to(ORIGIN)
        anim_time_3 = 2.000 * _scale_3
        self.play(
            LaggedStart(
                Create(ellipse1),
                Create(ellipse2),
                Create(ellipse3),
                lag_ratio=0.2,
            ),
            run_time=anim_time_3,
        )
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_gradient_d_2fb906c3d9/step_03.mp3")  # [auto-injected] duration=5.42s
        _audio_dur_3 = 5.42  # [audio-sync] actual TTS duration
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 1.500)
        grad_label = MathTex("\\nabla f = (2x,\\, 4y)", color=YELLOW, font_size=40)
        grad_label.to_corner(UR, buff=0.5)
        anim_time_4 = 1.500 * _scale_4
        self.play(Write(grad_label), run_time=anim_time_4)
        self.play(Circumscribe(grad_label, color=YELLOW))
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_gradient_d_2fb906c3d9/step_04.mp3")  # [auto-injected] duration=4.42s
        _audio_dur_4 = 4.42  # [audio-sync] actual TTS duration
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 1.000)
        dot_start = Dot(point=ORIGIN, color=RED, radius=0.1).move_to(ORIGIN + np.array([3, 2, 0]))
        start_label = MathTex("(3,2)", color=RED, font_size=30)
        start_label.next_to(dot_start, UR, buff=0.15)
        anim_time_5 = 1.000 * _scale_5
        self.play(Create(dot_start), FadeIn(start_label), run_time=anim_time_5)
        self.play(Indicate(dot_start, color=RED))
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_5))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_gradient_d_2fb906c3d9/step_05.mp3")  # [auto-injected] duration=6.24s
        _audio_dur_5 = 6.24  # [audio-sync] actual TTS duration
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 1.500)
        dir_label = MathTex("-\\nabla f = (-6,-8)", color=GREEN, font_size=32)
        dir_label.to_corner(UL, buff=0.5)
        anim_time_6 = 1.500 * _scale_6
        self.play(Write(dir_label), run_time=anim_time_6)
        self.play(Indicate(dir_label, color=GREEN))
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_6))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_gradient_d_2fb906c3d9/step_06.mp3")  # [auto-injected] duration=6.84s
        _audio_dur_6 = 6.84  # [audio-sync] actual TTS duration
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 1.500)
        descent_arrow = Arrow(start=[3, 2, 0], end=[2.4, 1.2, 0], color=GREEN, buff=0)
        dot1 = Dot(point=ORIGIN, color=ORANGE, radius=0.08).move_to(ORIGIN + np.array([2.4, 1.2, 0]))
        anim_time_7 = 1.500 * _scale_7
        self.play(GrowArrow(descent_arrow), run_time=anim_time_7 * 0.6)
        self.play(Create(dot1), run_time=anim_time_7 * 0.4)
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 + 0.1)
        self.wait(max(0.1, remaining_7))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_gradient_d_2fb906c3d9/step_07.mp3")  # [auto-injected] duration=5.62s
        _audio_dur_7 = 5.62  # [audio-sync] actual TTS duration
        # Step 8
        _scale_8 = max(1.0, (_audio_dur_7 * 0.7) / 1.500)
        dot2 = Dot(point=ORIGIN, color=ORANGE, radius=0.08).move_to(ORIGIN + np.array([1.92, 0.72, 0]))
        dot4 = Dot(point=ORIGIN, color=ORANGE, radius=0.08).move_to(ORIGIN + np.array([1.23, 0.26, 0]))
        seg1 = Line(dot1.get_center(), dot2.get_center(), color=GREEN, stroke_width=3)
        seg2 = Line(dot2.get_center(), dot4.get_center(), color=GREEN, stroke_width=3)
        self.play(FadeOut(dir_label))
        anim_time_8 = 1.500 * _scale_8
        self.play(
            LaggedStart(
                Create(seg1),
                Create(dot2),
                Create(seg2),
                Create(dot4),
                lag_ratio=0.15,
            ),
            run_time=anim_time_8,
        )
        remaining_8 = max(0.1, _audio_dur_7 - anim_time_8 + 0.1)
        self.wait(max(0.1, remaining_8))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_gradient_d_2fb906c3d9/step_08.mp3")  # [auto-injected] duration=5.81s
        _audio_dur_8 = 5.81  # [audio-sync] actual TTS duration
        # Step 9
        _scale_9 = max(1.0, (_audio_dur_8 * 0.7) / 1.500)
        dot6 = Dot(point=ORIGIN, color=ORANGE, radius=0.08).move_to(ORIGIN + np.array([0.79, 0.093, 0]))
        seg3 = Line(dot4.get_center(), dot6.get_center(), color=GREEN, stroke_width=3)
        anim_time_9 = 1.500 * _scale_9
        self.play(Create(seg3), Create(dot6), run_time=anim_time_9)
        self.play(Indicate(dot4, color=ORANGE))
        remaining_9 = max(0.1, _audio_dur_8 - anim_time_9 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_9))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_gradient_d_2fb906c3d9/step_09.mp3")  # [auto-injected] duration=6.17s
        _audio_dur_9 = 6.17  # [audio-sync] actual TTS duration
        # Step 10
        _scale_10 = max(1.0, (_audio_dur_9 * 0.7) / 2.000)
        conv_note = Text(
            "y converges faster than x: its coefficient (4) is larger",
            color=YELLOW,
            font_size=26,
        )
        conv_note.move_to([0, -2.2, 0])
        anim_time_10 = 2.000 * _scale_10
        self.play(Write(conv_note), run_time=anim_time_10)
        remaining_10 = max(0.1, _audio_dur_9 - anim_time_10 + 0.1)
        self.wait(max(0.1, remaining_10))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_gradient_d_2fb906c3d9/step_10.mp3")  # [auto-injected] duration=6.77s
        _audio_dur_10 = 6.77  # [audio-sync] actual TTS duration
        # Step 11
        _scale_11 = max(1.0, (_audio_dur_10 * 0.7) / 1.500)
        dot_final = Dot(point=ORIGIN, color=GREEN, radius=0.1).move_to(ORIGIN + np.array([0.4, 0.02, 0]))
        seg4 = Line(dot6.get_center(), dot_final.get_center(), color=GREEN, stroke_width=3)
        grad_zero_label = MathTex("\\nabla f \\approx 0", color=GREEN, font_size=30)
        grad_zero_label.next_to(dot_final, DOWN, buff=0.2)
        anim_time_11 = 1.500 * _scale_11
        self.play(Create(seg4), Create(dot_final), Write(grad_zero_label), run_time=anim_time_11)
        self.play(Indicate(dot_final, color=GREEN))
        remaining_11 = max(0.1, _audio_dur_10 - anim_time_11 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_11))