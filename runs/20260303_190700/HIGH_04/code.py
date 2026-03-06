'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the derivative of y = 0.5x² as the slope of the tangent line at each point.
# 2. Layout Strategy: Split-screen layout.
#    - Header Region: [y=3.0] for Title and Step Label.
#    - Main Content: Left side for graph (centered at ORIGIN), right side for slope display (x=4).
#    - Footer Region: [Bottom y=-2.5] for explanation text.
# 3. Anti-Overlap Check:
#    - Graph and slope display are separated horizontally.
#    - Step label is placed directly under title.
#    - Use VGroups for slope display area.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/derivative_slope_tangent/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Draw parabola.
#    - Step 3: Show derivative equation.
#    - Step 4: Show sample point.
#    - Step 5: Introduce moving tangent concept.
#    - Step 6: Animate point moving, updating tangent and slope.
'''

from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_a_Manim_anima_9b876d8ef6/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout plan zones
        header_center = 3.0 * UP
        graph_center = ORIGIN
        slope_display_anchor = 4 * RIGHT
        footer_center = 2.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Derivative as Slope of Tangent Line", color=WHITE, font_size=36)
        title.move_to(header_center)
        self.objects["title"] = title

        # step_label
        step_label = Text("Step 1: The Parabola y = 0.5x²", color=YELLOW, font_size=24)
        step_label.next_to(title, DOWN, buff=0.3)
        self.objects["step_label"] = step_label

        # axes
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-1, 5, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": GRAY_C}
        )
        axes.move_to(graph_center)
        self.objects["axes"] = axes

        # parabola
        parabola = axes.plot(lambda x: 0.5 * x**2, color=YELLOW, stroke_width=4)
        self.objects["parabola"] = parabola

        # moving_point (initial position at x=-3, y=4.5)
        moving_point = Dot(radius=0.08, color=WHITE, fill_opacity=1.0)
        moving_point.move_to(axes.c2p(-3, 4.5))
        self.objects["moving_point"] = moving_point

        # tangent_line (placeholder, will be replaced by always_redraw)
        tangent_line = Line(LEFT, RIGHT, color=RED, stroke_width=3)
        tangent_line.move_to(graph_center)
        self.objects["tangent_line"] = tangent_line

        # slope_label
        slope_label = Text("Slope at point:", color=GRAY_C, font_size=28)
        slope_label.move_to(slope_display_anchor + UP * 1.5)
        self.objects["slope_label"] = slope_label

        # slope_value
        slope_value = DecimalNumber(0.00, color=GREEN, font_size=36, num_decimal_places=2)
        slope_value.next_to(slope_label, DOWN, buff=0.5)
        self.objects["slope_value"] = slope_value

        # derivative_eq
        derivative_eq = MathTex(r"y' = x", color=BLUE, font_size=32)
        derivative_eq.next_to(slope_value, DOWN, buff=0.8)
        self.objects["derivative_eq"] = derivative_eq

        # explanation
        explanation = Text("The derivative gives the slope at each point", color=GRAY_C, font_size=24)
        explanation.move_to(footer_center)
        self.objects["explanation"] = explanation

        # ValueTracker for moving x-coordinate
        x_tracker = ValueTracker(-3.0)
        self.x_tracker = x_tracker

        # Dynamic tangent line and slope value using always_redraw
        def update_tangent_line():
            x = x_tracker.get_value()
            y = 0.5 * x**2
            point = axes.c2p(x, y)
            # Slope is derivative: x
            slope = x
            # Create a tangent line segment of length 2 total (1 unit each direction)
            # Direction vector: (1, slope)
            dir_vec = np.array([1, slope, 0])
            dir_vec = dir_vec / np.linalg.norm(dir_vec)  # normalize
            start = point - dir_vec
            end = point + dir_vec
            return Line(start, end, color=RED, stroke_width=3)

        dynamic_tangent = always_redraw(update_tangent_line)

        def update_slope_value():
            x = x_tracker.get_value()
            return DecimalNumber(x, color=GREEN, font_size=36, num_decimal_places=2).move_to(slope_value.get_center())

        dynamic_slope_value = always_redraw(update_slope_value)

        def update_moving_point():
            x = x_tracker.get_value()
            y = 0.5 * x**2
            return Dot(axes.c2p(x, y), radius=0.08, color=WHITE, fill_opacity=1.0)

        dynamic_moving_point = always_redraw(update_moving_point)

        # We'll replace the static objects with dynamic ones later
        # For now, store the dynamic versions
        self.dynamic_tangent = dynamic_tangent
        self.dynamic_slope_value = dynamic_slope_value
        self.dynamic_moving_point = dynamic_moving_point

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/derivative_slope_tangent/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["parabola"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["axes"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/derivative_slope_tangent/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Create(self.objects["parabola"]), run_time=2.5)
        remaining_2 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/derivative_slope_tangent/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["derivative_eq"], color=BLUE, run_time=1))
        step_label2 = Text("Step 2: The Derivative y' = x", color=YELLOW, font_size=24)
        step_label2.next_to(self.objects["title"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label2))
        self.objects["step_label"] = step_label2
        remaining_3 = max(0.1, 4.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/derivative_slope_tangent/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["moving_point"], color=WHITE, run_time=1))
        self.play(Create(self.objects["moving_point"]), run_time=1.5)
        # Also create slope display area
        self.play(Write(self.objects["slope_label"]), Write(self.objects["slope_value"]), Write(self.objects["derivative_eq"]), Write(self.objects["explanation"]), run_time=2.0)
        remaining_4 = max(0.1, 5.0 - (1.0 + 1.5 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/derivative_slope_tangent/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["slope_value"], color=GREEN, run_time=1))
        step_label3 = Text("Step 3: Moving Tangent Line", color=YELLOW, font_size=24)
        step_label3.next_to(self.objects["title"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label3))
        self.objects["step_label"] = step_label3
        # Replace static objects with dynamic ones
        self.remove(self.objects["moving_point"], self.objects["tangent_line"], self.objects["slope_value"])
        self.add(self.dynamic_moving_point, self.dynamic_tangent, self.dynamic_slope_value)
        remaining_5 = max(0.1, 4.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/derivative_slope_tangent/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["derivative_eq"], color=BLUE, run_time=1))
        self.play(self.x_tracker.animate.set_value(3.0), run_time=8.0, rate_func=linear)
        remaining_6 = max(0.1, 8.0 - 8.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))