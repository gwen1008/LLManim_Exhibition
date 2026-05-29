# [VISUAL REASONING]
# Concrete 3-4-5 triangle demonstrates Pythagorean theorem via area sum.
# Three colored squares bloom outward; final equation 9+16=25 morphs to a²+b²=c².
# Layout: title at HEADER, triangle+squares at CONTENT, equation at FOOTER.

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
        # Object registry
        title = Text("畢氏定理：面積證明", color=WHITE, font_size=36).to_edge(UP, buff=0.5)

        triangle = Polygon(
            [-0.5, -0.75, 0], [1.5, -0.75, 0], [-0.5, 0.75, 0],
            color=WHITE, fill_opacity=0.3, stroke_width=3
        ).move_to(ORIGIN)

        label_a = MathTex("a=3", color=BLUE).move_to(ORIGIN + np.array([-0.9, 0, 0]))
        label_b = MathTex("b=4", color=GREEN).move_to(ORIGIN + np.array([0.5, -1.05, 0]))
        label_c = MathTex("c=5", color=RED).move_to(ORIGIN + np.array([0.8, 0.4, 0]))

        square_a = Polygon(
            [-0.5, -0.75, 0], [-0.5, 0.75, 0], [-2.0, 0.75, 0], [-2.0, -0.75, 0],
            color=BLUE, fill_opacity=0.5, stroke_width=2
        )
        area_a_label = MathTex("a^2=9", color=WHITE).move_to(square_a.get_center())

        square_b = Polygon(
            [-0.5, -0.75, 0], [1.5, -0.75, 0], [1.5, -2.0, 0], [-0.5, -2.0, 0],
            color=GREEN, fill_opacity=0.5, stroke_width=2
        )
        area_b_label = MathTex("b^2=16", color=WHITE).move_to(square_b.get_center())

        square_c = Polygon(
            [1.5, -0.75, 0], [-0.5, 0.75, 0], [1.0, 2.25, 0], [3.0, 0.75, 0],
            color=RED, fill_opacity=0.5, stroke_width=2
        )
        area_c_label = MathTex("c^2=25", color=WHITE).move_to(square_c.get_center())

        eq_sum = MathTex("9", "+", "16", "=", "25", color=YELLOW, font_size=44).move_to(
            ORIGIN + np.array([0, -2.3, 0])
        )
        eq_general = MathTex("a^2", "+", "b^2", "=", "c^2", color=YELLOW, font_size=48).move_to(
            ORIGIN + np.array([0, -2.3, 0])
        )

        self.add(title)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q04_pythagorean_1779986651/media/audio/Prove_the_Pythagorea_d5a14d0ee5/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 4.78  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 2.000)
        self.set_subtitle("從一個直角三角形開始，兩股長度分別為三與四。", run_time=_audio_dur_0)
        anim_time_1 = 2.000 * _scale_1
        self.play(
            Create(triangle, run_time=2.0),
            LaggedStart(
                FadeIn(label_a), FadeIn(label_b), FadeIn(label_c),
                lag_ratio=0.2
            )
        )
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q04_pythagorean_1779986651/media/audio/Prove_the_Pythagorea_d5a14d0ee5/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 5.74  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.500)
        self.set_subtitle("在股 a 外側建立正方形，其面積等於 a 平方，也就是九。", run_time=_audio_dur_1)
        anim_time_2 = 2.500 * _scale_2
        self.play(Indicate(label_a, color=BLUE))
        self.play(Create(square_a, run_time=2.0))
        self.play(FadeIn(area_a_label, run_time=0.5))
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q04_pythagorean_1779986651/media/audio/Prove_the_Pythagorea_d5a14d0ee5/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 6.29  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.500)
        self.set_subtitle("在股 b 外側建立另一個正方形，其面積等於 b 平方，也就是十六。", run_time=_audio_dur_2)
        anim_time_3 = 2.500 * _scale_3
        self.play(Indicate(label_b, color=GREEN))
        self.play(Create(square_b, run_time=2.0))
        self.play(FadeIn(area_b_label, run_time=0.5))
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q04_pythagorean_1779986651/media/audio/Prove_the_Pythagorea_d5a14d0ee5/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.38  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 3.000)
        self.set_subtitle("現在在斜邊上建立正方形，其面積等於 c 平方，也就是二十五。", run_time=_audio_dur_3)
        anim_time_4 = 3.000 * _scale_4
        self.play(Indicate(label_c, color=RED))
        self.play(Create(square_c, run_time=2.5))
        self.play(FadeIn(area_c_label, run_time=0.5))
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q04_pythagorean_1779986651/media/audio/Prove_the_Pythagorea_d5a14d0ee5/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.86  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        self.set_subtitle("兩個股的正方形相加等於斜邊的正方形：九加十六等於二十五。", run_time=_audio_dur_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(Write(eq_sum, run_time=2.0))
        self.play(Circumscribe(eq_sum, color=YELLOW))
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.0 + 0.1)
        self.wait(remaining_5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q04_pythagorean_1779986651/media/audio/Prove_the_Pythagorea_d5a14d0ee5/step_05.mp3")  # [auto-injected]
        _audio_dur_5 = 6.12  # [audio-sync]
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 2.000)
        self.set_subtitle("這對每個直角三角形都成立：a 平方加 b 平方等於 c 平方。", run_time=_audio_dur_5)
        anim_time_6 = 2.000 * _scale_6
        self.play(TransformMatchingTex(eq_sum, eq_general, run_time=2.0))
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 + 0.1)
        self.wait(remaining_6)