from manim import *

# [VISUAL REASONING]
# Split-screen design: algebra column on the left (x≈-3.5), parabola graph on the right (x≈3.2).
# Each equation morphs in-place via ReplacementTransform so equations never stack.
# Graphical features (vertex, roots) mirror the algebraic results to bind algebraic and visual meaning.
# Signal actions (Indicate, Circumscribe) are hardcoded inline exactly as the Director specified.

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
        title = Text("Completing the Square", color=WHITE, font_size=36).to_edge(UP)

        eq0 = MathTex("x^2-6x+5=0", color=WHITE, font_size=40).move_to([-3.5, 0.8, 0])
        eq1 = MathTex("x^2-6x=-5", color=WHITE, font_size=40).move_to([-3.5, 0.8, 0])
        eq2 = MathTex("x^2-6x+9=-5+9", color=WHITE, font_size=36).move_to([-3.5, 0.8, 0])
        eq3 = MathTex("(x-3)^2=4", color=GREEN, font_size=42).move_to([-3.5, 0.8, 0])
        eq4 = MathTex("x-3=\\pm 2", color=WHITE, font_size=40).move_to([-3.5, 0.8, 0])
        eq5 = MathTex("x=1 \\quad x=5", color=RED, font_size=42).move_to([-3.5, 0.8, 0])

        axes = Axes(
            x_range=[-1, 7, 1],
            y_range=[-5, 5, 1],
            x_length=5.0,
            y_length=4.0,
            axis_config={"color": GREY, "include_tip": True},
        ).move_to([3.2, -0.2, 0])

        parabola = axes.plot(lambda x: x**2 - 6*x + 5, x_range=[-1, 7], color=BLUE)

        vertex_dot = Dot(point=axes.coords_to_point(3, -4), color=YELLOW, radius=0.08)
        vertex_label = MathTex("(3,-4)", color=YELLOW, font_size=28).next_to(vertex_dot, DOWN, buff=0.15)

        root_dot1 = Dot(point=axes.coords_to_point(1, 0), color=RED, radius=0.08)
        root_dot2 = Dot(point=axes.coords_to_point(5, 0), color=RED, radius=0.08)
        roots_label = MathTex("x=1,\\; x=5", color=RED, font_size=28).next_to(root_dot2, UR, buff=0.15)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H01_complete_square_1780228505/media/audio/Solve_the_quadratic__786f35833a/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 6.17  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.500)
        anim_time_1 = 1.500 * _scale_1
        self.play(Write(title), run_time=0.8)
        self.play(Write(eq0), run_time=anim_time_1)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 - 0.8 + 0.1)
        self.set_subtitle("我們從二次方程式 x 平方減六 x 加五等於零開始。", run_time=_audio_dur_0)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H01_complete_square_1780228505/media/audio/Solve_the_quadratic__786f35833a/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 4.68  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 1.800)
        self.set_subtitle("將常數項移到右邊，孤立含 x 的項。", run_time=_audio_dur_1)
        self.play(Indicate(eq0, color=YELLOW), run_time=(0.8)*_scale_2)
        anim_time_2 = 1.800 * _scale_2
        self.play(ReplacementTransform(eq0, eq1), run_time=anim_time_2)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 - 0.8 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H01_complete_square_1780228505/media/audio/Solve_the_quadratic__786f35833a/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 6.34  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 1.800)
        self.set_subtitle("兩邊各加九，因為六的一半平方等於九，以完成平方。", run_time=_audio_dur_2)
        anim_time_3 = 1.800 * _scale_3
        self.play(ReplacementTransform(eq1, eq2), run_time=anim_time_3)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H01_complete_square_1780228505/media/audio/Solve_the_quadratic__786f35833a/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.14  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 1.800)
        self.set_subtitle("左邊現在是一個完全平方，得到 x 減三的平方等於四。", run_time=_audio_dur_3)
        anim_time_4 = 1.800 * _scale_4
        self.play(ReplacementTransform(eq2, eq3), run_time=anim_time_4)
        self.play(Circumscribe(eq3, color=GREEN), run_time=1.0)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 - 1.0 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H01_complete_square_1780228505/media/audio/Solve_the_quadratic__786f35833a/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 8.83  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 1.500)
        self.set_subtitle("同時，拋物線 y 等於 x 平方減六 x 加五開口向上，頂點在三，負四。", run_time=_audio_dur_4)
        anim_time_5 = 1.500 * _scale_5
        self.play(Create(axes), run_time=anim_time_5)
        self.play(Create(parabola), run_time=1.2)
        self.play(FadeIn(vertex_dot), Write(vertex_label), run_time=0.8)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.2 - 0.8 + 0.1)
        self.wait(remaining_5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H01_complete_square_1780228505/media/audio/Solve_the_quadratic__786f35833a/step_05.mp3")  # [auto-injected]
        _audio_dur_5 = 6.10  # [audio-sync]
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 1.800)
        self.set_subtitle("對兩邊取平方根，得到 x 減三等於正負二。", run_time=_audio_dur_5)
        anim_time_6 = 1.800 * _scale_6
        self.play(ReplacementTransform(eq3, eq4), run_time=anim_time_6)
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 + 0.1)
        self.wait(remaining_6)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_H01_complete_square_1780228505/media/audio/Solve_the_quadratic__786f35833a/step_06.mp3")  # [auto-injected]
        _audio_dur_6 = 7.68  # [audio-sync]
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 1.800)
        self.set_subtitle("所以兩個根是 x 等於一和 x 等於五，正好是拋物線與 x 軸的交點。", run_time=_audio_dur_6)
        anim_time_7 = 1.800 * _scale_7
        self.play(ReplacementTransform(eq4, eq5), run_time=anim_time_7)
        self.play(LaggedStart(FadeIn(root_dot1), FadeIn(root_dot2), Write(roots_label), lag_ratio=0.2), run_time=1.2)
        self.play(Indicate(root_dot1, color=RED), run_time=0.8)
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 - 1.2 - 0.8 + 0.1)
        self.wait(remaining_7)