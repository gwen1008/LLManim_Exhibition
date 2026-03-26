from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors based on layout_plan
        title_anchor = 3.5 * UP
        global_center = ORIGIN
        group1_anchor = 3 * LEFT
        group2_anchor = 3 * RIGHT
        group3_anchor = 2.5 * DOWN
        footer_anchor = 3.2 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # Title
        title = Text("Visualizing Multiplication: 3 × 4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Create individual stars and groups
        # Red Group
        star_red_1 = Star(outer_radius=0.4, inner_radius=0.2, color="#E74C3C", fill_opacity=0.8)
        star_red_1.move_to(group1_anchor + LEFT*0.6 + UP*0.6)
        self.objects["star_red_1"] = star_red_1

        star_red_2 = Star(outer_radius=0.4, inner_radius=0.2, color="#E74C3C", fill_opacity=0.8)
        star_red_2.move_to(group1_anchor + RIGHT*0.6 + UP*0.6)
        self.objects["star_red_2"] = star_red_2

        star_red_3 = Star(outer_radius=0.4, inner_radius=0.2, color="#E74C3C", fill_opacity=0.8)
        star_red_3.move_to(group1_anchor + LEFT*0.6 + DOWN*0.6)
        self.objects["star_red_3"] = star_red_3

        star_red_4 = Star(outer_radius=0.4, inner_radius=0.2, color="#E74C3C", fill_opacity=0.8)
        star_red_4.move_to(group1_anchor + RIGHT*0.6 + DOWN*0.6)
        self.objects["star_red_4"] = star_red_4

        group_red = VGroup(star_red_1, star_red_2, star_red_3, star_red_4)
        group_red.move_to(group1_anchor)
        self.objects["group_red"] = group_red

        # Green Group
        star_green_1 = Star(outer_radius=0.4, inner_radius=0.2, color="#2ECC71", fill_opacity=0.8)
        star_green_1.move_to(group2_anchor + LEFT*0.6 + UP*0.6)
        self.objects["star_green_1"] = star_green_1

        star_green_2 = Star(outer_radius=0.4, inner_radius=0.2, color="#2ECC71", fill_opacity=0.8)
        star_green_2.move_to(group2_anchor + RIGHT*0.6 + UP*0.6)
        self.objects["star_green_2"] = star_green_2

        star_green_3 = Star(outer_radius=0.4, inner_radius=0.2, color="#2ECC71", fill_opacity=0.8)
        star_green_3.move_to(group2_anchor + LEFT*0.6 + DOWN*0.6)
        self.objects["star_green_3"] = star_green_3

        star_green_4 = Star(outer_radius=0.4, inner_radius=0.2, color="#2ECC71", fill_opacity=0.8)
        star_green_4.move_to(group2_anchor + RIGHT*0.6 + DOWN*0.6)
        self.objects["star_green_4"] = star_green_4

        group_green = VGroup(star_green_1, star_green_2, star_green_3, star_green_4)
        group_green.move_to(group2_anchor)
        self.objects["group_green"] = group_green

        # Blue Group
        star_blue_1 = Star(outer_radius=0.4, inner_radius=0.2, color="#3498DB", fill_opacity=0.8)
        star_blue_1.move_to(group3_anchor + LEFT*0.6 + UP*0.6)
        self.objects["star_blue_1"] = star_blue_1

        star_blue_2 = Star(outer_radius=0.4, inner_radius=0.2, color="#3498DB", fill_opacity=0.8)
        star_blue_2.move_to(group3_anchor + RIGHT*0.6 + UP*0.6)
        self.objects["star_blue_2"] = star_blue_2

        star_blue_3 = Star(outer_radius=0.4, inner_radius=0.2, color="#3498DB", fill_opacity=0.8)
        star_blue_3.move_to(group3_anchor + LEFT*0.6 + DOWN*0.6)
        self.objects["star_blue_3"] = star_blue_3

        star_blue_4 = Star(outer_radius=0.4, inner_radius=0.2, color="#3498DB", fill_opacity=0.8)
        star_blue_4.move_to(group3_anchor + RIGHT*0.6 + DOWN*0.6)
        self.objects["star_blue_4"] = star_blue_4

        group_blue = VGroup(star_blue_1, star_blue_2, star_blue_3, star_blue_4)
        group_blue.move_to(group3_anchor)
        self.objects["group_blue"] = group_blue

        # Labels
        label_multiplier = Tex(r"3 groups", color=YELLOW, font_size=36)
        label_multiplier.move_to(footer_anchor + LEFT*2)
        self.objects["label_multiplier"] = label_multiplier

        label_multiplicand = Tex(r"4 in each", color=YELLOW, font_size=36)
        label_multiplicand.move_to(footer_anchor)
        self.objects["label_multiplicand"] = label_multiplicand

        label_product = Tex(r"12 total", color=YELLOW, font_size=36)
        label_product.move_to(footer_anchor + RIGHT*2)
        self.objects["label_product"] = label_product

        # Final equation
        final_equation = MathTex(r"3 \times 4 = 12", color=WHITE, font_size=60)
        final_equation.move_to(global_center + DOWN*2.5)
        self.objects["final_equation"] = final_equation

        # Empty VGroup for the final grid (will be populated later)
        all_stars_grid = VGroup()
        all_stars_grid.move_to(global_center)
        self.objects["all_stars_grid"] = all_stars_grid

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        # [missing audio] self.add_sound("media/audio/Specification___1__S_7bf68ffc42/step_01.mp3")
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        # [missing audio] self.add_sound("media/audio/Specification___1__S_7bf68ffc42/step_02.mp3")
        self.play(Circumscribe(self.objects["group_red"], color="#E74C3C", run_time=1))
        self.play(Create(self.objects["group_red"]), run_time=2.0)
        remaining_2 = max(0.1, 3.0 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        # [missing audio] self.add_sound("media/audio/Specification___1__S_7bf68ffc42/step_03.mp3")
        self.play(Circumscribe(self.objects["group_green"], color="#2ECC71", run_time=1))
        self.play(Create(self.objects["group_green"]), run_time=2.0)
        remaining_3 = max(0.1, 3.0 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        # [missing audio] self.add_sound("media/audio/Specification___1__S_7bf68ffc42/step_04.mp3")
        self.play(Circumscribe(self.objects["group_blue"], color="#3498DB", run_time=1))
        self.play(Create(self.objects["group_blue"]), run_time=2.0)
        remaining_4 = max(0.1, 3.0 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        # [missing audio] self.add_sound("media/audio/Specification___1__S_7bf68ffc42/step_05.mp3")
        # Move red group to left side of center
        target_pos_red = global_center + LEFT * 2.5
        self.play(self.objects["group_red"].animate.move_to(target_pos_red), run_time=2.0)
        remaining_5 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        # [missing audio] self.add_sound("media/audio/Specification___1__S_7bf68ffc42/step_06.mp3")
        # Move green group to center
        target_pos_green = global_center
        self.play(self.objects["group_green"].animate.move_to(target_pos_green), run_time=2.0)
        remaining_6 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        # [missing audio] self.add_sound("media/audio/Specification___1__S_7bf68ffc42/step_07.mp3")
        # Move blue group to right side of center
        target_pos_blue = global_center + RIGHT * 2.5
        self.play(self.objects["group_blue"].animate.move_to(target_pos_blue), run_time=2.0)
        remaining_7 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        # [missing audio] self.add_sound("media/audio/Specification___1__S_7bf68ffc42/step_08.mp3")
        # Create the final grid of 12 stars (uniform color GOLD)
        # We'll create a new VGroup with all stars arranged in a 3x4 grid
        all_stars_list = []
        for star in self.objects["group_red"]:
            new_star = Star(outer_radius=0.4, inner_radius=0.2, color=GOLD, fill_opacity=0.8)
            all_stars_list.append(new_star)
        for star in self.objects["group_green"]:
            new_star = Star(outer_radius=0.4, inner_radius=0.2, color=GOLD, fill_opacity=0.8)
            all_stars_list.append(new_star)
        for star in self.objects["group_blue"]:
            new_star = Star(outer_radius=0.4, inner_radius=0.2, color=GOLD, fill_opacity=0.8)
            all_stars_list.append(new_star)

        final_grid = VGroup(*all_stars_list)
        final_grid.arrange_in_grid(rows=3, cols=4, buff=0.5)
        final_grid.move_to(global_center)

        # Replace the empty VGroup with the new grid for reference
        self.objects["all_stars_grid"] = final_grid

        self.play(Indicate(final_grid, color=YELLOW, run_time=1))
        # Animate the transformation from separate groups to the grid
        self.play(
            ReplacementTransform(self.objects["group_red"], final_grid[:4]),
            ReplacementTransform(self.objects["group_green"], final_grid[4:8]),
            ReplacementTransform(self.objects["group_blue"], final_grid[8:]),
            run_time=4.0
        )
        remaining_8 = max(0.1, 6.0 - (1 + 4.0) + 0.5)
        self.wait(max(0.1, remaining_8))

        # ========== Step 9 ==========
        # [missing audio] self.add_sound("media/audio/Specification___1__S_7bf68ffc42/step_09.mp3")
        self.play(Write(self.objects["final_equation"]), run_time=2.0)
        remaining_9 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))