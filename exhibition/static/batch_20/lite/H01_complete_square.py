from manim import *

# [VISUAL REASONING]
# Equation-morphing column communicates the algebraic flow of completing the square.
# Successive equations are centered and morphed via ReplacementTransform to show
# algebraic continuity. A number line is reserved for the final step to ground the
# roots geometrically without cluttering earlier algebra. Title sits in the header
# zone; all equations anchor to ORIGIN; number line sits low in CONTENT.

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
        title = Text("配方法", font_size=40).to_edge(UP)
        underline = Line(LEFT, RIGHT).set_width(title.width + 0.4).next_to(title, DOWN, buff=0.1)

        eq_original = MathTex("x^2 - 6x + 5 = 0", font_size=56).move_to(ORIGIN)
        eq_move = MathTex("x^2 - 6x = -5", font_size=56).move_to(ORIGIN)
        eq_addnine = MathTex("x^2 - 6x + 9 = -5 + 9", font_size=52).move_to(ORIGIN)
        eq_square = MathTex("(x-3)^2 = 4", font_size=60).move_to(ORIGIN)
        eq_roots = MathTex(r"x - 3 = \pm 2 \;\Rightarrow\; x = 1,\; x = 5", font_size=50).move_to(UP)

        number_line = NumberLine(x_range=[0, 6, 1], length=8, include_numbers=True).move_to(DOWN * 1.5)

        dot_root1 = Dot(number_line.n2p(1), radius=0.12, color="#FFD700")
        dot_root2 = Dot(number_line.n2p(5), radius=0.12, color="#FFD700")
        label1 = Text("1", font_size=28, color="#FFD700").next_to(dot_root1, UP, buff=0.15)
        label2 = Text("5", font_size=28, color="#FFD700").next_to(dot_root2, UP, buff=0.15)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H01_complete_square_1780228645/media/audio/_final_translation_S_8a295ecd37/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 9.10  # [audio-sync]
        # Step 1
        self.set_subtitle("我們從二次方程式 x 平方減六 x 加五等於零開始，用配方法優雅地求解。", run_time=_audio_dur_0)
        anim_time_1 = _audio_dur_0
        self.play(
            LaggedStart(
                Write(title),
                FadeIn(underline),
                Write(eq_original),
                Indicate(eq_original),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H01_complete_square_1780228645/media/audio/_final_translation_S_8a295ecd37/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 8.64  # [audio-sync]
        # Step 2
        self.set_subtitle("首先，我們把常數五移到等號右邊，讓變數項 x 平方減六 x 單獨留在左邊。", run_time=_audio_dur_1)
        box_right = SurroundingRectangle(eq_move, color=YELLOW, buff=0.15)
        anim_time_2 = _audio_dur_1
        self.play(
            LaggedStart(
                Indicate(eq_original),
                ReplacementTransform(eq_original, eq_move),
                Create(box_right),
                FadeOut(box_right),
                lag_ratio=0.25,
                run_time=anim_time_2,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H01_complete_square_1780228645/media/audio/_final_translation_S_8a295ecd37/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 9.02  # [audio-sync]
        # Step 3
        self.set_subtitle("關鍵步驟：兩邊同時加九，因為九是係數六一半的平方，這樣就能湊成完全平方。", run_time=_audio_dur_2)
        annotation = MathTex(r"\left(\tfrac{6}{2}\right)^2 = 9", font_size=40).next_to(eq_addnine, UP, buff=0.5)
        anim_time_3 = _audio_dur_2
        self.play(
            LaggedStart(
                ReplacementTransform(eq_move, eq_addnine),
                Write(annotation),
                Indicate(eq_addnine),
                FadeOut(annotation),
                lag_ratio=0.25,
                run_time=anim_time_3,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H01_complete_square_1780228645/media/audio/_final_translation_S_8a295ecd37/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 9.05  # [audio-sync]
        # Step 4
        self.set_subtitle("左邊整齊地因式分解成 x 減三的平方，右邊化簡為四，得到簡潔的形式。", run_time=_audio_dur_3)
        sq_box = SurroundingRectangle(eq_square, color=YELLOW, buff=0.2)
        anim_time_4 = _audio_dur_3
        self.play(
            LaggedStart(
                ReplacementTransform(eq_addnine, eq_square),
                Create(sq_box),
                Indicate(eq_square),
                FadeOut(sq_box),
                lag_ratio=0.25,
                run_time=anim_time_4,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H01_complete_square_1780228645/media/audio/_final_translation_S_8a295ecd37/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 9.82  # [audio-sync]
        # Step 5
        self.set_subtitle("兩邊開平方得到 x 減三等於正負二，於是得到兩個根 x 等於一和 x 等於五。", run_time=_audio_dur_4)
        self.play(FadeOut(eq_square), run_time=0.3)
        anim_time_5 = max(0.1, _audio_dur_4 - 0.3)
        self.play(
            LaggedStart(
                Write(eq_roots),
                Create(number_line),
                AnimationGroup(FadeIn(dot_root1, scale=1.5), FadeIn(label1)),
                AnimationGroup(FadeIn(dot_root2, scale=1.5), FadeIn(label2)),
                AnimationGroup(Indicate(dot_root1), Indicate(dot_root2)),
                lag_ratio=0.25,
                run_time=anim_time_5,
            )
        )
        self.wait(0.1)