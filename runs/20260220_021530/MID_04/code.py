'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually prove the Corresponding Angles Theorem using a geometric construction with parallel lines and a transversal, then demonstrate angle congruence via transformation.
# 2. Layout Strategy: Use LayoutEngine for zones.
#    - Header Region: [y=3.0] for Title
#    - Main Content: [Center y=0] for the geometric diagram
#    - Footer Region: [Bottom y=-3.0] for step-by-step explanation text
# 3. Anti-Overlap Check: Use LayoutEngine zones to keep title, diagram, and text separated. Diagram elements are positioned relative to each other using geometry_def coordinates.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step where audio_path is provided?
#    - [x] Files: "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_XX.mp3"
# 5. Animation Flow: Create lines and labels -> highlight corresponding angles -> state postulate -> transform top angle to bottom angle -> indicate congruence.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        layout = LayoutEngine()

        # Create objects from layout_plan.objects
        # title
        title = Text("Corresponding Angles Theorem", font_size=40, color=WHITE)
        self.objects["title"] = title
        layout.add(LayoutObject(title, "title"))

        # line_l
        line_l = Line(start=[-3, 1.5, 0], end=[3, 1.5, 0], color=BLUE, stroke_width=4)
        self.objects["line_l"] = line_l
        layout.add(LayoutObject(line_l, "line_l"))

        # line_m
        line_m = Line(start=[-3, -1.5, 0], end=[3, -1.5, 0], color=BLUE, stroke_width=4)
        self.objects["line_m"] = line_m
        layout.add(LayoutObject(line_m, "line_m"))

        # transversal_t
        transversal_t = Line(start=[-2.5, 2.25, 0], end=[2.5, -2.25, 0], color=YELLOW, stroke_width=4)
        self.objects["transversal_t"] = transversal_t
        layout.add(LayoutObject(transversal_t, "transversal_t"))

        # label_l
        label_l = MathTex("l", color=BLUE)
        self.objects["label_l"] = label_l
        # Position will be set after line_l is created and positioned
        layout.add(LayoutObject(label_l, "label_l"))

        # label_m
        label_m = MathTex("m", color=BLUE)
        self.objects["label_m"] = label_m
        layout.add(LayoutObject(label_m, "label_m"))

        # label_t
        label_t = MathTex("t", color=YELLOW)
        self.objects["label_t"] = label_t
        layout.add(LayoutObject(label_t, "label_t"))

        # arc_top
        arc_top = Arc(radius=0.4, angle=30*DEGREES, start_angle=180*DEGREES, color=GREEN, stroke_width=6)
        # Move to calculated intersection point: [-1.732, 1.5, 0]
        arc_top.move_to([-1.732, 1.5, 0])
        self.objects["arc_top"] = arc_top
        layout.add(LayoutObject(arc_top, "arc_top"))

        # arc_bottom
        arc_bottom = Arc(radius=0.4, angle=30*DEGREES, start_angle=180*DEGREES, color=GREEN, stroke_width=6)
        arc_bottom.move_to([-1.732, -1.5, 0])
        self.objects["arc_bottom"] = arc_bottom
        layout.add(LayoutObject(arc_bottom, "arc_bottom"))

        # step_text (initial content)
        step_text = Text("Step 1: Construct parallel lines and a transversal.", font_size=24, color=LIGHT_GRAY)
        self.objects["step_text"] = step_text
        layout.add(LayoutObject(step_text, "step_text"))

        # Apply layout zones
        layout.add_to_zone(layout.get("title"), "HEADER")
        layout.add_to_zone(layout.get("step_text"), "FOOTER")
        # Main diagram objects (lines, arcs, labels) go to CONTENT zone
        for obj_id in ["line_l", "line_m", "transversal_t", "label_l", "label_m", "label_t", "arc_top", "arc_bottom"]:
            layout.add_to_zone(layout.get(obj_id), "CONTENT")

        # Solve layout constraints
        layout.solve()

        # Now adjust label positions relative to lines (as per initial_pos notes)
        # These are relative positions that depend on the line endpoints after layout.
        label_l.next_to(line_l.get_end(), RIGHT, buff=0.2)
        label_m.next_to(line_m.get_end(), RIGHT, buff=0.2)
        label_t.next_to(transversal_t.get_end(), RIGHT+UP, buff=0.2)

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's start with two parallel lines, l and m, and a transversal line t cutting across them.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "line_l", "details": "Draw the top parallel line."},
                "duration": 6.504,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "line_m", "details": "Draw the bottom parallel line."},
                "duration": 2.0
            },
            {
                "step": 3,
                "narrative": "Now, we add the transversal.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "transversal_t", "details": "Draw the slanted transversal line."},
                "duration": 2.712,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "We label our lines for clarity.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_l", "details": "Add label 'l'."},
                "duration": 2.688,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_m", "details": "Add label 'm'."},
                "duration": 2.0
            },
            {
                "step": 6,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_t", "details": "Add label 't'."},
                "duration": 2.0
            },
            {
                "step": 7,
                "narrative": "Focus on a pair of interior angles on the same side of the transversal. These are called corresponding angles.",
                "signal_action": None,
                "visual_action": {"type": "UpdateText", "target_id": "step_text", "details": "Change text to 'Step 2: Identify a pair of corresponding interior angles.'"},
                "duration": 7.608,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "Let's highlight them in green.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "arc_top", "details": "Draw the angle arc at the top intersection."},
                "duration": 2.376,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_07.mp3"
            },
            {
                "step": 9,
                "narrative": "",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "arc_bottom", "details": "Draw the corresponding angle arc at the bottom intersection."},
                "duration": 2.0
            },
            {
                "step": 10,
                "narrative": "The Corresponding Angles Postulate tells us that if lines are parallel, then corresponding angles are congruent.",
                "signal_action": {"type": "Circumscribe", "target": "arc_top", "color": "YELLOW"},
                "visual_action": {"type": "UpdateText", "target_id": "step_text", "details": "Change text to 'Step 3: Postulate: If l || m, then corresponding angles are congruent.'"},
                "duration": 7.032,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_09.mp3"
            },
            {
                "step": 11,
                "narrative": "We can visualize this congruence. Watch as we transform the top angle onto the bottom one.",
                "signal_action": None,
                "visual_action": {"type": "UpdateText", "target_id": "step_text", "details": "Change text to 'Step 4: Visual proof via transformation.'"},
                "duration": 6.72,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_10.mp3"
            },
            {
                "step": 12,
                "narrative": "The angle slides down the transversal and rotates slightly to match its corresponding partner perfectly.",
                "signal_action": None,
                "visual_action": {"type": "Transform", "target_id": "arc_top", "details": "Animate arc_top moving to the position and orientation of arc_bottom. Use a smooth path that suggests sliding along the transversal."},
                "duration": 6.408,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_11.mp3"
            },
            {
                "step": 13,
                "narrative": "They are identical. This demonstrates their congruence, a direct consequence of the lines being parallel.",
                "signal_action": {"type": "Indicate", "target": "arc_top", "color": "GREEN"},
                "visual_action": {"type": "UpdateText", "target_id": "step_text", "details": "Change text to 'Step 5: The angles coincide, proving they are congruent.'"},
                "duration": 7.392,
                "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_12.mp3"
            }
        ]

        # First, add title and step_text (they are static throughout)
        self.play(Write(title))
        self.play(Write(step_text))
        self.wait(0.5)

        for step in sequence:
            step_num = step["step"]
            # Audio
            audio_file = None
            if "audio_path" in step and step["audio_path"]:
                audio_file = step["audio_path"]
            else:
                # Fallback (not needed here as all steps have audio_path)
                pass
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)

            # Signal Action
            if step.get("signal_action") is not None:
                signal = step["signal_action"]
                target_obj = self.objects[signal["target"]]
                color = eval(signal.get("color", "YELLOW"))
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))

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
            elif action_type == "UpdateText":
                # Create new text with updated content
                new_content = visual["details"].split("'")[1]  # Extract text from details
                new_text = Text(new_content, font_size=24, color=LIGHT_GRAY)
                # Position it at the same place as old step_text
                new_text.move_to(self.objects["step_text"].get_center())
                self.play(ReplacementTransform(self.objects["step_text"], new_text))
                self.objects["step_text"] = new_text
            elif action_type == "Transform":
                # Transform arc_top to arc_bottom's position and orientation
                # We'll create a copy of arc_bottom as the target for the transform
                target_arc = Arc(radius=0.4, angle=30*DEGREES, start_angle=180*DEGREES, color=GREEN, stroke_width=6)
                target_arc.move_to(arc_bottom.get_center())
                # We need to match the orientation. Since both arcs have same start_angle and angle, they are already oriented the same way.
                # Use Transform for smooth movement.
                self.play(Transform(self.objects["arc_top"], target_arc))

            # Wait for remaining duration
            # Estimate animation run_time: Create/Write/Transform typically 1 second, Circumscribe/Indicate 1 second.
            # We'll use a simple heuristic: each visual action ~1s, each signal action ~1s.
            anim_time = 0
            if step.get("signal_action") is not None:
                anim_time += 1
            if action_type in ["Create", "Write", "Transform"]:
                anim_time += 1
            elif action_type == "UpdateText":
                anim_time += 0.5  # ReplacementTransform is quick
            remaining = step["duration"] - anim_time + 0.5  # safety buffer
            if remaining > 0:
                self.wait(remaining)

        # Final pause
        self.wait(2)