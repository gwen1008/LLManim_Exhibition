from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout zones
        title_anchor = 3.5 * UP
        global_center = ORIGIN
        left_pan_anchor = global_center + 2.5 * LEFT + 0.5 * DOWN
        right_pan_anchor = global_center + 2.5 * RIGHT + 0.5 * DOWN
        footer_anchor = 3.0 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Scale pivot
        scale_pivot = Circle(radius=0.15, color=GREY, fill_opacity=0.7)
        scale_pivot.move_to(global_center)
        self.objects["scale_pivot"] = scale_pivot

        # Scale beam
        scale_beam = Line(start=3 * LEFT, end=3 * RIGHT, color=GRAY_B, stroke_width=8)
        scale_beam.move_to(global_center + 0.5 * UP)
        self.objects["scale_beam"] = scale_beam

        # Left pan
        left_pan = Rectangle(width=2.0, height=0.2, color=GREY, fill_opacity=0.3)
        left_pan.move_to(left_pan_anchor)
        self.objects["left_pan"] = left_pan

        # Right pan
        right_pan = Rectangle(width=2.0, height=0.2, color=GREY, fill_opacity=0.3)
        right_pan.move_to(right_pan_anchor)
        self.objects["right_pan"] = right_pan

        # Box 1
        box1 = Square(side_length=0.8, color=BLUE, fill_opacity=0.5, stroke_color=WHITE)
        box1.move_to(left_pan_anchor)
        self.objects["box1"] = box1

        # Box 2
        box2 = Square(side_length=0.8, color=BLUE, fill_opacity=0.5, stroke_color=WHITE)
        box2.next_to(box1, UP, buff=0.1)
        self.objects["box2"] = box2

        # Label x1
        label_x1 = MathTex("x", color=WHITE)
        label_x1.move_to(box1.get_center())
        self.objects["label_x1"] = label_x1

        # Label x2
        label_x2 = MathTex("x", color=WHITE)
        label_x2.move_to(box2.get_center())
        self.objects["label_x2"] = label_x2

        # Circles (create individually, then group)
        circle1 = Circle(radius=0.3, color=GREEN, fill_opacity=0.5, stroke_color=WHITE)
        circle1.move_to(right_pan_anchor + LEFT * 0.9 + UP * 0.4)
        self.objects["circle1"] = circle1

        circle2 = Circle(radius=0.3, color=GREEN, fill_opacity=0.5, stroke_color=WHITE)
        circle2.move_to(right_pan_anchor + LEFT * 0.9 + DOWN * 0.4)
        self.objects["circle2"] = circle2

        circle3 = Circle(radius=0.3, color=GREEN, fill_opacity=0.5, stroke_color=WHITE)
        circle3.move_to(right_pan_anchor + LEFT * 0.0 + UP * 0.4)
        self.objects["circle3"] = circle3

        circle4 = Circle(radius=0.3, color=GREEN, fill_opacity=0.5, stroke_color=WHITE)
        circle4.move_to(right_pan_anchor + LEFT * 0.0 + DOWN * 0.4)
        self.objects["circle4"] = circle4

        circle5 = Circle(radius=0.3, color=GREEN, fill_opacity=0.5, stroke_color=WHITE)
        circle5.move_to(right_pan_anchor + RIGHT * 0.9 + UP * 0.4)
        self.objects["circle5"] = circle5

        circle6 = Circle(radius=0.3, color=GREEN, fill_opacity=0.5, stroke_color=WHITE)
        circle6.move_to(right_pan_anchor + RIGHT * 0.9 + DOWN * 0.4)
        self.objects["circle6"] = circle6

        # Create VGroup for circles
        circles_group = VGroup(circle1, circle2, circle3, circle4, circle5, circle6)
        circles_group.move_to(box1.get_center() + DOWN*1.0)
        self.objects["circles_group"] = circles_group

        # Create '1' labels for each circle
        label_1_template = MathTex("1", color=WHITE).scale(0.7)
        label1 = label_1_template.copy().move_to(circle1.get_center())
        label2 = label_1_template.copy().move_to(circle2.get_center())
        label3 = label_1_template.copy().move_to(circle3.get_center())
        label4 = label_1_template.copy().move_to(circle4.get_center())
        label5 = label_1_template.copy().move_to(circle5.get_center())
        label6 = label_1_template.copy().move_to(circle6.get_center())
        self.objects["label1"] = label1
        self.objects["label2"] = label2
        self.objects["label3"] = label3
        self.objects["label4"] = label4
        self.objects["label5"] = label5
        self.objects["label6"] = label6

        # Equation initial
        equation_initial = MathTex("2x = 6", color=YELLOW, font_size=40)
        equation_initial.move_to(footer_anchor + UP * 0.5)
        self.objects["equation_initial"] = equation_initial

        # Equation final - moved further down to avoid overlap
        equation_final = MathTex("x = 3", color=GREEN, font_size=40)
        equation_final.next_to(footer_anchor, DOWN, buff=0.5)
        self.objects["equation_final"] = equation_final

        # Create target VGroups for split circles (for animation target positions)
        # These are not added to scene initially, just for positioning reference
        group1_circles = VGroup(
            Circle(radius=0.3, color=GREEN, fill_opacity=0.5, stroke_color=WHITE),
            Circle(radius=0.3, color=GREEN, fill_opacity=0.5, stroke_color=WHITE),
            Circle(radius=0.3, color=GREEN, fill_opacity=0.5, stroke_color=WHITE)
        )
        group1_circles.arrange(DOWN, buff=0.2)
        group1_circles.move_to(box1.get_center() + DOWN * 1.5)
        self.objects["group1_circles"] = group1_circles

        group2_circles = VGroup(
            Circle(radius=0.3, color=GREEN, fill_opacity=0.5, stroke_color=WHITE),
            Circle(radius=0.3, color=GREEN, fill_opacity=0.5, stroke_color=WHITE),
            Circle(radius=0.3, color=GREEN, fill_opacity=0.5, stroke_color=WHITE)
        )
        group2_circles.arrange(DOWN, buff=0.2)
        group2_circles.move_to(box2.get_center() + DOWN * 1.5)
        self.objects["group2_circles"] = group2_circles

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 5.544 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["box1"], color=YELLOW, run_time=1))
        self.play(
            Create(self.objects["scale_pivot"]),
            Create(self.objects["scale_beam"]),
            Create(self.objects["left_pan"]),
            Create(self.objects["right_pan"]),
            Create(self.objects["box1"]),
            Create(self.objects["box2"]),
            Write(self.objects["label_x1"]),
            Write(self.objects["label_x2"]),
            run_time=3.0
        )
        remaining_2 = max(0.1, 8.136 - 1 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["circles_group"], color=YELLOW, run_time=1))
        self.play(
            Create(self.objects["circle1"]),
            Create(self.objects["circle2"]),
            Create(self.objects["circle3"]),
            Create(self.objects["circle4"]),
            Create(self.objects["circle5"]),
            Create(self.objects["circle6"]),
            Write(self.objects["label1"]),
            Write(self.objects["label2"]),
            Write(self.objects["label3"]),
            Write(self.objects["label4"]),
            Write(self.objects["label5"]),
            Write(self.objects["label6"]),
            run_time=3.0
        )
        remaining_3 = max(0.1, 7.536 - 1 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["equation_initial"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["equation_initial"]), run_time=1.5)
        remaining_4 = max(0.1, 5.808 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(
            Indicate(self.objects["box1"], color=RED, run_time=0.5),
            Indicate(self.objects["box2"], color=RED, run_time=0.5)
        )
        # Animate splitting circles
        # First, lift circles off the pan
        circles = self.objects["circles_group"]
        labels = VGroup(
            self.objects["label1"], self.objects["label2"], self.objects["label3"],
            self.objects["label4"], self.objects["label5"], self.objects["label6"]
        )
        self.play(
            circles.animate.shift(UP * 0.5),
            labels.animate.shift(UP * 0.5),
            run_time=1.0
        )
        # Separate into two groups
        group1 = VGroup(circles[0], circles[2], circles[4])
        group2 = VGroup(circles[1], circles[3], circles[5])
        label_group1 = VGroup(labels[0], labels[2], labels[4])
        label_group2 = VGroup(labels[1], labels[3], labels[5])
        self.play(
            group1.animate.move_to(self.objects["group1_circles"].get_center()),
            group2.animate.move_to(self.objects["group2_circles"].get_center()),
            label_group1.animate.move_to(self.objects["group1_circles"].get_center()),
            label_group2.animate.move_to(self.objects["group2_circles"].get_center()),
            run_time=2.0
        )
        remaining_5 = max(0.1, 9.84 - 0.5 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(
            Circumscribe(self.objects["group1_circles"], color=GREEN, run_time=0.5),
            Circumscribe(self.objects["group2_circles"], color=GREEN, run_time=0.5)
        )
        self.play(
            ReplacementTransform(
                self.objects["equation_initial"],
                self.objects["equation_final"]
            ),
            run_time=1.5
        )
        remaining_6 = max(0.1, 6.744 - 0.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["equation_final"], color=GREEN, run_time=1))
        remaining_7 = max(0.1, 6.12 - 1 + 0.5)
        self.wait(max(0.1, remaining_7))