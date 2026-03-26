from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for all objects
        self.objects = {}
        
        # Define key anchor positions from layout_plan
        title_anchor = 3.5 * UP
        scale_center = ORIGIN
        left_pan_center = 3 * LEFT + 1 * DOWN
        right_pan_center = 3 * RIGHT + 1 * DOWN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Scale Structure
        beam = Line(start=4*LEFT, end=4*RIGHT, color=LIGHT_GRAY, stroke_width=8)
        beam.move_to(scale_center + 0.5*UP)
        self.objects["beam"] = beam
        
        # FIXED: Triangle doesn't accept height/width parameters, use scale instead
        fulcrum = Triangle(color=GRAY, fill_opacity=1)
        fulcrum.scale(0.3)  # Adjusted scale to approximate the desired size
        fulcrum.move_to(scale_center + 0.5*UP)
        self.objects["fulcrum"] = fulcrum
        
        left_pan = Circle(radius=0.8, color=LIGHT_GRAY, fill_opacity=0.2, stroke_width=3)
        left_pan.move_to(left_pan_center)
        self.objects["left_pan"] = left_pan
        
        right_pan = Circle(radius=0.8, color=LIGHT_GRAY, fill_opacity=0.2, stroke_width=3)
        right_pan.move_to(right_pan_center)
        self.objects["right_pan"] = right_pan
        
        left_string = Line(
            start=4*LEFT + 0.5*UP,
            end=left_pan.get_center() + 0.8*UP,
            color=LIGHT_GRAY,
            stroke_width=3
        )
        self.objects["left_string"] = left_string
        
        right_string = Line(
            start=4*RIGHT + 0.5*UP,
            end=right_pan.get_center() + 0.8*UP,
            color=LIGHT_GRAY,
            stroke_width=3
        )
        self.objects["right_string"] = right_string
        
        # Left side boxes and labels
        box1 = Square(side_length=0.7, color=BLUE, fill_opacity=0.7, stroke_width=2)
        box1.move_to(left_pan_center + 0.4*UP)
        self.objects["box1"] = box1
        
        box2 = Square(side_length=0.7, color=BLUE, fill_opacity=0.7, stroke_width=2)
        box2.move_to(left_pan_center + 0.4*DOWN)
        self.objects["box2"] = box2
        
        box_label_initial = MathTex("x", color=WHITE, font_size=24)
        box_label_initial.move_to(box1.get_center())
        self.objects["box_label_initial"] = box_label_initial
        
        box_label_initial2 = MathTex("x", color=WHITE, font_size=24)
        box_label_initial2.move_to(box2.get_center())
        self.objects["box_label_initial2"] = box_label_initial2
        
        left_group_label = MathTex("2x", color=YELLOW, font_size=30)
        left_group_label.next_to(left_pan, LEFT, buff=0.5)
        self.objects["left_group_label"] = left_group_label
        
        # Right side circles
        circle1 = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle1.move_to(right_pan_center + 0.6*LEFT + 0.3*UP)
        self.objects["circle1"] = circle1
        
        circle2 = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle2.move_to(right_pan_center + 0.3*UP)
        self.objects["circle2"] = circle2
        
        circle3 = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle3.move_to(right_pan_center + 0.6*RIGHT + 0.3*UP)
        self.objects["circle3"] = circle3
        
        circle4 = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle4.move_to(right_pan_center + 0.6*LEFT + 0.3*DOWN)
        self.objects["circle4"] = circle4
        
        circle5 = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle5.move_to(right_pan_center + 0.3*DOWN)
        self.objects["circle5"] = circle5
        
        circle6 = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle6.move_to(right_pan_center + 0.6*RIGHT + 0.3*DOWN)
        self.objects["circle6"] = circle6
        
        right_group_label = MathTex("6", color=YELLOW, font_size=30)
        right_group_label.next_to(right_pan, RIGHT, buff=0.5)
        self.objects["right_group_label"] = right_group_label
        
        # Explanation text
        explanation_text = Text("The scale is balanced: 2x equals 6.", color=LIGHT_GRAY, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text
        
        # Final labels (initially invisible, will be created when needed)
        final_x_label = MathTex("x", color=WHITE, font_size=24)
        final_x_label.move_to(left_pan_center)
        final_x_label.set_opacity(0)
        self.objects["final_x_label"] = final_x_label
        
        final_3_label = MathTex("3", color=YELLOW, font_size=30)
        final_3_label.next_to(right_pan, RIGHT, buff=0.5)
        final_3_label.set_opacity(0)
        self.objects["final_3_label"] = final_3_label
        
        # Create VGroups for easier manipulation
        box_group = VGroup(box1, box2, box_label_initial, box_label_initial2)
        circles_group = VGroup(circle1, circle2, circle3, circle4, circle5, circle6)
        self.objects["box_group"] = box_group
        self.objects["circles_group"] = circles_group
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = self.get_sequence_data()
        
        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_path = step.get("audio_path")
            
            # Add audio if path exists
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)
            
            # Handle signal_action
            signal_action = step.get("signal_action")
            if signal_action is not None:
                signal_type = signal_action["type"]
                target_ids = signal_action["target"]
                color_str = signal_action.get("color", "YELLOW")
                color = eval(color_str)
                
                # Get target objects
                if isinstance(target_ids, list):
                    targets = [self.objects[tid] for tid in target_ids]
                    target_group = VGroup(*targets)
                else:
                    target_group = self.objects[target_ids]
                
                if signal_type == "Circumscribe":
                    self.play(Circumscribe(target_group, color=color, run_time=1))
                elif signal_type == "Indicate":
                    self.play(Indicate(target_group, color=color))
                elif signal_type == "FocusOn":
                    self.play(FocusOn(target_group))
            
            # Handle visual_action
            visual_action = step["visual_action"]
            action_type = visual_action["type"]
            target_ids = visual_action.get("target_id")
            details = visual_action.get("details", "")
            
            if action_type == "Create":
                if isinstance(target_ids, list):
                    objs_to_create = [self.objects[tid] for tid in target_ids]
                    self.play(*[Create(obj) if not isinstance(obj, (Text, MathTex)) else Write(obj) for obj in objs_to_create])
                else:
                    obj = self.objects[target_ids]
                    if isinstance(obj, (Text, MathTex)):
                        self.play(Write(obj))
                    else:
                        self.play(Create(obj))
            
            elif action_type == "Write":
                obj = self.objects[target_ids]
                self.play(Write(obj))
            
            elif action_type == "Animate":
                # Step 6: Animate circles separating into two groups
                if target_ids == "circles_group":
                    # Create two groups
                    group1 = VGroup(circle1, circle2, circle3)
                    group2 = VGroup(circle4, circle5, circle6)
                    
                    # Animate group1 moving up, group2 moving down
                    self.play(
                        group1.animate.shift(UP * 0.8),
                        group2.animate.shift(DOWN * 0.8),
                        run_time=2
                    )
            
            elif action_type == "Transform":
                # Step 7: Transform two boxes into one centered box
                if isinstance(target_ids, list) and "box1" in target_ids and "box2" in target_ids:
                    # Create final box
                    final_box = Square(side_length=0.7, color=BLUE, fill_opacity=0.7)
                    final_box.move_to(left_pan_center)
                    self.objects["final_box"] = final_box
                    
                    # Transform boxes into final box
                    self.play(
                        Transform(box1, final_box),
                        Transform(box2, final_box),
                        run_time=2
                    )
                    # Fade out the duplicate
                    self.remove(box2)
                
                # Step 8: Move first group back, fade out second group
                elif isinstance(target_ids, list) and "circle1" in target_ids:
                    # Move group1 back to pan center
                    target_positions = {
                        "circle1": right_pan_center + 0.6*LEFT,
                        "circle2": right_pan_center,
                        "circle3": right_pan_center + 0.6*RIGHT
                    }
                    
                    moves = []
                    for cid, pos in target_positions.items():
                        circle = self.objects[cid]
                        moves.append(circle.animate.move_to(pos))
                    
                    # Fade out group2
                    fade_outs = [FadeOut(self.objects[cid]) for cid in ["circle4", "circle5", "circle6"]]
                    
                    self.play(*moves, *fade_outs, run_time=2)
            
            elif action_type == "ReplacementTransform":
                # Step 9: Transform left label to 'x' and right label to '3'
                if isinstance(target_ids, list) and "left_group_label" in target_ids:
                    # Create final labels
                    final_left_label = MathTex("x", color=YELLOW, font_size=30)
                    final_left_label.next_to(left_pan, LEFT, buff=0.5)
                    self.objects["final_left_label"] = final_left_label
                    
                    final_right_label = MathTex("3", color=YELLOW, font_size=30)
                    final_right_label.next_to(right_pan, RIGHT, buff=0.5)
                    self.objects["final_right_label"] = final_right_label
                    
                    # Transform labels
                    self.play(
                        ReplacementTransform(left_group_label, final_left_label),
                        ReplacementTransform(right_group_label, final_right_label),
                        run_time=2
                    )
            
            elif action_type == "UpdateText":
                # Step 10: Update explanation text
                if target_ids == "explanation_text":
                    new_content = visual_action.get("new_content", "Solution: x = 3")
                    new_text = Text(new_content, color=LIGHT_GRAY, font_size=24)
                    new_text.move_to(explanation_anchor)
                    
                    self.play(
                        ReplacementTransform(explanation_text, new_text),
                        run_time=2
                    )
                    self.objects["explanation_text"] = new_text
            
            # Calculate remaining wait time
            # Estimate animation runtime (simplified)
            anim_time = 2.0 if action_type in ["Transform", "ReplacementTransform", "Animate", "UpdateText"] else 1.0
            remaining = duration - anim_time + 0.5
            if remaining > 0:
                self.wait(remaining)
    
    def get_sequence_data(self):
        """Return the sequence data from the JSON."""
        return [
            {
                "step": 1,
                "duration": 5.04,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_00.mp3",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "title",
                    "details": "Fade in title"
                }
            },
            {
                "step": 2,
                "duration": 6.288,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_01.mp3",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": ["beam", "fulcrum", "left_pan", "right_pan", "left_string", "right_string"],
                    "details": "Draw the scale structure"
                }
            },
            {
                "step": 3,
                "duration": 5.304,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_02.mp3",
                "signal_action": {
                    "type": "Indicate",
                    "target": ["box1", "box2", "box_label_initial", "box_label_initial2"],
                    "color": "BLUE"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": ["box1", "box2", "box_label_initial", "box_label_initial2", "left_group_label"],
                    "details": "Create left side boxes with labels and group label"
                }
            },
            {
                "step": 4,
                "duration": 4.584,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_03.mp3",
                "signal_action": {
                    "type": "Indicate",
                    "target": ["circle1", "circle2", "circle3", "circle4", "circle5", "circle6"],
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": ["circle1", "circle2", "circle3", "circle4", "circle5", "circle6", "right_group_label"],
                    "details": "Create right side circles and label"
                }
            },
            {
                "step": 5,
                "duration": 8.424,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_04.mp3",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": ["left_group_label", "right_group_label"],
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "explanation_text",
                    "details": "Show explanation text"
                }
            },
            {
                "step": 6,
                "duration": 7.152,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_05.mp3",
                "signal_action": {
                    "type": "Indicate",
                    "target": ["circle1", "circle2", "circle3", "circle4", "circle5", "circle6"],
                    "color": "ORANGE"
                },
                "visual_action": {
                    "type": "Animate",
                    "target_id": "circles_group",
                    "details": "Animate the six circles separating into two distinct groups"
                }
            },
            {
                "step": 7,
                "duration": 4.632,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_06.mp3",
                "signal_action": {
                    "type": "Indicate",
                    "target": ["box2", "circle4", "circle5", "circle6"],
                    "color": "RED"
                },
                "visual_action": {
                    "type": "Transform",
                    "target_id": ["box1", "box2"],
                    "details": "Transform two boxes into one centered box"
                }
            },
            {
                "step": 8,
                "duration": 4.104,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_07.mp3",
                "signal_action": None,
                "visual_action": {
                    "type": "Transform",
                    "target_id": ["circle1", "circle2", "circle3"],
                    "details": "Move first group back, fade out second group"
                }
            },
            {
                "step": 9,
                "duration": 5.352,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_08.mp3",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": ["final_box", "circle1", "circle2", "circle3"],
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "ReplacementTransform",
                    "target_id": ["left_group_label", "right_group_label"],
                    "details": "Transform left label to 'x' and right label to '3'"
                }
            },
            {
                "step": 10,
                "duration": 6.648,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_09.mp3",
                "signal_action": {
                    "type": "Indicate",
                    "target": ["final_box", "final_left_label", "circle1", "circle2", "circle3", "final_right_label"],
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "UpdateText",
                    "target_id": "explanation_text",
                    "details": "Update explanation to 'Solution: x = 3'",
                    "new_content": "Solution: x = 3"
                }
            }
        ]