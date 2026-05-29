from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = MathTex(r"\ln(1+x) = x - \frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4} + \cdots").to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-3, 2, 1],
            x_length=9,
            y_length=5,
            axis_config={"include_tip": True, "include_numbers": True},
        ).shift(DOWN * 0.3)
        self.play(Create(axes))

        # True ln(1+x)
        true_graph = axes.plot(
            lambda x: np.log(1 + x),
            x_range=[-0.999, 1.5, 0.01],
            color=YELLOW,
        )
        true_label = MathTex(r"\ln(1+x)", color=YELLOW).scale(0.7).next_to(
            axes.c2p(1.2, np.log(2.2)), UR, buff=0.1
        )
        self.play(Create(true_graph), FadeIn(true_label))
        self.wait(0.5)

        # Convergence radius shading |x|<1
        radius_left = DashedLine(
            axes.c2p(-1, -3), axes.c2p(-1, 2), color=RED
        )
        radius_right = DashedLine(
            axes.c2p(1, -3), axes.c2p(1, 2), color=RED
        )
        radius_label = MathTex(r"|x| < 1", color=RED).scale(0.7).next_to(
            axes.c2p(0, 2), UP, buff=0.1
        )
        self.play(Create(radius_left), Create(radius_right), Write(radius_label))
        self.wait(0.5)

        terms = [
            (r"P_1(x) = x", lambda x: x),
            (r"P_2(x) = x - \tfrac{x^2}{2}", lambda x: x - x**2/2),
            (r"P_3(x) = x - \tfrac{x^2}{2} + \tfrac{x^3}{3}",
             lambda x: x - x**2/2 + x**3/3),
            (r"P_4(x) = P_3 - \tfrac{x^4}{4}",
             lambda x: x - x**2/2 + x**3/3 - x**4/4),
            (r"P_5(x) = P_4 + \tfrac{x^5}{5}",
             lambda x: x - x**2/2 + x**3/3 - x**4/4 + x**5/5),
            (r"P_8(x)",
             lambda x: sum(((-1)**(n+1)) * x**n / n for n in range(1, 9))),
        ]

        colors = [BLUE, GREEN, PURPLE, ORANGE, PINK, TEAL]

        current_graph = None
        current_label = None

        for (tex, fn), color in zip(terms, colors):
            new_graph = axes.plot(
                fn,
                x_range=[-0.99, 1.3, 0.01],
                color=color,
            )
            new_label = MathTex(tex, color=color).scale(0.6).to_corner(DL).shift(UP*0.3)

            if current_graph is None:
                self.play(Create(new_graph), FadeIn(new_label))
            else:
                self.play(
                    ReplacementTransform(current_graph, new_graph),
                    FadeOut(current_label),
                    FadeIn(new_label),
                    run_time=1.2,
                )
            current_graph = new_graph
            current_label = new_label
            self.wait(0.6)

        conclusion = Tex(
            r"Converges to $\ln(1+x)$ for $|x|<1$",
            color=RED,
        ).scale(0.7).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)