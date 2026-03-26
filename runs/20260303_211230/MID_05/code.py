'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually derive the relationship C = πD by unfolding a circle's circumference into a line and comparing it to three diameters placed end-to-end.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for circle (left) and lines (right)
#    - Footer Region: [Bottom y=-3.5] for final equation
# 3. Anti-Overlap Check:
#    - Strategy: Place circle on left, unfolded line and 3D line on right, aligned at left edge. Use vertical offset (UP*1.5) for 3D line to avoid overlap.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/circumference_and_pi_unfolding/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create circle.
#    - Step 2: Create diameter line and label.
#    - Step 3: Create polygonal circumference path.
#    - Step 4: Transform circumference path into unfolded line.
#    - Step 5-7: Create three diameter segments end-to-end.
#    - Step 8: Highlight difference between C and 3D.
#    - Step 9: Write final equation C = πD.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        circle_anchor = ORIGIN + 3.5 * LEFT  # Left side of content
        line_anchor = ORIGIN + 3.5 * RIGHT   # Right side of content
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Circumference and Pi: Unfolding a Circle", font_size=40, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle
        circle = Circle(radius=2, color=BLUE, stroke_width=4)
        circle.move_to(circle_anchor)
        self.objects["circle"] = circle

        # diameter_line
        diameter_line = Line(start=circle_anchor + 2*LEFT, end=circle_anchor + 2*RIGHT, color=YELLOW, stroke_width=6)
        self.objects["diameter_line"] = diameter_line

        # diameter_label
        diameter_label = MathTex("D", color=YELLOW)
        diameter_label.next_to(diameter_line, UP, buff=0.2)
        self.objects["diameter_label"] = diameter_label

        # circumference_path - create as polygonal approximation from circle
        # Use get_anchors to get points, then create a Polygon
        num_points = 60
        circle_points = circle.get_anchors()[:num_points]
        # Ensure closed polygon by including first point at end
        circumference_path = Polygon(*circle_points, color=GREEN, stroke_width=4, fill_opacity=0)
        self.objects["circumference_path"] = circumference_path

        # unfolded_line - length = π * D = π * 4 ≈ 12.566
        unfolded_line_length = PI * 4
        unfolded_line_start = line_anchor
        unfolded_line_end = line_anchor + unfolded_line_length * RIGHT
        unfolded_line = Line(start=unfolded_line_start, end=unfolded_line_end, color=GREEN, stroke_width=4)
        self.objects["unfolded_line"] = unfolded_line

        # line_label
        line_label = MathTex("C", color=GREEN)
        line_label.next_to(unfolded_line, UP, buff=0.2)
        self.objects["line_label"] = line_label

        # three_d_segment_1
        three_d_segment_1_start = line_anchor + 1.5 * UP
        three_d_segment_1_end = three_d_segment_1_start + 4 * RIGHT
        three_d_segment_1 = Line(start=three_d_segment_1_start, end=three_d_segment_1_end, color=YELLOW, stroke_width=6)
        self.objects["three_d_segment_1"] = three_d_segment_1

        # three_d_segment_2
        three_d_segment_2_start = three_d_segment_1_end
        three_d_segment_2_end = three_d_segment_2_start + 4 * RIGHT
        three_d_segment_2 = Line(start=three_d_segment_2_start, end=three_d_segment_2_end, color=YELLOW, stroke_width=6)
        self.objects["three_d_segment_2"] = three_d_segment_2

        # three_d_segment_3
        three_d_segment_3_start = three_d_segment_2_end
        three_d_segment_3_end = three_d_segment_3_start + 4 * RIGHT
        three_d_segment_3 = Line(start=three_d_segment_3_start, end=three_d_segment_3_end, color=YELLOW, stroke_width=6)
        self.objects["three_d_segment_3"] = three_d_segment_3

        # three_d_label
        three_d_label = MathTex("3D", color=YELLOW)
        three_d_label.next_to(three_d_segment_3, UP, buff=0.2)
        self.objects["three_d_label"] = three_d_label

        # pi_equation
        pi_equation = MathTex(r"C = \pi D", font_size=48, color=WHITE)
        pi_equation.move_to(footer_anchor)
        self.objects["pi_equation"] = pi_equation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_an_animation__bc494f588d/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/circumference_and_pi_unfolding/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Create(self.objects["circle"]), run_time=1.0)
        remaining_1 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_an_animation__bc494f588d/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/circumference_and_pi_unfolding/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["diameter_line"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["diameter_line"]), Write(self.objects["diameter_label"]), run_time=1.5)
        remaining_2 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_an_animation__bc494f588d/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/circumference_and_pi_unfolding/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["circumference_path"], color=GREEN, run_time=1))
        self.play(Create(self.objects["circumference_path"]), run_time=2.0)
        remaining_3 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_an_animation__bc494f588d/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/circumference_and_pi_unfolding/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Transform circumference_path into unfolded_line
        self.play(Transform(self.objects["circumference_path"], self.objects["unfolded_line"]), run_time=3.0)
        self.play(Write(self.objects["line_label"]), run_time=1.0)
        remaining_4 = max(0.1, 4.0 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_an_animation__bc494f588d/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/circumference_and_pi_unfolding/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["diameter_line"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["three_d_segment_1"]), run_time=1.5)
        remaining_5 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_an_animation__bc494f588d/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/circumference_and_pi_unfolding/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Create(self.objects["three_d_segment_2"]), run_time=1.5)
        remaining_6 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Create_an_animation__bc494f588d/step_06.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/circumference_and_pi_unfolding/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(Create(self.objects["three_d_segment_3"]), Write(self.objects["three_d_label"]), run_time=2.0)
        remaining_7 = max(0.1, 2.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Create_an_animation__bc494f588d/step_07.mp3")  # [auto-injected]
        # Step 8
        audio_step8 = "media/audio/circumference_and_pi_unfolding/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["unfolded_line"], color=RED, run_time=1))
        # Create a highlight for the portion of C that extends beyond 3D
        # 3D ends at x = 12, C ends at x ≈ 12.566
        highlight_start = line_anchor + 12 * RIGHT
        highlight_end = line_anchor + unfolded_line_length * RIGHT
        highlight_line = Line(start=highlight_start, end=highlight_end, color=RED, stroke_width=8)
        self.play(Create(highlight_line), run_time=1.5)
        self.wait(max(0.1, 0.5))
        self.play(FadeOut(highlight_line), run_time=1.0)
        remaining_8 = max(0.1, 4.0 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Create_an_animation__bc494f588d/step_08.mp3")  # [auto-injected]
        # Step 9
        audio_step9 = "media/audio/circumference_and_pi_unfolding/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["pi_equation"], color=WHITE, run_time=1))
        self.play(Write(self.objects["pi_equation"]), run_time=2.0)
        remaining_9 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Final hold
        self.wait(max(0.1, 2))