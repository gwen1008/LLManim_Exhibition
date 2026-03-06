'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the equivalence of fractions 1/2 and 2/4 using two geometric circles (pizzas).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for two pizzas side-by-side
#    - Footer Region: [Bottom y=-3.5] for final equivalence equation
# 3. Anti-Overlap Check:
#    - Strategy: Place pizzas at LEFT*3.5 and RIGHT*3.5 from center. Use VGroups for each pizza's components.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Create left pizza circle.
#    - Divide left pizza with a line.
#    - Fill one half (sector).
#    - Create right pizza circle.
#    - Divide right pizza with two lines (cross).
#    - Fill two quarters (sectors).
#    - Label fractions below pizzas.
#    - Transform labels into final equivalence equation at bottom.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_two_identical_130c2684c9/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan
        # title
        title = Text("Visualizing Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # pizza_left
        pizza_left = Circle(radius=2.0, color=WHITE, stroke_width=3)
        pizza_left.set_fill(color=GRAY_C, opacity=0.2)
        pizza_left.move_to(content_center + 3.5 * LEFT)
        self.objects["pizza_left"] = pizza_left

        # pizza_right
        pizza_right = Circle(radius=2.0, color=WHITE, stroke_width=3)
        pizza_right.set_fill(color=GRAY_C, opacity=0.2)
        pizza_right.move_to(content_center + 3.5 * RIGHT)
        self.objects["pizza_right"] = pizza_right

        # div_line_left
        div_line_left = Line(start=2 * UP, end=2 * DOWN, color=WHITE, stroke_width=3)
        div_line_left.move_to(pizza_left.get_center())
        self.objects["div_line_left"] = div_line_left

        # div_line_right_v
        div_line_right_v = Line(start=2 * UP, end=2 * DOWN, color=WHITE, stroke_width=3)
        div_line_right_v.move_to(pizza_right.get_center())
        self.objects["div_line_right_v"] = div_line_right_v

        # div_line_right_h
        div_line_right_h = Line(start=2 * LEFT, end=2 * RIGHT, color=WHITE, stroke_width=3)
        div_line_right_h.move_to(pizza_right.get_center())
        self.objects["div_line_right_h"] = div_line_right_h

        # sector_left
        sector_left = Sector(radius=2.0, angle=PI, start_angle=-PI/2)
        sector_left.set_stroke(width=0)
        sector_left.set_fill(color=BLUE, opacity=0.7)
        sector_left.move_to(pizza_left.get_center())
        self.objects["sector_left"] = sector_left

        # sector_right_top
        sector_right_top = Sector(radius=2.0, angle=PI/2, start_angle=0)
        sector_right_top.set_stroke(width=0)
        sector_right_top.set_fill(color=BLUE, opacity=0.7)
        sector_right_top.move_to(pizza_right.get_center())
        self.objects["sector_right_top"] = sector_right_top

        # sector_right_bottom
        sector_right_bottom = Sector(radius=2.0, angle=PI/2, start_angle=-PI/2)
        sector_right_bottom.set_stroke(width=0)
        sector_right_bottom.set_fill(color=BLUE, opacity=0.7)
        sector_right_bottom.move_to(pizza_right.get_center())
        self.objects["sector_right_bottom"] = sector_right_bottom

        # label_frac_left
        label_frac_left = MathTex(r"\frac{1}{2}", color=YELLOW, font_size=48)
        label_frac_left.next_to(pizza_left, DOWN, buff=0.8)
        self.objects["label_frac_left"] = label_frac_left

        # label_frac_right
        label_frac_right = MathTex(r"\frac{2}{4}", color=YELLOW, font_size=48)
        label_frac_right.next_to(pizza_right, DOWN, buff=0.8)
        self.objects["label_frac_right"] = label_frac_right

        # equation_final
        equation_final = MathTex(r"\frac{1}{2} = \frac{2}{4}", color=GREEN, font_size=56)
        equation_final.move_to(footer_anchor)
        self.objects["equation_final"] = equation_final

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        self.play(Create(self.objects["pizza_left"]), run_time=1.0)
        remaining_1 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        self.play(Create(self.objects["div_line_left"]), run_time=1.5)
        remaining_2 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        self.play(Indicate(self.objects["sector_left"], color=YELLOW, run_time=1))
        self.play(DrawBorderThenFill(self.objects["sector_left"]), run_time=2.5)
        remaining_3 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        self.play(Create(self.objects["pizza_right"]), run_time=1.0)
        self.wait(max(0.1, 0.2))
        self.play(
            Create(self.objects["div_line_right_v"]),
            Create(self.objects["div_line_right_h"]),
            run_time=2.0
        )
        remaining_4 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        self.play(
            Indicate(self.objects["sector_right_top"], color=YELLOW, run_time=0.6),
            Indicate(self.objects["sector_right_bottom"], color=YELLOW, run_time=0.6)
        )
        self.play(
            DrawBorderThenFill(self.objects["sector_right_top"]),
            DrawBorderThenFill(self.objects["sector_right_bottom"]),
            run_time=2.5
        )
        remaining_5 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        self.play(
            Write(self.objects["label_frac_left"]),
            Write(self.objects["label_frac_right"]),
            run_time=3.0
        )
        remaining_6 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        self.play(
            Circumscribe(
                VGroup(
                    self.objects["sector_left"],
                    self.objects["sector_right_top"],
                    self.objects["sector_right_bottom"]
                ),
                color=GREEN,
                run_time=1
            )
        )
        # Create a temporary VGroup of the two labels to transform into the final equation
        labels_group = VGroup(self.objects["label_frac_left"], self.objects["label_frac_right"])
        self.play(
            TransformMatchingTex(labels_group, self.objects["equation_final"]),
            run_time=2.5
        )
        remaining_7 = max(0.1, 4.0 - (1 + 2.5) + 0.5)
        self.wait(max(0.1, remaining_7))