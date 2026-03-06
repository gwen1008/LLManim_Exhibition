'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the process of measuring a 60-degree angle using a protractor.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Measuring a 60-Degree Angle"
#    - Main Content: [Center y=0] for the angle, rays, protractor, and label.
#    - Footer Region: [Bottom y=-3.5] for step explanation text.
# 3. Anti-Overlap Check:
#    - The protractor (radius 2.5) and rays (length 3) fit within the main content zone.
#    - The angle label is placed at an offset [1.2, 0.6, 0] from the vertex to avoid overlap.
#    - Footer text is scaled to 0.8 to fit width.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/angle_measurement/step_XX.mp3"
# 5. Animation Flow:
#    Step 1: Indicate vertex, create horizontal ray.
#    Step 2: Create 60-degree ray.
#    Step 3: Indicate vertex, create protractor semicircle.
#    Step 4: Create yellow angle arc.
#    Step 5: Circumscribe arc, write "60°" label.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/final_narrative.mp3")  # [auto-injected: full narration]
        self.camera.background_color = "#1e1e1e"
        
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        global_center = ORIGIN
        footer_anchor = 3.5 * DOWN
        
        # Object registry
        self.objects = {}
        
        # Create title
        title = Text("Measuring a 60-Degree Angle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Create vertex
        vertex = Dot(point=ORIGIN, color=WHITE, radius=0.08)
        vertex.move_to(global_center)
        self.objects["vertex"] = vertex
        
        # Create ray_horizontal
        ray_horizontal = Line(start=ORIGIN, end=[3, 0, 0], color=WHITE, stroke_width=4)
        ray_horizontal.move_to(global_center)
        self.objects["ray_horizontal"] = ray_horizontal
        
        # Create ray_60
        ray_60 = Line(start=ORIGIN, end=[1.5, 2.598, 0], color=WHITE, stroke_width=4)
        ray_60.move_to(global_center)
        self.objects["ray_60"] = ray_60
        
        # Create protractor_semicircle
        protractor_semicircle = Arc(radius=2.5, start_angle=0, angle=PI, color="#AAAAAA", stroke_width=3)
        protractor_semicircle.set_stroke(opacity=0.7)
        protractor_semicircle.move_to(global_center)
        self.objects["protractor_semicircle"] = protractor_semicircle
        
        # Create angle_arc
        angle_arc = Arc(radius=1.0, start_angle=0, angle=PI/3, color=YELLOW, stroke_width=6)
        angle_arc.move_to(global_center)
        self.objects["angle_arc"] = angle_arc
        
        # Create angle_label
        angle_label = MathTex(r"60^\circ", color=GREEN, font_size=36)
        angle_label.move_to(global_center + np.array([1.2, 0.6, 0]))
        self.objects["angle_label"] = angle_label
        
        # Create step_explanation (placeholder, will be updated per step)
        step_explanation = Text("Placeholder for step text.", color=GRAY_B, font_size=28)
        step_explanation.move_to(footer_anchor)
        step_explanation.scale(0.8)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/angle_measurement/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        # Signal action: Indicate vertex
        self.play(Indicate(self.objects["vertex"], color=YELLOW, run_time=1))
        # Visual action: Create ray_horizontal
        self.play(Create(self.objects["ray_horizontal"]), run_time=1.5)
        # Update step explanation
        step1_text = Text("We begin with the two rays that form our angle, sharing a common vertex.", color=GRAY_B, font_size=28)
        step1_text.move_to(footer_anchor).scale(0.8)
        self.play(Transform(self.objects["step_explanation"], step1_text))
        self.objects["step_explanation"] = step1_text
        
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/angle_measurement/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # No signal action
        # Visual action: Create ray_60
        self.play(Create(self.objects["ray_60"]), run_time=2.0)
        # Update step explanation
        step2_text = Text("The second ray is rotated 60 degrees counterclockwise from the first.", color=GRAY_B, font_size=28)
        step2_text.move_to(footer_anchor).scale(0.8)
        self.play(Transform(self.objects["step_explanation"], step2_text))
        self.objects["step_explanation"] = step2_text
        
        remaining_2 = max(0.1, 2.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/angle_measurement/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Indicate vertex
        self.play(Indicate(self.objects["vertex"], color=YELLOW, run_time=1))
        # Visual action: Create protractor_semicircle
        self.play(Create(self.objects["protractor_semicircle"]), run_time=2.5)
        # Update step explanation
        step3_text = Text("To measure this angle, we overlay a semicircular protractor, aligning its center precisely with the vertex.", color=GRAY_B, font_size=28)
        step3_text.move_to(footer_anchor).scale(0.8)
        self.play(Transform(self.objects["step_explanation"], step3_text))
        self.objects["step_explanation"] = step3_text
        
        remaining_3 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/angle_measurement/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # No signal action
        # Visual action: Create angle_arc
        self.play(Create(self.objects["angle_arc"]), run_time=2.5)
        # Update step explanation
        step4_text = Text("The angle's opening corresponds to an arc on the protractor. Let's highlight this arc.", color=GRAY_B, font_size=28)
        step4_text.move_to(footer_anchor).scale(0.8)
        self.play(Transform(self.objects["step_explanation"], step4_text))
        self.objects["step_explanation"] = step4_text
        
        remaining_4 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/angle_measurement/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe angle_arc
        self.play(Circumscribe(self.objects["angle_arc"], color=YELLOW, run_time=1))
        # Visual action: Write angle_label
        self.play(Write(self.objects["angle_label"]), run_time=1.5)
        # Update step explanation
        step5_text = Text("Where this arc meets the protractor's scale, we read the measurement: sixty degrees.", color=GRAY_B, font_size=28)
        step5_text.move_to(footer_anchor).scale(0.8)
        self.play(Transform(self.objects["step_explanation"], step5_text))
        self.objects["step_explanation"] = step5_text
        
        remaining_5 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final hold
        self.wait(max(0.1, 2))