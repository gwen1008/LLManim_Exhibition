'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually prove π > 3 by comparing the circumference (πD) to a line of length 3D.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for circle (left) and 3D construction (right)
#    - Footer Region: [Bottom y=-3.5] for conclusion text
# 3. Anti-Overlap Check:
#    - Use relative positioning (next_to, move_to) to avoid collisions.
#    - Scale final comparison lines to 0.8 to fit within screen bounds.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/unfolding_circle/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1-3: Introduce circle, diameter, circumference.
#    - Step 4: Unfold circumference into straight line (πD).
#    - Step 5-6: Construct 3D segment from three diameter copies.
#    - Step 7-8: Bring both lines down for side-by-side comparison.
#    - Step 9: Show conclusion (πD > 3D, so π > 3).
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan description
        title_anchor = 3.5 * UP
        circle_anchor = ORIGIN + LEFT * 3.5
        construction_anchor = ORIGIN + RIGHT * 3.5
        comparison_anchor = ORIGIN + DOWN * 1.5
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Unfolding a Circle: Circumference vs. Diameter", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Circle (radius=2.0)
        circle = Circle(radius=2.0, color=BLUE, stroke_width=4)
        circle.move_to(circle_anchor)
        self.objects["circle"] = circle

        # Diameter line (horizontal across circle, length = 2*radius = 4.0)
        # Start and end points: circle center ± radius along x-axis
        circle_center = circle.get_center()
        diameter_start = circle_center + LEFT * 2.0
        diameter_end = circle_center + RIGHT * 2.0
        diameter_line = Line(diameter_start, diameter_end, color=YELLOW, stroke_width=6)
        self.objects["diameter_line"] = diameter_line

        # Label D
        label_d = MathTex("D", color=YELLOW)
        label_d.next_to(diameter_line, UP, buff=0.2)
        self.objects["label_d"] = label_d

        # Circumference arc (full circle, same center as circle)
        circumference_arc = Arc(radius=2.0, start_angle=0, angle=TAU, color=GREEN, stroke_width=6)
        circumference_arc.move_to(circle_center)
        self.objects["circumference_arc"] = circumference_arc

        # Unfolded line (length = πD = π*4 ≈ 12.566)
        # Start at the right end of the diameter line (circle's rightmost point)
        unfolded_start = diameter_end
        unfolded_end = unfolded_start + RIGHT * (PI * 4.0)  # πD
        unfolded_line = Line(unfolded_start, unfolded_end, color=GREEN, stroke_width=6)
        self.objects["unfolded_line"] = unfolded_line

        # Label πD
        label_pi_d = MathTex(r"\pi D", color=GREEN)
        label_pi_d.next_to(unfolded_line, UP, buff=0.3)
        self.objects["label_pi_d"] = label_pi_d

        # Three diameter copies (each length 4.0)
        # Position them end-to-end on the right side (construction area)
        d1_start = construction_anchor + LEFT * 2.0  # Center the group
        d1_end = d1_start + RIGHT * 4.0
        d_copy_1 = Line(d1_start, d1_end, color=YELLOW, stroke_width=4)
        self.objects["d_copy_1"] = d_copy_1

        d2_start = d1_end
        d2_end = d2_start + RIGHT * 4.0
        d_copy_2 = Line(d2_start, d2_end, color=YELLOW, stroke_width=4)
        self.objects["d_copy_2"] = d_copy_2

        d3_start = d2_end
        d3_end = d3_start + RIGHT * 4.0
        d_copy_3 = Line(d3_start, d3_end, color=YELLOW, stroke_width=4)
        self.objects["d_copy_3"] = d_copy_3

        # VGroup for the three-diameter segment
        three_d_segment = VGroup(d_copy_1, d_copy_2, d_copy_3)
        three_d_segment.move_to(construction_anchor)
        self.objects["three_d_segment"] = three_d_segment

        # Label 3D
        label_3d = MathTex("3D", color=RED)
        label_3d.next_to(three_d_segment, UP, buff=0.3)
        self.objects["label_3d"] = label_3d

        # Scaled comparison lines (scale factor 0.8 as per hint)
        scale_factor = 0.8
        # πD line scaled
        comp_pi_d_length = PI * 4.0 * scale_factor
        comp_pi_d_start = comparison_anchor + LEFT * (comp_pi_d_length / 2)
        comp_pi_d_end = comparison_anchor + RIGHT * (comp_pi_d_length / 2)
        comparison_line_pi_d = Line(comp_pi_d_start, comp_pi_d_end, color=GREEN, stroke_width=6)
        self.objects["comparison_line_pi_d"] = comparison_line_pi_d

        # 3D line scaled
        comp_3d_length = 3 * 4.0 * scale_factor  # 3D = 12
        comp_3d_start = comparison_anchor + DOWN * 0.5 + LEFT * (comp_3d_length / 2)
        comp_3d_end = comparison_anchor + DOWN * 0.5 + RIGHT * (comp_3d_length / 2)
        comparison_line_3d = Line(comp_3d_start, comp_3d_end, color=RED, stroke_width=6)
        self.objects["comparison_line_3d"] = comparison_line_3d

        # Footer text
        footer_text = Text("The circumference (πD) is longer than 3D, showing π > 3.", color=WHITE, font_size=30)
        footer_text.move_to(footer_anchor)
        self.objects["footer_text"] = footer_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_an_animation__a57147797e/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/unfolding_circle/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["circle"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_an_animation__a57147797e/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/unfolding_circle/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["diameter_line"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["diameter_line"]), Write(self.objects["label_d"]), run_time=1.5)
        remaining_2 = max(0.1, 2.5 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_an_animation__a57147797e/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/unfolding_circle/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["circumference_arc"], color=GREEN, run_time=1))
        self.play(Create(self.objects["circumference_arc"]), run_time=2.0)
        remaining_3 = max(0.1, 3.0 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_an_animation__a57147797e/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/unfolding_circle/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # Transform arc into line. We'll morph the arc by stretching its angle to a line.
        # Create a target arc with near-zero angle and stretch it to the line length.
        target_arc = Arc(radius=2.0, start_angle=0, angle=0.001, color=GREEN, stroke_width=6)
        target_arc.move_to(circle_center)
        # Stretch it horizontally to match the unfolded line length
        target_arc.stretch_to_fit_width(PI * 4.0)
        target_arc.shift(RIGHT * (PI * 2.0))  # Shift so its left end aligns with diameter end
        self.play(Transform(self.objects["circumference_arc"], target_arc), run_time=3.0)
        # After transform, replace with the actual unfolded_line for consistency
        self.remove(self.objects["circumference_arc"])
        self.add(self.objects["unfolded_line"])
        self.play(Write(self.objects["label_pi_d"]), run_time=1.0)
        remaining_4 = max(0.1, 4.0 - (3.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_an_animation__a57147797e/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/unfolding_circle/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["diameter_line"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["d_copy_1"]), run_time=2.0)
        remaining_5 = max(0.1, 3.0 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_an_animation__a57147797e/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/unfolding_circle/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Create(self.objects["d_copy_2"]), Create(self.objects["d_copy_3"]), run_time=2.0)
        self.play(Write(self.objects["label_3d"]), run_time=1.0)
        remaining_6 = max(0.1, 3.0 - (2.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Create_an_animation__a57147797e/step_06.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/unfolding_circle/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(ReplacementTransform(self.objects["unfolded_line"], self.objects["comparison_line_pi_d"]), run_time=2.5)
        remaining_7 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Create_an_animation__a57147797e/step_07.mp3")  # [auto-injected]
        # Step 8
        audio_step8 = "media/audio/unfolding_circle/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        self.play(ReplacementTransform(self.objects["three_d_segment"], self.objects["comparison_line_3d"]), run_time=2.5)
        remaining_8 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Create_an_animation__a57147797e/step_08.mp3")  # [auto-injected]
        # Step 9
        audio_step9 = "media/audio/unfolding_circle/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["comparison_line_pi_d"], color=GREEN, run_time=1))
        self.play(Write(self.objects["footer_text"]), run_time=2.0)
        remaining_9 = max(0.1, 5.0 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_9))

        # Final hold
        self.wait(max(0.1, 2))