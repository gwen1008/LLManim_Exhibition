'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing translation on a number line as a vector and calculating its distance as the absolute difference of coordinates.
# 2. Layout Strategy: Use LayoutEngine for High-Low Split.
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line and points
#    - Footer Region: [Bottom y=-3.5] for explanation text and distance formula
# 3. Anti-Overlap Check: Use LayoutEngine zones to keep title, content, and footer separated. Anchor main content to center.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create number line.
#    - Step 2: Create point A (-2) and label.
#    - Step 3: Create point B (3) and label.
#    - Step 4: Create zero-length arrow at A.
#    - Step 5: Transform zero arrow into full arrow from A to B.
#    - Step 6: Write distance formula in footer.
'''

from manim import *
import os
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        layout = LayoutEngine()

        # Create objects from layout_plan
        # Title
        title = Text("Translation on a Number Line", color=WHITE, font_size=40)
        self.objects["title"] = title
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)

        # Number Line
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=8,
            include_numbers=True,
            color=LIGHT_GRAY
        )
        self.objects["number_line"] = number_line
        obj_number_line = LayoutObject(number_line, "number_line")
        layout.add(obj_number_line)
        layout.add_to_zone(obj_number_line, "CONTENT")
        layout.add_constraint(obj_number_line.center_x == 0)
        layout.add_constraint(obj_number_line.center_y == 0)

        # Point A and Label
        point_A = Dot(radius=0.08, color=BLUE)
        point_A.move_to(number_line.n2p(-2))
        self.objects["point_A"] = point_A
        label_A = MathTex("-2", color=BLUE, font_size=30)
        label_A.next_to(point_A, DOWN, buff=0.2)
        self.objects["label_A"] = label_A

        # Point B and Label
        point_B = Dot(radius=0.08, color=GREEN)
        point_B.move_to(number_line.n2p(3))
        self.objects["point_B"] = point_B
        label_B = MathTex("3", color=GREEN, font_size=30)
        label_B.next_to(point_B, DOWN, buff=0.2)
        self.objects["label_B"] = label_B

        # Arrows
        arrow_zero = Arrow(
            start=number_line.n2p(-2),
            end=number_line.n2p(-2),
            color=YELLOW,
            stroke_width=6,
            buff=0
        )
        self.objects["arrow_zero"] = arrow_zero

        arrow_full = Arrow(
            start=number_line.n2p(-2),
            end=number_line.n2p(3),
            color=YELLOW,
            stroke_width=6,
            buff=0
        )
        self.objects["arrow_full"] = arrow_full

        # Explanation Text and Distance Formula
        explanation_text = Text("Distance of translation:", color=LIGHT_GRAY, font_size=28)
        self.objects["explanation_text"] = explanation_text
        obj_explanation = LayoutObject(explanation_text, "explanation_text")
        layout.add(obj_explanation)
        layout.add_to_zone(obj_explanation, "FOOTER")
        layout.add_constraint(obj_explanation.center_x == -2)

        distance_eq = MathTex("|3 - (-2)| = 5", color=YELLOW, font_size=36)
        self.objects["distance_eq"] = distance_eq
        obj_distance = LayoutObject(distance_eq, "distance_eq")
        layout.add(obj_distance)
        layout.add_to_zone(obj_distance, "FOOTER")
        layout.align_to(obj_distance, obj_explanation, "RIGHT", buff=0.5)

        # Solve layout
        layout.solve()

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's start with a number line from negative five to five.",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "number_line",
                    "details": "Draw the number line with ticks and labels"
                },
                "duration": 3.984,
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "We plot a point at negative two, and another point at three.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "point_A",
                    "color": "BLUE"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "point_A",
                    "details": "Fade in the blue dot and its label at -2"
                },
                "duration": 4.32,
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, let's animate a translation, moving the point from negative two to three.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "point_B",
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "point_B",
                    "details": "Fade in the green dot and its label at 3"
                },
                "duration": 5.4,
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "The translation can be represented by a vector. We show this as an arrow starting at the original point.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "point_A",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "arrow_zero",
                    "details": "Show a zero-length arrow (just a dot) at point A"
                },
                "duration": 7.104,
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "The arrow scales to connect the start and end points, showing the full translation. Its length is the distance traveled.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "arrow_full",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Transform",
                    "target_id": "arrow_zero",
                    "details": "Morph the zero-length arrow into the full-length arrow from -2 to 3. Use target=arrow_full."
                },
                "duration": 7.92,
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "This distance is calculated as the absolute difference of the coordinates: three minus negative two equals five.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "distance_eq",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "distance_eq",
                    "details": "Write the distance formula in the footer area"
                },
                "duration": 7.248,
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_05.mp3"
            }
        ]

        # Initial add of title (it will be shown later)
        self.add(title)

        for step in sequence:
            # === AUDIO ===
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)

            # Signal Action
            signal = step.get("signal_action")
            if signal is not None:
                target_obj = self.objects[signal["target"]]
                color = eval(signal["color"]) if signal.get("color") else YELLOW
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal["type"] == "FocusOn":
                    self.play(FocusOn(target_obj))

            # Visual Action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            obj = self.objects[target_id]

            if visual["type"] == "Create":
                if target_id == "point_A":
                    self.play(Create(obj), Write(self.objects["label_A"]))
                elif target_id == "point_B":
                    self.play(Create(obj), Write(self.objects["label_B"]))
                else:
                    self.play(Create(obj))
            elif visual["type"] == "Write":
                self.play(Write(obj))
            elif visual["type"] == "Transform":
                # Transform arrow_zero into arrow_full
                self.play(Transform(self.objects["arrow_zero"], self.objects["arrow_full"]))

            # Wait for remaining duration
            animation_time = 1.0 if signal else 0.0
            if visual["type"] in ["Create", "Write"]:
                animation_time += 1.0
            elif visual["type"] == "Transform":
                animation_time += 1.5

            remaining = step["duration"] - animation_time + 0.5
            if remaining > 0:
                self.wait(remaining)