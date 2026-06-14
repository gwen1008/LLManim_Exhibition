from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("AA 相似 (兩角相等)", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Triangle ABC (smaller)
        A = np.array([-5.0, -1.0, 0])
        B = np.array([-3.0, -1.0, 0])
        C = np.array([-4.2, 1.0, 0])
        tri1 = Polygon(A, B, C, color=BLUE)
        lblA = MathTex("A").next_to(A, DL, buff=0.1)
        lblB = MathTex("B").next_to(B, DR, buff=0.1)
        lblC = MathTex("C").next_to(C, UP, buff=0.1)

        # Triangle DEF (larger, similar)
        scale = 1.5
        D = np.array([1.0, -1.2, 0])
        E = D + (B - A) * scale
        F = D + (C - A) * scale
        tri2 = Polygon(D, E, F, color=GREEN)
        lblD = MathTex("D").next_to(D, DL, buff=0.1)
        lblE = MathTex("E").next_to(E, DR, buff=0.1)
        lblF = MathTex("F").next_to(F, UP, buff=0.1)

        self.play(Create(tri1), Write(VGroup(lblA, lblB, lblC)))
        self.play(Create(tri2), Write(VGroup(lblD, lblE, lblF)))
        self.wait(0.5)

        # Mark equal angles
        angA = Angle(Line(A, C), Line(A, B), radius=0.4, color=YELLOW)
        angD = Angle(Line(D, F), Line(D, E), radius=0.4, color=YELLOW)
        angB = Angle(Line(B, A), Line(B, C), radius=0.4, color=RED)
        angE = Angle(Line(E, D), Line(E, F), radius=0.4, color=RED)

        cond = MathTex(r"\angle A = \angle D,\quad \angle B = \angle E",
                       font_size=34).next_to(title, DOWN, buff=0.3)
        self.play(Create(angA), Create(angD), Create(angB), Create(angE))
        self.play(Write(cond))
        self.wait(0.5)

        concl = Text("⇒ △ABC ∼ △DEF", font_size=32, color=YELLOW).next_to(cond, DOWN, buff=0.2)
        self.play(Write(concl))
        self.wait(1)

        # Fade triangles area to lower, show working on right/bottom
        self.play(FadeOut(concl), FadeOut(cond))

        # Edge labels with given values
        side_AB = MathTex("AB=4", font_size=28, color=BLUE).next_to(Line(A, B).get_center(), DOWN, buff=0.15)
        side_BC = MathTex("BC=5", font_size=28, color=BLUE).next_to(Line(B, C).get_center(), RIGHT, buff=0.15)
        side_DE = MathTex("DE=6", font_size=28, color=GREEN).next_to(Line(D, E).get_center(), DOWN, buff=0.15)
        side_EF = MathTex("EF=?", font_size=28, color=GREEN).next_to(Line(E, F).get_center(), RIGHT, buff=0.15)
        self.play(Write(VGroup(side_AB, side_BC, side_DE, side_EF)))
        self.wait(0.5)

        # Proportion steps
        step1 = MathTex(r"\frac{AB}{DE} = \frac{BC}{EF}", font_size=40)
        step2 = MathTex(r"\frac{4}{6} = \frac{5}{EF}", font_size=40)
        step3 = MathTex(r"EF = \frac{5 \times 6}{4}", font_size=40)
        step4 = MathTex(r"EF = 7.5", font_size=44, color=YELLOW)

        steps = VGroup(step1, step2, step3, step4).arrange(DOWN, buff=0.4)
        steps.to_edge(DOWN, buff=0.4)

        self.play(Write(step1))
        self.wait(0.6)
        self.play(Write(step2))
        self.wait(0.6)
        self.play(Write(step3))
        self.wait(0.6)
        self.play(Write(step4))
        box = SurroundingRectangle(step4, color=YELLOW, buff=0.15)
        self.play(Create(box))

        self.play(Transform(side_EF, MathTex("EF=7.5", font_size=28, color=GREEN).move_to(side_EF)))
        self.wait(2)