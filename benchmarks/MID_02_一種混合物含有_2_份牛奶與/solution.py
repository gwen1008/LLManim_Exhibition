from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}
        
        # Define zones manually (based on Past Lessons Learned)
        zones = {
            "HEADER": UP * 3,
            "CONTENT": ORIGIN,
            "FOOTER": DOWN * 3
        }
        
        # --- Create objects from layout_plan.objects ---
        # Title
        title = Text("Tape Diagram: Milk to Water Ratio 2:5", color=WHITE, font_size=36)
        self.objects["title"] = title
        title.move_to(zones["HEADER"])
        
        # Tape outline rectangle
        tape_rect = Rectangle(width=7, height=0.8, color=WHITE, fill_opacity=0.1, stroke_width=2)
        self.objects["tape_rect"] = tape_rect
        tape_rect.move_to(zones["CONTENT"])
        
        # Create 7 sections (individual rectangles)
        sections = []
        section_colors = [BLUE, BLUE, LIGHT_GRAY, LIGHT_GRAY, LIGHT_GRAY, LIGHT_GRAY, LIGHT_GRAY]
        section_fill_opacities = [0.5, 0.5, 0.3, 0.3, 0.3, 0.3, 0.3]
        
        # Position sections according to JSON specification
        # First section at tape_center + LEFT*3
        section1 = Rectangle(width=1, height=0.8,
                            color=section_colors[0],
                            fill_opacity=section_fill_opacities[0],
                            stroke_width=1)
        section1.move_to(tape_rect.get_center() + LEFT * 3)
        sections.append(section1)
        self.objects["section1"] = section1
        
        # Create remaining sections
        for i in range(1, 7):
            sect = Rectangle(width=1, height=0.8,
                            color=section_colors[i],
                            fill_opacity=section_fill_opacities[i],
                            stroke_width=1)
            sect.next_to(sections[i-1], RIGHT, buff=0)
            sections.append(sect)
            self.objects[f"section{i+1}"] = sect
        
        # Group sections for easier positioning
        sections_group = VGroup(*sections)
        self.objects["sections_group"] = sections_group
        
        # Milk label
        milk_label = Text("milk", color=BLUE, font_size=24)
        self.objects["milk_label"] = milk_label
        milk_label.next_to(section1, UP, buff=0.2)
        
        # Water label
        water_label = Text("water", color=GRAY, font_size=24)
        self.objects["water_label"] = water_label
        water_label.next_to(sections[3], UP, buff=0.2)  # section4 is index 3
        
        # X-axis (NumberLine)
        x_axis = NumberLine(x_range=[0, 7, 1], length=7, include_numbers=True, color=WHITE)
        self.objects["x_axis"] = x_axis
        x_axis.next_to(tape_rect, DOWN, buff=0.5)
        
        # Ratio label
        ratio_label = MathTex(r"\text{Ratio} = 2 : 5", color=YELLOW, font_size=32)
        self.objects["ratio_label"] = ratio_label
        
        # Milk fraction
        milk_fraction = MathTex(r"\frac{2}{7} \text{ milk}", color=BLUE, font_size=32)
        self.objects["milk_fraction"] = milk_fraction
        
        # Water fraction
        water_fraction = MathTex(r"\frac{5}{7} \text{ water}", color=GRAY, font_size=32)
        self.objects["water_fraction"] = water_fraction
        
        # Position footer group according to JSON specification
        ratio_label.move_to(zones["FOOTER"] + LEFT * 2)
        milk_fraction.next_to(ratio_label, RIGHT, buff=1.0)
        water_fraction.next_to(milk_fraction, RIGHT, buff=1.0)
        
        # Objects will be added to the scene via animations in Phase 2.
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = self.get_sequence_data()
        
        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_path = step.get("audio_path")
            
            # --- AUDIO (MANDATORY) ---
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)
            # If audio_path doesn't exist, we still proceed (but system should have generated it)
            
            # --- Signal Action ---
            signal_action = step.get("signal_action")
            if signal_action is not None:
                signal_type = signal_action["type"]
                target_id = signal_action["target"]
                color_str = signal_action.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "BLUE": BLUE, "WHITE": WHITE, "RED": RED, "GREEN": GREEN, "GRAY": GRAY, "LIGHT_GRAY": LIGHT_GRAY}
                color = color_map.get(color_str, YELLOW)
                
                target_obj = self.objects.get(target_id)
                if target_obj:
                    if signal_type == "Circumscribe":
                        self.play(Circumscribe(target_obj, color=color, run_time=1))
                    elif signal_type == "Indicate":
                        self.play(Indicate(target_obj, color=color))
                    elif signal_type == "FocusOn":
                        self.play(FocusOn(target_obj))
            
            # --- Visual Action ---
            visual_action = step["visual_action"]
            action_type = visual_action["type"]
            target_id = visual_action["target_id"]
            details = visual_action.get("details", "")
            
            target_obj = self.objects.get(target_id)
            
            if action_type == "Create":
                if target_obj:
                    if target_id == "tape_rect":
                        self.play(Create(target_obj), run_time=2)
                    elif target_id == "section1":
                        # Create all sections sequentially
                        anims = []
                        for i, sect in enumerate(sections):
                            anims.append(Create(sect))
                        self.play(*anims, run_time=3)
                    elif target_id == "x_axis":
                        self.play(Create(target_obj), run_time=2)
                    else:
                        self.play(Create(target_obj))
            elif action_type == "Write":
                if target_obj:
                    if target_id == "milk_label":
                        # Write milk_label and water_label
                        self.play(Write(self.objects["milk_label"]), Write(self.objects["water_label"]), run_time=2)
                    elif target_id == "ratio_label":
                        # Write ratio_label, milk_fraction, water_fraction
                        self.play(Write(self.objects["ratio_label"]),
                                Write(self.objects["milk_fraction"]),
                                Write(self.objects["water_fraction"]),
                                run_time=3)
                    else:
                        self.play(Write(target_obj))
            elif action_type == "Animation":
                if target_id == "section1":
                    # Pulse milk sections blue and water sections gray
                    milk_sects = [sections[0], sections[1]]
                    water_sects = sections[2:]
                    # Highlight milk
                    self.play(*[sect.animate.set_fill(opacity=0.8) for sect in milk_sects], run_time=0.5)
                    self.play(*[sect.animate.set_fill(opacity=0.5) for sect in milk_sects], run_time=0.5)
                    # Highlight water
                    self.play(*[sect.animate.set_fill(opacity=0.6) for sect in water_sects], run_time=0.5)
                    self.play(*[sect.animate.set_fill(opacity=0.3) for sect in water_sects], run_time=0.5)
            
            # --- Wait for remaining duration ---
            # Estimate animation runtime (simplified)
            anim_time = 0
            if signal_action is not None:
                anim_time += 1
            if action_type in ["Create", "Write", "Animation"]:
                if target_id in ["section1", "ratio_label"]:
                    anim_time += 3
                elif target_id in ["milk_label", "x_axis"]:
                    anim_time += 2
                else:
                    anim_time += 1
            
            remaining = duration - anim_time
            if remaining > 0:
                self.wait(remaining)
        
        # Final wait
        self.wait(2)
    
    def get_sequence_data(self):
        """Return the sequence data as defined in the JSON."""
        return [
            {
                "step": 1,
                "narrative": "Let's visualize a mixture with milk and water in a 2:5 ratio using a tape diagram.",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "title",
                    "details": "Fade in the title"
                },
                "duration": 6.12,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水。使用帶有標籤的條型圖（Tape_Diagram）來視覺化_2/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "We start with an empty tape that will be divided into 7 equal sections.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "tape_rect",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "tape_rect",
                    "details": "Draw the outline of the tape diagram"
                },
                "duration": 4.632,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水。使用帶有標籤的條型圖（Tape_Diagram）來視覺化_2/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now we divide the tape into 7 equal sections. The first 2 sections represent milk.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "section1",
                    "color": "BLUE"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "section1",
                    "details": "Draw first milk section, then sequentially create sections 2-7"
                },
                "duration": 6.528,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水。使用帶有標籤的條型圖（Tape_Diagram）來視覺化_2/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "We label the sections: 2 sections for milk and 5 sections for water.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "milk_label",
                    "color": "BLUE"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "milk_label",
                    "details": "Write 'milk' above first two sections, then write 'water' above remaining sections"
                },
                "duration": 5.088,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水。使用帶有標籤的條型圖（Tape_Diagram）來視覺化_2/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Below the tape, we add an x-axis showing the 7 units. This represents the total mixture.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "x_axis",
                    "color": "WHITE"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "x_axis",
                    "details": "Draw the number line with units 0 through 7"
                },
                "duration": 6.864,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水。使用帶有標籤的條型圖（Tape_Diagram）來視覺化_2/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "The ratio of milk to water is 2:5. As fractions of the total, milk is 2/7 and water is 5/7.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "ratio_label",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "ratio_label",
                    "details": "Write the ratio, then write the fractions for milk and water"
                },
                "duration": 8.52,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水。使用帶有標籤的條型圖（Tape_Diagram）來視覺化_2/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "Let's highlight how the 2:5 ratio corresponds to the visual sections in our tape diagram.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "section1",
                    "color": "BLUE"
                },
                "visual_action": {
                    "type": "Animation",
                    "target_id": "section1",
                    "details": "Pulse milk sections blue and water sections gray to emphasize the 2:5 division"
                },
                "duration": 6.072,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水。使用帶有標籤的條型圖（Tape_Diagram）來視覺化_2/step_06.mp3"
            }
        ]