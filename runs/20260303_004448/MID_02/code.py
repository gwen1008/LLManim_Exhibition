'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the ratio 2:5 using a tape diagram, showing the whole divided into 7 equal parts, then grouped and colored as 2 parts milk and 5 parts water.
# 2. Layout Strategy:
#    - Header Region: [y=3.0] for Title
#    - Main Content: [Center y=0] for tape diagram
#    - Footer Region: [Bottom y=-3.0] for ratio statement and total parts.
# 3. Anti-Overlap Check:
#    - Strategy: Center the main diagram at ORIGIN. Labels are placed above/below with buff. Use VGroups for related elements (dividers, labels).
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/tape_diagram_ratio/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show empty tape rectangle.
#    - Step 2: Indicate tape, then draw 6 dividers to create 7 sections.
#    - Step 3: Highlight milk area, fade in color and label.
#    - Step 4: Highlight water area, fade in color and label.
#    - Step 5: Indicate ratio footer, write ratio, total, and section numbers.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors
        global_center = ORIGIN
        title_anchor = 3.0 * UP
        footer_anchor = 3.0 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Tape Diagram: Milk to Water Ratio 2:5", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # tape_outer
        tape_outer = Rectangle(width=7.0, height=1.0, color=WHITE, stroke_width=3, fill_opacity=0.0)
        tape_outer.move_to(global_center)
        self.objects["tape_outer"] = tape_outer

        # Create dividers relative to tape_outer
        divider_positions = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        for i, pos in enumerate(divider_positions, start=1):
            divider = Line(start=UP*0.5, end=DOWN*0.5, color=WHITE, stroke_width=2)
            divider.move_to(tape_outer.get_left() + RIGHT * pos)
            self.objects[f"divider_{i}"] = divider

        # milk_block
        milk_block = Rectangle(width=2.0, height=1.0, color="#87CEEB", fill_opacity=0.5, stroke_opacity=0.0)
        milk_block.move_to(tape_outer.get_left() + RIGHT * 1.0)
        self.objects["milk_block"] = milk_block

        # water_block
        water_block = Rectangle(width=5.0, height=1.0, color="#E0F7FA", fill_opacity=0.5, stroke_opacity=0.0)
        water_block.move_to(tape_outer.get_left() + RIGHT * 4.5)
        self.objects["water_block"] = water_block

        # label_milk
        label_milk = Text("Milk (2 parts)", color="#87CEEB", font_size=28)
        label_milk.next_to(self.objects["milk_block"], UP, buff=0.5)
        self.objects["label_milk"] = label_milk

        # label_water
        label_water = Text("Water (5 parts)", color="#E0F7FA", font_size=28)
        label_water.next_to(self.objects["water_block"], UP, buff=0.5)
        self.objects["label_water"] = label_water

        # section labels 1-7
        section_positions = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
        for i, pos in enumerate(section_positions, start=1):
            label = MathTex(str(i), color=GRAY_C, font_size=24)
            label.next_to(tape_outer.get_left() + RIGHT * pos, DOWN, buff=0.3)
            self.objects[f"label_section_{i}"] = label

        # footer_ratio
        footer_ratio = MathTex(r"\mathrm{Ratio: Milk : Water = 2 : 5}", color=YELLOW, font_size=32)
        footer_ratio.move_to(footer_anchor + UP*0.5)
        self.objects["footer_ratio"] = footer_ratio

        # footer_total
        footer_total = MathTex(r"2 + 5 = 7 \mathrm{ total parts}", color=WHITE, font_size=28)
        footer_total.next_to(self.objects["footer_ratio"], DOWN, buff=0.3)
        self.objects["footer_total"] = footer_total

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/tape_diagram_ratio/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Create(self.objects["tape_outer"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/tape_diagram_ratio/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["tape_outer"], color=YELLOW, run_time=1))
        dividers = [self.objects[f"divider_{i}"] for i in range(1, 7)]
        self.play(LaggedStart(*[Create(d) for d in dividers], lag_ratio=0.2), run_time=2.5)
        remaining_2 = max(0.1, 3.5 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/tape_diagram_ratio/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["milk_block"], color=YELLOW, run_time=1))
        self.play(
            FadeIn(self.objects["milk_block"]),
            Write(self.objects["label_milk"]),
            run_time=2.0
        )
        remaining_3 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/tape_diagram_ratio/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["water_block"], color=YELLOW, run_time=1))
        self.play(
            FadeIn(self.objects["water_block"]),
            Write(self.objects["label_water"]),
            run_time=2.0
        )
        remaining_4 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/tape_diagram_ratio/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["footer_ratio"], color=YELLOW, run_time=1))
        section_labels = [self.objects[f"label_section_{i}"] for i in range(1, 8)]
        self.play(
            Write(self.objects["footer_ratio"]),
            Write(self.objects["footer_total"]),
            LaggedStart(*[FadeIn(label) for label in section_labels], lag_ratio=0.1),
            run_time=3.5
        )
        remaining_5 = max(0.1, 4.5 - 4.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))