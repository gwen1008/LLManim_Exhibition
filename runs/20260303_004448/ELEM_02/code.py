'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing multiplication 3×4 as repeated addition (three groups of four) and as a rectangular area (3 rows by 4 columns).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and Equation
#    - Main Content: [Center y=0] for star groups and final grid
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for star clusters and final grid. Position groups horizontally spaced, then transform to centered grid.
#    - Ensure explanation text stays in footer zone.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/understanding_multiplication_3x4/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show title.
#    - Step 2: Show equation and three groups of four stars.
#    - Step 3: Signal first group, update explanation.
#    - Step 4: Transform groups into a 3x4 grid.
#    - Step 5: Signal grid, update explanation, morph equation to show answer 12.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        cluster_anchor = ORIGIN
        grid_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create title_text
        title_text = Text("Understanding Multiplication: 3 × 4", color=WHITE, font_size=36)
        title_text.move_to(title_anchor + DOWN*0.5)
        self.objects["title_text"] = title_text
        
        # Create equation
        equation = MathTex(r"3 \times 4 = ?", color=YELLOW, font_size=40)
        equation.next_to(title_text, DOWN, buff=0.5)
        self.objects["equation"] = equation
        
        # Create star template (not shown directly)
        star_template = Star(outer_radius=0.3, density=2, color="#FFD700", fill_opacity=0.8, stroke_width=2)
        star_template.move_to(ORIGIN)
        
        # Helper function to create a 2x2 grid of stars
        def create_star_group(color):
            stars = VGroup(*[star_template.copy().set_color(color) for _ in range(4)])
            stars.arrange_in_grid(rows=2, cols=2, buff=0.3)
            return stars
        
        # Create group1, group2, group3
        group1 = create_star_group("#FF6B6B")
        group1.move_to(cluster_anchor + LEFT*3)
        self.objects["group1"] = group1
        
        group2 = create_star_group("#4ECDC4")
        group2.move_to(cluster_anchor)
        self.objects["group2"] = group2
        
        group3 = create_star_group("#95E1D3")
        group3.move_to(cluster_anchor + RIGHT*3)
        self.objects["group3"] = group3
        
        # Create all_stars_vgroup (container for all stars)
        all_stars_vgroup = VGroup(group1.copy(), group2.copy(), group3.copy())
        all_stars_vgroup.move_to(grid_anchor)
        self.objects["all_stars_vgroup"] = all_stars_vgroup
        
        # Create final_grid (3x4 arrangement)
        final_grid_stars = VGroup(*[star_template.copy().set_color("#FFD700") for _ in range(12)])
        final_grid_stars.arrange_in_grid(rows=3, cols=4, buff=0.5)
        final_grid_stars.move_to(grid_anchor)
        self.objects["final_grid"] = final_grid_stars
        
        # Create explanation_text
        explanation_text = Text("", color=GRAY_C, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        audio_step1 = "media/audio/understanding_multiplication_3x4/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title_text"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # Step 2
        audio_step2 = "media/audio/understanding_multiplication_3x4/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Update explanation text for step 2
        explanation_step2 = Text("Step 1: Three groups, each with four stars.", color=GRAY_C, font_size=24)
        explanation_step2.move_to(explanation_anchor)
        
        self.play(
            Write(self.objects["equation"]),
            Create(self.objects["group1"]),
            Create(self.objects["group2"]),
            Create(self.objects["group3"]),
            Transform(self.objects["explanation_text"], explanation_step2),
            run_time=3.5
        )
        remaining_2 = max(0.1, 5.0 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # Step 3
        audio_step3 = "media/audio/understanding_multiplication_3x4/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe group1
        self.play(Circumscribe(self.objects["group1"], color=YELLOW, run_time=1))
        
        # Update explanation text for step 3
        explanation_step3 = Text("Step 2: Combine all stars into one collection.", color=GRAY_C, font_size=24)
        explanation_step3.move_to(explanation_anchor)
        
        self.play(Transform(self.objects["explanation_text"], explanation_step3), run_time=1.5)
        remaining_3 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # Step 4
        audio_step4 = "media/audio/understanding_multiplication_3x4/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Transform the three groups into the final grid
        # We'll create a temporary VGroup containing all stars from the three groups
        all_stars_temp = VGroup(
            self.objects["group1"].copy(),
            self.objects["group2"].copy(),
            self.objects["group3"].copy()
        )
        all_stars_temp.move_to(grid_anchor)
        
        # Animate the original groups moving to center and becoming the final grid
        self.play(
            Transform(self.objects["group1"], self.objects["final_grid"][0:4]),
            Transform(self.objects["group2"], self.objects["final_grid"][4:8]),
            Transform(self.objects["group3"], self.objects["final_grid"][8:12]),
            run_time=3.5
        )
        remaining_4 = max(0.1, 4.0 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # Step 5
        audio_step5 = "media/audio/understanding_multiplication_3x4/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Indicate final_grid
        self.play(Indicate(self.objects["final_grid"], color=GREEN, run_time=1))
        
        # Update explanation text for step 5
        explanation_step5 = Text("Step 3: The array has 3 rows and 4 columns, making 12 stars total.", color=GRAY_C, font_size=24)
        explanation_step5.move_to(explanation_anchor)
        
        # Transform equation to show answer
        equation_final = MathTex(r"3 \times 4 = 12", color=YELLOW, font_size=40)
        equation_final.move_to(self.objects["equation"].get_center())
        
        self.play(
            Transform(self.objects["explanation_text"], explanation_step5),
            TransformMatchingTex(self.objects["equation"], equation_final),
            run_time=3.0
        )
        remaining_5 = max(0.1, 5.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))