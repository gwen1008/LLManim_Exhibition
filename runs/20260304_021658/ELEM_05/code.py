'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize rounding a decimal (3.7) to the nearest whole number using a number line.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line, points, and rounding animation
#    - Footer Region: [Bottom y=-3.5] for rule explanation
# 3. Anti-Overlap Check:
#    - Strategy: Keep number line centered, place labels above/below without overlapping.
#    - Use VGroups for composite labels (e.g., "3.7" with its point).
# 4. Audio Check (CRITICAL):
#    - [ ] Have I included self.add_sound() for EVERY step?
#    - [ ] Files: "media/audio/rounding/step_XX.mp3" (topic_safe_name = "rounding")
# 5. Animation Flow:
#    - Step 1: Create number line from 3 to 4.
#    - Step 2: Plot point 3.7 and label it.
#    - Step 3: Highlight midpoint 3.5 and explain rule.
#    - Step 4: Animate rounding: arrow from 3.7 to 4.
#    - Step 5: Show final result with text annotation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create Title
        title = Text("四捨五入：3.7 取整數", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.objects["title"] = title

        # Create Number Line from 3 to 4
        number_line = NumberLine(
            x_range=[3, 4, 0.1],
            length=8,
            include_numbers=True,
            numbers_with_elongated_ticks=[3, 3.5, 4],
            include_tip=True,
            tip_width=0.2,
            tip_height=0.2,
        )
        number_line.move_to(ORIGIN)
        self.objects["number_line"] = number_line

        # Create tick and label for midpoint 3.5
        midpoint_tick = Line(UP * 0.1, DOWN * 0.1, color=YELLOW)
        midpoint_tick.move_to(number_line.n2p(3.5))
        midpoint_label = MathTex("3.5", color=YELLOW, font_size=36)
        midpoint_label.next_to(midpoint_tick, DOWN, buff=0.2)
        self.objects["midpoint_tick"] = midpoint_tick
        self.objects["midpoint_label"] = midpoint_label

        # Create point and label for 3.7
        point_37 = Dot(color=BLUE, radius=0.08)
        point_37.move_to(number_line.n2p(3.7))
        label_37 = MathTex("3.7", color=BLUE, font_size=36)
        label_37.next_to(point_37, UP, buff=0.2)
        self.objects["point_37"] = point_37
        self.objects["label_37"] = label_37

        # Create point and label for 4 (target)
        point_4 = Dot(color=GREEN, radius=0.08)
        point_4.move_to(number_line.n2p(4))
        label_4 = MathTex("4", color=GREEN, font_size=36)
        label_4.next_to(point_4, UP, buff=0.2)
        self.objects["point_4"] = point_4
        self.objects["label_4"] = label_4

        # Create arrow for rounding animation
        rounding_arrow = Arrow(
            start=point_37.get_center(),
            end=point_4.get_center(),
            color=RED,
            buff=0.1,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["rounding_arrow"] = rounding_arrow

        # Create rule explanation text (footer)
        rule_text = Text("規則：大於或等於中點 (3.5) 則進位", font_size=32, color=YELLOW)
        rule_text.to_edge(DOWN, buff=0.5)
        self.objects["rule_text"] = rule_text

        # Create final result annotation
        result_text = Text("3.7 四捨五入後是 4", font_size=40, color=GREEN)
        result_text.next_to(rule_text, UP, buff=0.3)
        self.objects["result_text"] = result_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1: Show number line ==========
        audio_step1 = "media/audio/rounding/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Create(self.objects["number_line"]), run_time=2.0)
        remaining_1 = max(0.1, 4.0 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2: Plot 3.7 ==========
        audio_step2 = "media/audio/rounding/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Create(self.objects["point_37"]), run_time=1.0)
        self.play(Write(self.objects["label_37"]), run_time=1.0)
        remaining_2 = max(0.1, 3.0 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3: Highlight midpoint 3.5 and explain rule ==========
        audio_step3 = "media/audio/rounding/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Indicate the midpoint region
        self.play(
            Circumscribe(
                VGroup(self.objects["midpoint_tick"], self.objects["midpoint_label"]),
                color=YELLOW,
                run_time=1.5
            )
        )
        self.play(
            Create(self.objects["midpoint_tick"]),
            Write(self.objects["midpoint_label"]),
            run_time=1.5
        )
        self.play(Write(self.objects["rule_text"]), run_time=1.5)
        remaining_3 = max(0.1, 5.0 - 1.5 - 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4: Animate rounding (arrow from 3.7 to 4) ==========
        audio_step4 = "media/audio/rounding/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Indicate 3.7 before moving
        self.play(Indicate(self.objects["point_37"], color=BLUE, run_time=1.0))
        self.play(Create(self.objects["rounding_arrow"]), run_time=1.5)
        self.play(
            self.objects["point_37"].animate.move_to(self.objects["point_4"].get_center()),
            run_time=1.5
        )
        self.play(FadeOut(self.objects["rounding_arrow"]), run_time=0.5)
        remaining_4 = max(0.1, 4.0 - 1.0 - 1.5 - 1.5 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5: Show final result ==========
        audio_step5 = "media/audio/rounding/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(
            Create(self.objects["point_4"]),
            Write(self.objects["label_4"]),
            run_time=1.5
        )
        self.play(Write(self.objects["result_text"]), run_time=1.5)
        remaining_5 = max(0.1, 4.0 - 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2.0))