'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the ratio 2:5 using a tape diagram, showing the whole, equal partitions, colored groups, and labels.
# 2. Layout Strategy: Use High-Low Split.
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for tape diagram
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroup for partition lines. Position labels relative to diagram.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show tape outline.
#    - Step 2: Indicate outline, draw partition lines.
#    - Step 3: Circumscribe milk fill, fade it in.
#    - Step 4: Circumscribe water fill, fade it in.
#    - Step 5: Indicate labels, write all labels and explanation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors
        title_anchor = 3.5 * UP
        diagram_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Tape Diagram: Ratio of Milk to Water", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Tape outline (Polygon)
        tape_vertices = [
            (-3.5, -0.5, 0),
            (3.5, -0.5, 0),
            (3.5, 0.5, 0),
            (-3.5, 0.5, 0)
        ]
        tape_outline = Polygon(*tape_vertices, color=WHITE, stroke_width=3, fill_opacity=0.0)
        tape_outline.move_to(diagram_anchor)
        self.objects["tape_outline"] = tape_outline

        # Partition lines (6 lines)
        # Positions relative to diagram_anchor
        line_positions = [
            diagram_anchor + 2.5 * LEFT,
            diagram_anchor + 1.5 * LEFT,
            diagram_anchor + 0.5 * LEFT,
            diagram_anchor + 0.5 * RIGHT,
            diagram_anchor + 1.5 * RIGHT,
            diagram_anchor + 2.5 * RIGHT
        ]
        partition_lines = VGroup()
        for i, pos in enumerate(line_positions):
            line = Line(0.5 * UP, 0.5 * DOWN, color=WHITE, stroke_width=2)
            line.move_to(pos)
            partition_lines.add(line)
            self.objects[f"partition_line_{i+1}"] = line

        # Milk fill (Polygon)
        milk_vertices = [
            (-3.5, -0.5, 0),
            (-0.5, -0.5, 0),
            (-0.5, 0.5, 0),
            (-3.5, 0.5, 0)
        ]
        milk_fill = Polygon(*milk_vertices, color="#1E88E5", fill_opacity=0.7, stroke_width=0)
        milk_fill.move_to(diagram_anchor)
        self.objects["milk_fill"] = milk_fill

        # Water fill (Polygon)
        water_vertices = [
            (-0.5, -0.5, 0),
            (3.5, -0.5, 0),
            (3.5, 0.5, 0),
            (-0.5, 0.5, 0)
        ]
        water_fill = Polygon(*water_vertices, color="#80DEEA", fill_opacity=0.5, stroke_width=0)
        water_fill.move_to(diagram_anchor)
        self.objects["water_fill"] = water_fill

        # Labels
        label_milk = Text("Milk (2 parts)", color="#1E88E5", font_size=28)
        # Position: next_to tape_outline UP, buff=0.6, align left edge to milk_fill left, shift right 1.5 units
        label_milk.next_to(tape_outline, UP, buff=0.6)
        label_milk.align_to(milk_fill, LEFT)
        label_milk.shift(1.5 * RIGHT)
        self.objects["label_milk"] = label_milk

        label_water = Text("Water (5 parts)", color="#80DEEA", font_size=28)
        label_water.next_to(tape_outline, UP, buff=0.6)
        label_water.align_to(water_fill, LEFT)
        label_water.shift(2.5 * RIGHT)
        self.objects["label_water"] = label_water

        label_ratio = MathTex(r"\text{Ratio} = 2 : 5", color=YELLOW, font_size=36)
        label_ratio.next_to(tape_outline, DOWN, buff=0.8)
        self.objects["label_ratio"] = label_ratio

        explanation_text = Text("For every 2 parts milk, there are 5 parts water.", color=GRAY_B, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        step = {
            "step": 1,
            "duration": 7.296,
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_00.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(title))
        self.play(Create(tape_outline))
        animation_time = 2.0  # Write title + Create tape
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 2
        step = {
            "step": 2,
            "signal_action": {"type": "Indicate", "target": "tape_outline", "color": "YELLOW"},
            "duration": 9.216,
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_01.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action"):
            self.play(Indicate(tape_outline, color=YELLOW))
        # Create all partition lines at once (simultaneously)
        self.play(Create(partition_lines))
        animation_time = 1.0 + 2.0  # Indicate + Create lines
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 3
        step = {
            "step": 3,
            "signal_action": {"type": "Circumscribe", "target": "milk_fill", "color": "YELLOW"},
            "duration": 3.024,
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_02.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action"):
            self.play(Circumscribe(milk_fill, color=YELLOW, run_time=1))
        self.play(FadeIn(milk_fill))
        animation_time = 1.0 + 1.0  # Circumscribe + FadeIn
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 4
        step = {
            "step": 4,
            "signal_action": {"type": "Circumscribe", "target": "water_fill", "color": "YELLOW"},
            "duration": 3.12,
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_03.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action"):
            self.play(Circumscribe(water_fill, color=YELLOW, run_time=1))
        self.play(FadeIn(water_fill))
        animation_time = 1.0 + 1.0  # Circumscribe + FadeIn
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 5
        step = {
            "step": 5,
            "signal_action": [
                {"type": "Indicate", "target": "label_milk", "color": "YELLOW"},
                {"type": "Indicate", "target": "label_water", "color": "YELLOW"}
            ],
            "duration": 9.144,
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_04.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action"):
            signal_list = step["signal_action"]
            for signal in signal_list:
                target_obj = self.objects[signal["target"]]
                self.play(Indicate(target_obj, color=YELLOW))
        # Write labels in sequence
        self.play(Write(label_milk))
        self.play(Write(label_water))
        self.play(Write(label_ratio))
        self.play(Write(explanation_text))
        animation_time = 2.0 + 4.0  # 2 Indicate + 4 Write
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 2))