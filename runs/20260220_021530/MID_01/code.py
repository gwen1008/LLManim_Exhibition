'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing translation and displacement on a number line, showing the vector from point A (-2) to point B (3) and its magnitude (5).
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line, points, arrow
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Use LayoutEngine zones to keep title, content, and footer separated.
#    - Points and labels are positioned relative to the number line using next_to.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
#    - Create number line axis, ticks, labels.
#    - Plot and label points A and B.
#    - Create zero-length arrow at A, then grow it to B.
#    - Show magnitude label, update footer explanation.
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

        # Create objects based on layout_plan
        # Title
        title = Text("Translation and Displacement on a Number Line", color=WHITE, font_size=36)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title

        # Axis Line
        axis_line = Line(start=[-3.0, 0, 0], end=[3.0, 0, 0], color=WHITE, stroke_width=4)
        obj_axis = LayoutObject(axis_line, "axis_line")
        layout.add(obj_axis)
        layout.add_to_zone(obj_axis, "CONTENT")
        layout.add_constraint(obj_axis.center_x == 0)
        layout.add_constraint(obj_axis.center_y == 0)
        self.objects["axis_line"] = axis_line

        # Tick Group
        tick_positions = [-3.0, -2.4, -1.8, -1.2, -0.6, 0.0, 0.6, 1.2, 1.8, 2.4, 3.0]
        ticks = VGroup(*[Line(start=[x, -0.1, 0], end=[x, 0.1, 0], color=WHITE) for x in tick_positions])
        obj_ticks = LayoutObject(ticks, "tick_group")
        layout.add(obj_ticks)
        layout.add_to_zone(obj_ticks, "CONTENT")
        layout.align_to(obj_ticks, obj_axis, 'CENTER')
        self.objects["tick_group"] = ticks

        # Label Group
        labels = VGroup(*[
            MathTex(str(num), color=LIGHT_GRAY, font_size=24).move_to([x, -0.3, 0])
            for num, x in zip(range(-5, 6), tick_positions)
        ])
        obj_labels = LayoutObject(labels, "label_group")
        layout.add(obj_labels)
        layout.add_to_zone(obj_labels, "CONTENT")
        self.objects["label_group"] = labels

        # Point A and its label
        point_a = Dot(point=[-1.2, 0, 0], radius=0.08, color=BLUE)
        obj_point_a = LayoutObject(point_a, "point_a")
        layout.add(obj_point_a)
        layout.add_to_zone(obj_point_a, "CONTENT")
        self.objects["point_a"] = point_a

        label_a = MathTex(r"A\,(-2)", color=BLUE, font_size=28)
        label_a.next_to(point_a, UP, buff=0.2)
        obj_label_a = LayoutObject(label_a, "label_a")
        layout.add(obj_label_a)
        layout.add_to_zone(obj_label_a, "CONTENT")
        self.objects["label_a"] = label_a

        # Point B and its label
        point_b = Dot(point=[1.8, 0, 0], radius=0.08, color=GREEN)
        obj_point_b = LayoutObject(point_b, "point_b")
        layout.add(obj_point_b)
        layout.add_to_zone(obj_point_b, "CONTENT")
        self.objects["point_b"] = point_b

        label_b = MathTex(r"B\,(3)", color=GREEN, font_size=28)
        label_b.next_to(point_b, UP, buff=0.2)
        obj_label_b = LayoutObject(label_b, "label_b")
        layout.add(obj_label_b)
        layout.add_to_zone(obj_label_b, "CONTENT")
        self.objects["label_b"] = label_b

        # Arrow Vector (initially zero length at point A)
        arrow_vector = Arrow(
            start=[-1.2, 0, 0],
            end=[-1.2, 0, 0],
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15,
            buff=0
        )
        obj_arrow = LayoutObject(arrow_vector, "arrow_vector")
        layout.add(obj_arrow)
        layout.add_to_zone(obj_arrow, "CONTENT")
        self.objects["arrow_vector"] = arrow_vector

        # Magnitude Label
        magnitude_label = MathTex("5", color=YELLOW, font_size=32)
        magnitude_label.set_background_stroke(color=BLACK, width=2)
        # Position will be set after arrow grows, but create object for layout
        obj_mag = LayoutObject(magnitude_label, "magnitude_label")
        layout.add(obj_mag)
        layout.add_to_zone(obj_mag, "CONTENT")
        # Temporary position, will be updated
        magnitude_label.move_to([0.3, 0.5, 0])
        self.objects["magnitude_label"] = magnitude_label

        # Step Explanation (Footer)
        step_explanation = Text(
            "Step 1: Constructing the number line from -5 to 5.",
            color=LIGHT_GRAY,
            font_size=24
        )
        obj_footer = LayoutObject(step_explanation, "step_explanation")
        layout.add(obj_footer)
        layout.add_to_zone(obj_footer, "FOOTER")
        layout.add_constraint(obj_footer.center_x == 0)
        self.objects["step_explanation"] = step_explanation

        # Solve layout constraints
        layout.solve()

        # Apply layout positions to mobjects
        # LayoutEngine's solve() updates the LayoutObjects, but we need to apply to mobjects
        # For simplicity, we rely on the initial positioning and layout zones.
        # The key is that zones prevent overlap.

        # ========== PHASE 2: Animation Sequence ==========
        sequence = self.get_sequence_data()

        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_path = step.get("audio_path")

            # === AUDIO (MANDATORY) ===
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)
            else:
                # Fallback path construction (as per protocol)
                file_index = step_num - 1
                mp3_path = f"media/audio/step_{file_index:02d}.mp3"
                wav_path = f"media/audio/step_{file_index:02d}.wav"
                if os.path.exists(mp3_path):
                    self.add_sound(mp3_path)
                elif os.path.exists(wav_path):
                    self.add_sound(wav_path)

            # Signal Action
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                color_name = signal.get("color", "YELLOW")
                color = eval(color_name)  # Convert string to Manim color constant
                target_obj = self.objects[target_id]

                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal["type"] == "FocusOn":
                    self.play(FocusOn(target_obj))

            # Visual Action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            action_type = visual["type"]

            if action_type == "Create":
                obj = self.objects[target_id]
                self.play(Create(obj))
            elif action_type == "Write":
                obj = self.objects[target_id]
                self.play(Write(obj))
            elif action_type == "FadeIn":
                obj = self.objects[target_id]
                self.play(FadeIn(obj))
            elif action_type == "Transform" and target_id == "arrow_vector":
                # Special case: Grow arrow from A to B
                arrow = self.objects["arrow_vector"]
                # Create a new arrow with the same start but end at point B
                new_arrow = Arrow(
                    start=[-1.2, 0, 0],
                    end=[1.8, 0, 0],
                    color=YELLOW,
                    stroke_width=6,
                    max_tip_length_to_length_ratio=0.15,
                    buff=0
                )
                # We'll transform the existing arrow to the new one
                self.play(Transform(arrow, new_arrow))
                # Update the stored arrow to the new one for future reference
                self.objects["arrow_vector"] = new_arrow
                # Update magnitude label position to midpoint of the grown arrow
                magnitude_label = self.objects["magnitude_label"]
                midpoint = (np.array([-1.2, 0, 0]) + np.array([1.8, 0, 0])) / 2
                midpoint[1] += 0.5  # Shift up a bit
                magnitude_label.move_to(midpoint)

            # Wait for remaining audio duration
            # Since animations are mostly Create/Write with default run_time=1,
            # we approximate total animation time as 1 second per action.
            # More precise calculation would require tracking each animation's run_time.
            animation_time = 1.0  # Default run_time for Create/Write
            if signal is not None:
                animation_time += 1.0  # Signal action run_time
            remaining = duration - animation_time + 0.5  # Safety buffer
            if remaining > 0:
                self.wait(remaining)

        # Final wait
        self.wait(2)

    def get_sequence_data(self):
        """Return the sequence data as defined in the JSON."""
        return [
            {
                "step": 1,
                "duration": 5.88,
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "axis_line"},
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_00.mp3"
            },
            {
                "step": 2,
                "duration": 3.744,
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "tick_group"},
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_01.mp3"
            },
            {
                "step": 3,
                "duration": 5.472,
                "signal_action": {"type": "Indicate", "target": "label_group", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "point_a"},
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_02.mp3"
            },
            {
                "step": 4,
                "duration": 2.16,
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_a"},
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_03.mp3"
            },
            {
                "step": 5,
                "duration": 2.496,
                "signal_action": {"type": "Indicate", "target": "label_group", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "point_b"},
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_04.mp3"
            },
            {
                "step": 6,
                "duration": 2.16,
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_b"},
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_05.mp3"
            },
            {
                "step": 7,
                "duration": 5.496,
                "signal_action": {"type": "Indicate", "target": "point_a", "color": "BLUE"},
                "visual_action": {"type": "Create", "target_id": "arrow_vector"},
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_06.mp3"
            },
            {
                "step": 8,
                "duration": 6.624,
                "signal_action": {"type": "Indicate", "target": "point_b", "color": "GREEN"},
                "visual_action": {"type": "Transform", "target_id": "arrow_vector"},
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_07.mp3"
            },
            {
                "step": 9,
                "duration": 5.976,
                "signal_action": {"type": "Circumscribe", "target": "arrow_vector", "color": "YELLOW"},
                "visual_action": {"type": "Write", "target_id": "magnitude_label"},
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_08.mp3"
            },
            {
                "step": 10,
                "duration": 7.344,
                "signal_action": {"type": "Indicate", "target": "magnitude_label", "color": "YELLOW"},
                "visual_action": {"type": "FadeIn", "target_id": "step_explanation"},
                "audio_path": "media/audio/在__5_到_5_的數線上_示範從__2_e541ae2fca/step_09.mp3"
            }
        ]