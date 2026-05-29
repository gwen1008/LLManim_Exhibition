from manim import *
import numpy as np

# [VISUAL REASONING]
# An RC circuit schematic motivates Kirchhoff's law; in-place TransformMatchingTex
# carries the algebra from KVL to the solved ODE; a plotted exponential with
# time-constant markers (tau=63%, 5tau=99%) turns the formula into physical
# intuition about charging speed. A single central CONTENT stage is reused across
# three phases (circuit, derivation, plot) via cleanup arrays: fade circuit before
# equations, fade equations before plotting. Geometry stays within y in [-2.0, 2.5];
# subtitle band y < -2.8 stays empty.


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
        title = Text("RC Circuit Charging Response", color=WHITE, font_size=38)
        title.to_edge(UP)

        stage_center = np.array([0.0, 0.0, 0.0])

        loop = Rectangle(width=4.0, height=2.4, color=GREY_B)
        loop.move_to(stage_center + np.array([0, 0.2, 0]))

        resistor = Rectangle(width=1.2, height=0.4, color=ORANGE, fill_opacity=0.6)
        resistor.move_to(loop.get_center() + np.array([0, 1.2, 0]))

        cap_line1 = Line(start=[2.0, 0.6, 0], end=[2.0, -0.2, 0], color=BLUE)
        cap_line2 = Line(start=[2.3, 0.6, 0], end=[2.3, -0.2, 0], color=BLUE)
        battery_line = Line(start=[-2.0, 0.7, 0], end=[-2.0, -0.3, 0], color=RED)

        label_v0 = MathTex("V_0", color=RED).next_to(battery_line, LEFT, buff=0.25)
        label_r = MathTex("R", color=ORANGE).next_to(resistor, UP, buff=0.2)
        label_c = MathTex("C", color=BLUE).next_to(cap_line2, RIGHT, buff=0.25)

        current_arrow = Arrow(start=[-2.0, 1.4, 0], end=[-0.9, 1.4, 0], color=YELLOW)
        label_i = MathTex("i", color=YELLOW).next_to(current_arrow, UP, buff=0.15)

        kvl_eq = MathTex("V_0", "=", "R\\,i", "+", "V(t)", color=WHITE)
        kvl_eq.move_to(stage_center + np.array([0, 0.3, 0]))

        sub_eq = MathTex("V_0", "=", "RC\\,\\frac{dV}{dt}", "+", "V(t)", color=WHITE)
        sub_eq.move_to(stage_center + np.array([0, 0.3, 0]))

        sol_eq = MathTex("V(t) = V_0\\left(1 - e^{-t/RC}\\right)", color=GREEN)
        sol_eq.move_to(stage_center + np.array([0, 0.3, 0]))

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 1.2, 0.5],
            x_length=8,
            y_length=4,
            axis_config={"color": GREY_B},
        )
        axes.move_to(stage_center + np.array([0, -0.1, 0]))

        v_curve = axes.plot(lambda t: 1 - np.exp(-t), x_range=[0, 6], color=GREEN)

        asymptote = DashedLine(
            start=axes.c2p(0, 1),
            end=axes.c2p(6, 1),
            color=RED,
        )

        tau_line = DashedLine(
            start=axes.c2p(1, 0),
            end=axes.c2p(1, 0.63),
            color=YELLOW,
        )

        tau_dot = Dot(point=axes.c2p(1, 0.63), color=YELLOW, radius=0.08)
        tau_label = MathTex("\\tau = RC,\\ 63\\%", color=YELLOW, font_size=30)
        tau_label.next_to(tau_dot, UR, buff=0.15)

        fivetau_dot = Dot(point=axes.c2p(5, 0.99), color=TEAL, radius=0.08)
        fivetau_label = MathTex("5\\tau,\\ 99\\%", color=TEAL, font_size=30)
        fivetau_label.next_to(fivetau_dot, DR, buff=0.15)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Derive_and_visualize_a7cf812978/step_00.mp3")  # [auto-injected] duration=6.89s
        _audio_dur_0 = 6.89  # [audio-sync] actual TTS duration
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 3.000)
        self.set_subtitle("這是一個串聯 RC 電路：電源 V0 驅動電流通過電阻 R 流入電容 C。", run_time=_audio_dur_0)
        anim_time_1 = 3.000 * _scale_1
        self.play(Write(title), run_time=1.0)
        self.play(Create(loop), run_time=2.0)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Derive_and_visualize_a7cf812978/step_01.mp3")  # [auto-injected] duration=5.71s
        _audio_dur_1 = 5.71  # [audio-sync] actual TTS duration
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.000)
        self.set_subtitle("我們將電源、電阻與電容串聯排列在這個單一迴路上。", run_time=_audio_dur_1)
        anim_time_2 = 2.000 * _scale_2
        self.play(
            LaggedStart(
                Create(resistor),
                Create(battery_line),
                Create(cap_line1),
                Create(cap_line2),
                Write(label_v0),
                Write(label_r),
                Write(label_c),
                lag_ratio=0.15,
            ),
            run_time=2.0,
        )
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Derive_and_visualize_a7cf812978/step_02.mp3")  # [auto-injected] duration=4.66s
        _audio_dur_2 = 4.66  # [audio-sync] actual TTS duration
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 2.300)
        self.set_subtitle("當電容開始從電源充電時，電流 i 開始流動。", run_time=_audio_dur_2)
        anim_time_3 = 2.300 * _scale_3
        self.play(GrowArrow(current_arrow), Write(label_i), run_time=1.5)
        self.play(Indicate(current_arrow, color=YELLOW), run_time=0.8)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Derive_and_visualize_a7cf812978/step_03.mp3")  # [auto-injected] duration=6.00s
        _audio_dur_3 = 6.00  # [audio-sync] actual TTS duration
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 3.000)
        self.set_subtitle("克希荷夫電壓定律指出，電源電壓等於電阻壓降加上電容電壓。", run_time=_audio_dur_3)
        anim_time_4 = 3.000 * _scale_4
        self.play(
            FadeOut(loop, resistor, battery_line, cap_line1, cap_line2,
                    label_v0, label_r, label_c, current_arrow, label_i),
            run_time=1.0,
        )
        self.play(Write(kvl_eq), run_time=2.0)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Derive_and_visualize_a7cf812978/step_04.mp3")  # [auto-injected] duration=7.94s
        _audio_dur_4 = 7.94  # [audio-sync] actual TTS duration
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.800)
        self.set_subtitle("代入 i 等於 C 乘以 dV/dt，將電阻項轉換成 RC 乘以 dV/dt。", run_time=_audio_dur_4)
        anim_time_5 = 2.800 * _scale_5
        self.play(Indicate(kvl_eq, color=RED), run_time=0.8)
        self.play(TransformMatchingTex(kvl_eq, sub_eq), run_time=2.0)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(max(0.1, remaining_5))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Derive_and_visualize_a7cf812978/step_05.mp3")  # [auto-injected] duration=6.94s
        _audio_dur_5 = 6.94  # [audio-sync] actual TTS duration
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 2.500)
        self.set_subtitle("求解這個一階線性微分方程，得到電容電壓以一減指數的形式上升。", run_time=_audio_dur_5)
        anim_time_6 = 2.500 * _scale_6
        self.play(TransformMatchingTex(sub_eq, sol_eq), run_time=2.5)
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 + 0.1)
        self.wait(max(0.1, remaining_6))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Derive_and_visualize_a7cf812978/step_06.mp3")  # [auto-injected] duration=5.50s
        _audio_dur_6 = 5.50  # [audio-sync] actual TTS duration
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 3.000)
        self.set_subtitle("讓我們將這個電壓對時間作圖，看看電容實際上如何充電。", run_time=_audio_dur_6)
        anim_time_7 = 3.000 * _scale_7
        self.play(FadeOut(sol_eq), run_time=1.0)
        self.play(Create(axes), run_time=2.0)
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 + 0.1)
        self.wait(max(0.1, remaining_7))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Derive_and_visualize_a7cf812978/step_07.mp3")  # [auto-injected] duration=6.14s
        _audio_dur_7 = 6.14  # [audio-sync] actual TTS duration
        # Step 8
        _scale_8 = max(1.0, (_audio_dur_7 * 0.7) / 4.000)
        self.set_subtitle("電壓一開始急劇上升，接著彎曲並漸近地趨近 V0。", run_time=_audio_dur_7)
        anim_time_8 = 4.000 * _scale_8
        self.play(Create(v_curve), run_time=3.0)
        self.play(Create(asymptote), run_time=1.0)
        remaining_8 = max(0.1, _audio_dur_7 - anim_time_8 + 0.1)
        self.wait(max(0.1, remaining_8))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Derive_and_visualize_a7cf812978/step_08.mp3")  # [auto-injected] duration=7.06s
        _audio_dur_8 = 7.06  # [audio-sync] actual TTS duration
        # Step 9
        _scale_9 = max(1.0, (_audio_dur_8 * 0.7) / 3.600)
        self.set_subtitle("在一個時間常數 tau 等於 RC 時，電容達到滿充電量的百分之六十三。", run_time=_audio_dur_8)
        anim_time_9 = 3.600 * _scale_9
        self.play(Create(tau_line), run_time=2.0)
        self.play(FadeIn(tau_dot), Write(tau_label), run_time=0.8)
        self.play(Circumscribe(tau_dot, color=YELLOW), run_time=0.8)
        remaining_9 = max(0.1, _audio_dur_8 - anim_time_9 + 0.1)
        self.wait(max(0.1, remaining_9))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Derive_and_visualize_a7cf812978/step_09.mp3")  # [auto-injected] duration=6.74s
        _audio_dur_9 = 6.74  # [audio-sync] actual TTS duration
        # Step 10
        _scale_10 = max(1.0, (_audio_dur_9 * 0.7) / 2.800)
        self.set_subtitle("經過五個時間常數，電容約達百分之九十九充電，實際上已經完成。", run_time=_audio_dur_9)
        anim_time_10 = 2.800 * _scale_10
        self.play(FadeIn(fivetau_dot), Write(fivetau_label), run_time=2.0)
        self.play(Indicate(fivetau_dot, color=TEAL), run_time=0.8)
        remaining_10 = max(0.1, _audio_dur_9 - anim_time_10 + 0.1)
        self.wait(max(0.1, remaining_10))