'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing translation as movement on a number line and extracting the distance as a separate magnitude.
# 2. Layout Strategy: Use LayoutEngine for zones.
#    - Header Region: Title at y ~ 3.5.
#    - Main Content: Number line and points centered at y=0.
#    - Footer Region: Explanation text at y ~ -3.5.
# 3. Anti-Overlap Check: Use zones to keep title, content, and footer separate. Points and labels are positioned relative to the number line.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step? Yes, using provided audio_path.
#    - [x] Files: "media/audio/{topic_safe_name}/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create number line.
#    - Step 2: Create point A (-2) and label, with signal.
#    - Step 3: Create point B (3) and label, with signal.
#    - Step 4: Animate point A moving to B, leaving a ghost, with signal.
#    - Step 5: Grow arrow from A to B, with signal.
#    - Step 6: Write arrow label, with signal.
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

        # Create objects from layout_plan
        # Title
        title = Text("Translation and Distance on a Number Line", color=WHITE, font_size=36)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title

        # Number Line
        number_line = NumberLine(
            x_range=[-5.5, 5.5, 1],
            length=11,
            include_numbers=True,
            include_tip=True,
            color=LIGHT_GRAY
        )
        obj_number_line = LayoutObject(number_line, "number_line")
        layout.add(obj_number_line)
        layout.add_to_zone(obj_number_line, "CONTENT")
        layout.add_constraint(obj_number_line.center_x == 0)
        layout.add_constraint(obj_number_line.center_y == 0)
        self.objects["number_line"] = number_line

        # Point A and its label
        point_a = Dot(radius=0.08, color=BLUE)
        point_a.move_to(number_line.n2p(-2))
        label_a = MathTex("-2", color=BLUE, font_size=24)
        label_a.next_to(point_a, DOWN, buff=0.2)
        self.objects["point_a"] = point_a
        self.objects["label_a"] = label_a

        # Point B and its label
        point_b = Dot(radius=0.08, color=GREEN)
        point_b.move_to(number_line.n2p(3))
        label_b = MathTex("3", color=GREEN, font_size=24)
        label_b.next_to(point_b, DOWN, buff=0.2)
        self.objects["point_b"] = point_b
        self.objects["label_b"] = label_b

        # Arrow for distance (initially zero length at start point)
        arrow_start = number_line.n2p(-2)
        arrow_distance = Arrow(
            start=arrow_start,
            end=arrow_start,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["arrow_distance"] = arrow_distance

        # Arrow label
        arrow_label = MathTex("5\\ \\text{units}", color=YELLOW, font_size=28)
        # Position will be set relative to arrow after it's grown
        self.objects["arrow_label"] = arrow_label

        # Explanation text (initial content)
        explanation_text = Text("We start with a number line and two points.", color=LIGHT_GRAY, font_size=24)
        obj_explanation = LayoutObject(explanation_text, "explanation")
        layout.add(obj_explanation)
        layout.add_to_zone(obj_explanation, "FOOTER")
        layout.add_constraint(obj_explanation.center_x == 0)
        self.objects["explanation_text"] = explanation_text

        # Solve layout to position title, number_line, and explanation_text
        layout.solve()

        # Update explanation text content for each step (we'll create new Text objects and replace)
        # We'll store the current explanation mobject
        current_explanation = explanation_text

        # Ghost point for step 4 (faint copy of point A)
        ghost_point = Dot(radius=0.08, color=BLUE).set_opacity(0.3)
        ghost_point.move_to(number_line.n2p(-2))
        self.objects["ghost_point"] = ghost_point

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's create a number line from negative five to five.",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "number_line",
                    "details": "Draw the number line with ticks and labels."
                },
                "duration": 3.84,
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Now, plot a point at negative two, and another point at three.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "label_a",
                    "color": "BLUE"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "point_a",
                    "details": "Fade in the blue dot at -2 and its label."
                },
                "duration": 4.68,
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "And the point at positive three.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "label_b",
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "point_b",
                    "details": "Fade in the green dot at 3 and its label."
                },
                "duration": 2.472,
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "A translation moves the point from negative two to positive three. Watch it go.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "point_a",
                    "color": "BLUE"
                },
                "visual_action": {
                    "type": "Transform",
                    "target_id": "point_a",
                    "details": "Animate the blue dot moving along the number line from position -2 to position 3. Leave a faint copy or trace at the start."
                },
                "duration": 6.12,
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "The distance of this translation is five units. We can represent it with an arrow.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "arrow_distance",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "GrowArrow",
                    "target_id": "arrow_distance",
                    "details": "Animate the yellow arrow stretching from the start point (-2) to the end point (3). Update its geometry_def end point to number_line.n2p(3) during this animation."
                },
                "duration": 6.024,
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "And we label it: five units.",
                "signal_action": {
                    "type": "Write",
                    "target": "arrow_label",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "arrow_label",
                    "details": "Write the label '5 units' above the arrow."
                },
                "duration": 2.808,
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_05.mp3"
            }
        ]

        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_path = step.get("audio_path")

            # === AUDIO (MANDATORY) ===
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)

            # Update explanation text
            new_explanation_text = Text(step["narrative"], color=LIGHT_GRAY, font_size=24)
            new_explanation_text.move_to(current_explanation.get_center())
            if step_num > 1:
                self.play(ReplacementTransform(current_explanation, new_explanation_text))
            else:
                # For first step, explanation is already added by layout, just write it
                self.play(Write(new_explanation_text))
            current_explanation = new_explanation_text

            # Handle signal_action
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                target_obj = self.objects.get(target_id)
                color_str = signal.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "BLUE": BLUE, "GREEN": GREEN, "RED": RED}
                color = color_map.get(color_str, YELLOW)

                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal["type"] == "Write":
                    # For step 6, signal is Write on arrow_label, but visual_action also writes it.
                    # We'll handle the write in visual_action, so ignore signal write here.
                    pass

            # Handle visual_action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            action_type = visual["type"]

            if action_type == "Create":
                obj = self.objects[target_id]
                if target_id == "number_line":
                    self.play(Create(obj))
                elif target_id == "point_a":
                    # Create point_a and its label together
                    self.play(FadeIn(obj), Write(self.objects["label_a"]))
                elif target_id == "point_b":
                    self.play(FadeIn(obj), Write(self.objects["label_b"]))
            elif action_type == "Transform" and target_id == "point_a":
                # Move point_a from -2 to 3, leave ghost
                self.add(ghost_point)
                self.play(
                    point_a.animate.move_to(number_line.n2p(3)),
                    run_time=2
                )
            elif action_type == "GrowArrow" and target_id == "arrow_distance":
                # Grow arrow from start to end
                arrow = self.objects["arrow_distance"]
                arrow_end = number_line.n2p(3)
                # Create a new arrow with the correct end point for the animation
                arrow_full = Arrow(
                    start=number_line.n2p(-2),
                    end=arrow_end,
                    color=YELLOW,
                    stroke_width=6,
                    max_tip_length_to_length_ratio=0.15
                )
                self.play(GrowArrow(arrow_full))
                # Replace the zero-length arrow with the full one
                self.remove(arrow)
                self.add(arrow_full)
                self.objects["arrow_distance"] = arrow_full
                # Position the label
                arrow_label.next_to(arrow_full, UP, buff=0.1)
            elif action_type == "Write" and target_id == "arrow_label":
                self.play(Write(self.objects["arrow_label"]))

            # Calculate remaining wait time
            # Approximate animation times: Create/Write ~1s, Transform ~2s, GrowArrow ~2s
            # We'll use a simple heuristic: if action_type is Transform or GrowArrow, assume 2s, else 1s.
            if action_type in ["Transform", "GrowArrow"]:
                anim_time = 2.0
            else:
                anim_time = 1.0
            # Add signal animation time if present
            if signal is not None and signal["type"] != "Write":
                anim_time += 1.0
            remaining = duration - anim_time + 0.5  # Safety buffer
            if remaining > 0:
                self.wait(remaining)

        # Final wait
        self.wait(2)