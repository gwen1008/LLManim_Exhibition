from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}
        
        # Define anchors based on layout_plan
        title_anchor = UP * 3.5
        main_stage = ORIGIN
        comparison_left = LEFT * 3
        comparison_right = RIGHT * 3
        explanation_anchor = DOWN * 3.5
        
        # Title
        title = Text("Equivalent Fractions: 1/2 = 2/4", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Main Pizza Circle
        pizza_main = Circle(radius=2, color="#FFD700", fill_opacity=0.3, stroke_width=3)
        pizza_main.move_to(main_stage)
        self.objects["pizza_main"] = pizza_main
        
        # Division Lines (initially not added to scene)
        div_line_vertical = Line(start=UP*2, end=DOWN*2, color=BLACK, stroke_width=2)
        div_line_vertical.move_to(main_stage)
        self.objects["div_line_vertical"] = div_line_vertical
        
        div_line_horizontal = Line(start=LEFT*2, end=RIGHT*2, color=BLACK, stroke_width=2)
        div_line_horizontal.move_to(main_stage)
        self.objects["div_line_horizontal"] = div_line_horizontal
        
        # Sectors (initially not added to scene)
        # Right half sector (starts at -PI/2, angle PI)
        sector_half = AnnularSector(inner_radius=0, outer_radius=2, angle=PI, start_angle=-PI/2, color="#1E90FF", fill_opacity=0.7, stroke_width=0)
        sector_half.move_to(main_stage + RIGHT*0.001)  # Slight offset to avoid z-fighting
        self.objects["sector_half"] = sector_half
        
        # Two quarter sectors (for later transformation)
        sector_q1 = AnnularSector(inner_radius=0, outer_radius=2, angle=PI/2, start_angle=-PI/2, color="#1E90FF", fill_opacity=0.7, stroke_width=0)
        sector_q1.move_to(main_stage)
        self.objects["sector_q1"] = sector_q1
        
        sector_q2 = AnnularSector(inner_radius=0, outer_radius=2, angle=PI/2, start_angle=0, color="#1E90FF", fill_opacity=0.7, stroke_width=0)
        sector_q2.move_to(main_stage)
        self.objects["sector_q2"] = sector_q2
        
        # Fraction Labels for main stage
        label_half = MathTex(r"\frac{1}{2}", color=WHITE, font_size=36)
        label_half.next_to(pizza_main, RIGHT, buff=0.5)
        self.objects["label_half"] = label_half
        
        label_quarters = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        label_quarters.next_to(pizza_main, LEFT, buff=0.5)
        self.objects["label_quarters"] = label_quarters
        
        # Comparison Pizzas (smaller)
        pizza_left = Circle(radius=1.5, color="#FFD700", fill_opacity=0.3, stroke_width=3)
        pizza_left.move_to(comparison_left)
        self.objects["pizza_left"] = pizza_left
        
        pizza_right = Circle(radius=1.5, color="#FFD700", fill_opacity=0.3, stroke_width=3)
        pizza_right.move_to(comparison_right)
        self.objects["pizza_right"] = pizza_right
        
        # Comparison Sectors
        sector_left = AnnularSector(inner_radius=0, outer_radius=1.5, angle=PI, start_angle=-PI/2, color="#1E90FF", fill_opacity=0.7, stroke_width=0)
        sector_left.move_to(comparison_left + RIGHT*0.001)
        self.objects["sector_left"] = sector_left
        
        sector_right_q1 = AnnularSector(inner_radius=0, outer_radius=1.5, angle=PI/2, start_angle=-PI/2, color="#1E90FF", fill_opacity=0.7, stroke_width=0)
        sector_right_q1.move_to(comparison_right)
        self.objects["sector_right_q1"] = sector_right_q1
        
        sector_right_q2 = AnnularSector(inner_radius=0, outer_radius=1.5, angle=PI/2, start_angle=0, color="#1E90FF", fill_opacity=0.7, stroke_width=0)
        sector_right_q2.move_to(comparison_right)
        self.objects["sector_right_q2"] = sector_right_q2
        
        # Comparison Labels and Equals Sign
        label_left = MathTex(r"\frac{1}{2}", color=WHITE, font_size=32)
        label_left.next_to(pizza_left, UP, buff=0.3)
        self.objects["label_left"] = label_left
        
        label_right = MathTex(r"\frac{2}{4}", color=WHITE, font_size=32)
        label_right.next_to(pizza_right, UP, buff=0.3)
        self.objects["label_right"] = label_right
        
        equals_sign = MathTex(r"=", color=WHITE, font_size=48)
        equals_sign.move_to(ORIGIN)
        self.objects["equals_sign"] = equals_sign
        
        # Explanation Text
        explanation_text = Text("Start with a whole pizza", color=LIGHT_GRAY, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text
        
        # Group sectors for transformation (implementation_hints)
        sectors_half_group = VGroup(sector_half)
        sectors_quarters_group = VGroup(sector_q1, sector_q2)
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = self.sequence = [
            {
                "step": 1,
                "narrative": "Let's start with a whole pizza. We'll divide it into two equal halves.",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "pizza_main",
                    "details": "Draw the pizza circle"
                },
                "duration": 5.424,
                "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Now cut it vertically down the middle, creating two equal halves.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "div_line_vertical",
                    "color": "RED"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "div_line_vertical",
                    "details": "Draw vertical diameter line"
                },
                "duration": 4.464,
                "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Shade the right half blue. This represents one half, or 1/2 of the pizza.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "sector_half",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "sector_half",
                    "details": "Fill right half with blue"
                },
                "duration": 6.36,
                "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "Now let's cut each half horizontally, dividing the pizza into four equal quarters.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "div_line_horizontal",
                    "color": "RED"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "div_line_horizontal",
                    "details": "Draw horizontal diameter line"
                },
                "duration": 5.544,
                "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Notice the blue half is now made of two blue quarters. So 1/2 equals 2/4.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "sector_half",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "TransformMatchingShapes",
                    "target_id": "sector_half",
                    "details": "Morph the half into two separate quarters (sector_q1 and sector_q2)"
                },
                "duration": 7.056,
                "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "To compare clearly, let's create two smaller pizzas side by side.",
                "signal_action": None,
                "visual_action": {
                    "type": "ReplacementTransform",
                    "target_id": "pizza_main",
                    "details": "Scale down and split into pizza_left and pizza_right at their comparison positions"
                },
                "duration": 4.848,
                "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "The left pizza shows 1/2 shaded. The right pizza shows 2/4 shaded.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "sector_left",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_ids": [
                        "sector_left",
                        "sector_right_q1",
                        "sector_right_q2"
                    ],
                    "details": "Show shaded sectors on both comparison pizzas"
                },
                "duration": 6.456,
                "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "The shaded areas are identical, demonstrating that 1/2 equals 2/4.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "equals_sign",
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "Write",
                    "target_ids": [
                        "label_left",
                        "label_right",
                        "equals_sign"
                    ],
                    "details": "Add fraction labels and equals sign between pizzas"
                },
                "duration": 5.856,
                "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_07.mp3"
            }
        ]
        
        # Add title and explanation at the beginning
        self.add(title, explanation_text)
        
        # Animate according to sequence
        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_path = step.get("audio_path")
            
            # === AUDIO (MANDATORY) ===
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)
            
            # Signal Action
            signal_action = step.get("signal_action")
            if signal_action is not None:
                target_id = signal_action["target"]
                target_obj = self.objects[target_id]
                color_str = signal_action.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
                color = color_map.get(color_str, YELLOW)
                
                if signal_action["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal_action["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal_action["type"] == "FocusOn":
                    self.play(FocusOn(target_obj))
            
            # Visual Action
            visual_action = step["visual_action"]
            action_type = visual_action["type"]
            
            if action_type == "Create":
                if "target_id" in visual_action:
                    target_id = visual_action["target_id"]
                    target_obj = self.objects[target_id]
                    self.play(Create(target_obj))
                elif "target_ids" in visual_action:
                    target_ids = visual_action["target_ids"]
                    target_objs = [self.objects[tid] for tid in target_ids]
                    self.play(*[Create(obj) for obj in target_objs])
            
            elif action_type == "TransformMatchingShapes":
                # Morph sector_half into sector_q1 and sector_q2
                target_id = visual_action["target_id"]
                source_obj = self.objects[target_id]
                
                # Create target group (quarters)
                target_group = VGroup(sector_q1, sector_q2)
                
                # Transform
                self.play(TransformMatchingShapes(source_obj, target_group))
            
            elif action_type == "ReplacementTransform":
                # Transform pizza_main into two smaller pizzas at left and right
                source_obj = self.objects[visual_action["target_id"]]
                
                # Create target group: pizza_left and pizza_right at their positions
                # First, create copies at original position
                pizza_left_copy = pizza_left.copy().move_to(main_stage).scale(2/1.5)  # Scale to match original size
                pizza_right_copy = pizza_right.copy().move_to(main_stage).scale(2/1.5)
                target_group = VGroup(pizza_left_copy, pizza_right_copy)
                
                # Transform source into target group
                self.play(ReplacementTransform(source_obj, target_group))
                
                # Now animate the group splitting and scaling down
                self.play(
                    pizza_left_copy.animate.move_to(comparison_left).scale(1.5/2),
                    pizza_right_copy.animate.move_to(comparison_right).scale(1.5/2)
                )
                
                # Remove copies and add the actual pizza_left and pizza_right
                self.remove(pizza_left_copy, pizza_right_copy)
                self.add(pizza_left, pizza_right)
            
            elif action_type == "Write":
                target_ids = visual_action["target_ids"]
                target_objs = [self.objects[tid] for tid in target_ids]
                self.play(*[Write(obj) for obj in target_objs])
            
            # Calculate remaining wait time
            anim_time = 2.0  # base for visual action
            if signal_action is not None:
                anim_time += 1.0
            remaining = duration - anim_time + 0.5  # safety buffer
            if remaining > 0:
                self.wait(remaining)
        
        # Final wait
        self.wait(2)