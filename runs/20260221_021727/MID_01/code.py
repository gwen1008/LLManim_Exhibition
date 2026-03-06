'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing distance between two points on a number line as a directed arrow and the arithmetic formula (B - A).
# 2. Layout Strategy: High-Low Split
#    - Header Region: [y=3.5] for Title "Distance on a Number Line"
#    - Main Content: [Center y=0] for number line, points, arrow animation.
#    - Footer Region: [Bottom y=-3.5] for step captions and final formula.
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for point+label pairs. Keep footer text scaled to 0.8.
#    - Ensure arrow and distance label do not overlap with point labels.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step? YES, using provided audio_path.
#    - [x] Files: "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_XX.mp3"
# 5. Animation Flow:
#    Step 1: Fade in title.
#    Step 2: Draw number line, update footer.
#    Step 3: Create points A & B, write labels, indicate points, update footer.
#    Step 4: Show dashed connector, create zero-length arrow, circumscribe, update footer.
#    Step 5: Transform arrow to full length, write distance label, fade out dashed line, replace footer with final formula.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan
        # Title
        title = Text("Distance on a Number Line", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Number Line
        number_line = NumberLine(
            x_range=[-5.5, 5.5, 1],
            length=12,
            include_numbers=True,
            include_tip=True,
            color=GRAY_B  # LIGHT_GRAY maps to GRAY_B
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line
        
        # Point A and its label
        point_a = Dot(radius=0.08, color=BLUE)
        point_a.move_to(number_line.number_to_point(-2))
        self.objects["point_a"] = point_a
        
        label_a = MathTex("A", color=BLUE, font_size=30)
        label_a.next_to(point_a, UP, buff=0.2)
        self.objects["label_a"] = label_a
        
        # Point B and its label
        point_b = Dot(radius=0.08, color=RED)
        point_b.move_to(number_line.number_to_point(3))
        self.objects["point_b"] = point_b
        
        label_b = MathTex("B", color=RED, font_size=30)
        label_b.next_to(point_b, UP, buff=0.2)
        self.objects["label_b"] = label_b
        
        # Dashed connector
        dashed_connector = DashedLine(
            start=point_a.get_center(),
            end=point_b.get_center(),
            color=YELLOW,
            dash_length=0.1
        )
        self.objects["dashed_connector"] = dashed_connector
        
        # Arrow start (zero-length)
        arrow_start = Arrow(
            start=point_a.get_center(),
            end=point_a.get_center(),
            color=GREEN,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["arrow_start"] = arrow_start
        
        # Distance label (will be positioned later)
        distance_label = MathTex("5", color=GREEN, font_size=35)
        # Position will be set after arrow is created
        self.objects["distance_label"] = distance_label
        
        # Step caption (initial)
        step_caption = Text("Step 1: Draw the number line.", color=GRAY_B, font_size=24)
        step_caption.scale(0.8)
        step_caption.move_to(footer_anchor)
        self.objects["step_caption"] = step_caption
        
        # Final formula
        final_formula = MathTex("3 - (-2) = 5", color=YELLOW, font_size=32)
        final_formula.scale(0.8)
        final_formula.move_to(footer_anchor)
        self.objects["final_formula"] = final_formula
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        step = {
            "step": 1,
            "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_00.mp3",
            "duration": 4.344
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Visual Action
        self.play(FadeIn(self.objects["title"]))
        animation_time = 1.0  # Estimated run_time for FadeIn
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 2
        step = {
            "step": 2,
            "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_01.mp3",
            "duration": 6.264
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Create new step caption
        new_caption = Text("Step 2: Mark points A and B.", color=GRAY_B, font_size=24)
        new_caption.scale(0.8)
        new_caption.move_to(footer_anchor)
        # Visual Actions
        self.play(
            Create(self.objects["number_line"]),
            ReplacementTransform(self.objects["step_caption"], new_caption)
        )
        self.objects["step_caption"] = new_caption
        animation_time = 2.0  # Estimated for Create + ReplacementTransform
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 3
        step = {
            "step": 3,
            "signal_action": [
                {"type": "Indicate", "target": "point_a", "color": "YELLOW"},
                {"type": "Indicate", "target": "point_b", "color": "YELLOW"}
            ],
            "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_02.mp3",
            "duration": 5.472
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Actions
        if step.get("signal_action"):
            for signal in step["signal_action"]:
                target_obj = self.objects[signal["target"]]
                color = YELLOW if signal.get("color") == "YELLOW" else eval(signal.get("color"))
                self.play(Indicate(target_obj, color=color))
        # Create new step caption
        new_caption = Text("Step 3: Visualize the distance.", color=GRAY_B, font_size=24)
        new_caption.scale(0.8)
        new_caption.move_to(footer_anchor)
        # Visual Actions
        self.play(
            Create(self.objects["point_a"]),
            Create(self.objects["point_b"]),
            Write(self.objects["label_a"]),
            Write(self.objects["label_b"]),
            ReplacementTransform(self.objects["step_caption"], new_caption)
        )
        self.objects["step_caption"] = new_caption
        animation_time = 3.0  # Estimated for signal actions + creates + writes + transform
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 4
        step = {
            "step": 4,
            "signal_action": {"type": "Circumscribe", "target": "dashed_connector", "color": "GREEN"},
            "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_03.mp3",
            "duration": 7.944
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action"):
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = GREEN if signal.get("color") == "GREEN" else eval(signal.get("color"))
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        # Create new step caption
        new_caption = Text("Step 4: Animate the jump of 5 units.", color=GRAY_B, font_size=24)
        new_caption.scale(0.8)
        new_caption.move_to(footer_anchor)
        # Visual Actions
        self.play(
            Create(self.objects["dashed_connector"]),
            Create(self.objects["arrow_start"]),
            ReplacementTransform(self.objects["step_caption"], new_caption)
        )
        self.objects["step_caption"] = new_caption
        animation_time = 3.0  # Estimated for signal + creates + transform
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 5
        step = {
            "step": 5,
            "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_04.mp3",
            "duration": 11.376
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Create final arrow (target for transform)
        arrow_final = Arrow(
            start=self.objects["point_a"].get_center(),
            end=self.objects["point_b"].get_center(),
            color=GREEN,
            max_tip_length_to_length_ratio=0.15
        )
        # Position distance label above arrow's midpoint
        arrow_mid = (self.objects["point_a"].get_center() + self.objects["point_b"].get_center()) / 2
        self.objects["distance_label"].next_to(arrow_mid, UP, buff=0.3)
        # Visual Actions
        self.play(
            Transform(self.objects["arrow_start"], arrow_final),
            Write(self.objects["distance_label"]),
            FadeOut(self.objects["dashed_connector"]),
            ReplacementTransform(self.objects["step_caption"], self.objects["final_formula"])
        )
        animation_time = 4.0  # Estimated for Transform, Write, FadeOut, ReplacementTransform
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Final hold
        self.wait(max(0.1, 2))