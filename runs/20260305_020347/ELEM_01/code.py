'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Demonstrate the equivalence of 1/2 and 2/4 using two identical pizzas (circles).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for two pizzas side-by-side
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Place pizzas at x=-3 and x=3, centered at y=0. Use VGroups for each pizza and its labels.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Will assign `remaining_N = json_duration - anim_time + 0.5` for each step.
# 5. Animation Flow:
#    - Show title.
#    - Create two identical circles (pizzas).
#    - Cut first pizza into 2 equal parts, highlight 1 slice (1/2).
#    - Cut second pizza into 4 equal parts, highlight 2 slices (2/4).
#    - Extract highlighted slices and move them together for comparison.
#    - Show equivalence label.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Title
        title = Text("分數的等值：1/2 等於 2/4", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.objects["title"] = title

        # Two pizza circles
        pizza_left = Circle(radius=2, color=WHITE, stroke_width=4)
        pizza_left.move_to(LEFT * 3)
        self.objects["pizza_left"] = pizza_left

        pizza_right = Circle(radius=2, color=WHITE, stroke_width=4)
        pizza_right.move_to(RIGHT * 3)
        self.objects["pizza_right"] = pizza_right

        # Labels for whole pizzas
        label_left = Text("1 個披薩", font_size=30).next_to(pizza_left, DOWN, buff=0.3)
        self.objects["label_left"] = label_left
        label_right = Text("1 個披薩", font_size=30).next_to(pizza_right, DOWN, buff=0.3)
        self.objects["label_right"] = label_right

        # Sectors for left pizza (2 equal parts)
        sector_left_1 = Sector(radius=2, angle=PI, start_angle=0, color=BLUE, fill_opacity=0.0, stroke_width=0)
        sector_left_1.move_to(pizza_left.get_center())
        sector_left_2 = Sector(radius=2, angle=PI, start_angle=PI, color=BLUE, fill_opacity=0.0, stroke_width=0)
        sector_left_2.move_to(pizza_left.get_center())
        self.objects["sector_left_1"] = sector_left_1
        self.objects["sector_left_2"] = sector_left_2

        # Highlighted slice for 1/2 (will be filled)
        highlight_left = sector_left_1.copy().set_fill(YELLOW, opacity=0.7)
        self.objects["highlight_left"] = highlight_left

        # Sectors for right pizza (4 equal parts)
        sectors_right = VGroup()
        for i in range(4):
            sector = Sector(radius=2, angle=PI/2, start_angle=i * PI/2, color=GREEN, fill_opacity=0.0, stroke_width=0)
            sector.move_to(pizza_right.get_center())
            sectors_right.add(sector)
        self.objects["sectors_right"] = sectors_right

        # Highlighted slices for 2/4 (two adjacent quarters)
        highlight_right_1 = sectors_right[0].copy().set_fill(YELLOW, opacity=0.7)
        highlight_right_2 = sectors_right[1].copy().set_fill(YELLOW, opacity=0.7)
        self.objects["highlight_right_1"] = highlight_right_1
        self.objects["highlight_right_2"] = highlight_right_2

        # Cutting lines
        line_left = Line(pizza_left.get_center() + UP * 2, pizza_left.get_center() + DOWN * 2, color=WHITE)
        self.objects["line_left"] = line_left
        lines_right = VGroup(
            Line(pizza_right.get_center() + UP * 2, pizza_right.get_center() + DOWN * 2, color=WHITE),
            Line(pizza_right.get_center() + LEFT * 2, pizza_right.get_center() + RIGHT * 2, color=WHITE)
        )
        self.objects["lines_right"] = lines_right

        # Fraction labels
        frac_left = MathTex(r"\frac{1}{2}", font_size=60).next_to(pizza_left, UP, buff=0.5)
        self.objects["frac_left"] = frac_left
        frac_right = MathTex(r"\frac{2}{4}", font_size=60).next_to(pizza_right, UP, buff=0.5)
        self.objects["frac_right"] = frac_right

        # Extracted slices for comparison
        extracted_left = highlight_left.copy()
        extracted_right = VGroup(highlight_right_1.copy(), highlight_right_2.copy())
        self.objects["extracted_left"] = extracted_left
        self.objects["extracted_right"] = extracted_right

        # Comparison position (center)
        comparison_pos = ORIGIN + DOWN * 0.5
        extracted_left_target = extracted_left.copy().move_to(comparison_pos + LEFT * 1.5)
        extracted_right_target = extracted_right.copy().move_to(comparison_pos + RIGHT * 1.5)
        self.objects["extracted_left_target"] = extracted_left_target
        self.objects["extracted_right_target"] = extracted_right_target

        # Equivalence label and arrow
        equals = MathTex(r"=", font_size=80).move_to(comparison_pos)
        self.objects["equals"] = equals
        explanation = Text("兩份披薩面積相同，所以 1/2 = 2/4", font_size=36, color=YELLOW)
        explanation.to_edge(DOWN, buff=0.5)
        self.objects["explanation"] = explanation

        # ========== PHASE 2: Animation Sequence ==========
        # Step 1: Show title
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2: Create two pizzas
        self.play(
            Create(self.objects["pizza_left"]),
            Create(self.objects["pizza_right"]),
            run_time=2.0
        )
        self.play(
            Write(self.objects["label_left"]),
            Write(self.objects["label_right"]),
            run_time=1.5
        )
        remaining_2 = max(0.1, 4.0 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3: Cut left pizza into 2, show 1/2
        self.play(Create(self.objects["line_left"]), run_time=1.5)
        self.play(
            self.objects["sector_left_1"].animate.set_fill(BLUE, 0.3),
            self.objects["sector_left_2"].animate.set_fill(BLUE, 0.3),
            run_time=1.0
        )
        self.play(
            self.objects["sector_left_1"].animate.set_fill(BLUE, 0.0),
            self.objects["sector_left_2"].animate.set_fill(BLUE, 0.0),
            run_time=0.5
        )
        self.play(FadeIn(self.objects["highlight_left"]), run_time=1.0)
        self.play(Write(self.objects["frac_left"]), run_time=1.0)
        remaining_3 = max(0.1, 5.0 - 5.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4: Cut right pizza into 4, show 2/4
        self.play(Create(self.objects["lines_right"]), run_time=2.0)
        for sector in self.objects["sectors_right"]:
            self.play(sector.animate.set_fill(GREEN, 0.3), run_time=0.3)
            self.play(sector.animate.set_fill(GREEN, 0.0), run_time=0.2)
        self.play(
            FadeIn(self.objects["highlight_right_1"]),
            FadeIn(self.objects["highlight_right_2"]),
            run_time=1.5
        )
        self.play(Write(self.objects["frac_right"]), run_time=1.0)
        remaining_4 = max(0.1, 6.0 - 6.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5: Extract highlighted slices
        self.play(
            Transform(self.objects["highlight_left"], self.objects["extracted_left_target"]),
            Transform(self.objects["highlight_right_1"], self.objects["extracted_right_target"][0]),
            Transform(self.objects["highlight_right_2"], self.objects["extracted_right_target"][1]),
            run_time=2.5
        )
        remaining_5 = max(0.1, 4.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6: Compare and show equivalence
        self.play(Write(self.objects["equals"]), run_time=1.0)
        self.play(Circumscribe(VGroup(
            self.objects["extracted_left_target"],
            self.objects["extracted_right_target"]
        ), color=GREEN, run_time=2.0))
        self.play(Write(self.objects["explanation"]), run_time=2.0)
        remaining_6 = max(0.1, 5.0 - 5.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))