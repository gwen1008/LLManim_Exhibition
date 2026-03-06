'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the derivative of y=0.5x² as the slope of the tangent line at any point.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for axes and parabola
#    - Footer Region: [Bottom y=-3.5] for derivative formula and slope display
# 3. Anti-Overlap Check:
#    - Strategy: Use distinct zones. Title at top, graph centered, footer at bottom.
#    - The tangent line and point move within the graph area.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Title appears.
#    - Step 2: Axes appear.
#    - Step 3: Parabola drawn.
#    - Step 4: Derivative formula shown.
#    - Step 5: Tangent point appears.
#    - Step 6: Slope label appears.
#    - Step 7: Tangent line drawn.
#    - Step 8: Point moves along curve, line and slope update live.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        graph_anchor = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # title
        title = Text("Derivative as Slope: y = 0.5x²", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": GREY}
        )
        axes.move_to(graph_anchor)
        self.objects["axes"] = axes

        # graph_curve (parabola)
        # Use axes.plot for the function y = 0.5*x**2
        graph_curve = axes.plot(lambda x: 0.5 * x**2, color=BLUE, stroke_width=3)
        self.objects["graph_curve"] = graph_curve

        # tangent_point (Dot) - initial position at x=0
        tangent_point = Dot(radius=0.08, color=YELLOW)
        tangent_point.move_to(axes.c2p(0, 0))
        self.objects["tangent_point"] = tangent_point

        # tangent_line (Line) - will be updated by updater
        # Start with a dummy line, updater will set proper points
        tangent_line = Line(LEFT, RIGHT, color=RED, stroke_width=4)
        tangent_line.move_to(graph_anchor)
        self.objects["tangent_line"] = tangent_line

        # derivative_formula
        derivative_formula = MathTex(r"\frac{dy}{dx} = x", color=GREEN, font_size=36)
        derivative_formula.move_to(footer_anchor + LEFT * 3)
        self.objects["derivative_formula"] = derivative_formula

        # slope_label
        slope_label = Text("Slope m = ", color=WHITE, font_size=28)
        # Position relative to derivative_formula
        slope_label.next_to(derivative_formula, RIGHT, buff=1.0)
        slope_label.align_to(derivative_formula, DOWN)
        self.objects["slope_label"] = slope_label

        # slope_value (DecimalNumber)
        slope_value = DecimalNumber(0, num_decimal_places=2, color=RED, font_size=36)
        slope_value.next_to(slope_label, RIGHT, buff=0.3)
        self.objects["slope_value"] = slope_value

        # ValueTracker for the x-coordinate of the tangent point
        x_tracker = ValueTracker(0.0)
        self.objects["x_tracker"] = x_tracker

        # Updater for tangent_point position
        def update_tangent_point(dot):
            x = x_tracker.get_value()
            y = 0.5 * x**2
            dot.move_to(axes.c2p(x, y))
        tangent_point.add_updater(update_tangent_point)

        # Updater for tangent_line
        # Tangent line: slope = x (derivative), point (x, 0.5*x^2)
        # We'll draw a line segment centered at the point, length 2 units in x
        def update_tangent_line(line):
            x = x_tracker.get_value()
            y = 0.5 * x**2
            slope = x  # derivative
            # Start and end points in data coordinates
            dx = 1.5  # half-length in x-direction
            x_start = x - dx
            y_start = y - slope * dx
            x_end = x + dx
            y_end = y + slope * dx
            start_point = axes.c2p(x_start, y_start)
            end_point = axes.c2p(x_end, y_end)
            line.put_start_and_end_on(start_point, end_point)
        tangent_line.add_updater(update_tangent_line)

        # Updater for slope_value
        def update_slope_value(num):
            x = x_tracker.get_value()
            num.set_value(x)
        slope_value.add_updater(update_slope_value)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        step = {
            "step": 1,
            "narrative": "Let's visualize the function y equals one-half x squared.",
            "signal_action": None,
            "visual_action": {
                "type": "Create",
                "target_id": "title",
                "details": "Fade in the title."
            },
            "duration": 4.368,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_00.mp3"
        }
        # Audio
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Visual action
        self.play(Create(self.objects["title"]))
        animation_time = 1.0  # estimated run_time for Create
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        step = {
            "step": 2,
            "narrative": "We begin by drawing its graph, a parabola.",
            "signal_action": {
                "type": "Create",
                "target": "axes"
            },
            "visual_action": {
                "type": "Create",
                "target_id": "axes",
                "details": "Draw the coordinate axes."
            },
            "duration": 3.48,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_01.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action (Create axes) is same as visual action, so we just Create once.
        self.play(Create(self.objects["axes"]))
        animation_time = 1.5
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        step = {
            "step": 3,
            "narrative": "Here is the curve itself.",
            "signal_action": {
                "type": "Create",
                "target": "graph_curve"
            },
            "visual_action": {
                "type": "Create",
                "target_id": "graph_curve",
                "details": "Draw the parabola smoothly."
            },
            "duration": 2.208,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_02.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["graph_curve"]))
        animation_time = 1.5
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        step = {
            "step": 4,
            "narrative": "The derivative of this function, dy/dx, is simply x. This derivative tells us the slope of the tangent line at any point on the curve.",
            "signal_action": {
                "type": "Write",
                "target": "derivative_formula"
            },
            "visual_action": {
                "type": "Write",
                "target_id": "derivative_formula",
                "details": "Display the derivative formula in the footer."
            },
            "duration": 9.24,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_03.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["derivative_formula"]))
        animation_time = 1.0
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        step = {
            "step": 5,
            "narrative": "Let's pick a point on the curve and see this in action. The slope of the tangent line here is...",
            "signal_action": {
                "type": "GrowFromCenter",
                "target": "tangent_point"
            },
            "visual_action": {
                "type": "Create",
                "target_id": "tangent_point",
                "details": "Create the yellow dot at the starting position (x=0)."
            },
            "duration": 6.384,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_04.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: GrowFromCenter
        self.play(GrowFromCenter(self.objects["tangent_point"]))
        animation_time = 1.0
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 6
        step = {
            "step": 6,
            "narrative": "...which, according to our derivative, is just the x-coordinate. Let's display that value.",
            "signal_action": {
                "type": "Write",
                "target": "slope_label"
            },
            "visual_action": {
                "type": "Write",
                "target_id": "slope_label",
                "details": "Write the 'Slope m =' label."
            },
            "duration": 6.792,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_05.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["slope_label"]))
        animation_time = 1.0
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 7
        step = {
            "step": 7,
            "narrative": "Now, we draw the tangent line itself at this point.",
            "signal_action": {
                "type": "Create",
                "target": "tangent_line"
            },
            "visual_action": {
                "type": "Create",
                "target_id": "tangent_line",
                "details": "Draw the red tangent line. Its slope should be 0 (horizontal) at x=0."
            },
            "duration": 3.864,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_06.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Note: The tangent_line updater is already set, but we need to add the line to the scene.
        # We'll Create it, which will show the line with the correct position (horizontal at x=0).
        self.play(Create(self.objects["tangent_line"]))
        animation_time = 1.0
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 8
        step = {
            "step": 8,
            "narrative": "Watch what happens as the point moves. The tangent line rotates, and its slope updates in real-time, always equal to the x-coordinate.",
            "signal_action": {
                "type": "Indicate",
                "target": "slope_value",
                "color": "YELLOW"
            },
            "visual_action": {
                "type": "Transform",
                "target_id": "tangent_point",
                "details": "Animate the tangent_point moving along the curve from x=-3 to x=3 and back, over about 10 seconds. The tangent_line and slope_value should update via updaters during this transformation."
            },
            "duration": 9.384,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_07.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # First, add the slope_value to the scene (it hasn't been shown yet)
        self.add(self.objects["slope_value"])
        # Signal action: Indicate slope_value
        self.play(Indicate(self.objects["slope_value"], color=YELLOW))
        # Visual action: Move the point via ValueTracker animation.
        # We'll animate x_tracker from -3 to 3 and back to -3.
        # Total animation time should be about 10 seconds as per hint.
        # We'll split into two movements: -3 to 3 (5s) and 3 to -3 (5s).
        # But the step duration is 9.384s, so we adjust.
        move_time = step["duration"] - 1.0  # leave 1s for Indicate
        half_time = move_time / 2
        self.play(x_tracker.animate.set_value(3.0), run_time=half_time)
        self.play(x_tracker.animate.set_value(-3.0), run_time=half_time)
        # No additional wait needed because animation fills the time.

        # Final wait
        self.wait(max(0.1, 2))