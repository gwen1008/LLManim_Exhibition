from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = MathTex(r"\int_0^2 (3x^2 - 2x)\, dx").scale(1.2)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Left side: step-by-step solution
        steps = VGroup(
            MathTex(r"F(x) = x^3 - x^2"),
            MathTex(r"= \Big[ x^3 - x^2 \Big]_0^2"),
            MathTex(r"F(2) = 2^3 - 2^2 = 8 - 4 = 4"),
            MathTex(r"F(0) = 0^3 - 0^2 = 0"),
            MathTex(r"F(2) - F(0) = 4 - 0 = 4"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).scale(0.8)
        steps.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)

        # Right side: axes with shaded area
        axes = Axes(
            x_range=[0, 2.5, 1],
            y_range=[0, 9, 3],
            x_length=3.5,
            y_length=3.5,
            axis_config={"include_numbers": True, "font_size": 20},
            tips=False,
        ).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.3)

        func = lambda x: 3 * x**2 - 2 * x
        graph = axes.plot(func, x_range=[0, 2], color=YELLOW)
        area = axes.get_area(graph, x_range=[0, 2], color=BLUE, opacity=0.5)
        graph_label = MathTex(r"3x^2 - 2x", font_size=22).next_to(
            axes.c2p(2, func(2)), UP, buff=0.1
        )

        self.play(Create(axes))
        self.play(Create(graph), Write(graph_label))
        self.play(FadeIn(area))
        self.wait(0.3)

        for step in steps:
            self.play(Write(step))
            self.wait(0.6)

        result_box = SurroundingRectangle(steps[-1], color=GREEN, buff=0.15)
        self.play(Create(result_box))
        self.wait(2)