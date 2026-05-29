# [VISUAL REASONING]
# Show recursion visually by replacing the current triangle group with its subdivided
# successor each round, reinforcing self-similarity. Title stays in HEADER zone,
# triangle stage centered, iteration counter on right side.

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
        # Title
        title = Text("Sierpinski Triangle Construction", color=WHITE, font_size=38)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # Level 0 triangle
        level0 = Polygon(
            [0, 2.0, 0], [-2.0, -1.46, 0], [2.0, -1.46, 0],
            color=BLUE, fill_opacity=0.7, stroke_width=2,
        )
        level0.move_to(ORIGIN + np.array([0, 0.27, 0]))

        # Counter labels
        counter_label = Text("Iteration: 0", color=YELLOW, font_size=28).move_to([5.0, 2.0, 0])
        counter1 = Text("Iteration: 1", color=YELLOW, font_size=28).move_to([5.0, 2.0, 0])
        counter2 = Text("Iteration: 2", color=YELLOW, font_size=28).move_to([5.0, 2.0, 0])
        counter3 = Text("Iteration: 3", color=YELLOW, font_size=28).move_to([5.0, 2.0, 0])
        counter4 = Text("Iteration: 4", color=YELLOW, font_size=28).move_to([5.0, 2.0, 0])

        # Level 1 VGroup
        level1 = VGroup(
            Polygon([0, 2.0, 0], [-1.0, 0.27, 0], [1.0, 0.27, 0],
                    color=BLUE, fill_opacity=0.7, stroke_width=2),
            Polygon([-1.0, 0.27, 0], [-2.0, -1.46, 0], [0, -1.46, 0],
                    color=BLUE, fill_opacity=0.7, stroke_width=2),
            Polygon([1.0, 0.27, 0], [0, -1.46, 0], [2.0, -1.46, 0],
                    color=BLUE, fill_opacity=0.7, stroke_width=2),
        )
        level1.move_to(ORIGIN + np.array([0, 0.27, 0]))

        # Level 2 VGroup
        level2_verts = [
            [[0, 2.0, 0], [-0.5, 1.135, 0], [0.5, 1.135, 0]],
            [[-0.5, 1.135, 0], [-1.0, 0.27, 0], [0, 0.27, 0]],
            [[0.5, 1.135, 0], [0, 0.27, 0], [1.0, 0.27, 0]],
            [[-1.0, 0.27, 0], [-1.5, -0.595, 0], [-0.5, -0.595, 0]],
            [[-1.5, -0.595, 0], [-2.0, -1.46, 0], [-1.0, -1.46, 0]],
            [[-0.5, -0.595, 0], [-1.0, -1.46, 0], [0, -1.46, 0]],
            [[1.0, 0.27, 0], [0.5, -0.595, 0], [1.5, -0.595, 0]],
            [[0.5, -0.595, 0], [0, -1.46, 0], [1.0, -1.46, 0]],
            [[1.5, -0.595, 0], [1.0, -1.46, 0], [2.0, -1.46, 0]],
        ]
        level2 = VGroup(*[
            Polygon(*v, color=BLUE, fill_opacity=0.7, stroke_width=1)
            for v in level2_verts
        ])
        level2.move_to(ORIGIN + np.array([0, 0.27, 0]))

        # Level3 label
        level3_img = Text("27 triangles", color=WHITE, font_size=22).move_to([5.0, 1.4, 0])

        # Formula
        formula = MathTex("N_k = 3^k", color=GREEN).move_to([5.0, 0.5, 0])

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q10_sierpinski_1779987659/media/audio/Construct_the_Sierpi_ddff600f9c/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 5.62  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 2.000)
        self.set_subtitle("我們從一個等邊三角形開始，作為遞迴碎形的種子。", run_time=_audio_dur_0)
        anim_time_1 = 2.000 * _scale_1
        self.play(Create(level0), FadeIn(counter_label), run_time=2.0)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q10_sierpinski_1779987659/media/audio/Construct_the_Sierpi_ddff600f9c/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 5.45  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 3.500)
        self.set_subtitle("將其分成四個全等子三角形，並移除中央倒置的那一個。", run_time=_audio_dur_1)
        self.play(Indicate(level0, color=YELLOW))
        anim_time_2 = 3.500 * _scale_2
        self.play(
            ReplacementTransform(level0, level1),
            ReplacementTransform(counter_label, counter1),
            run_time=2.5,
        )
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q10_sierpinski_1779987659/media/audio/Construct_the_Sierpi_ddff600f9c/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 5.64  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.500)
        self.set_subtitle("對每個剩餘三角形套用相同規則，產生九個更小的副本。", run_time=_audio_dur_2)
        anim_time_3 = 2.500 * _scale_3
        self.play(
            ReplacementTransform(level1, level2),
            ReplacementTransform(counter1, counter2),
            run_time=2.5,
        )
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q10_sierpinski_1779987659/media/audio/Construct_the_Sierpi_ddff600f9c/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 5.93  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.000)
        self.set_subtitle("再次遞迴將數量乘以三，產生二十七個三角形。", run_time=_audio_dur_3)
        anim_time_4 = 2.000 * _scale_4
        self.play(
            Write(formula),
            ReplacementTransform(counter2, counter3),
            FadeIn(level3_img),
            run_time=2.0,
        )
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q10_sierpinski_1779987659/media/audio/Construct_the_Sierpi_ddff600f9c/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.05  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 3.000)
        self.set_subtitle("經過四次迭代，八十一個自相似三角形展現出謝爾賓斯基碎形。", run_time=_audio_dur_4)
        self.play(Circumscribe(formula, color=GREEN))
        anim_time_5 = 3.000 * _scale_5
        self.play(
            FadeIn(counter4),
            FadeOut(counter3),
            run_time=2.0,
        )
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)