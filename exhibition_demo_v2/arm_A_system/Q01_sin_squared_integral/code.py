from manim import *

# [VISUAL REASONING]
# A single equation anchor at y=+1.4 is morphed step-by-step via ReplacementTransform
# to avoid screen overflow, while a persistent shaded sin^2(x) curve below (y~-1.3)
# gives geometric meaning to the final value pi/2. All MathTex stay scaled ~0.9 to
# remain within bounds; axes and curve never cross y=-2.8.

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
        registry = {}

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Evaluate_the_integra_1f23b7486f/step_00.mp3")  # [auto-injected] duration=5.11s
        _audio_dur_0 = 5.11  # [audio-sync] actual TTS duration
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.500)
        title = Text("Integral of sin^2(x) from 0 to pi", color=WHITE, font_size=34)
        title.to_edge(UP, buff=0.5)
        registry["title"] = title
        self.set_subtitle("我們從 0 到 pi 的 sin 平方 x 定積分開始。", run_time=_audio_dur_0)
        anim_time_1 = 1.500 * _scale_1
        self.play(Write(title), run_time=anim_time_1)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Evaluate_the_integra_1f23b7486f/step_01.mp3")  # [auto-injected] duration=3.29s
        _audio_dur_1 = 3.29  # [audio-sync] actual TTS duration
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 1.500)
        eq1 = MathTex(r"\int_{0}^{\pi} \sin^2 x \, dx", color=WHITE).scale(0.9)
        eq1.move_to(ORIGIN + np.array([0, 1.4, 0]))
        registry["eq1"] = eq1
        self.set_subtitle("這是我們想要求的積分。", run_time=_audio_dur_1)
        anim_time_2 = 1.500 * _scale_2
        self.play(Write(eq1), run_time=anim_time_2)
        self.play(Circumscribe(eq1, color=YELLOW))
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Evaluate_the_integra_1f23b7486f/step_02.mp3")  # [auto-injected] duration=5.74s
        _audio_dur_2 = 5.74  # [audio-sync] actual TTS duration
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 1.500)
        axes = Axes(
            x_range=[0, 3.2, 1],
            y_range=[0, 1.2, 0.5],
            x_length=5.5,
            y_length=2.2,
            axis_config={"color": GREY},
        )
        axes.move_to(ORIGIN + np.array([0, -1.3, 0]))
        registry["axes"] = axes
        curve = axes.plot(lambda x: np.sin(x) ** 2, x_range=[0, PI], color=BLUE)
        registry["curve"] = curve
        area = axes.get_area(curve, x_range=[0, PI], color=TEAL, opacity=0.5)
        registry["area"] = area
        self.set_subtitle("讓我們畫出 sin 平方 x；答案就等於這條曲線下的陰影面積。", run_time=_audio_dur_2)
        anim_time_3 = 1.500 * _scale_3
        self.play(Create(axes), run_time=anim_time_3)
        self.play(Create(curve), run_time=1.0)
        self.play(FadeIn(area), run_time=1.0)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 2.0 + 0.1)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Evaluate_the_integra_1f23b7486f/step_03.mp3")  # [auto-injected] duration=6.67s
        _audio_dur_3 = 6.67  # [audio-sync] actual TTS duration
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.000)
        eq2 = MathTex(r"= \int_{0}^{\pi} \frac{1 - \cos 2x}{2} \, dx", color=WHITE).scale(0.9)
        eq2.move_to(ORIGIN + np.array([0, 1.4, 0]))
        registry["eq2"] = eq2
        self.set_subtitle("套用半角公式：sin 平方 x 等於 1 減去 cos 2x，再除以 2。", run_time=_audio_dur_3)
        anim_time_4 = 2.000 * _scale_4
        self.play(ReplacementTransform(eq1, eq2), run_time=anim_time_4)
        self.play(Indicate(eq2, color=RED))
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Evaluate_the_integra_1f23b7486f/step_04.mp3")  # [auto-injected] duration=6.31s
        _audio_dur_4 = 6.31  # [audio-sync] actual TTS duration
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        eq3 = MathTex(r"= \frac{1}{2}\int_{0}^{\pi} 1 \, dx - \frac{1}{2}\int_{0}^{\pi} \cos 2x \, dx", color=WHITE).scale(0.9)
        eq3.move_to(ORIGIN + np.array([0, 1.4, 0]))
        registry["eq3"] = eq3
        self.set_subtitle("將被積函數拆成兩個較簡單的積分，分離常數項與餘弦項。", run_time=_audio_dur_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(ReplacementTransform(eq2, eq3), run_time=anim_time_5)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(max(0.1, remaining_5))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Evaluate_the_integra_1f23b7486f/step_05.mp3")  # [auto-injected] duration=5.26s
        _audio_dur_5 = 5.26  # [audio-sync] actual TTS duration
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 2.000)
        eq4 = MathTex(r"= \left[ \frac{x}{2} - \frac{\sin 2x}{4} \right]_{0}^{\pi}", color=WHITE).scale(0.9)
        eq4.move_to(ORIGIN + np.array([0, 1.4, 0]))
        registry["eq4"] = eq4
        self.set_subtitle("對每一項積分，得到 x 除以 2 減去 sin 2x 除以 4。", run_time=_audio_dur_5)
        anim_time_6 = 2.000 * _scale_6
        self.play(ReplacementTransform(eq3, eq4), run_time=anim_time_6)
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 + 0.1)
        self.wait(max(0.1, remaining_6))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Evaluate_the_integra_1f23b7486f/step_06.mp3")  # [auto-injected] duration=5.09s
        _audio_dur_6 = 5.09  # [audio-sync] actual TTS duration
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 2.000)
        eq5 = MathTex(r"= \left( \frac{\pi}{2} - \frac{\sin 2\pi}{4} \right) - \left( 0 - 0 \right)", color=WHITE).scale(0.9)
        eq5.move_to(ORIGIN + np.array([0, 1.4, 0]))
        registry["eq5"] = eq5
        self.set_subtitle("代入上下界 pi 與 0；注意 sin 2pi 等於零。", run_time=_audio_dur_6)
        anim_time_7 = 2.000 * _scale_7
        self.play(ReplacementTransform(eq4, eq5), run_time=anim_time_7)
        self.play(Indicate(eq5, color=RED))
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_7))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Evaluate_the_integra_1f23b7486f/step_07.mp3")  # [auto-injected] duration=5.06s
        _audio_dur_7 = 5.06  # [audio-sync] actual TTS duration
        # Step 8
        _scale_8 = max(1.0, (_audio_dur_7 * 0.7) / 1.500)
        eq6 = MathTex(r"= \frac{\pi}{2}", color=YELLOW).scale(0.9)
        eq6.move_to(ORIGIN + np.array([0, 1.4, 0]))
        registry["eq6"] = eq6
        self.set_subtitle("化簡所有項後，剩下乾淨的最終答案，pi 除以 2。", run_time=_audio_dur_7)
        anim_time_8 = 1.500 * _scale_8
        self.play(ReplacementTransform(eq5, eq6), run_time=anim_time_8)
        remaining_8 = max(0.1, _audio_dur_7 - anim_time_8 + 0.1)
        self.wait(max(0.1, remaining_8))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Evaluate_the_integra_1f23b7486f/step_08.mp3")  # [auto-injected] duration=5.64s
        _audio_dur_8 = 5.64  # [audio-sync] actual TTS duration
        # Step 9
        _scale_9 = max(1.0, (_audio_dur_8 * 0.7) / 1.500)
        answer_box = SurroundingRectangle(eq6, color=YELLOW, buff=0.15)
        registry["answer_box"] = answer_box
        self.set_subtitle("這個值，pi 除以 2，正是曲線下的陰影面積。", run_time=_audio_dur_8)
        anim_time_9 = 1.500 * _scale_9
        self.play(Create(answer_box), run_time=anim_time_9)
        self.play(Indicate(area, color=TEAL))
        remaining_9 = max(0.1, _audio_dur_8 - anim_time_9 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_9))