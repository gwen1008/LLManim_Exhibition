from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create anchors based on layout_plan description
        title_anchor = 3.5 * UP
        scale_pivot = ORIGIN
        left_pan_center = scale_pivot + 3 * LEFT + DOWN * 1.2
        right_pan_center = scale_pivot + 3 * RIGHT + DOWN * 1.2
        explanation_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # title
        title = Text("Solving 2x = 6 with a Balance Scale", font_size=36, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # scale_beam
        scale_beam = Line(start=LEFT*3, end=RIGHT*3, color=GRAY_B, stroke_width=8)
        scale_beam.move_to(scale_pivot + UP*0.5)
        self.objects["scale_beam"] = scale_beam

        # scale_pivot_point
        scale_pivot_point = Circle(radius=0.2, color=GRAY, fill_opacity=1)
        scale_pivot_point.move_to(scale_pivot + UP*0.5)
        self.objects["scale_pivot_point"] = scale_pivot_point

        # left_pan
        left_pan = Circle(radius=1.0, color=GRAY, fill_opacity=0.2, stroke_width=3)
        left_pan.move_to(scale_beam.get_start() + DOWN*1.2)
        self.objects["left_pan"] = left_pan

        # right_pan
        right_pan = Circle(radius=1.0, color=GRAY, fill_opacity=0.2, stroke_width=3)
        right_pan.move_to(scale_beam.get_end() + DOWN*1.2)
        self.objects["right_pan"] = right_pan

        # box1
        box1 = Square(side_length=0.8, color=BLUE, fill_opacity=0.7, stroke_width=2)
        box1.move_to(left_pan.get_center() + UP*0.4)
        self.objects["box1"] = box1

        # box2
        box2 = Square(side_length=0.8, color=BLUE, fill_opacity=0.7, stroke_width=2)
        box2.move_to(left_pan.get_center() + DOWN*0.4)
        self.objects["box2"] = box2

        # label_x1
        label_x1 = MathTex("x", color=WHITE, font_size=30)
        label_x1.move_to(box1.get_center())
        self.objects["label_x1"] = label_x1

        # label_x2
        label_x2 = MathTex("x", color=WHITE, font_size=30)
        label_x2.move_to(box2.get_center())
        self.objects["label_x2"] = label_x2

        # circles 1-6
        circle1 = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle1.move_to(right_pan.get_center() + LEFT*0.8 + UP*0.8)
        self.objects["circle1"] = circle1

        circle2 = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle2.move_to(right_pan.get_center() + RIGHT*0.0 + UP*0.8)
        self.objects["circle2"] = circle2

        circle3 = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle3.move_to(right_pan.get_center() + RIGHT*0.8 + UP*0.8)
        self.objects["circle3"] = circle3

        circle4 = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle4.move_to(right_pan.get_center() + LEFT*0.8 + DOWN*0.0)
        self.objects["circle4"] = circle4

        circle5 = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle5.move_to(right_pan.get_center() + RIGHT*0.0 + DOWN*0.0)
        self.objects["circle5"] = circle5

        circle6 = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle6.move_to(right_pan.get_center() + RIGHT*0.8 + DOWN*0.0)
        self.objects["circle6"] = circle6

        # eq_initial
        eq_initial = MathTex("2x = 6", font_size=48, color=YELLOW)
        eq_initial.move_to(scale_pivot + UP*2.0)
        self.objects["eq_initial"] = eq_initial

        # step_explanation
        step_explanation = Text("The scale is balanced: 2x equals 6.", font_size=28, color=GRAY_B)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # Create VGroups for easier handling
        boxes_group = VGroup(box1, box2, label_x1, label_x2)
        circles_group = VGroup(circle1, circle2, circle3, circle4, circle5, circle6)
        scale_structure = VGroup(scale_beam, scale_pivot_point, left_pan, right_pan)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(FadeIn(self.objects["title"]))
        self.wait(max(0.1, max(0.1, 6.24 - 1.0)))

        # Step 2
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(scale_structure))
        self.wait(max(0.1, max(0.1, 6.048 - 1.0)))

        # Step 3
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(boxes_group))
        self.wait(max(0.1, max(0.1, 6.24 - 1.0)))

        # Step 4
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(circles_group))
        self.wait(max(0.1, max(0.1, 4.608 - 1.0)))

        # Step 5
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate eq_initial
        self.play(Indicate(self.objects["eq_initial"], color=YELLOW))
        # Visual action: Write eq_initial
        self.play(Write(self.objects["eq_initial"]))
        self.wait(max(0.1, max(0.1, 8.784 - 2.0)))

        # Step 6
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Circumscribe circles
        self.play(Circumscribe(circles_group, color=YELLOW, run_time=1))
        # Visual action: Update step_explanation text
        new_explanation = Text("Divide both sides by 2: Split the 6 into two groups of 3.", font_size=28, color=GRAY_B)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        self.wait(max(0.1, max(0.1, 5.472 - 2.0)))

        # Step 7
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate box2
        self.play(Indicate(self.objects["box2"], color=RED))
        # Visual action: GroupTransform circles and FadeOut box2, label_x2
        # Create target positions for circles (two groups)
        target_positions = [
            right_pan.get_center() + LEFT*1.0 + UP*0.0,
            right_pan.get_center() + RIGHT*0.0 + UP*0.0,
            right_pan.get_center() + RIGHT*1.0 + UP*0.0,
            right_pan.get_center() + LEFT*1.0 + DOWN*1.0,
            right_pan.get_center() + RIGHT*0.0 + DOWN*1.0,
            right_pan.get_center() + RIGHT*1.0 + DOWN*1.0
        ]
        # Animate circles moving to new positions
        circle_anims = []
        for i, circle in enumerate(circles_group):
            circle_anims.append(circle.animate.move_to(target_positions[i]))
        # Simultaneously fade out box2 and label_x2
        self.play(*circle_anims, FadeOut(self.objects["box2"]), FadeOut(self.objects["label_x2"]))
        self.wait(max(0.1, max(0.1, 5.856 - 2.0)))

        # Step 8
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_07.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Visual action: ReplacementTransform eq_initial to "x = 3"
        eq_final = MathTex("x = 3", font_size=48, color=GREEN)
        eq_final.move_to(self.objects["eq_initial"].get_center())
        self.play(ReplacementTransform(self.objects["eq_initial"], eq_final))
        self.objects["eq_initial"] = eq_final
        self.wait(max(0.1, max(0.1, 4.728 - 1.0)))

        # Step 9
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_08.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Circumscribe box1 and first three circles
        solution_group = VGroup(self.objects["box1"], circle1, circle2, circle3)
        self.play(Circumscribe(solution_group, color=GREEN, run_time=1))
        # Visual action: Update step_explanation text
        final_explanation = Text("Solution: x = 3. One box balances three units.", font_size=28, color=GRAY_B)
        final_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], final_explanation))
        self.wait(max(0.1, max(0.1, 2.712 - 2.0)))