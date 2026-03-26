'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing rounding to the nearest integer using a number line, comparing distances to the two nearest integers.
# 2. Layout Strategy: High-Low Split
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line and comparison
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Number line and comparison placed side-by-side in the main content area.
#    - Explanation text stacked vertically at the bottom.
#    - Use VGroups for composite objects (number line assembly).
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_XX.mp3"
# 5. Animation Flow:
#    - Create number line and integer labels.
#    - Place point 3.7.
#    - Draw distance segments on the number line.
#    - Transform segments to vertical comparison.
#    - Add comparison labels.
#    - Show explanation text.
#    - Morph point to 4 (rounding).
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan description
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        comparison_anchor = 3.5 * RIGHT  # X=3.5, Y=0

        # Create objects from layout_plan.objects
        # Title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Integer", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Number Line
        number_line = NumberLine(
            x_range=[2.5, 4.5, 0.1],
            length=8,
            include_numbers=False,
            color=GRAY_B  # LIGHT_GRAY -> GRAY_B
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # Tick and label for 3
        tick_3 = Line(start=DOWN*0.15, end=UP*0.15, color=WHITE, stroke_width=3)
        tick_3.move_to(content_center + 2 * LEFT)  # x = -2
        self.objects["tick_3"] = tick_3

        label_3 = MathTex("3", color=WHITE)
        label_3.next_to(tick_3, DOWN, buff=0.2)
        self.objects["label_3"] = label_3

        # Tick and label for 4
        tick_4 = Line(start=DOWN*0.15, end=UP*0.15, color=WHITE, stroke_width=3)
        tick_4.move_to(content_center + 2 * RIGHT)  # x = 2
        self.objects["tick_4"] = tick_4

        label_4 = MathTex("4", color=WHITE)
        label_4.next_to(tick_4, DOWN, buff=0.2)
        self.objects["label_4"] = label_4

        # Point 3.7 and label
        point_3_7_dot = Dot(radius=0.08, color=YELLOW)
        point_3_7_dot.move_to(content_center + 0.8 * RIGHT)  # x = 0.8
        self.objects["point_3_7_dot"] = point_3_7_dot

        label_3_7 = MathTex("3.7", color=YELLOW)
        label_3_7.next_to(point_3_7_dot, UP, buff=0.2)
        self.objects["label_3_7"] = label_3_7

        # Distance lines on number line
        dist_to_4_line = Line(
            start=content_center + 0.8 * RIGHT,
            end=content_center + 2 * RIGHT,
            color=GREEN,
            stroke_width=6
        )
        self.objects["dist_to_4_line"] = dist_to_4_line

        label_dist_4 = MathTex("0.3", color=GREEN)
        label_dist_4.next_to(dist_to_4_line, UP, buff=0.1)
        self.objects["label_dist_4"] = label_dist_4

        dist_to_3_line = Line(
            start=content_center + 2 * LEFT,
            end=content_center + 0.8 * RIGHT,
            color=RED,
            stroke_width=6
        )
        self.objects["dist_to_3_line"] = dist_to_3_line

        label_dist_3 = MathTex("0.7", color=RED)
        label_dist_3.next_to(dist_to_3_line, UP, buff=0.1)
        self.objects["label_dist_3"] = label_dist_3

        # Vertical comparison lines (targets for transformation)
        dist_to_4_vertical = Line(
            start=comparison_anchor + LEFT,
            end=comparison_anchor + LEFT + UP * 1.2,
            color=GREEN,
            stroke_width=6
        )
        self.objects["dist_to_4_vertical"] = dist_to_4_vertical

        dist_to_3_vertical = Line(
            start=comparison_anchor + RIGHT,
            end=comparison_anchor + RIGHT + UP * 2.8,
            color=RED,
            stroke_width=6
        )
        self.objects["dist_to_3_vertical"] = dist_to_3_vertical

        # Comparison labels
        comparison_label_left = MathTex("0.3", color=GREEN)
        comparison_label_left.next_to(dist_to_4_vertical, RIGHT, buff=0.2)
        self.objects["comparison_label_left"] = comparison_label_left

        comparison_label_right = MathTex("0.7", color=RED)
        comparison_label_right.next_to(dist_to_3_vertical, LEFT, buff=0.2)
        self.objects["comparison_label_right"] = comparison_label_right

        # Explanation text
        explanation_text_1 = Text("The distance from 3.7 to 4 is 0.3. The distance to 3 is 0.7.", color=GRAY_B, font_size=30)
        explanation_text_1.move_to(explanation_anchor)
        self.objects["explanation_text_1"] = explanation_text_1

        explanation_text_2 = Text("Since 0.3 < 0.7, 3.7 is closer to 4.", color=GRAY_B, font_size=30)
        explanation_text_2.next_to(explanation_text_1, DOWN, buff=0.3)
        self.objects["explanation_text_2"] = explanation_text_2

        explanation_text_3 = Text("Therefore, 3.7 rounds to the nearest integer, 4.", color=YELLOW, font_size=30)
        explanation_text_3.next_to(explanation_text_2, DOWN, buff=0.3)
        self.objects["explanation_text_3"] = explanation_text_3

        # Create a dot at 4 for final transformation target
        point_4_dot = Dot(radius=0.08, color=YELLOW)
        point_4_dot.move_to(content_center + 2 * RIGHT)  # at tick_4
        self.objects["point_4_dot"] = point_4_dot  # Not added initially

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["number_line"]))
        self.wait(max(0.1, max(0.1, 3.144 - 1)))  # Create run_time ~1

        # Step 2
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(
            Create(self.objects["tick_3"]),
            Write(self.objects["label_3"]),
            Create(self.objects["tick_4"]),
            Write(self.objects["label_4"])
        )
        self.wait(max(0.1, max(0.1, 2.832 - 1)))  # AnimationGroup run_time ~1

        # Step 3
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step_signal := {"type": "Indicate", "target": "point_3_7_dot", "color": "YELLOW"}:
            self.play(Indicate(self.objects["point_3_7_dot"], color=YELLOW))
        self.play(
            Create(self.objects["point_3_7_dot"]),
            Write(self.objects["label_3_7"])
        )
        self.wait(max(0.1, max(0.1, 3.768 - 2)))  # Indicate ~1 + AnimationGroup ~1

        # Step 4
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(
            Create(self.objects["dist_to_4_line"]),
            Write(self.objects["label_dist_4"]),
            Create(self.objects["dist_to_3_line"]),
            Write(self.objects["label_dist_3"])
        )
        self.wait(max(0.1, max(0.1, 5.88 - 2)))  # AnimationGroup run_time ~2

        # Step 5
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step_signal := {"type": "Circumscribe", "target": "label_dist_4", "color": "YELLOW"}:
            self.play(Circumscribe(self.objects["label_dist_4"], color=YELLOW, run_time=1))
        self.play(Transform(self.objects["dist_to_4_line"], self.objects["dist_to_4_vertical"]))
        self.wait(max(0.1, max(0.1, 5.184 - 2)))  # Circumscribe ~1 + Transform ~1

        # Step 6
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step_signal := {"type": "Circumscribe", "target": "label_dist_3", "color": "YELLOW"}:
            self.play(Circumscribe(self.objects["label_dist_3"], color=YELLOW, run_time=1))
        self.play(Transform(self.objects["dist_to_3_line"], self.objects["dist_to_3_vertical"]))
        self.wait(max(0.1, max(0.1, 2.592 - 2)))  # Circumscribe ~1 + Transform ~1

        # Step 7
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(
            Write(self.objects["comparison_label_left"]),
            Write(self.objects["comparison_label_right"])
        )
        self.wait(max(0.1, max(0.1, 6.96 - 1)))  # Write run_time ~1

        # Step 8
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_07.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(
            Write(self.objects["explanation_text_1"]),
            Write(self.objects["explanation_text_2"]),
            Write(self.objects["explanation_text_3"])
        )
        self.wait(max(0.1, max(0.1, 4.896 - 2)))  # Write run_time ~2

        # Step 9
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_08.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step_signal := {"type": "Indicate", "target": "label_4", "color": "YELLOW"}:
            self.play(Indicate(self.objects["label_4"], color=YELLOW))
        self.play(ReplacementTransform(self.objects["point_3_7_dot"], self.objects["point_4_dot"]))
        self.wait(max(0.1, max(0.1, 1.968 - 2)))  # Indicate ~1 + ReplacementTransform ~1

        # Final hold
        self.wait(max(0.1, 2))