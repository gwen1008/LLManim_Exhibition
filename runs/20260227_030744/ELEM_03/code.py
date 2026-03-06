from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors (zones)
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # rect
        rect = Rectangle(width=4, height=3, color=BLUE, stroke_width=4)
        rect.move_to(content_center)
        self.objects["rect"] = rect

        # dim_label_w
        dim_label_w = MathTex("4", color=YELLOW)
        dim_label_w.next_to(rect, DOWN, buff=0.2)
        self.objects["dim_label_w"] = dim_label_w

        # dim_label_h
        dim_label_h = MathTex("3", color=YELLOW)
        dim_label_h.next_to(rect, RIGHT, buff=0.2)
        self.objects["dim_label_h"] = dim_label_h

        # area_grid (8x6 grid of unit squares, side_length=0.5)
        grid = VGroup()
        side_len = 0.5
        for row in range(6):  # height = 3 units -> 6 rows of 0.5
            for col in range(8):  # width = 4 units -> 8 columns of 0.5
                sq = Square(side_length=side_len, color=GREEN, fill_opacity=0.3, stroke_width=0.5)
                # Position relative to bottom-left of rectangle
                sq.move_to(rect.get_corner(DL) + np.array([col * side_len + side_len/2, row * side_len + side_len/2, 0]))
                grid.add(sq)
        grid.move_to(rect.get_center())
        self.objects["area_grid"] = grid

        # perimeter_tracer
        perimeter_tracer = Dot(radius=0.05, color=RED)
        perimeter_tracer.move_to(rect.get_corner(DL))
        self.objects["perimeter_tracer"] = perimeter_tracer

        # perimeter_path (TracedPath)
        # Will be created and added later when needed (Step 7)
        # We'll store the lambda to create it later
        self.objects["perimeter_path_lambda"] = lambda: TracedPath(perimeter_tracer.get_center, stroke_color=RED, stroke_width=3)

        # step_explanation
        step_explanation = Text("Step 1: Define a rectangle with width 4 and height 3.", color=GRAY_B, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # area_formula
        area_formula = MathTex(r"\text{Area} = \text{length} \times \text{width} = 4 \times 3 = 12", color=GREEN)
        area_formula.move_to(explanation_anchor + 0.5 * UP).scale(0.8)
        self.objects["area_formula"] = area_formula

        # perimeter_formula
        perimeter_formula = MathTex(r"\text{Perimeter} = 2\times(\text{length}+\text{width}) = 2\times(4+3)=14", color=RED)
        perimeter_formula.move_to(explanation_anchor + 1.5 * UP).scale(0.8)
        self.objects["perimeter_formula"] = perimeter_formula

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/Create_a_4x3_rectang_45aac102a5/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["rect"]), run_time=2.0)
        remaining_1 = max(0.1, 6.792 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/Create_a_4x3_rectang_45aac102a5/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        # Signal action: Write dim_label_w (as per JSON signal_action)
        self.play(Write(self.objects["dim_label_w"]), run_time=1.0)
        remaining_2 = max(0.1, 4.632 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/Create_a_4x3_rectang_45aac102a5/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # Signal action: Indicate rect with YELLOW
        self.play(Indicate(self.objects["rect"], color=YELLOW, run_time=1.0))
        # Visual action: Write dim_label_h
        self.play(Write(self.objects["dim_label_h"]), run_time=1.0)
        remaining_3 = max(0.1, 7.536 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/Create_a_4x3_rectang_45aac102a5/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # Animate grid appearing row by row for clarity
        grid_animations = []
        for sq in self.objects["area_grid"]:
            grid_animations.append(Create(sq))
        self.play(LaggedStart(*grid_animations, lag_ratio=0.05), run_time=3.0)
        remaining_4 = max(0.1, 6.84 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/Create_a_4x3_rectang_45aac102a5/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # Signal action: Circumscribe area_grid with GREEN
        self.play(Circumscribe(self.objects["area_grid"], color=GREEN, run_time=1.0))
        # Visual action: Write area_formula
        self.play(Write(self.objects["area_formula"]), run_time=2.0)
        remaining_5 = max(0.1, 11.112 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/Create_a_4x3_rectang_45aac102a5/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # Signal action: Indicate rect with RED
        self.play(Indicate(self.objects["rect"], color=RED, run_time=1.0))
        # Visual action: FadeIn perimeter_tracer
        self.play(FadeIn(self.objects["perimeter_tracer"]), run_time=1.0)
        remaining_6 = max(0.1, 5.832 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/Create_a_4x3_rectang_45aac102a5/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # Create and add the TracedPath
        perimeter_path = self.objects["perimeter_path_lambda"]()
        self.add(perimeter_path)
        self.objects["perimeter_path"] = perimeter_path
        # No animation needed for Add, just wait for audio
        remaining_7 = max(0.1, 5.736 - 0.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        audio_step8 = "media/audio/Create_a_4x3_rectang_45aac102a5/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # Move dot from DL to DR (right along width)
        start_dl = self.objects["rect"].get_corner(DL)
        start_dr = self.objects["rect"].get_corner(DR)
        path_segment1 = Line(start_dl, start_dr)
        self.play(MoveAlongPath(self.objects["perimeter_tracer"], path_segment1), run_time=2.0, rate_func=linear)
        remaining_8 = max(0.1, 5.376 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        audio_step9 = "media/audio/Create_a_4x3_rectang_45aac102a5/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        # Move dot from DR to UR (up along height)
        start_ur = self.objects["rect"].get_corner(UR)
        path_segment2 = Line(start_dr, start_ur)
        self.play(MoveAlongPath(self.objects["perimeter_tracer"], path_segment2), run_time=1.5, rate_func=linear)
        remaining_9 = max(0.1, 2.688 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Step 10
        audio_step10 = "media/audio/Create_a_4x3_rectang_45aac102a5/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        # Move dot from UR to UL (left along width)
        start_ul = self.objects["rect"].get_corner(UL)
        path_segment3 = Line(start_ur, start_ul)
        self.play(MoveAlongPath(self.objects["perimeter_tracer"], path_segment3), run_time=2.0, rate_func=linear)
        remaining_10 = max(0.1, 2.184 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_10))

        # Step 11
        audio_step11 = "media/audio/Create_a_4x3_rectang_45aac102a5/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        # Move dot from UL to DL (down along height)
        path_segment4 = Line(start_ul, start_dl)
        self.play(MoveAlongPath(self.objects["perimeter_tracer"], path_segment4), run_time=1.5, rate_func=linear)
        remaining_11 = max(0.1, 3.264 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_11))

        # Step 12
        audio_step12 = "media/audio/Create_a_4x3_rectang_45aac102a5/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        # Signal action: Circumscribe perimeter_path with RED
        self.play(Circumscribe(self.objects["perimeter_path"], color=RED, run_time=1.0))
        # Visual action: Write perimeter_formula
        self.play(Write(self.objects["perimeter_formula"]), run_time=2.0)
        remaining_12 = max(0.1, 11.448 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_12))

        # Final hold
        self.wait(max(0.1, 2))