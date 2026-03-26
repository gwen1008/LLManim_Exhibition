from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}
        
        # Title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Integer", color=WHITE, font_size=36)
        self.objects["title"] = title
        
        # Number line and ticks
        number_line = Line(start=[-3.5, 0, 0], end=[3.5, 0, 0], color=WHITE, stroke_width=4)
        self.objects["number_line"] = number_line
        
        tick_3 = Line(start=[-3.5, -0.2, 0], end=[-3.5, 0.2, 0], color=WHITE, stroke_width=3)
        self.objects["tick_3"] = tick_3
        
        tick_4 = Line(start=[3.5, -0.2, 0], end=[3.5, 0.2, 0], color=WHITE, stroke_width=3)
        self.objects["tick_4"] = tick_4
        
        label_3 = MathTex("3", color=WHITE)
        self.objects["label_3"] = label_3
        
        label_4 = MathTex("4", color=WHITE)
        self.objects["label_4"] = label_4
        
        # Midpoint
        tick_mid = Line(start=[0, -0.15, 0], end=[0, 0.15, 0], color=YELLOW, stroke_width=3)
        self.objects["tick_mid"] = tick_mid
        
        label_mid = MathTex("3.5", color=YELLOW)
        self.objects["label_mid"] = label_mid
        
        # Pointer at 3.7
        pointer_37 = Triangle(color=GREEN, fill_opacity=1.0, stroke_width=0).scale(0.2)
        pointer_37.rotate(-PI/2)
        pointer_37.move_to([1.4, 0, 0])
        self.objects["pointer_37"] = pointer_37
        
        label_37 = MathTex("3.7", color=GREEN)
        self.objects["label_37"] = label_37
        
        # Distance bars
        dist_bar_left = Line(start=[1.4, 0.2, 0], end=[-3.5, 0.2, 0], color="#FF6666", stroke_width=6)
        self.objects["dist_bar_left"] = dist_bar_left
        
        dist_bar_right = Line(start=[1.4, 0.2, 0], end=[3.5, 0.2, 0], color="#66FF66", stroke_width=6)
        self.objects["dist_bar_right"] = dist_bar_right
        
        # Final pointer at 4
        pointer_4 = Triangle(color=BLUE, fill_opacity=0.0, stroke_width=0).scale(0.2)
        pointer_4.rotate(-PI/2)
        pointer_4.move_to([3.5, 0, 0])
        self.objects["pointer_4"] = pointer_4
        
        # Explanation text
        explanation_text_step1 = Text("We have a number line from 3 to 4.", color=WHITE, font_size=24)
        self.objects["explanation_text_step1"] = explanation_text_step1
        
        # ========== POSITIONING ==========
        # Position title
        title.to_edge(UP)
        
        # Position main content
        main_content = VGroup(
            number_line, tick_3, tick_4, label_3, label_4,
            tick_mid, label_mid, pointer_37, label_37,
            dist_bar_left, dist_bar_right, pointer_4
        )
        main_content.move_to(ORIGIN)
        
        # Position labels relative to ticks
        label_3.next_to(tick_3, DOWN, buff=0.3)
        label_4.next_to(tick_4, DOWN, buff=0.3)
        label_mid.next_to(tick_mid, DOWN, buff=0.3)
        label_37.next_to(pointer_37, UP, buff=0.3)
        
        # Position explanation
        explanation_text_step1.to_edge(DOWN)
        
        # Set z_index for pointers
        pointer_37.set_z_index(1)
        pointer_4.set_z_index(1)
        
        # Initially hide distance bars and pointer_4
        dist_bar_left.set_opacity(0)
        dist_bar_right.set_opacity(0)
        pointer_4.set_opacity(0)
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's consider a number line from 3 to 4.",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "title",
                    "details": "Fade in title"
                },
                "duration": 3.36,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "We draw the line and mark the integers 3 and 4.",
                "signal_action": None,
                "visual_action": {
                    "type": "AnimationGroup",
                    "target_ids": [
                        "number_line",
                        "tick_3",
                        "tick_4",
                        "label_3",
                        "label_4"
                    ],
                    "details": "Create number line, endpoints, and labels together"
                },
                "duration": 3.624,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "The midpoint between them is 3.5. And we have our point of interest, 3.7.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "label_mid",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "AnimationGroup",
                    "target_ids": [
                        "tick_mid",
                        "label_mid",
                        "pointer_37",
                        "label_37"
                    ],
                    "details": "Draw midpoint and the point 3.7 with its pointer"
                },
                "duration": 6.456,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "To see which integer 3.7 is closer to, we look at the distances. The distance to 3 is longer than the distance to 4.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "dist_bar_left",
                    "color": "#FF6666"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "dist_bar_left",
                    "details": "Draw red bar from pointer to 3"
                },
                "duration": 8.568,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Since 3.7 is to the right of the midpoint 3.5, it is closer to 4.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "dist_bar_right",
                    "color": "#66FF66"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "dist_bar_right",
                    "details": "Draw green bar from pointer to 4"
                },
                "duration": 5.472,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "Therefore, when rounding to the nearest integer, 3.7 rounds up to 4.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "label_4",
                    "color": "BLUE"
                },
                "visual_action": {
                    "type": "Transform",
                    "target_id": "pointer_37",
                    "details": "Transform the green pointer into the blue pointer at position 4. Simultaneously, transform the green distance bar into a very short line (or dot) at the pointer's new location to visualize the distance becoming zero.",
                    "target_end_state": "pointer_4"
                },
                "duration": 5.328,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_05.mp3"
            }
        ]
        
        for step in sequence:
            # === AUDIO ===
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # === VISUAL ACTION ===
            visual_action = step["visual_action"]
            action_type = visual_action["type"]
            
            if action_type == "Create":
                target_id = visual_action["target_id"]
                obj = self.objects[target_id]
                # Check if object is already visible by checking if it's in the scene
                if obj not in self.mobjects:
                    self.play(Create(obj))
                else:
                    # If already in scene but hidden, fade in
                    if obj.opacity == 0:
                        self.play(FadeIn(obj))
            
            elif action_type == "AnimationGroup":
                target_ids = visual_action["target_ids"]
                anims = []
                for tid in target_ids:
                    obj = self.objects[tid]
                    if obj not in self.mobjects:
                        anims.append(Create(obj))
                    else:
                        if obj.opacity == 0:
                            anims.append(FadeIn(obj))
                if anims:
                    self.play(*anims)
            
            elif action_type == "Transform":
                source_obj = self.objects[visual_action["target_id"]]
                target_obj = self.objects[visual_action["target_end_state"]]
                
                # Make pointer_4 visible and set its fill_opacity to 1
                pointer_4.set_fill(opacity=1.0)
                pointer_4.set_stroke(width=0)
                
                # Create a dot at the final position for the green bar transformation
                dot = Dot(color="#66FF66", radius=0.05).move_to([3.5, 0.2, 0])
                
                # Animate transformation of pointer and distance bar
                self.play(
                    Transform(source_obj, target_obj),
                    Transform(self.objects["dist_bar_right"], dot)
                )
            
            # === SIGNAL ACTION ===
            signal_action = step.get("signal_action")
            if signal_action is not None:
                target_obj = self.objects[signal_action["target"]]
                color_str = signal_action.get("color", "YELLOW")
                color_map = {
                    "YELLOW": YELLOW,
                    "RED": RED,
                    "GREEN": GREEN,
                    "BLUE": BLUE,
                    "#FF6666": "#FF6666",
                    "#66FF66": "#66FF66"
                }
                color = color_map.get(color_str, YELLOW)
                
                if signal_action["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal_action["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
            
            # === WAIT FOR REMAINING AUDIO DURATION ===
            # Use fixed animation times
            if action_type == "Create":
                anim_time = 1.0
            elif action_type == "AnimationGroup":
                anim_time = 2.0
            elif action_type == "Transform":
                anim_time = 2.0
            else:
                anim_time = 1.0
            
            # Add signal_action run_time if present
            if signal_action is not None:
                anim_time += 1.0
            
            remaining = step["duration"] - anim_time
            if remaining > 0:
                self.wait(max(0.1, remaining))
            else:
                self.wait(0.1)
        
        # Final wait
        self.wait(2)