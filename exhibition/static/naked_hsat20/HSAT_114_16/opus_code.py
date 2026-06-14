from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#0e1116"

        title = Text("弦長問題：圓與兩直線", font_size=36, color=YELLOW)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # ---- Coordinate system (left side) ----
        ax = Axes(
            x_range=[-4, 5, 1],
            y_range=[-4, 4, 1],
            x_length=6,
            y_length=5.5,
            tips=False,
            axis_config={"color": GREY_B, "include_numbers": False},
        )
        ax.to_edge(LEFT, buff=0.4).shift(DOWN * 0.3)
        origin = ax.c2p(0, 0)

        self.play(Create(ax), run_time=1.2)

        # Point P(3,1)
        P = ax.c2p(3, 1)
        dotP = Dot(P, color=RED)
        labP = MathTex("P(3,1)", font_size=26, color=RED).next_to(dotP, UR, buff=0.1)
        dotO = Dot(origin, color=WHITE)
        labO = MathTex("O", font_size=26).next_to(dotO, DL, buff=0.1)
        self.play(FadeIn(dotP, scale=0.5), Write(labP), FadeIn(dotO), Write(labO))
        self.wait(0.3)

        m = 3 / 4
        # L1: y = 1 + m(x-3), L2: y = 1 - m(x-3)
        L1 = ax.plot(lambda x: 1 + m * (x - 3), x_range=[-4, 5], color=BLUE)
        L2 = ax.plot(lambda x: 1 - m * (x - 3), x_range=[-1.5, 5], color=GREEN)
        l1lab = MathTex("L_1", font_size=28, color=BLUE).move_to(ax.c2p(-3.2, 1 + m * (-3.2 - 3)))
        l2lab = MathTex("L_2", font_size=28, color=GREEN).move_to(ax.c2p(4.5, 1 - m * (4.5 - 3)))

        self.play(Create(L1), Write(l1lab))
        self.play(Create(L2), Write(l2lab))
        self.wait(0.3)

        # Circle radius r = 13/5
        r = 13 / 5
        unit = np.linalg.norm(ax.c2p(1, 0) - ax.c2p(0, 0))
        circle = Circle(radius=r * unit, color=YELLOW).move_to(origin)
        clab = MathTex(r"\Gamma", font_size=30, color=YELLOW).move_to(ax.c2p(0, -2.9))
        self.play(Create(circle), Write(clab))
        self.wait(0.3)

        # Distance from O to L1 = 1 (foot of perpendicular)
        # L1: (3/4)x - y - 5/4 = 0 ; foot:
        a, b, c = 3 / 4, -1, -5 / 4
        d = (a * 0 + b * 0 + c) / (a * a + b * b)
        foot = (0 - a * d, 0 - b * d)
        Pfoot = ax.c2p(foot[0], foot[1])
        perp = Line(origin, Pfoot, color=ORANGE)
        dlab = MathTex("1", font_size=24, color=ORANGE).next_to(perp.get_center(), UR, buff=0.05)
        self.play(Create(perp), Write(dlab))

        # Chord endpoints A,B on circle ∩ L1
        # parametric intersection
        def inter(line_m):
            # line: y = 1 + line_m(x-3) ; x^2+y^2=r^2
            A_ = 1 + line_m**2
            B_ = 2 * line_m * (1 - 3 * line_m)
            C_ = (1 - 3 * line_m) ** 2 - r**2
            disc = B_**2 - 4 * A_ * C_
            xs = [(-B_ + np.sqrt(disc)) / (2 * A_), (-B_ - np.sqrt(disc)) / (2 * A_)]
            return [(x, 1 + line_m * (x - 3)) for x in xs]

        pts = inter(m)
        A = ax.c2p(*pts[0])
        B = ax.c2p(*pts[1])
        dotA = Dot(A, color=PINK)
        dotB = Dot(B, color=PINK)
        labA = MathTex("A", font_size=26, color=PINK).next_to(dotA, UP, buff=0.08)
        labB = MathTex("B", font_size=26, color=PINK).next_to(dotB, DOWN, buff=0.08)
        chord = Line(A, B, color=PINK, stroke_width=6)
        self.play(FadeIn(dotA), FadeIn(dotB), Write(labA), Write(labB))
        self.play(Create(chord))
        self.wait(0.5)

        # ---- Algebra (right side) ----
        steps = VGroup(
            MathTex(r"L_1:\ mx-y+(1-3m)=0", font_size=28),
            MathTex(r"\frac{|1-3m|}{\sqrt{m^2+1}}=1", font_size=30),
            MathTex(r"\Rightarrow 8m^2-6m=0\ \Rightarrow m=\tfrac{3}{4}", font_size=28),
            MathTex(r"r=\frac{|1+3m|}{\sqrt{m^2+1}}=\frac{13/4}{5/4}=\frac{13}{5}", font_size=28),
            MathTex(r"\overline{AB}=2\sqrt{r^2-1}", font_size=30),
            MathTex(r"=2\sqrt{\tfrac{169}{25}-1}=2\cdot\tfrac{12}{5}", font_size=30),
        )
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        steps.to_edge(RIGHT, buff=0.4).shift(UP * 0.2)

        for s in steps:
            self.play(Write(s), run_time=0.9)
            self.wait(0.2)

        ans = MathTex(r"\overline{AB}=\frac{24}{5}", font_size=40, color=YELLOW)
        ans.next_to(steps, DOWN, buff=0.4).align_to(steps, RIGHT)
        box = SurroundingRectangle(ans, color=YELLOW, buff=0.15)
        self.play(Write(ans), Create(box))
        self.play(Indicate(chord, color=YELLOW), Indicate(ans, color=YELLOW))
        self.wait(2)