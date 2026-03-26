from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Translation and Distance on a Number Line", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # number_line
        number_line = NumberLine(
            x_range=[-5.5, 5.5, 1],
            length=11,
            include_numbers=True,
            include_tip=True,
            color=GRAY_B
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # point_a and label_a
        point_a = Dot(point=[-2, 0, 0], radius=0.08, color=BLUE)
        self.objects["point_a"] = point_a
        label_a = MathTex("-2", color=BLUE, font_size=30)
        label_a.next_to(point_a, DOWN, buff=0.2)
        self.objects["label_a"] = label_a

        # point_b and label_b
        point_b = Dot(point=[3, 0, 0], radius=0.08, color=GREEN)
        self.objects["point_b"] = point_b
        label_b = MathTex("3", color=GREEN, font_size=30)
        label_b.next_to(point_b, DOWN, buff=0.2)
        self.objects["label_b"] = label_b

        # translation_arrow (initialized as zero-length at point A)
        translation_arrow = Arrow(
            start=[-2, 0, 0],
            end=[-2, 0, 0],
            color=YELLOW,
            max_tip_length_to_length_ratio=0.15,
            stroke_width=4,
            buff=0
        )
        self.objects["translation_arrow"] = translation_arrow

        # distance_line (initialized as zero-length at start position)
        distance_line = Line(
            start=[-2, 1, 0],
            end=[-2, 1, 0],
            color=RED,
            stroke_width=6
        )
        distance_line.align_to(number_line, LEFT).shift(UP)
        self.objects["distance_line"] = distance_line

        # distance_label
        distance_label = MathTex("5", color=RED, font_size=36)
        self.objects["distance_label"] = distance_label

        # step_explanation
        step_explanation = Text("Let's begin by drawing our number line.", color=GRAY_B, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(self.objects["number_line"]), Write(self.objects["step_explanation"]), run_time=2.0)
        remaining_1 = max(0.1, 4.536 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["point_a"], color=BLUE, run_time=1))
        new_explanation_2 = Text("Now, let's plot our two points: one at negative two, and another at positive three.", color=GRAY_B, font_size=28)
        new_explanation_2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_2))
        self.objects["step_explanation"] = new_explanation_2
        self.play(
            Create(self.objects["point_a"]),
            Write(self.objects["label_a"]),
            Create(self.objects["point_b"]),
            Write(self.objects["label_b"]),
            run_time=2.5
        )
        remaining_2 = max(0.1, 5.832 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["point_a"], color=YELLOW, run_time=1))
        new_explanation_3 = Text("The translation from negative two to positive three can be visualized as an arrow.", color=GRAY_B, font_size=28)
        new_explanation_3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_3))
        self.objects["step_explanation"] = new_explanation_3
        translation_arrow_final = Arrow(
            start=[-2, 0, 0],
            end=[3, 0, 0],
            color=YELLOW,
            max_tip_length_to_length_ratio=0.15,
            stroke_width=4,
            buff=0
        )
        self.play(Transform(self.objects["translation_arrow"], translation_arrow_final), run_time=3.0)
        self.objects["translation_arrow"] = translation_arrow_final
        remaining_3 = max(0.1, 8.856 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["translation_arrow"], color=RED, run_time=1))
        new_explanation_4 = Text("This arrow represents the translation vector. Its length is the distance.", color=GRAY_B, font_size=28)
        new_explanation_4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_4))
        self.objects["step_explanation"] = new_explanation_4
        distance_line_final = Line(
            start=[-2, 1, 0],
            end=[3, 1, 0],
            color=RED,
            stroke_width=6
        )
        distance_line_final.align_to(number_line, LEFT).shift(UP)
        self.play(ReplacementTransform(self.objects["translation_arrow"], distance_line_final), run_time=2.5)
        self.objects["distance_line"] = distance_line_final
        remaining_4 = max(0.1, 7.488 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["distance_line"], color=YELLOW, run_time=1))
        new_explanation_5 = Text("The length of this segment is exactly five units. This is the distance.", color=GRAY_B, font_size=28)
        new_explanation_5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_5))
        self.objects["step_explanation"] = new_explanation_5
        self.objects["distance_label"].next_to(self.objects["distance_line"], UP, buff=0.3)
        self.play(Write(self.objects["distance_label"]), run_time=1.5)
        remaining_5 = max(0.1, 9.072 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))