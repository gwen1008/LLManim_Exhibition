'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the relationship between circumference and diameter (C = πD) using the "cut and unroll" metaphor.
# 2. Layout Strategy: Horizontal split with zones.
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for circle (left) and unrolled line (right)
#    - Footer Region: [Bottom y=-3.5] for final formula and explanation
# 3. Anti-Overlap Check: Objects are placed in distinct zones. Circle on left, line on right. Use VGroups for measurement copies.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_XX.mp3"
# 5. Animation Flow: Show circle → highlight diameter → cut and unroll → measure line with diameter copies → reveal π relationship.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        circle_anchor = 3 * LEFT  # Left of center
        line_anchor = 3 * RIGHT   # Right of center, start of unrolled line
        footer_anchor = 3.5 * DOWN + 0.5 * UP  # Slightly above bottom edge

        # Create objects from layout_plan.objects
        # Title
        title = Text("Unrolling a Circle: Discovering π", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Circle
        circle = Circle(radius=2.0, color=BLUE, stroke_width=6)
        circle.move_to(circle_anchor)
        self.objects["circle"] = circle

        # Diameter line (horizontal across circle)
        diameter_line = Line(circle_anchor + 2 * LEFT, circle_anchor + 2 * RIGHT, color=YELLOW, stroke_width=4)
        self.objects["diameter_line"] = diameter_line

        # Diameter label
        diameter_label = MathTex("D", color=YELLOW)
        diameter_label.next_to(diameter_line, UP, buff=0.2)
        self.objects["diameter_label"] = diameter_label

        # Cut indicator (small red arc at top of circle)
        cut_indicator = Arc(radius=2.1, angle=0.5, start_angle=PI/2 - 0.25, color=RED, stroke_width=8)
        cut_indicator.move_to(circle_anchor)
        cut_indicator.set_opacity(0.0)
        self.objects["cut_indicator"] = cut_indicator

        # Unrolled line (circumference length = 2*π*radius)
        line_length = 2 * PI * 2.0  # circumference
        unrolled_line = Line(line_anchor, line_anchor + line_length * RIGHT, color=GREEN, stroke_width=6)
        unrolled_line.set_opacity(0.0)
        self.objects["unrolled_line"] = unrolled_line

        # Circumference label
        circumference_label = MathTex("C", color=GREEN)
        circumference_label.next_to(unrolled_line, UP, buff=0.2)
        circumference_label.set_opacity(0.0)
        self.objects["circumference_label"] = circumference_label

        # Diameter copies for measurement
        diameter_copy_1 = Line(line_anchor, line_anchor + 4.0 * RIGHT, color=YELLOW, stroke_width=3)
        diameter_copy_1.set_opacity(0.0)
        self.objects["diameter_copy_1"] = diameter_copy_1

        diameter_copy_2 = Line(line_anchor + 4.0 * RIGHT, line_anchor + 8.0 * RIGHT, color=YELLOW, stroke_width=3)
        diameter_copy_2.set_opacity(0.0)
        self.objects["diameter_copy_2"] = diameter_copy_2

        diameter_copy_3 = Line(line_anchor + 8.0 * RIGHT, line_anchor + 12.0 * RIGHT, color=YELLOW, stroke_width=3)
        diameter_copy_3.set_opacity(0.0)
        self.objects["diameter_copy_3"] = diameter_copy_3

        # Pi approximate label
        pi_approx_label = MathTex("C \\approx 3.14 \\times D", color=WHITE)
        pi_approx_label.next_to(diameter_copy_3, UP, buff=0.5)
        pi_approx_label.set_opacity(0.0)
        self.objects["pi_approx_label"] = pi_approx_label

        # Pi exact label (footer)
        pi_exact_label = MathTex("C = \\pi D", color=ORANGE, font_size=36)
        pi_exact_label.move_to(footer_anchor)
        self.objects["pi_exact_label"] = pi_exact_label

        # Explanation text
        explanation_text = Text("The circumference is about 3.14 times the diameter. This constant is π.", color=GRAY_B, font_size=24)
        explanation_text.next_to(pi_exact_label, DOWN, buff=0.5)
        explanation_text.set_opacity(0.0)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        step = {
            "step": 1,
            "duration": 6.432,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_00.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(Write(self.objects["title"]), run_time=1)
        self.play(Create(self.objects["circle"]), run_time=2)
        animation_time = 1 + 2
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 2
        step = {
            "step": 2,
            "signal_action": {"type": "Indicate", "target": "diameter_line", "color": "YELLOW"},
            "duration": 2.448,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_01.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action") is not None:
            self.play(Indicate(self.objects[step["signal_action"]["target"]]), run_time=1)
        self.play(Create(self.objects["diameter_line"]), Write(self.objects["diameter_label"]), run_time=1.5)
        animation_time = 1 + 1.5
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 3
        step = {
            "step": 3,
            "signal_action": {"type": "Indicate", "target": "cut_indicator", "color": "RED"},
            "duration": 4.992,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_02.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action") is not None:
            self.play(Indicate(self.objects["cut_indicator"]), run_time=1)
        self.play(self.objects["cut_indicator"].animate.set_opacity(1.0), run_time=0.5)
        # Create a copy of the circle's perimeter for the transform
        circle_perimeter = self.objects["circle"].copy()
        circle_perimeter.set_stroke(color=GREEN, width=6)
        self.add(circle_perimeter)
        self.play(Transform(circle_perimeter, self.objects["unrolled_line"]), run_time=2)
        self.remove(circle_perimeter)
        self.play(self.objects["unrolled_line"].animate.set_opacity(1.0), self.objects["circumference_label"].animate.set_opacity(1.0), run_time=0.5)
        animation_time = 1 + 0.5 + 2 + 0.5
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 4
        step = {
            "step": 4,
            "signal_action": {"type": "Circumscribe", "target": "unrolled_line", "color": "GREEN"},
            "duration": 5.184,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_03.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action") is not None:
            self.play(Circumscribe(self.objects["unrolled_line"], color=GREEN), run_time=1)
        animation_time = 1
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 5
        step = {
            "step": 5,
            "signal_action": {"type": "Indicate", "target": "diameter_copy_1", "color": "YELLOW"},
            "duration": 9.768,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_04.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action") is not None:
            self.play(Indicate(self.objects["diameter_copy_1"]), run_time=1)
        self.play(self.objects["diameter_copy_1"].animate.set_opacity(1.0), run_time=0.5)
        self.play(self.objects["diameter_copy_2"].animate.set_opacity(1.0), run_time=0.5)
        self.play(self.objects["diameter_copy_3"].animate.set_opacity(1.0), run_time=0.5)
        self.play(self.objects["pi_approx_label"].animate.set_opacity(1.0), run_time=0.5)
        animation_time = 1 + 0.5 + 0.5 + 0.5 + 0.5
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 6
        step = {
            "step": 6,
            "signal_action": {"type": "Indicate", "target": "pi_approx_label", "color": "WHITE"},
            "duration": 10.44,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_05.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action") is not None:
            self.play(Indicate(self.objects["pi_approx_label"]), run_time=1)
        animation_time = 1
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 7
        step = {
            "step": 7,
            "duration": 5.856,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_06.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(self.objects["pi_exact_label"].animate.set_opacity(1.0), run_time=1)
        self.play(self.objects["explanation_text"].animate.set_opacity(1.0), run_time=1)
        animation_time = 1 + 1
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 2))