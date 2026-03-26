'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Demonstrate how to measure a 60° angle using a protractor, emphasizing the alignment process (center and baseline).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for angle and protractor
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check:
#    - The protractor starts left of center and moves to center, ensuring no overlap during transition.
#    - The angle arc and label fade out before the protractor highlight appears to reduce clutter.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/measuring_angles/step_XX.mp3"
# 5. Animation Flow:
#    - Create the 60° angle (vertex, rays, arc, label).
#    - Introduce the protractor on the left.
#    - Animate protractor alignment (move + rotate).
#    - Highlight the measured sector and show final label.
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
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        protractor_start_pos = 4 * LEFT

        # Create objects from layout_plan
        # title
        title = Text("Measuring a 60° Angle", font_size=40, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # vertex_V
        vertex_V = Dot(radius=0.08, color=YELLOW)
        vertex_V.move_to(content_center)
        self.objects["vertex_V"] = vertex_V

        # ray_VA
        ray_VA = Line(start=content_center, end=content_center + RIGHT * 3, color=BLUE, stroke_width=4)
        self.objects["ray_VA"] = ray_VA

        # ray_VB
        ray_VB = Line(
            start=content_center,
            end=content_center + np.array([3 * np.cos(np.pi/3), 3 * np.sin(np.pi/3), 0]),
            color=BLUE,
            stroke_width=4
        )
        self.objects["ray_VB"] = ray_VB

        # angle_arc
        angle_arc = Arc(radius=0.8, angle=60*DEGREES, color=GREEN, stroke_width=3)
        angle_arc.move_to(content_center)
        self.objects["angle_arc"] = angle_arc

        # angle_label
        angle_label = MathTex("60^\\circ", color=GREEN).scale(0.8)
        # Position next to arc midpoint
        arc_mid_point = angle_arc.point_from_proportion(0.5)
        angle_label.next_to(arc_mid_point, UP+RIGHT, buff=0.1)
        self.objects["angle_label"] = angle_label

        # protractor_group (build as VGroup)
        protractor_radius = 2.5
        protractor_arc = Arc(radius=protractor_radius, angle=PI, color=GRAY_C, stroke_width=3)
        center_dot = Dot(radius=0.06, color=WHITE)
        baseline_indicator = Line(ORIGIN, RIGHT * protractor_radius * 0.9, color=WHITE, stroke_width=2)
        # Ticks and labels
        ticks = VGroup()
        labels = VGroup()
        for deg in range(0, 181, 10):
            angle_rad = deg * DEGREES
            start = protractor_radius * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            if deg % 90 == 0:
                end = (protractor_radius - 0.3) * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            elif deg % 30 == 0:
                end = (protractor_radius - 0.2) * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            else:
                end = (protractor_radius - 0.1) * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            tick = Line(start, end, color=GRAY_C, stroke_width=2)
            ticks.add(tick)
            if deg % 30 == 0:
                label_pos = (protractor_radius - 0.35) * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
                label = Text(str(deg), font_size=20, color=WHITE).scale(0.6).move_to(label_pos)
                labels.add(label)
        protractor_group = VGroup(protractor_arc, center_dot, baseline_indicator, ticks, labels)
        protractor_group.move_to(protractor_start_pos)
        self.objects["protractor_group"] = protractor_group

        # protractor_aligned (target state for transform)
        protractor_aligned = protractor_group.copy()
        protractor_aligned.move_to(content_center)
        # Rotate so baseline aligns with ray_VA (horizontal)
        # Since baseline_indicator points right (0°), and ray_VA is right, no rotation needed.
        self.objects["protractor_aligned"] = protractor_aligned

        # measurement_arc (AnnularSector)
        measurement_arc = AnnularSector(
            radius=2.3,
            angle=60*DEGREES,
            inner_radius=2.0,
            color="#FFA500",
            fill_opacity=0.5,
            stroke_width=0
        )
        measurement_arc.move_to(content_center)
        self.objects["measurement_arc"] = measurement_arc

        # measurement_label
        measurement_label = MathTex("60^\\circ", color="#FFA500", font_size=36)
        sector_mid_point = measurement_arc.point_from_proportion(0.5)
        measurement_label.next_to(sector_mid_point, UP+RIGHT, buff=0.2)
        self.objects["measurement_label"] = measurement_label

        # step_explanation
        step_explanation = Text("Step 1: Draw a 60-degree angle.", font_size=24, color=WHITE)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Draw_a_60_degree_ang_8c406cffb8/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/measuring_angles/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.wait(max(0.1, max(0.1, 1.0 - 1.0 + 0.5)))

        self.add_sound("media/audio/Draw_a_60_degree_ang_8c406cffb8/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/measuring_angles/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["vertex_V"]), run_time=1.0)
        self.wait(max(0.1, max(0.1, 1.0 - 1.0 + 0.5)))

        self.add_sound("media/audio/Draw_a_60_degree_ang_8c406cffb8/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/measuring_angles/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Create(self.objects["ray_VA"]), run_time=1.5)
        self.wait(max(0.1, max(0.1, 1.5 - 1.5 + 0.5)))

        self.add_sound("media/audio/Draw_a_60_degree_ang_8c406cffb8/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/measuring_angles/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Create(self.objects["ray_VB"]), run_time=1.5)
        self.wait(max(0.1, max(0.1, 1.5 - 1.5 + 0.5)))

        self.add_sound("media/audio/Draw_a_60_degree_ang_8c406cffb8/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/measuring_angles/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["angle_label"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["angle_arc"]), Write(self.objects["angle_label"]), run_time=1.0)
        self.wait(max(0.1, max(0.1, 2.0 - 1.0 + 0.5)))

        self.add_sound("media/audio/Draw_a_60_degree_ang_8c406cffb8/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/measuring_angles/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        new_explanation1 = Text("Step 2: Introduce the protractor.", font_size=24, color=WHITE)
        new_explanation1.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation1), run_time=1.5)
        self.objects["step_explanation"] = new_explanation1
        self.wait(max(0.1, max(0.1, 1.5 - 1.5 + 0.5)))

        self.add_sound("media/audio/Draw_a_60_degree_ang_8c406cffb8/step_06.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/measuring_angles/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["protractor_group"], color=YELLOW, run_time=1))
        self.play(FadeIn(self.objects["protractor_group"]), run_time=2.0)
        self.wait(max(0.1, max(0.1, 3.0 - 2.0 + 0.5)))

        self.add_sound("media/audio/Draw_a_60_degree_ang_8c406cffb8/step_07.mp3")  # [auto-injected]
        # Step 8
        audio_step8 = "media/audio/measuring_angles/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        new_explanation2 = Text("Step 3: Align the protractor.", font_size=24, color=WHITE)
        new_explanation2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation2), run_time=2.0)
        self.objects["step_explanation"] = new_explanation2
        self.wait(max(0.1, max(0.1, 2.0 - 2.0 + 0.5)))

        self.add_sound("media/audio/Draw_a_60_degree_ang_8c406cffb8/step_08.mp3")  # [auto-injected]
        # Step 9
        audio_step9 = "media/audio/measuring_angles/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(
            Transform(self.objects["protractor_group"], self.objects["protractor_aligned"]),
            FadeOut(self.objects["angle_arc"]),
            FadeOut(self.objects["angle_label"]),
            run_time=3.0
        )
        self.wait(max(0.1, max(0.1, 3.0 - 3.0 + 0.5)))

        self.add_sound("media/audio/Draw_a_60_degree_ang_8c406cffb8/step_09.mp3")  # [auto-injected]
        # Step 10
        audio_step10 = "media/audio/measuring_angles/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["ray_VB"], color=RED, run_time=1))
        new_explanation3 = Text("Step 4: Read the measurement.", font_size=24, color=WHITE)
        new_explanation3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation3), run_time=1.5)
        self.objects["step_explanation"] = new_explanation3
        self.wait(max(0.1, max(0.1, 2.5 - 1.5 + 0.5)))

        self.add_sound("media/audio/Draw_a_60_degree_ang_8c406cffb8/step_10.mp3")  # [auto-injected]
        # Step 11
        audio_step11 = "media/audio/measuring_angles/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        self.play(FadeIn(self.objects["measurement_arc"]), run_time=2.0)
        self.wait(max(0.1, max(0.1, 2.0 - 2.0 + 0.5)))

        # Step 12
        audio_step12 = "media/audio/measuring_angles/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["measurement_label"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["measurement_label"]), run_time=1.5)
        self.wait(max(0.1, max(0.1, 2.5 - 1.5 + 0.5)))

        # Final pause
        self.wait(max(0.1, 2))