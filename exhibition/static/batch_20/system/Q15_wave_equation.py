# [VISUAL REASONING]
# Translates the Director's blueprint for the 1D wave equation u(x,t)=sin(x-ct).
# Uses ValueTracker + always_redraw to animate rightward propagation.
# Layout: title in HEADER, axes centered in CONTENT, caption in FOOTER.

from manim import *
import numpy as np


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
        c = 1.0

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q15_wave_equation_1779988504/media/audio/Visualization_of_the_abf213ba92/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 6.82  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.800)
        title = Text("1D Wave Equation: Traveling Sine", color=WHITE, font_size=36)
        title.to_edge(UP, buff=0.5)
        self.set_subtitle("我們將視覺化一維波動方程的解 u(x,t) 等於 sin(x 減 ct)。", run_time=_audio_dur_0)
        anim_time_1 = 1.800 * _scale_1
        self.play(Write(title), run_time=anim_time_1)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q15_wave_equation_1779988504/media/audio/Visualization_of_the_abf213ba92/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 4.92  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.800)
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=11,
            y_length=3.2,
            axis_config={"color": GREY},
        ).move_to(np.array([0, 0.2, 0]))
        equation = MathTex("u(x,t)=\\sin(x-ct)", color=YELLOW)
        equation.move_to(np.array([3.5, 2.1, 0]))
        self.set_subtitle("建立座標軸，並顯示主導此行進波的方程式。", run_time=_audio_dur_1)
        anim_time_2 = 2.800 * _scale_2
        self.play(Create(axes), run_time=1.8)
        self.play(Write(equation), run_time=1.0)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q15_wave_equation_1779988504/media/audio/Visualization_of_the_abf213ba92/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 5.11  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.000)
        wave_initial = axes.plot(lambda x: np.sin(x), x_range=[-6, 6], color=BLUE)
        self.set_subtitle("在時間為零時,波形是一段純粹的正弦曲線。", run_time=_audio_dur_2)
        anim_time_3 = 2.000 * _scale_3
        self.play(Create(wave_initial), run_time=anim_time_3)
        self.play(Circumscribe(wave_initial, color=YELLOW), run_time=1.0)
        anim_time_3 += 1.0
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q15_wave_equation_1779988504/media/audio/Visualization_of_the_abf213ba92/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.53  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 7.400)
        t_tracker = ValueTracker(0.0)
        self.remove(wave_initial)
        wave_dynamic = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(x - c * t_tracker.get_value()),
                x_range=[-6, 6],
                color=BLUE,
            )
        )
        self.add(wave_dynamic)
        direction_arrow = Arrow(
            start=np.array([-1.0, 1.7, 0]),
            end=np.array([1.0, 1.7, 0]),
            color=GREEN,
            buff=0.0,
        )
        self.set_subtitle("隨著時間推進,波形的每一點以速度 c 向右平移,並保持形狀不變。", run_time=_audio_dur_3)
        self.play(Create(direction_arrow), run_time=(0.6)*_scale_4)
        self.play(Indicate(direction_arrow, color=GREEN), run_time=(0.8)*_scale_4)
        anim_time_4 = 7.400 * _scale_4
        self.play(t_tracker.animate.set_value(6.0), run_time=6.0, rate_func=linear)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q15_wave_equation_1779988504/media/audio/Visualization_of_the_abf213ba92/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 5.76  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        caption = Text("Wave moves right with speed c", color=WHITE, font_size=28)
        caption.move_to(np.array([0, -2.3, 0]))
        self.set_subtitle("這種剛性的向右平移,正是單向行進波解的特徵。", run_time=_audio_dur_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(Write(caption), run_time=anim_time_5)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)