from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        circle_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Circle Outline
        circle_outline = Circle(radius=2.0, color=WHITE, stroke_width=3)
        circle_outline.move_to(circle_center)
        self.objects["circle_outline"] = circle_outline

        # Half Sector
        half_sector = Sector(radius=2.0, angle=PI, start_angle=0, color="#1E90FF", fill_opacity=0.7, stroke_width=0)
        half_sector.move_to(circle_center)
        self.objects["half_sector"] = half_sector

        # Label Half
        label_half = MathTex(r"\frac{1}{2}", color="#1E90FF", font_size=36)
        label_half.move_to(circle_center + RIGHT * 2.5 + UP * 1.2)
        self.objects["label_half"] = label_half

        # Quarter Sectors
        quarter_sector_1 = Sector(radius=2.0, angle=PI/2, start_angle=0, color="#1E90FF", fill_opacity=0.7, stroke_width=0)
        quarter_sector_1.move_to(circle_center)
        self.objects["quarter_sector_1"] = quarter_sector_1

        quarter_sector_2 = Sector(radius=2.0, angle=PI/2, start_angle=PI/2, color="#87CEEB", fill_opacity=0.7, stroke_width=0)
        quarter_sector_2.move_to(circle_center)
        self.objects["quarter_sector_2"] = quarter_sector_2

        # Label Quarters
        label_quarters = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        label_quarters.move_to(circle_center + RIGHT * 2.5 + DOWN * 0.52)
        self.objects["label_quarters"] = label_quarters

        # Division Lines
        div_line_half = Line(start=circle_center + DOWN * 2.0, end=circle_center + UP * 2.0, color=WHITE, stroke_width=3)
        self.objects["div_line_half"] = div_line_half

        div_line_quarter_1 = Line(start=circle_center + LEFT * 2.0, end=circle_center + RIGHT * 2.0, color=WHITE, stroke_width=3)
        self.objects["div_line_quarter_1"] = div_line_quarter_1

        # Step Explanation
        step_explanation = Text("We start with a whole pizza.", color=YELLOW, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # Equality Text
        equality_text = MathTex(r"\frac{1}{2} = \frac{2}{4}", color=GREEN, font_size=42)
        equality_text.move_to(circle_center + DOWN * 3.2)
        self.objects["equality_text"] = equality_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["circle_outline"]), Write(self.objects["step_explanation"]), run_time=1.5)
        remaining_1 = max(0.1, 3.816 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.objects["step_explanation"].become(Text("Now, we cut it into two equal halves with a vertical line.", color=YELLOW, font_size=28).move_to(explanation_anchor))
        self.play(Create(self.objects["div_line_half"]), run_time=1.5)
        remaining_2 = max(0.1, 3.984 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.objects["step_explanation"].become(Text("We shade one of these halves to represent the fraction one-half.", color=YELLOW, font_size=28).move_to(explanation_anchor))
        self.play(Indicate(self.objects["half_sector"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["half_sector"]), run_time=1.5)
        remaining_3 = max(0.1, 3.552 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.objects["step_explanation"].become(Text("We label this shaded area as one-half.", color=YELLOW, font_size=28).move_to(explanation_anchor))
        self.play(Write(self.objects["label_half"]), run_time=1.0)
        remaining_4 = max(0.1, 3.168 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.objects["step_explanation"].become(Text("To find an equivalent fraction, we cut each half again, this time with a horizontal line, creating four equal quarters.", color=YELLOW, font_size=28).move_to(explanation_anchor))
        self.play(Indicate(self.objects["div_line_half"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["div_line_quarter_1"]), run_time=1.5)
        remaining_5 = max(0.1, 8.616 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.objects["step_explanation"].become(Text("The original shaded half is now composed of two quarters. Let's shade them to show this.", color=YELLOW, font_size=28).move_to(explanation_anchor))
        self.play(Circumscribe(self.objects["half_sector"], color=YELLOW, run_time=1))
        self.play(FadeOut(self.objects["half_sector"]), run_time=0.5)
        self.play(FadeIn(self.objects["quarter_sector_1"]), FadeIn(self.objects["quarter_sector_2"]), run_time=1.5)
        remaining_6 = max(0.1, 6.096 - (1 + 0.5 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.objects["step_explanation"].become(Text("We now have two shaded quarters out of four. We label this as two-fourths.", color=YELLOW, font_size=28).move_to(explanation_anchor))
        self.play(Write(self.objects["label_quarters"]), run_time=1.0)
        remaining_7 = max(0.1, 5.088 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        audio_step8 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        self.objects["step_explanation"].become(Text("Observe that the shaded area has not changed. The two shaded quarters exactly cover the same area as the original half.", color=YELLOW, font_size=28).move_to(explanation_anchor))
        self.play(Indicate(self.objects["quarter_sector_1"], color=RED, run_time=1))
        self.play(Indicate(self.objects["quarter_sector_2"], color=RED, run_time=1))
        remaining_8 = max(0.1, 8.328 - (1 + 1) + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        audio_step9 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.objects["step_explanation"].become(Text("Therefore, we can conclude that one-half is equal to two-fourths.", color=YELLOW, font_size=28).move_to(explanation_anchor))
        self.play(Write(self.objects["equality_text"]), run_time=1.5)
        remaining_9 = max(0.1, 4.656 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Final hold
        self.wait(max(0.1, 2))