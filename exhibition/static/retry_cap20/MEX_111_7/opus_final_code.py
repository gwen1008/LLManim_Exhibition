from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("點到直線的距離", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        question = VGroup(
            MathTex(r"L:\ x = -2"),
            MathTex(r"A = (6,\ 5)"),
        ).arrange(DOWN, buff=0.4).next_to(title, DOWN, buff=0.4)
        self.play(Write(question))
        self.wait(1)

        plane = NumberPlane(
            x_range=[-4, 8, 1],
            y_range=[-1, 7, 1],
            x_length=7,
            y_length=4.5,
            background_line_style={"stroke_opacity": 0.4},
        ).to_edge(DOWN, buff=0.5)
        self.play(Create(plane))
        self.wait(0.5)

        # Line L: x = -2
        line = plane.plot_line_graph(
            x_values=[-2, -2],
            y_values=[-1, 7],
            line_color=BLUE,
            add_vertex_dots=False,
        )
        line_label = MathTex("L:\\ x=-2", color=BLUE, font_size=28)
        line_label.next_to(plane.c2p(-2, 6), LEFT, buff=0.1)
        self.play(Create(line), Write(line_label))
        self.wait(0.5)

        # Point A
        A_dot = Dot(plane.c2p(6, 5), color=YELLOW)
        A_label = MathTex("A(6,5)", color=YELLOW, font_size=28).next_to(A_dot, UR, buff=0.1)
        self.play(FadeIn(A_dot, scale=0.5), Write(A_label))
        self.wait(0.5)

        # Foot of perpendicular
        foot = Dot(plane.c2p(-2, 5), color=GREEN)
        dist_line = DashedLine(plane.c2p(-2, 5), plane.c2p(6, 5), color=RED)
        self.play(FadeIn(foot, scale=0.5))
        self.play(Create(dist_line))
        self.wait(0.5)

        # Distance computation
        calc = VGroup(
            MathTex(r"d = |x_A - x_L|"),
            MathTex(r"= |6 - (-2)|"),
            MathTex(r"= 8"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        calc.to_edge(RIGHT, buff=0.3).shift(UP * 0.5)
        calc.scale(0.8)
        for c in calc:
            self.play(Write(c))
            self.wait(0.4)

        answer = MathTex(r"\Rightarrow (D)\ 8", color=GREEN, font_size=40)
        answer.next_to(calc, DOWN, buff=0.4)
        self.play(Write(answer))
        self.play(Indicate(answer))
        self.wait(2)