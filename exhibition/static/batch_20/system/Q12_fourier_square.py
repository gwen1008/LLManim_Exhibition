from manim import *
import numpy as np

# [VISUAL REASONING]
# A single shared Axes hosts a fixed dashed grey square wave reference plus an
# evolving partial-sum Fourier curve. By morphing S1 -> S3 -> S9 with
# ReplacementTransform while the square wave stays put, the viewer perceives
# convergence and the persistent Gibbs edge overshoot. The bottom formula ties
# the symbolic partial sum to the visual, and a final red arrow + label call out
# the ~9% overshoot near the discontinuity.

class SubtitleManager:
    """Auto-injected by RefiningLoop.pre_render_patch. Non-blocking subtitle (instant add/remove) —
    runs in parallel with animations and never stalls the main timeline.
    Does NOT use add_updater opacity tweening (broken on manim CE 0.19: VGroup.set_opacity(0)
    on a Text cannot be reversed inside an updater → subtitle stays invisible)."""
    MAX_WIDTH = 12.5
    Y_POSITION = 3.2 * DOWN

    def __init__(self, scene, font_size=28):
        self.scene = scene
        self.font_size = font_size
        self._current = None

    def show(self, text_str, run_time=1.0):
        # 瞬間顯示，不呼叫 scene.play/scene.wait → 不消耗時間軸（非阻塞）。
        # opacity 維持預設=1（絕不 set_opacity(0)），確保字幕一定可見。
        s = str(text_str).strip()
        if not s:
            return
        text_mob = Text(s, font_size=self.font_size, color=WHITE, weight="BOLD")
        bg = BackgroundRectangle(text_mob, color=BLACK, fill_opacity=0.75, buff=0.15)
        new_mob = VGroup(bg, text_mob).move_to(self.Y_POSITION)
        if new_mob.width > self.MAX_WIDTH:
            new_mob.scale_to_fit_width(self.MAX_WIDTH)
        if self._current is not None:
            self.scene.remove(self._current)
        self.scene.add(new_mob)
        self._current = new_mob

    def clear(self, run_time=0.0):
        if self._current is not None:
            self.scene.remove(self._current)
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

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q12_fourier_square_1781379459/media/audio/Use_Fourier_series_t_11dc7dcb0a/step_00_70c365e0.mp3")  # [auto-injected]
        _audio_dur_0 = 6.10  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 2.000))
        title = Text("Fourier Series: Building a Square Wave", color=WHITE, font_size=36)
        title.move_to([0, 3.0, 0])
        registry["title"] = title

        axes = Axes(
            x_range=[-3.14, 3.14, 1.57],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"color": GREY},
        )
        axes.move_to(ORIGIN)
        registry["axes"] = axes

        square_wave = axes.plot(
            lambda x: np.sign(np.sin(x)),
            x_range=[-3.14, 3.14, 0.01],
            use_smoothing=False,
            color=GREY_B,
        )
        square_wave = DashedVMobject(square_wave, num_dashes=80)
        registry["square_wave"] = square_wave

        formula = MathTex(
            r"S_N(x)=\frac{4}{\pi}\sum_{n\,odd}^{N}\frac{\sin(nx)}{n}",
            color=WHITE,
        )
        formula.move_to([0, -2.3, 0])
        registry["formula"] = formula

        self.set_subtitle("這是我們想要僅用正弦函數重建的理想方波。", run_time=_audio_dur_0)
        anim_time_1 = 2.000 * _scale_1
        self.play(Create(axes), run_time=(2.0)*_scale_1)
        self.play(Create(square_wave), Write(formula), Write(title), run_time=(1.5)*_scale_1)
        self.play(Circumscribe(square_wave, color=YELLOW))
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - (anim_time_1 + 1.5 + 1.0) + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q12_fourier_square_1781379459/media/audio/Use_Fourier_series_t_11dc7dcb0a/step_01_ba592fda.mp3")  # [auto-injected]
        _audio_dur_1 = 5.69  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 2.000))
        curve_n1 = axes.plot(
            lambda x: (4 / np.pi) * np.sin(x),
            x_range=[-3.14, 3.14, 0.01],
            color=YELLOW,
        )
        registry["curve_n1"] = curve_n1

        self.set_subtitle("第一諧波是係數為四除以 π 的單一正弦波。", run_time=_audio_dur_1)
        anim_time_2 = 2.000 * _scale_2
        self.play(Create(curve_n1), run_time=(2.0)*_scale_2)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - (anim_time_2 + 1.0) + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q12_fourier_square_1781379459/media/audio/Use_Fourier_series_t_11dc7dcb0a/step_02_f8a27404.mp3")  # [auto-injected]
        _audio_dur_2 = 6.19  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 2.000))
        curve_n3 = axes.plot(
            lambda x: (4 / np.pi) * (np.sin(x) + np.sin(3 * x) / 3),
            x_range=[-3.14, 3.14, 0.01],
            color=GOLD,
        )
        registry["curve_n3"] = curve_n3

        self.set_subtitle("加入第三諧波後，頂部變平、邊緣更陡，更接近目標形狀。", run_time=_audio_dur_2)
        anim_time_3 = 2.000 * _scale_3
        self.play(ReplacementTransform(curve_n1, curve_n3), run_time=(2.0)*_scale_3)
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q12_fourier_square_1781379459/media/audio/Use_Fourier_series_t_11dc7dcb0a/step_03_090bf320.mp3")  # [auto-injected]
        _audio_dur_3 = 7.61  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 2.500))
        curve_n5 = axes.plot(
            lambda x: (4 / np.pi) * (np.sin(x) + np.sin(3 * x) / 3 + np.sin(5 * x) / 5),
            x_range=[-3.14, 3.14, 0.01],
            color=ORANGE,
        )
        registry["curve_n5"] = curve_n5

        curve_n9 = axes.plot(
            lambda x: (4 / np.pi) * (
                np.sin(x)
                + np.sin(3 * x) / 3
                + np.sin(5 * x) / 5
                + np.sin(7 * x) / 7
                + np.sin(9 * x) / 9
            ),
            x_range=[-3.14, 3.14, 0.01],
            color=RED,
        )
        registry["curve_n9"] = curve_n9

        self.set_subtitle("再加入第五、第七與第九諧波，曲線幾乎處處貼合方波。", run_time=_audio_dur_3)
        anim_time_4 = 2.500 * _scale_4
        self.play(ReplacementTransform(curve_n3, curve_n5), run_time=(1.2)*_scale_4)
        self.play(ReplacementTransform(curve_n5, curve_n9), run_time=(1.3)*_scale_4)
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q12_fourier_square_1781379459/media/audio/Use_Fourier_series_t_11dc7dcb0a/step_04_643281cd.mp3")  # [auto-injected]
        _audio_dur_4 = 6.48  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 1.500))
        gibbs_arrow = Arrow(
            start=[1.2, 2.0, 0],
            end=[0.4, 1.25, 0],
            color=RED,
        )
        registry["gibbs_arrow"] = gibbs_arrow

        gibbs_label = Text("Gibbs overshoot (~9%)", color=RED, font_size=26)
        gibbs_label.next_to(gibbs_arrow, UP, buff=0.15)
        registry["gibbs_label"] = gibbs_label

        self.set_subtitle("注意每個邊緣附近頑固的尖峰始終不會縮小：這就是吉布斯過衝現象。", run_time=_audio_dur_4)
        anim_time_5 = 1.500 * _scale_5
        self.play(Create(gibbs_arrow), FadeIn(gibbs_label), run_time=(1.5)*_scale_5)
        self.play(Indicate(gibbs_arrow, color=RED))
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - (anim_time_5 + 1.0) + 0.1))
        self.wait(remaining_5)