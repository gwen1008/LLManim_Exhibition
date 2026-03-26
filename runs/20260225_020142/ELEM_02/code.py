'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing multiplication (3 × 4) as repeated addition, showing the equivalence between 3 groups of 4 and a total of 12.
# 2. Layout Strategy: Use three-zone layout.
#    - Header Region: [y=3.5] for Title "Visualizing Multiplication: 3 × 4"
#    - Main Content: [Center y=0] for the star grid and the final horizontal array.
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text.
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for the grid and array to keep elements together. Position the grid and array at the same center point (content_center) to ensure smooth transformation. Place equation below with sufficient buff.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Write title.
#    - Step 2: Create first row of stars and its label.
#    - Step 3: Create second and third rows, their labels, and the initial equation.
#    - Step 4: Indicate the grid, fade out row labels.
#    - Step 5: Transform grid into a horizontal array.
#    - Step 6: Circumscribe the array, transform the equation to show the result.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create title
        title = Text("Visualizing Multiplication: 3 × 4", font_size=48, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Create the 3x4 grid of stars
        star_radius = 0.2
        buff_x, buff_y = 0.6, 0.6
        rows = []
        for r in range(3):
            row_stars = VGroup()
            for c in range(4):
                star = Star(outer_radius=star_radius, color=BLUE, fill_opacity=0.8, stroke_width=2)
                star.shift(c * buff_x * RIGHT + r * buff_y * DOWN)
                row_stars.add(star)
            rows.append(row_stars)
        grid_group = VGroup(*rows)
        grid_group.move_to(content_center)
        self.objects["grid_group"] = grid_group
        # Also store rows for easy access in steps
        self.objects["grid_group[0]"] = rows[0]
        self.objects["grid_group[1]"] = rows[1]
        self.objects["grid_group[2]"] = rows[2]

        # Create row labels
        row_label_1 = Text("Group 1", font_size=30, color=YELLOW)
        row_label_1.next_to(rows[0], LEFT, buff=0.5)
        self.objects["row_label_1"] = row_label_1

        row_label_2 = Text("Group 2", font_size=30, color=YELLOW)
        row_label_2.next_to(rows[1], LEFT, buff=0.5)
        self.objects["row_label_2"] = row_label_2

        row_label_3 = Text("Group 3", font_size=30, color=YELLOW)
        row_label_3.next_to(rows[2], LEFT, buff=0.5)
        self.objects["row_label_3"] = row_label_3

        # Initial equation
        equation_initial = MathTex(r"3 \times 4 = ?", font_size=40, color=WHITE)
        equation_initial.next_to(grid_group, DOWN, buff=1.0)
        self.objects["equation_initial"] = equation_initial

        # Create the horizontal array of 12 stars (target for transformation)
        array_stars = VGroup()
        for i in range(12):
            star = Star(outer_radius=star_radius, color=BLUE, fill_opacity=0.8, stroke_width=2)
            array_stars.add(star)
        array_stars.arrange(RIGHT, buff=0.4)
        array_stars.move_to(content_center)
        self.objects["array_group"] = array_stars

        # Final equation
        equation_final = MathTex(r"3 \times 4 = 12", font_size=40, color=GREEN)
        equation_final.next_to(array_stars, DOWN, buff=1.0)
        self.objects["equation_final"] = equation_final

        # Explanation text (initial content)
        explanation_text = Text("We begin with 3 groups, each containing 4 stars.", font_size=28, color=GRAY_B)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 6.12 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(
            Create(self.objects["grid_group[0]"]),
            Write(self.objects["row_label_1"]),
            run_time=2.0
        )
        remaining_2 = max(0.1, 2.832 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(
            Create(self.objects["grid_group[1]"]),
            Write(self.objects["row_label_2"]),
            Create(self.objects["grid_group[2]"]),
            Write(self.objects["row_label_3"]),
            Write(self.objects["equation_initial"]),
            run_time=5.0
        )
        remaining_3 = max(0.1, 8.448 - 5.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # signal_action: Indicate grid_group with YELLOW
        self.play(Indicate(self.objects["grid_group"], color=YELLOW, run_time=1))
        self.play(
            FadeOut(self.objects["row_label_1"]),
            FadeOut(self.objects["row_label_2"]),
            FadeOut(self.objects["row_label_3"]),
            run_time=2.0
        )
        remaining_4 = max(0.1, 6.912 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(ReplacementTransform(self.objects["grid_group"], self.objects["array_group"]), run_time=3.0)
        remaining_5 = max(0.1, 5.928 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # signal_action: Circumscribe array_group with GREEN
        self.play(Circumscribe(self.objects["array_group"], color=GREEN, run_time=1))
        self.play(ReplacementTransform(self.objects["equation_initial"], self.objects["equation_final"]), run_time=2.0)
        remaining_6 = max(0.1, 6.984 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_6))