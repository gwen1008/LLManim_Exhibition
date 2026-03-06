'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize multiplication as repeated addition (3 groups of 4) and then as a rectangular array (3x4 grid), showing that both represent 12.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Multiplication: 3 × 4"
#    - Main Content: [Center y=0] for stars and grid transformation.
#    - Footer Region: [Bottom y=-3.5] for equation "3 × 4 = 12"
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for each row of stars. Position rows initially with vertical spacing, then transform to a compact grid. Keep all content within safe zones.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Write title.
#    - Steps 2-4: Create three rows of 4 stars each (3 groups of 4).
#    - Step 5: Show multiplication expression "3 × 4" and circumscribe it.
#    - Steps 6-8: Transform rows into a compact 3x4 grid.
#    - Step 9: Transform expression into "3 × 4 = 12" and indicate the result.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP  # HEADER
        content_center = ORIGIN  # CONTENT
        footer_anchor = 3.5 * DOWN  # FOOTER

        # Object registry
        self.objects = {}

        # Create title
        title = Text("Multiplication: 3 × 4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Create row1 (first row of 4 stars)
        row1_stars = VGroup()
        for x in [-1.2, -0.4, 0.4, 1.2]:
            star = Circle(radius=0.15, color="#FFD700", fill_opacity=1)
            star.move_to(content_center + UP * 0.8 + RIGHT * x)
            row1_stars.add(star)
        self.objects["row1"] = row1_stars

        # Create row2 (second row of 4 stars)
        row2_stars = VGroup()
        for x in [-1.2, -0.4, 0.4, 1.2]:
            star = Circle(radius=0.15, color="#FFD700", fill_opacity=1)
            star.move_to(content_center + RIGHT * x)
            row2_stars.add(star)
        self.objects["row2"] = row2_stars

        # Create row3 (third row of 4 stars)
        row3_stars = VGroup()
        for x in [-1.2, -0.4, 0.4, 1.2]:
            star = Circle(radius=0.15, color="#FFD700", fill_opacity=1)
            star.move_to(content_center + DOWN * 0.8 + RIGHT * x)
            row3_stars.add(star)
        self.objects["row3"] = row3_stars

        # Create multiplication expression
        multiplication_expr = MathTex("3 \\times 4", color=YELLOW, font_size=36)
        multiplication_expr.move_to(footer_anchor + UP * 0.5)
        self.objects["multiplication_expr"] = multiplication_expr

        # Create result equation (initially not shown, stored for later transform)
        result_eq = MathTex("3 \\times 4 = 12", color=GREEN, font_size=36)
        result_eq.move_to(footer_anchor)
        self.objects["result_eq"] = result_eq

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["title"]))
        self.wait(max(0.1, max(0.1, 6.0 - 1.0)))  # Write run_time ~1s

        # Step 2
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["row1"]))
        self.wait(max(0.1, max(0.1, 6.264 - 1.0)))

        # Step 3
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["row2"]))
        self.wait(max(0.1, max(0.1, 2.832 - 1.0)))

        # Step 4
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate row3
        self.play(Indicate(self.objects["row3"], color=YELLOW))
        # Visual action: Create row3
        self.play(Create(self.objects["row3"]))
        # Total animation time: Indicate (~1s) + Create (~1s) = ~2s
        self.wait(max(0.1, max(0.1, 6.72 - 2.0)))

        # Step 5
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Circumscribe multiplication_expr
        self.play(Circumscribe(self.objects["multiplication_expr"], color=YELLOW, run_time=1))
        # Visual action: Write multiplication_expr
        self.play(Write(self.objects["multiplication_expr"]))
        # Total animation time: Circumscribe (1s) + Write (~1s) = ~2s
        self.wait(max(0.1, max(0.1, 4.92 - 2.0)))

        # Step 6
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Create target positions for compact grid (3x4, tighter spacing)
        # Target grid: 3 rows, 4 columns, centered at content_center
        grid_rows = []
        for r in range(3):
            row = VGroup()
            for c in range(4):
                x = (c - 1.5) * 0.6  # column spacing 0.6
                y = (1 - r) * 0.6    # row spacing 0.6, top row y=0.6, bottom y=-0.6
                star = Circle(radius=0.15, color="#FFD700", fill_opacity=1)
                star.move_to(content_center + RIGHT * x + UP * y)
                row.add(star)
            grid_rows.append(row)
        # Transform row1 to grid top row
        self.play(ReplacementTransform(self.objects["row1"], grid_rows[0]))
        self.wait(max(0.1, max(0.1, 7.008 - 1.0)))

        # Step 7 (no audio, duration 2.0)
        # Transform row2 to grid middle row
        self.play(ReplacementTransform(self.objects["row2"], grid_rows[1]))
        self.wait(max(0.1, max(0.1, 2.0 - 1.0)))

        # Step 8 (no audio, duration 2.0)
        # Transform row3 to grid bottom row
        self.play(ReplacementTransform(self.objects["row3"], grid_rows[2]))
        self.wait(max(0.1, max(0.1, 2.0 - 1.0)))

        # Step 9
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_08.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate result_eq
        self.play(Indicate(self.objects["result_eq"], color=GREEN))
        # Visual action: TransformMatchingTex from multiplication_expr to result_eq
        self.play(TransformMatchingTex(self.objects["multiplication_expr"], self.objects["result_eq"]))
        # Total animation time: Indicate (~1s) + TransformMatchingTex (~1s) = ~2s
        self.wait(max(0.1, max(0.1, 7.848 - 2.0)))

        # Final hold
        self.wait(max(0.1, 2))