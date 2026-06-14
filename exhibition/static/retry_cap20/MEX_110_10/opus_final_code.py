from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("圓形紙片剪扇形問題", font_size=40, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        problem = VGroup(
            Text("半徑 = 6 的圓，沿兩條半徑剪開", font_size=28),
            Text("一個扇形弧長 = 5π，求另一扇形圓心角", font_size=28),
        ).arrange(DOWN, buff=0.2)
        problem.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(problem))
        self.wait(1)

        radius = 2.0
        center = LEFT * 3.5 + DOWN * 0.5

        circle = Circle(radius=radius, color=BLUE).move_to(center)
        self.play(Create(circle))
        self.wait(0.3)

        ang1 = 150 * DEGREES
        ang2 = 210 * DEGREES

        sector1 = Sector(
            radius=radius, angle=ang1, start_angle=0,
            color=GREEN, fill_opacity=0.5,
        )
        sector1.move_arc_center_to(center)

        sector2 = Sector(
            radius=radius, angle=ang2, start_angle=ang1,
            color=ORANGE, fill_opacity=0.5,
        )
        sector2.move_arc_center_to(center)

        self.play(FadeIn(sector1), FadeIn(sector2))

        lbl1 = Text("弧長 5π", font_size=24, color=GREEN).next_to(circle, UP, buff=0.1)
        lbl2 = Text("?", font_size=30, color=ORANGE).next_to(circle, DOWN, buff=0.1)
        self.play(Write(lbl1), Write(lbl2))
        self.wait(0.8)

        calc = VGroup(
            MathTex(r"C = 2\pi r = 2\pi(6) = 12\pi", font_size=34),
            MathTex(r"12\pi - 5\pi = 7\pi", font_size=34),
            MathTex(r"\ell = r\theta \Rightarrow 7\pi = 6\theta", font_size=34),
            MathTex(r"\theta = \frac{7\pi}{6} = 210^\circ", font_size=38, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        calc.shift(RIGHT * 2.8 + DOWN * 0.3)

        label_arc = Text("另一弧長：", font_size=24).next_to(calc[1], LEFT, buff=0.15)

        for i, m in enumerate(calc):
            if i == 1:
                self.play(Write(m), FadeIn(label_arc))
            else:
                self.play(Write(m))
            self.wait(0.4)

        box = SurroundingRectangle(calc[-1], color=RED, buff=0.15)
        self.play(Create(box))
        self.wait(0.5)

        ans = Text("答案：(D) 210", font_size=36, color=RED)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans, shift=UP))
        self.wait(2)