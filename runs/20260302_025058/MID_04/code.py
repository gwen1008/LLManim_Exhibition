'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually prove that interior angles on the same side of a transversal are equal (corresponding angles) when the lines are parallel.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for parallel lines, transversal, and angles
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for lines and labels. Position title high, explanation low, main diagram centered.
# 4. Audio Check (CRITICAL):
#    - [ ] Have I included self.add_sound() for EVERY step?
#    - [ ] Files: "media/audio/parallel_lines_transversal/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Draw two parallel horizontal lines.
#    - Step 2: Draw a slanted transversal line intersecting them.
#    - Step 3: Label intersection points and highlight the two target interior angles in green.
#    - Step 4: Create a copy of one angle, rotate and translate it to overlap the other, visually proving congruence.
#    - Step 5: Show equal signs or a label confirming the angles are equal.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create Title
        title = Text("平行線與截線：同側內角相等", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.objects["title"] = title

        # Create two parallel horizontal lines
        line1 = Line(start=LEFT * 4, end=RIGHT * 4, color=WHITE, stroke_width=4)
        line1.shift(UP * 1.5)
        self.objects["line1"] = line1

        line2 = Line(start=LEFT * 4, end=RIGHT * 4, color=WHITE, stroke_width=4)
        line2.shift(DOWN * 1.5)
        self.objects["line2"] = line2

        # Create a slanted transversal line
        transversal = Line(start=LEFT * 3 + UP * 2.5, end=RIGHT * 3 + DOWN * 2.5, color=BLUE, stroke_width=4)
        self.objects["transversal"] = transversal

        # Calculate intersection points (approximate for simplicity)
        # Intersection of transversal with line1 (top)
        inter1 = line1.get_center() + LEFT * 1.5
        # Intersection of transversal with line2 (bottom)
        inter2 = line2.get_center() + RIGHT * 1.5

        # Create angle arcs at the intersections (interior angles on same side)
        # We'll create two arcs: one at inter1 (left side) and one at inter2 (right side)
        # These are the interior angles on the same side of the transversal.
        # Angle at inter1: between line1 (left segment) and transversal (upper left segment)
        # We'll create an Arc between two lines.
        # For simplicity, we'll create arcs at fixed positions.
        arc1 = Arc(radius=0.5, start_angle=30 * DEGREES, angle=60 * DEGREES, color=GREEN, stroke_width=6)
        # Position arc1 near inter1, between line1 and transversal
        arc1.move_to(inter1 + LEFT * 0.3 + UP * 0.3)
        self.objects["arc1"] = arc1

        arc2 = Arc(radius=0.5, start_angle=210 * DEGREES, angle=60 * DEGREES, color=GREEN, stroke_width=6)
        # Position arc2 near inter2, between line2 and transversal
        arc2.move_to(inter2 + RIGHT * 0.3 + DOWN * 0.3)
        self.objects["arc2"] = arc2

        # Create angle labels
        label1 = MathTex(r"\theta", color=GREEN, font_size=36).next_to(arc1, UR, buff=0.1)
        self.objects["label1"] = label1
        label2 = MathTex(r"\theta", color=GREEN, font_size=36).next_to(arc2, DL, buff=0.1)
        self.objects["label2"] = label2

        # Create a copy of arc1 for the transformation
        arc1_copy = arc1.copy()
        arc1_copy.set_color(YELLOW)
        self.objects["arc1_copy"] = arc1_copy

        # Create equal sign to show congruence
        equal_sign = MathTex(r"=", color=YELLOW, font_size=72)
        equal_sign.move_to(ORIGIN + DOWN * 2.5)
        self.objects["equal_sign"] = equal_sign

        # Explanation text at bottom
        explanation = Text("同側內角相等（對應角）", font_size=36, color=YELLOW)
        explanation.to_edge(DOWN, buff=0.5)
        self.objects["explanation"] = explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1: Draw parallel lines
        audio_step1 = "media/audio/parallel_lines_transversal/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title"]), run_time=1.5)
        self.play(Create(self.objects["line1"]), Create(self.objects["line2"]), run_time=2.0)
        remaining_1 = max(0.1, 4.0 - 1.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2: Draw transversal
        audio_step2 = "media/audio/parallel_lines_transversal/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Create(self.objects["transversal"]), run_time=1.5)
        remaining_2 = max(0.1, 3.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3: Highlight the two interior angles
        audio_step3 = "media/audio/parallel_lines_transversal/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Indicate the two angles
        self.play(Indicate(self.objects["arc1"], color=GREEN, run_time=1),
                  Indicate(self.objects["arc2"], color=GREEN, run_time=1))
        self.play(Create(self.objects["arc1"]), Create(self.objects["arc2"]),
                  Write(self.objects["label1"]), Write(self.objects["label2"]), run_time=2.0)
        remaining_3 = max(0.1, 5.0 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4: Visual proof by rotating a copy of one angle onto the other
        audio_step4 = "media/audio/parallel_lines_transversal/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Focus on the first angle
        self.play(FocusOn(self.objects["arc1"]))
        # Create copy and animate transformation
        self.play(self.objects["arc1_copy"].animate.move_to(self.objects["arc1"].get_center()))
        self.wait(max(0.1, 0.5))
        # Rotate and translate the copy to match the second angle
        self.play(
            self.objects["arc1_copy"].animate.rotate(180 * DEGREES).move_to(self.objects["arc2"].get_center()),
            run_time=3.0
        )
        remaining_4 = max(0.1, 6.0 - 0.5 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5: Show equality
        audio_step5 = "media/audio/parallel_lines_transversal/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Circumscribe the two angles together
        angle_group = VGroup(self.objects["arc1"], self.objects["arc2"])
        self.play(Circumscribe(angle_group, color=YELLOW, run_time=1.5))
        self.play(Write(self.objects["equal_sign"]), Write(self.objects["explanation"]), run_time=2.0)
        remaining_5 = max(0.1, 5.0 - 1.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))