from manim import *
import math

class GeneratedScene(Scene):
    def construct(self):
        title = Text("Taylor Series Approximation of sin(x)", font_size=32).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-PI*1.5, PI*1.5, PI/2],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=4.5,
            axis_config={"include_tip": True, "include_numbers": False},
        ).shift(DOWN*0.3)

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        self.play(Create(axes), Write(x_label), Write(y_label))

        sin_graph = axes.plot(lambda x: math.sin(x), color=BLUE, x_range=[-PI*1.4, PI*1.4])
        sin_label = MathTex(r"\sin(x)", color=BLUE).next_to(axes, RIGHT).shift(UP*1.2 + LEFT*1.5)
        self.play(Create(sin_graph), Write(sin_label))

        def taylor(x, n):
            s = 0
            for k in range(n):
                s += (-1)**k * x**(2*k+1) / math.factorial(2*k+1)
            return s

        formulas = [
            r"P_1(x) = x",
            r"P_3(x) = x - \tfrac{x^3}{3!}",
            r"P_5(x) = x - \tfrac{x^3}{3!} + \tfrac{x^5}{5!}",
            r"P_7(x) = x - \tfrac{x^3}{3!} + \tfrac{x^5}{5!} - \tfrac{x^7}{7!}",
            r"P_9(x) = \sum_{k=0}^{4}\tfrac{(-1)^k x^{2k+1}}{(2k+1)!}",
        ]

        colors = [YELLOW, ORANGE, RED, PURPLE, GREEN]
        current_graph = None
        current_label = None

        for i, n in enumerate([1, 2, 3, 4, 5]):
            def make_func(k):
                return lambda x: max(min(taylor(x, k), 3), -3)
            new_graph = axes.plot(make_func(n), color=colors[i], x_range=[-PI*1.4, PI*1.4])
            new_label = MathTex(formulas[i], color=colors[i], font_size=30).to_corner(DL).shift(UP*0.2)

            if current_graph is None:
                self.play(Create(new_graph), Write(new_label))
            else:
                self.play(
                    Transform(current_graph, new_graph),
                    Transform(current_label, new_label),
                )
            if current_graph is None:
                current_graph = new_graph
                current_label = new_label
            self.wait(1.2)

        conclusion = Text("More terms → better approximation", font_size=28, color=WHITE).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)