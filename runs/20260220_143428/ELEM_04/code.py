from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create objects from layout_plan
        # Title
        title = Text("Constructing and Measuring a 60° Angle", color=WHITE, font_size=36)
        self.objects["title"] = title
        
        # Step text (initial)
        step_text = Text("Step 1: Place the vertex.", color=GRAY_B, font_size=24)
        self.objects["step_text"] = step_text
        
        # Vertex dot
        vertex_dot = Dot(radius=0.08, color=YELLOW)
        self.objects["vertex_dot"] = vertex_dot
        
        # Ray 1 (baseline)
        ray1 = Line(start=[0, 0, 0], end=[3, 0, 0], color=BLUE, stroke_width=6)
        self.objects["ray1"] = ray1
        
        # Ray 2 (initial short segment)
        ray2 = Line(start=[0, 0, 0], end=[0.1, 0, 0], color=GREEN, stroke_width=6)
        self.objects["ray2"] = ray2
        
        # Protractor arc
        protractor_arc = Arc(radius=3.5, start_angle=0, angle=PI, color=WHITE, stroke_width=2)
        protractor_arc.set_stroke(opacity=0.7)
        self.objects["protractor_arc"] = protractor_arc
        
        # Protractor center dot
        protractor_center_dot = Dot(radius=0.05, color=RED, fill_opacity=0.8)
        self.objects["protractor_center_dot"] = protractor_center_dot
        
        # Degree mark at 60°
        angle_rad = PI/3  # 60 degrees
        degree_mark_60 = Line(
            start=[0, 0, 0],
            end=[3.5 * np.cos(angle_rad), 3.5 * np.sin(angle_rad), 0],
            color=YELLOW,
            stroke_width=3
        )
        degree_mark_60.set_stroke(opacity=0.0)
        self.objects["degree_mark_60"] = degree_mark_60
        
        # Angle arc
        angle_arc = Arc(radius=1.0, start_angle=0, angle=angle_rad, color=YELLOW, stroke_width=5)
        angle_arc.set_stroke(opacity=0.0)
        self.objects["angle_arc"] = angle_arc
        
        # 60° label
        label_pos = np.array([np.cos(angle_rad/2), np.sin(angle_rad/2), 0]) * 1.3
        label_60 = MathTex("60^\\circ", color=YELLOW, font_size=36)
        label_60.move_to(label_pos)
        self.objects["label_60"] = label_60
        
        # Use LayoutEngine for positioning
        from utils.layout_engine import LayoutEngine, LayoutObject
        
        layout = LayoutEngine()
        
        # Create layout objects
        obj_title = LayoutObject(title, "title")
        obj_step = LayoutObject(step_text, "step_text")
        obj_vertex = LayoutObject(vertex_dot, "vertex_dot")
        obj_ray1 = LayoutObject(ray1, "ray1")
        obj_ray2 = LayoutObject(ray2, "ray2")
        obj_protractor_arc = LayoutObject(protractor_arc, "protractor_arc")
        obj_protractor_dot = LayoutObject(protractor_center_dot, "protractor_center_dot")
        obj_degree_mark = LayoutObject(degree_mark_60, "degree_mark_60")
        obj_angle_arc = LayoutObject(angle_arc, "angle_arc")
        obj_label = LayoutObject(label_60, "label_60")
        
        # Add to layout
        layout.add(obj_title)
        layout.add(obj_step)
        layout.add(obj_vertex)
        layout.add(obj_ray1)
        layout.add(obj_ray2)
        layout.add(obj_protractor_arc)
        layout.add(obj_protractor_dot)
        layout.add(obj_degree_mark)
        layout.add(obj_angle_arc)
        layout.add(obj_label)
        
        # Add to zones
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_to_zone(obj_step, "FOOTER")
        layout.add_to_zone(obj_vertex, "CONTENT")
        layout.add_to_zone(obj_ray1, "CONTENT")
        layout.add_to_zone(obj_ray2, "CONTENT")
        layout.add_to_zone(obj_protractor_arc, "CONTENT")
        layout.add_to_zone(obj_protractor_dot, "CONTENT")
        layout.add_to_zone(obj_degree_mark, "CONTENT")
        layout.add_to_zone(obj_angle_arc, "CONTENT")
        layout.add_to_zone(obj_label, "CONTENT")
        
        # Center all content objects at ORIGIN
        layout.add_constraint(obj_vertex.center_x == 0)
        layout.add_constraint(obj_vertex.center_y == 0)
        layout.align_to(obj_ray1, obj_vertex, "CENTER")
        layout.align_to(obj_ray2, obj_vertex, "CENTER")
        layout.align_to(obj_protractor_arc, obj_vertex, "CENTER")
        layout.align_to(obj_protractor_dot, obj_vertex, "CENTER")
        layout.align_to(obj_degree_mark, obj_vertex, "CENTER")
        layout.align_to(obj_angle_arc, obj_vertex, "CENTER")
        
        # Solve layout
        layout.solve()
        
        # Send protractor to back (z-index)
        protractor_arc.set_z_index(-1)
        protractor_center_dot.set_z_index(-1)
        degree_mark_60.set_z_index(-1)
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We begin with a point, the vertex of our angle.",
                "signal_action": {"type": "Indicate", "target": "vertex_dot", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "vertex_dot", "details": "Fade in the yellow vertex dot."},
                "duration": 3.624,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "From the vertex, we draw the first ray, establishing our baseline.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "ray1", "details": "Draw the blue horizontal ray from the vertex to (3,0,0)."},
                "duration": 4.944,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, we construct the second ray. It starts aligned with the first and sweeps open...",
                "signal_action": None,
                "visual_action": {"type": "GrowFromPoint", "target_id": "ray2", "details": "Extend the green ray from the vertex to its full length at 0° (temporarily)."},
                "duration": 6.144,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "... until it forms a 60-degree angle with the baseline.",
                "signal_action": None,
                "visual_action": {"type": "Rotate", "target_id": "ray2", "details": "Animate the green ray rotating counter-clockwise from 0° to 60° around the vertex. Simultaneously, update its end point to (1.5, 2.598, 0)."},
                "duration": 4.32,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "To measure this angle, we overlay a semicircular protractor, aligning its center with the vertex and its baseline with our first ray.",
                "signal_action": {"type": "Indicate", "target": "protractor_center_dot", "color": "RED"},
                "visual_action": {"type": "FadeIn", "target_id": "protractor_arc", "details": "Fade in the protractor arc and center dot. Use `protractor_arc.send_to_back()` to place it behind the rays."},
                "duration": 8.328,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "Now we verify: the second ray aligns precisely with the 60-degree marking on the protractor.",
                "signal_action": {"type": "Circumscribe", "target": "degree_mark_60", "color": "YELLOW"},
                "visual_action": {"type": "AnimationGroup", "target_id": None, "details": "Simultaneously: 1) Set stroke_opacity of `degree_mark_60` to 1.0, 2) Create the `angle_arc` (set its opacity to 1.0), 3) Write the `label_60`."},
                "duration": 6.792,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "This confirms our constructed angle measures exactly 60 degrees.",
                "signal_action": {"type": "Indicate", "target": "label_60", "color": "YELLOW"},
                "visual_action": {"type": "Wait", "target_id": None, "details": "Hold the final frame for emphasis."},
                "duration": 4.848,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_06.mp3"
            }
        ]
        
        # Step 0: Add title and initial step text
        self.play(Write(title), Write(step_text))
        self.wait(max(0.1, 0.5))
        
        for step in sequence:
            step_num = step["step"]
            
            # === AUDIO ===
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # === SIGNAL ACTION ===
            if step.get("signal_action") is not None:
                signal = step["signal_action"]
                signal_type = signal["type"]
                target_id = signal["target"]
                color_str = signal.get("color", "YELLOW")
                
                target_obj = self.objects[target_id]
                color = eval(color_str) if hasattr(self, color_str) else YELLOW
                
                if signal_type == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal_type == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal_type == "FocusOn":
                    self.play(FocusOn(target_obj))
            
            # === VISUAL ACTION ===
            visual = step["visual_action"]
            action_type = visual["type"]
            target_id = visual.get("target_id")
            
            if action_type == "Create":
                target_obj = self.objects[target_id]
                self.play(Create(target_obj))
                animation_time = 1.0
                
            elif action_type == "GrowFromPoint":
                target_obj = self.objects[target_id]
                # First extend ray2 to full length at 0°
                ray2_full = Line(start=[0, 0, 0], end=[3, 0, 0], color=GREEN, stroke_width=6)
                ray2_full.move_to(self.objects["vertex_dot"].get_center())
                self.play(Transform(target_obj, ray2_full))
                self.objects["ray2"] = ray2_full  # Update reference
                animation_time = 1.5
                
            elif action_type == "Rotate":
                target_obj = self.objects[target_id]
                # Create the final ray at 60°
                final_end = np.array([1.5, 2.598076211, 0])  # 3 * cos(60°), 3 * sin(60°)
                ray2_final = Line(start=[0, 0, 0], end=final_end, color=GREEN, stroke_width=6)
                ray2_final.move_to(self.objects["vertex_dot"].get_center())
                
                # Rotate animation
                self.play(Rotate(target_obj, angle=PI/3, about_point=target_obj.get_start(), run_time=2))
                # Transform to final position
                self.play(Transform(target_obj, ray2_final))
                self.objects["ray2"] = ray2_final  # Update reference
                animation_time = 3.0
                
            elif action_type == "FadeIn":
                if target_id == "protractor_arc":
                    # Fade in both protractor arc and center dot
                    self.play(
                        FadeIn(self.objects["protractor_arc"]),
                        FadeIn(self.objects["protractor_center_dot"])
                    )
                    # Ensure they stay behind rays
                    self.objects["protractor_arc"].set_z_index(-1)
                    self.objects["protractor_center_dot"].set_z_index(-1)
                animation_time = 1.5
                
            elif action_type == "AnimationGroup":
                # Show degree mark, angle arc, and label simultaneously
                degree_mark = self.objects["degree_mark_60"]
                angle_arc_obj = self.objects["angle_arc"]
                label = self.objects["label_60"]
                
                # Set opacities to 1
                degree_mark.set_stroke(opacity=1.0)
                angle_arc_obj.set_stroke(opacity=1.0)
                
                self.play(
                    degree_mark.animate.set_stroke(opacity=1.0),
                    Create(angle_arc_obj),
                    Write(label)
                )
                animation_time = 2.0
                
            elif action_type == "Wait":
                # Just wait, no animation
                animation_time = 0
                
            else:
                animation_time = 0
            
            # === UPDATE STEP TEXT ===
            if step_num > 1:
                new_text_content = f"Step {step_num}: {step['narrative']}"
                new_step_text = Text(new_text_content, color=GRAY_B, font_size=24)
                new_step_text.move_to(self.objects["step_text"].get_center())
                self.play(ReplacementTransform(self.objects["step_text"], new_step_text))
                self.objects["step_text"] = new_step_text
            
            # === WAIT FOR REMAINING AUDIO ===
            remaining = step["duration"] - animation_time + 0.5
            if remaining > 0:
                self.wait(max(0.1, max(0.1, remaining)))
        
        # Final wait
        self.wait(max(0.1, 2))