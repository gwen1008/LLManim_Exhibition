from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Vector Addition: The Triangle Rule", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # grid
        grid = NumberPlane(
            x_range=[-2, 6, 1],
            y_range=[-1, 5, 1],
            x_length=10,
            y_length=8,
            stroke_opacity=0.2,
            axis_config={"stroke_opacity": 0.5}
        )
        grid.move_to(content_center)
        self.objects["grid"] = grid

        # vec_A
        vec_A = Arrow(
            start=[0, 0, 0],
            end=[3, 1, 0],
            color="#1E88E5",
            stroke_width=8,
            buff=0
        )
        vec_A.move_to(content_center)
        self.objects["vec_A"] = vec_A

        # label_A
        label_A = MathTex(r"\vec{A} = (3, 1)", color="#1E88E5")
        label_A.next_to(vec_A.get_end(), RIGHT, buff=0.2)
        self.objects["label_A"] = label_A

        # vec_B
        vec_B = Arrow(
            start=[3, 1, 0],
            end=[4, 3, 0],
            color="#FF9800",
            stroke_width=8,
            buff=0
        )
        vec_B.move_to(content_center + [3, 1, 0])
        self.objects["vec_B"] = vec_B

        # label_B
        label_B = MathTex(r"\vec{B} = (1, 2)", color="#FF9800")
        label_B.next_to(vec_B.get_end(), UP + RIGHT, buff=0.2)
        self.objects["label_B"] = label_B

        # vec_C
        vec_C = Arrow(
            start=[0, 0, 0],
            end=[4, 3, 0],
            color="#4CAF50",
            stroke_width=10,
            buff=0
        )
        vec_C.move_to(content_center)
        self.objects["vec_C"] = vec_C

        # label_C
        label_C = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4, 3)", color="#4CAF50")
        label_C.next_to(vec_C.get_end(), LEFT + UP, buff=0.3)
        self.objects["label_C"] = label_C

        # triangle
        triangle = Polygon(
            [0, 0, 0],
            [3, 1, 0],
            [4, 3, 0],
            color="#FFEB3B",
            fill_opacity=0.2,
            stroke_width=3,
            stroke_color="#FFEB3B"
        )
        triangle.move_to(content_center)
        self.objects["triangle"] = triangle

        # step_explanation
        step_explanation = Text(
            "Define vectors A = (3,1) and B = (1,2).",
            color=GRAY_C,
            font_size=28
        )
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 0
        # [missing audio] self.add_sound("media/audio/To_create_an_animati_583ed954e4/step_00.mp3")
        _audio_dur_0 = 2.00  # [audio-sync] actual TTS duration
        # Step 1
        self.play(FadeIn(self.objects["grid"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        # Step 1
        # [missing audio] self.add_sound("media/audio/To_create_an_animati_583ed954e4/step_01.mp3")
        _audio_dur_1 = 2.00  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Indicate(self.objects["label_A"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["vec_A"]), run_time=2.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        # Step 2
        # [missing audio] self.add_sound("media/audio/To_create_an_animati_583ed954e4/step_02.mp3")
        _audio_dur_2 = 2.00  # [audio-sync] actual TTS duration
        # Step 3
        dot = Dot(self.objects["vec_A"].get_end(), color=WHITE, radius=0.1)
        self.play(Indicate(dot, scale_factor=1.5, color=WHITE), run_time=1)
        self.remove(dot)
        self.play(Create(self.objects["vec_B"]), run_time=2.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        # Step 3
        # [missing audio] self.add_sound("media/audio/To_create_an_animati_583ed954e4/step_03.mp3")
        _audio_dur_3 = 2.00  # [audio-sync] actual TTS duration
        # Step 4
        self.play(Indicate(self.objects["vec_C"], color=GREEN, run_time=1))
        self.play(Create(self.objects["vec_C"]), run_time=2.0)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        # Step 4
        # [missing audio] self.add_sound("media/audio/To_create_an_animati_583ed954e4/step_04.mp3")
        _audio_dur_4 = 2.00  # [audio-sync] actual TTS duration
        # Step 5
        self.play(Create(self.objects["triangle"]), run_time=2.0)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))