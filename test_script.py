from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # Object registry
        objects = {}
        
        # Scene setup
        title = Text("導數的定義").shift(3.5 * UP)
        self.add(title)
        objects["title"] = title
        
        # Process sequence steps
        data = {
            "rationale": "Using a limit-based definition to introduce the concept of derivatives, with clear signaling to highlight key components of the definition.",
            "scene_setup": {
                "background": "WHITE",
                "static_objects": [
                    {
                        "id": "title",
                        "type": "Text",
                        "content": "導數的定義",
                        "pos": "UP*3.5",
                        "color": "BLACK"
                    }
                ]
            },
            "sequence": [
                {
                    "step": 1,
                    "narrative": "Let's start with the definition of a derivative, which is based on limits.",
                    "signal_action": {"type": "Circumscribe", "target": "limit_expression", "color": "YELLOW", "description": "Highlighting the limit expression"},
                    "visual_action": {"type": "Write", "target": {"id": "limit_expression", "type": "MathTex", "content": "\\lim_{h \\to 0} \\frac{f(x + h) - f(x)}{h}", "pos": "CENTER"}, "details": "Show the limit definition of a derivative"},
                    "duration": 4.0,
                    "audio_path": None
                },
                {
                    "step": 2,
                    "narrative": "The derivative of a function f at point x is the limit as h approaches zero of the difference quotient.",
                    "signal_action": {"type": "Indicate", "target": "difference_quotient", "color": "BLUE", "description": "Pointing to the difference quotient"},
                    "visual_action": {"type": "Transform", "target": {"id": "difference_quotient", "type": "MathTex", "content": "\\frac{f(x + h) - f(x)}{h}", "pos": "CENTER + DOWN*1"}, "details": "Highlight the difference quotient part of the definition"},
                    "duration": 3.5,
                    "audio_path": None
                },
                {
                    "step": 3,
                    "narrative": "As h approaches zero, the difference quotient approaches the derivative of the function at x.",
                    "signal_action": {"type": "FocusOn", "target": "h_approaches_zero", "color": "RED", "description": "Zooming in on h approaching zero"},
                    "visual_action": {"type": "Transform", "target": {"id": "h_approaches_zero", "type": "MathTex", "content": "h \\to 0", "pos": "CENTER + DOWN*2"}, "details": "Show h approaching zero"},
                    "duration": 3.0,
                    "audio_path": None
                },
                {
                    "step": 4,
                    "narrative": "This definition allows us to calculate the derivative of a function at any point, which represents the rate of change of the function at that point.",
                    "signal_action": {"type": "Circumscribe", "target": "derivative_representation", "color": "GREEN", "description": "Highlighting the derivative representation"},
                    "visual_action": {"type": "Create", "target": {"id": "derivative_representation", "type": "MathTex", "content": "f'(x) = \\lim_{h \\to 0} \\frac{f(x + h) - f(x)}{h}", "pos": "CENTER + DOWN*3"}, "details": "Show the derivative representation"},
                    "duration": 4.5,
                    "audio_path": None
                }
            ]
        }
        sequence = data["sequence"]
        
        for i, step in enumerate(sequence):
            # Load audio with file existence check
            audio_file = None
            if step.get("audio_path"):
                audio_file = step["audio_path"]
            else:
                mp3_path = f"media/audio/step_{i:02d}.mp3"
                if os.path.exists(mp3_path):
                    audio_file = mp3_path
                else:
                    wav_path = f"media/audio/step_{i:02d}.wav"
                    if os.path.exists(wav_path):
                        audio_file = wav_path
            
            if audio_file:
                self.add_sound(audio_file)
            
            if step.get("signal_action"):  # signal_action exists
                signal = step["signal_action"]
                signal_type = signal["type"]
                target_id = signal["target"]
                color = signal.get("color", "YELLOW")  # Default to YELLOW
                
                if target_id in objects:
                    target_obj = objects[target_id]
                else:
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
                    
                    obj.shift(parse_position(position))  # You need to parse position string
                    objects[obj_id] = obj  # STORE IT
                    target_obj = obj
                
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
            
            obj.shift(parse_position(position))  # You need to parse position string
            objects[obj_id] = obj  # STORE IT
            
            if visual["type"] == "Write":
                self.play(Write(obj))
            elif visual["type"] == "Transform":
                src_id = visual.get("source", {}).get("id")
                if src_id in objects:
                    src_obj = objects[src_id]
                    self.play(Transform(src_obj, obj))
                else:
                    self.play(Write(obj))
            elif visual["type"] == "Create":
                self.play(Write(obj))
            
            animation_time = 1  # signal + visual
            remaining = step["duration"] - animation_time
            if remaining > 0:
                self.wait(remaining)

def parse_position(position):
    if position == "UP*3.5":
        return 3.5 * UP
    elif position == "CENTER":
        return ORIGIN
    elif position == "CENTER + DOWN*1":
        return ORIGIN + DOWN
    elif position == "CENTER + DOWN*2":
        return ORIGIN + 2 * DOWN
    elif position == "CENTER + DOWN*3":
        return ORIGIN + 3 * DOWN
    else:
        return ORIGIN