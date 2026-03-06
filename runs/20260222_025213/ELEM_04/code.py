'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing how to construct and measure a 60° angle using a protractor.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for geometric construction (vertex, rays, protractor)
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Protractor arc is drawn in upper half-plane (y>=0). Explanation text is placed in footer zone to avoid overlap.
#    - Use VGroup for protractor elements for easy positioning.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show vertex O and its label.
#    - Step 2: Draw fixed ray OA (baseline) and indicate it.
#    - Step 3: Create protractor (arc, tick marks, label) and initial ray OB (overlapping OA).
#    - Step 4: Rotate ray OB to 60°, simultaneously drawing the angle arc, and indicate the 60° protractor label.
#    - Step 5: Show the angle label and circumscribe it for emphasis.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors
        title_anchor = 3.5 * UP
        global_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Object registry
        self.objects = {}
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Measuring a 60° Angle with a Protractor", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # vertex_O
        vertex_O = Dot(radius=0.08, color=WHITE)
        vertex_O.move_to(global_center)
        self.objects["vertex_O"] = vertex_O
        
        # label_O
        label_O = MathTex("O", color=WHITE, font_size=24)
        label_O.next_to(vertex_O, DOWN + LEFT, buff=0.15)
        self.objects["label_O"] = label_O
        
        # ray_OA
        ray_OA = Line(start=global_center, end=global_center + 3 * RIGHT, color="#1E90FF", stroke_width=6)
        self.objects["ray_OA"] = ray_OA
        
        # ray_OB_initial
        ray_OB_initial = Line(start=global_center, end=global_center + 3 * RIGHT, color="#FF6B6B", stroke_width=6)
        self.objects["ray_OB_initial"] = ray_OB_initial
        
        # protractor_arc
        protractor_arc = Arc(radius=2.5, start_angle=0, angle=PI, color=GRAY_B, stroke_width=3, stroke_opacity=0.9)
        protractor_arc.move_to(global_center)
        self.objects["protractor_arc"] = protractor_arc
        
        # protractor_0_line
        protractor_0_line = Line(start=2.5*RIGHT, end=2.7*RIGHT, color=GRAY_B, stroke_width=2)
        protractor_0_line.move_to(global_center)
        self.objects["protractor_0_line"] = protractor_0_line
        
        # protractor_60_line
        angle_rad = PI / 3
        start_60 = 2.5 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
        end_60 = 2.7 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
        protractor_60_line = Line(start=start_60, end=end_60, color=GRAY_B, stroke_width=2)
        protractor_60_line.move_to(global_center)
        self.objects["protractor_60_line"] = protractor_60_line
        
        # protractor_60_label
        label_pos = global_center + 2.9 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
        protractor_60_label = MathTex("60^\\circ", color=GRAY_B, font_size=20)
        protractor_60_label.move_to(label_pos)
        self.objects["protractor_60_label"] = protractor_60_label
        
        # angle_arc (initially invisible)
        angle_arc = Arc(radius=1.0, start_angle=0, angle=0, color=YELLOW, stroke_width=5)
        angle_arc.move_to(global_center)
        angle_arc.set_stroke(opacity=0)
        self.objects["angle_arc"] = angle_arc
        
        # angle_label (initially invisible)
        label_angle_pos = global_center + 1.3 * np.array([np.cos(30*DEGREES), np.sin(30*DEGREES), 0])
        angle_label = MathTex("60^\\circ", color=YELLOW, font_size=28)
        angle_label.move_to(label_angle_pos)
        angle_label.set_opacity(0)
        self.objects["angle_label"] = angle_label
        
        # step_explanation (placeholder, will be updated per step)
        step_explanation = Text("Placeholder for step text.", color=GRAY_C, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # Group protractor elements for easier handling in signal_action
        protractor_group = VGroup(protractor_arc, protractor_0_line, protractor_60_line, protractor_60_label)
        self.objects["protractor_group"] = protractor_group
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        step = {
            "step": 1,
            "narrative": "We begin with a point O, the vertex of our angle. From it, we draw a fixed ray along the zero-degree direction.",
            "signal_action": None,
            "visual_action": {
                "type": "Create",
                "target_id": "vertex_O",
                "details": "Fade in the vertex dot and its label."
            },
            "duration": 7.776,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_00.mp3"
        }
        
        # Audio
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Visual Action
        self.play(Create(self.objects["vertex_O"]), Write(self.objects["label_O"]))
        
        # Update explanation text (optional, but good for clarity)
        exp_text = Text(step["narrative"], color=GRAY_C, font_size=24, line_spacing=1.2)
        exp_text.move_to(explanation_anchor)
        exp_text.set_width(12)
        self.play(ReplacementTransform(self.objects["step_explanation"], exp_text))
        self.objects["step_explanation"] = exp_text
        
        animation_time = 2.0  # Approximate time for Create and Write
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))
        
        # Step 2
        step = {
            "step": 2,
            "narrative": "Now, we overlay a semicircular protractor, ensuring its center is at the vertex O and its baseline aligns with our fixed ray.",
            "signal_action": {
                "type": "Indicate",
                "target": "ray_OA",
                "color": "#1E90FF"
            },
            "visual_action": {
                "type": "Create",
                "target_id": "ray_OA",
                "details": "Draw the fixed blue ray OA."
            },
            "duration": 8.352,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_01.mp3"
        }
        
        # Audio
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = signal.get("color", "YELLOW")
            # Indicate expects a color constant, but we have a hex string. Use default YELLOW.
            self.play(Indicate(target_obj, color=YELLOW))
        
        # Visual Action
        self.play(Create(self.objects["ray_OA"]))
        
        # Update explanation
        exp_text = Text(step["narrative"], color=GRAY_C, font_size=24, line_spacing=1.2)
        exp_text.move_to(explanation_anchor)
        exp_text.set_width(12)
        self.play(ReplacementTransform(self.objects["step_explanation"], exp_text))
        self.objects["step_explanation"] = exp_text
        
        animation_time = 3.0  # Indicate + Create
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))
        
        # Step 3
        step = {
            "step": 3,
            "narrative": "The protractor provides a scale for measurement. Notice the 0° mark aligns with our fixed ray.",
            "signal_action": {
                "type": "Create",
                "target": [
                    "protractor_arc",
                    "protractor_0_line",
                    "protractor_60_line",
                    "protractor_60_label"
                ],
                "color": None
            },
            "visual_action": {
                "type": "Create",
                "target_id": "ray_OB_initial",
                "details": "Create the red ray OB, initially on top of OA. Then create the protractor elements (arc, 0° tick, 60° tick, 60° label)."
            },
            "duration": 6.984,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_02.mp3"
        }
        
        # Audio
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Visual Action: Create ray_OB_initial
        self.play(Create(self.objects["ray_OB_initial"]))
        
        # Signal Action: Create protractor elements (treated as part of visual action per JSON)
        # Since signal_action type is "Create", we interpret it as creating the listed objects.
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_ids = signal["target"]
            for tid in target_ids:
                obj = self.objects[tid]
                self.play(Create(obj))
        
        # Update explanation
        exp_text = Text(step["narrative"], color=GRAY_C, font_size=24, line_spacing=1.2)
        exp_text.move_to(explanation_anchor)
        exp_text.set_width(12)
        self.play(ReplacementTransform(self.objects["step_explanation"], exp_text))
        self.objects["step_explanation"] = exp_text
        
        animation_time = 4.0  # Create multiple objects
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))
        
        # Step 4
        step = {
            "step": 4,
            "narrative": "We now rotate the second ray. As it sweeps open, the angle between the rays increases. We stop precisely at the 60-degree mark on the protractor.",
            "signal_action": {
                "type": "Indicate",
                "target": "protractor_60_label",
                "color": "YELLOW"
            },
            "visual_action": {
                "type": "Animate",
                "target_id": "ray_OB_initial",
                "details": "Apply Rotate transformation to ray_OB_initial: Rotate(ray_OB_initial, angle=60*DEGREES, about_point=global_center). Simultaneously, animate the angle_arc's stroke_opacity from 0 to 1 and grow it from angle=0 to angle=60°."
            },
            "duration": 11.136,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_03.mp3"
        }
        
        # Audio
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = signal.get("color", "YELLOW")
            self.play(Indicate(target_obj, color=YELLOW))
        
        # Visual Action: Rotate ray and animate angle arc
        ray_OB = self.objects["ray_OB_initial"]
        angle_arc = self.objects["angle_arc"]
        
        # Create a copy of the arc with full angle and opacity for transformation
        angle_arc_final = Arc(radius=1.0, start_angle=0, angle=60*DEGREES, color=YELLOW, stroke_width=5)
        angle_arc_final.move_to(global_center)
        
        # Animate rotation and arc simultaneously
        self.play(
            Rotate(ray_OB, angle=60*DEGREES, about_point=global_center),
            Transform(angle_arc, angle_arc_final),
            run_time=4
        )
        
        # Update explanation
        exp_text = Text(step["narrative"], color=GRAY_C, font_size=24, line_spacing=1.2)
        exp_text.move_to(explanation_anchor)
        exp_text.set_width(12)
        self.play(ReplacementTransform(self.objects["step_explanation"], exp_text))
        self.objects["step_explanation"] = exp_text
        
        animation_time = 5.0  # Indicate + Rotate + Transform
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))
        
        # Step 5
        step = {
            "step": 5,
            "narrative": "The rotation is complete. The arc between the rays subtends a 60-degree angle, confirmed by the protractor scale. This visually demonstrates how a protractor measures an angle.",
            "signal_action": {
                "type": "Circumscribe",
                "target": "angle_label",
                "color": "YELLOW"
            },
            "visual_action": {
                "type": "Write",
                "target_id": "angle_label",
                "details": "Fade in the yellow '60°' label inside the angle arc."
            },
            "duration": 12.816,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_04.mp3"
        }
        
        # Audio
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Visual Action: Write angle label
        angle_label = self.objects["angle_label"]
        self.play(angle_label.animate.set_opacity(1))
        
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = signal.get("color", "YELLOW")
            self.play(Circumscribe(target_obj, color=YELLOW, run_time=1))
        
        # Update explanation
        exp_text = Text(step["narrative"], color=GRAY_C, font_size=24, line_spacing=1.2)
        exp_text.move_to(explanation_anchor)
        exp_text.set_width(12)
        self.play(ReplacementTransform(self.objects["step_explanation"], exp_text))
        self.objects["step_explanation"] = exp_text
        
        animation_time = 3.0  # Write + Circumscribe
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))
        
        # Final hold
        self.wait(max(0.1, 2))