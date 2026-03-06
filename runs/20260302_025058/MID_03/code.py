'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Solve the linear equation 2x = 6 using a concrete balance scale model.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and Equation.
#    - Main Content: [Center y=0] for the balance scale and objects.
#    - Footer Region: [Bottom y=-3.0] for explanation text.
# 3. Anti-Overlap Check:
#    - The scale is centered. Objects are placed on pans. Equation is above.
#    - When circles group and move, ensure they stay within screen bounds.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Create_a_Manim_anima_5e127dcdaa/step_XX.mp3"
# 5. Animation Flow:
#    - Build scale structure.
#    - Place objects (boxes and circles) showing imbalance.
#    - Show equation.
#    - Group circles, move one group to balance one box.
#    - Update equation to x = 3 and balance the scale.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        scale_center = ORIGIN
        explanation_anchor = 3.0 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Scale Beam
        scale_beam = Line(start=LEFT*3, end=RIGHT*3, color=GRAY_B, stroke_width=8)
        scale_beam.move_to(scale_center + UP*1.5)
        self.objects["scale_beam"] = scale_beam

        # Fulcrum (Triangle)
        fulcrum = Polygon(
            [0, 0, 0],
            [-0.5, -1, 0],
            [0.5, -1, 0],
            color=GRAY, fill_opacity=1.0
        )
        fulcrum.move_to(scale_center + UP*1.5)
        self.objects["fulcrum"] = fulcrum

        # Left Pan
        left_pan = Rectangle(width=2.5, height=0.2, color=GOLD, fill_opacity=0.7)
        left_pan.move_to(scale_beam.get_start() + DOWN*1.5)
        self.objects["left_pan"] = left_pan

        # Right Pan
        right_pan = Rectangle(width=2.5, height=0.2, color=GOLD, fill_opacity=0.7)
        right_pan.move_to(scale_beam.get_end() + DOWN*1.5)
        self.objects["right_pan"] = right_pan

        # Left Objects: Two blue squares labeled 'x'
        square1 = Square(side_length=1, color=BLUE, fill_opacity=0.7)
        square2 = Square(side_length=1, color=BLUE, fill_opacity=0.7)
        label1 = MathTex("x", color=WHITE).scale(0.8).move_to(square1.get_center())
        label2 = MathTex("x", color=WHITE).scale(0.8).move_to(square2.get_center())
        left_objects = VGroup(square1, square2, label1, label2)
        left_objects.arrange(DOWN, buff=0.2)
        left_objects.move_to(left_pan.get_center())
        self.objects["left_objects"] = left_objects

        # Right Objects: Six red circles
        circles = VGroup(*[Circle(radius=0.4, color=RED, fill_opacity=0.7) for _ in range(6)])
        circles.arrange_in_grid(rows=2, cols=3, buff=0.3)
        circles.move_to(right_pan.get_center())
        self.objects["right_objects"] = circles

        # Equation
        equation = MathTex("2x = 6", color=YELLOW, font_size=48)
        equation.move_to(scale_center + UP*3.0)
        self.objects["equation"] = equation

        # Explanation Text
        explanation_text = Text("Let's set up the balance scale.", color=GRAY_B, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # Additional objects needed for later steps (created now but not added)
        # For step 6: Two groups of circles
        circle_group1 = VGroup(*circles[0:3])
        circle_group2 = VGroup(*circles[3:6])
        circle_group1.save_state()
        circle_group2.save_state()
        self.objects["circle_group_1"] = circle_group1
        self.objects["circle_group_2"] = circle_group2

        # For step 7: A copy of one group to move
        moving_group = circle_group1.copy()
        self.objects["moving_group"] = moving_group

        # For step 8: Transformed equation
        equation_final = MathTex("x = 3", color=GREEN, font_size=48)
        equation_final.move_to(equation.get_center())
        self.objects["equation_final"] = equation_final

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/Create_a_Manim_anima_5e127dcdaa/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(FadeIn(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 12.36 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/Create_a_Manim_anima_5e127dcdaa/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["fulcrum"]), run_time=2.0)
        remaining_2 = max(0.1, 7.56 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/Create_a_Manim_anima_5e127dcdaa/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(
            Create(self.objects["scale_beam"]),
            Create(self.objects["left_pan"]),
            Create(self.objects["right_pan"]),
            run_time=2.0
        )
        remaining_3 = max(0.1, 3.096 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/Create_a_Manim_anima_5e127dcdaa/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # Signal action: Indicate left_objects
        self.play(Indicate(self.objects["left_objects"], color=BLUE, run_time=1))
        # Visual action: Create left and right objects, tilt scale
        self.play(
            FadeIn(self.objects["left_objects"]),
            FadeIn(self.objects["right_objects"]),
            run_time=2.0
        )
        # Tilt the scale: right pan down, left pan up
        self.play(
            self.objects["right_pan"].animate.shift(DOWN*0.2),
            self.objects["left_pan"].animate.shift(UP*0.2),
            self.objects["scale_beam"].animate.rotate(-0.1, about_point=scale_center + UP*1.5),
            run_time=1.5
        )
        remaining_4 = max(0.1, 5.88 - (1 + 2.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/Create_a_Manim_anima_5e127dcdaa/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # Signal action: Circumscribe equation
        self.play(Circumscribe(self.objects["equation"], color=YELLOW, run_time=1))
        # Visual action: Write equation
        self.play(Write(self.objects["equation"]), run_time=1.5)
        # Update explanation text
        new_explanation = Text("This setup represents 2x = 6.", color=GRAY_B, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        remaining_5 = max(0.1, 9.48 - (1 + 1.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/Create_a_Manim_anima_5e127dcdaa/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # Signal action: Indicate right_objects
        self.play(Indicate(self.objects["right_objects"], color=RED, run_time=1))
        # Visual action: Separate circles into two groups
        group1_target = self.objects["circle_group_1"].copy()
        group2_target = self.objects["circle_group_2"].copy()
        group1_target.shift(LEFT*1.5 + UP*0.5)
        group2_target.shift(RIGHT*1.5 + UP*0.5)
        self.play(
            Transform(self.objects["circle_group_1"], group1_target),
            Transform(self.objects["circle_group_2"], group2_target),
            run_time=2.0
        )
        # Update explanation text
        new_explanation2 = Text("Divide the six into two equal groups.", color=GRAY_B, font_size=24)
        new_explanation2.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], new_explanation2))
        self.objects["explanation_text"] = new_explanation2
        remaining_6 = max(0.1, 10.896 - (1 + 2.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/Create_a_Manim_anima_5e127dcdaa/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # Signal action: Indicate one group of circles (use group1)
        self.play(Indicate(self.objects["circle_group_1"], color=GREEN, run_time=1))
        # Visual action: Move one group to left side next to a box
        moving_group = self.objects["moving_group"]
        left_box = self.objects["left_objects"][0]  # First square
        target_pos = left_box.get_center() + RIGHT*1.5
        self.play(moving_group.animate.move_to(target_pos), run_time=2.0)
        # Animate scale beginning to balance
        self.play(
            self.objects["right_pan"].animate.shift(UP*0.1),
            self.objects["left_pan"].animate.shift(DOWN*0.1),
            self.objects["scale_beam"].animate.rotate(0.05, about_point=scale_center + UP*1.5),
            run_time=1.5
        )
        # Update explanation text
        new_explanation3 = Text("One group of three balances one x.", color=GRAY_B, font_size=24)
        new_explanation3.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], new_explanation3))
        self.objects["explanation_text"] = new_explanation3
        remaining_7 = max(0.1, 8.088 - (1 + 2.0 + 1.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        audio_step8 = "media/audio/Create_a_Manim_anima_5e127dcdaa/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # Signal action: Circumscribe equation
        self.play(Circumscribe(self.objects["equation"], color=GREEN, run_time=1))
        # Visual action: Transform equation
        self.play(TransformMatchingTex(self.objects["equation"], self.objects["equation_final"]), run_time=1.5)
        self.objects["equation"] = self.objects["equation_final"]
        # Update explanation text
        new_explanation4 = Text("Therefore, x = 3.", color=GRAY_B, font_size=24)
        new_explanation4.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], new_explanation4))
        self.objects["explanation_text"] = new_explanation4
        remaining_8 = max(0.1, 8.304 - (1 + 1.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        audio_step9 = "media/audio/Create_a_Manim_anima_5e127dcdaa/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        # Visual action: Balance the scale completely
        self.play(
            self.objects["right_pan"].animate.shift(UP*0.1),  # Back to original
            self.objects["left_pan"].animate.shift(DOWN*0.1), # Back to original
            self.objects["scale_beam"].animate.rotate(0.05, about_point=scale_center + UP*1.5), # To horizontal
            run_time=2.0
        )
        remaining_9 = max(0.1, 6.648 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Final hold
        self.wait(max(0.1, 2))