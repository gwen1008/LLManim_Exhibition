from manim import *

# [VISUAL REASONING]
# Left half: unit circle (center -3,0, radius 2) with reference axes, a yellow
# y=1/2 sine-level line, and two intersection radii (BLUE 30°, GREEN 150°).
# Right column near x=3: equation solutions stacked vertically — two principal
# solutions then a braced general solution showing periodicity.
# Each step is one continuous LaggedStart filling its audio window.

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
        self._instrumentor = SceneInstrumentor(self)
        self._sm = SubtitleManager(self)
        self.set_subtitle = self._sm.show
        registry = {}

        title = MathTex(r"\sin\theta = \frac{1}{2}").to_edge(UP)
        registry["title"] = title

        axes_small = Axes(
            x_range=[-1.3, 1.3, 1],
            y_range=[-1.3, 1.3, 1],
            x_length=4,
            y_length=4,
        ).move_to([-3, 0, 0])
        registry["axes_small"] = axes_small

        unit_circle = Circle(radius=2, color=WHITE).move_to([-3, 0, 0])
        registry["unit_circle"] = unit_circle

        sine_level_line = DashedLine(
            start=[-5.2, 1.0, 0], end=[-0.8, 1.0, 0], color=YELLOW
        )
        registry["sine_level_line"] = sine_level_line

        radius_30 = Line(start=[-3, 0, 0], end=[-1.27, 1.0, 0], color=BLUE)
        registry["radius_30"] = radius_30

        radius_150 = Line(start=[-3, 0, 0], end=[-4.73, 1.0, 0], color=GREEN)
        registry["radius_150"] = radius_150

        dot_30 = Dot(point=[-1.27, 1.0, 0], color=BLUE)
        registry["dot_30"] = dot_30

        dot_150 = Dot(point=[-4.73, 1.0, 0], color=GREEN)
        registry["dot_150"] = dot_150

        label_30 = MathTex(r"30^\circ", color=BLUE).next_to(dot_30, UR, buff=0.15)
        registry["label_30"] = label_30

        label_150 = MathTex(r"150^\circ", color=GREEN).next_to(dot_150, UL, buff=0.15)
        registry["label_150"] = label_150

        sol_first = MathTex(r"\theta = 30^\circ", color=BLUE).move_to([3, 1.2, 0])
        registry["sol_first"] = sol_first

        sol_second = MathTex(r"\theta = 150^\circ", color=GREEN).move_to([3, 0.3, 0])
        registry["sol_second"] = sol_second

        general_sol = MathTex(
            r"\theta = 30^\circ + 360^\circ k",
            r"\theta = 150^\circ + 360^\circ k",
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3, -1.2, 0])
        registry["general_sol"] = general_sol

        general_brace = Brace(general_sol, direction=[-1, 0, 0])
        registry["general_brace"] = general_brace

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H02_sin_equation_1780241950/media/audio/Solve_the_trigonomet_3071f57192/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 9.91  # [audio-sync]
        # Step 1
        anim_time_1 = min((_audio_dur_0), max(0.6 * _audio_dur_0, min((_audio_dur_0), 3.0)))
        tracing_dot = Dot(color=YELLOW).move_to(unit_circle.point_at_angle(0))
        self.play(
            LaggedStart(
                Write(title),
                Create(axes_small),
                Create(unit_circle),
                FadeIn(tracing_dot),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1 + max(0.0, _audio_dur_0 - anim_time_1))
        self.remove(tracing_dot)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H02_sin_equation_1780241950/media/audio/Solve_the_trigonomet_3071f57192/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 11.52  # [audio-sync]
        # Step 2
        anim_time_2 = min((_audio_dur_1), max(0.6 * _audio_dur_1, min((_audio_dur_1), 3.0)))
        self.set_subtitle("在高度二分之一處畫一條水平線，")
        self.play(
            LaggedStart(
                Create(sine_level_line),
                FadeIn(dot_30),
                FadeIn(dot_150),
                AnimationGroup(Indicate(dot_30), Indicate(dot_150)),
                lag_ratio=0.25,
                run_time=anim_time_2,
            )
        )
        # 逐句字幕（拆 2 句，剩餘旁白時間逐句輪播）
        _remain = max(0.1, _audio_dur_1 - anim_time_2)
        _seg = _remain / 2
        self.wait(_seg)  # 第1句撐
        self.set_subtitle("它與圓相交於兩個位置。")
        self.wait(_seg)  # 末句撐到結束

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H02_sin_equation_1780241950/media/audio/Solve_the_trigonomet_3071f57192/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 9.00  # [audio-sync]
        # Step 3
        anim_time_3 = min((_audio_dur_2), max(0.6 * _audio_dur_2, min((_audio_dur_2), 3.0)))
        self.set_subtitle("第一個交點在第一象限的三十度，")
        self.play(
            LaggedStart(
                Create(radius_30),
                Write(label_30),
                Create(radius_150),
                Write(label_150),
                lag_ratio=0.25,
                run_time=anim_time_3,
            )
        )
        # 逐句字幕（拆 3 句，剩餘旁白時間逐句輪播）
        _remain = max(0.1, _audio_dur_2 - anim_time_3)
        _seg = _remain / 3
        self.wait(_seg)  # 第1句撐
        self.set_subtitle("第二個是它在第二象限的鏡像，")
        self.wait(_seg)
        self.set_subtitle("位於一百五十度。")
        self.wait(_seg)  # 末句撐到結束

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H02_sin_equation_1780241950/media/audio/Solve_the_trigonomet_3071f57192/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 10.20  # [audio-sync]
        # Step 4
        anim_time_4 = min((_audio_dur_3), max(0.6 * _audio_dur_3, min((_audio_dur_3), 3.0)))
        self.set_subtitle("所以兩個主要解是 θ 等於三十度與 θ 等於一百五十度，")
        self.play(
            LaggedStart(
                Write(sol_first),
                Indicate(dot_30),
                Write(sol_second),
                Indicate(dot_150),
                lag_ratio=0.25,
                run_time=anim_time_4,
            )
        )
        # 逐句字幕（拆 2 句，剩餘旁白時間逐句輪播）
        _remain = max(0.1, _audio_dur_3 - anim_time_4)
        _seg = _remain / 2
        self.wait(_seg)  # 第1句撐
        self.set_subtitle("這是一圈之內的答案。")
        self.wait(_seg)  # 末句撐到結束

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_H02_sin_equation_1780241950/media/audio/Solve_the_trigonomet_3071f57192/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 13.75  # [audio-sync]
        # Step 5
        anim_time_5 = min((_audio_dur_4), max(0.6 * _audio_dur_4, min((_audio_dur_4), 3.0)))
        self.set_subtitle("因為正弦每三百六十度重複一次，")
        self.play(
            LaggedStart(
                GrowFromCenter(general_brace),
                Write(general_sol[0]),
                Write(general_sol[1]),
                lag_ratio=0.25,
                run_time=anim_time_5,
            )
        )
        # 逐句字幕（拆 3 句，剩餘旁白時間逐句輪播）
        _remain = max(0.1, _audio_dur_4 - anim_time_5)
        _seg = _remain / 3
        self.wait(_seg)  # 第1句撐
        self.set_subtitle("加上任意整數圈，")
        self.wait(_seg)
        self.set_subtitle("得到通解 θ 等於三十加 360k 與一百五十加 360k。")
        self.wait(_seg)  # 末句撐到結束
