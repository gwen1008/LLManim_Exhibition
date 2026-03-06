'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing how to measure a 60° angle using a protractor.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for angle and protractor
#    - Footer Region: [Bottom y=-3.5] for step explanations
# 3. Anti-Overlap Check:
#    - Strategy: Keep protractor components in VGroups, position title high, explanation low.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/measuring_a_60_degree_angle_with_a_protractor/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1-4: Build the 60° angle.
#    - Step 5-8: Build the protractor piece by piece.
#    - Step 9-10: Measure and confirm the angle.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        self.objects = {}

        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors
        title_anchor = 3.5 * UP
        global_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Measuring a 60° Angle with a Protractor", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # vertex
        vertex = Dot(point=ORIGIN, color=YELLOW, radius=0.08)
        vertex.move_to(global_center)
        self.objects["vertex"] = vertex

        # ray_initial
        ray_initial = Line(start=ORIGIN, end=[3, 0, 0], color=BLUE)
        ray_initial.move_to(global_center)
        self.objects["ray_initial"] = ray_initial

        # ray_terminal
        ray_terminal = Line(start=ORIGIN, end=[1.5, 2.598, 0], color=BLUE)
        ray_terminal.move_to(global_center)
        self.objects["ray_terminal"] = ray_terminal

        # angle_arc
        angle_arc = Arc(radius=1.0, start_angle=0, angle=PI/3, color=GREEN, stroke_width=4)
        angle_arc.move_to(global_center)
        self.objects["angle_arc"] = angle_arc

        # angle_label
        angle_label = MathTex(r"60^\circ", color=GREEN, font_size=28)
        angle_label.next_to(angle_arc, RIGHT, buff=0.1).shift(UP*0.2)
        self.objects["angle_label"] = angle_label

        # protractor_arc
        protractor_arc = Arc(radius=3.0, start_angle=0, angle=PI, color=GRAY_B, stroke_width=3)
        protractor_arc.set_stroke(opacity=0.7)
        protractor_arc.move_to(global_center)
        self.objects["protractor_arc"] = protractor_arc

        # protractor_center_mark
        protractor_center_mark = Cross(scale_factor=0.15, color=RED, stroke_width=2)
        protractor_center_mark.move_to(global_center)
        self.objects["protractor_center_mark"] = protractor_center_mark

        # protractor_ticks_vgroup
        protractor_ticks_vgroup = VGroup()
        # Major ticks every 10 degrees, minor every 2 degrees
        for deg in range(0, 181, 2):
            angle_rad = deg * DEGREES
            is_major = (deg % 10 == 0)
            length = 0.2 if is_major else 0.1
            tick = Line(
                start=[3.0 * np.cos(angle_rad), 3.0 * np.sin(angle_rad), 0],
                end=[(3.0 - length) * np.cos(angle_rad), (3.0 - length) * np.sin(angle_rad), 0],
                color=WHITE,
                stroke_width=2 if is_major else 1
            )
            tick.move_to(global_center)
            protractor_ticks_vgroup.add(tick)
        self.objects["protractor_ticks_vgroup"] = protractor_ticks_vgroup

        # protractor_labels_vgroup
        protractor_labels_vgroup = VGroup()
        for deg in [0, 30, 60, 90, 120, 150, 180]:
            angle_rad = deg * DEGREES
            label = MathTex(str(deg) + r"^\circ", color=WHITE, font_size=20)
            label.move_to(global_center)
            label.shift(3.3 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0]))
            protractor_labels_vgroup.add(label)
        self.objects["protractor_labels_vgroup"] = protractor_labels_vgroup

        # measurement_line
        measurement_line = Line(
            start=ORIGIN,
            end=[2.8 * np.cos(PI/3), 2.8 * np.sin(PI/3), 0],
            color=YELLOW,
            stroke_width=2
        )
        measurement_line.set_stroke(opacity=0.8)
        measurement_line.move_to(global_center)
        self.objects["measurement_line"] = measurement_line

        # step_explanation
        step_explanation = Text("Step 1: Draw a 60-degree angle.", color=GRAY_B, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/measuring_a_60_degree_angle_with_a_protractor/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["vertex"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["vertex"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/measuring_a_60_degree_angle_with_a_protractor/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["ray_initial"], color=BLUE, run_time=1))
        self.play(Create(self.objects["ray_initial"]), run_time=2.0)
        remaining_2 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/measuring_a_60_degree_angle_with_a_protractor/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["ray_terminal"], color=BLUE, run_time=1))
        self.play(Create(self.objects["ray_terminal"]), run_time=2.0)
        remaining_3 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/measuring_a_60_degree_angle_with_a_protractor/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["angle_arc"], color=GREEN, run_time=1))
        self.play(Create(self.objects["angle_arc"]), run_time=2.0)
        remaining_4 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/measuring_a_60_degree_angle_with_a_protractor/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["protractor_center_mark"], color=RED, run_time=1))
        self.play(Create(self.objects["protractor_center_mark"]), run_time=2.0)
        remaining_5 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/measuring_a_60_degree_angle_with_a_protractor/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["protractor_arc"], color=GRAY_B, run_time=1))
        self.play(Create(self.objects["protractor_arc"]), run_time=2.5)
        remaining_6 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/measuring_a_60_degree_angle_with_a_protractor/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        # No signal action for step 7
        self.play(Create(self.objects["protractor_ticks_vgroup"]), run_time=3.0)
        remaining_7 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        audio_step8 = "media/audio/measuring_a_60_degree_angle_with_a_protractor/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["protractor_labels_vgroup"], color=WHITE, run_time=1))
        self.play(Write(self.objects["protractor_labels_vgroup"]), run_time=3.5)
        remaining_8 = max(0.1, 3.5 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        # ========== Step 9 ==========
        audio_step9 = "media/audio/measuring_a_60_degree_angle_with_a_protractor/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["measurement_line"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["measurement_line"]), run_time=3.0)
        remaining_9 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # ========== Step 10 ==========
        audio_step10 = "media/audio/measuring_a_60_degree_angle_with_a_protractor/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["angle_label"], color=GREEN, run_time=1))
        self.play(FadeIn(self.objects["angle_label"]), run_time=3.0)
        remaining_10 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_10))

        # Final hold
        self.wait(max(0.1, 2))