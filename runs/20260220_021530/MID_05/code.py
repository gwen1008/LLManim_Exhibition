'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually derive π by unrolling a circle's circumference and comparing it to its diameter.
# 2. Layout Strategy: Use LayoutEngine for three zones.
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for circle and unrolling action, [y=-2.5] for unrolled line and comparison.
#    - Footer Region: [Bottom y=-3.5] for final formula.
# 3. Anti-Overlap Check: Use LayoutEngine zones to keep title, main content, and footer separated. Group diameter copies into a VGroup for alignment.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_XX.mp3"
# 5. Animation Flow: Show circle → highlight diameter → unroll circumference → label it → compare with 3 diameters + remainder → reveal C = πD.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create all objects as defined in layout_plan
        self.objects = {}

        # Create objects from layout_plan.objects
        # title
        title = Text("Unrolling a Circle to Discover π", color=WHITE, font_size=40)
        self.objects["title"] = title

        # circle
        circle = Circle(radius=2.0, color=BLUE, stroke_width=4)
        self.objects["circle"] = circle

        # diameter_line
        diameter_line = Line(start=[-2, 0, 0], end=[2, 0, 0], color=RED, stroke_width=6)
        self.objects["diameter_line"] = diameter_line

        # label_diameter
        label_diameter = MathTex("D", color=RED)
        self.objects["label_diameter"] = label_diameter

        # circumference_arc
        circumference_arc = Arc(radius=2.0, start_angle=0, angle=2*PI, color=GREEN, stroke_width=4)
        self.objects["circumference_arc"] = circumference_arc

        # unrolled_line
        unrolled_line = Line(start=[-2, -2.5, 0], end=[10.566, -2.5, 0], color=GREEN, stroke_width=4, stroke_opacity=0.0)
        self.objects["unrolled_line"] = unrolled_line

        # label_circumference
        label_circumference = MathTex("C", color=GREEN, opacity=0.0)
        self.objects["label_circumference"] = label_circumference

        # d_copy1
        d_copy1 = Line(start=[-2, -1.5, 0], end=[2, -1.5, 0], color=RED, stroke_width=4, stroke_opacity=0.0)
        self.objects["d_copy1"] = d_copy1

        # d_copy2
        d_copy2 = Line(start=[2, -1.5, 0], end=[6, -1.5, 0], color=RED, stroke_width=4, stroke_opacity=0.0)
        self.objects["d_copy2"] = d_copy2

        # d_copy3
        d_copy3 = Line(start=[6, -1.5, 0], end=[10, -1.5, 0], color=RED, stroke_width=4, stroke_opacity=0.0)
        self.objects["d_copy3"] = d_copy3

        # d_remainder
        d_remainder = Line(start=[10, -1.5, 0], end=[10.566, -1.5, 0], color=YELLOW, stroke_width=4, stroke_opacity=0.0)
        self.objects["d_remainder"] = d_remainder

        # label_pi_relation
        label_pi_relation = MathTex("C = \\pi D", color=WHITE, font_size=36, opacity=0.0)
        self.objects["label_pi_relation"] = label_pi_relation

        # Initialize Layout Engine
        layout = LayoutEngine()

        # Register objects with layout
        obj_title = LayoutObject(title, "title")
        obj_circle = LayoutObject(circle, "circle")
        obj_diameter_line = LayoutObject(diameter_line, "diameter_line")
        obj_label_diameter = LayoutObject(label_diameter, "label_diameter")
        obj_circumference_arc = LayoutObject(circumference_arc, "circumference_arc")
        obj_unrolled_line = LayoutObject(unrolled_line, "unrolled_line")
        obj_label_circumference = LayoutObject(label_circumference, "label_circumference")
        obj_d_copy1 = LayoutObject(d_copy1, "d_copy1")
        obj_d_copy2 = LayoutObject(d_copy2, "d_copy2")
        obj_d_copy3 = LayoutObject(d_copy3, "d_copy3")
        obj_d_remainder = LayoutObject(d_remainder, "d_remainder")
        obj_label_pi_relation = LayoutObject(label_pi_relation, "label_pi_relation")

        layout.add(obj_title)
        layout.add(obj_circle)
        layout.add(obj_diameter_line)
        layout.add(obj_label_diameter)
        layout.add(obj_circumference_arc)
        layout.add(obj_unrolled_line)
        layout.add(obj_label_circumference)
        layout.add(obj_d_copy1)
        layout.add(obj_d_copy2)
        layout.add(obj_d_copy3)
        layout.add(obj_d_remainder)
        layout.add(obj_label_pi_relation)

        # Assign zones
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_to_zone(obj_circle, "CONTENT")
        layout.add_to_zone(obj_diameter_line, "CONTENT")
        layout.add_to_zone(obj_label_diameter, "CONTENT")
        layout.add_to_zone(obj_circumference_arc, "CONTENT")
        layout.add_to_zone(obj_unrolled_line, "CONTENT")
        layout.add_to_zone(obj_label_circumference, "CONTENT")
        layout.add_to_zone(obj_d_copy1, "CONTENT")
        layout.add_to_zone(obj_d_copy2, "CONTENT")
        layout.add_to_zone(obj_d_copy3, "CONTENT")
        layout.add_to_zone(obj_d_remainder, "CONTENT")
        layout.add_to_zone(obj_label_pi_relation, "FOOTER")

        # Center main content horizontally
        layout.add_constraint(obj_circle.center_x == 0)
        layout.add_constraint(obj_unrolled_line.center_x == 0)

        # Align label_diameter next to diameter_line
        layout.align_to(obj_label_diameter, obj_diameter_line, 'UP', buff=0.2)
        layout.add_constraint(obj_label_diameter.center_x == obj_diameter_line.center_x)

        # Align label_circumference next to unrolled_line
        layout.align_to(obj_label_circumference, obj_unrolled_line, 'UP', buff=0.2)
        layout.add_constraint(obj_label_circumference.center_x == obj_unrolled_line.center_x)

        # Align diameter copies above unrolled_line
        layout.align_to(obj_d_copy1, obj_unrolled_line, 'UP', buff=1.0)
        layout.align_to(obj_d_copy2, obj_d_copy1, 'RIGHT', buff=0)
        layout.align_to(obj_d_copy3, obj_d_copy2, 'RIGHT', buff=0)
        layout.align_to(obj_d_remainder, obj_d_copy3, 'RIGHT', buff=0)

        # Solve layout
        layout.solve()

        # Apply positions to mobjects (layout.solve() already updates LayoutObjects, but we ensure)
        # The positions are applied via LayoutObject's internal mobject.

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We start with a circle. Its diameter, the distance across through the center, is D.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "circle", "details": "Draw the blue circle."},
                "duration": 6.36,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Let's highlight its diameter.",
                "signal_action": {"type": "Indicate", "target": "diameter_line", "color": "RED"},
                "visual_action": {"type": "Create", "target_id": "diameter_line", "details": "Draw the red diameter line and its label."},
                "duration": 2.448,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, imagine cutting the circle's boundary and unrolling it into a straight line. This line is the circumference, C.",
                "signal_action": {"type": "Circumscribe", "target": "circumference_arc", "color": "YELLOW"},
                "visual_action": {"type": "Transform", "target_id": "circumference_arc", "details": "Transform the green Arc (the circle's edge) into the green unrolled_line. This is the core unrolling animation."},
                "duration": 8.28,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "How does this length C compare to the diameter D? Let's measure C using D as our ruler.",
                "signal_action": {"type": "Indicate", "target": "unrolled_line", "color": "GREEN"},
                "visual_action": {"type": "FadeIn", "target_id": "label_circumference", "details": "Fade in the label 'C' above the unrolled line."},
                "duration": 6.504,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "We place one diameter... then a second... and a third along the line.",
                "signal_action": None,
                "visual_action": {"type": "AnimationGroup", "target_id": ["d_copy1", "d_copy2", "d_copy3"], "details": "Animate the three red diameter copies fading in sequentially, aligned end-to-end above the green line."},
                "duration": 4.44,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "Three diameters almost reach the end, but a small remainder is left. This remainder is key.",
                "signal_action": {"type": "Indicate", "target": "d_remainder", "color": "YELLOW"},
                "visual_action": {"type": "FadeIn", "target_id": "d_remainder", "details": "Fade in the yellow remainder segment."},
                "duration": 7.056,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "The circumference C is equal to three diameters plus this remainder. The ratio of C to D is a fundamental constant, which we call Pi.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_pi_relation", "details": "Write the final formula 'C = πD' at the bottom of the screen."},
                "duration": 9.192,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_06.mp3"
            }
        ]

        # Step 1
        step = sequence[0]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["title"]))
        self.play(Create(self.objects["circle"]))
        animation_time = 2.0  # Approximate runtime for Write + Create
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)

        # Step 2
        step = sequence[1]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        self.play(Create(self.objects["diameter_line"]), Write(self.objects["label_diameter"]))
        animation_time = 1.5  # Indicate + Create + Write
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)

        # Step 3
        step = sequence[2]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        # Create the circumference_arc (initially invisible, but we need it for Transform)
        self.add(self.objects["circumference_arc"])
        self.objects["circumference_arc"].set_opacity(1)
        self.objects["unrolled_line"].set_opacity(1)
        self.play(Transform(self.objects["circumference_arc"], self.objects["unrolled_line"]))
        animation_time = 2.0  # Circumscribe + Transform
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)

        # Step 4
        step = sequence[3]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        self.objects["label_circumference"].set_opacity(1)
        self.play(FadeIn(self.objects["label_circumference"]))
        animation_time = 1.5  # Indicate + FadeIn
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)

        # Step 5
        step = sequence[4]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.objects["d_copy1"].set_opacity(1)
        self.objects["d_copy2"].set_opacity(1)
        self.objects["d_copy3"].set_opacity(1)
        self.play(
            FadeIn(self.objects["d_copy1"]),
            FadeIn(self.objects["d_copy2"]),
            FadeIn(self.objects["d_copy3"])
        )
        animation_time = 1.5  # FadeIn three objects
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)

        # Step 6
        step = sequence[5]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        self.objects["d_remainder"].set_opacity(1)
        self.play(FadeIn(self.objects["d_remainder"]))
        animation_time = 1.5  # Indicate + FadeIn
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)

        # Step 7
        step = sequence[6]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.objects["label_pi_relation"].set_opacity(1)
        self.play(Write(self.objects["label_pi_relation"]))
        animation_time = 1.5  # Write
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)

        # Final wait
        self.wait(2)