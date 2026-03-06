'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing how to measure a 60° angle using a protractor, showing the tool's components and alignment.
# 2. Layout Strategy:
#    - Header Region: [y=3.0] for Title
#    - Main Content: [Center y=0] for angle and protractor
#    - Footer Region: [Bottom y=-3.0] for step explanations
# 3. Anti-Overlap Check:
#    - Strategy: Keep protractor components in a VGroup for easy management. Position labels (0°, 90°, 180°) outside the main arc.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1: Show vertex and initial ray.
#    - Step 2: Draw terminal ray to form 60° angle.
#    - Step 3: Fade in protractor baseline and draw its arc.
#    - Step 4: Animate tick marks and degree labels appearing.
#    - Step 5: Highlight the measured 60° sector with a thick yellow arc.
#    - Step 6: Write the final measurement label.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"

        # ========== PHASE 1: Layout & Object Creation ==========
        # Create anchors
        vertex = ORIGIN
        title_anchor = 3.0 * UP
        explanation_anchor = 3.0 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan
        # title
        title = Text("Measuring a 60° Angle with a Protractor", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # ray_initial
        ray_initial = Line(start=[0, 0, 0], end=[3.5, 0, 0], color=GREEN, stroke_width=4)
        self.objects["ray_initial"] = ray_initial

        # ray_terminal
        # Endpoint for 60°: [r*cos(60°), r*sin(60°), 0] with r=3.5
        ray_terminal = Line(start=[0, 0, 0], end=[1.75, 3.031, 0], color=GREEN, stroke_width=4)
        self.objects["ray_terminal"] = ray_terminal

        # vertex_dot
        vertex_dot = Dot(radius=0.08, color=GREEN)
        vertex_dot.move_to(vertex)
        self.objects["vertex_dot"] = vertex_dot

        # protractor_arc
        protractor_arc = Arc(radius=3.0, angle=180 * DEGREES, start_angle=0, color=GRAY_C, stroke_width=3)
        protractor_arc.move_to(vertex)
        self.objects["protractor_arc"] = protractor_arc

        # protractor_baseline
        protractor_baseline = DashedLine(start=[-3.0, 0, 0], end=[3.0, 0, 0], color=GRAY_C, stroke_width=2, stroke_opacity=0.7)
        protractor_baseline.move_to(vertex)
        self.objects["protractor_baseline"] = protractor_baseline

        # angle_arc_indicator
        angle_arc_indicator = Arc(radius=2.2, angle=60 * DEGREES, start_angle=0, color=YELLOW, stroke_width=6)
        angle_arc_indicator.move_to(vertex)
        self.objects["angle_arc_indicator"] = angle_arc_indicator

        # measurement_label
        measurement_label = MathTex("60^\\circ", color=YELLOW, font_size=36)
        measurement_label.move_to(vertex + np.array([1.2, 0.8, 0]))
        self.objects["measurement_label"] = measurement_label

        # step_explanation
        step_explanation = Text("Step 1: We begin with a 60-degree angle.", color=GRAY_C, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # Additional objects needed for Step 4 (ticks and labels)
        # We'll create a VGroup for protractor ticks and labels
        protractor_ticks_group = VGroup()
        # Major ticks every 10 degrees
        for deg in range(0, 181, 10):
            angle_rad = deg * DEGREES
            # Tick position on the arc
            tick_start = vertex + 3.0 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            tick_end = vertex + 2.8 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            tick = Line(tick_start, tick_end, color=GRAY_C, stroke_width=2)
            protractor_ticks_group.add(tick)

            # Add labels for 0°, 90°, 180°
            if deg in [0, 90, 180]:
                label_pos = vertex + 2.5 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
                # Adjust label position slightly outward for readability
                offset = 0.3
                if deg == 0:
                    label_pos += offset * DOWN
                elif deg == 90:
                    label_pos += offset * LEFT
                elif deg == 180:
                    label_pos += offset * UP
                label = MathTex(f"{deg}^\\circ", color=GRAY_C, font_size=20)
                label.move_to(label_pos)
                protractor_ticks_group.add(label)

        self.objects["protractor_ticks_group"] = protractor_ticks_group

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Draw_a_60_degree_ang_0918435ba9/step_00.mp3")  # [auto-injected] duration=6.29s
        _audio_dur_0 = 6.29  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Write(self.objects["step_explanation"]), run_time=1.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration  # duration=2.0, anim=2.0
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Draw_a_60_degree_ang_0918435ba9/step_01.mp3")  # [auto-injected] duration=6.31s
        _audio_dur_1 = 6.31  # [audio-sync] actual TTS duration
        # Step 2
        new_explanation = Text("Step 2: The second ray completes the 60° angle.", color=GRAY_C, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation), run_time=0.5)
        self.objects["step_explanation"] = new_explanation
        self.play(Create(self.objects["ray_terminal"]), run_time=1.5)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration  # duration=2.5, anim=2.0
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Draw_a_60_degree_ang_0918435ba9/step_02.mp3")  # [auto-injected] duration=11.45s
        _audio_dur_2 = 11.45  # [audio-sync] actual TTS duration
        # Step 3
        new_explanation = Text("Step 3: Align the protractor's center and baseline.", color=GRAY_C, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation), run_time=0.5)
        self.objects["step_explanation"] = new_explanation
        self.play(FadeIn(self.objects["protractor_baseline"]), run_time=1.0)
        self.play(Create(self.objects["protractor_arc"]), run_time=1.5)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration  # duration=3.0, anim=2.0
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Draw_a_60_degree_ang_0918435ba9/step_03.mp3")  # [auto-injected] duration=11.14s
        _audio_dur_3 = 11.14  # [audio-sync] actual TTS duration
        # Step 4
        new_explanation = Text("Step 4: The protractor is marked with degrees.", color=GRAY_C, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation), run_time=0.5)
        self.objects["step_explanation"] = new_explanation
        # Animate ticks and labels appearing in sequence
        self.play(LaggedStart(*[Create(tick) for tick in self.objects["protractor_ticks_group"]], lag_ratio=0.05), run_time=3.0)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration  # duration=4.0, anim=3.5
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Draw_a_60_degree_ang_0918435ba9/step_04.mp3")  # [auto-injected] duration=8.23s
        _audio_dur_4 = 8.23  # [audio-sync] actual TTS duration
        # Step 5
        new_explanation = Text("Step 5: The arc between the rays measures 60 degrees.", color=GRAY_C, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation), run_time=0.5)
        self.objects["step_explanation"] = new_explanation
        self.play(Create(self.objects["angle_arc_indicator"]), run_time=2.0)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration  # duration=3.0, anim=2.5
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Draw_a_60_degree_ang_0918435ba9/step_05.mp3")  # [auto-injected] duration=3.89s
        _audio_dur_5 = 3.89  # [audio-sync] actual TTS duration
        # Step 6
        new_explanation = Text("Step 6: Therefore, the angle measures 60 degrees.", color=GRAY_C, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation), run_time=0.5)
        self.objects["step_explanation"] = new_explanation
        self.play(Write(self.objects["measurement_label"]), run_time=1.5)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration  # duration=2.0, anim=2.0
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))