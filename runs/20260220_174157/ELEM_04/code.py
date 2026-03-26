'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually demonstrate how a protractor measures a 60° angle by aligning its center with the vertex and baseline with a ray, showing the 60° tick mark intersects the second ray.
# 2. Layout Strategy:
#    - Header Region: [y=3.2] for Title
#    - Main Content: [Center y=0] for angle and protractor
#    - Footer Region: [Bottom y=-3.2] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: All geometric elements centered at ORIGIN. Title and explanation placed in dedicated zones.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show vertex dot.
#    - Step 2: Draw baseline ray (blue) with Indicate signal.
#    - Step 3: Draw 60° ray (green) with Indicate signal.
#    - Step 4: Draw protractor arc with Circumscribe signal on vertex.
#    - Step 5: Draw 0° tick mark with Indicate signal.
#    - Step 6: Draw 60° tick mark with Indicate signal.
#    - Step 7: Add "60°" label.
#    - Step 8: Show final explanation text.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create anchors
        global_center = ORIGIN
        title_anchor = 3.2 * UP
        explanation_anchor = 3.2 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan
        # title
        title = Text("Measuring a 60° Angle", font_size=40, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # vertex
        vertex = Dot(radius=0.08, color=YELLOW)
        vertex.move_to(global_center)
        self.objects["vertex"] = vertex

        # ray1 (baseline)
        ray1 = Line(start=[0,0,0], end=[4,0,0], color=BLUE, stroke_width=4)
        ray1.move_to(global_center)
        self.objects["ray1"] = ray1

        # ray2 (60° ray)
        ray2 = Line(start=[0,0,0], end=[2, 3.464, 0], color=GREEN, stroke_width=4)
        ray2.move_to(global_center)
        self.objects["ray2"] = ray2

        # protractor_arc_base
        protractor_arc_base = Arc(radius=3, start_angle=0, angle=PI, color=GRAY_B, stroke_width=3)
        protractor_arc_base.move_to(global_center)
        self.objects["protractor_arc_base"] = protractor_arc_base

        # protractor_center_dot (Note: This is a separate red dot at the center, distinct from the yellow vertex)
        protractor_center_dot = Dot(radius=0.06, color=RED)
        protractor_center_dot.move_to(global_center)
        self.objects["protractor_center_dot"] = protractor_center_dot

        # tick_0
        tick_0 = Line(start=[3,0,0], end=[2.7,0,0], color=WHITE, stroke_width=2)
        tick_0.move_to(global_center)
        self.objects["tick_0"] = tick_0

        # tick_60
        tick_60 = Line(start=[1.5, 2.598, 0], end=[1.2, 2.078, 0], color=YELLOW, stroke_width=3)
        tick_60.move_to(global_center)
        self.objects["tick_60"] = tick_60

        # label_60
        label_60 = MathTex("60^\\circ", color=YELLOW, font_size=30)
        label_60.move_to(global_center + [1.0, 1.8, 0])
        self.objects["label_60"] = label_60

        # explanation_text
        explanation_text = Text(
            "The protractor's 60° mark intersects the second ray, confirming the angle measure.",
            font_size=24, color=GRAY_C
        )
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        step = {
            "step": 1,
            "duration": 4.368,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_00.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Visual Action
        self.play(Create(self.objects["vertex"]))
        # Wait for remaining audio
        animation_time = 1.0  # Approximate run_time for Create
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Step 2
        step = {
            "step": 2,
            "signal_action": {"type": "Indicate", "target": "ray1", "color": "BLUE"},
            "duration": 5.544,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_01.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        # Visual Action
        self.play(Create(self.objects["ray1"]))
        # Wait for remaining audio
        animation_time = 2.0  # Approx for Indicate + Create
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Step 3
        step = {
            "step": 3,
            "signal_action": {"type": "Indicate", "target": "ray2", "color": "GREEN"},
            "duration": 4.752,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_02.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        # Visual Action
        self.play(Create(self.objects["ray2"]))
        # Wait for remaining audio
        animation_time = 2.0
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Step 4
        step = {
            "step": 4,
            "signal_action": {"type": "Circumscribe", "target": "vertex", "color": "YELLOW"},
            "duration": 8.04,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_03.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        # Visual Action
        self.play(Create(self.objects["protractor_arc_base"]))
        # Wait for remaining audio
        animation_time = 2.0  # Circumscribe + Create
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Step 5
        step = {
            "step": 5,
            "signal_action": {"type": "Indicate", "target": "tick_0", "color": "WHITE"},
            "duration": 4.272,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_04.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        # Visual Action
        self.play(Create(self.objects["tick_0"]))
        # Wait for remaining audio
        animation_time = 2.0
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Step 6
        step = {
            "step": 6,
            "signal_action": {"type": "Indicate", "target": "tick_60", "color": "YELLOW"},
            "duration": 7.152,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_05.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        # Visual Action
        self.play(Create(self.objects["tick_60"]))
        # Wait for remaining audio
        animation_time = 2.0
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Step 7
        step = {
            "step": 7,
            "signal_action": {"type": "Write", "target": "label_60", "color": "YELLOW"},
            "duration": 4.608,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_06.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action (Note: Signal type is "Write", but we interpret as Write animation)
        # We'll just Write the label as per visual_action.
        # Visual Action
        self.play(Write(self.objects["label_60"]))
        # Wait for remaining audio
        animation_time = 1.0
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Step 8
        step = {
            "step": 8,
            "duration": 8.544,
            "audio_path": "media/audio/繪製一個_60_度的角_並疊加一個半圓形_388462d1c9/step_07.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Visual Action
        self.play(Write(self.objects["explanation_text"]))
        # Wait for remaining audio
        animation_time = 1.0
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Final hold
        self.wait(max(0.1, 2))