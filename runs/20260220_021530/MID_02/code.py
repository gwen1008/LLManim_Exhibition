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
        # 1. Title
        title = Text("Tape Diagram: Ratio of Milk to Water", color=WHITE, font_size=36)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title
        
        # 2. Tape Outline
        tape_outline = Rectangle(width=7.0, height=1.0, color=WHITE, fill_opacity=0.0, stroke_width=3)
        obj_tape_outline = LayoutObject(tape_outline, "tape_outline")
        layout.add(obj_tape_outline)
        layout.add_to_zone(obj_tape_outline, "CONTENT")
        layout.add_constraint(obj_tape_outline.center_x == 0)
        layout.add_constraint(obj_tape_outline.center_y == 0)
        self.objects["tape_outline"] = tape_outline
        
        # 3. Milk Blocks VGroup (2 rectangles)
        milk_block1 = Rectangle(width=1.0, height=1.0, color="#66B3FF", fill_opacity=0.8)
        milk_block2 = Rectangle(width=1.0, height=1.0, color="#66B3FF", fill_opacity=0.8)
        milk_blocks_vgroup = VGroup(milk_block1, milk_block2)
        # Position will be set relative to tape_outline after layout.solve()
        obj_milk_blocks = LayoutObject(milk_blocks_vgroup, "milk_blocks_vgroup")
        layout.add(obj_milk_blocks)
        # Align left edge to tape outline's left edge, and vertically center
        layout.align_to(obj_milk_blocks, obj_tape_outline, 'LEFT')
        layout.align_to(obj_milk_blocks, obj_tape_outline, 'CENTER_Y')
        self.objects["milk_blocks_vgroup"] = milk_blocks_vgroup
        
        # 4. Water Blocks VGroup (5 rectangles)
        water_rects = []
        for _ in range(5):
            water_rects.append(Rectangle(width=1.0, height=1.0, color="#CCE5FF", fill_opacity=0.8))
        water_blocks_vgroup = VGroup(*water_rects)
        obj_water_blocks = LayoutObject(water_blocks_vgroup, "water_blocks_vgroup")
        layout.add(obj_water_blocks)
        # Position to the right of milk blocks, aligned vertically
        layout.align_to(obj_water_blocks, obj_milk_blocks, 'RIGHT')
        layout.align_to(obj_water_blocks, obj_tape_outline, 'CENTER_Y')
        self.objects["water_blocks_vgroup"] = water_blocks_vgroup
        
        # 5. Label Milk
        label_milk = Text("Milk (2 parts)", color="#66B3FF", font_size=28)
        obj_label_milk = LayoutObject(label_milk, "label_milk")
        layout.add(obj_label_milk)
        # Position above milk blocks
        layout.align_to(obj_label_milk, obj_milk_blocks, 'TOP', buff=0.5)
        layout.align_to(obj_label_milk, obj_milk_blocks, 'CENTER_X')
        self.objects["label_milk"] = label_milk
        
        # 6. Label Water
        label_water = Text("Water (5 parts)", color="#CCE5FF", font_size=28)
        obj_label_water = LayoutObject(label_water, "label_water")
        layout.add(obj_label_water)
        # Position above water blocks
        layout.align_to(obj_label_water, obj_water_blocks, 'TOP', buff=0.5)
        layout.align_to(obj_label_water, obj_water_blocks, 'CENTER_X')
        self.objects["label_water"] = label_water
        
        # 7. Brace Total
        brace_total = Brace(tape_outline, direction=DOWN, color=YELLOW)
        obj_brace_total = LayoutObject(brace_total, "brace_total")
        layout.add(obj_brace_total)
        # Position below tape outline
        layout.align_to(obj_brace_total, obj_tape_outline, 'BOTTOM', buff=0.2)
        layout.align_to(obj_brace_total, obj_tape_outline, 'CENTER_X')
        self.objects["brace_total"] = brace_total
        
        # 8. Label Total
        label_total = MathTex(r"7\text{ total parts}", color=YELLOW, font_size=32)
        obj_label_total = LayoutObject(label_total, "label_total")
        layout.add(obj_label_total)
        # Position below brace
        layout.align_to(obj_label_total, obj_brace_total, 'BOTTOM', buff=0.2)
        layout.align_to(obj_label_total, obj_brace_total, 'CENTER_X')
        self.objects["label_total"] = label_total
        
        # 9. Ratio Equation
        ratio_eq = MathTex(r"\text{Milk} : \text{Water} = 2 : 5", color=WHITE, font_size=36)
        obj_ratio_eq = LayoutObject(ratio_eq, "ratio_eq")
        layout.add(obj_ratio_eq)
        layout.add_to_zone(obj_ratio_eq, "FOOTER")
        # Position in footer, slightly above center of footer zone
        layout.add_constraint(obj_ratio_eq.center_x == 0)
        self.objects["ratio_eq"] = ratio_eq
        
        # 10. Fraction Equation
        fraction_eq = MathTex(r"\frac{2}{7}\text{ milk}, \quad \frac{5}{7}\text{ water}", color=WHITE, font_size=32)
        obj_fraction_eq = LayoutObject(fraction_eq, "fraction_eq")
        layout.add(obj_fraction_eq)
        layout.add_to_zone(obj_fraction_eq, "FOOTER")
        # Position below ratio equation
        layout.align_to(obj_fraction_eq, obj_ratio_eq, 'BOTTOM', buff=0.5)
        layout.align_to(obj_fraction_eq, obj_ratio_eq, 'CENTER_X')
        self.objects["fraction_eq"] = fraction_eq
        
        # Solve all layout constraints
        layout.solve()
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's visualize a mixture with a ratio of two parts milk to five parts water. We'll use a tape diagram.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "title", "details": "Fade in the title."},
                "duration": 7.536,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "The whole mixture has seven total parts. We start with an empty tape representing these seven parts.",
                "signal_action": {"type": "Indicate", "target": "tape_outline", "color": "WHITE"},
                "visual_action": {"type": "Create", "target_id": "tape_outline", "details": "Draw the rectangle outline."},
                "duration": 6.936,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, we fill the first two parts with milk.",
                "signal_action": {"type": "Indicate", "target": "milk_blocks_vgroup", "color": "#66B3FF"},
                "visual_action": {"type": "Transform", "target_id": "milk_blocks_vgroup", "details": "Animate the two blue rectangles appearing within the left side of the tape outline. Use TransformFromCopy or a matching Create animation."},
                "duration": 3.384,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "The remaining five parts are water.",
                "signal_action": {"type": "Indicate", "target": "water_blocks_vgroup", "color": "#CCE5FF"},
                "visual_action": {"type": "Transform", "target_id": "water_blocks_vgroup", "details": "Animate the five light blue rectangles appearing, filling the rest of the tape."},
                "duration": 2.76,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Let's label the sections: two parts milk, and five parts water. The ratio is two to five.",
                "signal_action": {"type": "Circumscribe", "target": "label_milk", "color": "YELLOW"},
                "visual_action": {"type": "Write", "target_id": "label_milk", "details": "Write the milk label above its section."},
                "duration": 7.32,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "",
                "signal_action": {"type": "Circumscribe", "target": "label_water", "color": "YELLOW"},
                "visual_action": {"type": "Write", "target_id": "label_water", "details": "Write the water label above its section."},
                "duration": 2.0
            },
            {
                "step": 7,
                "narrative": "The entire tape shows the total of seven parts.",
                "signal_action": {"type": "Indicate", "target": "brace_total", "color": "YELLOW"},
                "visual_action": {"type": "GrowFromCenter", "target_id": "brace_total", "details": "Animate the brace growing beneath the tape."},
                "duration": 3.504,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_total", "details": "Write the '7 total parts' label."},
                "duration": 2.0
            },
            {
                "step": 9,
                "narrative": "We can express this as a ratio, and also as fractions of the whole.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "ratio_eq", "details": "Write the ratio equation in the explanation area."},
                "duration": 4.608,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_08.mp3"
            },
            {
                "step": 10,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "fraction_eq", "details": "Write the fraction equation below the ratio."},
                "duration": 2.0
            }
        ]
        
        # Process each step
        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            
            # === AUDIO (MANDATORY) ===
            audio_file = None
            if "audio_path" in step and step["audio_path"]:
                audio_file = step["audio_path"]
            else:
                # Fallback construction (not needed here as all steps have audio_path)
                file_index = step_num - 1
                mp3_path = f"media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_{file_index:02d}.mp3"
                if os.path.exists(mp3_path):
                    audio_file = mp3_path
                else:
                    wav_path = f"media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_{file_index:02d}.wav"
                    audio_file = wav_path if os.path.exists(wav_path) else None
            
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # Signal Action
            signal_animation_time = 0
            if step.get("signal_action") is not None:
                signal = step["signal_action"]
                signal_type = signal["type"]
                target_id = signal["target"]
                color_str = signal.get("color", "YELLOW")
                
                # Map color string to Manim constant
                color_map = {
                    "YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE,
                    "WHITE": WHITE, "#66B3FF": "#66B3FF", "#CCE5FF": "#CCE5FF"
                }
                color = color_map.get(color_str, YELLOW)
                
                target_obj = self.objects.get(target_id)
                if target_obj:
                    if signal_type == "Circumscribe":
                        self.play(Circumscribe(target_obj, color=color, run_time=1))
                        signal_animation_time += 1
                    elif signal_type == "Indicate":
                        self.play(Indicate(target_obj, color=color))
                        signal_animation_time += 1
                    elif signal_type == "FocusOn":
                        self.play(FocusOn(target_obj))
                        signal_animation_time += 1
            
            # Visual Action
            visual = step["visual_action"]
            action_type = visual["type"]
            target_id = visual["target_id"]
            target_obj = self.objects.get(target_id)
            
            visual_animation_time = 0
            if target_obj:
                if action_type == "Create":
                    self.play(Create(target_obj))
                    visual_animation_time += 1
                elif action_type == "Write":
                    self.play(Write(target_obj))
                    visual_animation_time += 1
                elif action_type == "Transform":
                    # For milk and water blocks, we'll create them as if appearing from the outline
                    # Since they are already positioned, we can use FadeIn
                    self.play(FadeIn(target_obj))
                    visual_animation_time += 1
                elif action_type == "GrowFromCenter":
                    self.play(GrowFromCenter(target_obj))
                    visual_animation_time += 1
            
            # Wait for remaining duration
            total_animation_time = signal_animation_time + visual_animation_time
            remaining = duration - total_animation_time + 0.5  # 0.5s safety buffer
            if remaining > 0:
                self.wait(remaining)