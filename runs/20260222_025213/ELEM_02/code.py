'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing multiplication as repeated addition using a 3×4 grid of stars.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Multiplication: 3 × 4"
#    - Main Content: [Center y=0] for the 3×4 star grid and its transformation into a cluster.
#    - Footer Region: [Bottom y=-3.5] for the equation and final count label.
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for each row and the full grid. Position grid at ORIGIN. Equation and label at bottom.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Write title.
#    - Step 2: Create first row of 4 stars.
#    - Step 3: Indicate row1, create row2.
#    - Step 4: Indicate row2, create row3.
#    - Step 5: Circumscribe full grid, write equation "3 × 4 = ?".
#    - Step 6: Indicate full grid, transform grid into a circular cluster.
#    - Step 7: Circumscribe cluster, transform equation to "3 × 4 = 12".
#    - Step 8: Write final count label "Total: 12".
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create anchors
        title_anchor = 3.5 * UP
        grid_center = ORIGIN
        equation_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create title
        title = Text("Multiplication: 3 × 4", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Create stars for each row
        # Row 1 positions: [(-1.2, 0.8, 0), (-0.4, 0.8, 0), (0.4, 0.8, 0), (1.2, 0.8, 0)]
        row1_stars = VGroup(
            Star(n=5, color=BLUE, outer_radius=0.2).move_to([-1.2, 0.8, 0]),
            Star(n=5, color=BLUE, outer_radius=0.2).move_to([-0.4, 0.8, 0]),
            Star(n=5, color=BLUE, outer_radius=0.2).move_to([0.4, 0.8, 0]),
            Star(n=5, color=BLUE, outer_radius=0.2).move_to([1.2, 0.8, 0])
        )
        row1_stars.move_to(grid_center + UP*0.8)
        self.objects["row1"] = row1_stars

        # Row 2 positions: [(-1.2, 0.0, 0), (-0.4, 0.0, 0), (0.4, 0.0, 0), (1.2, 0.0, 0)]
        row2_stars = VGroup(
            Star(n=5, color=BLUE, outer_radius=0.2).move_to([-1.2, 0.0, 0]),
            Star(n=5, color=BLUE, outer_radius=0.2).move_to([-0.4, 0.0, 0]),
            Star(n=5, color=BLUE, outer_radius=0.2).move_to([0.4, 0.0, 0]),
            Star(n=5, color=BLUE, outer_radius=0.2).move_to([1.2, 0.0, 0])
        )
        row2_stars.move_to(grid_center)
        self.objects["row2"] = row2_stars

        # Row 3 positions: [(-1.2, -0.8, 0), (-0.4, -0.8, 0), (0.4, -0.8, 0), (1.2, -0.8, 0)]
        row3_stars = VGroup(
            Star(n=5, color=BLUE, outer_radius=0.2).move_to([-1.2, -0.8, 0]),
            Star(n=5, color=BLUE, outer_radius=0.2).move_to([-0.4, -0.8, 0]),
            Star(n=5, color=BLUE, outer_radius=0.2).move_to([0.4, -0.8, 0]),
            Star(n=5, color=BLUE, outer_radius=0.2).move_to([1.2, -0.8, 0])
        )
        row3_stars.move_to(grid_center + DOWN*0.8)
        self.objects["row3"] = row3_stars

        # Full grid VGroup
        full_grid = VGroup(row1_stars, row2_stars, row3_stars)
        full_grid.move_to(grid_center)
        self.objects["full_grid"] = full_grid

        # Equation: 3 × 4 = ?
        equation_mult = MathTex("3 \\times 4 = ?", color=YELLOW, font_size=32)
        equation_mult.move_to(equation_anchor)
        self.objects["equation_mult"] = equation_mult

        # Equation: 3 × 4 = 12
        equation_result = MathTex("3 \\times 4 = 12", color=GREEN, font_size=32)
        equation_result.move_to(equation_anchor)
        self.objects["equation_result"] = equation_result

        # Count label: Total: 12
        count_label = Text("Total: 12", color=BLUE, font_size=28)
        count_label.next_to(equation_result, DOWN, buff=0.8)
        self.objects["count_label"] = count_label

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Step 1
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["title"]))
        self.wait(max(0.1, max(0.1, 7.44 - 1.0)))

        # Step 2
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["row1"]))
        self.wait(max(0.1, max(0.1, 6.024 - 1.0)))

        # Step 3
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["row1"], color=YELLOW))
        self.play(Create(self.objects["row2"]))
        self.wait(max(0.1, max(0.1, 5.208 - 2.0)))

        # Step 4
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["row2"], color=YELLOW))
        self.play(Create(self.objects["row3"]))
        self.wait(max(0.1, max(0.1, 4.584 - 2.0)))

        # Step 5
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["full_grid"], color=PINK, run_time=1))
        self.play(Write(self.objects["equation_mult"]))
        self.wait(max(0.1, max(0.1, 5.496 - 2.0)))

        # Step 6
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["full_grid"], color=ORANGE))
        # Create target cluster positions (circular arrangement)
        cluster_center = grid_center
        radius = 1.0
        angles = [i * 2 * PI / 12 for i in range(12)]
        cluster_positions = []
        for angle in angles:
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            cluster_positions.append([x, y, 0])
        # Create target VGroup for transformation
        cluster_stars = VGroup()
        for i, pos in enumerate(cluster_positions):
            star = Star(n=5, color=BLUE, outer_radius=0.2).move_to(pos)
            cluster_stars.add(star)
        cluster_stars.move_to(cluster_center)
        # Animate transformation from grid to cluster
        self.play(Transform(self.objects["full_grid"], cluster_stars))
        self.wait(max(0.1, max(0.1, 3.96 - 2.0)))

        # Step 7
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["full_grid"], color=GREEN, run_time=1))
        self.play(ReplacementTransform(self.objects["equation_mult"], self.objects["equation_result"]))
        self.wait(max(0.1, max(0.1, 5.424 - 2.0)))

        # Step 8
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_07.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["count_label"]))
        self.wait(max(0.1, max(0.1, 3.408 - 1.0)))