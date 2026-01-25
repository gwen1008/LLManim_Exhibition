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
        title = Text("Addition: 45 + 9", color=WHITE).shift(3.5 * UP)
        self.add(title)
        objects["title"] = title
        
        # Process sequence steps
        sequence = [
            {
              "step": 1,
              "narrative": "First, let's look at the ones column: five plus nine",
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
                  "content": "5 + 9",
                  "pos": "RIGHT*2"
                },
                "details": "Show ones column"
              },
              "duration": 4.344,
              "audio_path": "media\\audio\\45+9\\step_00.mp3"
            },
            {
              "step": 2,
              "narrative": "That gives us fourteen. We write four and carry one",
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
                "details": "Small '1' above tens column"
              },
              "duration": 4.704,
              "audio_path": "media\\audio\\45+9\\step_01.mp3"
            },
            {
              "step": 3,
              "narrative": "Now, let's add the carry to the tens column: four plus one plus zero",
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
                  "content": "4 + 1 + 0",
                  "pos": "RIGHT*2 + UP*1"
                },
                "details": "Show tens column with carry"
              },
              "duration": 4.968,
              "audio_path": "media\\audio\\45+9\\step_02.mp3"
            },
            {
              "step": 4,
              "narrative": "That gives us five. So, our final answer is fifty-four",
              "signal_action": None,
              "visual_action": {
                "type": "Transform",
                "target": {
                  "id": "final_answer",
                  "type": "MathTex",
                  "content": "54",
                  "pos": "RIGHT*2 + DOWN*1"
                },
                "details": "Replace calculation with final result"
              },
              "duration": 5.256,
              "audio_path": "media\\audio\\45+9\\step_03.mp3"
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
                color = color_map.get(signal.get("color", "YELLOW"))
                
                if target_id in objects:
                    target_obj = objects[target_id]
                    if signal_type == "Circumscribe":
                        self.play(Circumscribe(target_obj, color=color, run_time=1))
                    elif signal_type == "Indicate":
                        self.play(Indicate(target_obj, color=color))
                    elif signal_type == "FocusOn":
                        self.play(FocusOn(target_obj))
            
            visual = step["visual_action"]
            target = visual["target"]
            obj_id = target["id"]
            obj_type = target["type"]
            content = target["content"]
            position = target["pos"]
            
            if obj_type == "MathTex":
                obj = MathTex(content)
            elif obj_type == "Text":
                obj = Text(content)
            
            obj.shift(eval(position))
            
            if "color" in target:
                obj.set_color(color_map.get(target["color"], WHITE))
            
            objects[obj_id] = obj
            
            if visual["type"] == "Write":
                self.play(Write(obj))
            elif visual["type"] == "Create":
                self.play(Create(obj))
            elif visual["type"] == "Transform":
                src_id = [k for k, v in objects.items() if v == obj][0]
                src_obj = objects[src_id]
                self.play(Transform(src_obj, obj))
            
            animation_time = 1  # signal + visual
            if step.get("signal_action"):
                animation_time += 1
            remaining = step["duration"] - animation_time
            if remaining > 0:
                self.wait(remaining)