from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title("直角三角形向量比例問題", include_underline=True)
        self.add(title)

        # ---- geometry coordinates (illustrative) ----
        A = np.array([-4.0, -1.5, 0])
        B = np.array([2.0, -1.5, 0])
        C = np.array([-4.0, 2.2, 0])
        # D such that AD = (3/11) AB
        D = A + (3.0 / 11.0) * (B - A)

        tri = Polygon(A, B, C, color=BLUE)
        cd = Line(C, D, color=YELLOW)

        right_angle = RightAngle(Line(A, B), Line(A, C), length=0.35, color=GREEN)

        labA = Text("A", font_size=28).next_to(A, DL, buff=0.15)
        labB = Text("B", font_size=28).next_to(B, DR, buff=0.15)
        labC = Text("C", font_size=28).next_to(C, UL, buff=0.15)
        labD = Text("D", font_size=28).next_to(D, DOWN, buff=0.2)

        dotD = Dot(D, color=YELLOW)

        self.play(Create(tri), Create(right_angle))
        self.play(*[Write(l) for l in (labA, labB, labC)])
        self.play(Create(cd), FadeIn(dotD), Write(labD))
        self.wait(0.5)

        # ---- given conditions ----
        given = VGroup(
            MathTex(r"\angle CAB = 90^\circ"),
            MathTex(r"\angle BCD = 2\,\angle ACD"),
            MathTex(r"\overline{BC} = 2\,\overline{BD}"),
            MathTex(r"\overrightarrow{AD} = k\,\overrightarrow{AB}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.6)
        given.to_corner(UR).shift(DOWN * 0.8)
        self.play(LaggedStartMap(FadeIn, given, shift=RIGHT, lag_ratio=0.3))
        self.wait(1)

        self.play(FadeOut(VGroup(tri, cd, right_angle, dotD,
                                 labA, labB, labC, labD, given)))

        # ---- solution steps ----
        s1 = MathTex(r"\angle ACD = \theta,\ \angle BCD = 2\theta")
        s2 = MathTex(r"\triangle BCD:\ \angle BDC = 90^\circ + \theta")
        s3 = MathTex(r"\frac{BC}{BD}=\frac{\sin\angle BDC}{\sin\angle BCD}"
                     r"=\frac{\cos\theta}{\sin 2\theta}=\frac{1}{2\sin\theta}")
        s4 = MathTex(r"\frac{BC}{BD}=2 \;\Rightarrow\; \sin\theta=\frac{1}{4}")

        steps = VGroup(s1, s2, s3, s4).arrange(DOWN, buff=0.35)
        steps.scale(0.7).next_to(title, DOWN, buff=0.5)
        for s in steps:
            self.play(Write(s))
            self.wait(0.5)
        self.wait(1)

        self.play(FadeOut(steps))

        # ---- final computation ----
        f1 = MathTex(r"\tan^2\theta=\frac{\sin^2\theta}{\cos^2\theta}"
                     r"=\frac{1/16}{15/16}=\frac{1}{15}")
        f2 = MathTex(r"k=\frac{AD}{AB}=\frac{\tan\theta}{\tan 3\theta}"
                     r"=\frac{1-3\tan^2\theta}{3-\tan^2\theta}")
        f3 = MathTex(r"k=\frac{1-\frac{3}{15}}{3-\frac{1}{15}}"
                     r"=\frac{4/5}{44/15}=\frac{3}{11}")

        fgrp = VGroup(f1, f2, f3).arrange(DOWN, buff=0.45)
        fgrp.scale(0.7).next_to(title, DOWN, buff=0.5)
        for f in fgrp:
            self.play(Write(f))
            self.wait(0.5)

        box = SurroundingRectangle(f3, color=YELLOW, buff=0.12)
        ans = MathTex(r"k=\frac{3}{11}", color=YELLOW).scale(1.1).to_edge(DOWN, buff=0.4)
        self.play(Create(box), Write(ans))
        self.wait(2)