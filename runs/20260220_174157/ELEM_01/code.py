from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        pizza1_anchor = 3 * LEFT
        pizza2_anchor = 3 * RIGHT
        center_anchor = ORIGIN
        footer_anchor = 3.5 * DOWN + 0.5 * UP  # Slightly above bottom edge

        # Object registry
        self.objects = {}

        # Create all objects from layout_plan.objects
        # Title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Pizza 1 (1/2)
        pizza1_circle = Circle(radius=2, color=WHITE, stroke_width=3)
        pizza1_circle.move_to(pizza1_anchor)
        self.objects["pizza1_circle"] = pizza1_circle

        pizza1_div_line = Line(LEFT*2, RIGHT*2, color=WHITE, stroke_width=2)
        pizza1_div_line.move_to(pizza1_anchor)
        self.objects["pizza1_div_line"] = pizza1_div_line

        # Note: Sector uses 'radius' not 'outer_radius' in Manim v0.19.2
        pizza1_shaded_sector = Sector(radius=2, angle=PI, start_angle=0, color="#FFD700", fill_opacity=0.8, stroke_width=0)
        pizza1_shaded_sector.move_to(pizza1_anchor)
        self.objects["pizza1_shaded_sector"] = pizza1_shaded_sector

        label_1over2 = MathTex(r"\frac{1}{2}", color=WHITE, font_size=36)
        label_1over2.move_to(pizza1_anchor)
        self.objects["label_1over2"] = label_1over2

        # Pizza 2 (2/4)
        pizza2_circle = Circle(radius=2, color=WHITE, stroke_width=3)
        pizza2_circle.move_to(pizza2_anchor)
        self.objects["pizza2_circle"] = pizza2_circle

        pizza2_div_line_h = Line(LEFT*2, RIGHT*2, color=WHITE, stroke_width=2)
        pizza2_div_line_h.move_to(pizza2_anchor)
        self.objects["pizza2_div_line_h"] = pizza2_div_line_h

        pizza2_div_line_v = Line(DOWN*2, UP*2, color=WHITE, stroke_width=2)
        pizza2_div_line_v.move_to(pizza2_anchor)
        self.objects["pizza2_div_line_v"] = pizza2_div_line_v

        pizza2_shaded_sector1 = Sector(radius=2, angle=PI/2, start_angle=0, color="#FFD700", fill_opacity=0.8, stroke_width=0)
        pizza2_shaded_sector1.move_to(pizza2_anchor)
        self.objects["pizza2_shaded_sector1"] = pizza2_shaded_sector1

        pizza2_shaded_sector2 = Sector(radius=2, angle=PI/2, start_angle=PI/2, color="#FFD700", fill_opacity=0.8, stroke_width=0)
        pizza2_shaded_sector2.move_to(pizza2_anchor)
        self.objects["pizza2_shaded_sector2"] = pizza2_shaded_sector2

        label_2over4 = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        label_2over4.move_to(pizza2_anchor)
        self.objects["label_2over4"] = label_2over4

        # Explanation text
        explanation_text = Text("The shaded area is the same: 1 out of 2 equals 2 out of 4.", color=GRAY_B, font_size=32)
        explanation_text.move_to(footer_anchor)
        self.objects["explanation_text"] = explanation_text

        # Equation
        equation = MathTex(r"\frac{1}{2} = \frac{2}{4}", color=GREEN, font_size=40)
        equation.next_to(explanation_text, UP, buff=0.5)
        self.objects["equation"] = equation

        # Create VGroups for each pizza (for moving together)
        pizza1_group = VGroup(
            self.objects["pizza1_circle"],
            self.objects["pizza1_div_line"],
            self.objects["pizza1_shaded_sector"],
            self.objects["label_1over2"]
        )

        pizza2_group = VGroup(
            self.objects["pizza2_circle"],
            self.objects["pizza2_div_line_h"],
            self.objects["pizza2_div_line_v"],
            self.objects["pizza2_shaded_sector1"],
            self.objects["pizza2_shaded_sector2"],
            self.objects["label_2over4"]
        )

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["title"]))
        self.wait(max(0.1, max(0.1, 4.032 - 1.0)))

        # Step 2
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["pizza1_circle"]))
        self.wait(max(0.1, max(0.1, 6.624 - 1.0)))

        # Step 3
        self.play(Create(self.objects["pizza1_div_line"]))
        self.wait(max(0.1, 2.0))

        # Step 4
        self.play(Create(self.objects["pizza1_shaded_sector"]))
        self.wait(max(0.1, 2.0))

        # Step 5
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["pizza1_shaded_sector"], color=YELLOW))
        self.play(Write(self.objects["label_1over2"]))
        self.wait(max(0.1, max(0.1, 2.88 - 2.0)))

        # Step 6
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["pizza2_circle"]))
        self.wait(max(0.1, max(0.1, 5.016 - 1.0)))

        # Step 7
        self.play(Create(self.objects["pizza2_div_line_h"]))
        self.wait(max(0.1, 2.0))

        # Step 8
        self.play(Create(self.objects["pizza2_div_line_v"]))
        self.wait(max(0.1, 2.0))

        # Step 9
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_08.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["pizza2_shaded_sector1"]))
        self.wait(max(0.1, max(0.1, 4.872 - 1.0)))

        # Step 10
        self.play(Create(self.objects["pizza2_shaded_sector2"]))
        self.wait(max(0.1, 2.0))

        # Step 11
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_10.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        shaded_group = VGroup(self.objects["pizza2_shaded_sector1"], self.objects["pizza2_shaded_sector2"])
        self.play(Indicate(shaded_group, color=YELLOW))
        self.play(Write(self.objects["label_2over4"]))
        self.wait(max(0.1, max(0.1, 3.096 - 2.0)))

        # Step 12
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_11.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["pizza1_shaded_sector"], color=GREEN, run_time=1))
        # Create target VGroup for transformation: two quarter sectors at pizza1 position
        target_sector1 = Sector(radius=2, angle=PI/2, start_angle=0, color="#FFD700", fill_opacity=0.8, stroke_width=0)
        target_sector1.move_to(pizza1_anchor)
        target_sector2 = Sector(radius=2, angle=PI/2, start_angle=PI/2, color="#FFD700", fill_opacity=0.8, stroke_width=0)
        target_sector2.move_to(pizza1_anchor)
        target_group = VGroup(target_sector1, target_sector2)
        self.play(Transform(self.objects["pizza1_shaded_sector"], target_group))
        # Update registry
        self.objects["pizza1_shaded_sector"] = target_group
        self.wait(max(0.1, max(0.1, 6.912 - 2.0)))

        # Step 13
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_12.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(pizza1_group.animate.move_to(center_anchor))
        self.wait(max(0.1, max(0.1, 3.696 - 1.0)))

        # Step 14
        self.play(pizza2_group.animate.move_to(center_anchor))
        self.wait(max(0.1, 2.0))

        # Step 15
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_14.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Create group of all shaded areas for indication
        all_shaded = VGroup()
        if isinstance(self.objects["pizza1_shaded_sector"], VGroup):
            all_shaded.add(*self.objects["pizza1_shaded_sector"])
        else:
            all_shaded.add(self.objects["pizza1_shaded_sector"])
        all_shaded.add(self.objects["pizza2_shaded_sector1"], self.objects["pizza2_shaded_sector2"])
        self.play(Indicate(all_shaded, color=GREEN))
        self.play(Write(self.objects["explanation_text"]))
        self.wait(max(0.1, max(0.1, 7.416 - 2.0)))

        # Step 16
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_15.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["equation"]))
        self.wait(max(0.1, max(0.1, 3.144 - 1.0)))

        # Step 17
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_16.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["equation"], color=GREEN, run_time=1))
        self.wait(max(0.1, max(0.1, 4.56 - 1.0)))