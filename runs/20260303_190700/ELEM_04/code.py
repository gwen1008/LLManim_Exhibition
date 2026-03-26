'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the measurement of a 60-degree angle using a constructed protractor scale, reinforcing the concept of an angle as a measure of rotation.
# 2. Layout Strategy:
#    - Header Region: [y=3.0] for Title
#    - Main Content: [Center y=0] for angle and protractor
#    - Footer Region: [Bottom y=-2.8] for step explanations
# 3. Anti-Overlap Check:
#    - Strategy: Use z_index to ensure rays are on top of the protractor. Position labels outside the arc.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/measuring_angle/step_XX.mp3"
# 5. Animation Flow: Show vertex, draw initial ray, draw terminal ray, introduce protractor arc, add scale ticks and labels, highlight the 60-degree arc, and label it.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_a_Manim_anima_2779aea7ff/final_narrative.mp3")  # [auto-injected: full narration]
        self.camera.background_color = "#1e1e1e"
        self.objects = {}

        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        vertex = ORIGIN
        title_anchor = 3.0 * UP
        explanation_anchor = 2.8 * DOWN

        # Create objects from layout_plan
        # vertex dot
        vertex_dot = Dot(point=vertex, color=WHITE, radius=0.08)
        self.objects["vertex"] = vertex_dot
        
        # title
        title = Text("Measuring a 60-Degree Angle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # ray_initial
        ray_initial = Line(start=[0,0,0], end=[3,0,0], color=BLUE, stroke_width=6)
        ray_initial.move_to(vertex, aligned_edge=LEFT)
        self.objects["ray_initial"] = ray_initial

        # ray_terminal
        ray_terminal = Line(start=[0,0,0], end=[1.5, 2.598, 0], color=GREEN, stroke_width=6)
        ray_terminal.move_to(vertex, aligned_edge=LEFT)
        self.objects["ray_terminal"] = ray_terminal

        # protractor_arc
        protractor_arc = Arc(radius=2.5, start_angle=0, angle=PI, color=GRAY_C, stroke_width=4, stroke_opacity=0.9)
        protractor_arc.move_to(vertex)
        protractor_arc.set_z_index(-1)
        self.objects["protractor_arc"] = protractor_arc

        # protractor_ticks
        tick_angles = [0, 30, 60, 90, 120, 150, 180]
        ticks = VGroup()
        for angle_deg in tick_angles:
            angle_rad = angle_deg * DEGREES
            point_on_arc = protractor_arc.point_from_proportion(angle_rad / PI)
            # Direction from center to point
            dir_vec = point_on_arc - vertex
            dir_vec = dir_vec / np.linalg.norm(dir_vec)
            tick_length = 0.15
            tick_start = point_on_arc - dir_vec * tick_length * 0.5
            tick_end = point_on_arc + dir_vec * tick_length * 0.5
            tick = Line(start=tick_start, end=tick_end, color=WHITE, stroke_width=2)
            ticks.add(tick)
        ticks.move_to(vertex)
        self.objects["protractor_ticks"] = ticks

        # protractor_labels
        labels = VGroup()
        label_data = [(0, r"0^\circ"), (60, r"60^\circ"), (90, r"90^\circ"), (180, r"180^\circ")]
        for angle_deg, tex in label_data:
            angle_rad = angle_deg * DEGREES
            point_on_arc = protractor_arc.point_from_proportion(angle_rad / PI)
            dir_vec = point_on_arc - vertex
            dir_vec = dir_vec / np.linalg.norm(dir_vec)
            label_pos = point_on_arc + dir_vec * 0.4
            label = MathTex(tex, color=YELLOW, font_size=24)
            label.move_to(label_pos)
            labels.add(label)
        labels.move_to(vertex)
        self.objects["protractor_labels"] = labels

        # angle_arc_highlight
        angle_arc_highlight = Arc(radius=2.3, start_angle=0, angle=60*DEGREES, color=YELLOW, stroke_width=8, stroke_opacity=0.7)
        angle_arc_highlight.move_to(vertex)
        self.objects["angle_arc_highlight"] = angle_arc_highlight

        # angle_label
        label_angle_rad = 30 * DEGREES
        point_on_arc = protractor_arc.point_from_proportion(label_angle_rad / PI)
        dir_vec = point_on_arc - vertex
        dir_vec = dir_vec / np.linalg.norm(dir_vec)
        label_pos = point_on_arc + dir_vec * 0.6
        angle_label = MathTex(r"60^\circ", color=RED, font_size=32)
        angle_label.move_to(label_pos)
        self.objects["angle_label"] = angle_label

        # step_explanation
        step_explanation = Text("Placeholder for step narration.", color=BLUE_C, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/measuring_angle/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # signal_action: Indicate vertex
        self.play(Indicate(self.objects["vertex"], color=WHITE, run_time=1))
        # visual_action: Create ray_initial
        self.play(Create(self.objects["ray_initial"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/measuring_angle/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # signal_action: null
        # visual_action: Create ray_terminal
        self.play(Create(self.objects["ray_terminal"]), run_time=2.0)
        remaining_2 = max(0.1, 2.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/measuring_angle/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # signal_action: Circumscribe protractor_arc
        self.play(Circumscribe(self.objects["protractor_arc"], color=YELLOW, run_time=1))
        # visual_action: Create protractor_arc
        self.play(Create(self.objects["protractor_arc"]), run_time=2.0)
        remaining_3 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/measuring_angle/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # signal_action: Indicate protractor_labels
        self.play(Indicate(self.objects["protractor_labels"], color=YELLOW, run_time=1))
        # visual_action: Create protractor_ticks and protractor_labels
        self.play(
            Create(self.objects["protractor_ticks"]),
            Write(self.objects["protractor_labels"]),
            run_time=2.5
        )
        remaining_4 = max(0.1, 3.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/measuring_angle/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # signal_action: Indicate angle_arc_highlight
        self.play(Indicate(self.objects["angle_arc_highlight"], color=RED, run_time=1))
        # visual_action: Create angle_arc_highlight and Write angle_label
        self.play(
            Create(self.objects["angle_arc_highlight"]),
            Write(self.objects["angle_label"]),
            run_time=3.0
        )
        remaining_5 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))