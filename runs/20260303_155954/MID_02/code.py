'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the ratio 2:5 using a tape diagram, showing the whole mixture partitioned into 7 equal parts, then grouping into milk (2 parts) and water (5 parts).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for tape diagram
#    - Footer Region: [Bottom y=-3.5] for ratio text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for division lines and colored rectangles to manage them as single units. Labels placed above with buff. Ensure ratio text at bottom does not overlap diagram.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/tape_diagram_milk_water/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create tape outline (whole).
#    - Step 2: Draw 6 division lines to create 7 equal parts.
#    - Step 3: Highlight first two parts as milk (fill + label).
#    - Step 4: Highlight remaining five parts as water (fill + label).
#    - Step 5: Write descriptive ratio at bottom.
#    - Step 6: Transform descriptive ratio into symbolic ratio.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors
        title_anchor = 3.5 * UP
        tape_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan
        # title
        title = Text("Tape Diagram: Milk and Water Mixture", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # tape_outline
        tape_outline = Rectangle(width=7.0, height=1.0, color=WHITE, stroke_width=3)
        tape_outline.move_to(tape_center)
        self.objects["tape_outline"] = tape_outline

        # division lines (positions relative to tape_center)
        div_line_1 = Line(UP*0.5, DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_1.move_to(tape_center + LEFT*2.5)
        self.objects["div_line_1"] = div_line_1

        div_line_2 = Line(UP*0.5, DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_2.move_to(tape_center + LEFT*1.5)
        self.objects["div_line_2"] = div_line_2

        div_line_3 = Line(UP*0.5, DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_3.move_to(tape_center + LEFT*0.5)
        self.objects["div_line_3"] = div_line_3

        div_line_4 = Line(UP*0.5, DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_4.move_to(tape_center + RIGHT*0.5)
        self.objects["div_line_4"] = div_line_4

        div_line_5 = Line(UP*0.5, DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_5.move_to(tape_center + RIGHT*1.5)
        self.objects["div_line_5"] = div_line_5

        div_line_6 = Line(UP*0.5, DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_6.move_to(tape_center + RIGHT*2.5)
        self.objects["div_line_6"] = div_line_6

        # milk_rect (width=2.0, height=1.0, centered at left two sections)
        milk_rect = Rectangle(width=2.0, height=1.0, color="#ADD8E6", fill_opacity=0.3, stroke_width=0)
        milk_rect.move_to(tape_center + LEFT*2.5)
        self.objects["milk_rect"] = milk_rect

        # water_rect (width=5.0, height=1.0, centered at right five sections)
        water_rect = Rectangle(width=5.0, height=1.0, color="#E0FFFF", fill_opacity=0.3, stroke_width=0)
        water_rect.move_to(tape_center + RIGHT*1.5)
        self.objects["water_rect"] = water_rect

        # label_milk (position relative to milk_rect)
        label_milk = Text("Milk (2 parts)", color="#ADD8E6", font_size=28)
        label_milk.next_to(milk_rect, UP, buff=0.5)
        self.objects["label_milk"] = label_milk

        # label_water (position relative to water_rect)
        label_water = Text("Water (5 parts)", color="#E0FFFF", font_size=28)
        label_water.next_to(water_rect, UP, buff=0.5)
        self.objects["label_water"] = label_water

        # ratio_text_parts
        ratio_text_parts = MathTex(r"\mathrm{Milk} : \mathrm{Water} = 2\mathrm{ parts} : 5\mathrm{ parts}", color=YELLOW, font_size=32)
        ratio_text_parts.move_to(explanation_anchor)
        self.objects["ratio_text_parts"] = ratio_text_parts

        # ratio_text_symbolic
        ratio_text_symbolic = MathTex(r"\mathrm{Ratio} = 2 : 5", color=YELLOW, font_size=32)
        ratio_text_symbolic.move_to(explanation_anchor)
        self.objects["ratio_text_symbolic"] = ratio_text_symbolic

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_tape_diagra_f907f55dbb/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/tape_diagram_milk_water/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["tape_outline"]), run_time=1.5)
        remaining_1 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_tape_diagra_f907f55dbb/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/tape_diagram_milk_water/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["tape_outline"], color=YELLOW, run_time=1))
        div_lines = VGroup(
            self.objects["div_line_1"],
            self.objects["div_line_2"],
            self.objects["div_line_3"],
            self.objects["div_line_4"],
            self.objects["div_line_5"],
            self.objects["div_line_6"]
        )
        self.play(LaggedStart(*[Create(line) for line in div_lines], lag_ratio=0.2), run_time=2.5)
        remaining_2 = max(0.1, 4.0 - 1 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_tape_diagra_f907f55dbb/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/tape_diagram_milk_water/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Indicate(VGroup(self.objects["div_line_1"], self.objects["div_line_2"]), color=PINK, run_time=1))
        self.play(FadeIn(self.objects["milk_rect"]), run_time=1.0)
        self.play(Write(self.objects["label_milk"]), run_time=1.0)
        remaining_3 = max(0.1, 3.5 - 1 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_tape_diagra_f907f55dbb/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/tape_diagram_milk_water/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Indicate(VGroup(self.objects["div_line_3"], self.objects["div_line_4"], self.objects["div_line_5"], self.objects["div_line_6"]), color=PINK, run_time=1))
        self.play(FadeIn(self.objects["water_rect"]), run_time=1.0)
        self.play(Write(self.objects["label_water"]), run_time=1.0)
        remaining_4 = max(0.1, 3.5 - 1 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_tape_diagra_f907f55dbb/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/tape_diagram_milk_water/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Indicate(VGroup(self.objects["label_milk"], self.objects["label_water"]), color=ORANGE, run_time=1))
        self.play(Write(self.objects["ratio_text_parts"]), run_time=1.5)
        remaining_5 = max(0.1, 3.0 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_a_tape_diagra_f907f55dbb/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/tape_diagram_milk_water/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(ReplacementTransform(self.objects["ratio_text_parts"], self.objects["ratio_text_symbolic"]), run_time=1.5)
        remaining_6 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))