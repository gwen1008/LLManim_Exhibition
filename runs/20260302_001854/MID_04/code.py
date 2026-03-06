'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the Corresponding Angles Theorem: when a transversal intersects two parallel lines, corresponding interior angles are equal.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for parallel lines, transversal, angles
#    - Footer Region: [Bottom y=-3.5] for step explanations
# 3. Anti-Overlap Check:
#    - Strategy: Use distinct zones. Diagram centered at origin. Labels placed near intersection points with buff.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Draw_two_parallel_li_d41c82c39f/step_XX.mp3"
# 5. Animation Flow:
#    - Draw parallel lines, transversal, intersection points.
#    - Label angles 3 and 7.
#    - Highlight corresponding angles with green arcs.
#    - Animate sliding one green arc down to prove equality.
#    - State the theorem.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        diagram_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Corresponding Angles Theorem", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # line1 (top parallel line)
        line1 = Line(start=[-4, 1, 0], end=[4, 1, 0], color=WHITE, stroke_width=3)
        line1.move_to(diagram_center + UP)
        self.objects["line1"] = line1

        # line2 (bottom parallel line)
        line2 = Line(start=[-4, -1, 0], end=[4, -1, 0], color=WHITE, stroke_width=3)
        line2.move_to(diagram_center + DOWN)
        self.objects["line2"] = line2

        # transversal
        transversal = Line(start=[-3, 1.5, 0], end=[3, -1.5, 0], color=YELLOW, stroke_width=4)
        transversal.move_to(diagram_center)
        self.objects["transversal"] = transversal

        # point_a
        point_a = Dot(point=[-1, 1, 0], color=WHITE, radius=0.06)
        self.objects["point_a"] = point_a

        # point_b
        point_b = Dot(point=[1, -1, 0], color=WHITE, radius=0.06)
        self.objects["point_b"] = point_b

        # angle1_arc (will be created later, after lines exist)
        # angle2_arc (will be created later, after lines exist)

        # angle_label_3
        angle_label_3 = MathTex("3", color=WHITE, font_size=24)
        # Position relative to point_a after point_a is created
        # We'll position it after creation
        self.objects["angle_label_3"] = angle_label_3

        # angle_label_7
        angle_label_7 = MathTex("7", color=WHITE, font_size=24)
        self.objects["angle_label_7"] = angle_label_7

        # step_label
        step_label = Text("Step 1: Draw parallel lines and a transversal", color=GRAY_C, font_size=28)
        step_label.move_to(explanation_anchor)
        self.objects["step_label"] = step_label

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/Draw_two_parallel_li_d41c82c39f/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(Create(self.objects["line1"]), run_time=2.0)
        remaining_1 = max(0.1, 7.776 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/Draw_two_parallel_li_d41c82c39f/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        # signal_action: Indicate line1 in BLUE
        self.play(Indicate(self.objects["line1"], color=BLUE, run_time=1))
        self.play(Create(self.objects["line2"]), run_time=2.0)
        remaining_2 = max(0.1, 5.976 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/Draw_two_parallel_li_d41c82c39f/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(Create(self.objects["transversal"]), run_time=2.5)
        remaining_3 = max(0.1, 7.944 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/Draw_two_parallel_li_d41c82c39f/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # signal_action: Circumscribe transversal in YELLOW
        self.play(Circumscribe(self.objects["transversal"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["point_a"]), run_time=1.0)
        remaining_4 = max(0.1, 5.136 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/Draw_two_parallel_li_d41c82c39f/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(Create(self.objects["point_b"]), run_time=1.0)
        remaining_5 = max(0.1, 3.288 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        # Position angle_label_3 relative to point_a
        self.objects["angle_label_3"].next_to(self.objects["point_a"], RIGHT + UP, buff=0.15)
        audio_step6 = "media/audio/Draw_two_parallel_li_d41c82c39f/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(Write(self.objects["angle_label_3"]), run_time=1.5)
        remaining_6 = max(0.1, 9.048 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        # Position angle_label_7 relative to point_b
        self.objects["angle_label_7"].next_to(self.objects["point_b"], RIGHT + DOWN, buff=0.15)
        audio_step7 = "media/audio/Draw_two_parallel_li_d41c82c39f/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(Write(self.objects["angle_label_7"]), run_time=1.5)
        remaining_7 = max(0.1, 4.08 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        # Create angle1_arc (angle at point_a between transversal and line1)
        # We need the intersection point for angle calculation.
        # The transversal intersects line1 at point_a's position.
        # Angle between transversal and line1 (horizontal).
        # Use Angle class: line1 is horizontal right from point_a, line2 is transversal direction from point_a.
        # We'll create a small horizontal line segment at point_a for reference.
        # Actually, Angle expects two lines. We'll create temporary lines for the angle.
        # Implementation hint: Use Angle class with radius=0.4
        # We'll create the angle arc dynamically.
        line1_at_a = Line(start=self.objects["point_a"].get_center(), end=self.objects["point_a"].get_center() + RIGHT, color=WHITE)
        # Direction of transversal from point_a: from point_a to a point on transversal further right.
        # transversal direction vector: (3 - (-3), -1.5 - 1.5) = (6, -3) normalized.
        # We'll take a point on transversal near point_a.
        trans_dir_a = self.objects["transversal"].get_end() - self.objects["transversal"].get_start()
        trans_point_a = self.objects["point_a"].get_center() + 0.5 * normalize(trans_dir_a)
        trans_line_at_a = Line(start=self.objects["point_a"].get_center(), end=trans_point_a, color=YELLOW)
        angle1_arc = Angle(line1=line1_at_a, line2=trans_line_at_a, radius=0.4, other_angle=False, color=GREEN, stroke_width=4)
        self.objects["angle1_arc"] = angle1_arc

        audio_step8 = "media/audio/Draw_two_parallel_li_d41c82c39f/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # signal_action: Indicate angle_label_3 in GREEN
        self.play(Indicate(self.objects["angle_label_3"], color=GREEN, run_time=1))
        self.play(Create(self.objects["angle1_arc"]), run_time=2.0)
        remaining_8 = max(0.1, 8.664 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        # Create angle2_arc (angle at point_b between transversal and line2)
        # Similar construction.
        line2_at_b = Line(start=self.objects["point_b"].get_center(), end=self.objects["point_b"].get_center() + RIGHT, color=WHITE)
        trans_dir_b = self.objects["transversal"].get_end() - self.objects["transversal"].get_start()
        trans_point_b = self.objects["point_b"].get_center() + 0.5 * normalize(trans_dir_b)
        trans_line_at_b = Line(start=self.objects["point_b"].get_center(), end=trans_point_b, color=YELLOW)
        angle2_arc = Angle(line1=line2_at_b, line2=trans_line_at_b, radius=0.4, other_angle=False, color=GREEN, stroke_width=4)
        self.objects["angle2_arc"] = angle2_arc

        audio_step9 = "media/audio/Draw_two_parallel_li_d41c82c39f/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        # signal_action: Indicate angle_label_7 in GREEN
        self.play(Indicate(self.objects["angle_label_7"], color=GREEN, run_time=1))
        self.play(Create(self.objects["angle2_arc"]), run_time=2.0)
        remaining_9 = max(0.1, 5.544 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Step 10
        # Create a copy of angle1_arc and animate it sliding down the transversal to overlap angle2_arc.
        audio_step10 = "media/audio/Draw_two_parallel_li_d41c82c39f/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        # signal_action: null
        angle1_copy = self.objects["angle1_arc"].copy()
        self.add(angle1_copy)
        # Animate translation and rotation to match angle2_arc.
        # We'll move it from point_a to point_b, and rotate to match orientation.
        # Use Transform: target is angle2_arc, but we want to keep original angle2_arc.
        # So we'll transform the copy into a new angle at point_b position with same shape.
        # Actually, we can animate the copy moving to angle2_arc's position and rotating.
        # Use MoveAlongPath? Simpler: use Transform with temporary target.
        # Create a target angle at point_b identical to angle2_arc but we will not show it.
        # Instead, we can use angle2_arc as target, but we don't want to transform the original.
        # Let's create a dummy target at same position as angle2_arc.
        dummy_target = Angle(line1=line2_at_b, line2=trans_line_at_b, radius=0.4, other_angle=False, color=GREEN, stroke_width=4)
        dummy_target.move_to(self.objects["angle2_arc"].get_center())
        # We'll animate the copy transforming into dummy_target.
        self.play(Transform(angle1_copy, dummy_target), run_time=3.0)
        remaining_10 = max(0.1, 9.624 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_10))
        self.remove(angle1_copy, dummy_target)

        # Step 11
        audio_step11 = "media/audio/Draw_two_parallel_li_d41c82c39f/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        # signal_action: Circumscribe angle2_arc in YELLOW
        self.play(Circumscribe(self.objects["angle2_arc"], color=YELLOW, run_time=1))
        # visual_action: Wait
        remaining_11 = max(0.1, 9.48 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_11))

        # Step 12
        # Update step_label to state the theorem.
        audio_step12 = "media/audio/Draw_two_parallel_li_d41c82c39f/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        # signal_action: null
        new_step_label = Text("Corresponding Angles Theorem: Corresponding angles are equal.", color=GRAY_C, font_size=28)
        new_step_label.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_label"], new_step_label), run_time=2.0)
        remaining_12 = max(0.1, 8.616 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_12))

        # Final hold
        self.wait(max(0.1, 2))