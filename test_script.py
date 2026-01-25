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
        title = Text("Adding Decimals: 6.8 + 9.6", color=WHITE).shift(3.5 * UP)
        self.add(title)
        objects["title"] = title
        
        # Process sequence steps
        sequence = [
            {
                "step": 1,
                "narrative": "First, let's align the decimal points and add the tenths place: 8 + 6",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "tenths_column",
                    "color": "YELLOW",
                    "description": "Highlighting tenths place"
                },
                "visual_action": {
                    "type": "Write",
                    "target": {
                        "id": "tenths_column",
                        "type": "MathTex",
                        "content": "8 + 6",
                        "pos": "RIGHT*2"
                    },
                    "details": "Show tenths column addition"
                },
                "duration": 5.352,
                "audio_path": "media/audio/6_8+9_6/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "That gives us fourteen. We write four and carry one to the ones place",
                "signal_action": {
                    "type": "Indicate",
                    "target": "carry_one",
                    "color": "RED",
                    "description": "Pointing to carry digit"
                },
                "visual_action": {
                    "type": "Create",
                    "target": {
                        "id": "carry_one",
                        "type": "Text",
                        "content": "1",
                        "pos": "UP*1.5 + RIGHT*1.5"
                    },
                    "details": "Small '1' above ones column"
                },
                "duration": 5.616,
                "audio_path": "media/audio/6_8+9_6/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, let's add the ones place: 6 + 9 + 1",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "ones_column",
                    "color": "YELLOW",
                    "description": "Highlighting ones place"
                },
                "visual_action": {
                    "type": "Write",
                    "target": {
                        "id": "ones_column",
                        "type": "MathTex",
                        "content": "6 + 9 + 1",
                        "pos": "RIGHT*2 + UP*1"
                    },
                    "details": "Show ones column addition with carry"
                },
                "duration": 4.2,
                "audio_path": "media/audio/6_8+9_6/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "That gives us sixteen. So, the result is 16.4",
                "signal_action": None,
                "visual_action": {
                    "type": "Transform",
                    "target": {
                        "id": "result",
                        "type": "MathTex",
                        "content": "16.4",
                        "pos": "RIGHT*2 + DOWN*1"
                    },
                    "details": "Show final result"
                },
                "duration": 5.4,
                "audio_path": "media/audio/6_8+9_6/step_03.mp3"
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
                    audio_file = wav_path if os.path.exists(wav_path) else None
            
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            if step.get("signal_action"):  # signal_action exists
                signal = step["signal_action"]
                signal_type = signal["type"]
                target_id = signal["target"]
                color = color_map.get(signal.get("color", "YELLOW"))
                
                # Find the target object by ID (must already be created)
                if target_id not in objects:
                    # Create the target object if it doesn't exist
                    visual = step["visual_action"]
                    target = visual["target"]
                    obj_type = target["type"]
                    content = target["content"]
                    position = target["pos"]
                    
                    if obj_type == "MathTex":
                        obj = MathTex(content)
                    elif obj_type == "Text":
                        obj = Text(content)
                    
                    obj.shift(eval(position))
                    objects[target_id] = obj
                
                target_obj = objects[target_id]
                
                # Execute the signal animation
                if signal_type == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal_type == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal_type == "FocusOn":
                    self.play(FocusOn(target_obj))
            
            # Handle visual_action
            visual = step["visual_action"]
            target = visual["target"]
            obj_type = target["type"]
            content = target["content"]
            position = target["pos"]
            
            if obj_type == "MathTex":
                obj = MathTex(content)
            elif obj_type == "Text":
                obj = Text(content)
            
            obj.shift(eval(position))
            objects[target["id"]] = obj
            
            if visual["type"] == "Write":
                self.play(Write(obj))
            elif visual["type"] == "Create":
                self.play(Create(obj))
            elif visual["type"] == "Transform":
                src_id = None
                for prev_step in sequence:
                    if prev_step["step"] < step["step"]:
                        prev_visual = prev_step["visual_action"]
                        if prev_visual["target"]["id"] == target["id"]:
                            src_id = prev_visual["target"]["id"]
                            break
                if src_id:
                    src_obj = objects[src_id]
                    self.play(Transform(src_obj, obj))
            
            # Calculate remaining time after animations
            animation_time = 1  # signal + visual
            if step.get("signal_action"):
                animation_time += 1
            remaining = step["duration"] - animation_time
            if remaining > 0:
                self.wait(remaining)