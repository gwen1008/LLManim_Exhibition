'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing a part-to-part ratio (2:5) using a tape diagram.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for tape diagram
#    - Footer Region: [Bottom y=-3.5] for ratio caption
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for fills and labels to keep them together. Position fills behind outline using z_index.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/tape_diagram_milk_water_ratio/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show empty tape outline.
#    - Step 2: Fill milk section (2 units).
#    - Step 3: Fill water section (5 units).
#    - Step 4 & 5: Label sections.
#    - Step 6: Show final ratio caption.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_a_Manim_anima_18ef87037b/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        tape_anchor = ORIGIN
        caption_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Tape Diagram: Milk to Water Ratio", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # tape_outline
        tape_outline = Rectangle(width=7.0, height=1.0, color=WHITE, fill_opacity=0.0, stroke_width=3)
        tape_outline.move_to(tape_anchor)
        self.objects["tape_outline"] = tape_outline

        # milk_fill
        milk_fill = Rectangle(width=2.0, height=1.0, color="#D2B48C", fill_opacity=0.8, stroke_width=0)
        milk_fill.align_to(tape_outline, LEFT).align_to(tape_outline, DOWN)
        self.objects["milk_fill"] = milk_fill

        # water_fill
        water_fill = Rectangle(width=5.0, height=1.0, color="#ADD8E6", fill_opacity=0.8, stroke_width=0)
        water_fill.next_to(milk_fill, RIGHT, buff=0.0).align_to(tape_outline, DOWN)
        self.objects["water_fill"] = water_fill

        # label_milk
        label_milk = Text("Milk", color=WHITE, font_size=28)
        label_milk.next_to(milk_fill, UP, buff=0.3)
        self.objects["label_milk"] = label_milk

        # label_water
        label_water = Text("Water", color=WHITE, font_size=28)
        label_water.next_to(water_fill, UP, buff=0.3)
        self.objects["label_water"] = label_water

        # ratio_text
        ratio_text = MathTex(r"\mathrm{Milk : Water} = 2 : 5", color=YELLOW, font_size=32)
        ratio_text.move_to(caption_anchor)
        self.objects["ratio_text"] = ratio_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/tape_diagram_milk_water_ratio/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(self.objects["tape_outline"]), run_time=1.5)
        remaining_1 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/tape_diagram_milk_water_ratio/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["tape_outline"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["milk_fill"]), run_time=1.5)
        remaining_2 = max(0.1, 3.0 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/tape_diagram_milk_water_ratio/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["tape_outline"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["water_fill"]), run_time=2.0)
        remaining_3 = max(0.1, 3.5 - 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/tape_diagram_milk_water_ratio/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Write(self.objects["label_milk"]), run_time=1.0)
        remaining_4 = max(0.1, 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/tape_diagram_milk_water_ratio/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Write(self.objects["label_water"]), run_time=1.0)
        remaining_5 = max(0.1, 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/tape_diagram_milk_water_ratio/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["tape_outline"], color=GREEN, run_time=1))
        self.play(Write(self.objects["ratio_text"]), run_time=1.5)
        remaining_6 = max(0.1, 4.0 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))