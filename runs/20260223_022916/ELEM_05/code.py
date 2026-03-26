from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.0 * DOWN
        
        # Create title
        title = Text("Rounding on a Number Line", font_size=40, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Create number line
        number_line = NumberLine(
            x_range=[3, 4, 1],
            length=8,
            include_numbers=True,
            color=GRAY_B
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line
        
        # Create tick dots
        tick_3 = Dot(radius=0.07, color=WHITE)
        tick_3.move_to(number_line.number_to_point(3))
        self.objects["tick_3"] = tick_3
        
        tick_4 = Dot(radius=0.07, color=WHITE)
        tick_4.move_to(number_line.number_to_point(4))
        self.objects["tick_4"] = tick_4
        
        # Create point at 3.7
        point_3_7 = Dot(radius=0.08, color=YELLOW, fill_opacity=1.0)
        point_3_7.move_to(number_line.number_to_point(3.7))
        self.objects["point_3_7"] = point_3_7
        
        # Create label for point at 3.7
        label_3_7 = MathTex("3.7", color=YELLOW)
        label_3_7.next_to(point_3_7, UP, buff=0.4)
        self.objects["label_3_7"] = label_3_7
        
        # Create segment from 3.7 to 4
        segment_to_4 = Line(
            start=number_line.number_to_point(3.7),
            end=number_line.number_to_point(4),
            color=GREEN,
            stroke_width=6
        )
        self.objects["segment_to_4"] = segment_to_4
        
        # Create segment from 3.7 to 3
        segment_to_3 = Line(
            start=number_line.number_to_point(3.7),
            end=number_line.number_to_point(3),
            color=RED,
            stroke_width=6
        )
        self.objects["segment_to_3"] = segment_to_3
        
        # Create label for segment to 4 (0.3)
        label_0_3 = MathTex("0.3", color=GREEN, font_size=30)
        label_0_3.next_to(segment_to_4, UP, buff=0.3)
        self.objects["label_0_3"] = label_0_3
        
        # Create label for segment to 3 (0.7)
        label_0_7 = MathTex("0.7", color=RED, font_size=30)
        label_0_7.next_to(segment_to_3, UP, buff=0.15)
        self.objects["label_0_7"] = label_0_7
        
        # Create inequality
        inequality = MathTex("0.7 \\geq 0.5", color=RED, font_size=36)
        inequality.next_to(point_3_7, RIGHT, buff=1.0)
        self.objects["inequality"] = inequality
        
        # Create footer text
        footer_text = Text(
            "Since 0.7 is greater than or equal to 0.5, 3.7 rounds up to 4.",
            font_size=24,
            color=BLUE_C
        )
        footer_text.move_to(footer_anchor)
        footer_text.shift(0.5 * UP)
        self.objects["footer_text"] = footer_text
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Create(self.objects["number_line"]), run_time=1.5)
        self.play(Create(self.objects["tick_3"]), Create(self.objects["tick_4"]), run_time=0.5)
        remaining_1 = max(0.1, 2.976 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_3_7"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["point_3_7"]), run_time=0.5)
        self.play(Write(self.objects["label_3_7"]), run_time=0.5)
        remaining_2 = max(0.1, 2.736 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["segment_to_4"]), run_time=1.0)
        self.play(Write(self.objects["label_0_3"]), run_time=0.5)
        self.play(Create(self.objects["segment_to_3"]), run_time=1.0)
        self.play(Write(self.objects["label_0_7"]), run_time=0.5)
        remaining_3 = max(0.1, 7.944 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["label_0_7"], color=RED, run_time=1))
        
        self.play(
            ReplacementTransform(self.objects["label_0_7"], self.objects["inequality"]),
            FadeOut(self.objects["label_0_3"]),
            FadeOut(self.objects["segment_to_4"]),
            FadeOut(self.objects["segment_to_3"]),
            run_time=2.0
        )
        remaining_4 = max(0.1, 13.488 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["inequality"], color=RED, run_time=1))
        
        # Create new label "4" at same position as current label
        label_4 = MathTex("4", color=YELLOW)
        label_4.move_to(self.objects["label_3_7"].get_center())
        
        self.play(
            Write(self.objects["footer_text"]),
            ReplacementTransform(self.objects["label_3_7"], label_4),
            self.objects["point_3_7"].animate.move_to(self.objects["tick_4"].get_center()),
            FadeOut(self.objects["inequality"]),
            run_time=2.0
        )
        remaining_5 = max(0.1, 3.624 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final pause
        self.wait(max(0.1, 2))