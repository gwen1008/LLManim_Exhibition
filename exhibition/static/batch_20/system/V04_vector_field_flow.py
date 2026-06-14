from manim import *
import numpy as np

# [VISUAL REASONING]
# Pedagogical Goal: Build intuition for the rotation field F=(-y, x) by layering a grid,
# overlaying direction arrows that swirl counterclockwise, drawing closed streamline circles,
# then orbiting particles to visualize nonzero curl and closed circular flow.
# Layout: One NumberPlane centered at ORIGIN (y-extent <= 2.4 to avoid subtitle zone),
# vector arrows tiling it, concentric guide circles + orbiting dots on top.
# Title in HEADER, formula label pinned to upper-left corner.

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

        title = Text("The Rotation Field F(x,y) = (-y, x)", color=WHITE, font_size=36)
        title.to_edge(UP, buff=0.4)
        registry["title"] = title

        grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-2.4, 2.4, 1],
            background_line_style={"stroke_color": GREY, "stroke_opacity": 0.4},
        )
        grid.move_to(ORIGIN)
        registry["grid"] = grid

        formula_label = MathTex(r"\vec{F} = (-y,\; x)", color=YELLOW)
        formula_label.to_corner(UL, buff=0.6)
        registry["formula_label"] = formula_label

        field_func = lambda p: np.array([-p[1], p[0], 0])
        field_arrows = ArrowVectorField(
            field_func,
            x_range=[-5, 5, 1],
            y_range=[-2, 2, 1],
            colors=[BLUE, GREEN, RED],
            length_func=lambda norm: 0.4 * sigmoid(norm),
        )
        field_arrows.move_to(ORIGIN)
        registry["field_arrows"] = field_arrows

        circle_r1 = Circle(radius=1.0, color=TEAL, stroke_opacity=0.5, fill_opacity=0)
        circle_r1.move_to(ORIGIN)
        registry["circle_r1"] = circle_r1

        circle_r2 = Circle(radius=2.0, color=TEAL, stroke_opacity=0.5, fill_opacity=0)
        circle_r2.move_to(ORIGIN)
        registry["circle_r2"] = circle_r2

        dot_inner = Dot(point=[1.0, 0, 0], color=YELLOW, radius=0.1)
        registry["dot_inner"] = dot_inner

        dot_outer = Dot(point=[2.0, 0, 0], color=ORANGE, radius=0.1)
        registry["dot_outer"] = dot_outer

        dot_top = Dot(point=[0, 1.5, 0], color=GREEN, radius=0.1)
        registry["dot_top"] = dot_top

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V04_vector_field_flow_1781402222/media/audio/Visualize_the_rotati_bfa4bf281e/step_00_a13271a9.mp3")  # [auto-injected]
        _audio_dur_0 = 7.51  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 2.000))
        self.set_subtitle("我們先建立座標格線，作為旋轉場 F 等於負 y, x 的舞台。", run_time=_audio_dur_0)
        anim_time_1 = 2.000 * _scale_1
        self.play(Create(grid), run_time=(2.0)*_scale_1)
        self.play(Write(title), Write(formula_label), run_time=(1.0)*_scale_1)
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - (anim_time_1 + 1.0) + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V04_vector_field_flow_1781402222/media/audio/Visualize_the_rotati_bfa4bf281e/step_01_346b83a6.mp3")  # [auto-injected]
        _audio_dur_1 = 9.43  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 3.000))
        self.set_subtitle("現在疊上場的箭頭；注意每個箭頭都垂直於它的位置，繞著原點逆時針旋轉。", run_time=_audio_dur_1)
        anim_time_2 = 3.000 * _scale_2
        self.play(Create(field_arrows), run_time=(3.0)*_scale_2)
        self.wait(0.5)  # [Final Guard: removed empty self.play()]
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - (anim_time_2 + 1.0) + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V04_vector_field_flow_1781402222/media/audio/Visualize_the_rotati_bfa4bf281e/step_02_3941ea71.mp3")  # [auto-injected]
        _audio_dur_2 = 7.73  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 2.000))
        self.set_subtitle("沿著箭頭，粒子永遠不會逃脫；它們描繪出以原點為中心的封閉同心圓。", run_time=_audio_dur_2)
        anim_time_3 = 2.000 * _scale_3
        self.play(Create(circle_r1), Create(circle_r2), run_time=(2.0)*_scale_3)
        self.play(LaggedStart(
            FadeIn(dot_inner, scale=0.5),
            FadeIn(dot_outer, scale=0.5),
            FadeIn(dot_top, scale=0.5),
            lag_ratio=0.2,
        ), run_time=(1.0)*_scale_3)
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - (anim_time_3 + 1.0) + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V04_vector_field_flow_1781402222/media/audio/Visualize_the_rotati_bfa4bf281e/step_03_d75185ac.mp3")  # [auto-injected]
        _audio_dur_3 = 8.09  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 5.000))
        self.set_subtitle("釋放粒子，它們一起繞行，各自乘著自己的流線，被場帶著轉動。", run_time=_audio_dur_3)
        anim_time_4 = 5.000 * _scale_4
        self.play(
            Rotate(dot_inner, angle=2 * PI, about_point=ORIGIN, rate_func=linear),
            Rotate(dot_outer, angle=2 * PI, about_point=ORIGIN, rate_func=linear),
            Rotate(dot_top, angle=2 * PI, about_point=ORIGIN, rate_func=linear),
            run_time=(5.0)*_scale_4,
        )
        self.play(Indicate(dot_inner, color=RED))
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - (anim_time_4 + 1.0) + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V04_vector_field_flow_1781402222/media/audio/Visualize_the_rotati_bfa4bf281e/step_04_3b768028.mp3")  # [auto-injected]
        _audio_dur_4 = 7.75  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 2.500))
        self.set_subtitle("這些永遠閉合的迴圈揭示了場的非零旋度，以及它純粹的圓形、受流線束縛的流動。", run_time=_audio_dur_4)
        anim_time_5 = 2.500 * _scale_5
        self.play(Indicate(circle_r1, color=TEAL), run_time=(2.5)*_scale_5)
        self.play(Circumscribe(circle_r2, color=TEAL))
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - (anim_time_5 + 1.0) + 0.1))
        self.wait(remaining_5)