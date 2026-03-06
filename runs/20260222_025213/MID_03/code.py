'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize solving the equation 2x = 6 using a balance scale metaphor to make the concept of equality and division tangible.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title (equation)
#    - Main Content: [Center y=0 to y=1] for the scale and objects
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for circles and boxes to keep them together. Position scale parts relative to anchors. Keep equation centered at top.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Build the scale structure.
#    - Step 2: Add boxes (left) and circles (right) to pans, indicate equation.
#    - Step 3: Highlight and separate circles into two groups.
#    - Step 4: Merge boxes, remove half the circles, animate remaining circles back.
#    - Step 5: Transform equation to final solution, highlight result.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors from layout_plan
        title_anchor = 3.5 * UP
        scale_pivot = ORIGIN + UP  # (0,1,0)
        left_pan_center = np.array([-2, 0.5, 0])
        right_pan_center = np.array([2, 0.5, 0])
        explanation_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # title_eq_initial
        title_eq_initial = MathTex("2x = 6", color=WHITE, font_size=48)
        title_eq_initial.move_to(title_anchor)
        self.objects["title_eq_initial"] = title_eq_initial

        # scale_beam
        scale_beam = Line(start=LEFT*3, end=RIGHT*3, color=WHITE, stroke_width=8)
        scale_beam.move_to(scale_pivot)
        self.objects["scale_beam"] = scale_beam

        # scale_pivot_point
        scale_pivot_point = Circle(radius=0.15, color=GRAY, fill_opacity=1)
        scale_pivot_point.move_to(scale_pivot)
        self.objects["scale_pivot_point"] = scale_pivot_point

        # left_pan
        left_pan = RoundedRectangle(width=1.5, height=0.2, corner_radius=0.1, color=GRAY_B, fill_opacity=0.7)
        left_pan.move_to(left_pan_center)
        self.objects["left_pan"] = left_pan

        # right_pan
        right_pan = RoundedRectangle(width=1.5, height=0.2, corner_radius=0.1, color=GRAY_B, fill_opacity=0.7)
        right_pan.move_to(right_pan_center)
        self.objects["right_pan"] = right_pan

        # left_pan_support
        left_pan_support = Line(
            start=scale_pivot + LEFT*2,
            end=left_pan_center + UP*0.1,
            color=WHITE,
            stroke_width=4
        )
        self.objects["left_pan_support"] = left_pan_support

        # right_pan_support
        right_pan_support = Line(
            start=scale_pivot + RIGHT*2,
            end=right_pan_center + UP*0.1,
            color=WHITE,
            stroke_width=4
        )
        self.objects["right_pan_support"] = right_pan_support

        # box1
        box1 = Square(side_length=0.7, color=BLUE, fill_opacity=0.8, stroke_width=2)
        box1.move_to(left_pan_center + UP*0.2)
        self.objects["box1"] = box1

        # box2
        box2 = Square(side_length=0.7, color=BLUE, fill_opacity=0.8, stroke_width=2)
        box2.move_to(left_pan_center + DOWN*0.2)
        self.objects["box2"] = box2

        # box_label_initial (create one, will be copied)
        box_label = MathTex("x", color=WHITE, font_size=30)
        box_label.move_to(box1.get_center())
        self.objects["box_label_initial"] = box_label

        # circles_group: Six circles arranged in 2x3 grid
        circles = []
        circle_radius = 0.25
        for i in range(2):  # rows
            for j in range(3):  # columns
                circle = Circle(radius=circle_radius, color=GREEN, fill_opacity=0.8)
                # Arrange relative to right_pan_center
                circle.move_to(right_pan_center + RIGHT * (j - 1) * 0.6 + DOWN * (i - 0.5) * 0.6)
                circles.append(circle)
        circles_group = VGroup(*circles)
        self.objects["circles_group"] = circles_group

        # step_text
        step_text = Text("Initial state: 2x = 6", color=YELLOW, font_size=28)
        step_text.move_to(explanation_anchor)
        self.objects["step_text"] = step_text

        # Create a copy of box label for box2
        box_label2 = box_label.copy()
        box_label2.move_to(box2.get_center())
        self.objects["box_label2"] = box_label2
        
        # Fix misalignment of initial box label
        box_label.move_to(box1.get_center())

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(
            Create(self.objects["scale_beam"]),
            Create(self.objects["scale_pivot_point"]),
            Create(self.objects["left_pan_support"]),
            Create(self.objects["right_pan_support"]),
            Create(self.objects["left_pan"]),
            Create(self.objects["right_pan"]),
            run_time=3
        )
        self.wait(max(0.1, max(0.1, 5.04 - 3)))

        # Step 2
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate title_eq_initial
        self.play(Indicate(self.objects["title_eq_initial"], color=YELLOW))
        # Visual action: Create boxes and circles
        self.play(
            Create(self.objects["box1"]),
            Create(self.objects["box2"]),
            Create(self.objects["circles_group"]),
            run_time=3
        )
        # Also write the equation title and step text
        self.play(Write(self.objects["title_eq_initial"]))
        self.play(Write(self.objects["step_text"]))
        # Write box labels
        self.play(Write(self.objects["box_label_initial"]), Write(self.objects["box_label2"]))
        self.wait(max(0.1, max(0.1, 8.28 - 3 - 1)))  # account for Indicate and Creates

        # Step 3
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Update step text
        new_step_text = Text("Divide both sides by 2", color=YELLOW, font_size=28)
        new_step_text.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], new_step_text))
        self.objects["step_text"] = new_step_text
        # Signal action: Circumscribe circles_group
        self.play(Circumscribe(self.objects["circles_group"], color=YELLOW, run_time=1))
        # Visual action: Animate circles rising and separating into two groups
        circles = self.objects["circles_group"]
        # Create two groups: left three and right three
        left_circles = VGroup(circles[0], circles[2], circles[4])  # assuming arrangement
        right_circles = VGroup(circles[1], circles[3], circles[5])
        # Animate them moving apart
        self.play(
            left_circles.animate.shift(LEFT * 0.8),
            right_circles.animate.shift(RIGHT * 0.8),
            run_time=2
        )
        self.wait(max(0.1, max(0.1, 7.584 - 1 - 2)))

        # Step 4
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Update step text
        new_step_text2 = Text("Merge boxes, remove half the circles", color=YELLOW, font_size=28)
        new_step_text2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], new_step_text2))
        self.objects["step_text"] = new_step_text2
        # Signal action: Indicate box1
        self.play(Indicate(self.objects["box1"], color=YELLOW))
        # Visual action: Merge boxes into one at left_pan_center
        merged_box = Square(side_length=0.7, color=BLUE, fill_opacity=0.8, stroke_width=2)
        merged_box.move_to(left_pan_center)
        merged_label = MathTex("x", color=WHITE, font_size=30)
        merged_label.move_to(merged_box.get_center())
        self.play(
            Transform(self.objects["box1"], merged_box),
            Transform(self.objects["box2"], merged_box.copy()),  # both transform to same
            Transform(self.objects["box_label_initial"], merged_label),
            Transform(self.objects["box_label2"], merged_label.copy()),
            run_time=2
        )
        # Fade out right_circles (three circles)
        self.play(FadeOut(right_circles), run_time=1)
        # Animate left_circles back to right pan center
        self.play(
            left_circles.animate.move_to(right_pan_center),
            run_time=2
        )
        self.wait(max(0.1, max(0.1, 11.28 - 2 - 1 - 2)))

        # Step 5
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Update step text
        final_step_text = Text("Solution: x = 3", color=GREEN, font_size=28)
        final_step_text.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], final_step_text))
        self.objects["step_text"] = final_step_text
        # Create final equation
        title_eq_final = MathTex("x = 3", color=WHITE, font_size=48)
        title_eq_final.move_to(title_anchor)
        self.objects["title_eq_final"] = title_eq_final
        # Visual action: ReplacementTransform equation
        self.play(ReplacementTransform(self.objects["title_eq_initial"], title_eq_final))
        # Signal action: Circumscribe final equation
        self.play(Circumscribe(title_eq_final, color=GREEN, run_time=1))
        self.wait(max(0.1, max(0.1, 7.584 - 1)))