from manim import *
import numpy as np


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
        # [VISUAL REASONING]
        # 1. Goal: Visualize the slope field of dy/dx = x - y and two solution curves converging to y = x - 1.
        # 2. Layout: Title + equation in HEADER, single centered Axes in CONTENT holding slope field, asymptote, dots, curves.
        # 3. Flow: axes -> slope field sweep -> asymptote -> red curve from (0,2) -> blue curve from (0,-2).

        registry = {}

        title = Text("Slope Field of dy/dx = x - y", color=WHITE, font_size=36)
        title.to_edge(UP, buff=0.35)
        registry["title"] = title

        equation = MathTex(r"\frac{dy}{dx} = x - y", color=YELLOW)
        equation.next_to(title, DOWN, buff=0.15)
        registry["equation"] = equation

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=8,
            y_length=5,
            axis_config={"color": GREY, "include_tip": True},
        )
        axes.move_to(ORIGIN + np.array([0, -0.2, 0]))
        registry["axes"] = axes

        slope_field = VGroup()
        for x in range(-3, 4):
            for y in range(-2, 3):
                angle = np.arctan(x - y)
                seg = Line(LEFT * 0.15, RIGHT * 0.15, color=GREY_B, stroke_width=2)
                seg.rotate(angle)
                seg.move_to(axes.c2p(x, y))
                slope_field.add(seg)
        registry["slope_field"] = slope_field

        asymptote = axes.plot(lambda x: x - 1, x_range=[-4, 4], color=GREEN, stroke_width=3)
        registry["asymptote"] = asymptote

        asym_label = MathTex("y = x - 1", color=GREEN)
        asym_label.next_to(asymptote, DR, buff=0.15)
        registry["asym_label"] = asym_label

        dot1 = Dot(axes.c2p(0, 2), color=RED, radius=0.09)
        registry["dot1"] = dot1

        dot2 = Dot(axes.c2p(0, -2), color=BLUE, radius=0.09)
        registry["dot2"] = dot2

        curve1 = axes.plot(lambda x: x - 1 + 3 * np.exp(-x), x_range=[-1.0, 4.0], color=RED, stroke_width=4)
        registry["curve1"] = curve1

        curve2 = axes.plot(lambda x: x - 1 - np.exp(-x), x_range=[0.0, 4.0], color=BLUE, stroke_width=4)
        registry["curve2"] = curve2

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q08_slope_field_1781379315/media/audio/Solve_the_first_orde_17a070ccda/step_00_bb73c6ed.mp3")  # [auto-injected]
        _audio_dur_0 = 9.38  # [audio-sync]
        # Step 1
        self.set_subtitle("我們從一階方程式 dy/dx 等於 x 減 y 開始，它在平面上每一點都指定了一個斜率。", run_time=_audio_dur_0)
        anim_time_1 = 0.0
        self.play(Write(title), run_time=1.0)
        anim_time_1 += 1.0
        self.play(Write(equation), run_time=1.0)
        anim_time_1 += 1.0
        self.play(Create(axes), run_time=1.5)
        anim_time_1 += 1.5
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        anim_time_1 += 1.0
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q08_slope_field_1781379315/media/audio/Solve_the_first_orde_17a070ccda/step_01_af199caf.mp3")  # [auto-injected]
        _audio_dur_1 = 8.28  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 3.000))
        self.set_subtitle("在每個格點上，我們畫一條斜率等於 x 減 y 的小線段，呈現出方向場。", run_time=_audio_dur_1)
        anim_time_2 = 3.000 * _scale_2
        self.play(LaggedStart(*[Create(seg) for seg in slope_field], lag_ratio=0.05, run_time=(3.0)*_scale_2))
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q08_slope_field_1781379315/media/audio/Solve_the_first_orde_17a070ccda/step_02_a9a2956c.mp3")  # [auto-injected]
        _audio_dur_2 = 8.26  # [audio-sync]
        # Step 3
        self.set_subtitle("注意線段沿著 y 等於 x 減一排列，這正是每條解都會趨近的漸近線。", run_time=_audio_dur_2)
        anim_time_3 = 0.0
        self.play(Create(asymptote), run_time=2.0)
        anim_time_3 += 2.0
        self.play(Write(asym_label), run_time=0.8)
        anim_time_3 += 0.8
        self.play(Indicate(asymptote, color=GREEN))
        anim_time_3 += 1.0
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q08_slope_field_1781379315/media/audio/Solve_the_first_orde_17a070ccda/step_03_61a3112c.mp3")  # [auto-injected]
        _audio_dur_3 = 10.30  # [audio-sync]
        # Step 4
        self.set_subtitle("從 (0, 2) 出發，曲線 y 等於 x 減一加三倍 e 的負 x 次方，順著方向場向下逼近漸近線。", run_time=_audio_dur_3)
        anim_time_4 = 0.0
        self.play(FadeIn(dot1), run_time=0.5)
        anim_time_4 += 0.5
        self.play(Indicate(dot1, color=RED))
        anim_time_4 += 1.0
        self.play(Create(curve1), run_time=3.0)
        anim_time_4 += 3.0
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q08_slope_field_1781379315/media/audio/Solve_the_first_orde_17a070ccda/step_04_d42c981a.mp3")  # [auto-injected]
        _audio_dur_4 = 11.40  # [audio-sync]
        # Step 5
        self.set_subtitle("從 (0, -2) 出發，曲線 y 等於 x 減一減 e 的負 x 次方向上攀升，兩條解都收斂到同一條直線。", run_time=_audio_dur_4)
        anim_time_5 = 0.0
        self.play(FadeIn(dot2), run_time=0.5)
        anim_time_5 += 0.5
        self.play(Indicate(dot2, color=BLUE))
        anim_time_5 += 1.0
        self.play(Create(curve2), run_time=3.0)
        anim_time_5 += 3.0
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)