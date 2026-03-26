from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create anchors based on layout plan
        title_anchor = UP * 3.5
        construction_anchor = ORIGIN
        explanation_anchor = DOWN * 3.0
        
        # Create all objects
        objects = {}
        
        # 1. Title
        title = Text("Constructing and Measuring a 60° Angle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        objects["title"] = title
        
        # 2. Vertex
        vertex = Dot(radius=0.08, color=YELLOW)
        vertex.move_to(construction_anchor)
        objects["vertex"] = vertex
        
        # 3. Ray1 (baseline)
        ray1 = Line(start=[0, 0, 0], end=[3, 0, 0], color=BLUE, stroke_width=6)
        ray1.move_to(construction_anchor)
        objects["ray1"] = ray1
        
        # 4. Ray1 label
        ray1_label = MathTex("A", color=BLUE, font_size=30)
        ray1_label.next_to(ray1.get_end(), RIGHT + DOWN, buff=0.15)
        objects["ray1_label"] = ray1_label
        
        # 5. Ray2 (60° angle)
        ray2 = Line(start=[0, 0, 0], end=[1.5, 2.598, 0], color=GREEN, stroke_width=6)
        ray2.move_to(construction_anchor)
        objects["ray2"] = ray2
        
        # 6. Ray2 label
        ray2_label = MathTex("B", color=GREEN, font_size=30)
        ray2_label.next_to(ray2.get_end(), UP + LEFT, buff=0.15)
        objects["ray2_label"] = ray2_label
        
        # 7. Protractor arc
        protractor_arc = Arc(radius=3.5, start_angle=0, angle=PI, 
                            color=LIGHT_GRAY, stroke_width=4, stroke_opacity=0.9)
        protractor_arc.move_to(construction_anchor)
        objects["protractor_arc"] = protractor_arc
        
        # 8. Protractor markings (VGroup)
        protractor_markings = VGroup()
        # Major degree markings: 0, 30, 60, 90, 120, 150, 180
        major_degrees = [0, 30, 60, 90, 120, 150, 180]
        for deg in major_degrees:
            angle_rad = deg * DEGREES
            # Tick mark
            start_point = protractor_arc.point_from_proportion(deg/180)
            end_point = start_point * 0.9  # Shorter for tick
            tick = Line(start=start_point, end=end_point, color=WHITE, stroke_width=2)
            protractor_markings.add(tick)
            
            # Label (position slightly inside)
            label_pos = start_point * 0.75
            label = MathTex(str(deg), color=WHITE, font_size=20)
            label.move_to(label_pos)
            protractor_markings.add(label)
        
        protractor_markings.move_to(construction_anchor)
        objects["protractor_markings"] = protractor_markings
        
        # 9. Angle arc
        angle_arc = Arc(radius=1.0, start_angle=0, angle=PI/3, 
                       color=YELLOW, stroke_width=8)
        angle_arc.move_to(construction_anchor)
        objects["angle_arc"] = angle_arc
        
        # 10. Angle label
        angle_label = MathTex("60^\\circ", color=YELLOW, font_size=36)
        angle_label.move_to(construction_anchor + np.array([1.2, 0.6, 0]))
        objects["angle_label"] = angle_label
        
        # 11. Step explanation
        step_explanation = Text("Step 1: Establish the baseline ray.", 
                               color=LIGHT_GRAY, font_size=28)
        step_explanation.move_to(explanation_anchor)
        objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We start by placing the vertex of our angle and drawing the first ray, which will serve as our baseline, or zero-degree reference.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "title", "details": "Fade in the title."},
                "duration": 7.896,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "First, we establish the vertex and the baseline ray.",
                "signal_action": {"type": "Indicate", "target": "vertex", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "vertex", "details": "Show the vertex dot."},
                "duration": 4.08,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "This ray, from the vertex to point A, defines our starting direction.",
                "signal_action": {"type": "Indicate", "target": "ray1", "color": "BLUE"},
                "visual_action": {"type": "Create", "target_id": "ray1", "details": "Draw the first ray. Then write its label."},
                "duration": 4.848,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "Now, we construct the second ray by rotating a copy of the first ray by 60 degrees counterclockwise about the vertex.",
                "signal_action": {"type": "Circumscribe", "target": "ray1", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "ray2", "details": "Animate the drawing of ray2. For clarity, this can be implemented as a Rotate transformation applied to a temporary copy of ray1."},
                "duration": 7.848,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "We now have our 60-degree angle. Let's verify this measurement by overlaying a protractor.",
                "signal_action": {"type": "Indicate", "target": "angle_arc", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "angle_arc", "details": "Draw the yellow arc between the two rays."},
                "duration": 7.176,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "The protractor's center is aligned with the vertex, and its baseline is aligned with our first ray.",
                "signal_action": {"type": "Indicate", "target": "protractor_arc", "color": "WHITE"},
                "visual_action": {"type": "Create", "target_id": "protractor_arc", "details": "Fade in the semicircular protractor outline."},
                "duration": 6.264,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "Its degree markings allow us to measure any angle. Let's find the 60-degree mark.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "protractor_markings", "details": "Fade in the major tick marks and labels (0, 30, 60, 90...)."},
                "duration": 6.624,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "As we can see, the second ray passes precisely through the 60-degree marking on the protractor, confirming our construction.",
                "signal_action": {"type": "Indicate", "target": "ray2", "color": "GREEN"},
                "visual_action": {"type": "Create", "target_id": "angle_label", "details": "Write the '60°' label next to the yellow arc."},
                "duration": 8.208,
                "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_07.mp3"
            }
        ]
        
        # Process each step
        for step in sequence:
            step_num = step["step"]
            
            # === AUDIO (MANDATORY) ===
            audio_file = None
            if "audio_path" in step and step["audio_path"]:
                audio_file = step["audio_path"]
            else:
                # Fallback path construction
                file_index = step_num - 1
                mp3_path = f"media/audio/step_{file_index:02d}.mp3"
                if os.path.exists(mp3_path):
                    audio_file = mp3_path
                else:
                    wav_path = f"media/audio/step_{file_index:02d}.wav"
                    audio_file = wav_path if os.path.exists(wav_path) else None
            
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # Update step explanation text
            if step_num > 1:
                new_text_content = f"Step {step_num}: {step['narrative']}"
                new_explanation = Text(new_text_content, color=LIGHT_GRAY, font_size=28)
                new_explanation.move_to(explanation_anchor)
                self.play(ReplacementTransform(objects["step_explanation"], new_explanation))
                objects["step_explanation"] = new_explanation
            
            # Handle signal action
            signal_action = step.get("signal_action")
            if signal_action is not None:
                target_id = signal_action["target"]
                signal_type = signal_action["type"]
                color_str = signal_action.get("color", "YELLOW")
                
                # Map color string to Manim color
                color_map = {
                    "YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE,
                    "WHITE": WHITE, "BLACK": BLACK, "LIGHT_GRAY": LIGHT_GRAY
                }
                color = color_map.get(color_str, YELLOW)
                
                target_obj = objects[target_id]
                
                if signal_type == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal_type == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal_type == "FocusOn":
                    self.play(FocusOn(target_obj))
            
            # Handle visual action
            visual_action = step["visual_action"]
            target_id = visual_action["target_id"]
            action_type = visual_action["type"]
            
            target_obj = objects[target_id]
            
            if action_type == "Create":
                # Special handling for ray2 (rotate animation)
                if target_id == "ray2":
                    # Create a temporary copy of ray1
                    temp_ray = ray1.copy()
                    self.add(temp_ray)
                    # Animate rotation
                    self.play(Rotate(temp_ray, angle=60*DEGREES, about_point=construction_anchor, run_time=2))
                    # Transform to final ray2
                    self.play(Transform(temp_ray, ray2))
                    self.remove(temp_ray)
                    self.add(ray2)
                    
                    # Also create ray2_label
                    self.play(Write(objects["ray2_label"]))
                elif target_id == "ray1":
                    self.play(Create(target_obj), Write(objects["ray1_label"]))
                elif target_id == "title":
                    self.play(Write(target_obj))
                else:
                    self.play(Create(target_obj))
            
            # Calculate wait time
            animation_time = 2.0 if target_id == "ray2" else 1.0  # Approximate animation times
            remaining = step["duration"] - animation_time + 0.5
            if remaining > 0:
                self.wait(remaining)
        
        # Final wait
        self.wait(2)