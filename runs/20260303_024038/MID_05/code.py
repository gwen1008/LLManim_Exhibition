'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually demonstrate that π > 3 by comparing the circumference (πD) to three diameters (3D).
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for circle (left) and line comparison (right)
#    - Footer Region: [Bottom y=-3.5] for conclusion formula
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Place circle on left, line segments on right. Use VGroups for 3D segment.
#    - Ensure labels are placed with buff to avoid overlap.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/why_pi_greater_than_3/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
#    - Step 1: Show circle and diameter.
#    - Step 2: Build 3D segment from diameter.
#    - Step 3: Unfurl circle into πD line above.
#    - Step 4: Compare lengths, show gap.
#    - Step 5: Show conclusion.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        circle_anchor = 3 * LEFT  # Left of center
        comparison_left_anchor = 3 * RIGHT  # Right of center, aligned left for segments
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Why π is Greater Than 3", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle
        circle = Circle(radius=2, color="#AAAAAA", stroke_width=4)
        circle.move_to(circle_anchor)
        self.objects["circle"] = circle

        # diameter_line (inside circle)
        diameter_line = Line(start=LEFT*2, end=RIGHT*2, color=YELLOW, stroke_width=6)
        diameter_line.move_to(circle_anchor)
        self.objects["diameter_line"] = diameter_line

        # label_D
        label_D = MathTex("D", color=YELLOW, font_size=36)
        label_D.next_to(diameter_line, UP, buff=0.2)
        self.objects["label_D"] = label_D

        # segment_3d (VGroup of three lines, each length 4)
        seg1 = Line(start=ORIGIN, end=RIGHT*4, color=GREEN, stroke_width=6)
        seg2 = Line(start=RIGHT*4, end=RIGHT*8, color=GREEN, stroke_width=6)
        seg3 = Line(start=RIGHT*8, end=RIGHT*12, color=GREEN, stroke_width=6)
        segment_3d = VGroup(seg1, seg2, seg3)
        segment_3d.move_to(comparison_left_anchor + DOWN*1.0).align_to(comparison_left_anchor, LEFT)
        self.objects["segment_3d"] = segment_3d

        # label_3d
        label_3d = MathTex("3D", color=GREEN, font_size=36)
        label_3d.next_to(segment_3d, DOWN, buff=0.3)
        self.objects["label_3d"] = label_3d

        # segment_pi_d (length πD ≈ 12.566, D=4 so πD ≈ 12.566)
        segment_pi_d = Line(start=ORIGIN, end=RIGHT*12.566, color=BLUE, stroke_width=6)
        segment_pi_d.move_to(comparison_left_anchor + UP*1.5).align_to(comparison_left_anchor, LEFT)
        self.objects["segment_pi_d"] = segment_pi_d

        # label_pi_d
        label_pi_d = MathTex("\\pi D", color=BLUE, font_size=36)
        label_pi_d.next_to(segment_pi_d, UP, buff=0.3)
        self.objects["label_pi_d"] = label_pi_d

        # length_gap (brace from end of 3D to end of πD)
        # The brace is placed at the right end of πD segment, shifted left by half the gap width? Actually brace should span the gap.
        # Gap length = πD - 3D = 12.566 - 12 = 0.566. We'll create a brace from x=12 to x=12.566.
        # We'll create it as a separate object and position it later.
        length_gap = Brace(segment_pi_d, DOWN, 0.1, color=RED, stroke_width=3)
        # We'll adjust its position in step 4 after both segments exist.
        self.objects["length_gap"] = length_gap

        # label_gap
        label_gap = MathTex("\\pi D - 3D", color=RED, font_size=28)
        label_gap.next_to(length_gap, DOWN, buff=0.2)
        self.objects["label_gap"] = label_gap

        # footer_text
        footer_text = MathTex("\\pi D > 3D \\quad \\Rightarrow \\quad \\pi > 3", color=WHITE, font_size=40)
        footer_text.move_to(footer_anchor)
        self.objects["footer_text"] = footer_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/The_animation_begins_a78f1ffe04/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/why_pi_greater_than_3/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(self.objects["circle"]), run_time=1.5)
        self.play(Create(self.objects["diameter_line"]), Write(self.objects["label_D"]), run_time=1.0)
        remaining_1 = max(0.1, 2.0 - 2.5 + 0.5)  # duration 2.0, anim ~2.5
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/The_animation_begins_a78f1ffe04/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/why_pi_greater_than_3/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["diameter_line"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["segment_3d"]), Write(self.objects["label_3d"]), run_time=2.5)
        remaining_2 = max(0.1, 4.0 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/The_animation_begins_a78f1ffe04/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/why_pi_greater_than_3/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["circle"], color=BLUE, run_time=1))
        # Transform circle into segment_pi_d. We'll create a copy of the circle's perimeter? Simpler: FadeOut circle and Create segment_pi_d.
        # But JSON says Transform circle's perimeter into segment_pi_d. We'll approximate with ReplacementTransform.
        # We need a copy of the circle's perimeter (just the circle) to transform.
        circle_perimeter = self.objects["circle"].copy()
        circle_perimeter.set_color(BLUE)
        self.add(circle_perimeter)
        self.remove(self.objects["circle"])
        self.play(ReplacementTransform(circle_perimeter, self.objects["segment_pi_d"]), run_time=3.0)
        self.play(Write(self.objects["label_pi_d"]), run_time=1.0)
        remaining_3 = max(0.1, 5.0 - 5.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/The_animation_begins_a78f1ffe04/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/why_pi_greater_than_3/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["segment_pi_d"], color=BLUE, run_time=1))
        # Now create the brace for the gap. The brace should span from end of 3D to end of πD.
        # We'll create a Line between those points and brace it.
        gap_start = self.objects["segment_3d"].get_right()
        gap_end = self.objects["segment_pi_d"].get_right()
        gap_line = Line(gap_start, gap_end, color=RED, stroke_width=0)  # invisible line for brace
        gap_brace = Brace(gap_line, DOWN, 0.1, 0.1, color=RED, stroke_width=3)
        gap_label = self.objects["label_gap"]
        gap_label.next_to(gap_brace, DOWN, buff=0.2)
        # Replace the placeholder length_gap with actual brace
        self.remove(self.objects["length_gap"])
        self.objects["length_gap"] = gap_brace
        self.play(Create(gap_brace), Write(gap_label), run_time=2.0)
        remaining_4 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/The_animation_begins_a78f1ffe04/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/why_pi_greater_than_3/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["footer_text"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["footer_text"]), run_time=2.0)
        remaining_5 = max(0.1, 5.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))