from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # Object registry
        objects = {}
        
        # Scene setup
        title = Text("分數的加減").shift(3.5 * UP)
        self.add(title)
        objects["title"] = title
        
        # Process sequence steps
        sequence = [
            {
              "step": 1,
              "narrative": "Let's start with adding 1/4 and 1/4",
              "signal_action": {"type": "Circumscribe", "target": "frac_1", "color": "YELLOW", "description": "Highlighting the first fraction"},
              "visual_action": {"type": "Create", "target": {"id": "frac_1", "type": "MathTex", "content": "1/4", "pos": "RIGHT*2"}, "details": "Show the first fraction on a number line"},
              "duration": 2.5,
              "audio_path": None
            },
            {
              "step": 2,
              "narrative": "Now, let's add the second 1/4",
              "signal_action": {"type": "Indicate", "target": "frac_2", "color": "BLUE", "description": "Pointing to the second fraction"},
              "visual_action": {"type": "Create", "target": {"id": "frac_2", "type": "MathTex", "content": "1/4", "pos": "RIGHT*2 + DOWN*1"}, "details": "Show the second fraction on the same number line"},
              "duration": 2.5,
              "audio_path": None
            },
            {
              "step": 3,
              "narrative": "The sum is 2/4, which simplifies to 1/2",
              "signal_action": {"type": "FocusOn", "target": "result", "color": "GREEN", "description": "Zooming in on the result"},
              "visual_action": {"type": "Transform", "target": {"id": "result", "type": "MathTex", "content": "1/2", "pos": "RIGHT*2 + DOWN*2"}, "details": "Replace the sum with the simplified result"},
              "duration": 3.0,
              "audio_path": None
            },
            {
              "step": 4,
              "narrative": "Now, let's try subtracting 1/4 from 1/2",
              "signal_action": {"type": "Circumscribe", "target": "frac_3", "color": "YELLOW", "description": "Highlighting the minuend"},
              "visual_action": {"type": "Create", "target": {"id": "frac_3", "type": "MathTex", "content": "1/2", "pos": "RIGHT*2"}, "details": "Show the minuend on a number line"},
              "duration": 2.5,
              "audio_path": None
            },
            {
              "step": 5,
              "narrative": "The difference is 1/4",
              "signal_action": {"type": "Indicate", "target": "result_2", "color": "GREEN", "description": "Pointing to the result"},
              "visual_action": {"type": "Create", "target": {"id": "result_2", "type": "MathTex", "content": "1/4", "pos": "RIGHT*2 + DOWN*1"}, "details": "Show the result on the same number line"},
              "duration": 2.5,
              "audio_path": None
            }
        ]
        
        for step in sequence:
            # Load audio with file existence check
            audio_file = None
            if step.get("audio_path"):
                audio_file = step["audio_path"]
            else:
                mp3_path = f"media/audio/step_{step['step']-1:02d}.mp3"
                if os.path.exists(mp3_path):
                    audio_file = mp3_path
                else:
                    wav_path = f"media/audio/step_{step['step']-1:02d}.wav"
                    if os.path.exists(wav_path):
                        audio_file = wav_path
            
            if audio_file:
                self.add_sound(audio_file)
            
            if step.get("signal_action"):  # signal_action exists
                signal = step["signal_action"]
                signal_type = signal["type"]
                target_id = signal["target"]
                color = signal.get("color", "YELLOW")  # Default to YELLOW
                
                # Find the target object by ID (must already be created)
                if target_id not in objects:
                    # Create the object if it doesn't exist
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
                    
                    obj.shift(eval(position))  # Apply position
                    objects[obj_id] = obj  # Store the object with its ID
                    
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
            obj_id = target["id"]
            obj_type = target["type"]
            content = target["content"]
            position = target["pos"]
            
            if obj_type == "MathTex":
                obj = MathTex(content)
            elif obj_type == "Text":
                obj = Text(content)
            
            obj.shift(eval(position))  # Apply position
            
            if visual["type"] == "Create":
                self.play(Write(obj))
            elif visual["type"] == "Transform":
                src_id = visual.get("source", {}).get("id")
                if src_id:
                    src_obj = objects[src_id]
                    self.play(Transform(src_obj, obj))
                else:
                    self.play(Write(obj))
            
            objects[obj_id] = obj  # Store the object with its ID
            
            # Calculate remaining time after animations
            animation_time = 1  # signal + visual
            remaining = step["duration"] - animation_time
            if remaining > 0:
                self.wait(remaining)