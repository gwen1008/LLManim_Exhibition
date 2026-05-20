# [VISUAL REASONING]
# Centered single-equation morphing demonstrating scientific notation addition.
# Title at top, step labels above equation, final boxed answer below, note at bottom.

from manim import *

class SubtitleManager:
    """Auto-injected by RefiningLoop.pre_render_patch. Prevents subtitle overlap and implements YT-style chunking."""
    MAX_WIDTH = 12.5

    def __init__(self, scene, font_size=28):
        self.scene = scene
        self.font_size = font_size
        self._current = None
        self._y = 3.2 * DOWN

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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate__4_5___10__ccbf65239b/step_00.mp3")  # [auto-injected] duration=6.22s
        _audio_dur_0 = 6.22  # [audio-sync] actual TTS duration
        # Step 1
        title = Text("Scientific Notation Addition", color=WHITE, font_size=38).to_edge(UP, buff=0.5)
        problem_eq = MathTex("(4.5 \\times 10^{5}) + (7 \\times 10^{4})", color=WHITE).move_to(ORIGIN)
        note = Text("Exponents must match before adding!", color=BLUE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))

        self.set_subtitle("我們要計算 4.5 乘以 10 的 5 次方，加上 7 乘以 10 的 4 次方。", run_time=_audio_dur_0)
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate__4_5___10__ccbf65239b/step_01.mp3")  # [auto-injected] duration=9.10s
        _audio_dur_1 = 9.10  # [audio-sync] actual TTS duration
        # Step 2
        step1_label = Text("Step 1: Align the exponents", color=YELLOW, font_size=30).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq_step1 = MathTex("(4.5 \\times 10^{5}) + (0.7 \\times 10^{5})", color=WHITE).move_to(ORIGIN)

        self.set_subtitle("第一步：對齊指數。把 7 乘以 10 的 4 次方改寫成 0.7 乘以 10 的 5 次方。", run_time=_audio_dur_1)
        anim_time_2 = 1.5 + 1.0 + 1.5
        self.play(Write(problem_eq), run_time=1.5)
        self.play(Circumscribe(problem_eq, color=YELLOW))
        self.play(FadeIn(step1_label), FadeIn(note), run_time=1.0)
        self.play(ReplacementTransform(problem_eq, eq_step1), run_time=1.5)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate__4_5___10__ccbf65239b/step_02.mp3")  # [auto-injected] duration=11.02s
        _audio_dur_2 = 11.02  # [audio-sync] actual TTS duration
        # Step 3
        step2_label = Text("Step 2: Add the coefficients", color=YELLOW, font_size=30).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq_step2 = MathTex("(4.5 + 0.7) \\times 10^{5} = 5.2 \\times 10^{5}", color=WHITE).move_to(ORIGIN)

        self.set_subtitle("第二步：把係數相加。4.5 加 0.7 等於 5.2，所以結果是 5.2 乘以 10 的 5 次方。", run_time=_audio_dur_2)
        anim_time_3 = 1.0 + 1.0 + 2.0
        self.play(Indicate(eq_step1, color=RED))
        self.play(FadeOut(step1_label), run_time=0.5)
        self.play(FadeIn(step2_label), run_time=1.0)
        self.play(ReplacementTransform(eq_step1, eq_step2), run_time=2.0)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate__4_5___10__ccbf65239b/step_03.mp3")  # [auto-injected] duration=7.32s
        _audio_dur_3 = 7.32  # [audio-sync] actual TTS duration
        # Step 4
        step3_label = Text("Step 3: Identify a and n", color=YELLOW, font_size=30).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq_an = MathTex("a = 5.2, \\quad n = 5", color=WHITE).move_to(ORIGIN)

        self.set_subtitle("第三步：找出 a 和 n。這裡 a 等於 5.2，n 等於 5。", run_time=_audio_dur_3)
        anim_time_4 = 0.5 + 1.0 + 2.0
        self.play(FadeOut(step2_label), run_time=0.5)
        self.play(FadeIn(step3_label), run_time=1.0)
        self.play(ReplacementTransform(eq_step2, eq_an), run_time=2.0)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Calculate__4_5___10__ccbf65239b/step_04.mp3")  # [auto-injected] duration=5.98s
        _audio_dur_4 = 5.98  # [audio-sync] actual TTS duration
        # Step 5
        eq_final = MathTex("a + n = 5.2 + 5 = 10.2", color=GREEN).move_to(ORIGIN + np.array([0, -0.8, 0]))

        self.set_subtitle("所以 a 加 n 等於 5.2 加 5，也就是 10.2。", run_time=_audio_dur_4)
        anim_time_5 = 2.0 + 1.0
        self.play(Write(eq_final), run_time=2.0)
        answer_box = SurroundingRectangle(eq_final, color=GREEN, buff=0.2)
        self.play(Create(answer_box), run_time=1.0)
        self.play(Circumscribe(eq_final, color=GREEN))
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.5)
        self.wait(max(0.1, remaining_5))