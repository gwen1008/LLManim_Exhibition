'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the derivative of y=0.5x² as the slope of the tangent line, connecting algebraic formula to geometric interpretation.
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for axes and parabola
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Use anchors to position title high, graph center, explanation low. Slope formula placed top-right of graph.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/To_create_an_animati_7590703919/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
#    - Step 1: Create axes, highlight function label.
#    - Step 2: Draw parabola.
#    - Step 3: Show derivative formula.
#    - Step 4: Show tangent point at vertex.
#    - Step 5: Draw horizontal tangent line.
#    - Step 6: Show slope value display.
#    - Step 7: Animate point moving, updating tangent line and slope value.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on layout_plan description
        title_anchor = 3.5 * UP
        graph_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        slope_display_anchor = 3 * RIGHT + 2.5 * UP

        # Object registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # title
        title = Text("Derivative as Slope of Tangent", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

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
        parabola = axes.plot(lambda x: 0.5 * x**2, color=BLUE, stroke_width=3)
        parabola.move_to(graph_center)
        self.objects["parabola"] = parabola

        # function_label
        function_label = MathTex(r"y = 0.5x^2", color=BLUE)
        function_label.next_to(parabola, UP + RIGHT, buff=0.2)
        self.objects["function_label"] = function_label

        # tangent_point (initial position at vertex)
        tangent_point = Dot(axes.c2p(0, 0), color=RED, radius=0.08)
        self.objects["tangent_point"] = tangent_point

        # tangent_line (initial horizontal line)
        tangent_line = Line(
            axes.c2p(-1.5, 0),
            axes.c2p(1.5, 0),
            color=YELLOW,
            stroke_width=2.5
        )
        self.objects["tangent_line"] = tangent_line

        # slope_formula
        slope_formula = MathTex(r"\frac{dy}{dx} = x", color=GREEN)
        slope_formula.move_to(slope_display_anchor)
        self.objects["slope_formula"] = slope_formula

        # slope_value (initial)
        slope_value = MathTex(r"\mathrm{Slope} = 0.00", color=GREEN)
        slope_value.next_to(slope_formula, DOWN, buff=0.3)
        self.objects["slope_value"] = slope_value

        # explanation_text
        explanation_text = Text("The parabola y = 0.5x²", color=GRAY_C, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ValueTracker for dynamic animations (step 7)
        x_tracker = ValueTracker(0)
        self.objects["x_tracker"] = x_tracker

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/To_create_an_animati_7590703919/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["function_label"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_1 = max(0.1, 5.04 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/To_create_an_animati_7590703919/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Create(self.objects["parabola"]), run_time=2.5)
        remaining_2 = max(0.1, 4.08 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/To_create_an_animati_7590703919/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["slope_formula"], color=GREEN, run_time=1))
        self.play(Write(self.objects["slope_formula"]), run_time=1.5)
        remaining_3 = max(0.1, 7.776 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/To_create_an_animati_7590703919/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["tangent_point"], color=RED, run_time=1))
        self.play(Create(self.objects["tangent_point"]), run_time=1.0)
        remaining_4 = max(0.1, 7.224 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/To_create_an_animati_7590703919/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["tangent_line"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["tangent_line"]), run_time=1.5)
        remaining_5 = max(0.1, 5.736 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/To_create_an_animati_7590703919/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Write(self.objects["slope_value"]), run_time=1.5)
        remaining_6 = max(0.1, 7.464 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        # Setup dynamic updaters for tangent line and slope value
        x_tracker = self.objects["x_tracker"]
        axes = self.objects["axes"]
        tangent_point = self.objects["tangent_point"]
        tangent_line = self.objects["tangent_line"]
        slope_value = self.objects["slope_value"]

        # Update tangent point position
        tangent_point.add_updater(
            lambda m: m.move_to(axes.c2p(x_tracker.get_value(), 0.5 * x_tracker.get_value()**2))
        )

        # Update tangent line (using always_redraw as per hints)
        def update_tangent_line():
            x = x_tracker.get_value()
            y = 0.5 * x**2
            slope = x  # derivative
            # Create a line segment centered at (x, y) with slope
            # Use a reasonable length
            length = 2.0
            dx = length / (2 * np.sqrt(1 + slope**2))
            dy = slope * dx
            start = axes.c2p(x - dx, y - dy)
            end = axes.c2p(x + dx, y + dy)
            return Line(start, end, color=YELLOW, stroke_width=2.5)

        dynamic_tangent_line = always_redraw(update_tangent_line)
        self.add(dynamic_tangent_line)
        self.remove(tangent_line)  # Remove static line

        # Update slope value text (using always_redraw)
        def update_slope_value():
            x = x_tracker.get_value()
            return MathTex(f"\\mathrm{{Slope}} = {x:.2f}", color=GREEN).next_to(
                self.objects["slope_formula"], DOWN, buff=0.3
            )

        dynamic_slope_value = always_redraw(update_slope_value)
        self.add(dynamic_slope_value)
        self.remove(slope_value)  # Remove static text

        audio_step7 = "media/audio/To_create_an_animati_7590703919/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["slope_formula"], color=GREEN, run_time=1))
        self.play(x_tracker.animate.set_value(2.5), run_time=4.0)
        self.play(x_tracker.animate.set_value(-2.5), run_time=4.0)
        remaining_7 = max(0.1, 8.28 - 8.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Final wait
        self.wait(max(0.1, 2))