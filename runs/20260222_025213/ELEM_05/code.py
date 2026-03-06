from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        number_line_anchor = 0.5 * UP
        addition_anchor = -1.5 * UP
        explanation_anchor = -3.0 * UP

        # Create objects from layout_plan.objects
        # title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Whole Number", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # number_line
        number_line = NumberLine(
            x_range=[3, 4, 0.1],
            length=4.0,
            include_numbers=True,
            numbers_to_include=[3.0, 3.5, 4.0],
            color=GRAY_B
        )
        number_line.move_to(number_line_anchor)
        self.objects["number_line"] = number_line

        # point_3.7
        point_3_7 = Dot(radius=0.08, color=RED, z_index=2)
        point_3_7.move_to(number_line.number_to_point(3.7))
        self.objects["point_3.7"] = point_3_7

        # label_3.7
        label_3_7 = MathTex("3.7", color=RED, font_size=28)
        label_3_7.next_to(point_3_7, UP, buff=0.2)
        self.objects["label_3.7"] = label_3_7

        # segment_to_4
        segment_to_4 = Line(
            start=number_line.number_to_point(3.7),
            end=number_line.number_to_point(4.0),
            color=BLUE,
            stroke_width=4
        )
        self.objects["segment_to_4"] = segment_to_4

        # segment_to_3
        segment_to_3 = Line(
            start=number_line.number_to_point(3.7),
            end=number_line.number_to_point(3.0),
            color=GREEN,
            stroke_width=4
        )
        self.objects["segment_to_3"] = segment_to_3

        # midpoint_dot
        midpoint_dot = Dot(radius=0.08, color=YELLOW, z_index=2, fill_opacity=0.0)
        midpoint_dot.move_to(number_line.number_to_point(3.5))
        self.objects["midpoint_dot"] = midpoint_dot

        # label_3.5
        label_3_5 = MathTex("3.5", color=YELLOW, font_size=28)
        label_3_5.set_opacity(0.0)
        label_3_5.next_to(midpoint_dot, DOWN, buff=0.2)
        self.objects["label_3.5"] = label_3_5

        # midpoint_highlight_line
        midpoint_highlight_line = Line(
            start=number_line.number_to_point(3.0),
            end=number_line.number_to_point(4.0),
            color=WHITE,
            stroke_width=6
        )
        midpoint_highlight_line.set_opacity(0.0)
        self.objects["midpoint_highlight_line"] = midpoint_highlight_line

        # addition_title
        addition_title = Text("Verification by Addition:", color=GRAY_B, font_size=24)
        addition_title.move_to(addition_anchor + 0.8 * UP)
        self.objects["addition_title"] = addition_title

        # addend_3.7
        addend_3_7 = MathTex("3.7", color=WHITE, font_size=36)
        addend_3_7.move_to(addition_anchor + LEFT * 1.5 + UP * 0.5)
        self.objects["addend_3.7"] = addend_3_7

        # addend_0.3
        addend_0_3 = MathTex("+\\,0.3", color=WHITE, font_size=36)
        addend_0_3.next_to(addend_3_7, DOWN, aligned_edge=LEFT, buff=0.5)
        self.objects["addend_0.3"] = addend_0_3

        # addition_line
        addition_line = Line(start=LEFT * 1.0, end=RIGHT * 1.0, color=WHITE)
        addition_line.next_to(addend_0_3, DOWN, buff=0.2)
        self.objects["addition_line"] = addition_line

        # sum_4.0
        sum_4_0 = MathTex("4.0", color=WHITE, font_size=36)
        sum_4_0.next_to(addition_line, DOWN, buff=0.2)
        self.objects["sum_4.0"] = sum_4_0

        # step_explanation
        step_explanation = Text("Step 1: Draw the number line and plot 3.7.", color=GRAY_B, font_size=20)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["number_line"]))
        self.wait(max(0.1, max(0.1, 5.712 - 1.0)))

        # Step 2
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["point_3.7"]))
        self.play(Write(self.objects["label_3.7"]))
        self.play(Indicate(self.objects["point_3.7"], color=RED))
        self.wait(max(0.1, max(0.1, 2.88 - 2.0)))

        # Step 3
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["segment_to_4"]))
        self.wait(max(0.1, max(0.1, 6.888 - 1.0)))

        # Step 4
        # No audio path provided for step 4, check if exists with pattern
        step_num = 4
        file_index = step_num - 1
        mp3_path = f"media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_{file_index:02d}.mp3"
        wav_path = f"media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_{file_index:02d}.wav"
        if os.path.exists(mp3_path):
            self.add_sound(mp3_path)
        elif os.path.exists(wav_path):
            self.add_sound(wav_path)
        self.play(Create(self.objects["segment_to_3"]))
        self.wait(max(0.1, max(0.1, 2.0 - 1.0)))

        # Step 5
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Circumscribe the number 3.5 on the number line
        # Access the number mobject. numbers_to_include=[3.0, 3.5, 4.0], so index 1 is 3.5
        num_mobs = self.objects["number_line"].numbers
        if len(num_mobs) >= 2:
            self.play(Circumscribe(num_mobs[1], color=YELLOW, run_time=1))
        # Visual action: Transform highlight line into midpoint dot and label
        highlight_line = self.objects["midpoint_highlight_line"]
        highlight_line.set_opacity(1)
        self.play(Create(highlight_line))
        self.play(
            Transform(highlight_line, self.objects["midpoint_dot"].copy().set_fill(opacity=1)),
            Write(self.objects["label_3.5"].copy().set_opacity(1))
        )
        # Clean up the transformed line and add the actual dot and label to scene
        self.remove(highlight_line)
        self.add(self.objects["midpoint_dot"].set_fill(opacity=1))
        self.add(self.objects["label_3.5"].set_opacity(1))
        self.wait(max(0.1, max(0.1, 6.12 - 3.0)))

        # Step 6
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["point_3.7"], color=RED))
        self.play(FadeOut(self.objects["segment_to_3"]))
        # Update explanation text
        new_explanation = Text("Step 6: 3.7 is right of 3.5, so it rounds up to 4.", color=GRAY_B, font_size=20)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        self.wait(max(0.1, max(0.1, 9.264 - 3.0)))

        # Step 7
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(
            FadeOut(self.objects["segment_to_4"]),
            FadeOut(self.objects["midpoint_dot"]),
            FadeOut(self.objects["label_3.5"])
        )
        self.play(Write(self.objects["addition_title"]))
        self.play(
            Write(self.objects["addend_3.7"]),
            Write(self.objects["addend_0.3"]),
            Create(self.objects["addition_line"])
        )
        self.wait(max(0.1, max(0.1, 6.984 - 3.0)))

        # Step 8
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_07.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["addend_0.3"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["sum_4.0"]))
        self.wait(max(0.1, max(0.1, 4.032 - 2.0)))

        # Step 9
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_08.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["sum_4.0"], color=GREEN))
        final_explanation = Text("Thus, 3.7 rounds up to 4.", color=GRAY_B, font_size=20)
        final_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], final_explanation))
        self.wait(max(0.1, max(0.1, 3.264 - 2.0)))