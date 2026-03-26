from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors
        title_anchor = 3.5 * UP
        tape_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title_text
        title_text = Text("Tape Diagram for a Mixture", color=WHITE, font_size=36)
        title_text.move_to(title_anchor + UP*0.2)
        self.objects["title_text"] = title_text

        # tape_outline (Polygon from vertices)
        tape_vertices = [
            np.array([-3.5, -0.75, 0]),
            np.array([3.5, -0.75, 0]),
            np.array([3.5, 0.75, 0]),
            np.array([-3.5, 0.75, 0])
        ]
        tape_outline = Polygon(*tape_vertices, color=WHITE, stroke_width=3)
        tape_outline.move_to(tape_anchor)
        self.objects["tape_outline"] = tape_outline

        # Division lines (6 lines) - aligned with tape_outline
        # Get left edge position from tape_outline
        left_edge = tape_outline.get_left()[0]
        tape_width = 7.0  # from -3.5 to 3.5
        section_width = tape_width / 7
        
        div_line_1 = Line(start=[left_edge + section_width, -0.75, 0], end=[left_edge + section_width, 0.75, 0], color=WHITE, stroke_width=2)
        div_line_1.move_to(tape_anchor + LEFT*(3.5 - section_width))
        self.objects["div_line_1"] = div_line_1

        div_line_2 = Line(start=[left_edge + 2*section_width, -0.75, 0], end=[left_edge + 2*section_width, 0.75, 0], color=WHITE, stroke_width=2)
        div_line_2.move_to(tape_anchor + LEFT*(3.5 - 2*section_width))
        self.objects["div_line_2"] = div_line_2

        div_line_3 = Line(start=[left_edge + 3*section_width, -0.75, 0], end=[left_edge + 3*section_width, 0.75, 0], color=WHITE, stroke_width=2)
        div_line_3.move_to(tape_anchor + LEFT*(3.5 - 3*section_width))
        self.objects["div_line_3"] = div_line_3

        div_line_4 = Line(start=[left_edge + 4*section_width, -0.75, 0], end=[left_edge + 4*section_width, 0.75, 0], color=WHITE, stroke_width=2)
        div_line_4.move_to(tape_anchor + LEFT*(3.5 - 4*section_width))
        self.objects["div_line_4"] = div_line_4

        div_line_5 = Line(start=[left_edge + 5*section_width, -0.75, 0], end=[left_edge + 5*section_width, 0.75, 0], color=WHITE, stroke_width=2)
        div_line_5.move_to(tape_anchor + LEFT*(3.5 - 5*section_width))
        self.objects["div_line_5"] = div_line_5

        div_line_6 = Line(start=[left_edge + 6*section_width, -0.75, 0], end=[left_edge + 6*section_width, 0.75, 0], color=WHITE, stroke_width=2)
        div_line_6.move_to(tape_anchor + LEFT*(3.5 - 6*section_width))
        self.objects["div_line_6"] = div_line_6

        # milk_fill (VGroup of two rectangles for sections 1 & 2)
        milk_rect1 = Rectangle(width=1.0, height=1.5, color="#D4A76A", fill_opacity=0.6, stroke_width=0)
        milk_rect1.move_to(tape_anchor + LEFT*3.0)  # Center of first section
        milk_rect2 = Rectangle(width=1.0, height=1.5, color="#D4A76A", fill_opacity=0.6, stroke_width=0)
        milk_rect2.move_to(tape_anchor + LEFT*2.0)  # Center of second section
        milk_fill = VGroup(milk_rect1, milk_rect2)
        self.objects["milk_fill"] = milk_fill

        # water_fill (VGroup of five rectangles for sections 3-7)
        water_rects = []
        for i in range(5):
            rect = Rectangle(width=1.0, height=1.5, color="#88CCEE", fill_opacity=0.6, stroke_width=0)
            rect.move_to(tape_anchor + LEFT*1.0 + RIGHT*i*1.0)  # Centers at sections 3,4,5,6,7
            water_rects.append(rect)
        water_fill = VGroup(*water_rects)
        self.objects["water_fill"] = water_fill

        # Section labels (1-7)
        # First, compute bottom-left corner of tape for reference
        tape_corner_dl = tape_outline.get_corner(DL)
        label_section_1 = MathTex("1", color=GRAY_B, font_size=24)
        label_section_1.next_to(tape_corner_dl + RIGHT*0.5, DOWN, buff=0.5)
        self.objects["label_section_1"] = label_section_1

        label_section_2 = MathTex("2", color=GRAY_B, font_size=24)
        label_section_2.next_to(label_section_1, RIGHT, buff=1.0)
        self.objects["label_section_2"] = label_section_2

        label_section_3 = MathTex("3", color=GRAY_B, font_size=24)
        label_section_3.next_to(label_section_2, RIGHT, buff=1.0)
        self.objects["label_section_3"] = label_section_3

        label_section_4 = MathTex("4", color=GRAY_B, font_size=24)
        label_section_4.next_to(label_section_3, RIGHT, buff=1.0)
        self.objects["label_section_4"] = label_section_4

        label_section_5 = MathTex("5", color=GRAY_B, font_size=24)
        label_section_5.next_to(label_section_4, RIGHT, buff=1.0)
        self.objects["label_section_5"] = label_section_5

        label_section_6 = MathTex("6", color=GRAY_B, font_size=24)
        label_section_6.next_to(label_section_5, RIGHT, buff=1.0)
        self.objects["label_section_6"] = label_section_6

        label_section_7 = MathTex("7", color=GRAY_B, font_size=24)
        label_section_7.next_to(label_section_6, RIGHT, buff=1.0)
        self.objects["label_section_7"] = label_section_7

        # Labels for milk and water
        label_milk = Text("Milk (2 parts)", color="#D4A76A", font_size=28)
        label_milk.move_to(tape_anchor + UP*1.2 + LEFT*2.0)
        self.objects["label_milk"] = label_milk

        label_water = Text("Water (5 parts)", color="#88CCEE", font_size=28)
        label_water.move_to(tape_anchor + UP*1.2 + RIGHT*1.0)
        self.objects["label_water"] = label_water

        # Final ratio statement
        ratio_tex = MathTex(r"\text{Milk : Water} = 2 : 5", color=YELLOW, font_size=32)
        ratio_tex.move_to(title_anchor + DOWN*1.2)
        self.objects["ratio_tex"] = ratio_tex

        # Step explanation placeholder (will be updated each step)
        step_explanation = Text("", color=GRAY_B, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/Create_a_tape_diagra_49f8761d10/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(title_text), run_time=1.5)
        self.play(Create(tape_outline), run_time=2.0)
        remaining_1 = max(0.1, 6.096 - 1.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/Create_a_tape_diagra_49f8761d10/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(tape_outline, color=YELLOW, run_time=1))
        # Create division lines sequentially
        self.play(Create(div_line_1), run_time=0.5)
        self.play(Create(div_line_2), run_time=0.5)
        self.play(Create(div_line_3), run_time=0.5)
        self.play(Create(div_line_4), run_time=0.5)
        self.play(Create(div_line_5), run_time=0.5)
        self.play(Create(div_line_6), run_time=0.5)
        anim_time_step2 = 1 + 0.5*6
        remaining_2 = max(0.1, 6.816 - anim_time_step2 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/Create_a_tape_diagra_49f8761d10/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Circumscribe(VGroup(label_section_1, label_section_2), color=YELLOW, run_time=1))
        self.play(FadeIn(milk_fill), run_time=1.5)
        self.play(Write(label_section_1), Write(label_section_2), run_time=1.0)
        anim_time_step3 = 1 + 1.5 + 1.0
        remaining_3 = max(0.1, 7.008 - anim_time_step3 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/Create_a_tape_diagra_49f8761d10/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Circumscribe(VGroup(label_section_3, label_section_4, label_section_5, label_section_6, label_section_7), color=YELLOW, run_time=1))
        self.play(FadeIn(water_fill), run_time=1.5)
        self.play(Write(label_section_3), Write(label_section_4), Write(label_section_5), Write(label_section_6), Write(label_section_7), run_time=1.5)
        anim_time_step4 = 1 + 1.5 + 1.5
        remaining_4 = max(0.1, 6.456 - anim_time_step4 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/Create_a_tape_diagra_49f8761d10/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Indicate(milk_fill, color=WHITE, run_time=1))
        self.play(Write(label_milk), run_time=1.5)
        anim_time_step5 = 1 + 1.5
        remaining_5 = max(0.1, 8.208 - anim_time_step5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/Create_a_tape_diagra_49f8761d10/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Indicate(label_water, color=WHITE, run_time=1))
        self.play(Write(label_water), run_time=1.5)
        self.play(Write(ratio_tex), run_time=1.5)
        anim_time_step6 = 1 + 1.5 + 1.5
        remaining_6 = max(0.1, 7.632 - anim_time_step6 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/Create_a_tape_diagra_49f8761d10/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(Circumscribe(ratio_tex, color=YELLOW, run_time=1))
        remaining_7 = max(0.1, 6.672 - 1 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Final hold
        self.wait(max(0.1, 2))