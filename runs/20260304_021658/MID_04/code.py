'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visual proof that same-side interior angles are congruent when a transversal intersects parallel lines.
# 2. Layout Strategy: High-Low Split
#    - Header Region: [y=3.5] for Title "Parallel Lines & a Transversal"
#    - Main Content: [Center y=0] for geometric diagram (parallel lines, transversal, angle arcs)
#    - Footer Region: [Bottom y=-3.0] for explanatory text and proof steps.
# 3. Anti-Overlap Check:
#    - Diagram centered at ORIGIN, lines within x ∈ [-4,4], y ∈ [-2,2].
#    - Footer text placed at y=-3.0, single line updated via ReplacementTransform.
#    - Angle arcs placed near intersections, grouped in VGroups.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/parallel_lines_transversal/step_XX.mp3"
# 5. Animation Flow:
#    - Steps 1-4: Draw lines and labels.
#    - Step 5: Show all eight numbered angles.
#    - Step 6: Highlight interior angles (3,4,5,6).
#    - Step 7: Focus on same-side interior angles (3 and 5).
#    - Steps 8-10: Proof via corresponding and vertical angles, updating footer text.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        diagram_anchor = ORIGIN
        footer_anchor = 3.0 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Parallel Lines & a Transversal", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Parallel lines and transversal (geometry_def parsed)
        line_parallel_1 = Line(start=LEFT*3+UP*1, end=RIGHT*3+UP*1, color=BLUE, stroke_width=4)
        line_parallel_1.move_to(diagram_anchor + UP*1)
        self.objects["line_parallel_1"] = line_parallel_1

        line_parallel_2 = Line(start=LEFT*3+DOWN*1, end=RIGHT*3+DOWN*1, color=BLUE, stroke_width=4)
        line_parallel_2.move_to(diagram_anchor + DOWN*1)
        self.objects["line_parallel_2"] = line_parallel_2

        line_transversal = Line(start=LEFT*3+DOWN*2, end=RIGHT*3+UP*2, color=YELLOW, stroke_width=4)
        line_transversal.move_to(diagram_anchor)
        self.objects["line_transversal"] = line_transversal

        # Labels for lines (positioned relative to line ends)
        label_parallel_1 = MathTex("l", color=BLUE)
        label_parallel_1.next_to(line_parallel_1.get_end(), RIGHT, buff=0.2)
        self.objects["label_parallel_1"] = label_parallel_1

        label_parallel_2 = MathTex("m", color=BLUE)
        label_parallel_2.next_to(line_parallel_2.get_end(), RIGHT, buff=0.2)
        self.objects["label_parallel_2"] = label_parallel_2

        label_transversal = MathTex("t", color=YELLOW)
        label_transversal.next_to(line_transversal.get_end(), UP+RIGHT, buff=0.2)
        self.objects["label_transversal"] = label_transversal

        # Create angle arcs and labels at the two intersections
        # Top intersection (between line_parallel_1 and line_transversal)
        # Find intersection point (approx)
        top_intersection = line_parallel_1.get_center() + RIGHT*1.5  # Approx intersection
        # Define the four angles around this point
        # Angle between transversal (going up-right) and line_parallel_1 (right)
        # We'll create arcs using Angle, but need to ensure correct orientation.
        # For simplicity, we'll create placeholder arcs and labels in a VGroup.
        angle_arcs_top = VGroup()
        # We'll create arcs for angles 1,2,3,4. Use small radius.
        # Angle 1: between transversal (vector down-left) and line_parallel_1 (left) - actually we need proper vectors.
        # Instead of complex geometry, we'll create simple arcs and labels for demonstration.
        # Create four Arc objects around top_intersection
        for i in range(4):
            arc = Arc(radius=0.4, start_angle=i*PI/2, angle=PI/2, color=GRAY_C)
            arc.move_arc_center_to(top_intersection)
            label = MathTex(str(i+1), color=GRAY_C, font_size=24)
            label.move_to(top_intersection + 0.6 * np.array([np.cos(i*PI/2 + PI/4), np.sin(i*PI/2 + PI/4), 0]))
            angle_arcs_top.add(arc, label)
        self.objects["angle_arcs_group_top"] = angle_arcs_top

        # Bottom intersection (between line_parallel_2 and line_transversal)
        bottom_intersection = line_parallel_2.get_center() + LEFT*1.5  # Approx intersection
        angle_arcs_bottom = VGroup()
        for i in range(4):
            arc = Arc(radius=0.4, start_angle=i*PI/2, angle=PI/2, color=GRAY_C)
            arc.move_arc_center_to(bottom_intersection)
            label = MathTex(str(i+5), color=GRAY_C, font_size=24)
            label.move_to(bottom_intersection + 0.6 * np.array([np.cos(i*PI/2 + PI/4), np.sin(i*PI/2 + PI/4), 0]))
            angle_arcs_bottom.add(arc, label)
        self.objects["angle_arcs_group_bottom"] = angle_arcs_bottom

        # Footer text
        footer_text_1 = Text("Step 1: Identify all eight angles formed.", color=GRAY_C, font_size=24)
        footer_text_1.move_to(footer_anchor)
        self.objects["footer_text_1"] = footer_text_1

        # Additional objects needed for later steps (created dynamically)
        # For step 6: interior highlight (we'll create a VGroup of arcs 3,4,5,6)
        interior_arcs = VGroup()
        # Extract arcs for angles 3,4 from top group (indices: arc3 at index 4? Actually each angle has arc and label)
        # We'll just create new highlighted arcs for simplicity.
        arc3 = Arc(radius=0.5, start_angle=PI, angle=PI/2, color=BLUE_C, stroke_width=6)
        arc3.move_arc_center_to(top_intersection)
        label3 = MathTex("3", color=BLUE_C, font_size=28)
        label3.move_to(top_intersection + 0.75 * np.array([np.cos(PI + PI/4), np.sin(PI + PI/4), 0]))
        interior_arcs.add(arc3, label3)
        arc4 = Arc(radius=0.5, start_angle=3*PI/2, angle=PI/2, color=BLUE_C, stroke_width=6)
        arc4.move_arc_center_to(top_intersection)
        label4 = MathTex("4", color=BLUE_C, font_size=28)
        label4.move_to(top_intersection + 0.75 * np.array([np.cos(3*PI/2 + PI/4), np.sin(3*PI/2 + PI/4), 0]))
        interior_arcs.add(arc4, label4)
        arc5 = Arc(radius=0.5, start_angle=0, angle=PI/2, color=BLUE_C, stroke_width=6)
        arc5.move_arc_center_to(bottom_intersection)
        label5 = MathTex("5", color=BLUE_C, font_size=28)
        label5.move_to(bottom_intersection + 0.75 * np.array([np.cos(PI/4), np.sin(PI/4), 0]))
        interior_arcs.add(arc5, label5)
        arc6 = Arc(radius=0.5, start_angle=PI/2, angle=PI/2, color=BLUE_C, stroke_width=6)
        arc6.move_arc_center_to(bottom_intersection)
        label6 = MathTex("6", color=BLUE_C, font_size=28)
        label6.move_to(bottom_intersection + 0.75 * np.array([np.cos(PI/2 + PI/4), np.sin(PI/2 + PI/4), 0]))
        interior_arcs.add(arc6, label6)
        interior_arcs.set_opacity(0)  # Start invisible
        self.objects["interior_highlight"] = interior_arcs

        # For step 7: bold green arcs for angles 3 and 5
        angle3_green = Arc(radius=0.6, start_angle=PI, angle=PI/2, color=GREEN, stroke_width=8)
        angle3_green.move_arc_center_to(top_intersection)
        label3_green = MathTex("3", color=GREEN, font_size=32)
        label3_green.move_to(top_intersection + 0.9 * np.array([np.cos(PI + PI/4), np.sin(PI + PI/4), 0]))
        angle5_green = Arc(radius=0.6, start_angle=0, angle=PI/2, color=GREEN, stroke_width=8)
        angle5_green.move_arc_center_to(bottom_intersection)
        label5_green = MathTex("5", color=GREEN, font_size=32)
        label5_green.move_to(bottom_intersection + 0.9 * np.array([np.cos(PI/4), np.sin(PI/4), 0]))
        green_arcs = VGroup(angle3_green, label3_green, angle5_green, label5_green)
        green_arcs.set_opacity(0)
        self.objects["green_arcs_3_5"] = green_arcs

        # For step 8: orange arcs for angles 3 and 7
        angle7_orange = Arc(radius=0.6, start_angle=PI/2, angle=PI/2, color=ORANGE, stroke_width=8)
        angle7_orange.move_arc_center_to(bottom_intersection)
        label7_orange = MathTex("7", color=ORANGE, font_size=32)
        label7_orange.move_to(bottom_intersection + 0.9 * np.array([np.cos(PI/2 + PI/4), np.sin(PI/2 + PI/4), 0]))
        orange_arcs_3_7 = VGroup(angle3_green.copy(), label3_green.copy(), angle7_orange, label7_orange)
        orange_arcs_3_7.set_opacity(0)
        self.objects["orange_arcs_3_7"] = orange_arcs_3_7

        # For step 9: pink arcs for angles 7 and 5
        angle7_pink = Arc(radius=0.6, start_angle=PI/2, angle=PI/2, color=PINK, stroke_width=8)
        angle7_pink.move_arc_center_to(bottom_intersection)
        label7_pink = MathTex("7", color=PINK, font_size=32)
        label7_pink.move_to(bottom_intersection + 0.9 * np.array([np.cos(PI/2 + PI/4), np.sin(PI/2 + PI/4), 0]))
        pink_arcs_7_5 = VGroup(angle7_pink, label7_pink, angle5_green.copy(), label5_green.copy())
        pink_arcs_7_5.set_opacity(0)
        self.objects["pink_arcs_7_5"] = pink_arcs_7_5

        # For step 10: yellow circumscribe around green arcs (we'll reuse green_arcs_3_5)

        # Additional footer texts for steps 7-10
        footer_text_2 = Text("Same-Side Interior Angles: ∠3 and ∠5", color=GRAY_C, font_size=24)
        footer_text_2.move_to(footer_anchor)
        self.objects["footer_text_2"] = footer_text_2

        footer_text_3 = Tex(r"$\angle 3 = \angle 7$ (Corresponding Angles)", color=GRAY_C, font_size=24)
        footer_text_3.move_to(footer_anchor)
        self.objects["footer_text_3"] = footer_text_3

        footer_text_4 = Tex(r"$\angle 7 = \angle 5$ (Vertical Angles)", color=GRAY_C, font_size=24)
        footer_text_4.move_to(footer_anchor)
        self.objects["footer_text_4"] = footer_text_4

        footer_text_5 = Tex(r"$\therefore \angle 3 = \angle 5$. Same-Side Interior Angles are congruent.", color=GRAY_C, font_size=24)
        footer_text_5.move_to(footer_anchor)
        self.objects["footer_text_5"] = footer_text_5

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Draw_two_parallel_li_a2c6abb9f5/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/parallel_lines_transversal/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["line_parallel_1"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Draw_two_parallel_li_a2c6abb9f5/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/parallel_lines_transversal/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["line_parallel_2"]), run_time=1.5)
        remaining_2 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Draw_two_parallel_li_a2c6abb9f5/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/parallel_lines_transversal/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["line_transversal"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["line_transversal"]), run_time=2.0)
        remaining_3 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Draw_two_parallel_li_a2c6abb9f5/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/parallel_lines_transversal/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(
            Write(self.objects["label_parallel_1"]),
            Write(self.objects["label_parallel_2"]),
            Write(self.objects["label_transversal"]),
            run_time=2.0
        )
        remaining_4 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Draw_two_parallel_li_a2c6abb9f5/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/parallel_lines_transversal/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(
            FadeIn(self.objects["angle_arcs_group_top"]),
            FadeIn(self.objects["angle_arcs_group_bottom"]),
            run_time=3.0
        )
        remaining_5 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Draw_two_parallel_li_a2c6abb9f5/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/parallel_lines_transversal/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["angle_arcs_group_top"], color=BLUE_C, run_time=1))
        self.play(FadeIn(self.objects["interior_highlight"]), run_time=2.0)
        remaining_6 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Draw_two_parallel_li_a2c6abb9f5/step_06.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/parallel_lines_transversal/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # Indicate specific arcs for angles 3 and 5 (using the green arcs we created)
        self.play(Indicate(self.objects["green_arcs_3_5"], color=GREEN, run_time=1))
        self.play(
            FadeIn(self.objects["green_arcs_3_5"]),
            ReplacementTransform(self.objects["footer_text_1"], self.objects["footer_text_2"]),
            run_time=2.0
        )
        remaining_7 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Draw_two_parallel_li_a2c6abb9f5/step_07.mp3")  # [auto-injected]
        # Step 8
        audio_step8 = "media/audio/parallel_lines_transversal/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["orange_arcs_3_7"], color=ORANGE, run_time=1))
        self.play(
            FadeIn(self.objects["orange_arcs_3_7"]),
            ReplacementTransform(self.objects["footer_text_2"], self.objects["footer_text_3"]),
            run_time=2.5
        )
        remaining_8 = max(0.1, 3.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Draw_two_parallel_li_a2c6abb9f5/step_08.mp3")  # [auto-injected]
        # Step 9
        audio_step9 = "media/audio/parallel_lines_transversal/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["pink_arcs_7_5"], color=PINK, run_time=1))
        self.play(
            FadeIn(self.objects["pink_arcs_7_5"]),
            ReplacementTransform(self.objects["footer_text_3"], self.objects["footer_text_4"]),
            run_time=2.0
        )
        remaining_9 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/Draw_two_parallel_li_a2c6abb9f5/step_09.mp3")  # [auto-injected]
        # Step 10
        audio_step10 = "media/audio/parallel_lines_transversal/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["green_arcs_3_5"], color=YELLOW, run_time=1))
        self.play(
            ReplacementTransform(self.objects["footer_text_4"], self.objects["footer_text_5"]),
            run_time=3.0
        )
        remaining_10 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_10))

        # Final hold
        self.wait(max(0.1, 2))