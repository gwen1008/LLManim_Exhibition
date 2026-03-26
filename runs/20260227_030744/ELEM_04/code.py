from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create anchors
        global_center = ORIGIN
        title_anchor = 3 * UP
        explanation_anchor = 3 * DOWN
        
        # Object registry
        self.objects = {}
        
        # Create title
        title = Text("Measuring a 60-Degree Angle with a Protractor", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Create vertex
        vertex = Dot(radius=0.08, color=WHITE)
        vertex.move_to(global_center)
        self.objects["vertex"] = vertex
        
        # Create ray1 (horizontal)
        ray1 = Line(start=[0, 0, 0], end=[3, 0, 0], color=BLUE, stroke_width=4)
        ray1.move_to(global_center)
        self.objects["ray1"] = ray1
        
        # Create ray2 (60 degrees)
        ray2 = Line(start=[0, 0, 0], end=[1.5, 2.598, 0], color=GREEN, stroke_width=4)
        ray2.move_to(global_center + UP*0.1 + RIGHT*0.1)
        self.objects["ray2"] = ray2
        
        # Create protractor arc
        protractor_arc = Arc(radius=2.5, start_angle=0, angle=PI, color=GRAY_B, stroke_width=3)
        protractor_arc.move_to(global_center)
        self.objects["protractor_arc"] = protractor_arc
        
        # Create protractor scale group (ticks and labels)
        protractor_scale_group = VGroup()
        radius = 2.5
        
        # Create tick marks (every 10 degrees, longer every 30)
        for angle_deg in range(0, 181, 10):
            angle_rad = angle_deg * DEGREES
            start_point = radius * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            
            # Determine tick length
            if angle_deg % 30 == 0:
                end_point = (radius - 0.3) * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
                # Add label for major ticks (0, 30, 60, 90, 120, 150, 180)
                if angle_deg <= 180:
                    label = MathTex(str(angle_deg) + "^\\circ", color=WHITE, font_size=24)
                    label_radius = radius - 0.5
                    label_pos = label_radius * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
                    label.move_to(label_pos)
                    protractor_scale_group.add(label)
            else:
                end_point = (radius - 0.15) * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            
            tick = Line(start=start_point, end=end_point, color=WHITE, stroke_width=2)
            protractor_scale_group.add(tick)
        
        protractor_scale_group.move_to(global_center)
        self.objects["protractor_scale_group"] = protractor_scale_group
        
        # Create angle arc (yellow highlight)
        angle_arc = Arc(radius=2.0, start_angle=0, angle=PI/3, color=YELLOW, stroke_width=6)
        angle_arc.set_stroke(opacity=0.7)
        angle_arc.move_to(global_center)
        self.objects["angle_arc"] = angle_arc
        
        # Create measurement label
        measurement_label = MathTex("60^\\circ", color=YELLOW, font_size=48)
        measurement_label.move_to(global_center + UP*1.5 + RIGHT*1.5)
        self.objects["measurement_label"] = measurement_label
        
        # Create step explanation (initial content)
        step_explanation = Text("Step 1: Drawing the angle.", color=GRAY_B, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/Create_an_animation__c572d4277f/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        # Update explanation text for step 1
        step1_text = Text("Step 1: Drawing the angle.", color=GRAY_B, font_size=24)
        step1_text.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], step1_text), run_time=0.5)
        self.objects["step_explanation"] = step1_text
        
        # Visual action: Create ray1
        self.play(Create(self.objects["ray1"]), run_time=1.5)
        remaining_1 = max(0.1, 6.696 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/Create_an_animation__c572d4277f/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Update explanation text for step 2
        step2_text = Text("Step 2: Forming the 60-degree angle.", color=GRAY_B, font_size=24)
        step2_text.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], step2_text), run_time=0.5)
        self.objects["step_explanation"] = step2_text
        
        # Signal action: Create vertex (simultaneously with ray2)
        # Visual action: Create ray2 and vertex
        self.play(
            Create(self.objects["vertex"]),
            Create(self.objects["ray2"]),
            run_time=2.0
        )
        remaining_2 = max(0.1, 6.504 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/Create_an_animation__c572d4277f/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Update explanation text for step 3
        step3_text = Text("Step 3: Placing the protractor center at the vertex.", color=GRAY_B, font_size=24)
        step3_text.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], step3_text), run_time=0.5)
        self.objects["step_explanation"] = step3_text
        
        # Signal action: Indicate ray1
        self.play(Indicate(self.objects["ray1"], color=BLUE, run_time=1.0))
        
        # Visual action: Create protractor_arc
        self.play(Create(self.objects["protractor_arc"]), run_time=2.0)
        remaining_3 = max(0.1, 10.32 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/Create_an_animation__c572d4277f/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Update explanation text for step 4
        step4_text = Text("Step 4: Adding the protractor scale.", color=GRAY_B, font_size=24)
        step4_text.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], step4_text), run_time=0.5)
        self.objects["step_explanation"] = step4_text
        
        # Signal action: Circumscribe protractor_arc
        self.play(Circumscribe(self.objects["protractor_arc"], color=WHITE, run_time=1.0))
        
        # Visual action: Create protractor_scale_group
        self.play(Create(self.objects["protractor_scale_group"]), run_time=3.0)
        remaining_4 = max(0.1, 12.408 - 1.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/Create_an_animation__c572d4277f/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Update explanation text for step 5
        step5_text = Text("Step 5: Reading the measurement: 60 degrees.", color=GRAY_B, font_size=24)
        step5_text.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], step5_text), run_time=0.5)
        self.objects["step_explanation"] = step5_text
        
        # Signal action: Indicate ray2
        self.play(Indicate(self.objects["ray2"], color=GREEN, run_time=1.0))
        
        # Visual action: Create angle_arc and Write measurement_label
        self.play(
            Create(self.objects["angle_arc"]),
            Write(self.objects["measurement_label"]),
            run_time=2.5
        )
        remaining_5 = max(0.1, 11.592 - 1.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final pause
        self.wait(max(0.1, 2))