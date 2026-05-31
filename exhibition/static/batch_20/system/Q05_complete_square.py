# [VISUAL REASONING]
# Pair algebraic completing-the-square with geometric vertex visualization.
# Left half: axes + parabola. Right half: equation morphing at eq_anchor.
# Vertex (3,-4) and axis of symmetry x=3 revealed after vertex form.

from manim import *


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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q05_complete_square_1779986807/media/audio/_final_translation___375556a503/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 7.42  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 3.500)
        title = Text("配方法：y = x² − 6x + 5", color=WHITE, font_size=34)
        title.to_edge(UP, buff=0.4)

        axes = Axes(
            x_range=[-1, 7, 1],
            y_range=[-5, 6, 1],
            x_length=5.0,
            y_length=4.2,
            axis_config={"color": GREY, "include_tip": False},
        ).move_to(np.array([-3.5, 0.0, 0]))

        parabola = axes.plot(lambda t: t * t - 6 * t + 5, x_range=[0.5, 5.5], color=BLUE)

        eq_step1 = MathTex("y = x^2 - 6x + 5", color=WHITE).move_to(np.array([3.2, 1.5, 0]))

        self.set_subtitle("我們從二次式 y 等於 x 平方減六 x 加五 開始，並畫出它的拋物線。", run_time=_audio_dur_0)
        anim_time_1 = 3.500 * _scale_1
        self.play(Write(title), run_time=1.0)
        self.play(Create(axes), run_time=2.0)
        self.play(Create(parabola), Write(eq_step1), run_time=1.5)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q05_complete_square_1779986807/media/audio/_final_translation___375556a503/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 5.76  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 3.500)
        eq_step2 = MathTex("y = (x^2 - 6x + 9) - 9 + 5", color=WHITE).move_to(np.array([3.2, 1.5, 0]))

        self.set_subtitle("把負六的一半得到負三，再平方得到九。", run_time=_audio_dur_1)
        anim_time_2 = 3.500 * _scale_2
        self.play(Circumscribe(eq_step1, color=YELLOW), run_time=1.5)
        self.play(TransformMatchingTex(eq_step1, eq_step2), run_time=2.0)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q05_complete_square_1779986807/media/audio/_final_translation___375556a503/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 5.95  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.000)
        eq_step3 = MathTex("y = (x - 3)^2 - 4", color=YELLOW).move_to(np.array([3.2, 1.5, 0]))

        self.set_subtitle("前三項組成完全平方，剩下常數負四。", run_time=_audio_dur_2)
        anim_time_3 = 2.000 * _scale_3
        self.play(TransformMatchingTex(eq_step2, eq_step3), run_time=2.0)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q05_complete_square_1779986807/media/audio/_final_translation___375556a503/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.79  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 3.000)
        vertex_dot = Dot(point=axes.c2p(3, -4), color=RED, radius=0.09)
        vertex_label = MathTex("(3,\\ -4)", color=RED, font_size=32).next_to(vertex_dot, DOWN, buff=0.2)

        self.set_subtitle("頂點式揭示頂點在三、負四，是拋物線的最低點。", run_time=_audio_dur_3)
        anim_time_4 = 3.000 * _scale_4
        self.play(Indicate(eq_step3, color=RED), run_time=1.5)
        self.play(Create(vertex_dot), Write(vertex_label), run_time=1.5)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q05_complete_square_1779986807/media/audio/_final_translation___375556a503/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.38  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.500)
        axis_sym = DashedLine(
            start=axes.c2p(3, -5),
            end=axes.c2p(3, 6),
            color=GREEN,
        )
        axis_label = MathTex("x = 3", color=GREEN, font_size=30).next_to(axis_sym, UP, buff=0.1)

        self.set_subtitle("拋物線對稱於 x 等於三 這條垂直線，也就是對稱軸。", run_time=_audio_dur_4)
        anim_time_5 = 2.500 * _scale_5
        self.play(Create(axis_sym), run_time=2.0)
        self.play(Write(axis_label), run_time=0.5)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)