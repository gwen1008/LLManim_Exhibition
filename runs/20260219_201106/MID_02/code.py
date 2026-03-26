from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}  # Registry for all objects

        # Create Layout Engine
        from utils.layout_engine import LayoutEngine, LayoutObject
        layout = LayoutEngine()

        # Create objects from layout_plan
        # Title
        title = Text("Tape Diagram: Ratio of Milk to Water", color=WHITE, font_size=40)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title

        # Tape Bar (Main rectangle)
        tape_bar = Rectangle(width=7.0, height=2.0, color=WHITE, stroke_width=3, fill_opacity=0.0)
        obj_tape_bar = LayoutObject(tape_bar, "tape_bar")
        layout.add(obj_tape_bar)
        layout.add_to_zone(obj_tape_bar, "CONTENT")
        layout.add_constraint(obj_tape_bar.center_x == 0)
        layout.add_constraint(obj_tape_bar.center_y == 0)
        self.objects["tape_bar"] = tape_bar

        # Division Lines (6 lines to create 7 sections)
        # Each section width = 7.0 / 7 = 1.0 unit
        # Line positions: x = -2.5, -1.5, -0.5, 0.5, 1.5, 2.5 (relative to center)
        line_positions = [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
        division_lines = VGroup()
        for i, pos in enumerate(line_positions):
            line = Line(start=UP, end=DOWN, color=WHITE, stroke_width=2)
            line.move_to(tape_bar.get_center() + pos * RIGHT)
            division_lines.add(line)
            self.objects[f"div_line_{i+1}"] = line

        # Milk Fill (leftmost 2 sections, width = 2.0)
        milk_fill = Rectangle(width=2.0, height=2.0, color="#FFFFFF", fill_opacity=0.3, stroke_width=0)
        milk_fill.move_to(tape_bar.get_center() + LEFT * 2.5)
        self.objects["milk_fill"] = milk_fill

        # Water Fill (rightmost 5 sections, width = 5.0)
        water_fill = Rectangle(width=5.0, height=2.0, color="#58ACFA", fill_opacity=0.3, stroke_width=0)
        water_fill.move_to(tape_bar.get_center() + RIGHT * 2.0)
        self.objects["water_fill"] = water_fill

        # Labels
        label_mixture = Text("Mixture", color=YELLOW, font_size=30)
        label_mixture.next_to(tape_bar, UP, buff=0.5)
        self.objects["label_mixture"] = label_mixture

        label_milk = Text("Milk", color=WHITE, font_size=28, weight=BOLD)
        label_milk.move_to(milk_fill.get_center())
        self.objects["label_milk"] = label_milk

        label_water = Text("Water", color="#58ACFA", font_size=28, weight=BOLD)
        label_water.move_to(water_fill.get_center())
        self.objects["label_water"] = label_water

        # Ratio Caption
        ratio_caption = MathTex(
            r"\text{Milk} : \text{Water} = 2 : 5 \quad \text{(Total: 7 parts)}",
            color=GREEN,
            font_size=35
        )
        obj_caption = LayoutObject(ratio_caption, "ratio_caption")
        layout.add(obj_caption)
        layout.add_to_zone(obj_caption, "CONTENT")
        layout.align_to(obj_caption, obj_tape_bar, "BOTTOM", buff=1.0)
        layout.add_constraint(obj_caption.center_x == 0)
        self.objects["ratio_caption"] = ratio_caption

        # Explanation Text
        explanation_text = Text(
            "The tape diagram shows the 2:5 ratio visually. For every 2 parts milk, there are 5 parts water, making 7 equal parts in total.",
            color=LIGHT_GRAY,
            font_size=26
        )
        obj_explanation = LayoutObject(explanation_text, "explanation_text")
        layout.add(obj_explanation)
        layout.add_to_zone(obj_explanation, "FOOTER")
        layout.add_constraint(obj_explanation.center_x == 0)
        self.objects["explanation_text"] = explanation_text

        # Solve layout
        layout.solve()

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We start by drawing a rectangle to represent the entire mixture.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "tape_bar", "details": "Draw the outline of the tape diagram bar."},
                "duration": 4.344,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "This mixture is divided into 7 equal parts.",
                "signal_action": {"type": "Indicate", "target": "tape_bar", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "div_line_1", "details": "Draw the six division lines one after another, from left to right, to create 7 sections."},
                "duration": 3.6,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Two of these parts represent milk.",
                "signal_action": {"type": "Circumscribe", "target": "milk_fill", "color": "YELLOW"},
                "visual_action": {"type": "FadeIn", "target_id": "milk_fill", "details": "Fill the leftmost two sections with a semi-transparent white color."},
                "duration": 2.76,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "The remaining five parts represent water.",
                "signal_action": {"type": "Circumscribe", "target": "water_fill", "color": "YELLOW"},
                "visual_action": {"type": "FadeIn", "target_id": "water_fill", "details": "Fill the rightmost five sections with a semi-transparent blue color."},
                "duration": 3.12,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Let's label the parts: Milk, Water, and the whole Mixture.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_mixture", "details": "Write the labels 'Mixture' above the bar, 'Milk' in the white section, and 'Water' in the blue section."},
                "duration": 4.608,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "This visual model directly represents the ratio: Milk to Water is two to five, for a total of seven parts.",
                "signal_action": {"type": "Indicate", "target": "ratio_caption", "color": "GREEN"},
                "visual_action": {"type": "Write", "target_id": "ratio_caption", "details": "Write the final ratio and total caption below the diagram."},
                "duration": 7.488,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "So, a tape diagram helps us see that a 2:5 ratio means for every 2 parts of one component, there are 5 parts of the other.",
                "signal_action": None,
                "visual_action": {"type": "FadeIn", "target_id": "explanation_text", "details": "Fade in the concluding explanation at the bottom of the screen."},
                "duration": 8.472,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_06.mp3"
            }
        ]

        # Step 0: Show title
        self.play(Write(title))
        self.wait(0.5)

        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_file = step.get("audio_path")
            
            # Add audio if file exists
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # Handle signal action
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                target_obj = self.objects[target_id]
                color_str = signal.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
                color = color_map.get(color_str, YELLOW)
                
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal["type"] == "FocusOn":
                    self.play(FocusOn(target_obj))
            
            # Handle visual action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            target_obj = self.objects[target_id]
            action_type = visual["type"]
            
            if action_type == "Create":
                if target_id == "tape_bar":
                    self.play(Create(target_obj))
                    anim_time = 1.5
                elif target_id == "div_line_1":
                    # Create all division lines sequentially
                    for i in range(6):
                        line = self.objects[f"div_line_{i+1}"]
                        self.play(Create(line), run_time=0.3)
                    anim_time = 1.8
                else:
                    self.play(Create(target_obj))
                    anim_time = 1.0
            elif action_type == "FadeIn":
                self.play(FadeIn(target_obj))
                anim_time = 1.0
            elif action_type == "Write":
                if target_id == "label_mixture":
                    # Write all three labels
                    self.play(Write(self.objects["label_mixture"]))
                    self.play(Write(self.objects["label_milk"]))
                    self.play(Write(self.objects["label_water"]))
                    anim_time = 2.5
                else:
                    self.play(Write(target_obj))
                    anim_time = 1.5
            else:
                anim_time = 1.0
            
            # Wait for remaining audio duration
            remaining = duration - anim_time + 0.5
            if remaining > 0:
                self.wait(remaining)
        
        # Final hold
        self.wait(2)