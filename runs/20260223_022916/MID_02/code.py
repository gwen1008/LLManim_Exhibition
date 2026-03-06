from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        tape_anchor = ORIGIN
        summary_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Tape Diagram: Ratio of Milk to Water", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Tape Outline
        tape_outline = Rectangle(width=7.0, height=1.0, color=WHITE, fill_opacity=0.0, stroke_width=3)
        tape_outline.move_to(tape_anchor)
        self.objects["tape_outline"] = tape_outline

        # Dividers
        # Divider positions are relative to tape_anchor: LEFT*2.5, LEFT*1.5, LEFT*0.5, RIGHT*0.5, RIGHT*1.5, RIGHT*2.5
        divider_positions = [
            2.5 * LEFT,
            1.5 * LEFT,
            0.5 * LEFT,
            0.5 * RIGHT,
            1.5 * RIGHT,
            2.5 * RIGHT
        ]
        dividers = VGroup()
        for pos in divider_positions:
            line = Line(start=0.5 * UP, end=0.5 * DOWN, color=WHITE, stroke_width=2)
            line.move_to(tape_anchor + pos)
            dividers.add(line)
        # Store individual dividers by ID as per JSON
        for i, div in enumerate(dividers, start=1):
            self.objects[f"divider_{i}"] = div

        # Milk Section Fill
        milk_section_fill = Rectangle(width=2.0, height=1.0, color="#D2B48C", fill_opacity=0.7, stroke_width=0)
        # Position: tape_anchor + LEFT*2.5 + RIGHT*0.5 = tape_anchor + 2.0*LEFT
        milk_section_fill.move_to(tape_anchor + 2.0 * LEFT)
        self.objects["milk_section_fill"] = milk_section_fill

        # Water Section Fill
        water_section_fill = Rectangle(width=5.0, height=1.0, color="#87CEEB", fill_opacity=0.7, stroke_width=0)
        # Position: tape_anchor + RIGHT*2.5 + LEFT*2.5 = tape_anchor + ORIGIN (center)
        water_section_fill.move_to(tape_anchor)
        self.objects["water_section_fill"] = water_section_fill

        # Labels
        label_milk = Text("milk", color="#D2B48C", font_size=28)
        label_milk.move_to(milk_section_fill.get_top() + UP*0.3)
        self.objects["label_milk"] = label_milk

        label_water = Text("water", color="#87CEEB", font_size=28)
        label_water.move_to(water_section_fill.get_top() + UP*0.3)
        self.objects["label_water"] = label_water

        # Ratio Summary
        ratio_summary = Tex(r"Milk : Water = 2 : 5", color=YELLOW, font_size=36)
        ratio_summary.next_to(tape_anchor, DOWN, buff=1.0)
        self.objects["ratio_summary"] = ratio_summary

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(self.objects["tape_outline"]), run_time=2.0)
        remaining_1 = max(0.1, 4.44 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["tape_outline"], color=YELLOW, run_time=1))
        self.play(Create(dividers), run_time=2.0)
        remaining_2 = max(0.1, 3.576 - 3.0 + 0.5)  # Indicate (1s) + Create dividers (2s)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["milk_section_fill"], color=YELLOW, run_time=1))
        self.play(FadeIn(self.objects["milk_section_fill"]), run_time=1.0)
        remaining_3 = max(0.1, 1.92 - 2.0 + 0.5)  # Circumscribe (1s) + FadeIn (1s)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["water_section_fill"], color=YELLOW, run_time=1))
        self.play(FadeIn(self.objects["water_section_fill"]), run_time=2.0)
        remaining_4 = max(0.1, 3.0 - 3.0 + 0.5)  # Circumscribe (1s) + FadeIn (2s)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Write labels and ratio summary
        self.play(Write(self.objects["label_milk"]), Write(self.objects["label_water"]), Write(self.objects["ratio_summary"]), run_time=3.0)
        remaining_5 = max(0.1, 7.056 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final pause
        self.wait(max(0.1, 2))