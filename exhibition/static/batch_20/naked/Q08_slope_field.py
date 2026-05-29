from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = MathTex(r"\frac{dy}{dx} = x - y").to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_tip": True, "stroke_width": 2},
        ).shift(DOWN * 0.3)
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        self.play(Create(axes), Write(x_label), Write(y_label))

        # Slope field
        arrows = VGroup()
        L = 0.3
        for x in np.arange(-3.5, 3.6, 0.6):
            for y in np.arange(-2.5, 2.6, 0.5):
                slope = x - y
                theta = np.arctan(slope)
                dx = L * np.cos(theta)
                dy = L * np.sin(theta)
                start = axes.c2p(x - dx, y - dy)
                end = axes.c2p(x + dx, y + dy)
                color = interpolate_color(BLUE, RED, (np.tanh(slope) + 1) / 2)
                arrow = Line(start, end, stroke_width=2, color=color)
                arrows.add(arrow)

        self.play(Create(arrows), run_time=2.5)

        sol_label = MathTex(r"y = x - 1 + C e^{-x}").scale(0.7).to_corner(UR).shift(DOWN*0.5)
        self.play(Write(sol_label))

        # Solution 1: through (-2, 2) => C = (2 - (-2-1)) e^{-2} = 5 e^{-2}
        # y(x0)=y0 => C = (y0 - x0 + 1) e^{x0}
        def make_sol(x0, y0, color):
            C = (y0 - x0 + 1) * np.exp(x0)
            return axes.plot(
                lambda x: x - 1 + C * np.exp(-x),
                x_range=[-3.8, 3.8],
                color=color,
                stroke_width=4,
            )

        dot1 = Dot(axes.c2p(-2, 2), color=YELLOW)
        curve1 = make_sol(-2, 2, YELLOW)
        label1 = MathTex(r"(-2, 2)").scale(0.6).next_to(dot1, UL, buff=0.1).set_color(YELLOW)
        self.play(FadeIn(dot1), Write(label1))
        self.play(Create(curve1), run_time=2)

        dot2 = Dot(axes.c2p(1, -2), color=GREEN)
        curve2 = make_sol(1, -2, GREEN)
        label2 = MathTex(r"(1, -2)").scale(0.6).next_to(dot2, DR, buff=0.1).set_color(GREEN)
        self.play(FadeIn(dot2), Write(label2))
        self.play(Create(curve2), run_time=2)

        self.wait(2)