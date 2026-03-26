from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN + 0.5 * UP  # Slightly above bottom edge
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Whole", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # number_line
        number_line = NumberLine(
            x_range=[3, 4, 0.1],
            length=6,
            include_numbers=True,
            numbers_to_include=[3, 4],
            include_tip=True,
            color=GRAY_B
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line
        
        # point_3_7
        point_3_7 = Dot(radius=0.08, color=YELLOW)
        point_3_7.move_to(content_center + RIGHT * 1.2)
        self.objects["point_3_7"] = point_3_7
        
        # label_3_7
        label_3_7 = MathTex("3.7", color=YELLOW, font_size=30)
        label_3_7.next_to(point_3_7, UP, buff=0.2)
        self.objects["label_3_7"] = label_3_7
        
        # dist_to_3_segment
        dist_to_3_segment = Line(
            start=content_center + LEFT * 3 + UP * 0.5,
            end=content_center + RIGHT * 1.2 + UP * 0.5,
            color="#FF6B6B",
            stroke_width=8
        )
        self.objects["dist_to_3_segment"] = dist_to_3_segment
        
        # dist_to_3_label
        dist_to_3_label = MathTex("0.3", color="#FF6B6B", font_size=28)
        dist_to_3_label.move_to(content_center + LEFT * 0.9 + UP * 0.9)
        self.objects["dist_to_3_label"] = dist_to_3_label
        
        # dist_to_4_segment
        dist_to_4_segment = Line(
            start=content_center + RIGHT * 1.2 + UP * 0.5,
            end=content_center + RIGHT * 3 + UP * 0.5,
            color="#4ECDC4",
            stroke_width=8
        )
        self.objects["dist_to_4_segment"] = dist_to_4_segment
        
        # dist_to_4_label
        dist_to_4_label = MathTex("0.3", color="#4ECDC4", font_size=28)
        dist_to_4_label.move_to(content_center + RIGHT * 2.1 + UP * 0.9)
        self.objects["dist_to_4_label"] = dist_to_4_label
        
        # footer_text_1
        footer_text_1 = Text("The distance from 3.7 to 3 is 0.3.", color=GRAY_B, font_size=26)
        footer_text_1.move_to(footer_anchor)
        self.objects["footer_text_1"] = footer_text_1
        
        # footer_text_2
        footer_text_2 = Text("The distance from 3.7 to 4 is 0.3.", color=GRAY_B, font_size=26)
        footer_text_2.next_to(footer_text_1, DOWN, buff=0.3)
        self.objects["footer_text_2"] = footer_text_2
        
        # footer_text_3 (initial version)
        footer_text_3 = Text("0.3 is less than 0.3, so 3.7 is closer to 4.", color=GRAY_B, font_size=26)
        footer_text_3.next_to(footer_text_2, DOWN, buff=0.3)
        self.objects["footer_text_3"] = footer_text_3
        
        # footer_text_4
        footer_text_4 = Text("Therefore, 3.7 rounds up to 4.", color=YELLOW, font_size=28)
        footer_text_4.next_to(footer_text_3, DOWN, buff=0.3)
        self.objects["footer_text_4"] = footer_text_4
        
        # Also create the transformed version of footer_text_3 for step 7
        footer_text_3_transformed = Text("0.3 is equal to 0.3. By convention, we round up.", color=GRAY_B, font_size=26)
        footer_text_3_transformed.move_to(footer_text_3.get_center())
        self.objects["footer_text_3_transformed"] = footer_text_3_transformed
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        audio_step1 = "media/audio/Create_a_number_line_fc61691ad9/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["number_line"]), run_time=2.0)
        remaining_1 = max(0.1, 5.328 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # Step 2
        audio_step2 = "media/audio/Create_a_number_line_fc61691ad9/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_3_7"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["point_3_7"]), Write(self.objects["label_3_7"]), run_time=1.5)
        remaining_2 = max(0.1, 3.648 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # Step 3
        audio_step3 = "media/audio/Create_a_number_line_fc61691ad9/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["dist_to_3_segment"], color="#FF6B6B", run_time=1))
        self.play(Create(self.objects["dist_to_3_segment"]), run_time=2.0)
        remaining_3 = max(0.1, 9.816 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # Step 4
        audio_step4 = "media/audio/Create_a_number_line_fc61691ad9/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["dist_to_3_label"], run_time=1))
        self.play(Write(self.objects["footer_text_1"]), run_time=1.0)
        remaining_4 = max(0.1, 3.672 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # Step 5
        audio_step5 = "media/audio/Create_a_number_line_fc61691ad9/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["dist_to_4_segment"], color="#4ECDC4", run_time=1))
        self.play(Create(self.objects["dist_to_4_segment"]), run_time=2.0)
        remaining_5 = max(0.1, 4.464 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Step 6
        audio_step6 = "media/audio/Create_a_number_line_fc61691ad9/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["dist_to_4_label"], run_time=1))
        self.play(Write(self.objects["footer_text_2"]), run_time=1.0)
        remaining_6 = max(0.1, 3.432 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Step 7
        audio_step7 = "media/audio/Create_a_number_line_fc61691ad9/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["dist_to_3_label"], color=WHITE, run_time=1))
        self.play(Write(self.objects["footer_text_3"]), run_time=1.5)
        # Then transform it
        self.play(ReplacementTransform(self.objects["footer_text_3"], self.objects["footer_text_3_transformed"]), run_time=2.0)
        remaining_7 = max(0.1, 12.384 - 1.0 - 1.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # Step 8
        audio_step8 = "media/audio/Create_a_number_line_fc61691ad9/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["footer_text_4"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["footer_text_4"]), run_time=1.5)
        remaining_8 = max(0.1, 3.624 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # Final hold
        self.wait(max(0.1, 2))