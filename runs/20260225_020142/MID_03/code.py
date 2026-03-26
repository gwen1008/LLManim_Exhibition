from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors from layout_plan
        title_anchor = 3.5 * UP
        fulcrum_anchor = ORIGIN
        left_pan_anchor = 3 * LEFT + 0.5 * DOWN
        right_pan_anchor = 3 * RIGHT + 0.5 * DOWN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Solving 2x = 6 with a Balance Scale", font_size=40, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # fulcrum (Triangle)
        fulcrum = Polygon(
            [0, 0.2, 0],
            [-0.15, -0.2, 0],
            [0.15, -0.2, 0],
            color=GREY,
            fill_opacity=1.0
        )
        fulcrum.move_to(fulcrum_anchor)
        self.objects["fulcrum"] = fulcrum

        # beam
        beam = Line(start=LEFT*3, end=RIGHT*3, color=GRAY_B, stroke_width=8)
        beam.move_to(fulcrum_anchor)
        self.objects["beam"] = beam

        # left_pan (VGroup: Circle + Line)
        left_pan_circle = Circle(radius=0.6, color=GREY, fill_opacity=0.2).shift(DOWN*0.1)
        left_pan_chain = Line(start=UP*0.1, end=DOWN*0.5, color=GREY)
        left_pan = VGroup(left_pan_circle, left_pan_chain)
        left_pan.move_to(3 * LEFT + 0.5 * DOWN)
        self.objects["left_pan"] = left_pan

        # right_pan (VGroup: Circle + Line)
        right_pan_circle = Circle(radius=0.6, color=GREY, fill_opacity=0.2).shift(DOWN*0.1)
        right_pan_chain = Line(start=UP*0.1, end=DOWN*0.5, color=GREY)
        right_pan = VGroup(right_pan_circle, right_pan_chain)
        right_pan.move_to(right_pan_anchor)
        self.objects["right_pan"] = right_pan

        # two_boxes_vg (VGroup of two boxes with 'x' labels)
        box1 = VGroup(
            Square(side_length=0.8, color=BLUE, fill_opacity=0.3),
            Text("x", color=WHITE, font_size=24).move_to(ORIGIN)
        )
        box2 = VGroup(
            Square(side_length=0.8, color=BLUE, fill_opacity=0.3),
            Text("x", color=WHITE, font_size=24).move_to(ORIGIN)
        )
        two_boxes_vg = VGroup(box1, box2)
        two_boxes_vg.next_to(left_pan, DOWN, buff=0).arrange(RIGHT, buff=0.3)
        self.objects["two_boxes_vg"] = two_boxes_vg

        # six_circles_vg (VGroup of six green circles)
        six_circles = [Circle(radius=0.3, color=GREEN, fill_opacity=0.5) for _ in range(6)]
        six_circles_vg = VGroup(*six_circles)
        six_circles_vg.next_to(right_pan, DOWN, buff=0)
        # Arrange in grid: 2 rows, 3 columns
        six_circles_vg.arrange_in_grid(rows=2, cols=3, buff=0.2)
        self.objects["six_circles_vg"] = six_circles_vg

        # one_box_vg (single box with 'x' label) - for final state, initially not added
        one_box = VGroup(
            Square(side_length=0.8, color=BLUE, fill_opacity=0.3),
            Text("x", color=WHITE, font_size=24).move_to(ORIGIN)
        )
        one_box_vg = VGroup(one_box)
        one_box_vg.next_to(left_pan, DOWN, buff=0)
        self.objects["one_box_vg"] = one_box_vg

        # three_circles_vg (three green circles) - for final state, initially not added
        three_circles = [Circle(radius=0.3, color=GREEN, fill_opacity=0.5) for _ in range(3)]
        three_circles_vg = VGroup(*three_circles)
        three_circles_vg.next_to(right_pan, DOWN, buff=0.3).arrange(RIGHT, buff=0.3).shift(RIGHT*0.3)
        self.objects["three_circles_vg"] = three_circles_vg

        # step_explanation
        step_explanation = Text("Initial equation: 2x = 6. The scale is balanced.", font_size=28, color=LIGHT_GRAY)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # final_equation
        final_equation = MathTex("x = 3", font_size=48, color=YELLOW)
        final_equation.move_to(explanation_anchor + 0.5 * UP)
        final_equation.set_opacity(0)  # Start invisible
        self.objects["final_equation"] = final_equation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(FadeIn(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 12.528 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Indicate two_boxes_vg
        self.play(Indicate(self.objects["two_boxes_vg"], color=BLUE, run_time=1))
        # Visual action: Create scale and weights
        self.play(
            AnimationGroup(
                Create(self.objects["fulcrum"]),
                Create(self.objects["beam"]),
                Create(self.objects["left_pan"]),
                Create(self.objects["right_pan"]),
                Write(self.objects["two_boxes_vg"]),
                Write(self.objects["six_circles_vg"]),
                Write(self.objects["step_explanation"]),
                lag_ratio=0.1
            ),
            run_time=3.0
        )
        remaining_2 = max(0.1, 12.48 - 1 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Circumscribe six_circles_vg
        self.play(Circumscribe(self.objects["six_circles_vg"], color=YELLOW, run_time=1))
        # Visual action: Transform six circles into two groups of three
        circles_list = [Circle(radius=0.3, color=GREEN, fill_opacity=0.5) for _ in range(6)]
        left_group = VGroup(*circles_list[:3]).arrange(DOWN, buff=0.2)
        right_group = VGroup(*circles_list[3:]).arrange(DOWN, buff=0.2)
        two_groups = VGroup(left_group, right_group).arrange(RIGHT, buff=0.5)
        two_groups.move_to(self.objects["six_circles_vg"].get_center())
        two_groups.next_to(self.objects["right_pan"], DOWN, buff=0)
        self.objects["six_circles_vg_target"] = two_groups

        # Update explanation text
        new_explanation = Text("Divide both sides by 2.", font_size=28, color=LIGHT_GRAY)
        new_explanation.move_to(explanation_anchor + 0.3 * UP)
        self.objects["step_explanation_target"] = new_explanation

        self.play(
            ReplacementTransform(self.objects["six_circles_vg"], two_groups),
            ReplacementTransform(self.objects["step_explanation"], new_explanation),
            run_time=2.0
        )
        # Update registry
        self.objects["six_circles_vg"] = two_groups
        self.objects["step_explanation"] = new_explanation
        remaining_3 = max(0.1, 9.12 - 1 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Indicate two_boxes_vg
        self.play(Indicate(self.objects["two_boxes_vg"], color=BLUE, run_time=1))
        # Visual action: Transform two boxes into one box, and two circle groups into one group of three
        beam = self.objects["beam"]
        beam.save_state()
        beam.rotate(0.1, about_point=fulcrum_anchor)

        self.play(
            AnimationGroup(
                ReplacementTransform(self.objects["two_boxes_vg"], self.objects["one_box_vg"]),
                ReplacementTransform(self.objects["six_circles_vg"], self.objects["three_circles_vg"]),
                Restore(beam),
                lag_ratio=0.2
            ),
            run_time=3.0
        )
        # Update registry
        self.objects["two_boxes_vg"] = self.objects["one_box_vg"]
        self.objects["six_circles_vg"] = self.objects["three_circles_vg"]
        remaining_4 = max(0.1, 11.976 - 1 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Circumscribe one_box_vg
        self.play(Circumscribe(self.objects["one_box_vg"], color=BLUE, run_time=1))
        # Visual action: Transform step_explanation into final_equation
        final_eq = self.objects["final_equation"]
        final_eq.set_opacity(1)
        self.play(
            ReplacementTransform(self.objects["step_explanation"], final_eq),
            run_time=1.5
        )
        self.objects["step_explanation"] = final_eq
        remaining_5 = max(0.1, 9.192 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))