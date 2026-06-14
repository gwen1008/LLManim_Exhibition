from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = Text("直角三角形 向量問題", font_size=38).to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # ---- geometry (units with AC = 1) ----
        sin_t = 0.25
        d = sin_t / (np.sqrt(15) / 4)      # tan θ
        b = 11 / (3 * np.sqrt(15))         # tan 3θ
        c = 1.0
        S = 3.6
        A = np.array([0, 0, 0])
        B = np.array([b, 0, 0]) * S
        C = np.array([0, c, 0]) * S
        D = np.array([d, 0, 0]) * S

        tri = Polygon(A, B, C, color=BLUE)
        cd = Line(C, D, color=YELLOW)

        dotA, dotB, dotC, dotD = Dot(A), Dot(B), Dot(C), Dot(D, color=YELLOW)
        lblA = Text("A", font_size=26).next_to(A, DL, buff=0.12)
        lblB = Text("B", font_size=26).next_to(B, DR, buff=0.12)
        lblC = Text("C", font_size=26).next_to(C, UL, buff=0.12)
        lblD = Text("D", font_size=26).next_to(D, DOWN, buff=0.12)

        ra = RightAngle(Line(A, B), Line(A, C), length=0.28, color=WHITE)
        ang1 = Angle(Line(C, A), Line(C, D), radius=0.9, color=GREEN)
        ang2 = Angle(Line(C, D), Line(C, B), radius=1.15, color=ORANGE)
        t1 = MathTex(r"\theta", font_size=26, color=GREEN).move_to(
            C + 1.25 * (Angle(Line(C, A), Line(C, D), radius=1.0).point_from_proportion(0.5) - C)
        )
        t2 = MathTex(r"2\theta", font_size=26, color=ORANGE).move_to(
            C + 1.5 * (Angle(Line(C, D), Line(C, B), radius=1.0).point_from_proportion(0.5) - C)
        )

        diagram = VGroup(
            tri, cd, ra, ang1, ang2, t1, t2,
            dotA, dotB, dotC, dotD, lblA, lblB, lblC, lblD,
        )
        diagram.scale(0.9).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)

        self.play(Create(tri), FadeIn(dotA, dotB, dotC),
                  Write(lblA), Write(lblB), Write(lblC))
        self.play(Create(ra))
        self.play(FadeIn(dotD), Write(lblD), Create(cd))
        self.play(Create(ang1), Create(ang2), Write(t1), Write(t2))
        self.wait(0.5)

        # ---- solution column ----
        cond = VGroup(
            MathTex(r"\angle BCD = 2\,\angle ACD", font_size=30),
            MathTex(r"\overline{BC} = 2\,\overline{BD}", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        steps = VGroup(
            MathTex(r"\angle ACD=\theta,\ \angle ACB=3\theta", font_size=28),
            MathTex(r"\sec 3\theta = 2(\tan 3\theta-\tan\theta)", font_size=28),
            MathTex(r"= \dfrac{2\sin 2\theta}{\cos 3\theta\cos\theta}", font_size=28),
            MathTex(r"\Rightarrow\ 4\sin\theta = 1,\quad \sin\theta=\tfrac14", font_size=28),
            MathTex(r"k=\dfrac{\overline{AD}}{\overline{AB}}=\dfrac{\tan\theta}{\tan 3\theta}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)

        col = VGroup(cond, steps).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        col.to_edge(RIGHT, buff=0.5).shift(UP * 0.2)

        box = SurroundingRectangle(cond, color=GREY, buff=0.2)
        self.play(Write(cond), Create(box))
        self.wait(0.3)
        for s in steps:
            self.play(Write(s))
            self.wait(0.3)

        result = MathTex(r"k=\dfrac{3}{11}", font_size=46, color=YELLOW)
        result.next_to(col, DOWN, buff=0.4).align_to(col, LEFT)
        rbox = SurroundingRectangle(result, color=YELLOW, buff=0.18)
        self.play(Write(result), Create(rbox))
        self.wait(2)