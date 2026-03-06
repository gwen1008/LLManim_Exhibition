'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually demonstrate multiplication (3 × 4) as repeated addition and aggregation.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Visualizing Multiplication: 3 × 4"
#    - Main Content: [Center y=0] for star groups and final grid
#    - Footer Region: [Bottom y=-3.5] for step-by-step narrative text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for each star cluster. Position groups horizontally spaced. Final grid centered.
#    - Narrative text at bottom will be updated via ReplacementTransform to avoid stacking.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/The_animation_will_i_82fc713334/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create first group of 4 stars and label.
#    - Step 2: Duplicate to create second group, update label.
#    - Step 3: Duplicate to create third group, update label.
#    - Step 4: Morph three groups into a single 3x4 grid.
#    - Step 5: Write equation 3 × 4 = 12.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # Set dark background as per hint
        self.camera.background_color = "#1e1e1e"
        
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create title
        title = Text("Visualizing Multiplication: 3 × 4", font_size=48, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Create star prototype (will be used to build groups)
        star_prototype = Text("★", font_size=36, color=YELLOW)
        star_prototype.move_to(ORIGIN)
        self.objects["star_prototype"] = star_prototype
        
        # Create group1: 4 stars in a column
        group1_stars = VGroup(*[star_prototype.copy() for _ in range(4)])
        group1_stars.arrange(DOWN, buff=0.8)
        group1_stars.move_to(content_center + UP*1.0 + LEFT*3.5)
        self.objects["group1"] = group1_stars
        
        # Create label for group1
        label_group1 = MathTex(r"1 \mathrm{ group of } 4", font_size=30, color=GRAY_B)
        label_group1.next_to(group1_stars, DOWN, buff=0.5)
        self.objects["label_group1"] = label_group1
        
        # Create group2: 4 stars in a column (will be positioned later)
        group2_stars = VGroup(*[star_prototype.copy() for _ in range(4)])
        group2_stars.arrange(DOWN, buff=0.8)
        group2_stars.move_to(content_center + UP*1.0)
        self.objects["group2"] = group2_stars
        
        # Create label for group2
        label_group2 = MathTex(r"2 \mathrm{ groups of } 4", font_size=30, color=GRAY_B)
        label_group2.next_to(group2_stars, DOWN, buff=0.5)
        self.objects["label_group2"] = label_group2
        
        # Create group3: 4 stars in a column (will be positioned later)
        group3_stars = VGroup(*[star_prototype.copy() for _ in range(4)])
        group3_stars.arrange(DOWN, buff=0.8)
        group3_stars.move_to(content_center + UP*1.0 + RIGHT*3.5)
        self.objects["group3"] = group3_stars
        
        # Create label for group3
        label_group3 = MathTex(r"3 \mathrm{ groups of } 4", font_size=30, color=GRAY_B)
        label_group3.next_to(group3_stars, DOWN, buff=0.5)
        self.objects["label_group3"] = label_group3
        
        # Create final grid: 3x4 grid of stars
        final_grid_stars = VGroup()
        for row in range(3):
            for col in range(4):
                star = star_prototype.copy()
                star.move_to(content_center + RIGHT * (col - 1.5) * 1.2 + DOWN * (row - 1) * 0.8)
                final_grid_stars.add(star)
        self.objects["final_grid"] = final_grid_stars
        
        # Create equation
        equation = MathTex(r"3 \times 4 = 12", font_size=48, color=GREEN)
        equation.next_to(final_grid_stars, DOWN, buff=1.0)
        self.objects["equation"] = equation
        
        # Create step narrative text (initial placeholder)
        step_narrative = Text("We begin with one group.", font_size=32, color=GRAY_B)
        step_narrative.move_to(explanation_anchor)
        self.objects["step_narrative"] = step_narrative
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/The_animation_will_i_82fc713334/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        # Signal action: Indicate group1
        self.play(Indicate(self.objects["group1"], color=YELLOW, run_time=1))
        
        # Visual action: Create group1 and its label
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Create(self.objects["group1"]), Write(self.objects["label_group1"]), run_time=2.0)
        self.play(Write(self.objects["step_narrative"]), run_time=1.0)
        
        remaining_1 = max(0.1, 4.512 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/The_animation_will_i_82fc713334/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Update narrative text
        new_narrative2 = Text("Multiplication means having multiple equal groups. Let's add a second group of four.", 
                              font_size=32, color=GRAY_B)
        new_narrative2.move_to(explanation_anchor)
        
        # Signal action: Indicate group1
        self.play(Indicate(self.objects["group1"], color=YELLOW, run_time=1))
        
        # Visual action: TransformFromCopy group1 to group2, update label
        self.play(ReplacementTransform(self.objects["step_narrative"], new_narrative2), run_time=0.5)
        self.objects["step_narrative"] = new_narrative2
        
        self.play(TransformFromCopy(self.objects["group1"], self.objects["group2"]), run_time=1.5)
        self.play(ReplacementTransform(self.objects["label_group1"], self.objects["label_group2"]), run_time=1.0)
        
        remaining_2 = max(0.1, 5.856 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/The_animation_will_i_82fc713334/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Update narrative text
        new_narrative3 = Text("Now, we add the third and final group. We now have three separate groups, each containing four stars.", 
                              font_size=32, color=GRAY_B)
        new_narrative3.move_to(explanation_anchor)
        
        # Signal action: Indicate group2
        self.play(Indicate(self.objects["group2"], color=YELLOW, run_time=1))
        
        # Visual action: TransformFromCopy group2 to group3, update label
        self.play(ReplacementTransform(self.objects["step_narrative"], new_narrative3), run_time=0.5)
        self.objects["step_narrative"] = new_narrative3
        
        self.play(TransformFromCopy(self.objects["group2"], self.objects["group3"]), run_time=1.5)
        self.play(ReplacementTransform(self.objects["label_group2"], self.objects["label_group3"]), run_time=1.0)
        
        remaining_3 = max(0.1, 7.512 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/The_animation_will_i_82fc713334/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Update narrative text
        new_narrative4 = Text("To find the total, we combine all the stars into one collection.", 
                              font_size=32, color=GRAY_B)
        new_narrative4.move_to(explanation_anchor)
        
        # Signal action: Circumscribe label_group3
        self.play(Circumscribe(self.objects["label_group3"], color=WHITE, run_time=1))
        
        # Visual action: Morph groups into final grid
        self.play(ReplacementTransform(self.objects["step_narrative"], new_narrative4), run_time=0.5)
        self.objects["step_narrative"] = new_narrative4
        
        # Create transformation animations for each star
        star_transforms = []
        all_stars = VGroup(self.objects["group1"], self.objects["group2"], self.objects["group3"])
        grid_stars = self.objects["final_grid"]
        
        # Pair each star in the scattered groups with a star in the grid
        for i, star in enumerate(all_stars):
            for j, single_star in enumerate(star):
                idx = i * 4 + j
                if idx < len(grid_stars):
                    star_transforms.append(ReplacementTransform(single_star, grid_stars[idx]))
        
        self.play(*star_transforms, run_time=2.0)
        self.play(FadeOut(self.objects["label_group3"]), run_time=0.5)
        
        remaining_4 = max(0.1, 4.896 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/The_animation_will_i_82fc713334/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Update narrative text
        new_narrative5 = Text("Let's count them. One, two, three... twelve. Three groups of four stars gives us a total of twelve stars.", 
                              font_size=32, color=GRAY_B)
        new_narrative5.move_to(explanation_anchor)
        
        # Signal action: Indicate final_grid
        self.play(Indicate(self.objects["final_grid"], color=GREEN, run_time=1))
        
        # Visual action: Write equation
        self.play(ReplacementTransform(self.objects["step_narrative"], new_narrative5), run_time=0.5)
        self.objects["step_narrative"] = new_narrative5
        
        self.play(Write(self.objects["equation"]), run_time=2.0)
        
        remaining_5 = max(0.1, 7.992 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final pause
        self.wait(max(0.1, 2))