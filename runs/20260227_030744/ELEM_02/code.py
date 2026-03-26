from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors from layout_plan
        title_anchor = np.array([0, 3.0, 0])  # Fixed: Changed from 3.5 to 3.0
        content_center = np.array([0, 0.5, 0])
        equation_anchor = np.array([0, -2.5, 0])
        group_left_pos = np.array([-3.5, 0.5, 0])
        group_center_pos = np.array([0, 0.5, 0])
        group_right_pos = np.array([3.5, 0.5, 0])
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Multiplication: 3 × 4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # group containers (initially empty VGroups)
        group1_container = VGroup()
        group1_container.move_to(group_left_pos)
        self.objects["group1_container"] = group1_container
        
        group2_container = VGroup()
        group2_container.move_to(group_center_pos)
        self.objects["group2_container"] = group2_container
        
        group3_container = VGroup()
        group3_container.move_to(group_right_pos)
        self.objects["group3_container"] = group3_container
        
        # group labels
        group1_label = Text("Group 1", color=BLUE, font_size=24)
        group1_label.next_to(group1_container, DOWN, buff=0.3)
        self.objects["group1_label"] = group1_label
        
        group2_label = Text("Group 2", color=GREEN, font_size=24)
        group2_label.next_to(group2_container, DOWN, buff=0.3)
        self.objects["group2_label"] = group2_label
        
        group3_label = Text("Group 3", color=YELLOW, font_size=24)
        group3_label.next_to(group3_container, DOWN, buff=0.3)
        self.objects["group3_label"] = group3_label
        
        # final equation
        final_equation = MathTex(r"3 \times 4 = 12", color=WHITE, font_size=42)
        final_equation.move_to(equation_anchor)
        self.objects["final_equation"] = final_equation
        
        # explanation text
        explanation_text = Text("Three groups of four stars equals twelve stars total", color=GRAY_B, font_size=36)
        explanation_text.next_to(final_equation, DOWN, buff=0.5)
        self.objects["explanation_text"] = explanation_text
        
        # Helper function to create a 2x2 grid of stars
        def create_star_grid():
            star = Star(color=YELLOW, outer_radius=0.2, inner_radius=0.1, density=5)
            star.set_fill(YELLOW, opacity=0.8)
            star.set_stroke(WHITE, width=1)
            star.set_z_index(1)
            return star
        
        # We'll create the star groups dynamically during the sequence
        # Store them for later use in merging
        self.star_groups = {}
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/Specification_for_An_07b842c1db/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 5.448 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/Specification_for_An_07b842c1db/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # signal_action: Indicate group1_label
        self.play(Indicate(self.objects["group1_label"], color=BLUE, run_time=1))
        # visual_action: Create group1_label
        self.play(Write(self.objects["group1_label"]), run_time=1.0)
        remaining_2 = max(0.1, 6.624 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/Specification_for_An_07b842c1db/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # signal_action: Circumscribe group1_container
        self.play(Circumscribe(self.objects["group1_container"], color=YELLOW, run_time=1))
        # visual_action: Create 4 stars in group1_container
        stars1 = VGroup()
        for _ in range(4):
            star = create_star_grid()
            stars1.add(star)
        stars1.arrange_in_grid(rows=2, cols=2, buff=0.3).move_to(self.objects["group1_container"].get_center())
        self.star_groups["group1"] = stars1
        # Add stars to the container VGroup
        self.objects["group1_container"].add(*stars1)
        self.play(Create(stars1), run_time=2.0)
        remaining_3 = max(0.1, 5.136 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/Specification_for_An_07b842c1db/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # signal_action: Indicate group2_label
        self.play(Indicate(self.objects["group2_label"], color=GREEN, run_time=1))
        # visual_action: Create group2_label and stars
        self.play(Write(self.objects["group2_label"]), run_time=0.5)
        stars2 = VGroup()
        for _ in range(4):
            star = create_star_grid()
            stars2.add(star)
        stars2.arrange_in_grid(rows=2, cols=2, buff=0.3).move_to(self.objects["group2_container"].get_center())
        self.star_groups["group2"] = stars2
        self.objects["group2_container"].add(*stars2)
        self.play(Create(stars2), run_time=2.0)
        remaining_4 = max(0.1, 3.816 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/Specification_for_An_07b842c1db/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # signal_action: Indicate group3_label
        self.play(Indicate(self.objects["group3_label"], color=YELLOW, run_time=1))
        # visual_action: Create group3_label and stars
        self.play(Write(self.objects["group3_label"]), run_time=0.5)
        stars3 = VGroup()
        for _ in range(4):
            star = create_star_grid()
            stars3.add(star)
        stars3.arrange_in_grid(rows=2, cols=2, buff=0.3).move_to(self.objects["group3_container"].get_center())
        self.star_groups["group3"] = stars3
        self.objects["group3_container"].add(*stars3)
        self.play(Create(stars3), run_time=2.0)
        remaining_5 = max(0.1, 5.688 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/Specification_for_An_07b842c1db/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # signal_action: Circumscribe group1_container
        self.play(Circumscribe(self.objects["group1_container"], color=WHITE, run_time=1))
        # visual_action: Animate group1_container moving to content_center
        # Also fade out its label
        self.play(
            self.objects["group1_container"].animate.move_to(content_center),
            FadeOut(self.objects["group1_label"]),
            run_time=2.0
        )
        remaining_6 = max(0.1, 5.736 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/Specification_for_An_07b842c1db/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        # signal_action: Indicate group2_container
        self.play(Indicate(self.objects["group2_container"], color=WHITE, run_time=1))
        # visual_action: Animate group2_container moving to content_center
        # Also fade out its label
        self.play(
            self.objects["group2_container"].animate.move_to(content_center),
            FadeOut(self.objects["group2_label"]),
            run_time=1.5
        )
        remaining_7 = max(0.1, 2.664 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # ========== Step 8 ==========
        audio_step8 = "media/audio/Specification_for_An_07b842c1db/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        # signal_action: Indicate group3_container
        self.play(Indicate(self.objects["group3_container"], color=WHITE, run_time=1))
        # visual_action: Animate group3_container moving to content_center
        # Also fade out its label
        self.play(
            self.objects["group3_container"].animate.move_to(content_center),
            FadeOut(self.objects["group3_label"]),
            run_time=1.5
        )
        remaining_8 = max(0.1, 3.936 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # ========== Step 9 ==========
        audio_step9 = "media/audio/Specification_for_An_07b842c1db/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        # signal_action: Circumscribe group1_container (now the merged group)
        self.play(Circumscribe(self.objects["group1_container"], color=GREEN, run_time=1))
        # visual_action: Create temporary counting labels
        # We'll count all 12 stars in the merged group
        merged_stars = VGroup(*self.star_groups["group1"], *self.star_groups["group2"], *self.star_groups["group3"])
        # Arrange stars in a better grid for counting (4x3)
        # First, let's reposition stars in a 4x3 grid at the center
        for idx, star in enumerate(merged_stars):
            row = idx // 4
            col = idx % 4
            target_pos = content_center + np.array([(col-1.5)*0.6, (0.5-row)*0.6, 0])
            star.generate_target()
            star.target.move_to(target_pos)
        
        self.play(
            *[MoveToTarget(star) for star in merged_stars],
            run_time=2.0
        )
        
        # Create counting labels
        count_labels = VGroup()
        for idx, star in enumerate(merged_stars):
            label = Text(str(idx+1), color=WHITE, font_size=20)
            label.next_to(star, UP, buff=0.1)
            count_labels.add(label)
        
        # Animate counting sequentially
        for i, label in enumerate(count_labels):
            self.play(FadeIn(label), run_time=0.2)
            self.wait(max(0.1, 0.1))
        
        remaining_9 = max(0.1, 4.944 - (2.0 + 12*0.3) + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # Fade out counting labels
        self.play(FadeOut(count_labels), run_time=0.5)
        
        # ========== Step 10 ==========
        audio_step10 = "media/audio/Specification_for_An_07b842c1db/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        
        # signal_action: Indicate final_equation
        self.play(Indicate(self.objects["final_equation"], color=YELLOW, run_time=1))
        # visual_action: Write final_equation
        self.play(Write(self.objects["final_equation"]), run_time=1.5)
        remaining_10 = max(0.1, 5.688 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_10))
        
        # ========== Step 11 ==========
        audio_step11 = "media/audio/Specification_for_An_07b842c1db/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        
        # signal_action: null
        # visual_action: Write explanation_text
        self.play(Write(self.objects["explanation_text"]), run_time=2.0)
        remaining_11 = max(0.1, 8.592 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_11))
        
        # Final pause
        self.wait(max(0.1, 2))