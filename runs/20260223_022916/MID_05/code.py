from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        circle_stage_center = 3.5 * LEFT
        line_stage_center = 3.5 * RIGHT
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Unrolling a Circle to Discover Pi (π)", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle
        circle = Circle(radius=2, color=BLUE, stroke_width=4)
        circle.move_to(circle_stage_center)
        self.objects["circle"] = circle

        # diameter_line - FIXED: align with circle center
        diameter_line = Line(start=[-5.5, 0, 0], end=[-1.5, 0, 0], color=RED, stroke_width=6)
        diameter_line.move_to(circle.get_center())
        self.objects["diameter_line"] = diameter_line

        # label_D - FIXED: increase buff to avoid overlap
        label_D = MathTex("D", color=RED)
        label_D.next_to(diameter_line, UP, buff=0.4)
        self.objects["label_D"] = label_D

        # label_C_circle
        label_C_circle = MathTex("C", color=YELLOW)
        label_C_circle.next_to(circle, UP+RIGHT, buff=0.3)
        self.objects["label_C_circle"] = label_C_circle

        # unrolled_line (final state: length = 2*PI*radius = 4*PI)
        unrolled_line_length = 2 * PI * 2
        unrolled_line_start = np.array([-1.5, 0, 0])
        unrolled_line_end = unrolled_line_start + np.array([unrolled_line_length, 0, 0])
        unrolled_line = Line(start=unrolled_line_start, end=unrolled_line_end, color=YELLOW, stroke_width=4)
        final_center = 3.5 * RIGHT
        unrolled_line.move_to(final_center)
        self.objects["unrolled_line"] = unrolled_line

        # label_C_line
        label_C_line = MathTex("C", color=YELLOW)
        label_C_line.next_to(unrolled_line, UP, buff=0.2)
        self.objects["label_C_line"] = label_C_line

        # diameter_copy_1 (length = diameter = 4)
        diam_length = 4
        diam_copy_1_start = unrolled_line.get_start() + DOWN
        diam_copy_1_end = diam_copy_1_start + np.array([diam_length, 0, 0])
        diameter_copy_1 = Line(start=diam_copy_1_start, end=diam_copy_1_end, color=RED, stroke_width=4)
        self.objects["diameter_copy_1"] = diameter_copy_1

        # diameter_copy_2
        diam_copy_2_start = diam_copy_1_end
        diam_copy_2_end = diam_copy_2_start + np.array([diam_length, 0, 0])
        diameter_copy_2 = Line(start=diam_copy_2_start, end=diam_copy_2_end, color=RED, stroke_width=4)
        self.objects["diameter_copy_2"] = diameter_copy_2

        # diameter_copy_3
        diam_copy_3_start = diam_copy_2_end
        diam_copy_3_end = diam_copy_3_start + np.array([diam_length, 0, 0])
        diameter_copy_3 = Line(start=diam_copy_3_start, end=diam_copy_3_end, color=RED, stroke_width=4)
        self.objects["diameter_copy_3"] = diameter_copy_3

        # diameter_remainder
        remainder_start = diam_copy_3_end
        remainder_end = unrolled_line.get_end() + DOWN
        diameter_remainder = Line(start=remainder_start, end=remainder_end, color=RED, stroke_width=4, stroke_opacity=0.5)
        self.objects["diameter_remainder"] = diameter_remainder

        # label_pi - FIXED: increase buff to avoid overlap with remainder
        label_pi = MathTex(r"\pi \approx 3.14", color=GREEN, font_size=36)
        label_pi.next_to(diameter_remainder, UP, buff=0.6)
        self.objects["label_pi"] = label_pi

        # final_formula - FIXED: scale to fit within frame
        final_formula = MathTex(r"C = \pi D", color=GREEN, font_size=48)
        final_formula.move_to(footer_anchor)
        final_formula.scale(0.8)
        self.objects["final_formula"] = final_formula

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title"]), run_time=1.5)
        self.play(Create(self.objects["circle"]), run_time=2.0)
        self.play(Indicate(self.objects["diameter_line"], color=RED, run_time=1))
        remaining_1 = max(0.1, 7.248 - 1.5 - 2.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["circle"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["label_C_circle"]), run_time=1.0)
        self.play(Create(self.objects["diameter_line"]), Write(self.objects["label_D"]), run_time=1.5)
        remaining_2 = max(0.1, 5.52 - 1 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # For unrolling, we create a copy of the circle's perimeter (an Arc) and transform it
        unrolling_arc = Arc(radius=2, angle=2*PI, color=YELLOW, stroke_width=4)
        unrolling_arc.move_to(self.objects["circle"].get_center())
        self.play(TransformFromCopy(self.objects["circle"], unrolling_arc), run_time=2.0)
        self.play(ReplacementTransform(unrolling_arc, self.objects["unrolled_line"]), run_time=2.0)
        self.play(Write(self.objects["label_C_line"]), run_time=0.8)
        remaining_3 = max(0.1, 6.936 - 2.0 - 2.0 - 0.8 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["diameter_line"], color=RED, run_time=1))
        self.play(Create(self.objects["diameter_copy_1"]), run_time=1.5)
        remaining_4 = max(0.1, 6.36 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Create(self.objects["diameter_copy_2"]), Create(self.objects["diameter_copy_3"]), run_time=2.0)
        remaining_5 = max(0.1, 6.216 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["diameter_remainder"], color=RED, run_time=1))
        self.play(Create(self.objects["diameter_remainder"]), Write(self.objects["label_pi"]), run_time=2.0)
        remaining_6 = max(0.1, 9.552 - 1 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["label_pi"], color=GREEN, run_time=1))
        self.play(Write(self.objects["final_formula"]), run_time=1.5)
        remaining_7 = max(0.1, 13.512 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))