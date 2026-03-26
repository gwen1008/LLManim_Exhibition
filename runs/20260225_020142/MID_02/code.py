from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on layout_plan
        title_anchor = 3.5 * UP
        content_anchor = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # Title
        title = Text("Ratio: Milk to Water", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Milk bar (final rectangle)
        milk_bar = Rectangle(width=1.6, height=1.0, color="#66B2FF", fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        milk_bar.move_to(content_anchor + LEFT * 1.2)
        milk_bar.align_to(content_anchor, DOWN)
        self.objects["milk_bar"] = milk_bar

        # Water bar (final rectangle)
        water_bar = Rectangle(width=4.0, height=1.0, color="#90EE90", fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        water_bar.next_to(milk_bar, RIGHT, buff=0.1)
        water_bar.align_to(milk_bar, DOWN)
        self.objects["water_bar"] = water_bar

        # Labels
        label_milk = Text("Milk", color="#66B2FF", font_size=32)
        label_milk.next_to(milk_bar, UP, buff=0.5)
        self.objects["label_milk"] = label_milk

        label_water = Text("Water", color="#90EE90", font_size=32)
        label_water.next_to(water_bar, UP, buff=0.5)
        self.objects["label_water"] = label_water

        label_ratio = MathTex("2 : 5", color=YELLOW, font_size=40)
        label_ratio.next_to(label_milk, UP, buff=0.8)
        label_ratio.align_to(content_anchor, UP)
        self.objects["label_ratio"] = label_ratio

        caption = Text("For every 2 parts milk, there are 5 parts water.", color=GRAY_B, font_size=32)
        caption.move_to(footer_anchor)
        self.objects["caption"] = caption

        # Create unit squares VGroups (not in layout_plan but needed for steps)
        # Milk unit squares: two squares side length 0.8, arranged horizontally
        milk_unit_sq1 = Square(side_length=0.8, color="#66B2FF", fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        milk_unit_sq2 = Square(side_length=0.8, color="#66B2FF", fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        milk_unit_vgroup = VGroup(milk_unit_sq1, milk_unit_sq2).arrange(RIGHT, buff=0)
        milk_unit_vgroup.move_to(milk_bar.get_center())
        self.objects["milk_unit_vgroup"] = milk_unit_vgroup

        # Water unit squares: five squares side length 0.8, arranged horizontally
        water_unit_squares = VGroup(*[Square(side_length=0.8, color="#90EE90", fill_opacity=0.7, stroke_color=WHITE, stroke_width=2) for _ in range(5)])
        water_unit_squares.arrange(RIGHT, buff=0)
        water_unit_squares.move_to(water_bar.get_center())
        self.objects["water_unit_vgroup"] = water_unit_squares

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/ratio_milk_to_water/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/ratio_milk_to_water/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["milk_unit_vgroup"]), run_time=2.0)
        remaining_2 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/ratio_milk_to_water/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["milk_unit_vgroup"], color=YELLOW, run_time=1))
        self.play(Transform(self.objects["milk_unit_vgroup"], self.objects["milk_bar"]), run_time=1.5)
        remaining_3 = max(0.1, 2.5 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/ratio_milk_to_water/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Create(self.objects["water_unit_vgroup"]), run_time=3.0)
        remaining_4 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/ratio_milk_to_water/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["water_unit_vgroup"], color=YELLOW, run_time=1))
        self.play(Transform(self.objects["water_unit_vgroup"], self.objects["water_bar"]), run_time=2.0)
        remaining_5 = max(0.1, 3.0 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/ratio_milk_to_water/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Write(self.objects["label_milk"]), run_time=0.8)
        self.play(Write(self.objects["label_water"]), run_time=0.8)
        self.play(Write(self.objects["label_ratio"]), run_time=1.0)
        remaining_6 = max(0.1, 4.0 - (0.8 + 0.8 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/ratio_milk_to_water/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["label_ratio"], color=GREEN, run_time=1))
        self.play(Write(self.objects["caption"]), run_time=2.0)
        remaining_7 = max(0.1, 4.0 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_7))