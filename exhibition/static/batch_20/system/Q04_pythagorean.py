from manim import *

# [VISUAL REASONING]
# Split layout: shaded area-under-curve on the left (compact Axes ~0.8 scale),
# symbolic FTC derivation morphing in-place on the right. ReplacementTransform
# morphs the antiderivative bracket into the evaluated limits so equations never
# stack messily. get_area shades f(x)=3x^2-2x on x in [0,2]. All z=0, nothing
# extends below y=-2.5. Signal actions (Circumscribe/Indicate) hardcoded inline.

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

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q04_pythagorean_1780228981/media/audio/Calculate_the_defini_33d454edba/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 5.64  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 2.000)
        title = Text("定積分與微積分基本定理", color=WHITE, font_size=34)
        title.to_edge(UP)
        registry["title"] = title

        integral = MathTex(r"\int_0^2 (3x^2-2x)\,dx", color=WHITE)
        integral.move_to(ORIGIN + np.array([3.2, 1.2, 0]))
        registry["integral"] = integral

        self.add(title)
        self.set_subtitle("我們要計算 3x 平方減 2x 從 0 到 2 的定積分。", run_time=_audio_dur_0)
        anim_time_1 = 2.000 * _scale_1
        self.play(Write(integral), run_time=2.0)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q04_pythagorean_1780228981/media/audio/Calculate_the_defini_33d454edba/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 5.88  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 1.500)
        axes = Axes(
            x_range=[0, 2.5, 1],
            y_range=[0, 9, 3],
            x_length=4.5,
            y_length=4.0,
            axis_config={"color": GREY},
        )
        axes.move_to(ORIGIN + np.array([-3.5, -0.3, 0]))
        registry["axes"] = axes

        curve = axes.plot(lambda x: 3 * x**2 - 2 * x, x_range=[0, 2.2, 0.05], color=BLUE)
        registry["curve"] = curve

        curve_label = MathTex(r"f(x)=3x^2-2x", color=BLUE)
        curve_label.next_to(axes, UP, buff=0.15)
        registry["curve_label"] = curve_label

        self.set_subtitle("從幾何來看，這個積分就是曲線與 x 軸之間的陰影面積。", run_time=_audio_dur_1)
        anim_time_2 = 1.500 * _scale_2
        self.play(Create(axes), run_time=1.5)
        self.play(Create(curve), Write(curve_label), run_time=1.5)
        remaining_2 = max(0.1, _audio_dur_1 - (anim_time_2 + 1.5) + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q04_pythagorean_1780228981/media/audio/Calculate_the_defini_33d454edba/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 5.35  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 1.500)
        area = axes.get_area(curve, x_range=[0, 2], color=TEAL, opacity=0.5)
        registry["area"] = area

        self.set_subtitle("把 0 到 2 之間塗上顏色，正好標出積分所量度的面積。", run_time=_audio_dur_2)
        anim_time_3 = 1.500 * _scale_3
        self.play(FadeIn(area), run_time=1.5)
        self.play(Circumscribe(area, color=YELLOW))
        remaining_3 = max(0.1, _audio_dur_2 - (anim_time_3 + 1.0) + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q04_pythagorean_1780228981/media/audio/Calculate_the_defini_33d454edba/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 6.89  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 2.000)
        antideriv = MathTex(r"=\Big[\,x^3-x^2\,\Big]_0^2", color=WHITE)
        antideriv.move_to(ORIGIN + np.array([3.2, 0.0, 0]))
        registry["antideriv"] = antideriv

        self.set_subtitle("根據微積分基本定理，使用反導函數 F of x 等於 x 立方減 x 平方。", run_time=_audio_dur_3)
        anim_time_4 = 2.000 * _scale_4
        self.play(Write(antideriv), run_time=2.0)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q04_pythagorean_1780228981/media/audio/Calculate_the_defini_33d454edba/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.07  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        evaluated = MathTex(r"=(8-4)-(0-0)", color=WHITE)
        evaluated.move_to(ORIGIN + np.array([3.2, 0.0, 0]))
        registry["evaluated"] = evaluated

        self.set_subtitle("代入上下限得到 F of 2 等於 4，減去 F of 0 等於 0。", run_time=_audio_dur_4)
        self.play(Indicate(antideriv, color=RED))
        anim_time_5 = 2.000 * _scale_5
        self.play(ReplacementTransform(antideriv, evaluated), run_time=2.0)
        remaining_5 = max(0.1, _audio_dur_4 - (anim_time_5 + 1.0) + 0.1)
        self.wait(remaining_5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q04_pythagorean_1780228981/media/audio/Calculate_the_defini_33d454edba/step_05.mp3")  # [auto-injected]
        _audio_dur_5 = 5.04  # [audio-sync]
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 1.500)
        result = MathTex(r"=4", color=YELLOW)
        result.move_to(ORIGIN + np.array([3.2, -1.2, 0]))
        registry["result"] = result

        self.set_subtitle("結果是 4，正是這個區間內曲線下方的精確面積。", run_time=_audio_dur_5)
        anim_time_6 = 1.500 * _scale_6
        self.play(Write(result), run_time=1.5)
        self.play(Circumscribe(result, color=YELLOW))
        remaining_6 = max(0.1, _audio_dur_5 - (anim_time_6 + 1.0) + 0.1)
        self.wait(remaining_6)