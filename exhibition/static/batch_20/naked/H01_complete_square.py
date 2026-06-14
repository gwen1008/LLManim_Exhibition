from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("配方法解一元二次方程", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Steps on the left
        eq0 = MathTex("x^2 - 6x + 5 = 0").scale(0.9)
        eq1 = MathTex("x^2 - 6x = -5").scale(0.9)
        eq2 = MathTex("x^2 - 6x + 9 = -5 + 9").scale(0.9)
        eq3 = MathTex("(x-3)^2 = 4").scale(0.9)
        eq4 = MathTex("x - 3 = \\pm 2").scale(0.9)
        eq5 = MathTex("x = 1 \\quad \\text{or} \\quad x = 5").scale(0.9)

        steps = VGroup(eq0, eq1, eq2, eq3, eq4, eq5).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35
        )
        steps.to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)

        self.play(Write(eq0))
        self.wait(0.4)
        self.play(TransformMatchingTex(eq0.copy(), eq1))
        self.wait(0.4)

        note = Text("配方: 加上 (6/2)²=9", font_size=24, color=YELLOW)
        note.next_to(eq2, RIGHT, buff=0.3)
        self.play(TransformMatchingTex(eq1.copy(), eq2), FadeIn(note))
        self.wait(0.5)
        self.play(FadeOut(note))

        self.play(TransformMatchingTex(eq2.copy(), eq3))
        self.wait(0.4)
        self.play(TransformMatchingTex(eq3.copy(), eq4))
        self.wait(0.4)
        self.play(Write(eq5))
        self.wait(0.5)

        # Coordinate system on the right
        axes = Axes(
            x_range=[-1, 7, 1],
            y_range=[-5, 6, 2],
            x_length=5,
            y_length=5,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 18},
        )
        axes.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.2)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        graph = axes.plot(
            lambda x: x**2 - 6 * x + 5,
            x_range=[0.0, 6.0],
            color=BLUE,
        )
        graph_label = MathTex("y = x^2 - 6x + 5", font_size=28, color=BLUE)
        graph_label.next_to(axes, UP, buff=0.1)

        self.play(Create(axes), FadeIn(axes_labels))
        self.play(Create(graph), Write(graph_label))
        self.wait(0.5)

        # Vertex (3, -4)
        vertex = Dot(axes.c2p(3, -4), color=YELLOW)
        vertex_label = MathTex("(3,-4)", font_size=24, color=YELLOW)
        vertex_label.next_to(vertex, DOWN, buff=0.15)
        self.play(FadeIn(vertex, scale=0.5), Write(vertex_label))
        self.wait(0.4)

        # Roots x=1 and x=5
        root1 = Dot(axes.c2p(1, 0), color=RED)
        root2 = Dot(axes.c2p(5, 0), color=RED)
        root1_label = MathTex("x=1", font_size=24, color=RED).next_to(
            root1, UP, buff=0.15
        )
        root2_label = MathTex("x=5", font_size=24, color=RED).next_to(
            root2, UP, buff=0.15
        )
        self.play(
            FadeIn(root1, scale=0.5),
            FadeIn(root2, scale=0.5),
            Write(root1_label),
            Write(root2_label),
        )

        self.play(Indicate(eq5), Indicate(root1), Indicate(root2))
        self.wait(2)