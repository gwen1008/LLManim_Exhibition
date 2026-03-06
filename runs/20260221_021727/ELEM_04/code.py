'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Demonstrate how a protractor measures an angle by aligning its center and baseline with the angle's vertex and one ray, showing that the second ray aligns with the 60° tick mark.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for angle and protractor
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroup for protractor parts (arc, ticks, labels) and set its z_index below the rays.
#    - The rays will be created first and have higher z_index to be on top.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Draw horizontal ray (baseline).
#    - Step 2: Indicate baseline, draw 60° ray.
#    - Step 3: Circumscribe vertex, fade in protractor center dot.
#    - Step 4: Indicate baseline, draw protractor arc.
#    - Step 5: Indicate 60° tick, draw ticks and labels (0° and 60°).
#    - Step 6: Circumscribe and write final angle label.
'''

from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}

        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        vertex = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Measuring a 60° Angle with a Protractor", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Ray Baseline (horizontal)
        ray_baseline = Line(start=ORIGIN, end=4*RIGHT, color=BLUE, stroke_width=6)
        ray_baseline.move_to(vertex, aligned_edge=LEFT)
        self.objects["ray_baseline"] = ray_baseline

        # Ray at 60°
        # Endpoint calculated: [2, 3.464, 0] for length ~4 at 60°
        ray_60deg = Line(start=ORIGIN, end=np.array([2.0, 3.464, 0]), color=GREEN, stroke_width=6)
        ray_60deg.move_to(vertex, aligned_edge=LEFT)
        self.objects["ray_60deg"] = ray_60deg

        # Protractor Arc (semicircle)
        protractor_arc = Arc(radius=3.5, start_angle=0, angle=PI, color=GRAY_B, stroke_width=4)
        protractor_arc.move_to(vertex)
        self.objects["protractor_arc"] = protractor_arc

        # Protractor Center Dot
        protractor_center_dot = Dot(radius=0.08, color=RED)
        protractor_center_dot.move_to(vertex)
        self.objects["protractor_center_dot"] = protractor_center_dot

        # Tick marks and labels
        # Tick at 0°
        tick_0_start = 3.5 * RIGHT
        tick_0_end = 3.8 * RIGHT
        tick_0 = Line(start=tick_0_start, end=tick_0_end, color=WHITE, stroke_width=3)
        tick_0.move_to(vertex)
        self.objects["tick_0"] = tick_0

        # Tick at 60°
        angle_rad = PI / 3  # 60 degrees
        tick_60_start = 3.5 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
        tick_60_end = 3.8 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
        tick_60 = Line(start=tick_60_start, end=tick_60_end, color=YELLOW, stroke_width=5)
        tick_60.move_to(vertex)
        self.objects["tick_60"] = tick_60

        # Label for 0°
        label_0 = MathTex("0^\\circ", color=WHITE, font_size=24)
        label_0.next_to(tick_0, RIGHT, buff=0.1)
        self.objects["label_0"] = label_0

        # Label for 60°
        label_60 = MathTex("60^\\circ", color=YELLOW, font_size=24)
        label_60.next_to(tick_60, UR, buff=0.1)
        self.objects["label_60"] = label_60

        # Final angle label
        angle_label = MathTex("60^\\circ", color=YELLOW, font_size=36)
        angle_label.move_to(vertex + np.array([1.2, 0.8, 0]))
        self.objects["angle_label"] = angle_label

        # Step explanation (dynamic, will be updated)
        step_explanation = Text("Step 1: Draw the angle.", color=GRAY_B, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # Group protractor parts for z-index management
        protractor_group = VGroup(
            protractor_arc,
            protractor_center_dot,
            tick_0,
            tick_60,
            label_0,
            label_60
        )
        protractor_group.set_z_index(0)
        # Rays should be on top
        ray_baseline.set_z_index(1)
        ray_60deg.set_z_index(1)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        step = {
            "step": 1,
            "duration": 6.528,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_00.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Visual Action
        self.play(Write(self.objects["title"]))
        self.play(Create(self.objects["ray_baseline"]))
        self.play(Write(self.objects["step_explanation"]))
        animation_time = 3.0  # Approximate total run_time for Write+Create+Write
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 2
        step = {
            "step": 2,
            "signal_action": {"type": "Indicate", "target": "ray_baseline", "color": "YELLOW"},
            "duration": 5.304,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_01.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Update explanation
        new_explanation = Text("Step 2: Draw the second ray at 60°.", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal.get("color") == "YELLOW" else eval(signal["color"])
            self.play(Indicate(target_obj, color=color))
        # Visual Action
        self.play(Create(self.objects["ray_60deg"]))
        animation_time = 4.0  # ReplacementTransform + Indicate + Create
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 3
        step = {
            "step": 3,
            "signal_action": {"type": "Circumscribe", "target": "vertex", "color": "RED"},
            "duration": 8.52,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_02.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Update explanation
        new_explanation = Text("Step 3: Align protractor center with vertex.", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Signal Action (Circumscribe the vertex location - create a temporary dot)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            # Create a dot at vertex for circumscribing
            temp_dot = Dot(vertex, color=RED, radius=0.1)
            self.add(temp_dot)
            color = RED if signal.get("color") == "RED" else eval(signal["color"])
            self.play(Circumscribe(temp_dot, color=color, run_time=1))
            self.remove(temp_dot)
        # Visual Action
        self.play(FadeIn(self.objects["protractor_center_dot"]))
        animation_time = 4.0  # ReplacementTransform + Circumscribe + FadeIn
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 4
        step = {
            "step": 4,
            "signal_action": {"type": "Indicate", "target": "ray_baseline", "color": "YELLOW"},
            "duration": 5.976,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_03.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Update explanation
        new_explanation = Text("Step 4: Place protractor arc, align 0° with baseline.", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal.get("color") == "YELLOW" else eval(signal["color"])
            self.play(Indicate(target_obj, color=color))
        # Visual Action
        self.play(Create(self.objects["protractor_arc"]))
        animation_time = 4.0  # ReplacementTransform + Indicate + Create
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 5
        step = {
            "step": 5,
            "signal_action": {"type": "Indicate", "target": "tick_60", "color": "YELLOW"},
            "duration": 9.024,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_04.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Update explanation
        new_explanation = Text("Step 5: The 60° tick aligns with the second ray.", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Signal Action (Indicate the tick_60 line)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal.get("color") == "YELLOW" else eval(signal["color"])
            self.play(Indicate(target_obj, color=color))
        # Visual Action: Create ticks and labels
        self.play(
            Create(self.objects["tick_0"]),
            Create(self.objects["tick_60"]),
            Write(self.objects["label_0"]),
            Write(self.objects["label_60"])
        )
        animation_time = 5.0  # ReplacementTransform + Indicate + multiple creates
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Step 6
        step = {
            "step": 6,
            "signal_action": {"type": "Circumscribe", "target": "angle_label", "color": "YELLOW"},
            "duration": 3.672,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_05.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Update explanation
        new_explanation = Text("Step 6: Therefore, the angle measures 60°.", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Visual Action
        self.play(Write(self.objects["angle_label"]))
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal.get("color") == "YELLOW" else eval(signal["color"])
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        animation_time = 3.0  # ReplacementTransform + Write + Circumscribe
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 2))