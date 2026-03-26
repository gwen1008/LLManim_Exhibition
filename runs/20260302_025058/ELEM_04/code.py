'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing how to measure a 60-degree angle using a protractor, constructed step-by-step around the angle.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for the angle and protractor
#    - Footer Region: [Bottom y=-3.5] for step explanations
# 3. Anti-Overlap Check:
#    - The protractor is large (radius 3.5). Ensure it stays within safe zone y ∈ [-3.0, 3.0]. It fits because radius 3.5 < 3.5 screen height.
#    - Explanations at bottom will not overlap.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1-4: Draw the 60-degree angle (vertex, arms, small arc).
#    - Step 5-8: Construct the protractor around it (baseline, arc, ticks, labels).
#    - Step 9-10: Measure the angle with a yellow arc and label.
'''

from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        self.objects = {}

        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors
        global_center = ORIGIN
        title_anchor = 3.5 * UP
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Measuring a 60-Degree Angle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # vertex
        vertex = Dot(radius=0.08, color=WHITE)
        vertex.move_to(global_center)
        self.objects["vertex"] = vertex

        # arm_initial
        arm_initial = Line(start=[0,0,0], end=[3,0,0], color=BLUE, stroke_width=4)
        arm_initial.move_to(global_center)
        self.objects["arm_initial"] = arm_initial

        # arm_terminal
        arm_terminal = Line(start=[0,0,0], end=[1.5, 2.598, 0], color=BLUE, stroke_width=4)
        arm_terminal.move_to(global_center)
        self.objects["arm_terminal"] = arm_terminal

        # angle_arc
        angle_arc = Arc(radius=1.0, start_angle=0, angle=60*DEGREES, color=BLUE, stroke_width=3)
        angle_arc.move_to(global_center)
        self.objects["angle_arc"] = angle_arc

        # protractor_baseline
        protractor_baseline = Line(start=[-3.5,0,0], end=[3.5,0,0], color=GRAY_B, stroke_width=2)
        protractor_baseline.set_stroke(opacity=0.7)
        protractor_baseline.move_to(global_center)
        self.objects["protractor_baseline"] = protractor_baseline

        # protractor_arc
        protractor_arc = Arc(radius=3.5, start_angle=0, angle=PI, color=WHITE, stroke_width=3)
        protractor_arc.move_to(global_center)
        self.objects["protractor_arc"] = protractor_arc

        # protractor_ticks (VGroup of lines at 10-degree intervals)
        protractor_ticks = VGroup()
        for angle in range(0, 181, 10):
            start_rad = 3.4
            end_rad = 3.5
            start_point = np.array([start_rad * np.cos(angle * DEGREES), start_rad * np.sin(angle * DEGREES), 0])
            end_point = np.array([end_rad * np.cos(angle * DEGREES), end_rad * np.sin(angle * DEGREES), 0])
            tick = Line(start=start_point, end=end_point, color=WHITE, stroke_width=1.5)
            protractor_ticks.add(tick)
        protractor_ticks.move_to(global_center)
        self.objects["protractor_ticks"] = protractor_ticks

        # protractor_labels (VGroup of MathTex labels)
        protractor_labels = VGroup()
        for angle in range(0, 181, 10):
            label_rad = 3.1
            pos = np.array([label_rad * np.cos(angle * DEGREES), label_rad * np.sin(angle * DEGREES), 0])
            label = MathTex(str(angle), color=WHITE, font_size=24)
            label.move_to(pos)
            # Rotate label for readability (avoid upside-down)
            if 90 < angle < 270:
                label.rotate(PI)
            protractor_labels.add(label)
        protractor_labels.move_to(global_center)
        self.objects["protractor_labels"] = protractor_labels

        # measurement_arc
        measurement_arc = Arc(radius=3.0, start_angle=0, angle=60*DEGREES, color=YELLOW, stroke_width=6)
        measurement_arc.move_to(global_center)
        self.objects["measurement_arc"] = measurement_arc

        # measurement_label
        label_pos = global_center + np.array([3.0 * np.cos(30*DEGREES), 3.0 * np.sin(30*DEGREES) + 0.3, 0])
        measurement_label = MathTex("60^\\circ", color=YELLOW, font_size=36)
        measurement_label.move_to(label_pos)
        self.objects["measurement_label"] = measurement_label

        # step_explanation (placeholder, will be updated per step)
        step_explanation = Text("Placeholder", color=GRAY_B, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["vertex"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["vertex"]), run_time=1.5)
        remaining_1 = max(0.1, 7.632 - 1.5 - 1 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["arm_initial"]), run_time=2.0)
        remaining_2 = max(0.1, 5.352 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["arm_terminal"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["arm_terminal"]), run_time=2.0)
        remaining_3 = max(0.1, 5.592 - 2.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Create(self.objects["angle_arc"]), run_time=2.0)
        remaining_4 = max(0.1, 9.216 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["protractor_baseline"], color=GREEN, run_time=1))
        self.play(Create(self.objects["protractor_baseline"]), run_time=2.0)
        remaining_5 = max(0.1, 7.464 - 2.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Create(self.objects["protractor_arc"]), run_time=2.0)
        remaining_6 = max(0.1, 5.688 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["protractor_labels"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["protractor_ticks"]), run_time=3.0)
        remaining_7 = max(0.1, 10.776 - 3.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        audio_step8 = "media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        self.play(Write(self.objects["protractor_labels"]), run_time=3.0)
        remaining_8 = max(0.1, 4.92 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        audio_step9 = "media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["measurement_arc"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["measurement_arc"]), run_time=2.5)
        remaining_9 = max(0.1, 6.6 - 2.5 - 1 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Step 10
        audio_step10 = "media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["measurement_label"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["measurement_label"]), run_time=1.5)
        remaining_10 = max(0.1, 6.912 - 1.5 - 1 + 0.5)
        self.wait(max(0.1, remaining_10))

        # Final hold
        self.wait(max(0.1, 2))