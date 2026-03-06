'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize displacement on a number line, connecting the physical journey of a point to the abstract vector and the symbolic calculation 3 - (-2) = 5.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Displacement on a Number Line"
#    - Main Content: [Center y=0] for number line, dots, labels, and displacement arrow.
#    - Footer Region: [Bottom y=-3.0] for the calculation equations.
# 3. Anti-Overlap Check:
#    - Number line is centered. Dots and labels are placed relative to it.
#    - Displacement arrow is offset UP*0.2 to avoid overlapping the line.
#    - Footer equation is placed at a fixed anchor, ensuring no overlap with main content.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/On_a_number_line_ran_2578696a33/step_XX.mp3"
# 5. Animation Flow:
#    - Create number line.
#    - Mark start (A) and end (B) points.
#    - Animate a yellow dot moving from A to B.
#    - Grow displacement arrow from A to B and label it.
#    - Show and transform the calculation equation in the footer.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout plan zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.0 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Displacement on a Number Line", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # number_line
        # Note: GRAY_C is not a standard Manim color. Use GRAY_B or LIGHT_GREY? Using GRAY_B.
        number_line = NumberLine(
            x_range=[-5.5, 5.5, 1],
            length=12,
            include_numbers=True,
            color=GRAY_B
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # dot_start
        dot_start = Dot(radius=0.08, color=GREEN)
        dot_start.move_to(number_line.number_to_point(-2))
        self.objects["dot_start"] = dot_start

        # label_start
        label_start = MathTex("A(-2)", color=GREEN, font_size=24)
        label_start.next_to(dot_start, UP, buff=0.2)
        self.objects["label_start"] = label_start

        # dot_end
        dot_end = Dot(radius=0.08, color=RED)
        dot_end.move_to(number_line.number_to_point(3))
        self.objects["dot_end"] = dot_end

        # label_end
        label_end = MathTex("B(3)", color=RED, font_size=24)
        label_end.next_to(dot_end, UP, buff=0.2)
        self.objects["label_end"] = label_end

        # dot_mover
        dot_mover = Dot(radius=0.1, color=YELLOW)
        dot_mover.move_to(dot_start.get_center())
        self.objects["dot_mover"] = dot_mover

        # disp_arrow
        # Arrow start and end are defined relative to dot positions, offset UP*0.2
        arrow_start = dot_start.get_center() + UP * 0.2
        arrow_end = dot_end.get_center() + UP * 0.2
        disp_arrow = Arrow(
            start=arrow_start,
            end=arrow_end,
            color=BLUE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["disp_arrow"] = disp_arrow

        # arrow_label
        arrow_label = MathTex(r"\Delta x = 5", color=BLUE, font_size=28)
        arrow_label.next_to(disp_arrow, UP, buff=0.1)
        self.objects["arrow_label"] = arrow_label

        # calc_eq1
        calc_eq1 = MathTex(r"-2 + \, ? \, = 3", color=WHITE, font_size=36)
        calc_eq1.move_to(footer_anchor)
        self.objects["calc_eq1"] = calc_eq1

        # calc_eq2
        calc_eq2 = MathTex(r"? = 3 - (-2) = 5", color=YELLOW, font_size=36)
        calc_eq2.move_to(footer_anchor)
        self.objects["calc_eq2"] = calc_eq2

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/On_a_number_line_ran_2578696a33/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["number_line"]), run_time=2.0)
        remaining_1 = max(0.1, 11.424 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/On_a_number_line_ran_2578696a33/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["dot_start"], color=GREEN, run_time=1))
        self.play(
            Create(self.objects["dot_start"]),
            Write(self.objects["label_start"]),
            run_time=1.5
        )
        remaining_2 = max(0.1, 5.976 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/On_a_number_line_ran_2578696a33/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["dot_end"], color=RED, run_time=1))
        self.play(
            Create(self.objects["dot_end"]),
            Write(self.objects["label_end"]),
            run_time=1.5
        )
        remaining_3 = max(0.1, 3.336 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/On_a_number_line_ran_2578696a33/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["dot_mover"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["dot_mover"]), run_time=1.0)
        remaining_4 = max(0.1, 3.792 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/On_a_number_line_ran_2578696a33/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # Create a path along the number line from x=-2 to x=3
        start_point = self.objects["number_line"].number_to_point(-2)
        end_point = self.objects["number_line"].number_to_point(3)
        path = Line(start_point, end_point)
        self.play(
            MoveAlongPath(self.objects["dot_mover"], path),
            run_time=3.0
        )
        remaining_5 = max(0.1, 3.84 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/On_a_number_line_ran_2578696a33/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["disp_arrow"], color=BLUE, run_time=1))
        self.play(
            GrowFromPoint(self.objects["disp_arrow"], self.objects["dot_start"].get_center() + UP * 0.2),
            run_time=2.0
        )
        remaining_6 = max(0.1, 7.224 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/On_a_number_line_ran_2578696a33/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(Write(self.objects["arrow_label"]), run_time=1.5)
        remaining_7 = max(0.1, 6.096 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        audio_step8 = "media/audio/On_a_number_line_ran_2578696a33/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        self.play(Write(self.objects["calc_eq1"]), run_time=2.0)
        remaining_8 = max(0.1, 6.984 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        audio_step9 = "media/audio/On_a_number_line_ran_2578696a33/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["calc_eq2"], color=YELLOW, run_time=1))
        self.play(
            TransformMatchingTex(self.objects["calc_eq1"], self.objects["calc_eq2"]),
            run_time=2.0
        )
        remaining_9 = max(0.1, 5.88 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Final hold
        self.wait(max(0.1, 2))