from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Tex(r"求 $a$ 值", font_size=44).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Setup
        a_val = 6
        problem = VGroup(
            MathTex(r"P(a,0),\ a>0"),
            MathTex(r"L_1:\ m=-\tfrac{4}{3},\quad L_2:\ m=-\tfrac{3}{2}"),
            MathTex(r"\text{兩三角形面積差}=3"),
        ).arrange(DOWN, buff=0.35).next_to(title, DOWN, buff=0.4)
        for line in problem:
            self.play(FadeIn(line, shift=UP * 0.2))
        self.wait(0.8)
        self.play(problem.animate.scale(0.7).to_corner(UL))

        # Axes
        axes = Axes(
            x_range=[-1, 7, 1],
            y_range=[-1, 10, 2],
            x_length=5.5,
            y_length=5,
            tips=False,
            axis_config={"include_numbers": False},
        ).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
        self.play(Create(axes))

        P = axes.c2p(a_val, 0)
        dotP = Dot(P, color=YELLOW)
        labP = MathTex("P(a,0)", font_size=30).next_to(dotP, DOWN)
        self.play(FadeIn(dotP), Write(labP))

        # L1: y-int = 4a/3
        y1 = axes.c2p(0, 4 * a_val / 3)
        line1 = Line(P, y1, color=BLUE)
        tri1 = Polygon(axes.c2p(0, 0), P, y1, color=BLUE, fill_opacity=0.3)
        lab1 = MathTex(r"L_1", font_size=30, color=BLUE).next_to(line1.get_center(), RIGHT)
        self.play(Create(line1), Write(lab1))
        self.play(FadeIn(tri1))

        # L2: y-int = 3a/2
        y2 = axes.c2p(0, 3 * a_val / 2)
        line2 = Line(P, y2, color=RED)
        tri2 = Polygon(axes.c2p(0, 0), P, y2, color=RED, fill_opacity=0.25)
        lab2 = MathTex(r"L_2", font_size=30, color=RED).next_to(line2.get_center(), UR, buff=0.1)
        self.play(Create(line2), Write(lab2))
        self.play(FadeIn(tri2))
        self.wait(0.5)

        # Derivation
        steps = VGroup(
            MathTex(r"A_1=\tfrac12\cdot a\cdot \tfrac{4a}{3}=\tfrac{2a^2}{3}", color=BLUE),
            MathTex(r"A_2=\tfrac12\cdot a\cdot \tfrac{3a}{2}=\tfrac{3a^2}{4}", color=RED),
            MathTex(r"\left|\tfrac{2a^2}{3}-\tfrac{3a^2}{4}\right|=\tfrac{a^2}{12}=3"),
            MathTex(r"a^2=36\ \Rightarrow\ a=6", color=GREEN),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).scale(0.62).to_corner(DL).shift(UP*0.2)

        for s in steps:
            self.play(Write(s))
            self.wait(0.4)

        box = SurroundingRectangle(steps[-1], color=GREEN, buff=0.15)
        self.play(Create(box))
        self.wait(2)