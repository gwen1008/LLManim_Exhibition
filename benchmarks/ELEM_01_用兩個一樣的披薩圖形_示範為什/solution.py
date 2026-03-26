from manim import *
import numpy as np
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        
        # Create Anchors (as dummy mobjects for reference)
        title_anchor = Dot(point=ORIGIN).set_opacity(0)
        left_pizza_anchor = Dot(point=3*LEFT).set_opacity(0)
        right_pizza_anchor = Dot(point=3*RIGHT).set_opacity(0)
        center_stage = Dot(point=ORIGIN).set_opacity(0)
        footer_anchor = Dot(point=ORIGIN).set_opacity(0)
        
        # Title
        title = Text("Visualizing Equivalent Fractions", font_size=48, color=WHITE)
        title.move_to(UP * 3.5)
        
        # Left Pizza Circle
        pizza_left_circle = Circle(radius=2, color=WHITE, stroke_width=3)
        pizza_left_circle.move_to(LEFT * 3)
        
        # Right Pizza Circle
        pizza_right_circle = Circle(radius=2, color=WHITE, stroke_width=3)
        pizza_right_circle.move_to(RIGHT * 3)
        
        # Divider Line Left (Vertical line for halves)
        divider_line_left = Line(
            start=pizza_left_circle.get_center() + UP * 2,
            end=pizza_left_circle.get_center() + DOWN * 2,
            color=WHITE, stroke_width=3
        )
        
        # Divider Lines Right (Four radial lines for quarters)
        angles = [0, PI/2, PI, 3*PI/2]
        lines_right = VGroup()
        for angle in angles:
            line = Line(
                start=pizza_right_circle.get_center(),
                end=pizza_right_circle.get_center() + 2 * np.array([np.cos(angle), np.sin(angle), 0]),
                color=WHITE, stroke_width=3
            )
            lines_right.add(line)
        
        # Shading Left (Half pizza sector) - FIXED: Use AnnularSector with correct parameters
        shading_left = AnnularSector(
            inner_radius=0,
            outer_radius=2,
            angle=PI,
            start_angle=-PI/2,
            color="#FF6B6B",
            fill_opacity=0.7,
            stroke_width=0
        )
        shading_left.move_to(pizza_left_circle.get_center())
        
        # Shading Right (Two quarters: top and bottom) - FIXED: Use AnnularSector
        sector1 = AnnularSector(
            inner_radius=0,
            outer_radius=2,
            angle=PI,
            start_angle=-PI/2,
            color="#4ECDC4",
            fill_opacity=0.7,
            stroke_width=0
        )
        sector2 = AnnularSector(
            inner_radius=0,
            outer_radius=2,
            angle=PI,
            start_angle=PI/2,
            color="#4ECDC4",
            fill_opacity=0.7,
            stroke_width=0
        )
        shading_right = VGroup(sector1, sector2)
        shading_right.move_to(pizza_right_circle.get_center())
        
        # Label Left
        label_left = MathTex(r"\frac{1}{2}", color=WHITE, font_size=48)
        label_left.next_to(pizza_left_circle, DOWN, buff=0.8)
        
        # Label Right
        label_right = MathTex(r"\frac{2}{4}", color=WHITE, font_size=48)
        label_right.next_to(pizza_right_circle, DOWN, buff=0.8)
        
        # Conclusion Text
        conclusion_text = Text("The shaded areas are equal: 1/2 = 2/4", font_size=36, color=YELLOW)
        conclusion_text.move_to(DOWN * 3.5)
        
        # Store objects in a dictionary for easy access by ID
        objects = {
            "title": title,
            "pizza_left_circle": pizza_left_circle,
            "pizza_right_circle": pizza_right_circle,
            "divider_line_left": divider_line_left,
            "divider_lines_right": lines_right,
            "shading_left": shading_left,
            "shading_right": shading_right,
            "label_left": label_left,
            "label_right": label_right,
            "conclusion_text": conclusion_text,
        }
        
        # Initially add only the title (others will be created in sequence)
        self.add(title)
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's start with two identical whole pizzas.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "pizza_left_circle", "details": "Draw the left circle outline"},
                "duration": 3.264,
                "audio_path": "media/audio/用兩個一樣的披薩圖形，示範為什麼_1_2_等於_2_4，並塗色對比區域。/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "pizza_right_circle", "details": "Draw the right circle outline"},
                "duration": 2.0
            },
            {
                "step": 3,
                "narrative": "We divide the first pizza into two equal halves.",
                "signal_action": {"type": "Indicate", "target": "pizza_left_circle", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "divider_line_left", "details": "Draw the vertical dividing line"},
                "duration": 3.72,
                "audio_path": "media/audio/用兩個一樣的披薩圖形，示範為什麼_1_2_等於_2_4，並塗色對比區域。/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "And we shade one of these halves.",
                "signal_action": {"type": "Circumscribe", "target": "shading_left", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "shading_left", "details": "Fill the right half of the left circle with red"},
                "duration": 2.496,
                "audio_path": "media/audio/用兩個一樣的披薩圖形，示範為什麼_1_2_等於_2_4，並塗色對比區域。/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "This represents the fraction one-half.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_left", "details": "Write the label 1/2 below the left pizza"},
                "duration": 3.0,
                "audio_path": "media/audio/用兩個一樣的披薩圖形，示範為什麼_1_2_等於_2_4，並塗色對比區域。/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "Now, we divide the second pizza into four equal quarters.",
                "signal_action": {"type": "Indicate", "target": "pizza_right_circle", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "divider_lines_right", "details": "Draw the four radial dividing lines"},
                "duration": 4.392,
                "audio_path": "media/audio/用兩個一樣的披薩圖形，示範為什麼_1_2_等於_2_4，並塗色對比區域。/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "We shade two of these quarters.",
                "signal_action": {"type": "Circumscribe", "target": "shading_right", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "shading_right", "details": "Fill the top and bottom quarters of the right circle with teal"},
                "duration": 2.496,
                "audio_path": "media/audio/用兩個一樣的披薩圖形，示範為什麼_1_2_等於_2_4，並塗色對比區域。/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "This represents the fraction two-quarters.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_right", "details": "Write the label 2/4 below the right pizza"},
                "duration": 3.144,
                "audio_path": "media/audio/用兩個一樣的披薩圖形，示範為什麼_1_2_等於_2_4，並塗色對比區域。/step_07.mp3"
            },
            {
                "step": 9,
                "narrative": "To see if these fractions are equal, let's compare the shaded areas directly.",
                "signal_action": {"type": "Indicate", "target": "shading_left", "color": "YELLOW"},
                "visual_action": {"type": "Transform", "target_id": "shading_left", "details": "Move the red shaded half to the center stage, scaling it slightly for focus"},
                "duration": 5.016,
                "audio_path": "media/audio/用兩個一樣的披薩圖形，示範為什麼_1_2_等於_2_4，並塗色對比區域。/step_08.mp3"
            },
            {
                "step": 10,
                "narrative": "",
                "signal_action": {"type": "Indicate", "target": "shading_right", "color": "YELLOW"},
                "visual_action": {"type": "Transform", "target_id": "shading_right", "details": "Move the teal shaded quarters to the center stage, overlapping the red area"},
                "duration": 2.0
            },
            {
                "step": 11,
                "narrative": "Watch closely. The shaded area from the first pizza...",
                "signal_action": None,
                "visual_action": {"type": "Transform", "target_id": "shading_left", "details": "Morph the red half into the shape of the two teal quarters. This is the key equivalence transformation."},
                "duration": 4.656,
                "audio_path": "media/audio/用兩個一樣的披薩圖形，示範為什麼_1_2_等於_2_4，並塗色對比區域。/step_10.mp3"
            },
            {
                "step": 12,
                "narrative": "...perfectly matches the shaded area from the second pizza. They cover the same amount of pizza.",
                "signal_action": None,
                "visual_action": {"type": "FadeOut", "target_id": "shading_left", "details": "Fade out the morphed shape"},
                "duration": 6.504,
                "audio_path": "media/audio/用兩個一樣的披薩圖形，示範為什麼_1_2_等於_2_4，並塗色對比區域。/step_11.mp3"
            },
            {
                "step": 13,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "FadeOut", "target_id": "shading_right", "details": "Fade out the teal quarters"},
                "duration": 2.0
            },
            {
                "step": 14,
                "narrative": "Therefore, one-half is equal to two-quarters.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "conclusion_text", "details": "Display the final conclusion at the bottom of the screen"},
                "duration": 3.576,
                "audio_path": "media/audio/用兩個一樣的披薩圖形，示範為什麼_1_2_等於_2_4，並塗色對比區域。/step_13.mp3"
            }
        ]
        
        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_path = step.get("audio_path")
            
            # === AUDIO (MANDATORY) ===
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)
            # Note: For steps without audio_path, we still proceed.
            
            # Track total animation time for this step
            anim_time = 0
            
            # 1. Handle signal_action
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                target_obj = objects[target_id]
                color_str = signal.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
                color = color_map.get(color_str, YELLOW)
                
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                    anim_time += 1
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                    anim_time += 1
            
            # 2. Handle visual_action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            target_obj = objects[target_id]
            
            if visual["type"] == "Create":
                self.play(Create(target_obj))
                anim_time += 1.5  # Approximate runtime for Create
            elif visual["type"] == "Write":
                self.play(Write(target_obj))
                anim_time += 1.0
            elif visual["type"] == "Transform":
                # For steps 9 and 10: Move shaded areas to center stage
                if step_num in [9, 10]:
                    # Create a copy at the center for transformation target
                    if step_num == 9:
                        # Move shading_left to center
                        target_pos = ORIGIN
                        # Scale slightly for focus
                        transformed = target_obj.copy().scale(1.1).move_to(target_pos)
                    else: # step 10
                        # Move shading_right to center, overlapping
                        target_pos = ORIGIN
                        transformed = target_obj.copy().move_to(target_pos)
                    self.play(Transform(target_obj, transformed))
                    anim_time += 1.5
                elif step_num == 11:
                    # Morph shading_left into shading_right's shape
                    morph_target = shading_right.copy()
                    self.play(Transform(target_obj, morph_target))
                    anim_time += 2.0
                else:
                    # Generic transform
                    self.play(Transform(target_obj, target_obj.copy()))  # Placeholder
                    anim_time += 1.5
            elif visual["type"] == "FadeOut":
                self.play(FadeOut(target_obj))
                anim_time += 0.5
            
            # 3. Wait for remaining audio duration
            remaining = duration - anim_time
            if remaining > 0:
                self.wait(remaining)