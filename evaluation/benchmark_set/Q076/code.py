# [VISUAL REASONING]
# Number line visualization of integers x where 2 < |x| < 7.
# Blue dots for positive solutions (3,4,5,6), green for negatives (-3,-4,-5,-6).
# Final count 4+4=8 shown at bottom.

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
        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/There_are_8_integers_01638050f6/step_00.mp3")  # [auto-injected] duration=11.21s
        _audio_dur_0 = 11.21  # [audio-sync] actual TTS duration
        # Step 1
        title = Text("Integers with 2 < |x| < 7", color=WHITE, font_size=38).to_edge(UP, buff=0.5)
        number_line = NumberLine(x_range=[-7, 7, 1], length=11, include_numbers=True, color=WHITE).move_to(ORIGIN)
        origin_dot = Dot(point=ORIGIN, color=YELLOW, radius=0.1)
        abs_def = Text("|x| = distance from origin", color=YELLOW, font_size=28).move_to([0, 2.0, 0])

        self.set_subtitle("我們要找出絕對值大於 2 且小於 7 的所有整數。記住，絕對值就是數線上到原點的距離。", run_time=_audio_dur_0)
        anim_time_1 = 3.0
        self.play(Write(title), run_time=1.0)
        self.play(Create(number_line), FadeIn(origin_dot), Write(abs_def), run_time=2.0)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/There_are_8_integers_01638050f6/step_01.mp3")  # [auto-injected] duration=10.32s
        _audio_dur_1 = 10.32  # [audio-sync] actual TTS duration
        # Step 2
        dot_p3 = Dot(point=[2.357, 0, 0], color=BLUE, radius=0.12)
        dot_p4 = Dot(point=[3.143, 0, 0], color=BLUE, radius=0.12)
        dot_p5 = Dot(point=[3.929, 0, 0], color=BLUE, radius=0.12)
        dot_p6 = Dot(point=[4.714, 0, 0], color=BLUE, radius=0.12)
        pos_label = MathTex(r"3, 4, 5, 6 \;(4)", color=BLUE).move_to([3.5, 1.0, 0])

        self.set_subtitle("首先找出嚴格介於 2 和 7 之間的正整數，分別是 3、4、5、6，共四個。", run_time=_audio_dur_1)
        anim_time_2 = 2.5
        self.play(LaggedStart(*[FadeIn(d) for d in [dot_p3, dot_p4, dot_p5, dot_p6]], lag_ratio=0.2), run_time=1.5)
        self.play(Write(pos_label), run_time=1.0)
        self.play(Circumscribe(dot_p3, color=BLUE))
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/There_are_8_integers_01638050f6/step_02.mp3")  # [auto-injected] duration=11.02s
        _audio_dur_2 = 11.02  # [audio-sync] actual TTS duration
        # Step 3
        dot_n3 = Dot(point=[-2.357, 0, 0], color=GREEN, radius=0.12)
        dot_n4 = Dot(point=[-3.143, 0, 0], color=GREEN, radius=0.12)
        dot_n5 = Dot(point=[-3.929, 0, 0], color=GREEN, radius=0.12)
        dot_n6 = Dot(point=[-4.714, 0, 0], color=GREEN, radius=0.12)
        neg_label = MathTex(r"-6, -5, -4, -3 \;(4)", color=GREEN).move_to([-3.5, 1.0, 0])

        self.set_subtitle("由對稱性，同樣距離的負整數也符合條件：-3、-4、-5、-6，又是四個。", run_time=_audio_dur_2)
        anim_time_3 = 2.5
        self.play(LaggedStart(*[FadeIn(d) for d in [dot_n3, dot_n4, dot_n5, dot_n6]], lag_ratio=0.2), run_time=1.5)
        self.play(Write(neg_label), run_time=1.0)
        self.play(Indicate(neg_label, color=GREEN))
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/There_are_8_integers_01638050f6/step_03.mp3")  # [auto-injected] duration=6.43s
        _audio_dur_3 = 6.43  # [audio-sync] actual TTS duration
        # Step 4
        final_eq = MathTex(r"4 + 4 = 8", color=YELLOW).move_to([0, -2.3, 0])

        self.set_subtitle("把四個正整數和四個負整數相加，4 加 4 等於 8。", run_time=_audio_dur_3)
        anim_time_4 = 2.5
        self.play(FadeOut(abs_def), run_time=0.5)
        self.play(Write(final_eq), run_time=2.0)
        self.play(Circumscribe(final_eq, color=YELLOW))
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))