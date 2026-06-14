# [VISUAL REASONING]
# A contour map (concentric circles) represents the 2D loss surface with the
# minimum at the origin. A zigzag trajectory of dots and segments shows gradient
# descent stepping downhill, with a gradient arrow on the first step and a
# convergence ring at the end. Each step is a single LaggedStart spanning its
# narration window per LITE MODE.

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
        title = Text("Gradient Descent on a Loss Surface", font_size=34).to_edge(UP)

        axes_main = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
        ).move_to(ORIGIN)

        contour1 = Circle(radius=0.7, color="#4FC3F7").move_to(ORIGIN)
        contour2 = Circle(radius=1.5, color="#4FC3F7").move_to(ORIGIN)
        contour3 = Circle(radius=2.4, color="#4FC3F7").move_to(ORIGIN)
        contour4 = Circle(radius=3.3, color="#4FC3F7").move_to(ORIGIN)

        min_dot = Dot(point=[0, 0, 0], radius=0.09, color="#FFD54F").move_to(ORIGIN)
        min_label = MathTex(r"\theta^*", font_size=30).next_to(min_dot, DOWN)

        start_dot = Dot(point=[3, 2.5, 0], radius=0.09, color="#FF7043")
        start_label = MathTex(r"\theta_0", font_size=30).next_to(start_dot, UR, buff=0.1)

        dot1 = Dot(point=[2.4, -1.5, 0], radius=0.07, color="#FF7043")
        dot2 = Dot(point=[1.9, 1.0, 0], radius=0.07, color="#FF7043")
        dot3 = Dot(point=[1.5, -0.6, 0], radius=0.07, color="#FF7043")
        dot4 = Dot(point=[1.0, 0.4, 0], radius=0.07, color="#FF7043")
        dot5 = Dot(point=[0.6, -0.2, 0], radius=0.07, color="#FF7043")
        dot6 = Dot(point=[0.25, 0.08, 0], radius=0.06, color="#FF7043")

        grad_arrow = Arrow(start=[3, 2.5, 0], end=[2.4, -1.5, 0], color="#E040FB", buff=0.0)

        seg1 = Line(start=[3, 2.5, 0], end=[2.4, -1.5, 0], color="#FFFFFF")
        seg2 = Line(start=[2.4, -1.5, 0], end=[1.9, 1.0, 0], color="#FFFFFF")
        seg3 = Line(start=[1.9, 1.0, 0], end=[1.5, -0.6, 0], color="#FFFFFF")
        seg4 = Line(start=[1.5, -0.6, 0], end=[1.0, 0.4, 0], color="#FFFFFF")
        seg5 = Line(start=[1.0, 0.4, 0], end=[0.6, -0.2, 0], color="#FFFFFF")
        seg6 = Line(start=[0.6, -0.2, 0], end=[0.25, 0.08, 0], color="#FFFFFF")
        seg7 = Line(start=[0.25, 0.08, 0], end=[0, 0, 0], color="#FFFFFF")

        update_eq = MathTex(
            r"\theta_{k+1} = \theta_k - \eta\,\nabla L(\theta_k)", font_size=32
        ).move_to(np.array([0, -2.0, 0]))

        converge_ring = Circle(radius=0.3, color="#FFD54F").move_to(ORIGIN)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N03_gradient_descent_1780054024/media/audio/On_the_contour_map_o_3868394a1d/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 9.02  # [audio-sync]
        # Step 1
        self.set_subtitle("這是一個二維損失曲面，畫成等高線圖；每一個圈是一條等位線，明亮的中心標記我們想要抵達的最小值。", run_time=_audio_dur_0)
        anim_time_1 = _audio_dur_0
        self.play(
            LaggedStart(
                Write(title),
                Create(axes_main),
                AnimationGroup(
                    Create(contour4),
                    Create(contour3),
                    Create(contour2),
                    Create(contour1),
                    lag_ratio=0.2,
                ),
                AnimationGroup(FadeIn(min_dot), Write(min_label)),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N03_gradient_descent_1780054024/media/audio/On_the_contour_map_o_3868394a1d/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 6.53  # [audio-sync]
        # Step 2
        self.set_subtitle("我們從一個初始猜測 theta-zero 出發，它位於遠處的高等高線上，損失值很大。", run_time=_audio_dur_1)
        anim_time_2 = _audio_dur_1
        self.play(
            LaggedStart(
                GrowFromCenter(start_dot),
                Write(start_label),
                Write(update_eq),
                Indicate(start_dot),
                lag_ratio=0.25,
                run_time=anim_time_2,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N03_gradient_descent_1780054024/media/audio/On_the_contour_map_o_3868394a1d/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 8.64  # [audio-sync]
        # Step 3
        self.set_subtitle("我們計算梯度，然後沿著負梯度方向、依學習率縮放後邁出一步，往較低的等高線下坡移動。", run_time=_audio_dur_2)
        anim_time_3 = _audio_dur_2
        self.play(
            LaggedStart(
                GrowArrow(grad_arrow),
                Create(seg1),
                GrowFromCenter(dot1),
                Indicate(update_eq),
                lag_ratio=0.25,
                run_time=anim_time_3,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N03_gradient_descent_1780054024/media/audio/On_the_contour_map_o_3868394a1d/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 8.93  # [audio-sync]
        # Step 4
        self.play(FadeOut(grad_arrow), run_time=0.3)
        self.set_subtitle("不斷重複這個更新，軌跡在山谷間來回曲折，每一步都比前一步短，逐漸逼近最小值。", run_time=_audio_dur_3)
        anim_time_4 = max(0.1, _audio_dur_3 - 0.3)
        self.play(
            LaggedStart(
                AnimationGroup(Create(seg2), GrowFromCenter(dot2)),
                AnimationGroup(Create(seg3), GrowFromCenter(dot3)),
                AnimationGroup(Create(seg4), GrowFromCenter(dot4)),
                AnimationGroup(Create(seg5), GrowFromCenter(dot5)),
                AnimationGroup(Create(seg6), GrowFromCenter(dot6)),
                lag_ratio=0.3,
                run_time=anim_time_4,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_N03_gradient_descent_1780054024/media/audio/On_the_contour_map_o_3868394a1d/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 7.90  # [audio-sync]
        # Step 5
        self.set_subtitle("最後步伐消失在中心：演算法已經收斂到 theta-star，也就是損失曲面的最小值。", run_time=_audio_dur_4)
        anim_time_5 = _audio_dur_4
        self.play(
            LaggedStart(
                Create(seg7),
                Create(converge_ring),
                ScaleInPlace(min_dot, 1.6),
                Indicate(min_label),
                lag_ratio=0.25,
                run_time=anim_time_5,
            )
        )
        self.wait(0.1)