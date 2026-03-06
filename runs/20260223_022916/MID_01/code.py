from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Translation and Displacement on a Number Line", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Number Line
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=8.8,
            include_numbers=True,
            numbers_to_include=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
            color=GRAY_B
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # Point A and its label (at -2)
        point_a = Dot(radius=0.08, color=BLUE, fill_opacity=1.0)
        point_a.move_to(number_line.number_to_point(-2))
        self.objects["point_a"] = point_a

        label_a = MathTex("-2", color=BLUE, font_size=30)
        label_a.next_to(point_a, DOWN, buff=0.2)
        self.objects["label_a"] = label_a

        # Point B and its label (at 3) - FIXED: Use align_to for proper alignment
        point_b = Dot(radius=0.08, color=GREEN, fill_opacity=1.0)
        point_b.move_to(number_line.number_to_point(3))
        point_b.align_to(number_line.number_to_point(3), ORIGIN)
        self.objects["point_b"] = point_b

        label_b = MathTex("3", color=GREEN, font_size=30)
        label_b.next_to(point_b, DOWN, buff=0.2)
        self.objects["label_b"] = label_b

        # Displacement Arrow (from point_a to point_b)
        arrow_start = number_line.number_to_point(-2)
        arrow_end = number_line.number_to_point(3)
        displacement_arrow = Arrow(
            start=arrow_start,
            end=arrow_end,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["displacement_arrow"] = displacement_arrow

        # Displacement Label - FIXED: Increased font size to 48
        displacement_label = MathTex("+5", color=YELLOW, font_size=48)
        displacement_label.next_to(displacement_arrow, UP, buff=0.15)
        self.objects["displacement_label"] = displacement_label

        # Tracer Dot
        tracer_dot = Dot(radius=0.06, color=RED, fill_opacity=1.0)
        tracer_dot.move_to(arrow_start)
        self.objects["tracer_dot"] = tracer_dot

        # Explanation Text
        explanation_text = Text("Start: Plot the points.", color=GRAY_B, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(self.objects["number_line"]), run_time=2.0)
        remaining_1 = max(0.1, 5.784 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Indicate label_a
        self.play(Indicate(self.objects["label_a"], color=BLUE, run_time=1))
        # Visual action: Create points and labels
        self.play(
            Create(self.objects["point_a"]),
            Write(self.objects["label_a"]),
            Create(self.objects["point_b"]),
            Write(self.objects["label_b"]),
            run_time=2.0
        )
        remaining_2 = max(0.1, 5.4 - 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3 - FIXED: Use ReplacementTransform instead of Transform
        audio_step3 = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Indicate point_a
        self.play(Indicate(self.objects["point_a"], color=WHITE, run_time=1))
        # Visual action: Transform point_a to point_b's position
        point_a_end = self.objects["point_a"].copy()
        point_a_end.move_to(self.objects["point_b"].get_center())
        self.play(ReplacementTransform(self.objects["point_a"], point_a_end), run_time=3.0)
        self.objects["point_a"] = point_a_end  # Update reference
        remaining_3 = max(0.1, 8.472 - 3.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Circumscribe displacement_arrow
        self.play(Circumscribe(self.objects["displacement_arrow"], color=YELLOW, run_time=1))
        # Visual action: GrowArrow
        self.play(GrowArrow(self.objects["displacement_arrow"]), run_time=2.0)
        remaining_4 = max(0.1, 7.704 - 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Indicate tracer_dot
        self.play(Indicate(self.objects["tracer_dot"], color=RED, run_time=1))
        # Visual action: MoveAlongPath
        self.play(MoveAlongPath(self.objects["tracer_dot"], self.objects["displacement_arrow"]), run_time=2.5)
        remaining_5 = max(0.1, 6.576 - 2.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Write(self.objects["displacement_label"]), run_time=1.5)
        remaining_6 = max(0.1, 3.936 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Final wait
        self.wait(max(0.1, 2))