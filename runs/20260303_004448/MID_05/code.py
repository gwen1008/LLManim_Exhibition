'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually demonstrate the relationship between circumference and diameter (C = πD) by unrolling a circle and measuring the resulting line with copies of the diameter.
# 2. Layout Strategy: Define the screen zones
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for circle and unrolled line
#    - Footer Region: [Bottom y=-3.5] for step text and final formula
# 3. Anti-Overlap Check: Use VGroups for the diameter copies and labels to keep them together. Position the unrolled line and measurement tools below the main circle to avoid clutter.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/unfolding_circumference/step_XX.mp3"
# 5. Animation Flow: Show circle and diameter -> unroll circumference -> measure with three diameters -> show extra piece -> reveal formula C = πD.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan
        # Title
        title = Text("Unfolding the Circumference: C = πD", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Circle
        circle = Circle(radius=2, color=BLUE, stroke_width=5)
        circle.move_to(content_center)
        self.objects["circle"] = circle
        
        # Diameter line
        diameter_line = Line(start=[-2,0,0], end=[2,0,0], color=RED, stroke_width=6)
        diameter_line.move_to(content_center)
        self.objects["diameter_line"] = diameter_line
        
        # Label D
        label_d = MathTex("D", color=RED)
        label_d.next_to(diameter_line, UP, buff=0.2)
        self.objects["label_d"] = label_d
        
        # Unrolled line (circumference)
        unrolled_line = Line(start=[-6.283, -2.5, 0], end=[6.283, -2.5, 0], color=GREEN, stroke_width=5)
        unrolled_line.move_to([0, -2.5, 0])
        self.objects["unrolled_line"] = unrolled_line
        
        # Diameter copies for measurement
        d_copy_1 = Line(start=[-6.283, -3.5, 0], end=[-2.283, -3.5, 0], color=YELLOW, stroke_width=6)
        d_copy_1.move_to([-4.283, -3.5, 0])
        self.objects["d_copy_1"] = d_copy_1
        
        d_copy_2 = Line(start=[-2.283, -3.5, 0], end=[1.717, -3.5, 0], color=YELLOW, stroke_width=6)
        d_copy_2.move_to([-0.283, -3.5, 0])
        self.objects["d_copy_2"] = d_copy_2
        
        d_copy_3 = Line(start=[1.717, -3.5, 0], end=[5.717, -3.5, 0], color=YELLOW, stroke_width=6)
        d_copy_3.move_to([3.717, -3.5, 0])
        self.objects["d_copy_3"] = d_copy_3
        
        # Extra piece
        extra_piece = Line(start=[5.717, -3.5, 0], end=[6.283, -3.5, 0], color=PINK, stroke_width=6)
        extra_piece.move_to([6.0, -3.5, 0])
        self.objects["extra_piece"] = extra_piece
        
        # Label 3D
        label_3d = MathTex("3D", color=YELLOW)
        label_3d.next_to(d_copy_2, DOWN, buff=0.3)
        self.objects["label_3d"] = label_3d
        
        # Label extra
        label_extra = MathTex(r"\approx 0.14D", color=PINK)
        label_extra.next_to(extra_piece, DOWN, buff=0.3)
        self.objects["label_extra"] = label_extra
        
        # Step text (initial)
        step_text = Text("Step 1: Present the circle and its diameter D.", color=GRAY_C, font_size=24)
        step_text.move_to(footer_anchor)
        self.objects["step_text"] = step_text
        
        # Final formula
        final_formula = MathTex(r"C = \pi D", color=WHITE, font_size=36)
        final_formula.move_to(footer_anchor + DOWN*0.7)
        self.objects["final_formula"] = final_formula
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        audio_step1 = "media/audio/unfolding_circumference/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["diameter_line"], color=RED, run_time=1))
        self.play(Create(self.objects["circle"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # Step 2
        audio_step2 = "media/audio/unfolding_circumference/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        step_text_2 = Text("Step 2: Unfold the circumference into a straight line.", color=GRAY_C, font_size=24)
        step_text_2.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], step_text_2))
        self.objects["step_text"] = step_text_2
        remaining_2 = max(0.1, 1.5 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # Step 3
        audio_step3 = "media/audio/unfolding_circumference/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["unrolled_line"], color=GREEN, run_time=1))
        # Simpler alternative: FadeOut circle and Create unrolled_line simultaneously
        self.play(FadeOut(self.objects["circle"]), Create(self.objects["unrolled_line"]), run_time=2.0)
        remaining_3 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # Step 4
        audio_step4 = "media/audio/unfolding_circumference/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["d_copy_1"]), run_time=1.0)
        step_text_4 = Text("Step 3: Measure the line using the diameter D.", color=GRAY_C, font_size=24)
        step_text_4.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], step_text_4))
        self.objects["step_text"] = step_text_4
        remaining_4 = max(0.1, 3.0 - 1.0 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # Step 5
        audio_step5 = "media/audio/unfolding_circumference/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["label_3d"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["d_copy_2"]), Create(self.objects["d_copy_3"]), run_time=2.0)
        remaining_5 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Step 6
        audio_step6 = "media/audio/unfolding_circumference/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["extra_piece"], color=PINK, run_time=1))
        self.play(Create(self.objects["extra_piece"]), run_time=1.5)
        remaining_6 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Step 7
        audio_step7 = "media/audio/unfolding_circumference/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["final_formula"]), run_time=1.5)
        step_text_7 = Text("Conclusion: The circumference is pi times the diameter.", color=GRAY_C, font_size=24)
        step_text_7.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], step_text_7))
        self.objects["step_text"] = step_text_7
        remaining_7 = max(0.1, 4.0 - 1.5 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # Step 8
        audio_step8 = "media/audio/unfolding_circumference/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["final_formula"], color=YELLOW, run_time=1))
        remaining_8 = max(0.1, 3.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_8))