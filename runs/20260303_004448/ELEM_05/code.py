'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the rule for rounding decimals to the nearest whole number using a number line, color-coded zones, and a midpoint.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line, zones, points, and arrow.
#    - Footer Region: [Bottom y=-3.5] for dynamic explanatory text.
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for related objects (e.g., point and its label). Position regions relative to number line coordinates using n2p. Keep explanation text scaled down at the bottom.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/rounding_on_number_line/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Title appears.
#    - Step 2: Number line drawn.
#    - Step 3: Midpoint line and label appear, label is indicated.
#    - Step 4: Color-coded rounding regions fade in, round-up region is circumscribed.
#    - Step 5: Point at 3.7 and its label appear, point is indicated.
#    - Step 6: Point is indicated again, round-up region is circumscribed.
#    - Step 7: Arrow appears at point, label 4 is indicated.
#    - Step 8: Arrow transforms to point from 3.7 to 4, point moves to 4.
#    - Step 9: Arrow, original point, and label fade out, label 4 is circumscribed.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        topic_safe_name = "rounding_on_number_line"

        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Rounding on a Number Line: 3.7 to 4", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # number_line
        number_line = NumberLine(x_range=[2.5, 4.5, 0.5], length=6, include_numbers=False, color=GRAY_C)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # label_3
        label_3 = MathTex("3", color=WHITE)
        label_3.next_to(number_line.n2p(3), DOWN, buff=0.2)
        self.objects["label_3"] = label_3

        # label_4
        label_4 = MathTex("4", color=WHITE)
        label_4.next_to(number_line.n2p(4), DOWN, buff=0.2)
        self.objects["label_4"] = label_4

        # midpoint_line
        midpoint_line = DashedLine(start=UP*0.5, end=DOWN*0.5, dash_length=0.1, color=YELLOW)
        midpoint_line.move_to(number_line.n2p(3.5))
        self.objects["midpoint_line"] = midpoint_line

        # label_3.5
        label_3_5 = MathTex("3.5", color=YELLOW, font_size=30)
        label_3_5.next_to(midpoint_line, UP, buff=0.15)
        self.objects["label_3.5"] = label_3_5

        # region_round_down
        region_round_down = Rectangle(height=1.2, width=3.0, color=RED, fill_opacity=0.15, stroke_width=0)
        region_round_down.align_to(number_line.n2p(3), LEFT)
        region_round_down.align_to(number_line, UP)
        region_round_down.shift(DOWN*0.1)
        self.objects["region_round_down"] = region_round_down

        # region_round_up
        region_round_up = Rectangle(height=1.2, width=3.0, color=GREEN, fill_opacity=0.15, stroke_width=0)
        region_round_up.align_to(number_line.n2p(3.5), LEFT)
        region_round_up.align_to(number_line, UP)
        region_round_up.shift(DOWN*0.1)
        self.objects["region_round_up"] = region_round_up

        # point_3.7
        point_3_7 = Dot(radius=0.08, color=BLUE)
        point_3_7.move_to(number_line.n2p(3.7))
        self.objects["point_3.7"] = point_3_7

        # label_point
        label_point = MathTex("3.7", color=BLUE)
        label_point.next_to(point_3_7, UP, buff=0.15)
        self.objects["label_point"] = label_point

        # rounding_arrow (start position only, end will be set in sequence)
        rounding_arrow = Arrow(start=LEFT*0.1, end=RIGHT*0.1, buff=0, color=PINK, max_tip_length_to_length_ratio=0.25)
        rounding_arrow.move_to(point_3_7.get_center()).shift(RIGHT*0.5 + UP*0.3)
        self.objects["rounding_arrow"] = rounding_arrow

        # explanation_text (initial content)
        explanation_text = Text("We begin with a number line showing the integers 3 and 4.", color=GRAY_C, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = f"media/audio/{topic_safe_name}/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = f"media/audio/{topic_safe_name}/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["number_line"]), run_time=2.0)
        remaining_2 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = f"media/audio/{topic_safe_name}/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # Signal action
        self.play(Indicate(self.objects["label_3.5"], color=YELLOW, run_time=1))
        # Visual action
        self.play(Create(self.objects["midpoint_line"]), Write(self.objects["label_3.5"]), run_time=2.0)
        remaining_3 = max(0.1, 3.0 - 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = f"media/audio/{topic_safe_name}/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # Signal action
        self.play(Circumscribe(self.objects["region_round_up"], color=GREEN, run_time=1))
        # Visual action
        self.play(FadeIn(self.objects["region_round_down"]), FadeIn(self.objects["region_round_up"]), run_time=2.0)
        remaining_4 = max(0.1, 4.0 - 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = f"media/audio/{topic_safe_name}/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # Signal action
        self.play(Indicate(self.objects["point_3.7"], color=BLUE, run_time=1))
        # Visual action
        self.play(Create(self.objects["point_3.7"]), Write(self.objects["label_point"]), run_time=1.5)
        remaining_5 = max(0.1, 2.5 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = f"media/audio/{topic_safe_name}/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # Signal action
        self.play(Circumscribe(self.objects["region_round_up"], color=GREEN, run_time=1))
        # Visual action (Indicate the point)
        self.play(Indicate(self.objects["point_3.7"], color=BLUE, run_time=1.5))
        remaining_6 = max(0.1, 3.0 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = f"media/audio/{topic_safe_name}/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # Signal action
        self.play(Indicate(self.objects["label_4"], color=WHITE, run_time=1))
        # Visual action
        self.play(Create(self.objects["rounding_arrow"]), run_time=1.0)
        remaining_7 = max(0.1, 2.0 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        audio_step8 = f"media/audio/{topic_safe_name}/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # Create target arrow from 3.7 to 4
        arrow_start = self.objects["point_3.7"].get_center()
        arrow_end = self.objects["number_line"].n2p(4)
        # Create a new arrow for the transformation
        target_arrow = Arrow(start=arrow_start, end=arrow_end, buff=0, color=PINK, max_tip_length_to_length_ratio=0.25)
        target_arrow.shift(UP*0.3) # Keep the upward shift for visual clarity
        # Also create a target point at 4
        point_at_4 = Dot(radius=0.08, color=GREEN).move_to(arrow_end)
        # Animate arrow transformation and point movement simultaneously
        self.play(
            Transform(self.objects["rounding_arrow"], target_arrow),
            Transform(self.objects["point_3.7"], point_at_4),
            run_time=2.0
        )
        remaining_8 = max(0.1, 2.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        audio_step9 = f"media/audio/{topic_safe_name}/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        # Signal action
        self.play(Circumscribe(self.objects["label_4"], color=GREEN, run_time=1))
        # Visual action
        self.play(
            FadeOut(self.objects["rounding_arrow"]),
            FadeOut(self.objects["point_3.7"]),
            FadeOut(self.objects["label_point"]),
            run_time=1.5
        )
        remaining_9 = max(0.1, 3.0 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_9))