from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Translation on a Number Line", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Number Line
        # Note: LIGHT_GRAY is not a valid constant, using GRAY_B as replacement
        number_line = NumberLine(x_range=[-5, 5, 1], length=10, include_numbers=True, color=GRAY_B)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # Point A and its label
        point_a = Dot(radius=0.08, color=BLUE)
        point_a.move_to(number_line.n2p(-2))
        self.objects["point_a"] = point_a

        label_a = MathTex("-2", color=BLUE, font_size=30)
        label_a.next_to(point_a, UP, buff=0.2)
        self.objects["label_a"] = label_a

        # Point B and its label
        point_b = Dot(radius=0.08, color=GREEN)
        point_b.move_to(number_line.n2p(3))
        self.objects["point_b"] = point_b

        label_b = MathTex("3", color=GREEN, font_size=30)
        label_b.next_to(point_b, UP, buff=0.2)
        self.objects["label_b"] = label_b

        # Arrows (initial positions based on points, but points might move, so set later)
        # arrow_zero: start and end at point_a's initial center
        arrow_zero_start = number_line.n2p(-2)
        arrow_zero = Arrow(start=arrow_zero_start, end=arrow_zero_start, color=YELLOW, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        self.objects["arrow_zero"] = arrow_zero

        # arrow_full: from point_a's initial center to point_b's center
        arrow_full_start = number_line.n2p(-2)
        arrow_full_end = number_line.n2p(3)
        arrow_full = Arrow(start=arrow_full_start, end=arrow_full_end, color=YELLOW, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        self.objects["arrow_full"] = arrow_full

        # Distance label
        distance_label = MathTex("5 \\text{ units}", color=YELLOW, font_size=30)
        # Position will be set relative to arrow_full after it's created/transformed
        self.objects["distance_label"] = distance_label

        # Explanation text (initial content from layout_plan)
        explanation_text = Text("Step 1: The number line from -5 to 5.", color=GRAY_B, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        step = {
            "step": 1,
            "duration": 4.968,
            "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_00.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["title"]))
        self.play(Create(self.objects["number_line"]))
        # Update explanation text for step 1 (already created with correct content)
        self.play(Write(self.objects["explanation_text"]))
        animation_time = 2.0  # Estimate for Write(title) + Create(number_line) + Write(explanation)
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        step = {
            "step": 2,
            "signal_action": {"type": "Indicate", "target": "point_a", "color": "YELLOW"},
            "duration": 6.024,
            "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_01.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal.get("color") == "YELLOW" else eval(signal.get("color"))
            self.play(Indicate(target_obj, color=color))
        # Visual action: Create point_a, label_a, point_b, label_b
        self.play(Create(self.objects["point_a"]), Write(self.objects["label_a"]))
        self.play(Create(self.objects["point_b"]), Write(self.objects["label_b"]))
        # Update explanation text
        new_explanation = Text("Step 2: Plot points at -2 (blue) and 3 (green).", color=GRAY_B, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        animation_time = 4.0  # Estimate for Indicate + 4 creations + ReplacementTransform
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        step = {
            "step": 3,
            "signal_action": {"type": "Indicate", "target": "point_a", "color": "BLUE"},
            "duration": 8.184,
            "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_02.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = BLUE if signal.get("color") == "BLUE" else eval(signal.get("color"))
            self.play(Indicate(target_obj, color=color))
        # Visual action: Animate point_a moving to point_b
        self.play(self.objects["point_a"].animate.move_to(self.objects["point_b"].get_center()))
        # Update explanation text
        new_explanation = Text("Step 3: Translate the blue point from -2 to 3.", color=GRAY_B, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        animation_time = 3.0  # Estimate for Indicate + move animation + ReplacementTransform
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        step = {
            "step": 4,
            "signal_action": {"type": "Circumscribe", "target": "point_a", "color": "YELLOW"},
            "duration": 8.952,
            "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_03.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action (point_a is at new position, but we still refer to the object)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal.get("color") == "YELLOW" else eval(signal.get("color"))
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        # Visual action: Create arrow_zero (zero-length arrow at original point_a position)
        # Need to reset arrow_zero to original start position (point_a moved)
        arrow_zero_start_original = number_line.n2p(-2)
        arrow_zero_new = Arrow(start=arrow_zero_start_original, end=arrow_zero_start_original, color=YELLOW, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        self.objects["arrow_zero"] = arrow_zero_new
        self.play(Create(arrow_zero_new))
        # Update explanation text
        new_explanation = Text("Step 4: Represent the translation with a vector (arrow).", color=GRAY_B, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        animation_time = 3.0  # Estimate for Circumscribe + Create + ReplacementTransform
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        step = {
            "step": 5,
            "signal_action": {"type": "Indicate", "target": "arrow_full", "color": "RED"},
            "duration": 7.488,
            "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_04.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action (arrow_full exists in objects but not yet added to scene)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = RED if signal.get("color") == "RED" else eval(signal.get("color"))
            # We need to add arrow_full to scene first for Indicate to work, but it's not yet visible.
            # Instead, we'll indicate after the transformation.
            pass
        # Visual action: ReplacementTransform arrow_zero to arrow_full, then write distance label
        self.play(ReplacementTransform(self.objects["arrow_zero"], self.objects["arrow_full"]))
        # Now indicate the full arrow
        self.play(Indicate(self.objects["arrow_full"], color=RED))
        # Position and write distance label
        self.objects["distance_label"].next_to(self.objects["arrow_full"], UP, buff=0.3)
        self.play(Write(self.objects["distance_label"]))
        # Update explanation text
        new_explanation = Text("Step 5: The arrow length is the distance: 5 units.", color=GRAY_B, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        animation_time = 4.0  # Estimate for ReplacementTransform + Indicate + Write + ReplacementTransform
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 2))