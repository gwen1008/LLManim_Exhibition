'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the derivative as the slope of a tangent line on the parabola y = 0.5x^2.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title, function, and derivative labels.
#    - Main Content: [Center y=0] for axes, parabola, moving point, and tangent line.
#    - Footer Region: [Bottom y=-3.5] for slope formula and live slope value.
# 3. Anti-Overlap Check:
#    - Strategy: Use distinct zones. Keep title/func_label/deriv_label in header, axes/parabola in center, slope labels in footer.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/derivative_slope_tangent/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Draw parabola, write title, function, derivative labels.
#    - Step 3: Create moving dot and tangent line at initial point.
#    - Step 4: Write slope formula and dynamic slope value in footer.
#    - Step 5: Animate dot moving from x=-3 to 3, updating tangent and slope in real-time.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Animate_the_graph_of_0ed9a09920/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        graph_anchor = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Derivative as Slope of a Tangent Line", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # func_label
        func_label = MathTex(r"y = 0.5x^2", color=BLUE)
        func_label.next_to(title, DOWN, buff=0.3)
        self.objects["func_label"] = func_label

        # deriv_label
        deriv_label = MathTex(r"y' = x", color=GREEN)
        deriv_label.next_to(func_label, RIGHT, buff=1.0)
        self.objects["deriv_label"] = deriv_label

        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True}
        )
        axes.move_to(graph_anchor)
        self.objects["axes"] = axes

        # parabola
        parabola = axes.plot(lambda x: 0.5 * x**2, color=BLUE, x_range=[-3.5, 3.5])
        self.objects["parabola"] = parabola

        # moving_dot
        moving_dot = Dot(radius=0.08, color=YELLOW, z_index=2)
        moving_dot.move_to(axes.c2p(-3, 0.5 * (-3)**2))
        self.objects["moving_dot"] = moving_dot

        # tangent_line (initial placeholder, will be updated by always_redraw)
        tangent_line = Line(LEFT, RIGHT, color=RED, stroke_width=3)
        tangent_line.move_to(axes.get_origin())
        self.objects["tangent_line"] = tangent_line

        # slope_eq_label
        slope_eq_label = MathTex(r"m = y'(x) = x", color=WHITE)
        slope_eq_label.move_to(footer_anchor + UP * 0.3)
        self.objects["slope_eq_label"] = slope_eq_label

        # slope_value
        slope_value = DecimalNumber(0, color=YELLOW, num_decimal_places=2)
        slope_value.next_to(slope_eq_label, DOWN, buff=0.5)
        self.objects["slope_value"] = slope_value

        # ValueTracker for the x-coordinate of the moving point
        x_tracker = ValueTracker(-3.0)
        self.objects["x_tracker"] = x_tracker

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/derivative_slope_tangent/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(self.objects["axes"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/derivative_slope_tangent/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Create parabola
        self.play(Create(self.objects["parabola"].set_color(BLUE)), run_time=1.5)
        # Visual action: Write title, func_label, deriv_label
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Write(self.objects["func_label"]), Write(self.objects["deriv_label"]), run_time=1.0)
        total_anim_time_step2 = 1.5 + 1.0 + 1.0
        remaining_2 = max(0.1, 4.0 - total_anim_time_step2 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/derivative_slope_tangent/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Indicate moving_dot
        self.play(Indicate(self.objects["moving_dot"], color=YELLOW, run_time=1))
        # Visual action: Create moving_dot and tangent_line
        self.play(Create(self.objects["moving_dot"]), run_time=1.0)

        # Define the tangent line updater function
        def get_tangent_line():
            x = x_tracker.get_value()
            y = 0.5 * x**2
            slope = x  # derivative y' = x
            point = axes.c2p(x, y)
            # Create a line segment centered at the point, with length 4
            line_length = 4.0
            dx = line_length / 2.0
            dy = slope * dx
            start = axes.c2p(x - dx, y - dy)
            end = axes.c2p(x + dx, y + dy)
            return Line(start, end, color=RED, stroke_width=3)

        # Replace the placeholder tangent_line with the always_redraw version
        self.remove(self.objects["tangent_line"])
        tangent_line_dynamic = always_redraw(get_tangent_line)
        self.objects["tangent_line"] = tangent_line_dynamic
        self.add(tangent_line_dynamic)

        # Update moving_dot position based on x_tracker
        moving_dot.add_updater(lambda m: m.move_to(axes.c2p(x_tracker.get_value(), 0.5 * x_tracker.get_value()**2)))
        self.add(moving_dot)

        total_anim_time_step3 = 1.0 + 1.0
        remaining_3 = max(0.1, 5.0 - total_anim_time_step3 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/derivative_slope_tangent/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Circumscribe slope_value
        self.play(Circumscribe(self.objects["slope_value"], color=YELLOW, run_time=1))
        # Visual action: Write slope_eq_label and create slope_value
        self.play(Write(self.objects["slope_eq_label"]), run_time=1.0)
        self.play(Write(self.objects["slope_value"]), run_time=1.0)

        # Update slope_value based on x_tracker
        slope_value.add_updater(lambda d: d.set_value(x_tracker.get_value()))
        self.add(slope_value)

        total_anim_time_step4 = 1.0 + 1.0 + 1.0
        remaining_4 = max(0.1, 4.0 - total_anim_time_step4 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/derivative_slope_tangent/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Animate x_tracker from -3 to 3 over 8 seconds
        self.play(x_tracker.animate.set_value(3.0), run_time=8.0, rate_func=linear)
        remaining_5 = max(0.1, 8.0 - 8.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final wait
        self.wait(max(0.1, 2))