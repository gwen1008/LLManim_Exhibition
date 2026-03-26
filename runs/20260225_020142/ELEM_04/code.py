from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        self.objects = {}  # Registry for all objects

        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        geometry_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title_text
        title_text = Text("Constructing and Measuring a 60° Angle", color=WHITE, font_size=40)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text

        # line_fixed
        line_fixed = Line(start=[0, 0, 0], end=[4, 0, 0], color="#FF5555", stroke_width=6)
        line_fixed.move_to(geometry_center, aligned_edge=LEFT)
        self.objects["line_fixed"] = line_fixed

        # line_rotating - start at 0 degrees (overlaps line_fixed), endpoint pre-calculated for 60 degrees
        # We'll create it initially at 0 degrees, then rotate it in Step 2.
        line_rotating = Line(start=[0, 0, 0], end=[4, 0, 0], color="#5555FF", stroke_width=6)
        line_rotating.move_to(geometry_center, aligned_edge=LEFT)
        self.objects["line_rotating"] = line_rotating

        # angle_arc
        angle_arc = Arc(radius=1.0, start_angle=0, angle=PI/3, color=YELLOW, stroke_width=4)
        angle_arc.move_to(geometry_center)
        self.objects["angle_arc"] = angle_arc

        # protractor_vgroup - we'll build it as a VGroup
        protractor_arc = Arc(radius=4.5, start_angle=0, angle=PI, color=WHITE, stroke_width=3)
        protractor_arc.set_stroke(opacity=0.7)
        protractor_arc.move_to(ORIGIN)

        # Create scale marks for the protractor (simplified: major marks at 0, 30, 60, 90, 120, 150, 180)
        scale_marks = VGroup()
        for angle_deg in [0, 30, 60, 90, 120, 150, 180]:
            angle_rad = angle_deg * DEGREES
            start_point = 4.3 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            end_point = 4.5 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            mark = Line(start=start_point, end=end_point, color=WHITE, stroke_width=2)
            scale_marks.add(mark)

        # The 60-degree scale mark is also stored separately as per layout_plan
        protractor_scale_60 = scale_marks[2]  # index 2 corresponds to 60 degrees
        self.objects["protractor_scale_60"] = protractor_scale_60

        # Assemble the protractor VGroup
        protractor_vgroup = VGroup(protractor_arc, scale_marks)
        protractor_vgroup.move_to(geometry_center).rotate(30 * DEGREES, about_point=geometry_center)
        # Set z_index so protractor is above lines but below highlights (will be adjusted later)
        protractor_vgroup.set_z_index(1)
        self.objects["protractor_vgroup"] = protractor_vgroup

        # label_60_line
        label_60_line = MathTex(r"60^\circ", color="#5555FF", font_size=30)
        # Position will be set after line_rotating is in final position (Step 2)
        self.objects["label_60_line"] = label_60_line

        # label_60_protractor
        label_60_protractor = MathTex(r"60^\circ", color=YELLOW, font_size=28)
        label_pos = 4.9 * np.array([np.cos(60 * DEGREES), np.sin(60 * DEGREES), 0])
        label_60_protractor.move_to(label_pos)
        label_60_protractor.set_z_index(3)  # On top of protractor
        self.objects["label_60_protractor"] = label_60_protractor

        # explanation_text - will be updated each step
        explanation_text = Text("Step 1: Draw the fixed reference line along the x-axis.",
                                 color=GRAY_B, font_size=28)
        explanation_text.move_to(explanation_anchor + UP*0.5)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # Visual action: Create line_fixed
        self.play(Write(title_text), run_time=0.5)
        self.play(Create(line_fixed), Write(explanation_text), run_time=1.5)
        remaining_1 = max(0.1, 4.464 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Update explanation text
        new_explanation_2 = Text("Step 2: Rotate a second line to form a 60° angle.",
                                 color=GRAY_B, font_size=28)
        new_explanation_2.move_to(explanation_anchor + UP*0.5)
        self.play(ReplacementTransform(explanation_text, new_explanation_2))
        explanation_text = new_explanation_2

        # Signal action: Indicate line_fixed
        self.play(Indicate(line_fixed, color=YELLOW, run_time=1))

        # Visual action: Rotate line_rotating from 0 to 60 degrees
        # First, create line_rotating at 0 degrees (overlapping line_fixed)
        self.play(Create(line_rotating), run_time=0.5)
        self.play(Rotate(line_rotating, angle=60*DEGREES, about_point=geometry_center), run_time=2.5)
        # Position the label near the end of the rotating line
        label_60_line.next_to(line_rotating.get_end(), UR, buff=0.2)
        self.play(Write(label_60_line), run_time=0.5)
        remaining_2 = max(0.1, 6.144 - 4.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        new_explanation_3 = Text("Step 3: Add an arc to highlight the 60° angle.",
                                 color=GRAY_B, font_size=28)
        new_explanation_3.move_to(explanation_anchor + UP*0.5)
        self.play(ReplacementTransform(explanation_text, new_explanation_3))
        explanation_text = new_explanation_3

        # Signal action: Circumscribe angle_arc
        self.play(Circumscribe(angle_arc, color=YELLOW, run_time=1))

        # Visual action: Create angle_arc
        self.play(Create(angle_arc), run_time=1.5)
        remaining_3 = max(0.1, 4.728 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        new_explanation_4 = Text("Step 4: Introduce a protractor (misaligned).",
                                 color=GRAY_B, font_size=28)
        new_explanation_4.move_to(explanation_anchor + UP*0.5)
        self.play(ReplacementTransform(explanation_text, new_explanation_4))
        explanation_text = new_explanation_4

        # Visual action: FadeIn protractor_vgroup
        self.play(FadeIn(protractor_vgroup), run_time=2.0)
        remaining_4 = max(0.1, 8.208 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        new_explanation_5 = Text("Step 5: Align the protractor's baseline with the fixed line.",
                                 color=GRAY_B, font_size=28)
        new_explanation_5.move_to(explanation_anchor + UP*0.5)
        self.play(ReplacementTransform(explanation_text, new_explanation_5))
        explanation_text = new_explanation_5

        # Signal action: Indicate line_fixed
        self.play(Indicate(line_fixed, color=RED, run_time=1))

        # Visual action: Rotate protractor_vgroup by -30 degrees to align (from +30 to 0)
        self.play(Rotate(protractor_vgroup, angle=-30*DEGREES, about_point=geometry_center), run_time=2.5)
        remaining_5 = max(0.1, 9.6 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        new_explanation_6 = Text("Step 6: Read the measurement: the line intersects at 60°.",
                                 color=GRAY_B, font_size=28)
        new_explanation_6.move_to(explanation_anchor + UP*0.5)
        self.play(ReplacementTransform(explanation_text, new_explanation_6))
        explanation_text = new_explanation_6

        # Signal action: Indicate protractor_scale_60
        self.play(Indicate(protractor_scale_60, color=YELLOW, run_time=1))

        # Visual action: Create label_60_protractor
        self.play(Write(label_60_protractor), run_time=1.5)
        # Also add a small dot at the intersection for emphasis
        intersection_dot = Dot(point=line_rotating.get_end(), color=YELLOW, radius=0.08)
        intersection_dot.set_z_index(4)
        self.play(FadeIn(intersection_dot), run_time=0.5)
        remaining_6 = max(0.1, 11.736 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))