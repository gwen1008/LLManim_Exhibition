from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = Text("弦長問題", font_size=40)
        title.to_edge(UP)
        underline = Line(title.get_corner(DL), title.get_corner(DR)).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), Create(underline))
        self.wait(0.5)

        # ---- Problem setup text ----
        setup = VGroup(
            VGroup(MathTex(r"L_1, L_2"), Text("過 (3,1), 斜率 m, -m", font_size=24)).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"\Gamma:"), Text("圓心在原點", font_size=24)).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"d(O, L_1) = 1,"), Text("Γ 與 L₂ 相切", font_size=24)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.8).next_to(title, DOWN, buff=0.3)
        for line in setup:
            self.play(FadeIn(line, shift=RIGHT), run_time=0.6)
        self.wait(0.5)

        # ---- Coordinate plane ----
        self.play(FadeOut(setup))
        plane = NumberPlane(
            x_range=[-4, 5, 1],
            y_range=[-4, 4, 1],
            x_length=6.5,
            y_length=5.5,
            background_line_style={"stroke_opacity": 0.3},
        ).next_to(title, DOWN, buff=0.2)
        self.play(Create(plane), run_time=1.2)

        def to_pt(x, y):
            return plane.coords_to_point(x, y)

        # Key point (3,1)
        P = Dot(to_pt(3, 1), color=YELLOW)
        P_lbl = MathTex("(3,1)").scale(0.6).next_to(P, UR, buff=0.1)
        O = Dot(to_pt(0, 0), color=WHITE)
        O_lbl = MathTex("O").scale(0.6).next_to(O, DL, buff=0.1)
        self.play(FadeIn(P), Write(P_lbl), FadeIn(O), Write(O_lbl))

        m = 3 / 4
        r = 13 / 5

        def L1y(x):
            return m * (x - 3) + 1

        def L2y(x):
            return -m * (x - 3) + 1

        L1 = Line(to_pt(-4, L1y(-4)), to_pt(5, L1y(5)), color=BLUE)
        L2 = Line(to_pt(-4, L2y(-4)), to_pt(5, L2y(5)), color=GREEN)
        L1_lbl = MathTex("L_1", color=BLUE).scale(0.7).next_to(L1.get_start(), UR, buff=0.1)
        L2_lbl = MathTex("L_2", color=GREEN).scale(0.7).next_to(L2.get_end(), UL, buff=0.1)
        self.play(Create(L1), Write(L1_lbl))
        self.play(Create(L2), Write(L2_lbl))
        self.wait(0.3)

        circle = Circle(radius=plane.x_axis.unit_size * r, color=RED).move_to(to_pt(0, 0))
        self.play(Create(circle), run_time=1.2)
        self.wait(0.3)

        # Chord endpoints A, B
        a_c = 1 + m * m
        b_c = 2 * m * (1 - 3 * m)
        c_c = (1 - 3 * m) ** 2 - r * r
        disc = b_c * b_c - 4 * a_c * c_c
        x1 = (-b_c + np.sqrt(disc)) / (2 * a_c)
        x2 = (-b_c - np.sqrt(disc)) / (2 * a_c)
        A = Dot(to_pt(x1, L1y(x1)), color=ORANGE)
        B = Dot(to_pt(x2, L1y(x2)), color=ORANGE)
        A_lbl = MathTex("A").scale(0.6).next_to(A, UR, buff=0.08)
        B_lbl = MathTex("B").scale(0.6).next_to(B, DL, buff=0.08)
        chord = Line(A.get_center(), B.get_center(), color=ORANGE, stroke_width=6)
        self.play(FadeIn(A), FadeIn(B), Write(A_lbl), Write(B_lbl))
        self.play(Create(chord))

        foot = self.foot_of_perp(np.array([0, 0]), 3, 1, m)
        d_line = Line(to_pt(0, 0), to_pt(foot[0], foot[1]), color=PURPLE)
        d_lbl = MathTex("1", color=PURPLE).scale(0.6).next_to(d_line.get_center(), RIGHT, buff=0.1)
        self.play(Create(d_line), Write(d_lbl))
        self.wait(0.5)

        # ---- Solution derivation ----
        solution = VGroup(
            MathTex(r"\frac{|1-3m|}{\sqrt{m^2+1}} = 1 \Rightarrow m=\tfrac{3}{4}"),
            MathTex(r"r = \frac{|1+3m|}{\sqrt{m^2+1}} = \frac{13}{5}"),
            MathTex(r"\overline{AB} = 2\sqrt{r^2-1^2}"),
            MathTex(r"= 2\sqrt{\tfrac{169}{25}-1} = \frac{24}{5}"),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.6)
        solution.to_edge(RIGHT).shift(DOWN * 0.3)

        box = SurroundingRectangle(solution, color=YELLOW, buff=0.2)
        movers = VGroup(plane, circle, L1, L2, P, O, A, B, chord, d_line,
                        P_lbl, O_lbl, A_lbl, B_lbl, d_lbl, L1_lbl, L2_lbl)
        self.play(movers.animate.shift(LEFT * 2.2), run_time=1.0)

        for s in solution:
            self.play(Write(s), run_time=0.8)
        self.play(Create(box))
        self.wait(2)

    def foot_of_perp(self, O, px, py, m):
        a, b, c = m, -1, (py - m * px)
        x0, y0 = O
        denom = a * a + b * b
        foot_x = x0 - a * (a * x0 + b * y0 + c) / denom
        foot_y = y0 - b * (a * x0 + b * y0 + c) / denom
        return np.array([foot_x, foot_y])