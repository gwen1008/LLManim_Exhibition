'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the derivative of y=0.5x² as the slope of the tangent line at any point x.
# 2. Layout Strategy: Use LayoutEngine for zones.
#    - Header Region: Title at y~3.5
#    - Main Content: Axes and graph centered at ORIGIN
#    - Footer Region: Derivative equation at y~-3.5
# 3. Anti-Overlap Check: Use LayoutEngine zones to keep title, content, and footer separated.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step? Yes, using provided audio_path.
#    - [x] Files: "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_XX.mp3"
# 5. Animation Flow: Show title, axes, graph, derivative eq, then point, slope label, tangent line, finally animate point moving.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        layout = LayoutEngine()

        # Create objects from layout_plan
        # Title
        title = Text("Tangent Line to a Parabola: y = 0.5x²", color=WHITE, font_size=36)
        self.objects["title"] = title
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)

        # Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": LIGHT_GRAY}
        )
        self.objects["axes"] = axes
        obj_axes = LayoutObject(axes, "axes")
        layout.add(obj_axes)
        layout.add_to_zone(obj_axes, "CONTENT")
        layout.add_constraint(obj_axes.center_x == 0)
        layout.add_constraint(obj_axes.center_y == 0)

        # Graph (ParametricFunction)
        graph = axes.plot(lambda x: 0.5 * x**2, color=BLUE, stroke_width=4)
        self.objects["graph"] = graph

        # Moving dot (initial at x=-3)
        moving_dot = Dot(radius=0.08, color=RED, fill_opacity=1)
        moving_dot.move_to(axes.c2p(-3, 0.5 * (-3)**2))
        self.objects["moving_dot"] = moving_dot

        # Tangent line (placeholder, will be set by updater)
        # Initial geometry for x=-3: slope = -3, line length 2 units total (1 unit each side)
        # For x=-3, y=4.5, slope m=-3. Line: y - 4.5 = -3(x + 3)
        # Choose x from -4 to -2 for line segment
        tangent_line = Line(
            start=axes.c2p(-4, 0.5 * (-4)**2),  # Placeholder, will be updated
            end=axes.c2p(-2, 0.5 * (-2)**2),    # Placeholder
            color=YELLOW,
            stroke_width=3
        )
        self.objects["tangent_line"] = tangent_line

        # Slope label
        slope_label = MathTex("m = -3.00", color=GREEN, font_size=30)
        # Position will be set relative to dot via updater
        self.objects["slope_label"] = slope_label

        # Derivative equation
        derivative_eq = MathTex(r"\frac{dy}{dx} = x \quad \text{(Slope of the tangent line)}", color=WHITE, font_size=28)
        self.objects["derivative_eq"] = derivative_eq
        obj_deriv = LayoutObject(derivative_eq, "derivative_eq")
        layout.add(obj_deriv)
        layout.add_to_zone(obj_deriv, "FOOTER")
        layout.add_constraint(obj_deriv.center_x == 0)

        # Solve layout
        layout.solve()

        # ValueTracker for x-coordinate (a)
        a_tracker = ValueTracker(-3.0)

        # Updater for moving dot
        def update_dot(dot):
            a = a_tracker.get_value()
            dot.move_to(axes.c2p(a, 0.5 * a**2))
        moving_dot.add_updater(update_dot)

        # Updater for tangent line
        def update_tangent_line(line):
            a = a_tracker.get_value()
            y_a = 0.5 * a**2
            slope = a  # derivative is x
            # Create a line segment of total length 2 (1 unit each side of point)
            # Parametric: point at t: (a + t, y_a + slope * t)
            # We'll set t from -1 to 1
            start = axes.c2p(a - 1, y_a + slope * (-1))
            end = axes.c2p(a + 1, y_a + slope * 1)
            line.put_start_and_end_on(start, end)
        tangent_line.add_updater(update_tangent_line)

        # Updater for slope label
        def update_slope_label(label):
            a = a_tracker.get_value()
            # Format to 2 decimal places
            new_label = MathTex(f"m = {a:.2f}", color=GREEN, font_size=30)
            new_label.move_to(label.get_center())
            label.become(new_label)
        slope_label.add_updater(update_slope_label)

        # Initially, don't add objects to scene (Just-in-Time Entrance)
        # They will be added via Create/Write animations

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's explore the function y equals one-half x squared.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "title", "details": "Fade in the title."},
                "duration": 4.104,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "We plot its graph, which is a parabola opening upwards.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "axes", "details": "Draw the coordinate axes."},
                "duration": 4.176,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, we draw the curve itself.",
                "signal_action": {"type": "Indicate", "target": "graph", "color": "BLUE"},
                "visual_action": {"type": "Create", "target_id": "graph", "details": "Draw the parabola smoothly from left to right."},
                "duration": 2.784,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "A fundamental concept in calculus is the derivative. For this function, the derivative is dy/dx equals x.",
                "signal_action": {"type": "Circumscribe", "target": "derivative_eq", "color": "YELLOW"},
                "visual_action": {"type": "Write", "target_id": "derivative_eq", "details": "Write the derivative equation at the bottom."},
                "duration": 8.664,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "This derivative gives the slope of the tangent line at any point on the curve. Let's pick a point and see.",
                "signal_action": {"type": "Indicate", "target": "moving_dot", "color": "RED"},
                "visual_action": {"type": "Create", "target_id": "moving_dot", "details": "Create the red dot on the parabola at x = -3."},
                "duration": 7.2,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "At this point, the slope of the tangent line is simply its x-coordinate, which is negative three.",
                "signal_action": {"type": "Indicate", "target": "slope_label", "color": "GREEN"},
                "visual_action": {"type": "Create", "target_id": "slope_label", "details": "Write the slope label 'm = -3.00' next to the dot."},
                "duration": 6.264,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "Now, let's draw the tangent line itself, which just touches the curve at this single point.",
                "signal_action": {"type": "Indicate", "target": "tangent_line", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "tangent_line", "details": "Draw the yellow tangent line at the initial point. Its slope should match the label."},
                "duration": 5.784,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "Watch what happens as the point moves along the curve. The tangent line transforms, and its slope updates in real time.",
                "signal_action": None,
                "visual_action": {"type": "Animate", "target_id": "moving_dot", "details": "Animate the dot moving from x=-3 to x=3 along the parabola over 8 seconds. The tangent line and slope label should update continuously via updaters/ValueTracker."},
                "duration": 8.376,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_07.mp3"
            }
        ]

        for step in sequence:
            # Audio
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)

            # Signal action
            signal = step.get("signal_action")
            if signal is not None:
                target_obj = self.objects[signal["target"]]
                color = eval(signal["color"]) if signal["color"] in ["YELLOW", "RED", "GREEN", "BLUE", "WHITE"] else YELLOW
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))

            # Visual action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            obj = self.objects[target_id]

            if visual["type"] == "Create":
                self.play(Create(obj))
            elif visual["type"] == "Write":
                self.play(Write(obj))
            elif visual["type"] == "Animate":
                # Animate dot moving from x=-3 to x=3
                self.play(a_tracker.animate.set_value(3.0), run_time=8)

            # Wait for remaining audio duration
            animation_time = 1 if signal else 0  # signal run_time
            if visual["type"] == "Create" or visual["type"] == "Write":
                animation_time += 1  # approximate creation time
            elif visual["type"] == "Animate":
                animation_time += 8  # run_time of the animation
            remaining = max(0.1, step["duration"] - animation_time + 0.5)
            if remaining > 0:
                self.wait(max(0.1, remaining))

        # Final wait
        self.wait(max(0.1, 2))