'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize slope as "rise over run" using the classic right triangle method on the graph of y = 2x - 1.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Slope: Rise over Run"
#    - Main Content: [Center y=0] for coordinate plane, line, triangle, and points.
#    - Footer Region: [Bottom y=-3.5] for explanation text and slope formula.
# 3. Anti-Overlap Check:
#    - Strategy: Use `next_to` with buff for labels. Keep triangle and labels within the axes area. The footer text is placed low to avoid the main visual.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step?
# 5. Animation Flow:
#    - Create axes and line graph.
#    - Introduce points A and B, then the segment between them.
#    - Construct the right triangle legs (run, rise) and label them.
#    - Show explanatory text and the slope formula.
#    - Finally, morph the formula to the simplified slope value.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors based on layout_plan description
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Slope: Rise over Run", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-4, 4, 1],
            axis_config={"include_numbers": True}
        ).scale(0.9).move_to(content_center)
        self.objects["axes"] = axes

        # Line Graph
        line_graph = axes.plot(lambda x: 2*x - 1, color=BLUE, stroke_width=4)
        self.objects["line_graph"] = line_graph

        # Point A (0, -1)
        point_A = Dot(axes.c2p(0, -1), color=YELLOW, radius=0.08)
        self.objects["point_A"] = point_A

        # Point B (1, 1)
        point_B = Dot(axes.c2p(1, 1), color=YELLOW, radius=0.08)
        self.objects["point_B"] = point_B

        # Segment AB
        segment_AB = Line(axes.c2p(0, -1), axes.c2p(1, 1), color=GREEN, stroke_width=6)
        self.objects["segment_AB"] = segment_AB

        # Triangle Rise (vertical leg)
        triangle_rise = Line(axes.c2p(1, -1), axes.c2p(1, 1), color=RED, stroke_width=5)
        self.objects["triangle_rise"] = triangle_rise

        # Triangle Run (horizontal leg)
        triangle_run = Line(axes.c2p(0, -1), axes.c2p(1, -1), color=GREEN, stroke_width=5)
        self.objects["triangle_run"] = triangle_run

        # Rise Label
        rise_label = MathTex(r"\Delta y = 2", color=RED)
        rise_label.next_to(triangle_rise, RIGHT, buff=0.2)
        self.objects["rise_label"] = rise_label

        # Run Label
        run_label = MathTex(r"\Delta x = 1", color=GREEN)
        run_label.next_to(triangle_run, DOWN, buff=0.2)
        self.objects["run_label"] = run_label

        # Step Explanation (Footer text)
        step_explanation = Text(
            "The slope is the ratio of the vertical change to the horizontal change.",
            color=GRAY_C, font_size=24
        )
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # Slope Equation
        slope_equation = Tex(r'Slope $= \frac{\Delta y}{\Delta x} = \frac{2}{1}$', color=WHITE, font_size=32)
        slope_equation.next_to(step_explanation, DOWN, buff=0.5)
        self.objects["slope_equation"] = slope_equation

        # Slope Simplified (will be positioned later)
        slope_simplified = Tex(r'Slope $= 2$', color=YELLOW, font_size=32)
        # Position it at the same center as slope_equation for smooth transform
        slope_simplified.move_to(slope_equation.get_center())
        self.objects["slope_simplified"] = slope_simplified

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_an_animation__54a57dd5a9/step_00.mp3")  # [auto-injected] duration=4.82s
        _audio_dur_0 = 4.82  # [audio-sync] actual TTS duration
        # Step 1: Create axes
        self.play(Create(axes), run_time=2.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_an_animation__54a57dd5a9/step_01.mp3")  # [auto-injected] duration=6.14s
        _audio_dur_1 = 6.14  # [audio-sync] actual TTS duration
        # Step 2: Create line graph
        self.play(Create(line_graph), run_time=3.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_an_animation__54a57dd5a9/step_02.mp3")  # [auto-injected] duration=9.29s
        _audio_dur_2 = 9.29  # [audio-sync] actual TTS duration
        # Step 3: Indicate line, then create point A
        self.play(Indicate(line_graph, color=YELLOW, run_time=1))
        self.play(Create(point_A), run_time=2.0)  # Adjusted anim time for step 3
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_an_animation__54a57dd5a9/step_03.mp3")  # [auto-injected] duration=5.69s
        _audio_dur_3 = 5.69  # [audio-sync] actual TTS duration
        # Step 4: Indicate point A, then create point B and segment AB
        self.play(Indicate(point_A, color=YELLOW, run_time=1))
        self.play(Create(point_B), Create(segment_AB), run_time=2.0)  # Combined anim
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_an_animation__54a57dd5a9/step_04.mp3")  # [auto-injected] duration=6.74s
        _audio_dur_4 = 6.74  # [audio-sync] actual TTS duration
        # Step 5: Circumscribe point A, then create triangle run
        self.play(Circumscribe(point_A, color=GREEN, run_time=1))
        self.play(Create(triangle_run), run_time=1.5)  # Adjusted anim time
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_an_animation__54a57dd5a9/step_05.mp3")  # [auto-injected] duration=3.79s
        _audio_dur_5 = 3.79  # [audio-sync] actual TTS duration
        # Step 6: Circumscribe point B, then create triangle rise
        self.play(Circumscribe(point_B, color=RED, run_time=1))
        self.play(Create(triangle_rise), run_time=1.5)  # Adjusted anim time
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Create_an_animation__54a57dd5a9/step_06.mp3")  # [auto-injected] duration=6.22s
        _audio_dur_6 = 6.22  # [audio-sync] actual TTS duration
        # Step 7: Indicate triangle run, then write run label
        self.play(Indicate(triangle_run, color=GREEN, run_time=1))
        self.play(Write(run_label), run_time=1.0)  # Adjusted anim time
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Create_an_animation__54a57dd5a9/step_07.mp3")  # [auto-injected] duration=4.61s
        _audio_dur_7 = 4.61  # [audio-sync] actual TTS duration
        # Step 8: Indicate triangle rise, then write rise label
        self.play(Indicate(triangle_rise, color=RED, run_time=1))
        self.play(Write(rise_label), run_time=1.0)  # Adjusted anim time
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Create_an_animation__54a57dd5a9/step_08.mp3")  # [auto-injected] duration=5.62s
        _audio_dur_8 = 5.62  # [audio-sync] actual TTS duration
        # Step 9: Write step explanation
        self.play(Write(step_explanation), run_time=2.5)
        remaining_9 = _audio_dur_8  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/Create_an_animation__54a57dd5a9/step_09.mp3")  # [auto-injected] duration=6.94s
        _audio_dur_9 = 6.94  # [audio-sync] actual TTS duration
        # Step 10: Write slope equation
        self.play(Write(slope_equation), run_time=3.0)
        remaining_10 = _audio_dur_9  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_10))

        self.add_sound("media/audio/Create_an_animation__54a57dd5a9/step_10.mp3")  # [auto-injected] duration=6.86s
        _audio_dur_10 = 6.86  # [audio-sync] actual TTS duration
        # Step 11: Indicate segment AB, then transform slope equation to simplified
        self.play(Indicate(segment_AB, color=YELLOW, run_time=1))
        self.play(TransformMatchingTex(slope_equation, slope_simplified), run_time=2.0)  # Adjusted anim time
        remaining_11 = _audio_dur_10  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_11))