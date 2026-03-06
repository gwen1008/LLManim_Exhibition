'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the ratio 2:5 using a tape diagram to represent a mixture of milk and water.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for the 7-unit tape diagram and labels
#    - Footer Region: [Bottom y=-3.5] for final explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for milk segments and water segments for collective animation and positioning.
#    - Labels are placed above the tape with buff, ratio below with buff.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Create_a_tape_diagra_02d952142d/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create outer tape outline.
#    - Step 2: Highlight and fill two milk segments, add milk label.
#    - Step 3: Highlight and fill five water segments, add water label.
#    - Step 4: Circumscribe milk label, write ratio notation.
#    - Step 5: Write final explanation footer.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        tape_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Tape Diagram: Milk and Water Mixture", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Tape Outline
        tape_outline = Rectangle(width=7, height=1, color=WHITE, fill_opacity=0.0, stroke_width=3)
        tape_outline.move_to(tape_center)
        self.objects["tape_outline"] = tape_outline

        # Create 7 segments using a loop for easier positioning
        segments = VGroup()
        for i in range(7):
            seg = Rectangle(width=1, height=1, stroke_width=2, fill_opacity=0.0)
            # Position each segment: start from left edge of tape (center x - 3.5) then shift right by (i + 0.5) to center of each unit
            seg.move_to(tape_center + LEFT * 3 + RIGHT * (i + 0.5))
            segments.add(seg)
            self.objects[f"segment_{i+1}"] = seg

        # Set colors for segments as per plan
        segments[0].set_color("#ADD8E6")  # Milk segment 1
        segments[1].set_color("#ADD8E6")  # Milk segment 2
        for i in range(2, 7):
            segments[i].set_color("#D3D3D3")  # Water segments 3-7

        # Labels
        label_milk = MathTex(r"\mathrm{Milk (2 parts)}", color="#ADD8E6")
        # Position above tape, aligned to left of segment_1, shifted right by 0.5 (center of first two segments)
        label_milk.next_to(tape_outline, UP, buff=0.5)
        label_milk.align_to(segments[0], LEFT).shift(RIGHT * 0.5)
        self.objects["label_milk"] = label_milk

        label_water = MathTex(r"\mathrm{Water (5 parts)}", color="#D3D3D3")
        # Position above tape, aligned to left of segment_3, shifted right by 2.0 (center of the five water segments)
        label_water.next_to(tape_outline, UP, buff=0.5)
        label_water.align_to(segments[2], LEFT).shift(RIGHT * 2.0)
        self.objects["label_water"] = label_water

        # Ratio notation
        ratio_notation = MathTex(r"\mathrm{Milk : Water} = 2 : 5", color=YELLOW)
        ratio_notation.next_to(tape_outline, DOWN, buff=0.8)
        self.objects["ratio_notation"] = ratio_notation

        # Footer text
        footer_text = Text(
            "The mixture has 2 parts milk for every 5 parts water, making 7 total parts.",
            color=GRAY_B, font_size=28
        )
        footer_text.move_to(footer_anchor)
        self.objects["footer_text"] = footer_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/Create_a_tape_diagra_02d952142d/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(title), run_time=1.5)
        self.play(Create(tape_outline), run_time=2.0)
        remaining_1 = max(0.1, 10.2 - 1.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/Create_a_tape_diagra_02d952142d/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Indicate segment_1
        self.play(Indicate(self.objects["segment_1"], color=YELLOW, run_time=1))
        # Visual action: Fill milk segments and write label
        milk_fill_anim = AnimationGroup(
            self.objects["segment_1"].animate.set_fill("#ADD8E6", 0.5),
            self.objects["segment_2"].animate.set_fill("#ADD8E6", 0.5),
            run_time=1.5
        )
        self.play(milk_fill_anim)
        self.play(Write(label_milk), run_time=1.0)
        remaining_2 = max(0.1, 5.4 - 1.0 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/Create_a_tape_diagra_02d952142d/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Indicate segment_3
        self.play(Indicate(self.objects["segment_3"], color=YELLOW, run_time=1))
        # Visual action: Fill water segments and write label
        water_fill_anim = AnimationGroup(
            self.objects["segment_3"].animate.set_fill("#D3D3D3", 0.5),
            self.objects["segment_4"].animate.set_fill("#D3D3D3", 0.5),
            self.objects["segment_5"].animate.set_fill("#D3D3D3", 0.5),
            self.objects["segment_6"].animate.set_fill("#D3D3D3", 0.5),
            self.objects["segment_7"].animate.set_fill("#D3D3D3", 0.5),
            run_time=2.0
        )
        self.play(water_fill_anim)
        self.play(Write(label_water), run_time=1.0)
        remaining_3 = max(0.1, 5.376 - 1.0 - 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/Create_a_tape_diagra_02d952142d/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Circumscribe label_milk
        self.play(Circumscribe(self.objects["label_milk"], color=YELLOW, run_time=1))
        # Visual action: Write ratio notation
        self.play(Write(ratio_notation), run_time=1.5)
        remaining_4 = max(0.1, 7.176 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/Create_a_tape_diagra_02d952142d/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # No signal action
        self.play(Write(footer_text), run_time=2.0)
        remaining_5 = max(0.1, 5.76 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))