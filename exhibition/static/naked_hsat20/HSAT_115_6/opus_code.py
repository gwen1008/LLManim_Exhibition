from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title("直線 $y=-6$ 上使 $\\triangle ABC$ 等腰的點 $C$", font_size=34)
        self.play(Write(title))

        # coordinate system
        ax = Axes(
            x_range=[-10, 6, 2],
            y_range=[-8, 5, 2],
            x_length=10.5,
            y_length=7,
            tips=False,
            axis_config={"include_numbers": False, "color": GREY_B},
        ).scale(0.9).shift(DOWN * 0.4)

        def P(x, y):
            return ax.c2p(x, y)

        # line y = -6
        line = DashedLine(P(-10, -6), P(6, -6), color=YELLOW)
        line_label = MathTex("y=-6", color=YELLOW, font_size=30).next_to(P(5, -6), UP)

        A = Dot(P(2, -2), color=RED)
        B = Dot(P(-1, 2), color=BLUE)
        Alab = MathTex("A(2,-2)", font_size=28, color=RED).next_to(A, RIGHT, buff=0.15)
        Blab = MathTex("B(-1,2)", font_size=28, color=BLUE).next_to(B, UP, buff=0.15)
        AB = Line(A.get_center(), B.get_center(), color=WHITE)
        AB_len = MathTex("AB=5", font_size=28).next_to(AB.get_center(), LEFT, buff=0.3)

        self.play(Create(ax))
        self.play(Create(line), Write(line_label))
        self.play(FadeIn(A, B), Write(Alab), Write(Blab))
        self.play(Create(AB), Write(AB_len))
        self.wait(0.5)

        # ---- Case 1: CA = CB (perpendicular bisector) ----
        case1 = Tex("情況一：$CA=CB$（$AB$ 中垂線）", font_size=30, color=GREEN).to_corner(DL)
        mid = Dot(P(0.5, 0), color=GREEN, radius=0.05)
        # perp bisector: y = 3/4 (x-0.5); at y=-6 -> x=-7.5
        pb = Line(P(-9, 3/4*(-9-0.5)), P(4, 3/4*(4-0.5)), color=GREEN)
        C1 = Dot(P(-7.5, -6), color=GREEN)
        C1lab = MathTex("C_1", font_size=26, color=GREEN).next_to(C1, DOWN, buff=0.1)
        self.play(Write(case1), FadeIn(mid))
        self.play(Create(pb))
        self.play(FadeIn(C1), Write(C1lab))
        self.wait(0.4)
        cnt1 = MathTex("\\Rightarrow 1\\ \\text{個}", font_size=28, color=GREEN).next_to(case1, RIGHT)
        self.play(Write(cnt1))
        self.wait(0.5)
        self.play(FadeOut(pb), FadeOut(mid), FadeOut(case1), FadeOut(cnt1))

        # ---- Case 2: AC = AB (circle center A, r=5) ----
        case2 = Tex("情況二：$AC=AB=5$（以 $A$ 為圓心）", font_size=30, color=ORANGE).to_corner(DL)
        rA = ax.x_length / (ax.x_range[1] - ax.x_range[0]) * 5
        circA = Circle(radius=rA, color=ORANGE).move_to(P(2, -2))
        dist2 = Tex("$A$ 到直線距離 $=4<5$", font_size=26, color=ORANGE).next_to(case2, UP, aligned_edge=LEFT)
        # intersections: |x-2|=3 -> x=5 or x=-1
        C2 = Dot(P(5, -6), color=ORANGE)
        C3 = Dot(P(-1, -6), color=ORANGE)
        C2lab = MathTex("C_2", font_size=26, color=ORANGE).next_to(C2, DOWN, buff=0.1)
        C3lab = MathTex("C_3", font_size=26, color=ORANGE).next_to(C3, DOWN, buff=0.1)
        self.play(Write(case2), Write(dist2))
        self.play(Create(circA))
        self.play(FadeIn(C2, C3), Write(C2lab), Write(C3lab))
        cnt2 = MathTex("\\Rightarrow 2\\ \\text{個}", font_size=28, color=ORANGE).next_to(case2, RIGHT)
        self.play(Write(cnt2))
        self.wait(0.5)
        self.play(FadeOut(circA), FadeOut(case2), FadeOut(dist2), FadeOut(cnt2))

        # ---- Case 3: BC = AB (circle center B, r=5) ----
        case3 = Tex("情況三：$BC=AB=5$（以 $B$ 為圓心）", font_size=30, color=PURPLE).to_corner(DL)
        circB = Circle(radius=rA, color=PURPLE).move_to(P(-1, 2))
        dist3 = Tex("$B$ 到直線距離 $=8>5$，無交點", font_size=26, color=PURPLE).next_to(case3, UP, aligned_edge=LEFT)
        self.play(Write(case3), Create(circB))
        self.play(Write(dist3))
        cnt3 = MathTex("\\Rightarrow 0\\ \\text{個}", font_size=28, color=PURPLE).next_to(case3, RIGHT)
        self.play(Write(cnt3))
        self.wait(0.5)
        self.play(FadeOut(circB), FadeOut(case3), FadeOut(dist3), FadeOut(cnt3))

        # ---- Conclusion ----
        box = SurroundingRectangle(
            VGroup(C1, C2, C3), color=WHITE, buff=0.3
        )
        ans = MathTex("1+2+0=3", font_size=40, color=WHITE).to_corner(DR)
        ansbox = SurroundingRectangle(ans, color=GOLD, buff=0.2)
        self.play(Indicate(C1), Indicate(C2), Indicate(C3))
        self.play(Write(ans), Create(ansbox))
        self.wait(2)