from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create objects from layout_plan
        # Title
        title = Text("Corresponding Angles with Parallel Lines", color=WHITE, font_size=40)
        self.objects["title"] = title
        
        # Lines
        line_l1 = Line(start=[-4, 1.5, 0], end=[4, 1.5, 0], color=BLUE, stroke_width=4)
        self.objects["line_l1"] = line_l1
        
        line_l2 = Line(start=[-4, -1.5, 0], end=[4, -1.5, 0], color=BLUE, stroke_width=4)
        self.objects["line_l2"] = line_l2
        
        transversal = Line(start=[-4, -2.309, 0], end=[4, 2.309, 0], color=RED, stroke_width=4)
        self.objects["transversal"] = transversal
        
        # Labels for lines
        label_l1 = MathTex("l_1", color=BLUE, font_size=30)
        self.objects["label_l1"] = label_l1
        
        label_l2 = MathTex("l_2", color=BLUE, font_size=30)
        self.objects["label_l2"] = label_l2
        
        label_t = MathTex("t", color=RED, font_size=30)
        self.objects["label_t"] = label_t
        
        # Calculate intersection points using get_center() approach
        # For angle1: intersection of transversal and l1 (upper right)
        # We'll position the angle at the intersection point
        intersection1 = np.array([2.598, 1.5, 0])  # Pre-calculated intersection
        
        # Create angle1 using the intersection point
        angle1 = Angle(
            line1=transversal.copy().shift(-intersection1),
            line2=line_l1.copy().shift(-intersection1),
            radius=0.4,
            color=GREEN,
            stroke_width=6
        ).shift(intersection1)
        self.objects["angle1"] = angle1
        
        # For angle2: intersection of l2 and transversal (lower left)
        intersection2 = np.array([-2.598, -1.5, 0])  # Pre-calculated intersection
        
        # Create angle2 using the intersection point
        angle2 = Angle(
            line1=line_l2.copy().shift(-intersection2),
            line2=transversal.copy().shift(-intersection2),
            radius=0.4,
            color=GREEN,
            stroke_width=6
        ).shift(intersection2)
        self.objects["angle2"] = angle2
        
        # Angle labels
        angle1_label = MathTex(r"\angle 1", color=GREEN, font_size=24).scale(0.7)
        self.objects["angle1_label"] = angle1_label
        
        angle2_label = MathTex(r"\angle 2", color=GREEN, font_size=24).scale(0.7)
        self.objects["angle2_label"] = angle2_label
        
        # Explanation text
        explanation_text = Text(
            "Corresponding Angles Postulate: If lines are parallel, corresponding angles are congruent.",
            color=YELLOW,
            font_size=28
        )
        self.objects["explanation_text"] = explanation_text
        
        # Position objects manually according to layout plan
        title.to_edge(UP)
        explanation_text.to_edge(DOWN)
        
        # Position labels relative to lines
        label_l1.next_to(line_l1.get_end(), RIGHT, buff=0.2)
        label_l2.next_to(line_l2.get_end(), RIGHT, buff=0.2)
        label_t.next_to(transversal.get_end(), UP+RIGHT, buff=0.2)
        
        # Position angle labels relative to their angles
        angle1_label.next_to(angle1, UR, buff=0.1)
        angle2_label.next_to(angle2, DL, buff=0.1)
        
        # Center the diagram
        diagram_group = VGroup(line_l1, line_l2, transversal, label_l1, label_l2, label_t, angle1, angle2, angle1_label, angle2_label)
        diagram_group.move_to(ORIGIN)
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's start with two parallel lines, l1 and l2, and a transversal line t cutting across them.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "line_l1", "details": "Draw the upper parallel line."},
                "duration": 6.816,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "line_l2", "details": "Draw the lower parallel line."},
                "duration": 2.0
            },
            {
                "step": 3,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "transversal", "details": "Draw the slanted transversal line."},
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
                "narrative": "Now, we identify a pair of corresponding interior angles on the same side of the transversal. Let's highlight them in green.",
                "signal_action": {"type": "Indicate", "target": "angle1", "color": "GREEN"},
                "visual_action": {"type": "Create", "target_id": "angle1", "details": "Draw the green arc at the upper intersection."},
                "duration": 8.592,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "",
                "signal_action": {"type": "Indicate", "target": "angle2", "color": "GREEN"},
                "visual_action": {"type": "Create", "target_id": "angle2", "details": "Draw the green arc at the lower intersection."},
                "duration": 2.0
            },
            {
                "step": 9,
                "narrative": "We label these angles as angle 1 and angle 2.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "angle1_label", "details": "Write label for angle 1."},
                "duration": 3.672,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_08.mp3"
            },
            {
                "step": 10,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "angle2_label", "details": "Write label for angle 2."},
                "duration": 2.0
            },
            {
                "step": 11,
                "narrative": "The Corresponding Angles Postulate tells us: if lines are parallel, then corresponding angles are congruent.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "explanation_text", "details": "Display the postulate at the bottom."},
                "duration": 7.32,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_10.mp3"
            },
            {
                "step": 12,
                "narrative": "Let's visualize this congruence. Watch as angle 1 transforms and maps perfectly onto angle 2.",
                "signal_action": {"type": "Circumscribe", "target": "angle1", "color": "YELLOW"},
                "visual_action": {"type": "Transform", "details": "Use Transform(angle1, angle2) to morph the first green arc into the second."},
                "duration": 7.488,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_11.mp3"
            },
            {
                "step": 13,
                "narrative": "The perfect match demonstrates that angle 1 is congruent to angle 2.",
                "signal_action": {"type": "Indicate", "target": "angle2", "color": "GREEN"},
                "visual_action": {"type": "Wait", "details": "Hold the final transformed angle on screen."},
                "duration": 4.776,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_12.mp3"
            }
        ]
        
        # First, add title (it will be written in step 1 implicitly via audio sync)
        self.play(Write(title))
        
        for step in sequence:
            step_num = step["step"]
            
            # === AUDIO (MANDATORY) ===
            audio_file = None
            if "audio_path" in step and step["audio_path"]:
                audio_file = step["audio_path"]
            else:
                # Fallback construction
                file_index = step_num - 1
                mp3_path = f"media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_{file_index:02d}.mp3"
                wav_path = f"media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_{file_index:02d}.wav"
                if os.path.exists(mp3_path):
                    audio_file = mp3_path
                elif os.path.exists(wav_path):
                    audio_file = wav_path
            
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # Signal Action
            signal_action = step.get("signal_action")
            if signal_action is not None:
                target_obj = self.objects[signal_action["target"]]
                color_str = signal_action.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
                color = color_map.get(color_str, YELLOW)
                
                if signal_action["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal_action["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
            
            # Visual Action
            visual_action = step["visual_action"]
            action_type = visual_action["type"]
            
            if action_type == "Create":
                target_id = visual_action["target_id"]
                obj = self.objects[target_id]
                self.play(Create(obj))
                animation_time = 1.0
            elif action_type == "Write":
                target_id = visual_action["target_id"]
                obj = self.objects[target_id]
                self.play(Write(obj))
                animation_time = 1.0
            elif action_type == "Transform":
                # For angle transformation, create a copy of angle1 to transform into angle2
                # This preserves the original angle1 in the diagram
                angle1_obj = self.objects["angle1"]
                angle2_obj = self.objects["angle2"]
                angle1_copy = angle1_obj.copy()
                self.play(Transform(angle1_copy, angle2_obj))
                # Keep the copy for the rest of the scene
                self.objects["angle1_transformed"] = angle1_copy
                animation_time = 2.0
            elif action_type == "Wait":
                # No animation, just waiting
                animation_time = 0.0
            
            # Calculate remaining wait time
            total_duration = step["duration"]
            remaining = total_duration - animation_time + 0.5  # 0.5s safety buffer
            if remaining > 0:
                self.wait(remaining)
        
        # Final hold
        self.wait(2)