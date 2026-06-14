from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("兩直角三角形面積差求 a", font_size=36)
        title.to_edge(UP, buff=0.3)
        underline = Line(
            title.get_left(), title.get_right(), color=WHITE
        ).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), Create(underline))
        self.wait(0.5)

        # Setup axes
        axes = Axes(
            x_range=[-1, 8, 1],
            y_range=[-1, 11, 2],
            x_length=6.0,
            y_length=5.0,
            tips=True,
        ).to_edge(LEFT, buff=0.6).to_edge(DOWN, buff=0.6)
        self.play(Create(axes))

        a = 6.0
        P = axes.c2p(a, 0)
        Pdot = Dot(P, color=YELLOW)
        Plabel = MathTex("P(a,0)", font_size=30).next_to(Pdot, DOWN, buff=0.15)
        self.play(FadeIn(Pdot), Write(Plabel))
        self.wait(0.3)

        # L1: slope -4/3, y-intercept 4a/3 = 8
        y1 = 4 * a / 3
        l1 = Line(axes.c2p(0, y1), P, color=BLUE)
        tri1 = Polygon(
            axes.c2p(0, 0), axes.c2p(0, y1), P,
            fill_color=BLUE, fill_opacity=0.35, stroke_width=0,
        )
        l1_lbl = MathTex(r"L_1:\ m=-\tfrac{4}{3}", font_size=26, color=BLUE)
        l1_lbl.next_to(axes.c2p(0, y1), RIGHT, buff=0.2)

        # L2: slope -3/2, y-intercept 3a/2 = 9
        y2 = 3 * a / 2
        l2 = Line(axes.c2p(0, y2), P, color=RED)
        tri2 = Polygon(
            axes.c2p(0, 0), axes.c2p(0, y2), P,
            fill_color=RED, fill_opacity=0.35, stroke_width=0,
        )
        l2_lbl = MathTex(r"L_2:\ m=-\tfrac{3}{2}", font_size=26, color=RED)
        l2_lbl.next_to(axes.c2p(0, y2), RIGHT, buff=0.2)

        self.play(Create(l1), FadeIn(tri1), Write(l1_lbl))
        self.wait(0.3)
        self.play(Create(l2), FadeIn(tri2), Write(l2_lbl))
        self.wait(0.5)

        # Right-side derivation
        steps = VGroup(
            MathTex(r"A_1=\frac12\cdot a\cdot \frac{4a}{3}=\frac{2a^2}{3}", font_size=30),
            MathTex(r"A_2=\frac12\cdot a\cdot \frac{3a}{2}=\frac{3a^2}{4}", font_size=30),
            MathTex(r"A_2-A_1=\frac{3a^2}{4}-\frac{2a^2}{3}=\frac{a^2}{12}", font_size=30),
            MathTex(r"\frac{a^2}{12}=3\ \Rightarrow\ a^2=36", font_size=30),
            MathTex(r"a=6\quad(a>0)", font_size=36, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        steps.to_edge(RIGHT, buff=0.5).shift(UP * 0.3)

        steps[0].set_color(BLUE)
        steps[1].set_color(RED)

        for s in steps:
            self.play(Write(s))
            self.wait(0.4)

        box = SurroundingRectangle(steps[4], color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(2)