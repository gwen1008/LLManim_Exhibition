from manim import *

# [VISUAL REASONING]
# The equation is solved through one morphing central anchor: combine logs (product rule),
# convert to exponential form, expand to a quadratic, factor, extract roots, then apply the
# domain constraint to reject the extraneous root x=-2. A single equation stays visible at the
# center and morphs in place via TransformMatchingTex for smooth continuity, while a yellow step
# label sits above and a red domain note anchors the footer. The rejected root is struck through
# in red before the green boxed final answer x=4 is revealed.

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
        title_pos = UP * 2.9
        eq_center = ORIGIN + UP * 0.5
        step_pos = UP * 2.0
        note_pos = DOWN * 2.2

        title = Text("Solving a Logarithmic Equation", color=WHITE, font_size=36).move_to(title_pos)
        eq0 = MathTex(r"\log_2(x) + \log_2(x-2) = 3", color=WHITE).move_to(eq_center)
        eq1 = MathTex(r"\log_2\big(x(x-2)\big) = 3", color=WHITE).move_to(eq_center)
        eq2 = MathTex(r"x(x-2) = 2^{3} = 8", color=WHITE).move_to(eq_center)
        eq3 = MathTex(r"x^2 - 2x - 8 = 0", color=WHITE).move_to(eq_center)
        eq4 = MathTex(r"(x-4)(x+2) = 0", color=WHITE).move_to(eq_center)
        roots = MathTex(r"x = 4 \quad or \quad x = -2", color=WHITE).move_to(eq_center)
        domain_note = Tex(r"Domain: $x>0$ and $x-2>0 \Rightarrow x>2$", color=RED).move_to(note_pos)
        reject_cross = Line(start=[2.3, 0.5, 0], end=[3.6, 0.5, 0], color=RED).move_to(ORIGIN + [3.0, 0.5, 0])
        final_answer = MathTex(r"x = 4", color=GREEN).move_to(eq_center)
        answer_box = SurroundingRectangle(final_answer, color=GREEN, buff=0.25)
        step_label = Text("Step 1: Combine the logarithms", color=YELLOW, font_size=28).move_to(step_pos)

        self.add(title)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1780228804/media/audio/log₂_x____log₂_x_2___ef4b301378/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 7.39  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 2.000)
        self.set_subtitle("我們從對數方程式 log 以 2 為底 x 加上 log 以 2 為底 x 減 2 等於 3 開始。", run_time=_audio_dur_0)
        anim_time_1 = 2.000 * _scale_1
        self.play(Write(eq0), run_time=2.0)
        self.play(Circumscribe(eq0, color=YELLOW))
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 - 1.0 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1780228804/media/audio/log₂_x____log₂_x_2___ef4b301378/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 4.99  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 1.000)
        self.set_subtitle("利用乘積律，對數的和會變成乘積的對數。", run_time=_audio_dur_1)
        anim_time_2 = 1.000 * _scale_2
        self.play(Write(step_label), run_time=1.0)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1780228804/media/audio/log₂_x____log₂_x_2___ef4b301378/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 5.40  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.000)
        self.set_subtitle("所以左邊合併成 log 以 2 為底 x 乘以 x 減 2。", run_time=_audio_dur_2)
        anim_time_3 = 2.000 * _scale_3
        self.play(TransformMatchingTex(eq0, eq1), run_time=2.0)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1780228804/media/audio/log₂_x____log₂_x_2___ef4b301378/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.02  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.000)
        self.set_subtitle("改寫成指數形式，乘積必須等於 2 的 3 次方，也就是 8。", run_time=_audio_dur_3)
        anim_time_4 = 2.000 * _scale_4
        self.play(TransformMatchingTex(eq1, eq2), run_time=2.0)
        self.play(Indicate(eq2, color=RED))
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 - 1.0 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1780228804/media/audio/log₂_x____log₂_x_2___ef4b301378/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 5.06  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        self.set_subtitle("展開並把所有項移到一邊，得到一個標準二次式。", run_time=_audio_dur_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(TransformMatchingTex(eq2, eq3), run_time=2.0)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1780228804/media/audio/log₂_x____log₂_x_2___ef4b301378/step_05.mp3")  # [auto-injected]
        _audio_dur_5 = 5.42  # [audio-sync]
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 2.000)
        self.set_subtitle("這個二次式可以漂亮地因式分解成 x 減 4 乘以 x 加 2。", run_time=_audio_dur_5)
        anim_time_6 = 2.000 * _scale_6
        self.play(TransformMatchingTex(eq3, eq4), run_time=2.0)
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 + 0.1)
        self.wait(remaining_6)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1780228804/media/audio/log₂_x____log₂_x_2___ef4b301378/step_06.mp3")  # [auto-injected]
        _audio_dur_6 = 7.15  # [audio-sync]
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 2.000)
        self.set_subtitle("令每個因式為零，得到兩個候選根，x 等於 4 或 x 等於負 2。", run_time=_audio_dur_6)
        anim_time_7 = 2.000 * _scale_7
        self.play(TransformMatchingTex(eq4, roots), run_time=2.0)
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 + 0.1)
        self.wait(remaining_7)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1780228804/media/audio/log₂_x____log₂_x_2___ef4b301378/step_07.mp3")  # [auto-injected]
        _audio_dur_7 = 6.31  # [audio-sync]
        # Step 8
        _scale_8 = max(1.0, (_audio_dur_7 * 0.7) / 2.000)
        self.set_subtitle("但對數要求引數為正，所以定義域強制 x 大於 2。", run_time=_audio_dur_7)
        anim_time_8 = 2.000 * _scale_8
        self.play(Write(domain_note), run_time=2.0)
        self.play(Circumscribe(domain_note, color=RED))
        remaining_8 = max(0.1, _audio_dur_7 - anim_time_8 - 1.0 + 0.1)
        self.wait(remaining_8)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1780228804/media/audio/log₂_x____log₂_x_2___ef4b301378/step_08.mp3")  # [auto-injected]
        _audio_dur_8 = 5.11  # [audio-sync]
        # Step 9
        _scale_9 = max(1.0, (_audio_dur_8 * 0.7) / 1.500)
        self.set_subtitle("由於負 2 違反定義域，我們將它視為增根而捨去。", run_time=_audio_dur_8)
        anim_time_9 = 1.500 * _scale_9
        self.play(Create(reject_cross), run_time=1.5)
        self.play(Indicate(reject_cross, color=RED))
        remaining_9 = max(0.1, _audio_dur_8 - anim_time_9 - 1.0 + 0.1)
        self.wait(remaining_9)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1780228804/media/audio/log₂_x____log₂_x_2___ef4b301378/step_09.mp3")  # [auto-injected]
        _audio_dur_9 = 4.30  # [audio-sync]
        # Step 10
        _scale_10 = max(1.0, (_audio_dur_9 * 0.7) / 1.500)
        self.set_subtitle("因此唯一有效的解是 x 等於 4。", run_time=_audio_dur_9)
        anim_time_10 = 1.500 * _scale_10
        self.play(
            FadeOut(roots),
            FadeOut(reject_cross),
            FadeOut(step_label),
            FadeOut(domain_note),
        )
        self.play(Write(final_answer), run_time=1.5)
        remaining_10 = max(0.1, _audio_dur_9 - anim_time_10 + 0.1)
        self.wait(remaining_10)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q02_newton_iteration_1780228804/media/audio/log₂_x____log₂_x_2___ef4b301378/step_10.mp3")  # [auto-injected]
        _audio_dur_10 = 4.15  # [audio-sync]
        # Step 11
        _scale_11 = max(1.0, (_audio_dur_10 * 0.7) / 1.500)
        self.set_subtitle("我們把答案框起來，確認我們的解已經完成。", run_time=_audio_dur_10)
        anim_time_11 = 1.500 * _scale_11
        self.play(Create(answer_box), run_time=1.5)
        remaining_11 = max(0.1, _audio_dur_10 - anim_time_11 + 0.1)
        self.wait(remaining_11)