from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # Object registry
        objects = {}
        
        # Color mapping
        color_map = {
            "YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE,
            "WHITE": WHITE, "BLACK": BLACK
        }
        
        # Scene setup
        scene_setup = {
            "background": "BLACK",
            "static_objects": [
                {
                    "id": "title",
                    "type": "Text",
                    "content": "Addition of 42 and 54",
                    "pos": "UP*3.5",
                    "color": "WHITE"
                }
            ]
        }
        
        # Create static objects
        for obj in scene_setup["static_objects"]:
            if obj["type"] == "Text":
                text_obj = Text(obj["content"]).shift(self.parse_position(obj["pos"])).set_color(color_map.get(obj.get("color"), WHITE))
                objects[obj["id"]] = text_obj
                self.add(text_obj)
        
        # Process sequence steps
        sequence = [
            {
                "step": 1,
                "narrative": "Let's start with the ones column: two plus four",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "ones_col",
                    "color": "YELLOW",
                    "description": "Highlighting ones place"
                },
                "visual_action": {
                    "type": "Write",
                    "target": {
                        "id": "ones_col",
                        "type": "MathTex",
                        "content": "2 + 4",
                        "pos": "RIGHT*2"
                    },
                    "details": "Show ones column"
                },
                "duration": 3.696,
                "audio_path": "media/audio/42+54/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "That gives us six. Now, let's move to the tens column: forty plus fifty",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "tens_col",
                    "color": "YELLOW",
                    "description": "Highlighting tens place"
                },
                "visual_action": {
                    "type": "Write",
                    "target": {
                        "id": "tens_col",
                        "type": "MathTex",
                        "content": "40 + 50",
                        "pos": "RIGHT*2 + UP*1.5"
                    },
                    "details": "Show tens column"
                },
                "duration": 6.36,
                "audio_path": "media/audio/42+54/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "That gives us ninety. Now, let's combine the results: ninety plus six",
                "signal_action": {
                    "type": "Indicate",
                    "target": "result",
                    "color": "GREEN",
                    "description": "Pointing to the final result"
                },
                "visual_action": {
                    "type": "Transform",
                    "target": {
                        "id": "result",
                        "type": "MathTex",
                        "content": "96",
                        "pos": "RIGHT*2 + DOWN*1.5"
                    },
                    "details": "Show the final result"
                },
                "duration": 6.096,
                "audio_path": "media/audio/42+54/step_02.mp3"
            }
        ]
        
        for step in sequence:
            # Load audio with file existence check
            audio_file = None
            if "audio_path" in step and step["audio_path"]:
                audio_file = step["audio_path"]
            else:
                step_num = step.get("step", 0)
                file_index = step_num - 1
                mp3_path = f"media/audio/step_{file_index:02d}.mp3"
                if os.path.exists(mp3_path):
                    audio_file = mp3_path
                else:
                    wav_path = f"media/audio/step_{file_index:02d}.wav"
                    if os.path.exists(wav_path):
                        audio_file = wav_path
            
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            if step.get("signal_action"):  # signal_action exists
                signal = step["signal_action"]
                signal_type = signal["type"]
                target_id = signal["target"]
                color = color_map.get(signal.get("color"), YELLOW)
                
                if target_id not in objects:
                    # Create target object if it doesn't exist
                    target = step["visual_action"]["target"]
                    if target["type"] == "MathTex":
                        obj = MathTex(target["content"]).shift(self.parse_position(target["pos"]))
                    elif target["type"] == "Text":
                        obj = Text(target["content"]).shift(self.parse_position(target["pos"]))
                    objects[target_id] = obj
                
                target_obj = objects[target_id]
                if signal_type == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal_type == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal_type == "FocusOn":
                    self.play(FocusOn(target_obj))
            
            visual = step["visual_action"]
            target = visual["target"]
            if target["type"] == "MathTex":
                obj = MathTex(target["content"]).shift(self.parse_position(target["pos"]))
            elif target["type"] == "Text":
                obj = Text(target["content"]).shift(self.parse_position(target["pos"]))
            objects[target["id"]] = obj
            
            if visual["type"] == "Write":
                self.play(Write(obj))
            elif visual["type"] == "Transform":
                src_id = [k for k, v in objects.items() if isinstance(v, MathTex) and v.tex_string == visual["target"]["content"]][0]
                src_obj = objects[src_id]
                self.play(Transform(src_obj, obj))
            
            animation_time = 1 + 1  # signal + visual
            remaining = step["duration"] - animation_time
            if remaining > 0:
                self.wait(remaining)
        
        self.wait(2)
    
    def parse_position(self, position_str):
        if position_str == "ORIGIN" or position_str == "CENTER":
            return ORIGIN
        elif position_str == "UL":
            return UL
        elif position_str == "UR":
            return UR
        elif position_str == "DL":
            return DL
        elif position_str == "DR":
            return DR
        else:
            import re
            match = re.match(r"(\w+)\*(\d+(?:\.\d+)?)", position_str)
            if match:
                direction, multiplier = match.groups()
                multiplier = float(multiplier)
                if direction == "UP":
                    return multiplier * UP
                elif direction == "DOWN":
                    return multiplier * DOWN
                elif direction == "LEFT":
                    return multiplier * LEFT
                elif direction == "RIGHT":
                    return multiplier * RIGHT
            match = re.match(r"(\w+)\*(\d+(?:\.\d+)?)\s*\+\s*(\w+)\*(\d+(?:\.\d+)?)", position_str)
            if match:
                direction1, multiplier1, direction2, multiplier2 = match.groups()
                multiplier1, multiplier2 = float(multiplier1), float(multiplier2)
                if direction1 == "UP":
                    vec1 = multiplier1 * UP
                elif direction1 == "DOWN":
                    vec1 = multiplier1 * DOWN
                elif direction1 == "LEFT":
                    vec1 = multiplier1 * LEFT
                elif direction1 == "RIGHT":
                    vec1 = multiplier1 * RIGHT
                if direction2 == "UP":
                    vec2 = multiplier2 * UP
                elif direction2 == "DOWN":
                    vec2 = multiplier2 * DOWN
                elif direction2 == "LEFT":
                    vec2 = multiplier2 * LEFT
                elif direction2 == "RIGHT":
                    vec2 = multiplier2 * RIGHT
                return vec1 + vec2