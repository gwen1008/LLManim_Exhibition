from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/The_animation_will_i_fa9588e2a4/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN + 0.5 * UP  # Slightly above bottom edge
        
        # Create objects from layout_plan.objects
        # title_text
        title_text = Text("Understanding Multiplication: 3 × 4", color=WHITE, font_size=36)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text
        
        # equation
        equation = MathTex(r"3 \times 4 = ?", color=YELLOW)
        equation.next_to(title_text, DOWN, buff=0.5)
        self.objects["equation"] = equation
        
        # prototype_star (not shown initially, used for cloning)
        prototype_star = Star(n=5, outer_radius=0.2, color=BLUE, fill_opacity=0.8)
        prototype_star.move_to(ORIGIN)
        self.objects["prototype_star"] = prototype_star
        
        # group_prototype (first group of 4 stars)
        # Build from prototype star at positions relative to content_center
        star_positions = [
            np.array([-0.5, 0.5, 0]),
            np.array([0.5, 0.5, 0]),
            np.array([-0.5, -0.5, 0]),
            np.array([0.5, -0.5, 0])
        ]
        stars = VGroup(*[prototype_star.copy().move_to(content_center + pos) for pos in star_positions])
        self.objects["group_prototype"] = stars
        # Also store as group_1 for later reference in sequence
        self.objects["group_1"] = stars
        
        # counter_label
        counter_label = Text("Total Stars:", color=GRAY_B, font_size=28)
        counter_label.move_to(footer_anchor + 2 * LEFT)
        self.objects["counter_label"] = counter_label
        
        # counter_number (using Integer)
        counter_number = Integer(0, color=GREEN, font_size=36)
        counter_number.next_to(counter_label, RIGHT, buff=0.3)
        self.objects["counter_number"] = counter_number
        
        # final_grid (will be created during animation, store placeholder)
        # Define grid positions for 3 rows, 4 columns
        grid_positions = []
        for row in range(3):
            for col in range(4):
                x = -1.5 + col * 1.0
                y = 1.0 - row * 1.0
                grid_positions.append(np.array([x, y, 0]))
        final_stars = VGroup(*[prototype_star.copy().move_to(pos) for pos in grid_positions])
        final_stars.set_color(GREEN)
        self.objects["final_grid"] = final_stars
        
        # Create duplicate groups (group_2, group_3) for step 4
        group_2 = stars.copy()
        group_2.move_to(content_center + 2.5 * LEFT)
        self.objects["group_2"] = group_2
        
        group_3 = stars.copy()
        group_3.move_to(content_center + 2.5 * RIGHT)
        self.objects["group_3"] = group_3
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/understanding_multiplication_3x4/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(FadeIn(title_text), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/understanding_multiplication_3x4/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Signal action: Write equation (as per JSON signal_action)
        self.play(Write(equation), run_time=1.5)
        remaining_2 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/understanding_multiplication_3x4/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Indicate group_prototype
        self.play(Indicate(stars, color=YELLOW, run_time=1))
        # Visual action: Create the first group
        self.play(Create(stars), run_time=2.0)
        # Also add counter label and number
        self.play(FadeIn(counter_label), FadeIn(counter_number), run_time=1.0)
        # Update counter to 4
        self.play(counter_number.animate.set_value(4), run_time=1.0)
        remaining_3 = max(0.1, 4.0 - (1 + 2.0 + 1.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/understanding_multiplication_3x4/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # No signal action for this step (null)
        # Visual action: Duplicate two more groups
        self.play(Create(group_2), Create(group_3), run_time=2.0)
        # Update counter to 12
        self.play(counter_number.animate.set_value(12), run_time=1.5)
        remaining_4 = max(0.1, 4.0 - (2.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/understanding_multiplication_3x4/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Indicate all three groups
        self.play(
            Indicate(stars, color=ORANGE, run_time=1),
            Indicate(group_2, color=ORANGE, run_time=1),
            Indicate(group_3, color=ORANGE, run_time=1)
        )
        # Visual action: Transform all stars into final grid
        # We'll animate each star to its grid position
        all_stars = VGroup(stars, group_2, group_3)
        # Create a list of all current star positions and target positions
        current_stars = [star for group in all_stars for star in group]
        target_stars = final_stars  # Already created VGroup
        
        # Animate each star moving to its target position
        animations = []
        for i, star in enumerate(current_stars):
            if i < len(target_stars):
                animations.append(star.animate.move_to(target_stars[i].get_center()).set_color(GREEN))
        # Also update counter to 12 and equation
        animations.append(counter_number.animate.set_value(12))
        # Update equation
        new_equation = MathTex(r"3 \times 4 = 12", color=YELLOW)
        new_equation.move_to(equation.get_center())
        animations.append(TransformMatchingTex(equation, new_equation))
        
        self.play(*animations, run_time=3.0)
        # Update equation reference
        self.objects["equation"] = new_equation
        remaining_5 = max(0.1, 5.0 - (1 + 3.0) + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/understanding_multiplication_3x4/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe final_grid
        self.play(Circumscribe(final_stars, color=GREEN, run_time=1))
        # Visual action: Wait (hold scene)
        remaining_6 = max(0.1, 4.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_6))