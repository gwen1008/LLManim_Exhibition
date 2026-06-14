from manim import *
import numpy as np

# [VISUAL REASONING]
# An anisotropic (elongated) loss landscape demonstrates gradient descent's
# characteristic zigzag convergence. Concentric ellipses encode loss level sets,
# and a precomputed trajectory of dots connected by negative-gradient arrows
# makes each iteration's geometry explicit. All coordinates are precomputed for
# f(x,y)=x^2/4+y^2 with learning rate 0.7 (scaled 0.8), centered at ORIGIN.


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

        title = Text("Gradient Descent on a Loss Surface", color=WHITE, font_size=36)
        title.to_edge(UP, buff=0.4)
        registry["title"] = title

        contour1 = Ellipse(width=7.0, height=3.4, color=BLUE, stroke_opacity=0.5).move_to(ORIGIN)
        contour2 = Ellipse(width=5.2, height=2.5, color=BLUE, stroke_opacity=0.6).move_to(ORIGIN)
        contour3 = Ellipse(width=3.6, height=1.7, color=TEAL, stroke_opacity=0.7).move_to(ORIGIN)
        contour4 = Ellipse(width=2.0, height=0.95, color=TEAL, stroke_opacity=0.8).move_to(ORIGIN)
        registry["contour1"] = contour1
        registry["contour2"] = contour2
        registry["contour3"] = contour3
        registry["contour4"] = contour4

        min_dot = Dot(point=[0, 0, 0], color=GREEN, radius=0.1)
        registry["min_dot"] = min_dot
        min_label = MathTex(r"\theta^*", color=GREEN).next_to(min_dot, DOWN, buff=0.2)
        registry["min_label"] = min_label

        d0 = Dot(point=[-3.2, 1.44, 0], color=RED, radius=0.09)
        registry["d0"] = d0
        d0_label = MathTex(r"\theta_0", color=RED).next_to(d0, UP, buff=0.15)
        registry["d0_label"] = d0_label

        arr1 = Arrow(start=[-3.2, 1.44, 0], end=[-2.08, -0.576, 0], color=ORANGE, buff=0.05, stroke_width=4)
        d1 = Dot(point=[-2.08, -0.576, 0], color=YELLOW, radius=0.07)
        arr2 = Arrow(start=[-2.08, -0.576, 0], end=[-1.35, 0.23, 0], color=ORANGE, buff=0.05, stroke_width=4)
        d2 = Dot(point=[-1.35, 0.23, 0], color=YELLOW, radius=0.07)
        arr3 = Arrow(start=[-1.35, 0.23, 0], end=[-0.88, -0.096, 0], color=ORANGE, buff=0.05, stroke_width=4)
        d3 = Dot(point=[-0.88, -0.096, 0], color=YELLOW, radius=0.07)
        arr4 = Arrow(start=[-0.88, -0.096, 0], end=[-0.57, 0.04, 0], color=ORANGE, buff=0.04, stroke_width=3)
        d4 = Dot(point=[-0.57, 0.04, 0], color=YELLOW, radius=0.07)
        arr5 = Arrow(start=[-0.57, 0.04, 0], end=[-0.2, -0.01, 0], color=ORANGE, buff=0.04, stroke_width=3)
        d5 = Dot(point=[-0.2, -0.01, 0], color=YELLOW, radius=0.07)
        registry["arr1"] = arr1
        registry["d1"] = d1
        registry["arr2"] = arr2
        registry["d2"] = d2
        registry["arr3"] = arr3
        registry["d3"] = d3
        registry["arr4"] = arr4
        registry["d4"] = d4
        registry["arr5"] = arr5
        registry["d5"] = d5

        update_rule = MathTex(r"\theta_{k+1}=\theta_k-\eta\nabla f(\theta_k)", color=WHITE)
        update_rule.to_edge(DOWN, buff=0.55)
        registry["update_rule"] = update_rule

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N03_gradient_descent_1780053796/media/audio/On_a_contour_map_of__67fca5a634/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 6.82  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.000)
        self.set_subtitle("這些巢狀的橢圓是等高線，每一圈標記著曲面上損失相等的點。", run_time=_audio_dur_0)
        anim_time_1 = 1.000 * _scale_1
        self.play(Write(title), run_time=anim_time_1)
        self.play(
            LaggedStart(
                Create(contour1),
                Create(contour2),
                Create(contour3),
                Create(contour4),
                lag_ratio=0.2,
            ),
            run_time=2.0,
        )
        remaining_1 = max(0.1, _audio_dur_0 - (anim_time_1 + 2.0) + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N03_gradient_descent_1780053796/media/audio/On_a_contour_map_of__67fca5a634/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 5.98  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 1.500)
        self.set_subtitle("中心是我們尋找的最小值，也就是使損失盡可能小的參數。", run_time=_audio_dur_1)
        anim_time_2 = 1.500 * _scale_2
        self.play(FadeIn(min_dot), FadeIn(min_label), run_time=anim_time_2)
        self.play(Circumscribe(min_dot, color=GREEN))
        remaining_2 = max(0.1, _audio_dur_1 - (anim_time_2 + 1.0) + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N03_gradient_descent_1780053796/media/audio/On_a_contour_map_of__67fca5a634/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 5.62  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 1.500)
        self.set_subtitle("我們從一個初始猜測開始，它落在外圈上，代表它的損失仍然很高。", run_time=_audio_dur_2)
        anim_time_3 = 1.500 * _scale_3
        self.play(FadeIn(d0), FadeIn(d0_label), run_time=anim_time_3)
        self.play(Indicate(d0, color=RED))
        remaining_3 = max(0.1, _audio_dur_2 - (anim_time_3 + 1.0) + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N03_gradient_descent_1780053796/media/audio/On_a_contour_map_of__67fca5a634/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 7.54  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 1.500)
        self.set_subtitle("每次迭代沿著負梯度方向前進，這是讓損失下降最快的最陡下降路徑。", run_time=_audio_dur_3)
        anim_time_4 = 1.500 * _scale_4
        self.play(Write(update_rule), run_time=0.8)
        self.play(GrowArrow(arr1), run_time=anim_time_4)
        self.play(FadeIn(d1), run_time=0.5)
        self.play(Indicate(arr1, color=ORANGE))
        remaining_4 = max(0.1, _audio_dur_3 - (0.8 + anim_time_4 + 0.5 + 1.0) + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N03_gradient_descent_1780053796/media/audio/On_a_contour_map_of__67fca5a634/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.36  # [audio-sync]
        # Step 5
        self.set_subtitle("由於山谷是狹長的，軌跡在橫越時來回鋸齒前進，同時穩定地往內推進。", run_time=_audio_dur_4)
        self.play(GrowArrow(arr2), run_time=1.0)
        self.play(FadeIn(d2), run_time=0.4)
        self.play(GrowArrow(arr3), run_time=1.0)
        self.play(FadeIn(d3), run_time=0.4)
        remaining_5 = max(0.1, _audio_dur_4 - 2.8 + 0.1)
        self.wait(remaining_5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_N03_gradient_descent_1780053796/media/audio/On_a_contour_map_of__67fca5a634/step_05.mp3")  # [auto-injected]
        _audio_dur_5 = 6.22  # [audio-sync]
        # Step 6
        self.set_subtitle("接近底部時梯度趨於平坦，步伐隨之縮小，於是軌跡收斂到最小值。", run_time=_audio_dur_5)
        self.play(GrowArrow(arr4), run_time=1.0)
        self.play(FadeIn(d4), run_time=0.4)
        self.play(GrowArrow(arr5), run_time=1.0)
        self.play(FadeIn(d5), run_time=0.4)
        self.play(Circumscribe(min_dot, color=GREEN))
        remaining_6 = max(0.1, _audio_dur_5 - 3.8 + 0.1)
        self.wait(remaining_6)