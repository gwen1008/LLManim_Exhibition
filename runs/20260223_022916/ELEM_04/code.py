from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        vertex = ORIGIN
        title_anchor = 3.0 * UP
        explanation_anchor = 3.0 * DOWN

        # Helper to parse position strings (simplified for this blueprint)
        def parse_position(pos_str, ref_obj=None):
            if pos_str == "move_to(title_anchor)":
                return title_anchor
            elif pos_str == "move_to(vertex)":
                return vertex
            elif pos_str == "move_to(vertex, aligned_edge=LEFT)":
                return vertex
            elif pos_str == "move_to(explanation_anchor)":
                return explanation_anchor
            elif pos_str.startswith("next_to"):
                # Simplified: we'll handle specific cases in object creation
                return ORIGIN
            else:
                return ORIGIN

        # Create objects from layout_plan.objects
        # title
        title = Text("Constructing and Measuring a 60° Angle", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # ray_initial (will be created via transformation from triangle_AB)
        # triangle_AB
        triangle_AB = Line(start=vertex, end=vertex + 4 * RIGHT, color=GRAY_C, stroke_width=2)
        triangle_AB.set_opacity(0.5)
        self.objects["triangle_AB"] = triangle_AB
        # Also create the final ray_initial (blue, bold) for later transformation
        ray_initial = Line(start=vertex, end=vertex + 4 * RIGHT, color=BLUE, stroke_width=4)
        self.objects["ray_initial"] = ray_initial

        # ray_terminal (will be created via transformation from triangle_AC)
        # triangle_AC
        triangle_AC = Line(start=vertex, end=vertex + np.array([2, 3.464, 0]), color=GRAY_C, stroke_width=2)
        triangle_AC.set_opacity(0.5)
        self.objects["triangle_AC"] = triangle_AC
        # Final ray_terminal
        ray_terminal = Line(start=vertex, end=vertex + np.array([2, 3.464, 0]), color=BLUE, stroke_width=4)
        self.objects["ray_terminal"] = ray_terminal

        # triangle_BC
        triangle_BC = Line(start=vertex + 4 * RIGHT, end=vertex + np.array([2, 3.464, 0]), color=GRAY_C, stroke_width=2)
        triangle_BC.set_opacity(0.5)
        self.objects["triangle_BC"] = triangle_BC

        # protractor_arc
        protractor_arc = Arc(radius=3.5, start_angle=0, angle=PI, color=WHITE, stroke_width=3)
        protractor_arc.move_to(vertex)
        self.objects["protractor_arc"] = protractor_arc

        # protractor_baseline
        protractor_baseline = Line(start=vertex + 3.5 * LEFT, end=vertex + 3.5 * RIGHT, color=WHITE, stroke_width=2)
        protractor_baseline.move_to(vertex)
        self.objects["protractor_baseline"] = protractor_baseline

        # protractor_ticks_vg
        protractor_ticks_vg = VGroup()
        major_angles = [0, 30, 60, 90, 120, 150, 180]
        tick_length = 0.2
        label_distance = 0.4
        for angle in major_angles:
            rad_angle = angle * DEGREES
            start_point = vertex + 3.5 * np.array([np.cos(rad_angle), np.sin(rad_angle), 0])
            end_point = vertex + (3.5 - tick_length) * np.array([np.cos(rad_angle), np.sin(rad_angle), 0])
            tick = Line(start=start_point, end=end_point, color=WHITE, stroke_width=2)
            protractor_ticks_vg.add(tick)
            # Label
            label_pos = vertex + (3.5 - label_distance) * np.array([np.cos(rad_angle), np.sin(rad_angle), 0])
            label = Text(str(angle), color=WHITE, font_size=20)
            label.move_to(label_pos)
            protractor_ticks_vg.add(label)
        self.objects["protractor_ticks_vg"] = protractor_ticks_vg
        # Store individual tick label for step 6 signal action
        # The 60° label is the 4th element in the VGroup (index 3: tick, index 4: label)
        self.objects["protractor_60_label"] = protractor_ticks_vg[4]

        # angle_arc
        angle_arc = Arc(radius=2.5, start_angle=0, angle=60*DEGREES, color=YELLOW, stroke_width=6)
        angle_arc.move_to(vertex)
        self.objects["angle_arc"] = angle_arc

        # angle_label
        angle_label = MathTex(r"60^\circ", color=YELLOW).scale(0.8)
        # Position next to arc center (approximation)
        arc_center_point = vertex + 2.5/2 * np.array([np.cos(30*DEGREES), np.sin(30*DEGREES), 0])
        angle_label.next_to(arc_center_point, UP+RIGHT, buff=0.2)
        self.objects["angle_label"] = angle_label

        # step_explanation (initial text)
        step_explanation = Text("Step 1: We begin by constructing two rays from a common vertex.", color=GRAY_C, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # Create other explanation texts for later steps
        step2_text = Text("Step 2: Draw the base of an equilateral triangle from the vertex.", color=GRAY_C, font_size=24)
        step2_text.move_to(explanation_anchor)
        self.objects["step2_text"] = step2_text

        step3_text = Text("Step 3: Complete the equilateral triangle. The angle at the vertex is 60°.", color=GRAY_C, font_size=24)
        step3_text.move_to(explanation_anchor)
        self.objects["step3_text"] = step3_text

        step4_text = Text("Step 4: The two rays form our angle. Now we measure it with a protractor.", color=GRAY_C, font_size=24)
        step4_text.move_to(explanation_anchor)
        self.objects["step4_text"] = step4_text

        step5_text = Text("Step 5: The protractor is aligned. The center is at the vertex, and the baseline matches the initial ray.", color=GRAY_C, font_size=24)
        step5_text.move_to(explanation_anchor)
        self.objects["step5_text"] = step5_text

        step6_text = Text("Step 6: The terminal ray aligns with the 60° mark, confirming the angle measure.", color=GRAY_C, font_size=24)
        step6_text.move_to(explanation_anchor)
        self.objects["step6_text"] = step6_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 11.112 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["triangle_AB"]), run_time=1.5)
        self.play(ReplacementTransform(self.objects["step_explanation"], self.objects["step2_text"]), run_time=1.0)
        remaining_2 = max(0.1, 6.552 - (1.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        vertex_dot = Dot(vertex, color=GREEN)
        self.play(Indicate(vertex_dot, color=GREEN, run_time=1))
        self.play(Create(self.objects["triangle_AC"]), Create(self.objects["triangle_BC"]), run_time=2.0)
        self.play(ReplacementTransform(self.objects["step2_text"], self.objects["step3_text"]), run_time=1.0)
        remaining_3 = max(0.1, 9.432 - (1 + 2.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        vertex_dot2 = Dot(vertex)
        self.play(Circumscribe(vertex_dot2, color=YELLOW, run_time=1))
        self.play(FadeOut(self.objects["triangle_BC"]), run_time=0.5)
        self.play(Transform(self.objects["triangle_AB"], self.objects["ray_initial"]), run_time=1.0)
        self.play(Transform(self.objects["triangle_AC"], self.objects["ray_terminal"]), run_time=1.0)
        self.play(ReplacementTransform(self.objects["step3_text"], self.objects["step4_text"]), run_time=1.0)
        remaining_4 = max(0.1, 7.776 - (1 + 0.5 + 1.0 + 1.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["ray_initial"], color=RED, run_time=1))
        self.play(Create(self.objects["protractor_baseline"]), Create(self.objects["protractor_arc"]), run_time=2.0)
        self.play(Create(self.objects["protractor_ticks_vg"]), run_time=2.0)
        self.play(ReplacementTransform(self.objects["step4_text"], self.objects["step5_text"]), run_time=1.0)
        remaining_5 = max(0.1, 10.08 - (1 + 2.0 + 2.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["ray_terminal"], color=RED, run_time=1))
        self.play(Create(self.objects["angle_arc"]), run_time=1.5)
        self.play(Write(self.objects["angle_label"]), run_time=1.0)
        self.play(Circumscribe(self.objects["protractor_60_label"], color=YELLOW, run_time=1))
        self.play(ReplacementTransform(self.objects["step5_text"], self.objects["step6_text"]), run_time=1.0)
        remaining_6 = max(0.1, 10.32 - (1 + 1.5 + 1.0 + 1 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_6))