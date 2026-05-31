from manim import *

# [VISUAL REASONING]
# A persistent shaded triangle on the left grounds the abstract bounds, while
# the right-side equation morphs step-by-step via ReplacementTransform to avoid
# vertical overflow. The axes+triangle group stays static on the left the whole
# time; a single equation anchor on the right is morphed between derivation steps.

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
        title = Text("Double Integral over a Triangular Region", color=WHITE, font_size=34)
        title.to_edge(UP)

        axes = Axes(
            x_range=[0, 1.2, 0.5],
            y_range=[0, 1.2, 0.5],
            x_length=3,
            y_length=3,
            axis_config={"color": GREY},
        )
        axes.move_to(np.array([-3.5, -0.3, 0]))

        triangle = Polygon(
            np.array([-5, -1.8, 0]),
            np.array([-2, -1.8, 0]),
            np.array([-2, 1.2, 0]),
            color=BLUE,
            fill_opacity=0.45,
        )
        triangle.move_to(axes.get_center())

        line_label = MathTex("y=x", color=YELLOW, font_size=30)
        line_label.move_to(triangle.get_center() + np.array([-0.2, 1.4, 0]))

        eq_anchor = np.array([3.3, 0.3, 0])

        eq_setup = MathTex(r"\int_{0}^{1}\int_{0}^{x} xy \, dy \, dx", color=WHITE, font_size=40)
        eq_setup.move_to(eq_anchor)
        eq_setup.scale(0.85)

        eq_inner = MathTex(r"\int_{0}^{1} \left[ \frac{x y^2}{2} \right]_{0}^{x} dx", color=WHITE, font_size=40)
        eq_inner.move_to(eq_anchor)
        eq_inner.scale(0.85)

        eq_inner_simpl = MathTex(r"\int_{0}^{1} \frac{x^3}{2} \, dx", color=WHITE, font_size=44)
        eq_inner_simpl.move_to(eq_anchor)
        eq_inner_simpl.scale(0.85)

        eq_outer = MathTex(r"\left[ \frac{x^4}{8} \right]_{0}^{1}", color=WHITE, font_size=44)
        eq_outer.move_to(eq_anchor)
        eq_outer.scale(0.85)

        eq_final = MathTex(r"= \frac{1}{8}", color=GREEN, font_size=52)
        eq_final.move_to(eq_anchor)
        eq_final.scale(0.85)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_double_i_cba00fc8ec/step_00.mp3")  # [auto-injected] duration=5.59s
        _audio_dur_0 = 5.59  # [audio-sync] actual TTS duration
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.500)
        self.set_subtitle("我們先畫出由直線 y 等於 x 所圍成的三角形區域。", run_time=_audio_dur_0)
        anim_time_1 = 1.500 * _scale_1
        self.play(Create(axes), run_time=1.5)
        self.play(Write(title), run_time=1.0)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_double_i_cba00fc8ec/step_01.mp3")  # [auto-injected] duration=6.00s
        _audio_dur_1 = 6.00  # [audio-sync] actual TTS duration
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.000)
        self.set_subtitle("為 x 從零到一、y 從零上升到 x 的區域著色。", run_time=_audio_dur_1)
        anim_time_2 = 2.000 * _scale_2
        self.play(FadeIn(triangle), run_time=2.0)
        self.play(Write(line_label), run_time=0.8)
        self.play(Indicate(line_label, color=YELLOW))
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 - 0.8 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_double_i_cba00fc8ec/step_02.mp3")  # [auto-injected] duration=7.15s
        _audio_dur_2 = 7.15  # [audio-sync] actual TTS duration
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.000)
        self.set_subtitle("設定逐次積分：外層對 x 從零到一，內層對 y 從零到 x。", run_time=_audio_dur_2)
        anim_time_3 = 2.000 * _scale_3
        self.play(Write(eq_setup), run_time=2.0)
        self.play(Circumscribe(eq_setup, color=YELLOW))
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_double_i_cba00fc8ec/step_03.mp3")  # [auto-injected] duration=6.53s
        _audio_dur_3 = 6.53  # [audio-sync] actual TTS duration
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.000)
        self.set_subtitle("先對 y 積分，得到 x y 平方除以二，從零到 x 求值。", run_time=_audio_dur_3)
        anim_time_4 = 2.000 * _scale_4
        self.play(ReplacementTransform(eq_setup, eq_inner), run_time=2.0)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_double_i_cba00fc8ec/step_04.mp3")  # [auto-injected] duration=5.21s
        _audio_dur_4 = 5.21  # [audio-sync] actual TTS duration
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        self.set_subtitle("代入上下限後，內層積分收縮為 x 的三次方除以二。", run_time=_audio_dur_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(ReplacementTransform(eq_inner, eq_inner_simpl), run_time=2.0)
        self.play(Indicate(eq_inner_simpl, color=RED))
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_5))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_double_i_cba00fc8ec/step_05.mp3")  # [auto-injected] duration=5.83s
        _audio_dur_5 = 5.83  # [audio-sync] actual TTS duration
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 2.000)
        self.set_subtitle("接著對 x 積分，得到 x 的四次方除以八，從零到一。", run_time=_audio_dur_5)
        anim_time_6 = 2.000 * _scale_6
        self.play(ReplacementTransform(eq_inner_simpl, eq_outer), run_time=2.0)
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 + 0.1)
        self.wait(max(0.1, remaining_6))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Compute_the_double_i_cba00fc8ec/step_06.mp3")  # [auto-injected] duration=5.45s
        _audio_dur_6 = 5.45  # [audio-sync] actual TTS duration
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 2.000)
        self.set_subtitle("代入上下限求值後，化簡得到最終答案，八分之一。", run_time=_audio_dur_6)
        anim_time_7 = 2.000 * _scale_7
        self.play(ReplacementTransform(eq_outer, eq_final), run_time=2.0)
        final_box = SurroundingRectangle(eq_final, color=GREEN)
        self.play(Create(final_box), run_time=0.8)
        self.play(Circumscribe(eq_final, color=GREEN))
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 - 0.8 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_7))