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
    """
    [VISUAL REASONING]
    1. Goal: Show how 60 straight chords (connect i -> 2i mod 60) collectively
       trace a cardioid envelope, then validate with the analytic cardioid.
    2. Layout:
       - Center at [0, 0.3, 0], radius R=2.5.
       - Title banner on top edge.
       - All geometry (circle, 60 dots, chords, cardioid) built on the circle.
    3. Flow: circle -> 60 dots -> first example chord (i=1->2) -> second example
       chord (i=15->30) -> all 60 chords -> overlay analytic red cardioid.
    """

    def construct(self):
        self._instrumentor = SceneInstrumentor(self, log_path='/Users/liaozhenting/Desktop/LLManim_Agent/scene_state_log.json')
        self._sm = SubtitleManager(self)
        self.set_subtitle = self._sm.show
        center = np.array([0, 0.3, 0])
        R = 2.5
        N = 60

        def P(k):
            return center + np.array([R * np.cos(2 * PI * k / N), R * np.sin(2 * PI * k / N), 0])

        registry = {}

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V03_cardioid_envelope_1781430478/media/audio/Generate_a_cardioid__41f5b3edaf/step_00_11d65931.mp3")  # [auto-injected]
        _audio_dur_0 = 6.14  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 1.500))
        title = Text("Cardioid from Chords: connect i -> 2i (mod 60)", color=WHITE, font_size=32)
        title.to_edge(UP, buff=0.4)
        registry["title"] = title

        circle_main = Circle(radius=2.5, color=GREY_B, stroke_width=2.0)
        circle_main.move_to(center)
        registry["circle_main"] = circle_main

        self.play(Write(title), run_time=(1.0)*_scale_1)
        anim_time_1 = 1.500 * _scale_1
        self.play(Create(circle_main), run_time=(1.5)*_scale_1)
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - anim_time_1 - 1.0 + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V03_cardioid_envelope_1781430478/media/audio/Generate_a_cardioid__41f5b3edaf/step_01_26cd4ced.mp3")  # [auto-injected]
        _audio_dur_1 = 5.81  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 2.000))
        dots_group = VGroup(*[Dot(P(k), radius=0.03, color=BLUE_D) for k in range(N)])
        registry["dots_group"] = dots_group
        anim_time_2 = 2.000 * _scale_2
        self.play(FadeIn(dots_group, lag_ratio=0.02), run_time=(2.0)*_scale_2)
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V03_cardioid_envelope_1781430478/media/audio/Generate_a_cardioid__41f5b3edaf/step_02_cf5ffdba.mp3")  # [auto-injected]
        _audio_dur_2 = 6.70  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 1.800))
        first_chord = Line(
            start=[2.4863, 0.5614, 0],
            end=[2.4454, 0.8197, 0],
            color=YELLOW,
            stroke_width=3.0,
        )
        registry["first_chord"] = first_chord
        anim_time_3 = 1.800 * _scale_3
        self.play(Create(first_chord), run_time=(1.8)*_scale_3)
        self.play(Indicate(first_chord, color=YELLOW))
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 - 1.0 + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V03_cardioid_envelope_1781430478/media/audio/Generate_a_cardioid__41f5b3edaf/step_03_475616ee.mp3")  # [auto-injected]
        _audio_dur_3 = 7.15  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 1.800))
        second_chord = Line(
            start=[0, 2.8, 0],
            end=[-2.5, 0.3, 0],
            color=ORANGE,
            stroke_width=3.0,
        )
        registry["second_chord"] = second_chord
        anim_time_4 = 1.800 * _scale_4
        self.play(Create(second_chord), run_time=(1.8)*_scale_4)
        self.play(Indicate(second_chord, color=ORANGE))
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 - 1.0 + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V03_cardioid_envelope_1781430478/media/audio/Generate_a_cardioid__41f5b3edaf/step_04_32081c33.mp3")  # [auto-injected]
        _audio_dur_4 = 7.51  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 6.000))
        self.play(FadeOut(first_chord), FadeOut(second_chord), run_time=(0.5)*_scale_5)
        chords_group = VGroup(*[
            Line(P(i), P((2 * i) % N), stroke_width=1.2, stroke_opacity=0.6, color=BLUE_B)
            for i in range(N)
        ])
        registry["chords_group"] = chords_group
        anim_time_5 = 6.000 * _scale_5
        self.play(Create(chords_group, lag_ratio=0.08), run_time=(6.0)*_scale_5)
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - anim_time_5 - 0.5 + 0.1))
        self.wait(remaining_5)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/system_V03_cardioid_envelope_1781430478/media/audio/Generate_a_cardioid__41f5b3edaf/step_05_beca009b.mp3")  # [auto-injected]
        _audio_dur_5 = 7.06  # [audio-sync]
        # Step 6
        _scale_6 = min(2.5, max(1.0, (_audio_dur_5 * 0.95) / 2.500))
        a = R / 3
        cardioid_curve = ParametricFunction(
            lambda t: center + np.array([
                2 * a * np.cos(t) - a * np.cos(2 * t),
                2 * a * np.sin(t) - a * np.sin(2 * t),
                0,
            ]),
            t_range=[0, TAU],
            color=RED,
            stroke_width=4.0,
        )
        registry["cardioid_curve"] = cardioid_curve
        anim_time_6 = 2.500 * _scale_6
        self.play(Create(cardioid_curve), run_time=(2.5)*_scale_6)
        self.play(Circumscribe(cardioid_curve, color=RED))
        remaining_6 = min(1.5, max(0.1, _audio_dur_5 - anim_time_6 - 1.0 + 0.1))
        self.wait(remaining_6)