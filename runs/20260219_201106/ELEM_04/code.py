from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Object Creation ==========
        self.objects = {}
        
        # Title
        title = Text("Constructing and Measuring a 60° Angle", color=WHITE, font_size=40)
        title.to_edge(UP, buff=0.5)
        self.objects["title"] = title
        
        # Step Explanation
        step_explanation = Text("Step 1: Establish the baseline (0° ray).", color=LIGHT_GRAY, font_size=28)
        step_explanation.to_edge(DOWN, buff=0.5)
        self.objects["step_explanation"] = step_explanation
        
        # Vertex
        vertex = Dot(radius=0.08, color=WHITE)
        vertex.move_to(ORIGIN)
        self.objects["vertex"] = vertex
        
        # Ray1 (baseline)
        ray1 = Line(start=ORIGIN, end=3*RIGHT, color=BLUE, stroke_width=6)
        self.objects["ray1"] = ray1
        
        # Sweeping line (initially overlaps ray1)
        sweeping_line = Line(start=ORIGIN, end=3*RIGHT, color=YELLOW, stroke_width=4, stroke_opacity=0.9)
        self.objects["sweeping_line"] = sweeping_line
        
        # Ray2 (60° ray) - pre-calculated end point: 3 * (cos(60°), sin(60°), 0)
        ray2_end = 3 * np.array([np.cos(PI/3), np.sin(PI/3), 0])
        ray2 = Line(start=ORIGIN, end=ray2_end, color=GREEN, stroke_width=6)
        self.objects["ray2"] = ray2
        
        # Protractor arc (semicircle)
        protractor_arc = Arc(radius=3.5, start_angle=0, angle=PI, color=LIGHT_GRAY, stroke_width=3, stroke_opacity=0.7)
        protractor_arc.move_to(ORIGIN)
        self.objects["protractor_arc"] = protractor_arc
        
        # Protractor center dot
        protractor_center_dot = Dot(radius=0.06, color=RED, fill_opacity=0.8)
        protractor_center_dot.move_to(ORIGIN)
        self.objects["protractor_center_dot"] = protractor_center_dot
        
        # Degree markings (VGroup of ticks and labels)
        degree_markings = VGroup()
        for angle_deg in [0, 30, 60, 90, 120, 150, 180]:
            angle_rad = angle_deg * DEGREES
            # Tick line
            start_point = 3.5 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            end_point = 3.3 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            tick = Line(start=start_point, end=end_point, color=WHITE, stroke_width=2)
            # Label
            if angle_deg in [0, 30, 60, 90, 120, 150, 180]:
                label_pos = 3.1 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
                # Adjust label position for readability
                if angle_deg == 0:
                    label_pos += 0.2 * DOWN
                elif angle_deg == 180:
                    label_pos += 0.2 * DOWN
                elif angle_deg == 90:
                    label_pos += 0.2 * LEFT
                label = MathTex(f"{angle_deg}^\\circ", color=WHITE, font_size=24).move_to(label_pos)
                degree_markings.add(tick, label)
            else:
                degree_markings.add(tick)
        self.objects["degree_markings"] = degree_markings
        
        # Label 60°
        label_60_pos = 3.5 * 0.8 * np.array([np.cos(PI/3), np.sin(PI/3), 0]) + np.array([0, 0.3, 0])
        label_60 = MathTex("60^\\circ", color=YELLOW, font_size=36).move_to(label_60_pos)
        self.objects["label_60"] = label_60
        
        # Verification arrow (from label to ray end)
        arrow_start = label_60.get_center()
        arrow_end = ray2_end + np.array([-0.2, -0.2, 0])
        verification_arrow = CurvedArrow(start_point=arrow_start, end_point=arrow_end, color=YELLOW, stroke_width=3)
        self.objects["verification_arrow"] = verification_arrow
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We start by placing the vertex of our angle and establishing a horizontal baseline, which will represent 0 degrees.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "vertex", "details": "Fade in the vertex dot."},
                "duration": 7.272,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "From the vertex, we draw our first ray extending to the right. This is our reference line.",
                "signal_action": {"type": "Indicate", "target": "vertex", "color": "RED"},
                "visual_action": {"type": "Create", "target_id": "ray1", "details": "Draw the blue horizontal ray."},
                "duration": 6.48,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, to create a 60-degree angle, we animate a line sweeping from the baseline.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "sweeping_line", "details": "Fade in the yellow sweeping line (initially overlapping ray1)."},
                "duration": 6.312,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "The line rotates 60 degrees counter-clockwise, defining our second ray.",
                "signal_action": {"type": "Indicate", "target": "sweeping_line", "color": "YELLOW"},
                "visual_action": {"type": "Rotate", "target_id": "sweeping_line", "details": "Rotate sweeping_line about the vertex from 0 to 60 degrees (PI/3 radians)."},
                "duration": 5.304,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "We solidify this position as our second ray. The angle between the blue and green rays is now 60 degrees.",
                "signal_action": None,
                "visual_action": {"type": "ReplacementTransform", "target_id": "sweeping_line", "details": "Transform the yellow sweeping_line into the permanent green ray2. Then fade out sweeping_line."},
                "duration": 7.824,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "To verify the measurement, we overlay a semicircular protractor. Its center must align precisely with the vertex.",
                "signal_action": {"type": "Indicate", "target": "vertex", "color": "RED"},
                "visual_action": {"type": "Create", "target_id": "protractor_arc", "details": "Fade in the gray protractor arc."},
                "duration": 8.4,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "The protractor's 0-degree line is aligned with our baseline ray. Its center dot coincides with our vertex.",
                "signal_action": [
                    {"type": "Circumscribe", "target": "ray1", "color": "BLUE"},
                    {"type": "Create", "target": "protractor_center_dot"}
                ],
                "visual_action": {"type": "Create", "target_id": "degree_markings", "details": "Fade in the degree ticks and labels (0°, 30°, 60°, etc.) on the arc."},
                "duration": 7.944,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "Finally, we verify the measurement. The green ray passes exactly through the 60-degree marking on the protractor.",
                "signal_action": {"type": "Indicate", "target": "ray2", "color": "GREEN"},
                "visual_action": [
                    {"type": "Write", "target_id": "label_60", "details": "Write the '60°' label near the 60° tick mark."},
                    {"type": "Create", "target_id": "verification_arrow", "details": "Draw a curved arrow from the label to the ray."}
                ],
                "duration": 8.256,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_07.mp3"
            }
        ]

        # Initial display of title and step explanation
        self.play(Write(title), Write(step_explanation))
        self.wait(0.5)

        for step in sequence:
            step_num = step["step"]
            audio_file = step.get("audio_path")
            
            # Audio
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # Update step explanation if narrative changed
            if step_num > 1:
                new_text = step["narrative"]
                new_explanation = Text(new_text, color=LIGHT_GRAY, font_size=28)
                new_explanation.move_to(step_explanation.get_center())
                self.play(ReplacementTransform(step_explanation, new_explanation))
                step_explanation = new_explanation
                self.objects["step_explanation"] = new_explanation
            
            # Signal Action
            signal_action = step.get("signal_action")
            if signal_action is not None:
                if isinstance(signal_action, list):
                    for sig in signal_action:
                        self._execute_signal_action(sig)
                else:
                    self._execute_signal_action(signal_action)
            
            # Visual Action
            visual_action = step["visual_action"]
            
            # Handle both single and multiple visual actions
            if isinstance(visual_action, list):
                # Multiple visual actions (step 8)
                anim_time = 0
                for vis in visual_action:
                    sub_action_type = vis["type"]
                    sub_target_id = vis["target_id"]
                    sub_obj = self.objects[sub_target_id]
                    
                    if sub_action_type == "Write":
                        self.play(Write(sub_obj))
                        anim_time += 1.0
                    elif sub_action_type == "Create":
                        self.play(Create(sub_obj))
                        anim_time += 1.0
            else:
                # Single visual action
                target_id = visual_action["target_id"]
                action_type = visual_action["type"]
                
                if action_type == "Create":
                    obj = self.objects[target_id]
                    self.play(Create(obj))
                    anim_time = 1.0
                elif action_type == "Rotate":
                    obj = self.objects[target_id]
                    self.play(Rotate(obj, angle=PI/3, about_point=ORIGIN, run_time=2.0, rate_func=smooth))
                    anim_time = 2.0
                elif action_type == "ReplacementTransform":
                    src = self.objects[target_id]
                    tgt = self.objects["ray2"]
                    self.play(ReplacementTransform(src, tgt))
                    anim_time = 1.5
                    # Fade out the original sweeping_line (now transformed)
                    self.play(FadeOut(src))
                    anim_time += 0.5
                else:
                    anim_time = 1.0  # default
            
            # Wait for remaining audio duration
            remaining = step["duration"] - anim_time + 0.5
            if remaining > 0:
                self.wait(remaining)
        
        # Final hold
        self.wait(2)

    def _execute_signal_action(self, signal):
        sig_type = signal["type"]
        target_id = signal["target"]
        color_str = signal.get("color", "YELLOW")
        
        color_map = {
            "YELLOW": YELLOW,
            "RED": RED,
            "GREEN": GREEN,
            "BLUE": BLUE
        }
        color = color_map.get(color_str, YELLOW)
        
        target_obj = self.objects[target_id]
        
        if sig_type == "Circumscribe":
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        elif sig_type == "Indicate":
            self.play(Indicate(target_obj, color=color))
        elif sig_type == "Create":
            self.play(Create(target_obj))