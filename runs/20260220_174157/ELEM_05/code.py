from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Integer", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Number Line
        number_line = Line(start=[-3, 0, 0], end=[3, 0, 0], color=WHITE, stroke_width=4)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # Ticks and Labels
        tick_3 = Line(start=[-3, -0.2, 0], end=[-3, 0.2, 0], color=WHITE, stroke_width=3)
        tick_3.move_to(number_line.get_start() + DOWN * 0.2)
        self.objects["tick_3"] = tick_3

        tick_4 = Line(start=[3, -0.2, 0], end=[3, 0.2, 0], color=WHITE, stroke_width=3)
        tick_4.move_to(number_line.get_end() + DOWN * 0.2)
        self.objects["tick_4"] = tick_4

        tick_35 = Line(start=[0, -0.15, 0], end=[0, 0.15, 0], color=WHITE, stroke_width=2)
        tick_35.move_to(content_center + DOWN * 0.15)
        self.objects["tick_35"] = tick_35

        label_3 = MathTex("3", color=WHITE)
        label_3.next_to(tick_3, DOWN, buff=0.3)
        self.objects["label_3"] = label_3

        label_4 = MathTex("4", color=WHITE)
        label_4.next_to(tick_4, DOWN, buff=0.3)
        self.objects["label_4"] = label_4

        label_35 = MathTex("3.5", color=YELLOW)
        label_35.next_to(tick_35, DOWN, buff=0.4)
        self.objects["label_35"] = label_35

        # Midpoint line (dashed)
        midpoint_line = DashedLine(start=[0, -0.5, 0], end=[0, 0.5, 0], color=YELLOW, stroke_width=3, dash_length=0.1)
        midpoint_line.move_to(content_center)
        self.objects["midpoint_line"] = midpoint_line

        # Point 3.7 and label
        point_37 = Dot(point=[1.2, 0, 0], radius=0.08, color=GREEN)
        self.objects["point_37"] = point_37

        label_37 = MathTex("3.7", color=GREEN)
        label_37.next_to(point_37, UP, buff=0.3)
        self.objects["label_37"] = label_37

        # Pointer (Triangle)
        pointer = Triangle(color=GREEN, fill_opacity=1, start_angle=-PI/2)
        pointer.height = 0.4
        pointer.move_to(point_37.get_center() + UP * 0.7)
        self.objects["pointer"] = pointer

        # Decision text
        decision_text = MathTex("3.7 > 3.5", color=ORANGE, font_size=36)
        decision_text.move_to(content_center + UP * 1.5)
        self.objects["decision_text"] = decision_text

        # Rounding arrow
        rounding_arrow = Arrow(start=[1.2, 0.5, 0], end=[3, 0.5, 0], color=PINK, stroke_width=4, buff=0)
        rounding_arrow.move_to(content_center)
        self.objects["rounding_arrow"] = rounding_arrow

        # Explanation text
        explanation_text = Text("Since 3.7 is to the right of 3.5, it is closer to 4.", color=GRAY_B, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["number_line"]))
        self.wait(max(0.1, max(0.1, 3.144 - 1)))

        # Step 2
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(
            Create(self.objects["tick_3"]),
            Create(self.objects["tick_4"]),
            Create(self.objects["tick_35"]),
            Write(self.objects["label_3"]),
            Write(self.objects["label_4"]),
            Write(self.objects["label_35"]),
            Create(self.objects["midpoint_line"])
        )
        self.wait(max(0.1, max(0.1, 5.448 - 1)))

        # Step 3
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action for step 3
        self.play(Indicate(self.objects["label_37"], color=GREEN))
        self.play(
            FadeIn(self.objects["point_37"]),
            Write(self.objects["label_37"]),
            FadeIn(self.objects["pointer"])
        )
        self.wait(max(0.1, max(0.1, 5.208 - 1)))

        # Step 4
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action for step 4
        self.play(Circumscribe(self.objects["decision_text"], color=ORANGE, run_time=1))
        self.play(Write(self.objects["decision_text"]))
        self.wait(max(0.1, max(0.1, 8.52 - 1)))

        # Step 5
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action for step 5
        self.play(Indicate(self.objects["rounding_arrow"], color=PINK))
        self.play(Create(self.objects["rounding_arrow"]))
        self.wait(max(0.1, max(0.1, 8.472 - 1)))

        # Step 6
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action for step 6
        self.play(Indicate(self.objects["pointer"], color=GREEN))
        # Create final pointer position
        pointer_final = Triangle(color=GREEN, fill_opacity=1, start_angle=-PI/2)
        pointer_final.height = 0.4
        pointer_final.move_to([3, 0.7, 0])
        self.play(ReplacementTransform(self.objects["pointer"], pointer_final))
        self.objects["pointer"] = pointer_final  # Update registry
        self.wait(max(0.1, max(0.1, 5.856 - 1)))

        # Step 7
        audio_file = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action for step 7
        self.play(Circumscribe(self.objects["label_4"], color=GREEN, run_time=1))
        self.play(
            FadeOut(self.objects["decision_text"]),
            FadeOut(self.objects["rounding_arrow"])
        )
        self.wait(max(0.1, max(0.1, 3.504 - 1)))