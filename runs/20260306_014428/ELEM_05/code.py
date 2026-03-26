'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the rounding of a decimal (3.7) to the nearest whole number (4) using a number line, focusing on distance comparison.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line and visual elements
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for related elements (e.g., tick and label). Position distance comparison segments above the number line to avoid clutter.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1: Draw number line.
#    - Step 2: Show integer ticks (3,4) and the decimal point 3.7.
#    - Step 3: Draw distance lines from 3.7 to 3 and 4 on the number line.
#    - Step 4: Lift and compare the distances, showing lengths 0.7 and 0.3.
#    - Step 5: Animate the point moving to 4, showing the rounding result.
#    - Step 6: Display final conclusion text.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # [missing audio] self.add_sound("media/audio/Create_a_number_line_a4afeaa881/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Rounding on the Number Line: 3.7 to 4", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # number_line
        number_line = NumberLine(x_range=[0, 7, 1], length=7, include_numbers=False, color=WHITE)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # tick_3
        tick_3 = Line(start=DOWN*0.15, end=UP*0.15, color=GREEN, stroke_width=6)
        tick_3.move_to(content_center + RIGHT*3)
        self.objects["tick_3"] = tick_3

        # label_3
        label_3 = MathTex("3", color=GREEN)
        label_3.next_to(tick_3, DOWN, buff=0.2)
        self.objects["label_3"] = label_3

        # tick_4
        tick_4 = Line(start=DOWN*0.15, end=UP*0.15, color=GREEN, stroke_width=6)
        tick_4.move_to(content_center + RIGHT*4)
        self.objects["tick_4"] = tick_4

        # label_4
        label_4 = MathTex("4", color=GREEN)
        label_4.next_to(tick_4, DOWN, buff=0.2)
        self.objects["label_4"] = label_4

        # point_3_7
        point_3_7 = Dot(radius=0.08, color=YELLOW)
        point_3_7.move_to(content_center + RIGHT*3.7)
        self.objects["point_3_7"] = point_3_7

        # label_3_7
        label_3_7 = MathTex("3.7", color=YELLOW)
        label_3_7.next_to(point_3_7, UP, buff=0.15)
        self.objects["label_3_7"] = label_3_7

        # dist_line_to_3
        dist_line_to_3 = Line(
            start=content_center + RIGHT*3.7,
            end=content_center + RIGHT*3,
            color=RED,
            stroke_width=4
        )
        self.objects["dist_line_to_3"] = dist_line_to_3

        # dist_line_to_4
        dist_line_to_4 = Line(
            start=content_center + RIGHT*3.7,
            end=content_center + RIGHT*4,
            color=BLUE,
            stroke_width=4
        )
        self.objects["dist_line_to_4"] = dist_line_to_4

        # dist_compare_to_3
        dist_compare_to_3 = Line(
            start=content_center + RIGHT*3.7 + UP*0.5,
            end=content_center + RIGHT*3 + UP*0.5,
            color=RED,
            stroke_width=4
        )
        self.objects["dist_compare_to_3"] = dist_compare_to_3

        # dist_compare_to_4
        dist_compare_to_4 = Line(
            start=content_center + RIGHT*3.7 + UP*0.5,
            end=content_center + RIGHT*4 + UP*0.5,
            color=BLUE,
            stroke_width=4
        )
        self.objects["dist_compare_to_4"] = dist_compare_to_4

        # label_dist_3
        label_dist_3 = MathTex("0.7", color=RED)
        label_dist_3.next_to(dist_compare_to_3, UP, buff=0.1)
        self.objects["label_dist_3"] = label_dist_3

        # label_dist_4
        label_dist_4 = MathTex("0.3", color=BLUE)
        label_dist_4.next_to(dist_compare_to_4, UP, buff=0.1)
        self.objects["label_dist_4"] = label_dist_4

        # explanation_text
        explanation_text = Text(
            "3.7 is closer to 4 than to 3. Therefore, it rounds to 4.",
            color=WHITE,
            font_size=28
        )
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        self.play(Create(self.objects["number_line"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        self.play(Indicate(self.objects["tick_3"], color=GREEN),
                  Indicate(self.objects["label_3"], color=GREEN),
                  Indicate(self.objects["tick_4"], color=GREEN),
                  Indicate(self.objects["label_4"], color=GREEN),
                  run_time=1)
        self.play(AnimationGroup(
            Create(self.objects["tick_3"]),
            Write(self.objects["label_3"]),
            Create(self.objects["tick_4"]),
            Write(self.objects["label_4"]),
            Create(self.objects["point_3_7"]),
            Write(self.objects["label_3_7"]),
            lag_ratio=0.1
        ), run_time=2.0)
        remaining_2 = max(0.1, 3.0 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        self.play(Indicate(self.objects["point_3_7"], color=YELLOW, run_time=1))
        self.play(AnimationGroup(
            Create(self.objects["dist_line_to_3"]),
            Create(self.objects["dist_line_to_4"]),
            lag_ratio=0.2
        ), run_time=2.0)
        remaining_3 = max(0.1, 3.0 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        self.play(Circumscribe(VGroup(self.objects["dist_line_to_3"], self.objects["dist_line_to_4"]),
                               color=YELLOW,
                               run_time=1))
        self.play(AnimationGroup(
            Transform(self.objects["dist_line_to_3"], self.objects["dist_compare_to_3"]),
            Transform(self.objects["dist_line_to_4"], self.objects["dist_compare_to_4"]),
            Write(self.objects["label_dist_3"]),
            Write(self.objects["label_dist_4"]),
            lag_ratio=0.2
        ), run_time=3.0)
        remaining_4 = max(0.1, 4.0 - (1 + 3.0) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        self.play(Indicate(self.objects["label_dist_4"], color=BLUE, run_time=1))

        # Create a new dot at position 4 and a new label "4"
        point_at_4 = Dot(radius=0.08, color=YELLOW)
        point_at_4.move_to(content_center + RIGHT*4)
        label_4_new = MathTex("4", color=YELLOW)
        label_4_new.next_to(point_at_4, UP, buff=0.15)

        self.play(
            Transform(self.objects["point_3_7"], point_at_4),
            Transform(self.objects["label_3_7"], label_4_new),
            run_time=1.5
        )
        # Update the registry for the transformed objects
        self.objects["point_3_7"] = point_at_4
        self.objects["label_3_7"] = label_4_new

        # Highlight integer 4
        self.play(
            Indicate(self.objects["tick_4"], color=GREEN),
            Indicate(self.objects["label_4"], color=GREEN),
            run_time=0.5
        )
        remaining_5 = max(0.1, 3.0 - (1 + 1.5 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        self.play(Write(self.objects["explanation_text"]), run_time=2.5)
        remaining_6 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_6))