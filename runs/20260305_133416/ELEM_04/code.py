'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the construction and measurement of a 60-degree angle, first by geometric proof (equilateral triangle) then by tool (protractor).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Measuring a 60-Degree Angle"
#    - Main Content: [Center y=0] for the angle, triangle, and protractor.
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanations.
# 3. Anti-Overlap Check:
#    - Strategy: All geometric objects (rays, triangle, protractor) share the same vertex at ORIGIN. Use VGroups for protractor ticks/labels. The explanation text is placed at the bottom, away from the main diagram.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] I will assign `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step.
# 5. Animation Flow:
#    - Step 1: Draw the horizontal ray (ray1).
#    - Step 2: Draw the 60-degree ray (ray2), with an Indicate signal.
#    - Step 3: Draw the equilateral triangle sides to prove the angle, with a Circumscribe signal on the vertex.
#    - Step 4: Fade in the protractor (arc and baseline), with an Indicate signal.
#    - Step 5: Draw the red measurement arc on the protractor and show the "60°" label, with an Indicate signal.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"

        # ========== PHASE 1: Layout & Object Creation ==========
        # Create anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Helper to parse geometry_def strings (simplified for this specific JSON)
        def parse_point(point_str):
            # point_str is like "[0,0,0]" or "[1.5, 2.598, 0]"
            # Remove brackets and split
            coords = point_str.strip('[]').split(',')
            return np.array([float(c.strip()) for c in coords])

        # Create objects from layout_plan.objects
        # We'll create them in an order that makes sense for dependencies.

        # 1. Title
        title = Text("Measuring a 60-Degree Angle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # 2. Vertex (Dot at origin)
        vertex = Dot(point=ORIGIN, color=YELLOW, radius=0.08)
        self.objects["vertex"] = vertex

        # 3. Ray1 (horizontal)
        ray1 = Line(start=ORIGIN, end=3*RIGHT, color=BLUE, stroke_width=4)
        self.objects["ray1"] = ray1

        # 4. Ray2 (60 degrees)
        # Endpoint: 3*(cos60, sin60) = (1.5, 2.598...)
        ray2_end = np.array([1.5, 2.598076211, 0])
        ray2 = Line(start=ORIGIN, end=ray2_end, color=GREEN, stroke_width=4)
        self.objects["ray2"] = ray2

        # 5. Angle arc (60 degrees)
        angle_arc = Arc(radius=1.0, start_angle=0, angle=PI/3, color=YELLOW, stroke_width=6)
        self.objects["angle_arc"] = angle_arc

        # 6. Equilateral triangle sides (for proof)
        # Side1 (coincides with ray1, but shorter and semi-transparent)
        triangle_side1 = Line(start=ORIGIN, end=2*RIGHT, color=BLUE, stroke_width=4, stroke_opacity=0.5)
        self.objects["triangle_side1"] = triangle_side1
        # Side2
        side2_end = np.array([1, 1.732050808, 0])  # (cos60, sin60) * 2
        triangle_side2 = Line(start=2*RIGHT, end=side2_end, color=GREEN, stroke_width=4, stroke_opacity=0.5)
        self.objects["triangle_side2"] = triangle_side2
        # Side3 (coincides with ray2, but shorter and semi-transparent)
        triangle_side3 = Line(start=side2_end, end=ORIGIN, color=PURPLE, stroke_width=4, stroke_opacity=0.5)
        self.objects["triangle_side3"] = triangle_side3

        # 7. Protractor components
        protractor_arc = Arc(radius=2.5, start_angle=0, angle=PI, color=GRAY_C, stroke_width=3, stroke_opacity=0.7)
        self.objects["protractor_arc"] = protractor_arc

        protractor_baseline = Line(start=2.5*LEFT, end=2.5*RIGHT, color=GRAY_C, stroke_width=2, stroke_opacity=0.7)
        self.objects["protractor_baseline"] = protractor_baseline

        # Protractor ticks (every 15 degrees from 0 to 180)
        protractor_ticks = VGroup()
        for deg in range(0, 181, 15):
            rad = deg * PI / 180
            start_point = 2.5 * np.array([np.cos(rad), np.sin(rad), 0])
            end_point = 2.3 * np.array([np.cos(rad), np.sin(rad), 0])
            tick = Line(start=start_point, end=end_point, color=WHITE, stroke_width=1.5, stroke_opacity=0.8)
            protractor_ticks.add(tick)
        self.objects["protractor_ticks"] = protractor_ticks

        # Protractor labels (key angles)
        protractor_labels = VGroup()
        label_angles = [0, 30, 60, 90, 120, 150, 180]
        for deg in label_angles:
            rad = deg * PI / 180
            # Position at radius 2.7
            pos = 2.7 * np.array([np.cos(rad), np.sin(rad), 0])
            label = Text(str(deg), color=WHITE, font_size=24)
            label.move_to(pos)
            protractor_labels.add(label)
        self.objects["protractor_labels"] = protractor_labels

        # 8. Measurement arc (red, on protractor)
        measurement_arc = Arc(radius=2.2, start_angle=0, angle=PI/3, color=RED, stroke_width=8)
        self.objects["measurement_arc"] = measurement_arc

        # 9. Measurement label "60°"
        measurement_label = MathTex("60^\\circ", color=RED, font_size=36)
        # Position: move_to(content_center) + UP*1.0 + RIGHT*1.5
        measurement_label.move_to(ORIGIN + UP*1.0 + RIGHT*1.5)
        self.objects["measurement_label"] = measurement_label

        # 10. Explanation text (dynamic, will be updated per step)
        explanation_text = Text("Placeholder for step explanation.", color=WHITE, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Draw_a_60_degree_ang_d725da8b47/step_00.mp3")  # [auto-injected] duration=6.14s
        _audio_dur_0 = 6.14  # [audio-sync] actual TTS duration
        # Step 1
        # Narrative: "We begin with a 60-degree angle. One ray is placed along the horizontal axis."
        # signal_action: null
        # visual_action: Create ray1
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.wait(max(0.1, 0.5))
        self.play(Create(self.objects["ray1"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        # Update explanation text for Step 1
        new_explanation_1 = Text("We begin with a 60-degree angle. One ray is placed along the horizontal axis.", color=WHITE, font_size=28)
        new_explanation_1.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation_1))
        self.objects["explanation_text"] = new_explanation_1
        self.wait(max(0.1, 0.5))

        self.add_sound("media/audio/Draw_a_60_degree_ang_d725da8b47/step_01.mp3")  # [auto-injected] duration=12.79s
        _audio_dur_1 = 12.79  # [audio-sync] actual TTS duration
        # Step 2
        # Narrative: "The second ray is positioned such that the angle between them is exactly 60 degrees..."
        # signal_action: Indicate ray2 (GREEN)
        # visual_action: Create ray2
        self.play(Indicate(self.objects["ray2"], color=GREEN, run_time=1))
        self.play(Create(self.objects["ray2"]), run_time=2.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        new_explanation_2 = Text("The second ray is positioned at exactly 60 degrees. This angle comes from an equilateral triangle.", color=WHITE, font_size=28)
        new_explanation_2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation_2))
        self.objects["explanation_text"] = new_explanation_2
        self.wait(max(0.1, 0.5))

        self.add_sound("media/audio/Draw_a_60_degree_ang_d725da8b47/step_02.mp3")  # [auto-injected] duration=11.74s
        _audio_dur_2 = 11.74  # [audio-sync] actual TTS duration
        # Step 3
        # Narrative: "Let's verify this is 60 degrees by constructing an equilateral triangle..."
        # signal_action: Circumscribe vertex (YELLOW)
        # visual_action: Create triangle_side2 (and also side1 & side3 for completeness)
        self.play(Circumscribe(self.objects["vertex"], color=YELLOW, run_time=1))
        # Draw all three triangle sides (they are already created, just not added)
        self.play(
            Create(self.objects["triangle_side1"]),
            Create(self.objects["triangle_side2"]),
            Create(self.objects["triangle_side3"]),
            run_time=3.0
        )
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        new_explanation_3 = Text("Constructing an equilateral triangle proves the angle is 60 degrees.", color=WHITE, font_size=28)
        new_explanation_3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation_3))
        self.objects["explanation_text"] = new_explanation_3
        self.wait(max(0.1, 0.5))

        self.add_sound("media/audio/Draw_a_60_degree_ang_d725da8b47/step_03.mp3")  # [auto-injected] duration=12.00s
        _audio_dur_3 = 12.00  # [audio-sync] actual TTS duration
        # Step 4
        # Narrative: "Now, to measure the angle using a standard tool, we overlay a semicircular protractor..."
        # signal_action: Indicate protractor_arc (WHITE)
        # visual_action: Create protractor_arc (and baseline, ticks, labels)
        self.play(Indicate(self.objects["protractor_arc"], color=WHITE, run_time=1))
        # Fade in the entire protractor assembly
        self.play(
            FadeIn(self.objects["protractor_arc"]),
            FadeIn(self.objects["protractor_baseline"]),
            FadeIn(self.objects["protractor_ticks"]),
            FadeIn(self.objects["protractor_labels"]),
            run_time=2.0
        )
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        new_explanation_4 = Text("A protractor is aligned with the vertex and baseline. Its markings show degrees.", color=WHITE, font_size=28)
        new_explanation_4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation_4))
        self.objects["explanation_text"] = new_explanation_4
        self.wait(max(0.1, 0.5))

        self.add_sound("media/audio/Draw_a_60_degree_ang_d725da8b47/step_04.mp3")  # [auto-injected] duration=10.63s
        _audio_dur_4 = 10.63  # [audio-sync] actual TTS duration
        # Step 5
        # Narrative: "The protractor shows degree markings. The angle spans from the 0-degree mark to the 60-degree mark..."
        # signal_action: Indicate measurement_arc (RED)
        # visual_action: Create measurement_arc, then Write measurement_label
        self.play(Indicate(self.objects["measurement_arc"], color=RED, run_time=1))
        self.play(Create(self.objects["measurement_arc"]), run_time=2.0)
        self.play(Write(self.objects["measurement_label"]), run_time=1.0)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        new_explanation_5 = Text("The red arc spans 60 degrees on the protractor, confirming the measurement.", color=WHITE, font_size=28)
        new_explanation_5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation_5))
        self.objects["explanation_text"] = new_explanation_5

        # Final hold
        self.wait(max(0.1, 2))