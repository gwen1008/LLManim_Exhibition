'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Demonstrate how to measure a 60° angle using a protractor, showing the step-by-step process of placing the protractor and reading the measurement.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for the angle and protractor
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - The protractor and angle rays will be centered at ORIGIN.
#    - The title is at the top, explanation at the bottom, leaving the central area clear.
#    - The angle label is placed near the vertex but offset to avoid overlap.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/measuring_angle_with_protractor/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show title.
#    - Step 2: Create vertex dot.
#    - Step 3: Draw initial ray (0° reference).
#    - Step 4: Draw second ray (60° angle).
#    - Step 5: Draw protractor arc, emphasizing centering on vertex.
#    - Step 6: Draw protractor baseline.
#    - Step 7: Animate measurement arc from 0° to 60°.
#    - Step 8: Show final angle label.
'''

from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_an_animation__a31b604f54/final_narrative.mp3")  # [auto-injected: full narration]
        self.camera.background_color = "#1e1e1e"
        self.objects = {}

        # ========== PHASE 1: Layout & Object Creation ==========
        # Create anchors
        title_anchor = 3.5 * UP
        global_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Measuring a 60° Angle with a Protractor", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # vertex
        vertex = Dot(radius=0.08, color=YELLOW)
        vertex.move_to(global_center)
        self.objects["vertex"] = vertex

        # ray_initial
        ray_initial = Line(start=ORIGIN, end=RIGHT*3, color=BLUE, stroke_width=4)
        ray_initial.move_to(global_center)
        self.objects["ray_initial"] = ray_initial

        # ray_60
        angle_rad = 60 * PI / 180
        ray_60 = Line(start=ORIGIN, end=np.array([3*np.cos(angle_rad), 3*np.sin(angle_rad), 0]), color=GREEN, stroke_width=4)
        ray_60.move_to(global_center)
        self.objects["ray_60"] = ray_60

        # protractor_arc
        protractor_arc = Arc(radius=2.5, start_angle=0, angle=PI, color=GRAY_B, stroke_width=6, stroke_opacity=0.7)
        protractor_arc.move_to(global_center)
        self.objects["protractor_arc"] = protractor_arc

        # protractor_base
        protractor_base = Line(start=LEFT*2.5, end=RIGHT*2.5, color=GRAY_B, stroke_width=4, stroke_opacity=0.7)
        protractor_base.move_to(global_center)
        self.objects["protractor_base"] = protractor_base

        # measurement_arc
        measurement_arc = Arc(radius=2.8, start_angle=0, angle=angle_rad, color=RED, stroke_width=8, stroke_opacity=0.9)
        measurement_arc.move_to(global_center)
        self.objects["measurement_arc"] = measurement_arc

        # angle_label
        angle_label = MathTex(r"60^\circ", color=YELLOW, font_size=36)
        angle_label.move_to(global_center + UP*1.2 + RIGHT*0.8)
        self.objects["angle_label"] = angle_label

        # explanation_text
        explanation_text = Text("We begin with a blank scene.", color=GRAY_C, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/measuring_angle_with_protractor/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/measuring_angle_with_protractor/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["vertex"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["vertex"]), run_time=1.5)
        remaining_2 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/measuring_angle_with_protractor/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["ray_initial"], color=BLUE, run_time=1))
        self.play(Create(self.objects["ray_initial"]), run_time=2.0)
        remaining_3 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/measuring_angle_with_protractor/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["ray_60"], color=GREEN, run_time=1))
        self.play(Create(self.objects["ray_60"]), run_time=2.0)
        remaining_4 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/measuring_angle_with_protractor/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["vertex"], color=ORANGE, run_time=1))
        self.play(Create(self.objects["protractor_arc"]), run_time=2.5)
        remaining_5 = max(0.1, 4.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/measuring_angle_with_protractor/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["ray_initial"], color=BLUE, run_time=1))
        self.play(Create(self.objects["protractor_base"]), run_time=2.0)
        remaining_6 = max(0.1, 3.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/measuring_angle_with_protractor/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["ray_60"], color=GREEN, run_time=1))
        self.play(Create(self.objects["measurement_arc"]), run_time=3.0)
        remaining_7 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        audio_step8 = "media/audio/measuring_angle_with_protractor/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["measurement_arc"], color=RED, run_time=1))
        self.play(Write(self.objects["angle_label"]), run_time=1.5)
        remaining_8 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Final hold
        self.wait(max(0.1, 2))