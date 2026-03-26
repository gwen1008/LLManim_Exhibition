'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing fraction equivalence 1/2 = 2/4 using a concrete pizza analogy.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Fraction Equivalence: 1/2 = 2/4"
#    - Main Content: [Center y=0] Two pizzas side-by-side, left at x=-3.5, right at x=3.5.
#    - Footer Region: [Bottom y=-3.5] for final equation "1/2 = 2/4"
# 3. Anti-Overlap Check:
#    - Strategy: Position pizzas with sufficient horizontal spacing (7 units apart). Labels placed above each pizza. Final equation centered at bottom.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Show title.
#    - Draw left pizza, cut it, color half, label it 1/2.
#    - Draw right pizza, cut it into quarters, color two quarters, label it 2/4.
#    - Highlight colored areas, then show equivalence equation at bottom.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        pizza_left_center = 3.5 * LEFT
        pizza_right_center = 3.5 * RIGHT
        equation_anchor = 3.5 * DOWN

        # Object Registry
        self.objects = {}

        # Create objects from layout_plan
        # title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # pizza_left
        pizza_left = Circle(radius=2, color=WHITE, stroke_width=3)
        pizza_left.move_to(pizza_left_center)
        self.objects["pizza_left"] = pizza_left

        # pizza_right
        pizza_right = Circle(radius=2, color=WHITE, stroke_width=3)
        pizza_right.move_to(pizza_right_center)
        self.objects["pizza_right"] = pizza_right

        # label_left
        label_left = MathTex(r"\frac{1}{2}", color=WHITE, font_size=36)
        label_left.next_to(pizza_left, UP, buff=1.2)
        self.objects["label_left"] = label_left

        # label_right
        label_right = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        label_right.next_to(pizza_right, UP, buff=1.2)
        self.objects["label_right"] = label_right

        # cut_line_half
        cut_line_half = Line(DOWN*2, UP*2, color=WHITE, stroke_width=3)
        cut_line_half.move_to(pizza_left_center)
        self.objects["cut_line_half"] = cut_line_half

        # sector_half
        sector_half = Sector(radius=2, angle=PI, start_angle=-PI/2, color="#1E88E5", fill_opacity=0.7, stroke_width=0)
        sector_half.move_to(pizza_left_center)
        self.objects["sector_half"] = sector_half

        # cut_line_vertical
        cut_line_vertical = Line(DOWN*2, UP*2, color=WHITE, stroke_width=3)
        cut_line_vertical.move_to(pizza_right_center)
        self.objects["cut_line_vertical"] = cut_line_vertical

        # cut_line_horizontal
        cut_line_horizontal = Line(LEFT*2, RIGHT*2, color=WHITE, stroke_width=3)
        cut_line_horizontal.move_to(pizza_right_center)
        self.objects["cut_line_horizontal"] = cut_line_horizontal

        # sector_quarter_1
        sector_quarter_1 = Sector(radius=2, angle=PI/2, start_angle=0, color="#64B5F6", fill_opacity=0.7, stroke_width=0)
        sector_quarter_1.move_to(pizza_right_center)
        self.objects["sector_quarter_1"] = sector_quarter_1

        # sector_quarter_2
        sector_quarter_2 = Sector(radius=2, angle=PI/2, start_angle=PI/2, color="#90CAF9", fill_opacity=0.7, stroke_width=0)
        sector_quarter_2.move_to(pizza_right_center)
        self.objects["sector_quarter_2"] = sector_quarter_2

        # equation_equiv
        equation_equiv = MathTex(r"\frac{1}{2} = \frac{2}{4}", color=YELLOW, font_size=48)
        equation_equiv.move_to(equation_anchor)
        self.objects["equation_equiv"] = equation_equiv

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        # narrative: "Let's start with two identical whole pizzas."
        # signal_action: null
        # visual_action: Create title
        self.play(FadeIn(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        # narrative: "We divide the first pizza into two equal halves."
        # signal_action: null
        # visual_action: Create pizza_left
        self.play(Create(self.objects["pizza_left"]), run_time=1.5)
        remaining_2 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        # narrative: "We color one of these halves to represent the fraction one-half."
        # signal_action: Indicate cut_line_half
        # visual_action: Create cut_line_half
        self.play(Indicate(self.objects["cut_line_half"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["cut_line_half"]), run_time=2.0)
        remaining_3 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        # narrative: "Now, let's label this pizza one-half."
        # signal_action: null
        # visual_action: Create sector_half
        self.play(FadeIn(self.objects["sector_half"]), run_time=2.0)
        remaining_4 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        # narrative: "We divide the second pizza into four equal quarters."
        # signal_action: null
        # visual_action: Write label_left
        self.play(Write(self.objects["label_left"]), run_time=1.5)
        remaining_5 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        # narrative: "We color two of these quarters to represent the fraction two-fourths."
        # signal_action: null
        # visual_action: Create pizza_right
        self.play(Create(self.objects["pizza_right"]), run_time=1.5)
        remaining_6 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        # narrative: "Notice that the colored area in both pizzas is exactly the same amount."
        # signal_action: Indicate cut_line_vertical
        # visual_action: Create cut_line_vertical
        self.play(Indicate(self.objects["cut_line_vertical"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["cut_line_vertical"]), run_time=1.5)
        remaining_7 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        # narrative: "This visual equality demonstrates the mathematical truth that one-half is equal to two-fourths."
        # signal_action: Indicate cut_line_horizontal
        # visual_action: Create cut_line_horizontal
        self.play(Indicate(self.objects["cut_line_horizontal"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["cut_line_horizontal"]), run_time=1.5)
        remaining_8 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        # ========== Step 9 ==========
        # narrative: "We can now write this equivalence as a mathematical equation."
        # signal_action: null
        # visual_action: Create sector_quarter_1
        self.play(FadeIn(self.objects["sector_quarter_1"]), run_time=1.5)
        remaining_9 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_9))

        # ========== Step 10 ==========
        # narrative: "The colored area in both pizzas is exactly the same amount."
        # signal_action: null
        # visual_action: Create sector_quarter_2
        self.play(FadeIn(self.objects["sector_quarter_2"]), run_time=1.5)
        remaining_10 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_10))

        # ========== Step 11 ==========
        # narrative: "This visual equality demonstrates the mathematical truth that one-half is equal to two-fourths."
        # signal_action: null
        # visual_action: Write label_right
        self.play(Write(self.objects["label_right"]), run_time=2.0)
        remaining_11 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_11))

        # ========== Step 12 ==========
        # narrative: "We can now write this equivalence as a mathematical equation."
        # signal_action: Circumscribe sectors
        # visual_action: Create equation_equiv
        colored_sectors = VGroup(
            self.objects["sector_half"],
            self.objects["sector_quarter_1"],
            self.objects["sector_quarter_2"]
        )
        self.play(Circumscribe(colored_sectors, color=YELLOW, run_time=1))
        self.play(Write(self.objects["equation_equiv"]), run_time=3.0)
        remaining_12 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_12))