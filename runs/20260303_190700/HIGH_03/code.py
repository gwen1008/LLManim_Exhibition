from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # === SKELETON: DO NOT CHANGE THIS ARCHITECTURE ===
        theta = ValueTracker(0)
        TWO_PI = 2 * np.pi

        # --- LEFT: Unit Circle ---
        circle_center = LEFT * 3
        circle = Circle(radius=2, color=BLUE).move_to(circle_center)
        circle_dot = always_redraw(lambda: Dot(
            circle_center + 2 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
            color=RED
        ))
        radius_line = always_redraw(lambda: Line(
            circle_center,
            circle_center + 2 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
            color=WHITE
        ))

        # --- RIGHT: Sine Graph ---
        axes = Axes(
            x_range=[0, TWO_PI, np.pi/2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5, y_length=3,
        ).move_to(RIGHT * 3)
        sine_curve = axes.plot(lambda x: np.sin(x), x_range=[0, TWO_PI], color=YELLOW)
        
        # Create initial dots and lines (without always_redraw)
        initial_theta = theta.get_value()
        graph_dot = Dot(
            axes.c2p(initial_theta, np.sin(initial_theta)),
            color=RED
        )
        proj_line = DashedLine(
            circle_center + 2 * np.array([np.cos(initial_theta), np.sin(initial_theta), 0]),
            axes.c2p(initial_theta, np.sin(initial_theta)),
            color=GRAY, stroke_width=1
        )

        # === Setup ===
        self.play(Create(circle), Create(axes))
        self.play(Create(sine_curve), run_time=2)
        self.add(circle_dot, radius_line, graph_dot, proj_line)

        # === Main animation: ONE ValueTracker drives ALL movement ===
        # Animate the graph_dot and proj_line alongside theta
        graph_dot_anim = graph_dot.animate.move_to(axes.c2p(TWO_PI, np.sin(TWO_PI)))
        proj_line_anim = proj_line.animate.become(DashedLine(
            circle_center + 2 * np.array([np.cos(TWO_PI), np.sin(TWO_PI), 0]),
            axes.c2p(TWO_PI, np.sin(TWO_PI)),
            color=GRAY, stroke_width=1
        ))
        
        self.play(
            theta.animate.set_value(TWO_PI),
            graph_dot_anim,
            proj_line_anim,
            run_time=8,
            rate_func=linear
        )
        self.wait(1)