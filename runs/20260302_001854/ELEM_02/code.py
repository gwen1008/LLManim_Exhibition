'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing multiplication as repeated addition and grouping, showing 3 groups of 4 equals 12.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and final equation
#    - Main Content: [Center y=0] for star groups and final grid
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Position three groups horizontally spaced during construction phase.
#    - Use VGroups to manage each set of stars and labels.
#    - Final grid will occupy the center, groups will transform into it.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/To_visualize_the_con_242ac4f280/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create first blue star group.
#    - Step 2: Label first group, create second green group.
#    - Step 3: Update label to "2 groups", create third red group.
#    - Step 4: Update label to "3 groups", transform three groups into final 3x4 white grid.
#    - Step 5: Write final equation and indicate it.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on layout zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Horizontal positions for the three groups during construction
        group1_pos = content_center + 3.5 * LEFT
        group2_pos = content_center
        group3_pos = content_center + 3.5 * RIGHT
        
        # Create title_text
        title_text = Text("Visualizing Multiplication: 3 × 4", color=WHITE, font_size=48)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text
        
        # Create final_equation (will be added later)
        final_equation = MathTex(r"3 \times 4 = 12", color=YELLOW, font_size=40)
        final_equation.next_to(title_text, DOWN, buff=0.5)
        self.objects["final_equation"] = final_equation
        
        # Create star groups (each with 4 stars in 2x2 arrangement)
        # Group 1 - Blue
        stars1 = VGroup(*[Star(color="#3498db", fill_opacity=0.8) for _ in range(4)])
        stars1.arrange_in_grid(rows=2, cols=2, buff=0.3)
        stars1.move_to(group1_pos)
        self.objects["group1"] = stars1
        
        # Group 2 - Green
        stars2 = VGroup(*[Star(color="#2ecc71", fill_opacity=0.8) for _ in range(4)])
        stars2.arrange_in_grid(rows=2, cols=2, buff=0.3)
        stars2.move_to(group2_pos)
        self.objects["group2"] = stars2
        
        # Group 3 - Red
        stars3 = VGroup(*[Star(color="#e74c3c", fill_opacity=0.8) for _ in range(4)])
        stars3.arrange_in_grid(rows=2, cols=2, buff=0.3)
        stars3.move_to(group3_pos)
        self.objects["group3"] = stars3
        
        # Create labels for groups
        label_group1 = Text("1 group of 4", color="#3498db", font_size=30)
        label_group1.next_to(stars1, DOWN, buff=0.5)
        self.objects["label_group1"] = label_group1
        
        label_group2 = Text("2 groups of 4", color="#2ecc71", font_size=30)
        label_group2.next_to(stars2, DOWN, buff=0.5)
        self.objects["label_group2"] = label_group2
        
        label_group3 = Text("3 groups of 4", color="#e74c3c", font_size=30)
        label_group3.next_to(stars3, DOWN, buff=0.5)
        self.objects["label_group3"] = label_group3
        
        # Create final grid (3x4 arrangement of white stars)
        final_stars = VGroup(*[Star(color=WHITE, fill_opacity=0.8) for _ in range(12)])
        final_stars.arrange_in_grid(rows=3, cols=4, buff=0.3)
        final_stars.move_to(content_center)
        self.objects["final_grid"] = final_stars
        
        # Create step explanation text
        step_explanation = Text("We start by building our first group.", color=GRAY_C, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/To_visualize_the_con_242ac4f280/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        # Update explanation text for step 1
        new_explanation1 = Text("We start by building our first group.", color=GRAY_C, font_size=28)
        new_explanation1.move_to(explanation_anchor)
        
        self.play(
            Write(self.objects["title_text"]),
            ReplacementTransform(self.objects["step_explanation"], new_explanation1)
        )
        self.objects["step_explanation"] = new_explanation1
        
        self.play(Create(self.objects["group1"]), run_time=2.0)
        remaining_1 = max(0.1, 6.264 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/To_visualize_the_con_242ac4f280/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Signal action: Write label_group1
        self.play(Write(self.objects["label_group1"]), run_time=1.0)
        
        # Update explanation text for step 2
        new_explanation2 = Text("This is one group of four. Now, let's add a second identical group.", color=GRAY_C, font_size=28)
        new_explanation2.move_to(explanation_anchor)
        
        self.play(
            ReplacementTransform(self.objects["step_explanation"], new_explanation2),
            run_time=1.0
        )
        self.objects["step_explanation"] = new_explanation2
        
        self.play(Create(self.objects["group2"]), run_time=2.0)
        remaining_2 = max(0.1, 4.728 - 2.0 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/To_visualize_the_con_242ac4f280/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: ReplacementTransform label_group1 to label_group2
        self.play(ReplacementTransform(self.objects["label_group1"], self.objects["label_group2"]), run_time=1.0)
        
        # Update explanation text for step 3
        new_explanation3 = Text("Now we have two groups of four. Let's add our third and final group.", color=GRAY_C, font_size=28)
        new_explanation3.move_to(explanation_anchor)
        
        self.play(
            ReplacementTransform(self.objects["step_explanation"], new_explanation3),
            run_time=1.0
        )
        self.objects["step_explanation"] = new_explanation3
        
        self.play(Create(self.objects["group3"]), run_time=2.0)
        remaining_3 = max(0.1, 4.536 - 2.0 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/To_visualize_the_con_242ac4f280/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Signal action: ReplacementTransform label_group2 to label_group3
        self.play(ReplacementTransform(self.objects["label_group2"], self.objects["label_group3"]), run_time=1.0)
        
        # Update explanation text for step 4
        new_explanation4 = Text("We now have three separate groups. Multiplication means combining these groups.", color=GRAY_C, font_size=28)
        new_explanation4.move_to(explanation_anchor)
        
        self.play(
            ReplacementTransform(self.objects["step_explanation"], new_explanation4),
            run_time=1.0
        )
        self.objects["step_explanation"] = new_explanation4
        
        # Visual action: Transform three groups into final grid
        # Create a temporary VGroup containing all three groups for transformation
        all_groups = VGroup(self.objects["group1"], self.objects["group2"], self.objects["group3"])
        
        self.play(Transform(all_groups, self.objects["final_grid"]), run_time=4.0)
        
        # Remove the temporary transformed groups and add the final grid
        self.remove(all_groups)
        self.add(self.objects["final_grid"])
        
        remaining_4 = max(0.1, 10.512 - 4.0 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/To_visualize_the_con_242ac4f280/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Update explanation text for step 5
        new_explanation5 = Text("The array shows three rows of four, making twelve stars total.", color=GRAY_C, font_size=28)
        new_explanation5.move_to(explanation_anchor)
        
        self.play(
            ReplacementTransform(self.objects["step_explanation"], new_explanation5),
            run_time=1.0
        )
        self.objects["step_explanation"] = new_explanation5
        
        # Visual action: Write final equation
        self.play(Write(self.objects["final_equation"]), run_time=2.0)
        
        # Signal action: Indicate final equation
        self.play(Indicate(self.objects["final_equation"], color=YELLOW, run_time=1.0))
        
        remaining_5 = max(0.1, 8.52 - 2.0 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))