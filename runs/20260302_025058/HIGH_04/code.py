'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the relationship between a parabola y = 0.5x² and its derivative y' = x, showing how the slope of the tangent line changes linearly with x.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for graph and tangent line
#    - Footer Region: [Bottom y=-3.5] for slope display and derivative equation
# 3. Anti-Overlap Check:
#    - Strategy: Keep axes and parabola in center, slope display at bottom. Use ValueTracker and always_redraw for dynamic elements to avoid manual positioning conflicts.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/To_animate_the_curve_d5d9a54042/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Create parabola, indicate it.
#    - Step 3: Create tangent point, circumscribe it.
#    - Step 4: Write derivative equation, indicate it.
#    - Step 5: Animate point moving from x=-3 to x=3, with tangent line and slope updating in real-time, indicate slope display.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_center = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create title
        title = Text("Tangent Line to a Parabola: y = 0.5x²", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": GRAY_C}
        )
        axes.move_to(content_center)
        self.objects["axes"] = axes

        # Create parabola (static, will be drawn)
        parabola = axes.plot(lambda x: 0.5 * x**2, color=BLUE, stroke_width=3)
        parabola.move_to(content_center)
        self.objects["parabola"] = parabola

        # Create tangent point (initial position at x=0)
        tangent_point = Dot(radius=0.08, color=YELLOW)
        tangent_point.move_to(axes.c2p(0, 0))
        self.objects["tangent_point"] = tangent_point

        # Create tangent line (will be updated via always_redraw)
        # Initial dummy line, will be replaced by dynamic one
        tangent_line = Line(LEFT, RIGHT, color=RED, stroke_width=3)
        tangent_line.move_to(content_center)
        self.objects["tangent_line"] = tangent_line

        # Create slope display (will be updated via always_redraw)
        slope_display = MathTex("m = 0.00", color=GREEN, font_size=32)
        slope_display.move_to(footer_center + UP * 0.5)
        self.objects["slope_display"] = slope_display

        # Create derivative equation
        derivative_eq = MathTex("y' = x", color=ORANGE, font_size=28)
        derivative_eq.next_to(slope_display, DOWN, buff=0.5)
        self.objects["derivative_eq"] = derivative_eq

        # ValueTracker for x-coordinate of tangency
        x_tracker = ValueTracker(0.0)

        # Dynamic updaters for tangent line and slope display
        def update_tangent_line():
            x = x_tracker.get_value()
            y = 0.5 * x**2
            slope = x  # derivative is x
            # Create a line segment of length 4 centered at the point
            # Direction vector is (1, slope) normalized
            length = 4.0
            direction = np.array([1, slope, 0])
            norm = np.linalg.norm(direction)
            if norm > 0:
                direction = direction / norm
            start = axes.c2p(x, y) - direction * length / 2
            end = axes.c2p(x, y) + direction * length / 2
            return Line(start, end, color=RED, stroke_width=3)

        # Always redraw tangent line
        dynamic_tangent_line = always_redraw(update_tangent_line)

        def update_slope_display():
            x = x_tracker.get_value()
            # Format to 2 decimal places
            slope_text = f"m = {x:.2f}"
            return MathTex(slope_text, color=GREEN, font_size=32).move_to(footer_center + UP * 0.5)

        # Always redraw slope display
        dynamic_slope_display = always_redraw(update_slope_display)

        def update_tangent_point():
            x = x_tracker.get_value()
            y = 0.5 * x**2
            return Dot(axes.c2p(x, y), radius=0.08, color=YELLOW)

        # Always redraw tangent point
        dynamic_tangent_point = always_redraw(update_tangent_point)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/To_animate_the_curve_d5d9a54042/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_1 = max(0.1, 6.528 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/To_animate_the_curve_d5d9a54042/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["parabola"], color=BLUE, run_time=1))
        self.play(Create(self.objects["parabola"]), run_time=3.0)
        remaining_2 = max(0.1, 6.624 - 3.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/To_animate_the_curve_d5d9a54042/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["tangent_point"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["tangent_point"]), run_time=1.5)
        remaining_3 = max(0.1, 11.808 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/To_animate_the_curve_d5d9a54042/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["derivative_eq"], color=ORANGE, run_time=1))
        self.play(Write(self.objects["derivative_eq"]), run_time=1.5)
        remaining_4 = max(0.1, 10.968 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        # Before animation, replace static objects with dynamic ones
        self.remove(self.objects["tangent_point"], self.objects["tangent_line"], self.objects["slope_display"])
        self.add(dynamic_tangent_point, dynamic_tangent_line, dynamic_slope_display)

        audio_step5 = "media/audio/To_animate_the_curve_d5d9a54042/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Indicate(dynamic_slope_display, color=GREEN, run_time=1))
        # Animate x_tracker from -3 to 3
        self.play(x_tracker.animate.set_value(3.0), run_time=8.0, rate_func=linear)
        remaining_5 = max(0.1, 11.28 - 8.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2.0))