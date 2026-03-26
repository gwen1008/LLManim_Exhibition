'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the ratio 2:5 using a tape diagram to show the relationship between parts (milk and water).
# 2. Layout Strategy:
#    - Header Region: [y=3.0] for Title
#    - Main Content: [Center y=0] for tape diagram and ratio label
#    - Footer Region: [Bottom y=-3.0] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use LayoutEngine zones to keep title, content, and footer separated.
#    - The tape rectangles are positioned side-by-side with no gap (buff=0) at the same baseline (y=0).
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Fade in title.
#    - Step 2: Create milk rectangle.
#    - Step 3: Indicate milk rectangle, write "Milk" label.
#    - Step 4: Indicate milk rectangle, create water rectangle adjacent.
#    - Step 5: Indicate water rectangle, write "Water" label.
#    - Step 6: Circumscribe ratio label, write "2 : 5".
#    - Step 7: Write explanation text.
'''

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
        # Title
        title = Text("Visualizing a 2:5 Ratio", color=WHITE, font_size=48)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title

        # Milk Rectangle
        milk_rect = Rectangle(width=2.0, height=1.0, color="#ADD8E6", fill_opacity=0.7,
                              stroke_color=WHITE, stroke_width=2)
        obj_milk_rect = LayoutObject(milk_rect, "milk_rect")
        layout.add(obj_milk_rect)
        # Position relative to a calculated left edge anchor (x=-2.5, y=0)
        # We'll set its center manually after solving, but first add to CONTENT zone
        layout.add_to_zone(obj_milk_rect, "CONTENT")
        self.objects["milk_rect"] = milk_rect

        # Water Rectangle
        water_rect = Rectangle(width=5.0, height=1.0, color="#87CEEB", fill_opacity=0.7,
                               stroke_color=WHITE, stroke_width=2)
        obj_water_rect = LayoutObject(water_rect, "water_rect")
        layout.add(obj_water_rect)
        layout.add_to_zone(obj_water_rect, "CONTENT")
        self.objects["water_rect"] = water_rect

        # Label Milk
        label_milk = Text("Milk", color="#ADD8E6", font_size=32)
        obj_label_milk = LayoutObject(label_milk, "label_milk")
        layout.add(obj_label_milk)
        layout.add_to_zone(obj_label_milk, "CONTENT")
        # Constraint: label below milk_rect
        layout.add_constraint(obj_label_milk.center_x == obj_milk_rect.center_x)
        layout.add_constraint(obj_label_milk.top == obj_milk_rect.bottom - 0.3)
        self.objects["label_milk"] = label_milk

        # Label Water
        label_water = Text("Water", color="#87CEEB", font_size=32)
        obj_label_water = LayoutObject(label_water, "label_water")
        layout.add(obj_label_water)
        layout.add_to_zone(obj_label_water, "CONTENT")
        # Constraint: label below water_rect
        layout.add_constraint(obj_label_water.center_x == obj_water_rect.center_x)
        layout.add_constraint(obj_label_water.top == obj_water_rect.bottom - 0.3)
        self.objects["label_water"] = label_water

        # Ratio Label
        ratio_label = MathTex("2 : 5", color=YELLOW, font_size=40)
        obj_ratio_label = LayoutObject(ratio_label, "ratio_label")
        layout.add(obj_ratio_label)
        layout.add_to_zone(obj_ratio_label, "CONTENT")
        layout.add_constraint(obj_ratio_label.center_x == 0)
        # Place above the tape diagram (constraint relative to milk_rect top)
        layout.add_constraint(obj_ratio_label.bottom == obj_milk_rect.top - 0.5)
        self.objects["ratio_label"] = ratio_label

        # Explanation
        explanation = Text("For every 2 parts milk, there are 5 parts water.",
                           color=GRAY_B, font_size=32)
        obj_explanation = LayoutObject(explanation, "explanation")
        layout.add(obj_explanation)
        layout.add_to_zone(obj_explanation, "FOOTER")
        layout.add_constraint(obj_explanation.center_x == 0)
        self.objects["explanation"] = explanation

        # Additional constraint: milk_rect and water_rect aligned at bottom (y=0) and adjacent
        layout.add_constraint(obj_milk_rect.bottom == 0)
        layout.add_constraint(obj_water_rect.bottom == 0)
        # Adjacent: water_rect left edge equals milk_rect right edge (no gap)
        layout.add_constraint(obj_water_rect.left == obj_milk_rect.right)

        # Solve all constraints
        layout.solve()

        # Apply solved positions to mobjects (LayoutEngine already updates them)
        # No need for extra moves; layout.solve() sets the mobject positions.

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's visualize the ratio of milk to water, which is two to five.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "title", "details": "Fade in the title at the top of the screen."},
                "duration": 4.8,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "We start with the amount of milk: two parts.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "milk_rect", "details": "Draw the blue rectangle with a width of 2 units."},
                "duration": 3.48,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "We label this section 'Milk'.",
                "signal_action": {"type": "Indicate", "target": "milk_rect", "color": "YELLOW"},
                "visual_action": {"type": "Write", "target_id": "label_milk", "details": "Write the 'Milk' label below the rectangle."},
                "duration": 2.472,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "Next, we add the water: five parts, placed right next to the milk.",
                "signal_action": {"type": "Indicate", "target": "milk_rect", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "water_rect", "details": "Draw the light blue rectangle adjacent to the milk rectangle, with a width of 5 units."},
                "duration": 5.352,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "We label this section 'Water'.",
                "signal_action": {"type": "Indicate", "target": "water_rect", "color": "YELLOW"},
                "visual_action": {"type": "Write", "target_id": "label_water", "details": "Write the 'Water' label below the rectangle."},
                "duration": 2.472,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "Together, they form a tape diagram. The ratio of their lengths is two to five.",
                "signal_action": {"type": "Circumscribe", "target": "ratio_label", "color": "YELLOW"},
                "visual_action": {"type": "Write", "target_id": "ratio_label", "details": "Write the ratio label '2 : 5' above the diagram."},
                "duration": 6.12,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "This visual means: for every two parts milk, there are five parts water.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "explanation", "details": "Write the explanatory text at the bottom of the screen."},
                "duration": 5.328,
                "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_06.mp3"
            }
        ]

        for step in sequence:
            # === AUDIO (MANDATORY) ===
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)

            # Signal Action
            signal = step.get("signal_action")
            if signal is not None:
                target_obj = self.objects[signal["target"]]
                color = YELLOW if signal.get("color") == "YELLOW" else eval(signal["color"])
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))

            # Visual Action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            obj = self.objects[target_id]
            action_type = visual["type"]

            if action_type == "Create":
                self.play(Create(obj))
            elif action_type == "Write":
                self.play(Write(obj))
            # Note: No FadeIn used in this sequence per JSON.

            # Wait for remaining audio duration
            animation_time = 1.0 if signal else 0  # signal run_time approx 1s
            if action_type == "Create":
                animation_time += 1.0
            elif action_type == "Write":
                animation_time += 1.0
            remaining = step["duration"] - animation_time + 0.5
            if remaining > 0:
                self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 2))