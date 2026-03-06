from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors (from layout_plan.anchors)
        title_anchor = 3.5 * UP
        stage1_anchor = ORIGIN
        stage2_anchor = ORIGIN
        comparison_anchor = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Unrolling a Circle to Discover Pi", font_size=40, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Circle
        circle = Circle(radius=1.5, color=BLUE, stroke_width=4)
        circle.move_to(stage1_anchor)
        self.objects["circle"] = circle

        # Diameter (Line) - geometry_def uses circle's left/right, so create after circle
        diameter = Line(circle.get_left(), circle.get_right(), color=RED, stroke_width=6)
        self.objects["diameter"] = diameter

        # Diameter Label
        diameter_label = MathTex("D", color=RED)
        diameter_label.move_to(diameter.get_center() + UP * 0.5)
        self.objects["diameter_label"] = diameter_label

        # Circumference Arc
        circumference_arc = Arc(radius=1.5, angle=2*PI, start_angle=0, color=YELLOW, stroke_width=6)
        circumference_arc.move_to(stage1_anchor)
        self.objects["circumference_arc"] = circumference_arc

        # Unrolled Line
        unrolled_line = Line(LEFT * PI * 1.5, RIGHT * PI * 1.5, color=YELLOW, stroke_width=6)
        unrolled_line.move_to(stage2_anchor)
        self.objects["unrolled_line"] = unrolled_line

        # Diameter Copy (for comparison)
        diameter_copy = Line(LEFT * 1.5, RIGHT * 1.5, color=RED, stroke_width=6)
        diameter_copy.move_to(comparison_anchor + DOWN * 1.5)
        self.objects["diameter_copy"] = diameter_copy

        # Brace for unrolled line
        brace_line = Brace(unrolled_line, UP, color=WHITE)
        brace_line.align_to(unrolled_line, UP)
        self.objects["brace_line"] = brace_line

        # Brace for diameter copy
        brace_diameter = Brace(diameter_copy, UP, color=WHITE)
        brace_diameter.align_to(diameter_copy, UP)
        self.objects["brace_diameter"] = brace_diameter

        # Label for circumference brace
        label_circ = MathTex("C", color=YELLOW)
        label_circ.next_to(brace_line, UP, buff=0.2)
        self.objects["label_circ"] = label_circ

        # Label for diameter copy brace
        label_diam_copy = MathTex("D", color=RED)
        label_diam_copy.next_to(brace_diameter, UP, buff=0.2)
        self.objects["label_diam_copy"] = label_diam_copy

        # Approximate formula
        formula_approx = MathTex(r"C \approx 3.14 \times D", font_size=36, color=GREEN)
        formula_approx.move_to(footer_anchor)
        self.objects["formula_approx"] = formula_approx

        # Exact formula
        formula_exact = MathTex(r"C = \pi D", font_size=36, color=GREEN)
        formula_exact.move_to(footer_anchor)
        self.objects["formula_exact"] = formula_exact

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["circle"]), run_time=2.0)
        remaining_1 = max(0.1, 7.032 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["diameter"], color=RED, run_time=1))
        self.play(Create(self.objects["diameter"]), Write(self.objects["diameter_label"]), run_time=1.5)
        remaining_2 = max(0.1, 3.192 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["circle"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["circumference_arc"]), run_time=2.0)
        remaining_3 = max(0.1, 6.912 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Transform(self.objects["circumference_arc"], self.objects["unrolled_line"]), run_time=3.0)
        self.objects["circumference_arc"] = self.objects["unrolled_line"]
        remaining_4 = max(0.1, 6.864 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["unrolled_line"], color=YELLOW, run_time=1))
        self.play(
            FadeOut(self.objects["circle"]),
            FadeOut(self.objects["diameter"]),
            FadeOut(self.objects["diameter_label"]),
            Create(self.objects["brace_line"]),
            Write(self.objects["label_circ"]),
            Create(self.objects["diameter_copy"]),
            Create(self.objects["brace_diameter"]),
            Write(self.objects["label_diam_copy"]),
            run_time=3.0
        )
        remaining_5 = max(0.1, 6.072 - (1 + 3.0) + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["unrolled_line"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["formula_approx"]), run_time=2.0)
        remaining_6 = max(0.1, 10.584 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(TransformMatchingTex(self.objects["formula_approx"], self.objects["formula_exact"]), run_time=3.0)
        remaining_7 = max(0.1, 7.08 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_7))