'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing multiplication as grouping and aggregation (3 groups of 4 equals 12).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and Equation.
#    - Main Content: [Center y=0] for three groups of dots and final grid.
#    - Footer Region: [Bottom y=-3.5] for step explanation text.
# 3. Anti-Overlap Check:
#    - Groups are positioned in a triangle around center with sufficient spacing.
#    - Final grid is centered, replacing groups.
#    - Explanation text stays at bottom, separate.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/visualizing_multiplication_3x4/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show title and equation, indicate equation.
#    - Step 2: Create first group, circumscribe it.
#    - Step 3: Create second and third groups, circumscribe both.
#    - Step 4: Transform all groups into a 4x3 grid, indicate grid.
#    - Step 5: Morph equation to show answer 12, circumscribe final grid.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/The_animation_should_0d16e96e98/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on layout_plan description
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create title_text
        title_text = Text("Visualizing Multiplication: 3 × 4", color=WHITE, font_size=40)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text
        
        # Create equation
        equation = MathTex(r"3 \times 4 = ?", color=BLUE_B, font_size=36)
        equation.next_to(title_text, DOWN, buff=0.5)
        self.objects["equation"] = equation
        
        # Create group1 (4 dots in 2x2 grid)
        group1_dots = VGroup(*[Dot(color=YELLOW) for _ in range(4)])
        group1_dots.arrange_in_grid(rows=2, cols=2, buff=0.3)
        group1_dots.move_to(content_center + UP * 2.5)
        self.objects["group1"] = group1_dots
        
        # Create group2
        group2_dots = VGroup(*[Dot(color=YELLOW) for _ in range(4)])
        group2_dots.arrange_in_grid(rows=2, cols=2, buff=0.3)
        group2_dots.move_to(content_center + LEFT * 2.165 + DOWN * 1.25)
        self.objects["group2"] = group2_dots
        
        # Create group3
        group3_dots = VGroup(*[Dot(color=YELLOW) for _ in range(4)])
        group3_dots.arrange_in_grid(rows=2, cols=2, buff=0.3)
        group3_dots.move_to(content_center + RIGHT * 2.165 + DOWN * 1.25)
        self.objects["group3"] = group3_dots
        
        # Create final_grid (12 dots in 4x3 grid)
        final_grid_dots = VGroup(*[Dot(color=YELLOW) for _ in range(12)])
        final_grid_dots.arrange_in_grid(rows=3, cols=4, buff=0.7)
        final_grid_dots.move_to(content_center)
        final_grid_dots.set_opacity(0)  # Initially invisible
        self.objects["final_grid"] = final_grid_dots
        
        # Create step_explanation
        step_explanation = Text(
            "We begin with the multiplication problem 3 times 4.",
            color=GRAY_B,  # GRAY_C is not defined, use GRAY_B
            font_size=28
        )
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/visualizing_multiplication_3x4/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        # Signal action: Indicate equation
        self.play(Indicate(self.objects["equation"], color=YELLOW, run_time=1))
        # Visual action: Create title and equation
        self.play(
            Write(self.objects["title_text"]),
            Write(self.objects["equation"]),
            Write(self.objects["step_explanation"]),
            run_time=2.0
        )
        remaining_1 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/visualizing_multiplication_3x4/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Update explanation text
        new_explanation_2 = Text(
            "This means we have three groups, each containing four items.",
            color=GRAY_B, font_size=28
        )
        new_explanation_2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_2))
        self.objects["step_explanation"] = new_explanation_2
        
        # Signal action: Circumscribe group1
        self.play(Circumscribe(self.objects["group1"], color=GREEN, run_time=1))
        # Visual action: Create group1
        self.play(Create(self.objects["group1"]), run_time=1.5)
        remaining_2 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/visualizing_multiplication_3x4/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Update explanation text
        new_explanation_3 = Text(
            "Here are all three groups of four. We now have all three groups clearly visible.",
            color=GRAY_B, font_size=28
        )
        new_explanation_3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_3))
        self.objects["step_explanation"] = new_explanation_3
        
        # Signal actions: Circumscribe group2 and group3
        self.play(
            Circumscribe(self.objects["group2"], color=GREEN, run_time=1),
            Circumscribe(self.objects["group3"], color=GREEN, run_time=1)
        )
        # Visual action: Create group2 and group3 simultaneously
        self.play(
            Create(self.objects["group2"]),
            Create(self.objects["group3"]),
            run_time=2.0
        )
        remaining_3 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/visualizing_multiplication_3x4/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Update explanation text
        new_explanation_4 = Text(
            "To find the total, we combine all items from every group.",
            color=GRAY_B, font_size=28
        )
        new_explanation_4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_4))
        self.objects["step_explanation"] = new_explanation_4
        
        # Signal action: Indicate final_grid (which is currently invisible)
        # We'll indicate the area where grid will appear
        self.play(Indicate(self.objects["final_grid"], color=ORANGE, run_time=1))
        
        # Prepare for transformation: make final_grid visible and groups transform into it
        # We'll create a copy of final_grid with opacity 1 for transformation target
        final_grid_visible = self.objects["final_grid"].copy()
        final_grid_visible.set_opacity(1)
        
        # Visual action: Transform all groups into the final grid
        # We'll move each dot from groups to corresponding position in grid
        # Since we have 12 dots in each, we can match them by index
        all_groups = VGroup(
            self.objects["group1"],
            self.objects["group2"],
            self.objects["group3"]
        )
        
        # Create transformation animations
        transform_anims = []
        for i, dot in enumerate(final_grid_visible):
            # Find corresponding dot in original groups (flatten groups)
            if i < 4:
                src_dot = self.objects["group1"][i]
            elif i < 8:
                src_dot = self.objects["group2"][i-4]
            else:
                src_dot = self.objects["group3"][i-8]
            transform_anims.append(Transform(src_dot, dot))
        
        self.play(*transform_anims, run_time=3.0)
        # Replace the transformed dots with the final grid
        self.remove(*[anim.mobject for anim in transform_anims])
        self.add(final_grid_visible)
        self.objects["final_grid"] = final_grid_visible
        
        remaining_4 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/visualizing_multiplication_3x4/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Update explanation text
        new_explanation_5 = Text(
            "When we arrange them, we can count the total: twelve.",
            color=GRAY_B, font_size=28
        )
        new_explanation_5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_5))
        self.objects["step_explanation"] = new_explanation_5
        
        # Signal action: Circumscribe final_grid
        self.play(Circumscribe(self.objects["final_grid"], color=YELLOW, run_time=1))
        
        # Visual action: Transform equation from "3 × 4 = ?" to "3 × 4 = 12"
        equation_new = MathTex(r"3 \times 4 = 12", color=BLUE_B, font_size=36)
        equation_new.next_to(self.objects["title_text"], DOWN, buff=0.5)
        # Color the "12" part green
        equation_new.set_color_by_tex("12", GREEN)
        
        self.play(TransformMatchingTex(self.objects["equation"], equation_new))
        self.objects["equation"] = equation_new
        
        remaining_5 = max(0.1, 4.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final hold
        self.wait(max(0.1, 2.0))