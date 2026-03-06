'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually demonstrate that 3 × 4 means "3 groups of 4", linking repeated addition to multiplication.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "3 × 4 = ?"
#    - Main Content: [Center y=0] for three group containers and stars.
#    - Footer Region: [Bottom y=-3.5] for explanation text and final equation.
# 3. Anti-Overlap Check:
#    - Strategy: Place three containers in a horizontal row with sufficient spacing (LEFT*3.5, 0, RIGHT*3.5). Use VGroups for each container+stars.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step?
# 5. Animation Flow:
#    - Step 1: Show title.
#    - Step 2: Show three empty group containers.
#    - Step 3: Show counter (label and number 0).
#    - Steps 4-6: Fill each group with 4 stars, incrementing counter after each star.
#    - Step 7: Highlight counter, fade out containers.
#    - Step 8: Transform bottom text into final equation.
#    - Step 9: Indicate final equation and hold.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/The_animation_will_i_a7ef4644eb/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Object Registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # title
        title = MathTex(r"3 \times 4 = ?", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # group containers
        group1_container = Rectangle(width=2, height=1.5, color="#1E90FF", fill_opacity=0.2, stroke_width=2)
        group1_container.move_to(content_center + 3.5 * LEFT)
        self.objects["group1_container"] = group1_container

        group2_container = Rectangle(width=2, height=1.5, color="#1E90FF", fill_opacity=0.2, stroke_width=2)
        group2_container.move_to(content_center)
        self.objects["group2_container"] = group2_container

        group3_container = Rectangle(width=2, height=1.5, color="#1E90FF", fill_opacity=0.2, stroke_width=2)
        group3_container.move_to(content_center + 3.5 * RIGHT)
        self.objects["group3_container"] = group3_container

        # counter label and number
        counter_label = Text("Total:", color=YELLOW)
        counter_label.move_to(content_center + 2.0 * UP + 1.5 * LEFT)
        self.objects["counter_label"] = counter_label

        counter_number = DecimalNumber(0, color=YELLOW, num_decimal_places=0)
        counter_number.next_to(counter_label, RIGHT, buff=0.3)
        self.objects["counter_number"] = counter_number

        # explanation text and final equation (will be transformed)
        explanation_text = Text("3 groups, each will have 4 stars.", color=GRAY_C, font_size=32)
        explanation_text.move_to(footer_anchor)
        self.objects["explanation_text"] = explanation_text

        final_equation = MathTex(r"3 \times 4 = 12", color=GREEN, font_size=40)
        final_equation.move_to(footer_anchor)
        self.objects["final_equation"] = final_equation

        # We will create stars dynamically during steps 4-6.
        # Store star groups for later reference.
        self.star_groups = {}
        self.all_stars = VGroup()

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        # narrative: "We want to understand what three times four means. Let's start by showing three distinct groups."
        # signal_action: null
        # visual_action: Create title
        self.play(Write(title), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        # narrative: "Here are our three groups, represented by these containers."
        # signal_action: null
        # visual_action: Create three rectangles simultaneously
        self.play(
            Create(group1_container),
            Create(group2_container),
            Create(group3_container),
            run_time=2.0
        )
        remaining_2 = max(0.1, 2.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        # narrative: "We'll also set up a counter to track the total number of items. It starts at zero."
        # signal_action: Indicate counter_number
        # visual_action: Write counter_label and counter_number
        self.play(Indicate(counter_number, color=YELLOW, run_time=1))
        self.play(
            Write(counter_label),
            Write(counter_number),
            run_time=1.5
        )
        remaining_3 = max(0.1, 2.5 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        # narrative: "Now, let's fill the first group. Three times four means we put four stars into the first group."
        # signal_action: Indicate group1_container
        # visual_action: Create four stars inside group1_container, increment counter after each.
        self.play(Indicate(group1_container, color=ORANGE, run_time=1))
        # Create stars for group 1 in a 2x2 grid inside the container
        stars_g1 = VGroup()
        star_positions_g1 = [
            group1_container.get_center() + 0.5 * LEFT + 0.5 * UP,
            group1_container.get_center() + 0.5 * RIGHT + 0.5 * UP,
            group1_container.get_center() + 0.5 * LEFT + 0.5 * DOWN,
            group1_container.get_center() + 0.5 * RIGHT + 0.5 * DOWN,
        ]
        for i, pos in enumerate(star_positions_g1):
            star = Star(color=YELLOW, outer_radius=0.2, density=2)
            star.move_to(pos)
            stars_g1.add(star)
            self.play(Create(star), run_time=0.5)
            # Increment counter
            new_value = i + 1
            self.play(
                ChangeDecimalToValue(counter_number, new_value),
                run_time=0.5
            )
        self.star_groups["group1"] = stars_g1
        self.all_stars.add(*stars_g1)
        remaining_4 = max(0.1, 5.0 - (1 + 4*0.5 + 4*0.5) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        # narrative: "Next, we fill the second group with another four stars."
        # signal_action: Indicate group2_container
        # visual_action: Create four stars inside group2_container, incrementing counter (from 4 to 8).
        self.play(Indicate(group2_container, color=ORANGE, run_time=1))
        stars_g2 = VGroup()
        star_positions_g2 = [
            group2_container.get_center() + 0.5 * LEFT + 0.5 * UP,
            group2_container.get_center() + 0.5 * RIGHT + 0.5 * UP,
            group2_container.get_center() + 0.5 * LEFT + 0.5 * DOWN,
            group2_container.get_center() + 0.5 * RIGHT + 0.5 * DOWN,
        ]
        for i, pos in enumerate(star_positions_g2):
            star = Star(color=YELLOW, outer_radius=0.2, density=2)
            star.move_to(pos)
            stars_g2.add(star)
            self.play(Create(star), run_time=0.5)
            new_value = 4 + i + 1
            self.play(
                ChangeDecimalToValue(counter_number, new_value),
                run_time=0.5
            )
        self.star_groups["group2"] = stars_g2
        self.all_stars.add(*stars_g2)
        remaining_5 = max(0.1, 4.0 - (1 + 4*0.5 + 4*0.5) + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        # narrative: "Finally, we fill the third group with the last four stars."
        # signal_action: Indicate group3_container
        # visual_action: Create four stars inside group3_container, incrementing counter (from 8 to 12).
        self.play(Indicate(group3_container, color=ORANGE, run_time=1))
        stars_g3 = VGroup()
        star_positions_g3 = [
            group3_container.get_center() + 0.5 * LEFT + 0.5 * UP,
            group3_container.get_center() + 0.5 * RIGHT + 0.5 * UP,
            group3_container.get_center() + 0.5 * LEFT + 0.5 * DOWN,
            group3_container.get_center() + 0.5 * RIGHT + 0.5 * DOWN,
        ]
        for i, pos in enumerate(star_positions_g3):
            star = Star(color=YELLOW, outer_radius=0.2, density=2)
            star.move_to(pos)
            stars_g3.add(star)
            self.play(Create(star), run_time=0.5)
            new_value = 8 + i + 1
            self.play(
                ChangeDecimalToValue(counter_number, new_value),
                run_time=0.5
            )
        self.star_groups["group3"] = stars_g3
        self.all_stars.add(*stars_g3)
        remaining_6 = max(0.1, 4.0 - (1 + 4*0.5 + 4*0.5) + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        # narrative: "Look at the counter. We have placed twelve stars in total. Now, let's combine the groups to see the total clearly."
        # signal_action: Circumscribe counter_number
        # visual_action: Fade out the rectangle containers
        self.play(Circumscribe(counter_number, color=GREEN, run_time=1))
        self.play(
            FadeOut(group1_container),
            FadeOut(group2_container),
            FadeOut(group3_container),
            run_time=1.5
        )
        remaining_7 = max(0.1, 3.0 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        # narrative: "The twelve stars together show the result of our multiplication."
        # signal_action: null
        # visual_action: ReplacementTransform explanation_text into final_equation
        self.play(
            ReplacementTransform(explanation_text, final_equation),
            run_time=2.0
        )
        remaining_8 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # ========== Step 9 ==========
        # narrative: "Therefore, three groups of four equals twelve. Three times four is twelve."
        # signal_action: Indicate final_equation
        # visual_action: Wait
        self.play(Indicate(final_equation, color=GREEN, run_time=1))
        remaining_9 = max(0.1, 3.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_9))