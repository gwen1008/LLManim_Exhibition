from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}
        
        # Initialize Layout Engine
        layout = LayoutEngine()
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Integer", color=WHITE, font_size=36)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title
        
        # Number Line (Main content)
        number_line = NumberLine(
            x_range=[3, 4, 0.1],
            length=8,
            include_numbers=True,
            numbers_to_include=[3, 4],
            color=LIGHT_GRAY
        )
        obj_number_line = LayoutObject(number_line, "number_line")
        layout.add(obj_number_line)
        layout.add_to_zone(obj_number_line, "CONTENT")
        layout.add_constraint(obj_number_line.center_x == 0)
        layout.add_constraint(obj_number_line.center_y == 0)
        self.objects["number_line"] = number_line
        
        # Tick at 3.5 (small vertical line on number line)
        tick_3_5 = Line(start=UP*0.15, end=DOWN*0.15, color=LIGHT_GRAY, stroke_width=2)
        # Position will be set after number_line is solved
        self.objects["tick_3.5"] = tick_3_5
        
        # Labels for integers 3 and 4
        label_3 = MathTex("3", color=BLUE)
        self.objects["label_3"] = label_3
        
        label_4 = MathTex("4", color=BLUE)
        self.objects["label_4"] = label_4
        
        # Label for midpoint 3.5
        label_3_5 = MathTex("3.5", color=YELLOW)
        self.objects["label_3.5"] = label_3_5
        
        # Vertical dashed line at midpoint
        midpoint_vertical_line = DashedLine(
            start=UP*1.5,
            end=DOWN*1.0,
            color=YELLOW,
            dash_length=0.1,
            stroke_width=3
        )
        # Position will be set after number_line is solved
        self.objects["midpoint_vertical_line"] = midpoint_vertical_line
        
        # Dot and label for 3.7
        dot_3_7 = Dot(radius=0.08, color=GREEN)
        self.objects["dot_3.7"] = dot_3_7
        
        label_3_7 = MathTex("3.7", color=GREEN)
        self.objects["label_3.7"] = label_3_7
        
        # Arrow from 3.7 to midpoint line
        arrow_to_midpoint = Arrow(
            start=ORIGIN,
            end=RIGHT,
            color=WHITE,
            stroke_width=2,
            buff=0
        )
        # Start and end will be set dynamically
        self.objects["arrow_to_midpoint"] = arrow_to_midpoint
        
        # Footer text
        footer_text = Text(
            "Since 3.7 > 3.5, it is closer to 4. Therefore, 3.7 rounds up to 4.",
            color=LIGHT_GRAY,
            font_size=28
        )
        obj_footer = LayoutObject(footer_text, "footer_text")
        layout.add(obj_footer)
        layout.add_to_zone(obj_footer, "FOOTER")
        layout.add_constraint(obj_footer.center_x == 0)
        self.objects["footer_text"] = footer_text
        
        # Final label "4" that will replace "3.7"
        label_4_final = MathTex("4", color=GREEN, opacity=0)
        self.objects["label_4_final"] = label_4_final
        
        # Solve layout to get positions for title, number_line, and footer
        layout.solve()
        
        # Now position dependent objects relative to number_line
        # Get number_line center after layout solve
        nl_center = obj_number_line.get_center()
        nl_left = obj_number_line.get_left()
        nl_right = obj_number_line.get_right()
        
        # Position tick at 3.5 on number line
        tick_3_5.move_to(number_line.n2p(3.5))
        
        # Position labels for integers 3 and 4
        label_3.next_to(number_line.n2p(3), DOWN, buff=0.2)
        label_4.next_to(number_line.n2p(4), DOWN, buff=0.2)
        
        # Position label for 3.5
        label_3_5.next_to(tick_3_5, DOWN, buff=0.3)
        
        # Position vertical dashed line at 3.5
        midpoint_vertical_line.move_to(number_line.n2p(3.5))
        
        # Position dot and label for 3.7
        dot_3_7.move_to(number_line.n2p(3.7))
        label_3_7.next_to(dot_3_7, UP, buff=0.2)
        
        # Position arrow (will be updated when created)
        arrow_start = dot_3_7.get_center()
        arrow_end = midpoint_vertical_line.get_top()
        arrow_to_midpoint.put_start_and_end_on(arrow_start, arrow_end)
        
        # Position final label 4 at same spot as label_3_7 initially
        label_4_final.move_to(label_3_7.get_center())
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = self.get_sequence_data()
        
        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_path = step.get("audio_path", "")
            
            # === AUDIO (MANDATORY) ===
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)
            
            # Track animation time for this step
            animation_time = 0
            
            # Handle signal_action if present
            signal_action = step.get("signal_action")
            if signal_action is not None:
                signal_type = signal_action["type"]
                target_id = signal_action["target"]
                color_name = signal_action.get("color", "YELLOW")
                color = eval(color_name)
                
                target_obj = self.objects[target_id]
                
                if signal_type == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                    animation_time += 1
                elif signal_type == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                    animation_time += 1
                elif signal_type == "FocusOn":
                    self.play(FocusOn(target_obj))
                    animation_time += 1
            
            # Handle visual_action
            visual_action = step["visual_action"]
            action_type = visual_action["type"]
            target_id = visual_action["target_id"]
            
            if step_num == 1:
                # Create number line with labels
                self.play(Create(number_line), run_time=2)
                self.play(Write(label_3), Write(label_4), run_time=1)
                animation_time += 3
                
            elif step_num == 2:
                # Create midpoint elements
                self.play(Create(tick_3_5), run_time=0.5)
                self.play(Create(midpoint_vertical_line), run_time=1.5)
                self.play(Write(label_3_5), run_time=1)
                animation_time += 3
            
            elif step_num == 3:
                # Create dot and label for 3.7
                self.play(Create(dot_3_7), run_time=1)
                self.play(Write(label_3_7), run_time=1)
                animation_time += 2
            
            elif step_num == 4:
                # Create arrow and show footer text
                self.play(Create(arrow_to_midpoint), run_time=1.5)
                self.play(Write(footer_text), run_time=1.5)
                animation_time += 3
            
            elif step_num == 5:
                # Transform label 3.7 to 4, move to integer 4, clean up
                # First morph the label
                self.play(
                    TransformMatchingTex(label_3_7, label_4_final),
                    run_time=2
                )
                # Make the final label visible
                self.play(
                    label_4_final.animate.set_opacity(1),
                    run_time=0.5
                )
                # Move it to align with integer 4 label
                final_position = label_4.get_center() + UP * 0.5
                self.play(
                    label_4_final.animate.move_to(final_position),
                    run_time=1.5
                )
                # Fade out arrow and dot
                self.play(
                    FadeOut(arrow_to_midpoint),
                    FadeOut(dot_3_7),
                    run_time=1
                )
                animation_time += 5
            
            # Wait for remaining audio duration
            remaining = duration - animation_time + 0.5
            if remaining > 0:
                self.wait(remaining)
    
    def get_sequence_data(self):
        """Return the sequence data from the JSON blueprint."""
        return [
            {
                "step": 1,
                "duration": 3.36,
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "number_line"
                },
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_00.mp3"
            },
            {
                "step": 2,
                "duration": 6.216,
                "signal_action": {
                    "type": "Indicate",
                    "target": "tick_3.5",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "midpoint_vertical_line"
                },
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_01.mp3"
            },
            {
                "step": 3,
                "duration": 3.768,
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "dot_3.7"
                },
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_02.mp3"
            },
            {
                "step": 4,
                "duration": 6.624,
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "dot_3.7",
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "arrow_to_midpoint"
                },
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_03.mp3"
            },
            {
                "step": 5,
                "duration": 10.2,
                "signal_action": {
                    "type": "Indicate",
                    "target": "label_4",
                    "color": "BLUE"
                },
                "visual_action": {
                    "type": "Transform",
                    "target_id": "label_3.7"
                },
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_04.mp3"
            }
        ]