'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the process of measuring a 60-degree angle using a protractor, linking geometric construction to numerical measurement.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for angle, vertex, protractor, and measurement arc.
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text.
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroup for protractor scale ticks. Position measurement arc with a slightly smaller radius (2.2) than the protractor (2.5) to ensure visibility. Keep explanation text at the bottom, clear of main graphics.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1-3: Draw the 60-degree angle (vertex, baseline ray, 60-degree ray).
#    - Step 4-5: Introduce the protractor (semicircle, scale ticks), emphasizing alignment.
#    - Step 6-7: Animate the measurement arc sweeping from 0 to 60 degrees and label it.
#    - Step 8: Final conclusion, highlighting the 60° label.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"

        # ========== PHASE 1: Layout & Object Creation ==========
        # Initialize layout engine
        layout = LayoutEngine()

        # Create anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        self.objects = {}

        # scene_title
        scene_title = Text("Measuring a 60-Degree Angle", color=WHITE, font_size=40)
        scene_title.move_to(title_anchor)
        self.objects["scene_title"] = scene_title
        layout.add(LayoutObject(scene_title, "scene_title"))
        layout.add_to_zone(layout.get("scene_title"), "HEADER")
        layout.add_constraint(layout.get("scene_title").center_x == 0)

        # vertex_V
        vertex_V = Dot(radius=0.08, color=YELLOW)
        vertex_V.move_to(content_center)
        self.objects["vertex_V"] = vertex_V
        layout.add(LayoutObject(vertex_V, "vertex_V"))
        layout.add_to_zone(layout.get("vertex_V"), "CONTENT")
        layout.add_constraint(layout.get("vertex_V").center_x == 0)
        layout.add_constraint(layout.get("vertex_V").center_y == 0)

        # ray_baseline
        ray_baseline = Line(start=ORIGIN, end=3*RIGHT, color=BLUE, stroke_width=4)
        ray_baseline.move_to(content_center)
        self.objects["ray_baseline"] = ray_baseline
        layout.add(LayoutObject(ray_baseline, "ray_baseline"))
        layout.add_to_zone(layout.get("ray_baseline"), "CONTENT")
        layout.align_to(layout.get("ray_baseline"), layout.get("vertex_V"), 'CENTER')

        # ray_60deg
        # Endpoint calculated for 60 degrees: (cos(60°)*1.5, sin(60°)*1.5) = (0.75, 1.299), scaled by 2 for length ~3
        ray_60deg = Line(start=ORIGIN, end=1.5*RIGHT + 2.598076211*UP, color=GREEN, stroke_width=4)
        ray_60deg.move_to(content_center)
        self.objects["ray_60deg"] = ray_60deg
        layout.add(LayoutObject(ray_60deg, "ray_60deg"))
        layout.add_to_zone(layout.get("ray_60deg"), "CONTENT")
        layout.align_to(layout.get("ray_60deg"), layout.get("vertex_V"), 'CENTER')

        # protractor_semicircle
        protractor_semicircle = Arc(radius=2.5, angle=PI, start_angle=0, color=GRAY_C, stroke_width=3, fill_opacity=0.1)
        protractor_semicircle.move_to(content_center)
        self.objects["protractor_semicircle"] = protractor_semicircle
        layout.add(LayoutObject(protractor_semicircle, "protractor_semicircle"))
        layout.add_to_zone(layout.get("protractor_semicircle"), "CONTENT")
        layout.align_to(layout.get("protractor_semicircle"), layout.get("vertex_V"), 'CENTER')

        # protractor_scale_ticks (VGroup to be populated)
        protractor_scale_ticks = VGroup()
        # Create tick marks and labels for 0, 30, 60, 90, 120, 150, 180 degrees
        tick_radius = 2.5
        label_radius = 2.7
        for angle_deg in [0, 30, 60, 90, 120, 150, 180]:
            angle_rad = angle_deg * DEGREES
            # Outer tick
            start_point = tick_radius * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            end_point = (tick_radius - 0.2) * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            tick = Line(start=start_point, end=end_point, color=WHITE, stroke_width=2)
            # Label
            if angle_deg == 0:
                label_text = MathTex("0^\\circ", font_size=20, color=WHITE)
            elif angle_deg == 180:
                label_text = MathTex("180^\\circ", font_size=20, color=WHITE)
            else:
                label_text = MathTex(f"{angle_deg}^\\circ", font_size=20, color=WHITE)
            label_text.move_to(label_radius * np.array([np.cos(angle_rad), np.sin(angle_rad), 0]))
            protractor_scale_ticks.add(tick, label_text)
        protractor_scale_ticks.move_to(content_center)
        self.objects["protractor_scale_ticks"] = protractor_scale_ticks
        layout.add(LayoutObject(protractor_scale_ticks, "protractor_scale_ticks"))
        layout.add_to_zone(layout.get("protractor_scale_ticks"), "CONTENT")
        layout.align_to(layout.get("protractor_scale_ticks"), layout.get("vertex_V"), 'CENTER')

        # measurement_arc
        measurement_arc = Arc(radius=2.2, angle=PI/3, start_angle=0, color=RED, stroke_width=6)
        measurement_arc.move_to(content_center)
        self.objects["measurement_arc"] = measurement_arc
        layout.add(LayoutObject(measurement_arc, "measurement_arc"))
        layout.add_to_zone(layout.get("measurement_arc"), "CONTENT")
        layout.align_to(layout.get("measurement_arc"), layout.get("vertex_V"), 'CENTER')

        # measurement_label
        measurement_label = MathTex("60^\\circ", color=RED, font_size=36)
        measurement_label.move_to(content_center + 1.2*RIGHT + 1.2*UP)
        self.objects["measurement_label"] = measurement_label
        layout.add(LayoutObject(measurement_label, "measurement_label"))
        layout.add_to_zone(layout.get("measurement_label"), "CONTENT")

        # step_explanation (dynamic text, will be updated)
        step_explanation = Text("Step 1: Draw the angle to be measured.", color=WHITE, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        layout.add(LayoutObject(step_explanation, "step_explanation"))
        layout.add_to_zone(layout.get("step_explanation"), "FOOTER")
        layout.add_constraint(layout.get("step_explanation").center_x == 0)

        # Solve layout constraints
        layout.solve()

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_00.mp3")  # [auto-injected] duration=5.83s
        _audio_dur_0 = 5.83  # [audio-sync] actual TTS duration
        # Step 1
        self.objects["step_explanation"].become(Text("Step 1: Draw the angle to be measured.", color=WHITE, font_size=24))
        self.objects["step_explanation"].move_to(explanation_anchor)
        self.play(Indicate(self.objects["vertex_V"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["vertex_V"]), run_time=1.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_01.mp3")  # [auto-injected] duration=2.71s
        _audio_dur_1 = 2.71  # [audio-sync] actual TTS duration
        # Step 2
        self.objects["step_explanation"].become(Text("Step 2: Draw the baseline ray.", color=WHITE, font_size=24))
        self.objects["step_explanation"].move_to(explanation_anchor)
        self.play(Create(self.objects["ray_baseline"]), run_time=1.5)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_02.mp3")  # [auto-injected] duration=5.66s
        _audio_dur_2 = 5.66  # [audio-sync] actual TTS duration
        # Step 3
        self.objects["step_explanation"].become(Text("Step 3: Draw the second ray at 60 degrees.", color=WHITE, font_size=24))
        self.objects["step_explanation"].move_to(explanation_anchor)
        self.play(Create(self.objects["ray_60deg"]), run_time=2.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_03.mp3")  # [auto-injected] duration=8.09s
        _audio_dur_3 = 8.09  # [audio-sync] actual TTS duration
        # Step 4
        self.objects["step_explanation"].become(Text("Step 4: Place the protractor center on the vertex.", color=WHITE, font_size=24))
        self.objects["step_explanation"].move_to(explanation_anchor)
        self.play(Circumscribe(self.objects["vertex_V"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["protractor_semicircle"]), run_time=3.0)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_04.mp3")  # [auto-injected] duration=7.34s
        _audio_dur_4 = 7.34  # [audio-sync] actual TTS duration
        # Step 5
        self.objects["step_explanation"].become(Text("Step 5: Align the protractor's 0° mark with the baseline.", color=WHITE, font_size=24))
        self.objects["step_explanation"].move_to(explanation_anchor)
        self.play(Indicate(self.objects["ray_baseline"], color=BLUE, run_time=1))
        # Create the scale ticks, emphasizing the 0 mark
        # We'll create the VGroup but highlight the 0 tick
        zero_tick = protractor_scale_ticks[0]  # First element is the 0-degree tick line
        zero_label = protractor_scale_ticks[1] # Second element is the 0-degree label
        self.play(Create(protractor_scale_ticks), run_time=2.5)
        self.play(Indicate(zero_tick, color=YELLOW), Indicate(zero_label, color=YELLOW), run_time=0.5)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_05.mp3")  # [auto-injected] duration=8.90s
        _audio_dur_5 = 8.90  # [audio-sync] actual TTS duration
        # Step 6
        self.objects["step_explanation"].become(Text("Step 6: Sweep the arc from 0° to the second ray.", color=WHITE, font_size=24))
        self.objects["step_explanation"].move_to(explanation_anchor)
        # Animate the drawing of the measurement arc
        self.play(Create(self.objects["measurement_arc"]), run_time=3.0)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_06.mp3")  # [auto-injected] duration=4.44s
        _audio_dur_6 = 4.44  # [audio-sync] actual TTS duration
        # Step 7
        self.objects["step_explanation"].become(Text("Step 7: The arc reaches the 60° mark on the scale.", color=WHITE, font_size=24))
        self.objects["step_explanation"].move_to(explanation_anchor)
        # Indicate the 60-degree tick and label (elements 4 and 5 in the VGroup)
        sixty_tick = protractor_scale_ticks[4]
        sixty_label = protractor_scale_ticks[5]
        self.play(Indicate(sixty_tick, color=YELLOW), Indicate(sixty_label, color=YELLOW), run_time=1)
        self.play(Write(self.objects["measurement_label"]), run_time=1.5)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Draw_a_60_degree_ang_9e7aa1e1ee/step_07.mp3")  # [auto-injected] duration=3.77s
        _audio_dur_7 = 3.77  # [audio-sync] actual TTS duration
        # Step 8
        self.objects["step_explanation"].become(Text("Step 8: Therefore, the angle measures 60 degrees.", color=WHITE, font_size=24))
        self.objects["step_explanation"].move_to(explanation_anchor)
        self.play(Circumscribe(self.objects["measurement_label"], color=RED, run_time=1))
        # Ensure title is visible (it was created but not added to scene yet)
        self.play(FadeIn(self.objects["scene_title"]), run_time=1.0)
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        # Final hold
        self.wait(max(0.1, 2))