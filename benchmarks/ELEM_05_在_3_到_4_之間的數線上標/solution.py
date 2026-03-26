from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        obj_registry = {}

        # Helper to parse position strings (simplified for this specific JSON)
        def parse_position(pos_str, ref_obj=None):
            if pos_str == "move_to(title_anchor)":
                return UP * 3.5
            elif pos_str == "move_to(number_line_center)":
                return ORIGIN
            elif pos_str == "move_to(explanation_anchor)":
                return DOWN * 2.5
            elif pos_str == "move_to(number_line_center + LEFT*3)":
                return LEFT * 3
            elif pos_str == "move_to(number_line_center + RIGHT*3)":
                return RIGHT * 3
            elif pos_str == "move_to(number_line_center + RIGHT*1.2)":
                return RIGHT * 1.2
            elif pos_str == "move_to(number_line_center + UP*2)":
                return UP * 2
            elif pos_str == "move_to(dot_3_7.get_center() + UP*0.5)":
                # This will be handled after dot_3_7 is created
                if "dot_3_7" in obj_registry:
                    return obj_registry["dot_3_7"].get_center() + UP * 0.5
                else:
                    return RIGHT * 1.2 + UP * 0.5  # Fallback
            elif pos_str.startswith("next_to"):
                # Parse next_to(tick_3, DOWN, buff=0.2)
                parts = pos_str.replace("next_to(", "").replace(")", "").split(",")
                target_id = parts[0].strip()
                direction = eval(parts[1].strip())
                buff = float(parts[2].strip().split("=")[1]) if len(parts) > 2 else 0.2
                if target_id in obj_registry:
                    # Use .height attribute instead of deprecated get_height()
                    return obj_registry[target_id].get_center() + direction * (obj_registry[target_id].height/2 + buff)
                else:
                    return ORIGIN
            else:
                return ORIGIN

        # Color mapping
        color_map = {
            "YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE,
            "WHITE": WHITE, "LIGHT_GRAY": LIGHT_GRAY
        }

        # Create objects from layout_plan.objects
        # We'll create them but not add to scene yet (they will be added via Create animations)
        objects_data = [
            {
                "id": "title",
                "type": "Text",
                "content": "Rounding on a Number Line",
                "initial_pos": "move_to(title_anchor)",
                "properties": {"color": "WHITE", "font_size": 40},
            },
            {
                "id": "number_line",
                "type": "NumberLine",
                "geometry_def": "x_range=[3, 4, 0.1], length=6, include_numbers=False",
                "initial_pos": "move_to(number_line_center)",
                "properties": {"color": "LIGHT_GRAY"},
            },
            {
                "id": "tick_3",
                "type": "Line",
                "geometry_def": "start=DOWN*0.15, end=UP*0.15",
                "initial_pos": "move_to(number_line_center + LEFT*3)",
                "properties": {"color": "WHITE", "stroke_width": 3},
            },
            {
                "id": "label_3",
                "type": "MathTex",
                "content": "3",
                "initial_pos": "next_to(tick_3, DOWN, buff=0.2)",
                "properties": {"color": "WHITE"},
            },
            {
                "id": "tick_4",
                "type": "Line",
                "geometry_def": "start=DOWN*0.15, end=UP*0.15",
                "initial_pos": "move_to(number_line_center + RIGHT*3)",
                "properties": {"color": "WHITE", "stroke_width": 3},
            },
            {
                "id": "label_4",
                "type": "MathTex",
                "content": "4",
                "initial_pos": "next_to(tick_4, DOWN, buff=0.2)",
                "properties": {"color": "WHITE"},
            },
            {
                "id": "midpoint_line",
                "type": "DashedLine",
                "geometry_def": "start=UP*1, end=DOWN*1",
                "initial_pos": "move_to(number_line_center)",
                "properties": {"color": "YELLOW", "dash_length": 0.1},
            },
            {
                "id": "label_3_5",
                "type": "MathTex",
                "content": "3.5",
                "initial_pos": "next_to(midpoint_line, UP, buff=0.2)",
                "properties": {"color": "YELLOW"},
            },
            {
                "id": "dot_3_7",
                "type": "Dot",
                "geometry_def": "radius=0.08",
                "initial_pos": "move_to(number_line_center + RIGHT*1.2)",
                "properties": {"color": "GREEN"},
            },
            {
                "id": "label_3_7_point",
                "type": "MathTex",
                "content": "3.7",
                "initial_pos": "next_to(dot_3_7, UP, buff=0.2)",
                "properties": {"color": "GREEN"},
            },
            {
                "id": "pointer",
                "type": "Triangle",
                "geometry_def": "fill_opacity=1, color=BLUE, start_angle=-PI/2",
                "initial_pos": "move_to(dot_3_7.get_center() + UP*0.5)",
                "properties": {"color": "BLUE", "fill_opacity": 1, "height": 0.4, "width": 0.4},
            },
            {
                "id": "value_display_initial",
                "type": "MathTex",
                "content": "3.7",
                "initial_pos": "move_to(number_line_center + UP*2)",
                "properties": {"color": "GREEN", "font_size": 48},
            },
            {
                "id": "value_display_final",
                "type": "MathTex",
                "content": "4",
                "initial_pos": "move_to(number_line_center + UP*2)",
                "properties": {"color": "RED", "font_size": 48},
            },
            {
                "id": "explanation_text",
                "type": "Text",
                "content": "",
                "initial_pos": "move_to(explanation_anchor)",
                "properties": {"color": "LIGHT_GRAY", "font_size": 24},
            }
        ]

        for obj_data in objects_data:
            obj_id = obj_data["id"]
            obj_type = obj_data["type"]
            content = obj_data.get("content", "")
            pos_str = obj_data["initial_pos"]
            props = obj_data.get("properties", {})

            # Create object based on type
            if obj_type == "Text":
                obj = Text(content, font_size=props.get("font_size", 24))
            elif obj_type == "MathTex":
                obj = MathTex(content)
                if "font_size" in props:
                    obj.scale(props["font_size"] / 48)  # 48 is default reference
            elif obj_type == "NumberLine":
                # Parse geometry_def: "x_range=[3, 4, 0.1], length=6, include_numbers=False"
                # This is simplified parsing for this specific case
                obj = NumberLine(
                    x_range=[3, 4, 0.1],
                    length=6,
                    include_numbers=False,
                    color=color_map.get(props.get("color", "LIGHT_GRAY"), LIGHT_GRAY)
                )
            elif obj_type == "Line":
                # geometry_def: "start=DOWN*0.15, end=UP*0.15"
                obj = Line(DOWN*0.15, UP*0.15, stroke_width=props.get("stroke_width", 2))
            elif obj_type == "DashedLine":
                # geometry_def: "start=UP*1, end=DOWN*1"
                obj = DashedLine(UP*1, DOWN*1, dash_length=props.get("dash_length", 0.1))
            elif obj_type == "Dot":
                obj = Dot(radius=props.get("radius", 0.08))
            elif obj_type == "Triangle":
                # Create triangle with default size, then scale it
                obj = Triangle(color=color_map.get(props.get("color", "BLUE"), BLUE))
                obj.set_fill(color=color_map.get(props.get("color", "BLUE"), BLUE), opacity=props.get("fill_opacity", 1))
                # Use scale instead of set_height/set_width to avoid deprecation warnings
                scale_factor = props.get("height", 0.4) / obj.height
                obj.scale(scale_factor)
                # Rotate to point down (start_angle=-PI/2)
                obj.rotate(-PI/2)
            else:
                continue  # Skip unknown types

            # Apply color
            if "color" in props:
                obj.set_color(color_map.get(props["color"], WHITE))

            # Position
            pos = parse_position(pos_str, obj_registry)
            obj.move_to(pos)

            # Special handling for pointer position (needs dot_3_7)
            if obj_id == "pointer" and "dot_3_7" in obj_registry:
                obj.move_to(obj_registry["dot_3_7"].get_center() + UP * 0.5)

            # Store in registry
            obj_registry[obj_id] = obj

        # Create value_display_final but keep it invisible initially
        obj_registry["value_display_final"].set_opacity(0)

        # Create explanation text (empty initially)
        obj_registry["explanation_text"].set_opacity(0)

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's look at a number line from 3 to 4.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "number_line", "details": "Draw the number line."},
                "duration": 3.144,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3_7，並標出距離來解釋為什麼它四捨五入後是_4。/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "We mark the endpoints: 3 and 4.",
                "signal_action": {"type": "Indicate", "target": "tick_3", "color": "WHITE"},
                "visual_action": {"type": "Create", "target_id": ["tick_3", "label_3", "tick_4", "label_4"], "details": "Draw the endpoint ticks and labels simultaneously."},
                "duration": 3.264,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3_7，並標出距離來解釋為什麼它四捨五入後是_4。/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "The midpoint between them is 3.5. This is our decision boundary for rounding.",
                "signal_action": {"type": "Circumscribe", "target": "label_3_5", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": ["midpoint_line", "label_3_5"], "details": "Draw the dashed vertical line and its label."},
                "duration": 6.024,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3_7，並標出距離來解釋為什麼它四捨五入後是_4。/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "Now consider the number 3.7. We place it on the number line.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": ["dot_3_7", "label_3_7_point", "pointer", "value_display_initial"], "details": "Show the dot, its label, the pointer above it, and the numerical display showing 3.7."},
                "duration": 5.304,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3_7，並標出距離來解釋為什麼它四捨五入後是_4。/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Observe: 3.7 is to the right of 3.5. The distance from 3.7 to 4 is shorter than the distance from 3.7 to 3.",
                "signal_action": {"type": "Indicate", "target": "midpoint_line", "color": "YELLOW"},
                "visual_action": {"type": "Animation", "target_id": None, "details": "Temporarily highlight the segment from the dot to the midpoint line in one color (e.g., RED for 'far side') and from the dot to tick_4 in another (e.g., GREEN for 'near side'). This could be done with temporary Lines created and faded out."},
                "duration": 9.336,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3_7，並標出距離來解釋為什麼它四捨五入後是_4。/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "Therefore, 3.7 is closer to 4. When rounding to the nearest integer, it rounds up to 4.",
                "signal_action": {"type": "Indicate", "target": "value_display_initial", "color": "GREEN"},
                "visual_action": {"type": "Transform", "target_id": "pointer", "details": "Move the pointer from its position above 3.7 to a position above 4 (screen x=3). Create a target pointer at the new location and transform the original to it."},
                "duration": 7.488,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3_7，並標出距離來解釋為什麼它四捨五入後是_4。/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "The value updates from 3.7 to 4.",
                "signal_action": {"type": "Indicate", "target": "value_display_final", "color": "RED"},
                "visual_action": {"type": "ReplacementTransform", "target_id": ["value_display_initial", "value_display_final"], "details": "Morph the numerical display from '3.7' to '4'."},
                "duration": 3.36,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3_7，並標出距離來解釋為什麼它四捨五入後是_4。/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "Thus, 3.7 rounded to the nearest integer is 4.",
                "signal_action": None,
                "visual_action": {"type": "Wait", "target_id": None, "details": "Hold the final frame for a moment."},
                "duration": 4.272,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3_7，並標出距離來解釋為什麼它四捨五入後是_4。/step_07.mp3"
            }
        ]

        for step in sequence:
            step_num = step["step"]
            audio_file = step.get("audio_path")
            
            # === AUDIO (MANDATORY) ===
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # Signal action
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                color = color_map.get(signal.get("color", "YELLOW"), YELLOW)
                target_obj = obj_registry.get(target_id)
                
                if target_obj and signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif target_obj and signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif target_obj and signal["type"] == "FocusOn":
                    self.play(FocusOn(target_obj))
            
            # Visual action
            visual = step["visual_action"]
            action_type = visual["type"]
            target_id = visual["target_id"]
            
            if action_type == "Create":
                if isinstance(target_id, list):
                    # Create multiple objects
                    anims = [Create(obj_registry[tid]) for tid in target_id if tid in obj_registry]
                    if anims:
                        self.play(*anims)
                elif target_id in obj_registry:
                    self.play(Create(obj_registry[target_id]))
            
            elif action_type == "Animation" and step_num == 5:
                # Step 5: Create temporary distance lines
                dot = obj_registry["dot_3_7"]
                midpoint = obj_registry["midpoint_line"]
                tick_4 = obj_registry["tick_4"]
                tick_3 = obj_registry["tick_3"]
                
                # Line from dot to midpoint (far side, RED)
                line_to_mid = Line(dot.get_center(), midpoint.get_start(), color=RED, stroke_width=4)
                # Line from dot to 4 (near side, GREEN)
                line_to_4 = Line(dot.get_center(), tick_4.get_start(), color=GREEN, stroke_width=4)
                # Line from dot to 3 (for comparison, GRAY)
                line_to_3 = Line(dot.get_center(), tick_3.get_start(), color=LIGHT_GRAY, stroke_width=2)
                
                self.play(Create(line_to_mid), Create(line_to_4), Create(line_to_3))
                self.wait(1)
                self.play(FadeOut(line_to_mid), FadeOut(line_to_4), FadeOut(line_to_3))
            
            elif action_type == "Transform" and step_num == 6:
                # Step 6: Move pointer to above 4
                pointer = obj_registry["pointer"]
                # Create target pointer at position above 4 (x=3)
                target_pointer = Triangle(color=BLUE, fill_opacity=1)
                target_pointer.set_fill(color=BLUE, opacity=1)
                # Scale to match original pointer size
                scale_factor = 0.4 / target_pointer.height
                target_pointer.scale(scale_factor)
                target_pointer.rotate(-PI/2)
                target_pointer.move_to(RIGHT*3 + UP*0.5)
                
                self.play(Transform(pointer, target_pointer))
            
            elif action_type == "ReplacementTransform" and step_num == 7:
                # Step 7: Transform value display
                initial = obj_registry["value_display_initial"]
                final = obj_registry["value_display_final"]
                final.set_opacity(1)  # Make visible
                self.play(ReplacementTransform(initial, final))
            
            elif action_type == "Wait":
                # Step 8: Just wait (no animation)
                pass
            
            # Calculate remaining wait time
            # Estimate animation runtime: signal (1s) + visual (varies)
            visual_time = 0
            if action_type == "Create":
                visual_time = 1.5
            elif action_type == "Animation" and step_num == 5:
                visual_time = 3  # Lines creation + fade out
            elif action_type == "Transform" and step_num == 6:
                visual_time = 1.5
            elif action_type == "ReplacementTransform" and step_num == 7:
                visual_time = 1.5
            
            signal_time = 1 if signal is not None else 0
            total_anim_time = signal_time + visual_time
            
            remaining = step["duration"] - total_anim_time
            if remaining > 0:
                self.wait(remaining)