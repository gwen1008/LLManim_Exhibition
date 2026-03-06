from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}  # Registry for all objects
        
        # Create zones for layout
        HEADER_ZONE = UP * 3.0
        CONTENT_ZONE = ORIGIN
        FOOTER_ZONE = DOWN * 3.0
        
        # Title
        title = Text("Measuring a 60° Angle", color=WHITE, font_size=40)
        title.move_to(HEADER_ZONE)
        self.objects["title"] = title
        
        # Vertex (anchor point at ORIGIN)
        vertex = ORIGIN
        
        # Ray VA (horizontal baseline)
        ray_va = Line(start=ORIGIN, end=[4, 0, 0], color=BLUE, stroke_width=6)
        ray_va.shift(vertex - ray_va.get_start())
        self.objects["ray_va"] = ray_va
        
        # Ray VB (60° from horizontal)
        # Coordinates: length=4, angle=60° => (4*cos60, 4*sin60) = (2, 3.464)
        ray_vb = Line(start=ORIGIN, end=[2, 3.464, 0], color=GREEN, stroke_width=6)
        ray_vb.shift(vertex - ray_vb.get_start())
        self.objects["ray_vb"] = ray_vb
        
        # Vertex Dot
        vertex_dot = Dot(point=vertex, radius=0.08, color=YELLOW)
        self.objects["vertex_dot"] = vertex_dot
        
        # Protractor Arc (semicircle, initially flat edge down)
        protractor_arc = Arc(
            radius=4.5,
            angle=PI,
            start_angle=-PI/2,
            color=LIGHT_GRAY,
            stroke_width=4,
            fill_opacity=0.2,
            fill_color=LIGHT_GRAY
        )
        protractor_arc.move_arc_center_to(vertex)
        self.objects["protractor_arc"] = protractor_arc
        
        # Protractor Baseline (diameter line)
        protractor_baseline = Line(
            start=[-4.5, 0, 0],
            end=[4.5, 0, 0],
            color=LIGHT_GRAY,
            stroke_width=2
        )
        protractor_baseline.move_to(vertex)
        self.objects["protractor_baseline"] = protractor_baseline
        
        # Angle Arc (for measurement highlight)
        angle_arc = Arc(
            radius=1.5,
            angle=60*DEGREES,
            start_angle=0,
            color=YELLOW,
            stroke_width=6
        )
        angle_arc.move_arc_center_to(vertex)
        self.objects["angle_arc"] = angle_arc
        
        # Measurement Label
        measurement_label = MathTex("60^\\circ", color=YELLOW, font_size=36)
        measurement_label.move_to(vertex + np.array([1.2, 0.8, 0]))
        self.objects["measurement_label"] = measurement_label
        
        # Step Explanation (dynamic text)
        step_explanation = Text("Step 1: Construct a 60° angle.", color=WHITE, font_size=28)
        step_explanation.move_to(FOOTER_ZONE)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "First, we construct a sixty-degree angle. We start with a vertex and draw the first ray horizontally to the right.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "title", "details": "Fade in the title."},
                "duration": 7.8,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "This ray will serve as our zero-degree reference, or baseline.",
                "signal_action": {"type": "Create", "target": "ray_va"},
                "visual_action": {"type": "Create", "target_id": "vertex_dot", "details": "Create the vertex dot and the first ray simultaneously."},
                "duration": 4.32,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, from the same vertex, we draw the second ray at a sixty-degree angle from the first.",
                "signal_action": {"type": "Create", "target": "ray_vb"},
                "visual_action": {"type": "UpdateText", "target_id": "step_explanation", "details": "Change explanation text to 'Step 2: Draw the second ray at 60°.'"},
                "duration": 6.024,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "To measure this angle, we use a protractor. Its center must coincide with the vertex, and its baseline must align with our first ray.",
                "signal_action": {"type": "Indicate", "target": "vertex_dot", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "protractor_baseline", "details": "Fade in the protractor's baseline, already aligned with ray_va."},
                "duration": 9.36,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "We place the semicircular scale over the angle. Notice how the zero-degree line matches our first ray.",
                "signal_action": {"type": "Create", "target": "protractor_arc"},
                "visual_action": {"type": "UpdateText", "target_id": "step_explanation", "details": "Change explanation text to 'Step 3: Align the protractor.'"},
                "duration": 7.248,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "Now we can read the measurement. The second ray passes through the sixty-degree mark on the scale.",
                "signal_action": {"type": "Create", "target": "angle_arc"},
                "visual_action": {"type": "Create", "target_id": "measurement_label", "details": "Draw a yellow arc between the rays and label it 60°."},
                "duration": 6.528,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "Therefore, we have demonstrated that the angle measures sixty degrees.",
                "signal_action": {"type": "Circumscribe", "target": "measurement_label", "color": "YELLOW"},
                "visual_action": {"type": "UpdateText", "target_id": "step_explanation", "details": "Change explanation text to 'Measurement: The angle is 60°.'"},
                "duration": 4.752,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_06.mp3"
            }
        ]
        
        for step in sequence:
            # === AUDIO (MANDATORY) ===
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            else:
                # Fallback path check (legacy support)
                step_num = step.get("step", 0)
                file_index = step_num - 1
                mp3_path = f"media/audio/step_{file_index:02d}.mp3"
                if os.path.exists(mp3_path):
                    self.add_sound(mp3_path)
                else:
                    wav_path = f"media/audio/step_{file_index:02d}.wav"
                    if os.path.exists(wav_path):
                        self.add_sound(wav_path)
            
            # Signal Action
            signal = step.get("signal_action")
            if signal is not None:
                signal_type = signal["type"]
                target_id = signal["target"]
                target_obj = self.objects[target_id]
                color_str = signal.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
                color = color_map.get(color_str, YELLOW)
                
                if signal_type == "Create":
                    self.play(Create(target_obj))
                elif signal_type == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal_type == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
            
            # Visual Action
            visual = step["visual_action"]
            action_type = visual["type"]
            target_id = visual["target_id"]
            target_obj = self.objects[target_id]
            
            if action_type == "Create":
                self.play(Create(target_obj))
            elif action_type == "UpdateText":
                # UpdateText means replace the Text object with new content
                if step["step"] == 3:
                    new_text = Text("Step 2: Draw the second ray at 60°.", color=WHITE, font_size=28)
                elif step["step"] == 5:
                    new_text = Text("Step 3: Align the protractor.", color=WHITE, font_size=28)
                elif step["step"] == 7:
                    new_text = Text("Measurement: The angle is 60°.", color=WHITE, font_size=28)
                else:
                    new_content = visual.get("details", "").strip("'")
                    new_text = Text(new_content, color=WHITE, font_size=28)
                
                # Position new text at the same place as old
                new_text.move_to(target_obj.get_center())
                self.play(ReplacementTransform(target_obj, new_text))
                # Update registry
                self.objects[target_id] = new_text
            
            # Calculate wait time
            animation_time = 1.0  # Default estimate for Create/Transform
            if signal and signal_type in ["Indicate", "Circumscribe"]:
                animation_time += 1.0
            remaining = step["duration"] - animation_time + 0.5
            if remaining > 0:
                self.wait(remaining)