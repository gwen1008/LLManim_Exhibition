from manim import *
import numpy as np

# [VISUAL REASONING]
# Keep one fixed sine reference and overlay each higher-order Taylor polynomial
# in a distinct color so the widening match interval is visible. A persistent
# top-right legend encodes order-to-color mapping. All curves inherit coordinates
# from a single shared Axes (no repositioning). y_range clamped to [-2,2] so
# high-order polynomials are naturally clipped.

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
        title = Text("Taylor Approximations of sin(x)", color=WHITE, font_size=36)
        title.to_edge(UP)

        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-2, 2, 1],
            x_length=11,
            y_length=4.2,
            axis_config={"color": GREY},
        )
        axes.move_to(ORIGIN)

        sine_curve = axes.plot(lambda x: np.sin(x), x_range=[-6, 6], color=BLUE)
        t1_curve = axes.plot(lambda x: x, x_range=[-6, 6], color=YELLOW)
        t3_curve = axes.plot(lambda x: x - x**3/6, x_range=[-6, 6], color=GREEN)
        t5_curve = axes.plot(lambda x: x - x**3/6 + x**5/120, x_range=[-6, 6], color=ORANGE)
        t7_curve = axes.plot(lambda x: x - x**3/6 + x**5/120 - x**7/5040, x_range=[-6, 6], color=RED)

        legend_sin = Text("sin(x)", color=BLUE, font_size=24).to_corner(UR, buff=0.4)
        legend_t1 = Text("T1 = x", color=YELLOW, font_size=24).next_to(legend_sin, DOWN, buff=0.2)
        legend_t3 = Text("T3", color=GREEN, font_size=24).next_to(legend_t1, DOWN, buff=0.2)
        legend_t5 = Text("T5", color=ORANGE, font_size=24).next_to(legend_t3, DOWN, buff=0.2)
        legend_t7 = Text("T7", color=RED, font_size=24).next_to(legend_t5, DOWN, buff=0.2)

        explanation = Text("Higher order = wider matching interval", color=WHITE, font_size=26)
        explanation.move_to([0, -2.5, 0])

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_how_Taylor_662d400deb/step_00.mp3")  # [auto-injected] duration=5.09s
        _audio_dur_0 = 5.09  # [audio-sync] actual TTS duration
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.500)
        self.set_subtitle("我們先在共用座標系上畫出真正的正弦曲線，以藍色呈現。", run_time=_audio_dur_0)
        anim_time_1 = 1.500 * _scale_1
        self.play(Create(axes), run_time=anim_time_1)
        self.play(Write(title), run_time=0.8)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 - 0.8 + 0.1)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_how_Taylor_662d400deb/step_01.mp3")  # [auto-injected] duration=5.98s
        _audio_dur_1 = 5.98  # [audio-sync] actual TTS duration
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.000)
        self.set_subtitle("這條藍色曲線是我們的目標函數，每一個泰勒多項式都會嘗試逼近它。", run_time=_audio_dur_1)
        anim_time_2 = 2.000 * _scale_2
        self.play(Create(sine_curve), run_time=anim_time_2)
        self.play(FadeIn(legend_sin), run_time=0.5)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 - 0.5 + 0.1)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_how_Taylor_662d400deb/step_02.mp3")  # [auto-injected] duration=7.13s
        _audio_dur_2 = 7.13  # [audio-sync] actual TTS duration
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.000)
        self.set_subtitle("一階逼近 T1 等於 x，只是一條直線，僅在原點附近與正弦曲線吻合。", run_time=_audio_dur_2)
        anim_time_3 = 2.000 * _scale_3
        self.play(Create(t1_curve), run_time=anim_time_3)
        self.play(FadeIn(legend_t1), run_time=0.5)
        self.play(Indicate(legend_t1, color=YELLOW))
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 0.5 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_how_Taylor_662d400deb/step_03.mp3")  # [auto-injected] duration=6.94s
        _audio_dur_3 = 6.94  # [audio-sync] actual TTS duration
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.000)
        self.set_subtitle("加入三次項得到 T3，它開始彎曲，並在更寬的範圍內貼合正弦曲線。", run_time=_audio_dur_3)
        anim_time_4 = 2.000 * _scale_4
        self.play(Create(t3_curve), run_time=anim_time_4)
        self.play(FadeIn(legend_t3), run_time=0.5)
        self.play(Indicate(legend_t3, color=GREEN))
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 - 0.5 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_how_Taylor_662d400deb/step_04.mp3")  # [auto-injected] duration=5.64s
        _audio_dur_4 = 5.64  # [audio-sync] actual TTS duration
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        self.set_subtitle("五階的 T5 以橘色呈現，將緊密吻合的範圍從零點延伸得更遠。", run_time=_audio_dur_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(Create(t5_curve), run_time=anim_time_5)
        self.play(FadeIn(legend_t5), run_time=0.5)
        self.play(Indicate(legend_t5, color=ORANGE))
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 0.5 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_5))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_how_Taylor_662d400deb/step_05.mp3")  # [auto-injected] duration=6.02s
        _audio_dur_5 = 6.02  # [audio-sync] actual TTS duration
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 2.000)
        self.set_subtitle("最後，七階的 T7 以紅色呈現，能在更寬的區間內追蹤正弦曲線。", run_time=_audio_dur_5)
        anim_time_6 = 2.000 * _scale_6
        self.play(Create(t7_curve), run_time=anim_time_6)
        self.play(FadeIn(legend_t7), run_time=0.5)
        self.play(Indicate(legend_t7, color=RED))
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 - 0.5 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_6))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Visualize_how_Taylor_662d400deb/step_06.mp3")  # [auto-injected] duration=6.31s
        _audio_dur_6 = 6.31  # [audio-sync] actual TTS duration
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 2.000)
        self.set_subtitle("所以每個更高階的泰勒多項式都能在逐漸變寬的區間內與函數吻合。", run_time=_audio_dur_6)
        anim_time_7 = 2.000 * _scale_7
        self.play(Write(explanation), run_time=anim_time_7)
        self.play(Circumscribe(explanation, color=YELLOW))
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_7))