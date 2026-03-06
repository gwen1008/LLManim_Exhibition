'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing how to measure a 60° angle using a protractor, showing the correspondence between geometric rotation and numerical measurement.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for protractor, angle, and rays
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Keep vertex at ORIGIN. Protractor arc radius (3) and ray length (3.5) chosen to fit within safe zone. Angle label placed at offset [1.2, 0.5, 0] to avoid overlapping rays/arc.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Draw_a_60_degree_ang_2bb286efd2/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show vertex.
#    - Step 2: Draw initial ray (0° baseline), signal with Indicate.
#    - Step 3: Draw protractor semicircle and center dot, signal center dot.
#    - Step 4: Rotate terminal ray 60° while sweeping out angle arc, signal ray.
#    - Step 5: Highlight angle arc with Circumscribe, write angle label.
'''

from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create anchors
        global_center = ORIGIN
        title_anchor = 3.5 * UP
        explanation_anchor = 3.5 * DOWN
        
        # Object registry
        self.objects = {}
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Measuring a 60° Angle with a Protractor", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # vertex
        vertex = Dot(radius=0.08, color=YELLOW)
        vertex.move_to(global_center)
        self.objects["vertex"] = vertex
        
        # ray_initial
        ray_initial = Line(start=[0,0,0], end=[3.5,0,0], color=BLUE, stroke_width=4)
        ray_initial.move_to(global_center)
        self.objects["ray_initial"] = ray_initial
        
        # protractor_semicircle
        # Note: LIGHT_GRAY is not a standard Manim color. Use GRAY_B or GRAY_C.
        protractor_semicircle = Arc(radius=3, start_angle=-PI/2, angle=PI, color=GRAY_B, stroke_width=3)
        protractor_semicircle.move_to(global_center)
        self.objects["protractor_semicircle"] = protractor_semicircle
        
        # protractor_center_dot
        protractor_center_dot = Dot(radius=0.05, color=WHITE)
        protractor_center_dot.move_to(global_center)
        self.objects["protractor_center_dot"] = protractor_center_dot
        
        # ray_terminal - initial state (0 degrees)
        ray_terminal = Line(start=[0,0,0], end=[3.5,0,0], color=GREEN, stroke_width=4)
        ray_terminal.move_to(global_center)
        self.objects["ray_terminal"] = ray_terminal
        
        # angle_arc - final state (60 degrees)
        angle_arc = Arc(radius=1.0, start_angle=0, angle=60*DEGREES, color=YELLOW, stroke_width=6)
        angle_arc.move_to(global_center)
        self.objects["angle_arc"] = angle_arc
        
        # angle_label
        angle_label = MathTex(r"60^\circ", color=YELLOW, font_size=36)
        angle_label.move_to(global_center + np.array([1.2, 0.5, 0]))
        self.objects["angle_label"] = angle_label
        
        # step_explanation
        step_explanation = Text("Step 1: Draw the vertex and the initial side (0° line).", color=GRAY_B, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/Draw_a_60_degree_ang_2bb286efd2/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        # signal_action: null
        # visual_action: Create vertex
        self.play(FadeIn(self.objects["vertex"]), run_time=1.5)
        remaining_1 = max(0.1, 7.032 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/Draw_a_60_degree_ang_2bb286efd2/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # signal_action: Indicate ray_initial
        self.play(Indicate(self.objects["ray_initial"], color=BLUE, run_time=1))
        # visual_action: Create ray_initial
        self.play(Create(self.objects["ray_initial"]), run_time=2.0)
        remaining_2 = max(0.1, 7.392 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/Draw_a_60_degree_ang_2bb286efd2/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # signal_action: Indicate protractor_center_dot
        self.play(Indicate(self.objects["protractor_center_dot"], color=WHITE, run_time=1))
        # visual_action: Create protractor_semicircle then center dot
        self.play(Create(self.objects["protractor_semicircle"]), run_time=2.5)
        self.play(FadeIn(self.objects["protractor_center_dot"]), run_time=0.5)
        remaining_3 = max(0.1, 9.432 - 1.0 - 2.5 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/Draw_a_60_degree_ang_2bb286efd2/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # signal_action: Indicate ray_terminal
        self.play(Indicate(self.objects["ray_terminal"], color=GREEN, run_time=1))
        
        # visual_action: Rotate ray_terminal and create angle_arc from 0 to 60 degrees
        # Create a starting arc with angle=0 (or near zero for stability)
        start_arc = Arc(radius=1.0, start_angle=0, angle=0.001, color=YELLOW, stroke_width=6)
        start_arc.move_to(global_center)
        
        # Rotate the terminal ray
        rotation_animation = Rotate(self.objects["ray_terminal"], angle=60*DEGREES, about_point=global_center, run_time=3.0)
        # Transform the arc from 0 to 60 degrees
        arc_animation = Transform(start_arc, self.objects["angle_arc"], run_time=3.0)
        
        self.play(rotation_animation, arc_animation)
        # Add the final arc to the scene for later reference
        self.add(self.objects["angle_arc"])
        self.remove(start_arc)
        
        remaining_4 = max(0.1, 10.728 - 1.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/Draw_a_60_degree_ang_2bb286efd2/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # signal_action: Circumscribe angle_arc
        self.play(Circumscribe(self.objects["angle_arc"], color=YELLOW, run_time=1))
        # visual_action: Write angle_label
        self.play(Write(self.objects["angle_label"]), run_time=1.5)
        remaining_5 = max(0.1, 13.224 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final hold
        self.wait(max(0.1, 2))