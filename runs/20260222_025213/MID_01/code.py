'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing translation and displacement on a number line, showing the movement from point A (-2) to point B (3) and calculating the magnitude.
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line and points
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Use VGroups for number line components. Position labels above points. Place magnitude label above arrow. Keep step explanation at bottom.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
#    - Create number line, ticks, labels.
#    - Create points A and B with labels.
#    - Show ghost point moving from A to B.
#    - Draw displacement arrow and scale it.
#    - Show magnitude calculation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        self.objects = {}

        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Translation and Displacement on a Number Line", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Number Line (main line)
        number_line = Line(start=5*LEFT, end=5*RIGHT, color=GRAY_B, stroke_width=4)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # Ticks Group
        ticks = VGroup()
        for x in range(-5, 6):
            tick = Line(start=[x, -0.2, 0], end=[x, 0.2, 0], color=WHITE, stroke_width=2)
            ticks.add(tick)
        ticks.move_to(content_center)
        self.objects["ticks_group"] = ticks

        # Labels Group
        labels = VGroup()
        for x in range(-5, 6):
            label = MathTex(str(x), color=WHITE, font_size=24)
            label.move_to([x, -0.6, 0])
            labels.add(label)
        labels.move_to(content_center)
        self.objects["labels_group"] = labels

        # Point A and its label
        point_a = Dot(point=2*LEFT, radius=0.08, color=BLUE, fill_opacity=1)
        self.objects["point_a"] = point_a
        label_a = MathTex("A(-2)", color=BLUE, font_size=28)
        label_a.next_to(point_a, UP, buff=0.3)
        self.objects["label_a"] = label_a

        # Point B and its label
        point_b = Dot(point=3*RIGHT, radius=0.08, color=GREEN, fill_opacity=1)
        self.objects["point_b"] = point_b
        label_b = MathTex("B(3)", color=GREEN, font_size=28)
        label_b.next_to(point_b, UP, buff=0.3)
        self.objects["label_b"] = label_b

        # Ghost point (initially at A)
        ghost_point = Dot(point=point_a.get_center(), radius=0.08, color=BLUE, fill_opacity=0.4)
        self.objects["ghost_point"] = ghost_point

        # Displacement arrow (final, from A to B)
        displacement_arrow_final = Arrow(
            start=point_a.get_center(),
            end=point_b.get_center(),
            buff=0,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["displacement_arrow_final"] = displacement_arrow_final

        # Zero-length arrow at A (for scaling animation)
        displacement_arrow_zero = Arrow(
            start=point_a.get_center(),
            end=point_a.get_center(),
            buff=0,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["displacement_arrow_zero"] = displacement_arrow_zero

        # Magnitude label
        magnitude_label = MathTex("|3 - (-2)| = 5", color=YELLOW, font_size=32)
        magnitude_label.next_to(displacement_arrow_final, UP, buff=0.5)
        self.objects["magnitude_label"] = magnitude_label

        # Step explanation text (initial content)
        step_explanation = Text(
            "Step 1: Construct the number line from -5 to 5.",
            color=GRAY_B,
            font_size=26
        )
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Step 1
        audio_file = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["step_explanation"]))
        self.play(Create(self.objects["number_line"]))
        self.wait(max(0.1, max(0.1, 5.856 - 2)))

        # Step 2
        audio_file = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Update explanation
        new_explanation = Text(
            "Step 2: Add tick marks and labels for each integer.",
            color=GRAY_B,
            font_size=26
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        self.play(Create(self.objects["ticks_group"]), Create(self.objects["labels_group"]))
        self.wait(max(0.1, max(0.1, 3.312 - 2)))

        # Step 3
        audio_file = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        new_explanation = Text(
            "Step 3: Plot point A at -2 and point B at 3.",
            color=GRAY_B,
            font_size=26
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Signal action for point_a
        self.play(Indicate(self.objects["point_a"], color=BLUE))
        self.play(Create(self.objects["point_a"]), Write(self.objects["label_a"]))
        self.wait(max(0.1, max(0.1, 7.344 - 3)))

        # Step 4 (Note: narrative is empty, but step exists)
        # No audio path provided, so skip audio
        new_explanation = Text(
            "Step 4: Plot point B.",
            color=GRAY_B,
            font_size=26
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Signal action for point_b
        self.play(Indicate(self.objects["point_b"], color=GREEN))
        self.play(Create(self.objects["point_b"]), Write(self.objects["label_b"]))
        self.wait(max(0.1, max(0.1, 2.0 - 2)))

        # Step 5
        audio_file = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        new_explanation = Text(
            "Step 5: Animate translation from A to B using a ghost point.",
            color=GRAY_B,
            font_size=26
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Signal action for ghost_point
        self.play(Circumscribe(self.objects["ghost_point"], color=BLUE, run_time=1))
        self.play(FadeIn(self.objects["ghost_point"]))
        self.wait(max(0.1, max(0.1, 8.088 - 2)))

        # Step 6
        audio_file = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        new_explanation = Text(
            "Step 6: The ghost point travels the distance.",
            color=GRAY_B,
            font_size=26
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Signal action for ghost_point
        self.play(Indicate(self.objects["ghost_point"], color=BLUE))
        # Move ghost point along a straight path
        path = Line(start=2*LEFT, end=3*RIGHT)
        self.play(MoveAlongPath(self.objects["ghost_point"], path), run_time=2)
        self.wait(max(0.1, max(0.1, 4.632 - 3)))

        # Step 7
        audio_file = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        new_explanation = Text(
            "Step 7: The displacement vector is shown as an arrow.",
            color=GRAY_B,
            font_size=26
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        self.play(Create(self.objects["displacement_arrow_final"]))
        self.wait(max(0.1, max(0.1, 6.816 - 2)))

        # Step 8
        audio_file = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_07.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        new_explanation = Text(
            "Step 8: The arrow scales up to show the magnitude of 5 units.",
            color=GRAY_B,
            font_size=26
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Signal action for displacement_arrow_zero
        self.play(Indicate(self.objects["displacement_arrow_zero"], color=YELLOW))
        # Transform zero-length arrow into final arrow
        self.play(Transform(self.objects["displacement_arrow_zero"], self.objects["displacement_arrow_final"]))
        self.wait(max(0.1, max(0.1, 7.92 - 2)))

        # Step 9
        audio_file = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_08.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        new_explanation = Text(
            "Step 9: Calculate the magnitude: |3 - (-2)| = 5.",
            color=GRAY_B,
            font_size=26
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Signal action for magnitude_label
        self.play(Circumscribe(self.objects["magnitude_label"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["magnitude_label"]))
        self.wait(max(0.1, max(0.1, 7.44 - 2)))

        # Final hold
        self.wait(max(0.1, 2))