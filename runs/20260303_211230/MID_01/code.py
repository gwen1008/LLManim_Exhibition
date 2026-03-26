'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize movement on a number line from -2 to +3, connecting the concrete journey (moving dot) to the abstract vector and arithmetic calculation (3 - (-2) = 5).
# 2. Layout Strategy: Use High-Low Split.
#    - Header Region: [y=3.5] for Title "Movement on a Number Line"
#    - Main Content: [Center y=0] for number line, dots, arrow, and distance equation.
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text.
# 3. Anti-Overlap Check:
#    - Number line is centered. Dots and labels are placed relative to it.
#    - Distance label and equation occupy the same spot (UP*1.5 from center) using ReplacementTransform.
#    - Explanation text is at the bottom, away from main visuals.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/movement_on_number_line/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Title appears.
#    - Step 2: Number line drawn.
#    - Step 3: Start point (-2) appears.
#    - Step 4: End point (+3) appears.
#    - Step 5: Moving dot appears at start.
#    - Step 6: Dot animates from start to end.
#    - Step 7: Red arrow drawn along the path.
#    - Step 8: Distance label "5 units" written.
#    - Step 9: Label morphs into equation "3 - (-2) = 5".
#    - Step 10: Final emphasis.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Object Registry
        self.objects = {}

        # Create objects from layout_plan
        # Title
        title = Text("Movement on a Number Line", font_size=48, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Number Line
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=12,
            include_numbers=True,
            include_ticks=True,
            color=GRAY_B  # GRAY_C -> GRAY_B
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # Start Point (-2)
        start_point = Dot(radius=0.1, color=YELLOW, fill_opacity=1.0)
        start_point.move_to(number_line.n2p(-2))
        self.objects["start_point"] = start_point

        start_label = MathTex("-2", color=YELLOW)
        start_label.next_to(start_point, UP, buff=0.2)
        self.objects["start_label"] = start_label

        # End Point (+3)
        end_point = Dot(radius=0.1, color=GREEN, fill_opacity=1.0)
        end_point.move_to(number_line.n2p(3))
        self.objects["end_point"] = end_point

        end_label = MathTex("+3", color=GREEN)
        end_label.next_to(end_point, UP, buff=0.2)
        self.objects["end_label"] = end_label

        # Moving Dot
        moving_dot = Dot(radius=0.08, color=BLUE, fill_opacity=1.0)
        moving_dot.move_to(start_point.get_center())
        self.objects["moving_dot"] = moving_dot

        # Movement Arrow (created later, but define geometry)
        movement_arrow = Arrow(
            start=start_point.get_center(),
            end=end_point.get_center(),
            color=RED,
            stroke_width=6,
            buff=0
        )
        self.objects["movement_arrow"] = movement_arrow

        # Distance Label and Final Equation (occupy same spot)
        distance_label_step = MathTex(r"5\mathrm{ units}", color=TEAL)
        distance_label_step.move_to(content_center + UP * 1.5)
        self.objects["distance_label_step"] = distance_label_step

        distance_eq_final = MathTex("3 - (-2) = 5", color=TEAL)
        distance_eq_final.move_to(content_center + UP * 1.5)
        self.objects["distance_eq_final"] = distance_eq_final

        # Step Explanation Text
        step_explanation = Text(
            "We begin with a number line from -5 to 5.",
            font_size=36,
            color=GRAY_B  # GRAY_C -> GRAY_B
        )
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/On_a_number_line_fro_9f7d629837/step_00.mp3")  # [auto-injected]
        # Step 1: Title
        audio_step1 = "media/audio/movement_on_number_line/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Write(title), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/On_a_number_line_fro_9f7d629837/step_01.mp3")  # [auto-injected]
        # Step 2: Number Line
        audio_step2 = "media/audio/movement_on_number_line/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Indicate(number_line, color=WHITE, run_time=1))
        self.play(Create(number_line), run_time=2.0)
        remaining_2 = max(0.1, 3.0 - 2.0 - 1.0 + 0.5)  # Indicate (1s) + Create (2s)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/On_a_number_line_fro_9f7d629837/step_02.mp3")  # [auto-injected]
        # Step 3: Start Point
        audio_step3 = "media/audio/movement_on_number_line/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Circumscribe(start_point, color=YELLOW, run_time=1))
        self.play(Create(start_point), Write(start_label), run_time=1.5)
        remaining_3 = max(0.1, 2.5 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/On_a_number_line_fro_9f7d629837/step_03.mp3")  # [auto-injected]
        # Step 4: End Point
        audio_step4 = "media/audio/movement_on_number_line/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Circumscribe(end_point, color=GREEN, run_time=1))
        self.play(Create(end_point), Write(end_label), run_time=1.5)
        remaining_4 = max(0.1, 2.5 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/On_a_number_line_fro_9f7d629837/step_04.mp3")  # [auto-injected]
        # Step 5: Moving Dot appears
        audio_step5 = "media/audio/movement_on_number_line/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Indicate(moving_dot, color=BLUE, run_time=1))
        self.play(Create(moving_dot), run_time=0.5)
        remaining_5 = max(0.1, 1.5 - 0.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/On_a_number_line_fro_9f7d629837/step_05.mp3")  # [auto-injected]
        # Step 6: Dot moves from start to end
        audio_step6 = "media/audio/movement_on_number_line/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(moving_dot.animate.move_to(end_point.get_center()), run_time=3.0, rate_func=smooth)
        remaining_6 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/On_a_number_line_fro_9f7d629837/step_06.mp3")  # [auto-injected]
        # Step 7: Draw the red arrow
        audio_step7 = "media/audio/movement_on_number_line/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(Create(movement_arrow.set_color(RED)), run_time=1.5)
        remaining_7 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/On_a_number_line_fro_9f7d629837/step_07.mp3")  # [auto-injected]
        # Step 8: Write distance label "5 units"
        audio_step8 = "media/audio/movement_on_number_line/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        self.play(Indicate(distance_label_step, color=TEAL, run_time=1))
        self.play(Write(distance_label_step), run_time=1.5)
        remaining_8 = max(0.1, 2.5 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/On_a_number_line_fro_9f7d629837/step_08.mp3")  # [auto-injected]
        # Step 9: Morph into full equation
        audio_step9 = "media/audio/movement_on_number_line/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(Circumscribe(end_label, color=GREEN, run_time=1))
        self.play(TransformMatchingTex(distance_label_step, distance_eq_final), run_time=2.0)
        remaining_9 = max(0.1, 4.0 - 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/On_a_number_line_fro_9f7d629837/step_09.mp3")  # [auto-injected]
        # Step 10: Final emphasis
        audio_step10 = "media/audio/movement_on_number_line/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        self.play(Indicate(distance_eq_final, color=YELLOW, run_time=1))
        remaining_10 = max(0.1, 3.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_10))