from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Object Creation ==========
        # Create a registry for all objects
        self.objects = {}
        
        # --- Create objects from layout_plan.objects ---
        # title
        title = Text("Corresponding Interior Angles", color=WHITE, font_size=40)
        title.move_to(UP * 3.2)
        self.objects["title"] = title
        
        # line_l1
        line_l1 = Line(start=[-4, 1, 0], end=[4, 1, 0], color=BLUE, stroke_width=4)
        line_l1.move_to(ORIGIN + UP)
        self.objects["line_l1"] = line_l1
        
        # line_l2
        line_l2 = Line(start=[-4, -1, 0], end=[4, -1, 0], color=BLUE, stroke_width=4)
        line_l2.move_to(ORIGIN + DOWN)
        self.objects["line_l2"] = line_l2
        
        # transversal
        transversal = Line(start=[-3, -1, 0], end=[3, 1, 0], color=RED, stroke_width=4)
        transversal.move_to(ORIGIN)
        self.objects["transversal"] = transversal
        
        # label_l1
        label_l1 = MathTex("l_1", color=BLUE)
        label_l1.next_to(line_l1.get_end(), RIGHT, buff=0.2)
        self.objects["label_l1"] = label_l1
        
        # label_l2
        label_l2 = MathTex("l_2", color=BLUE)
        label_l2.next_to(line_l2.get_end(), RIGHT, buff=0.2)
        self.objects["label_l2"] = label_l2
        
        # label_t
        label_t = MathTex("t", color=RED)
        label_t.next_to(transversal.get_end(), UP+RIGHT, buff=0.2)
        self.objects["label_t"] = label_t
        
        # angle1_arc
        angle1_arc = Arc(radius=0.4, angle=PI/4, start_angle=PI/4, color=GREEN, stroke_width=6)
        angle1_arc.move_to([1, 1, 0])
        self.objects["angle1_arc"] = angle1_arc
        
        # angle2_arc
        angle2_arc = Arc(radius=0.4, angle=PI/4, start_angle=5*PI/4, color=GREEN, stroke_width=6)
        angle2_arc.move_to([-1, -1, 0])
        self.objects["angle2_arc"] = angle2_arc
        
        # angle1_group - will be constructed in step 11
        angle1_group = VGroup()
        self.objects["angle1_group"] = angle1_group
        
        # step_label
        step_label = Text("Step 1: Draw two parallel lines and a transversal.", color=YELLOW, font_size=28)
        step_label.move_to(DOWN * 2.8)
        self.objects["step_label"] = step_label
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's start with two parallel lines, L1 and L2, and a transversal line t cutting across them.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "line_l1", "details": "Draw the first parallel line."},
                "duration": 6.816,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "line_l2", "details": "Draw the second parallel line below."},
                "duration": 2.0
            },
            {
                "step": 3,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "transversal", "details": "Draw the transversal line slanted across both parallels."},
                "duration": 2.0
            },
            {
                "step": 4,
                "narrative": "We label the lines for clarity.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_l1", "details": "Write label l1."},
                "duration": 2.616,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_l2", "details": "Write label l2."},
                "duration": 2.0
            },
            {
                "step": 6,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_t", "details": "Write label t."},
                "duration": 2.0
            },
            {
                "step": 7,
                "narrative": "Now, we identify a pair of corresponding interior angles on the same side of the transversal. These are the angles inside the parallel lines and on the right side.",
                "signal_action": {"type": "Indicate", "target": "transversal", "color": "YELLOW"},
                "visual_action": {"type": "ReplacementTransform", "target_id": "step_label", "details": "Update step label to: 'Step 2: Identify corresponding interior angles (green).'"},
                "duration": 10.728,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "We mark them in green.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "angle1_arc", "details": "Draw the green arc at the upper intersection (right side)."},
                "duration": 2.16,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_07.mp3"
            },
            {
                "step": 9,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "angle2_arc", "details": "Draw the matching green arc at the lower intersection (right side)."},
                "duration": 2.0
            },
            {
                "step": 10,
                "narrative": "The property of corresponding angles tells us these two angles are congruent. Let's prove it visually.",
                "signal_action": {"type": "Circumscribe", "target": "angle1_arc", "color": "YELLOW"},
                "visual_action": {"type": "ReplacementTransform", "target_id": "step_label", "details": "Update step label to: 'Step 3: Demonstrate congruence via rigid motion.'"},
                "duration": 6.984,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_09.mp3"
            },
            {
                "step": 11,
                "narrative": "We can take the upper angle, and through a combination of rotation and translation...",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "angle1_group", "details": "Construct the VGroup for angle1 (two rays and the arc) at its current location. This is the object we will transform."},
                "duration": 5.184,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_10.mp3"
            },
            {
                "step": 12,
                "narrative": "...move it to perfectly overlap the lower angle.",
                "signal_action": {"type": "Indicate", "target": "angle2_arc", "color": "YELLOW"},
                "visual_action": {"type": "Transform", "target_id": "angle1_group", "details": "Animate the angle1_group rotating and translating so its components align exactly with the lower angle (angle2_arc and its surrounding lines). This is a Transform, not a ReplacementTransform, as we want the object to move."},
                "duration": 3.696,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_11.mp3"
            },
            {
                "step": 13,
                "narrative": "The perfect fit shows they are congruent. This visual proof relies on the fact that the lines are parallel.",
                "signal_action": {"type": "Circumscribe", "target": "line_l1", "color": "BLUE"},
                "visual_action": {"type": "ReplacementTransform", "target_id": "step_label", "details": "Update step label to: 'Conclusion: Corresponding interior angles are congruent (∠1 ≅ ∠2).'"},
                "duration": 7.176,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_12.mp3"
            }
        ]
        
        # Add title and step_label to scene (they will be animated later)
        self.add(title, step_label)
        
        # Process each step
        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            
            # === AUDIO (MANDATORY) ===
            audio_file = None
            if "audio_path" in step and step["audio_path"]:
                audio_file = step["audio_path"]
            
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # 1. Handle signal_action
            signal = step.get("signal_action")
            if signal is not None:
                target_obj = self.objects[signal["target"]]
                color = eval(signal["color"])  # Convert string to Manim color constant
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
            
            # 2. Handle visual_action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            action_type = visual["type"]
            
            if action_type == "Create":
                obj = self.objects[target_id]
                if target_id == "angle1_group":
                    # Construct angle1_group properly for step 11
                    # Create rays for the angle at upper intersection
                    upper_center = np.array([1, 1, 0])
                    # Ray along transversal (from intersection point)
                    ray1 = Line(start=upper_center, 
                               end=upper_center + np.array([2, 2/3, 0]), 
                               color=GREEN, stroke_width=4)
                    # Ray along line_l1 (horizontal right)
                    ray2 = Line(start=upper_center, 
                               end=upper_center + np.array([2, 0, 0]), 
                               color=GREEN, stroke_width=4)
                    # Create the arc
                    arc = Arc(radius=0.4, angle=PI/4, start_angle=PI/4, 
                             color=GREEN, stroke_width=6)
                    arc.move_to(upper_center)
                    
                    # Create the VGroup
                    angle1_group = VGroup(ray1, ray2, arc)
                    self.objects["angle1_group"] = angle1_group
                    self.play(Create(angle1_group))
                else:
                    self.play(Create(obj))
            
            elif action_type == "Write":
                obj = self.objects[target_id]
                self.play(Write(obj))
            
            elif action_type == "ReplacementTransform":
                # For step_label updates
                old_label = self.objects[target_id]
                # Create new label with updated text
                if step_num == 7:
                    new_content = "Step 2: Identify corresponding interior angles (green)."
                elif step_num == 10:
                    new_content = "Step 3: Demonstrate congruence via rigid motion."
                elif step_num == 13:
                    new_content = "Conclusion: Corresponding interior angles are congruent (∠1 ≅ ∠2)."
                else:
                    new_content = old_label.text  # fallback
                
                new_label = Text(new_content, color=YELLOW, font_size=28)
                new_label.move_to(old_label.get_center())  # Keep same position
                self.play(ReplacementTransform(old_label, new_label))
                self.objects[target_id] = new_label
            
            elif action_type == "Transform":
                # Step 12: Transform angle1_group to overlap angle2_arc
                angle1_group_obj = self.objects[target_id]
                
                # Create target group at lower intersection
                lower_center = np.array([-1, -1, 0])
                # Create rays for lower angle
                ray1_target = Line(start=lower_center, 
                                  end=lower_center + np.array([-2, -2/3, 0]), 
                                  color=GREEN, stroke_width=4)
                ray2_target = Line(start=lower_center, 
                                  end=lower_center + np.array([-2, 0, 0]), 
                                  color=GREEN, stroke_width=4)
                # Create the arc
                arc_target = Arc(radius=0.4, angle=PI/4, start_angle=5*PI/4, 
                                color=GREEN, stroke_width=6)
                arc_target.move_to(lower_center)
                
                target_group = VGroup(ray1_target, ray2_target, arc_target)
                
                self.play(Transform(angle1_group_obj, target_group))
            
            # 3. Wait for remaining duration
            # Estimate animation time for this step
            anim_time = 0
            if signal is not None:
                anim_time += 1  # signal run_time
            if action_type in ["Create", "Write"]:
                anim_time += 1
            elif action_type == "ReplacementTransform":
                anim_time += 1
            elif action_type == "Transform":
                anim_time += 2  # longer transformation
            
            remaining = duration - anim_time + 0.5  # safety buffer
            if remaining > 0:
                self.wait(remaining)
        
        # Final wait
        self.wait(2)