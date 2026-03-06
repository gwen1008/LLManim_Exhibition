'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing multiplication as repeated addition/groups, specifically 3 groups of 4 equals 12.
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for star groups and final grid
#    - Footer Region: [Bottom y=-3.5] for final equation
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Use VGroups for each cluster and the final grid. Position groups horizontally spaced, then morph into centered grid.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/3x4_groups_of_four/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
#    Step 1: Create single star prototype.
#    Step 2: Indicate star, then create first group of 4 around it.
#    Step 3: Circumscribe first group, then duplicate to create two more groups.
#    Step 4: Morph three groups into a single 3x4 grid.
#    Step 5: Indicate grid, then write final equation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/The_animation_will_i_63401df0be/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        equation_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create title
        title = Text("3 × 4: Groups of Four", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Create star prototype (off-screen initially, will be moved into position)
        star_prototype = Star(n=5, outer_radius=0.2, color=YELLOW, fill_opacity=0.8)
        star_prototype.move_to(content_center + 4 * LEFT)  # Start off-screen left
        self.objects["star_prototype"] = star_prototype

        # Create first group of 4 stars (arranged in 2x2)
        group1_stars = []
        for i in range(2):
            for j in range(2):
                star = Star(n=5, outer_radius=0.2, color=YELLOW, fill_opacity=0.8)
                star.move_to(content_center + LEFT * 3 + RIGHT * i * 0.6 + UP * j * 0.6)
                group1_stars.append(star)
        group1 = VGroup(*group1_stars)
        self.objects["group1"] = group1

        # Create second group (identical arrangement, different position)
        group2_stars = []
        for i in range(2):
            for j in range(2):
                star = Star(n=5, outer_radius=0.2, color=YELLOW, fill_opacity=0.8)
                star.move_to(content_center + RIGHT * i * 0.6 + UP * j * 0.6)
                group2_stars.append(star)
        group2 = VGroup(*group2_stars)
        self.objects["group2"] = group2

        # Create third group
        group3_stars = []
        for i in range(2):
            for j in range(2):
                star = Star(n=5, outer_radius=0.2, color=YELLOW, fill_opacity=0.8)
                star.move_to(content_center + RIGHT * 3 + RIGHT * i * 0.6 + UP * j * 0.6)
                group3_stars.append(star)
        group3 = VGroup(*group3_stars)
        self.objects["group3"] = group3

        # Create all stars grid (3x4 arrangement)
        all_stars_list = []
        for row in range(3):
            for col in range(4):
                star = Star(n=5, outer_radius=0.2, color=YELLOW, fill_opacity=0.8)
                all_stars_list.append(star)
        all_stars_grid = VGroup(*all_stars_list)
        all_stars_grid.arrange_in_grid(rows=3, cols=4, buff=0.6)
        all_stars_grid.move_to(content_center)
        self.objects["all_stars_grid"] = all_stars_grid

        # Create final equation
        equation = MathTex(r"3 \times 4 = 12", color=GREEN, font_size=48)
        equation.move_to(equation_anchor)
        self.objects["equation"] = equation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/3x4_groups_of_four/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # Move prototype to center and create it
        star_prototype.move_to(content_center)
        self.play(Create(star_prototype), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/3x4_groups_of_four/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Indicate prototype
        self.play(Indicate(star_prototype, color=YELLOW, run_time=1))
        # Visual action: Create first group (including the prototype)
        # We'll fade out the single star and create the group in its place
        self.play(FadeOut(star_prototype), run_time=0.5)
        self.play(Create(group1), run_time=2.0)
        remaining_2 = max(0.1, 3.0 - (1 + 0.5 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/3x4_groups_of_four/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Circumscribe group1
        self.play(Circumscribe(group1, color=BLUE, run_time=1))
        # Visual action: Transform to create groups 2 and 3
        # We'll create copies of group1 and position them
        group2_copy = group1.copy()
        group2_copy.move_to(content_center)
        group3_copy = group1.copy()
        group3_copy.move_to(content_center + RIGHT * 3)
        
        self.play(
            Transform(group1.copy(), group2),
            Transform(group1.copy(), group3),
            run_time=2.0
        )
        remaining_3 = max(0.1, 3.0 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/3x4_groups_of_four/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # No signal action
        # Visual action: ReplacementTransform groups into grid
        # We need to create temporary copies for transformation
        temp_group1 = group1.copy()
        temp_group2 = group2.copy()
        temp_group3 = group3.copy()
        
        self.play(
            ReplacementTransform(temp_group1, all_stars_grid[0:4]),
            ReplacementTransform(temp_group2, all_stars_grid[4:8]),
            ReplacementTransform(temp_group3, all_stars_grid[8:12]),
            run_time=2.5
        )
        # Remove original groups (they're replaced by grid)
        self.remove(group1, group2, group3)
        self.add(all_stars_grid)
        remaining_4 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/3x4_groups_of_four/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Indicate grid
        self.play(Indicate(all_stars_grid, color=YELLOW, run_time=1))
        # Visual action: Write equation
        self.play(Write(equation), run_time=2.0)
        remaining_5 = max(0.1, 4.0 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))