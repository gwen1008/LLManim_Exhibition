from manim import *

# [VISUAL REASONING]
# The Director wants viewers to literally watch the conformal map w = z^2 bend a
# square grid into confocal parabolas. We build a live NumberPlane (unit-length=1 so
# the blueprint's absolute coordinates align with the gridlines), overlay one yellow
# vertical and one red horizontal highlight line plus a green right-angle marker at
# their (1,1) crossing. We then apply the SAME apply_complex_function(z -> z**2) to the
# plane and both lines together so they deform in sync. Scaling the whole stage to 0.9
# keeps the z^2-grown parabolas inside the safe frame. Finally we Indicate the bent
# parabolas and Circumscribe the still-perpendicular angle marker to prove conformality.

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

        # Title (HEADER)
        title = MathTex(r"Complex Map  w = z^2", color=WHITE)
        title.to_edge(UP)
        registry["title"] = title

        # Plane (CONTENT) — unit length 1 so blueprint coords match gridlines
        plane = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 2,
                "stroke_opacity": 0.7,
            },
        )
        plane.move_to(ORIGIN)
        registry["plane"] = plane

        # Highlight lines on TOP of the plane
        line_vert = Line(
            start=[1, -2, 0], end=[1, 2, 0], color=YELLOW, stroke_width=5
        )
        registry["line_vert"] = line_vert

        line_horiz = Line(
            start=[-2, 1, 0], end=[2, 1, 0], color=RED, stroke_width=5
        )
        registry["line_horiz"] = line_horiz

        # Right-angle marker at the (1,1) intersection
        angle_marker = Square(side_length=0.3, color=GREEN, stroke_width=4)
        angle_marker.move_to([1, 1, 0])
        registry["angle_marker"] = angle_marker

        # Footer explanation
        explain = Text(
            "Angles are preserved: a conformal map", color=GREEN, font_size=30
        )
        explain.scale(0.8)
        explain.move_to([0, -2.6, 0])
        registry["explain"] = explain

        # Keep the whole morphing stage within frame after z^2 growth
        stage = VGroup(plane, line_vert, line_horiz, angle_marker)
        stage.scale(0.9)
        stage.move_to(ORIGIN)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V05_complex_square_map_1781402344/media/audio/Visualize_the_comple_45cf8b9985/step_00_bbd779f1.mp3")  # [auto-injected]
        _audio_dur_0 = 8.14  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 2.500))
        self.set_subtitle("這是複數平面，承載著由水平與垂直線組成的方格，全部以直角相交。", run_time=_audio_dur_0)
        anim_time_1 = 2.500 * _scale_1
        self.play(Create(plane), Write(title), run_time=(2.5)*_scale_1)
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - anim_time_1 + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V05_complex_square_map_1781402344/media/audio/Visualize_the_comple_45cf8b9985/step_01_8606876f.mp3")  # [auto-injected]
        _audio_dur_1 = 7.39  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 3.500))
        self.set_subtitle("聚焦其中一條垂直線與一條水平線，注意它們以垂直方式相交。", run_time=_audio_dur_1)
        anim_time_2 = 3.500 * _scale_2
        self.play(Create(line_vert), Create(line_horiz), run_time=(2.0)*_scale_2)
        self.play(FadeIn(angle_marker), run_time=(0.5)*_scale_2)
        self.play(Indicate(angle_marker, color=GREEN), run_time=(1.0)*_scale_2)
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V05_complex_square_map_1781402344/media/audio/Visualize_the_comple_45cf8b9985/step_02_991ee5d0.mp3")  # [auto-injected]
        _audio_dur_2 = 8.88  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 4.000))
        self.set_subtitle("現在套用映射 w 等於 z 平方，觀察每一條直線如何連續地彎曲成平滑的拋物線。", run_time=_audio_dur_2)
        anim_time_3 = 4.000 * _scale_3
        morph_group = VGroup(plane, line_vert, line_horiz, angle_marker)
        self.play(
            morph_group.animate.apply_complex_function(lambda z: z**2),
            run_time=(4.0)*_scale_3,
            rate_func=smooth,
        )
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V05_complex_square_map_1781402344/media/audio/Visualize_the_comple_45cf8b9985/step_03_c4aae9c7.mp3")  # [auto-injected]
        _audio_dur_3 = 9.94  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 2.500))
        self.set_subtitle("垂直線變成向左開口的拋物線，水平線變成向右開口的拋物線，形成兩個正交的族群。", run_time=_audio_dur_3)
        anim_time_4 = 2.500 * _scale_4
        self.play(
            Indicate(line_vert, color=YELLOW),
            Indicate(line_horiz, color=RED),
            run_time=(2.5)*_scale_4,
        )
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V05_complex_square_map_1781402344/media/audio/Visualize_the_comple_45cf8b9985/step_04_bcded4cd.mp3")  # [auto-injected]
        _audio_dur_4 = 8.71  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 2.000))
        self.set_subtitle("然而在每個交點處，拋物線仍以九十度相交，揭示了這個映射保角的本質。", run_time=_audio_dur_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(
            Circumscribe(angle_marker, color=GREEN),
            Write(explain),
            run_time=(2.0)*_scale_5,
        )
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - anim_time_5 + 0.1))
        self.wait(remaining_5)