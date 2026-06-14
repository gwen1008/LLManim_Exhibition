from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("抽球機率問題", font="Noto Sans CJK TC", color=YELLOW).scale(0.9)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        setup = VGroup(
            Text("箱內：白球 50 顆，紅球 10 顆", font="Noto Sans CJK TC").scale(0.55),
            Text("白球抽出後放回，紅球抽出後不放回", font="Noto Sans CJK TC").scale(0.55),
            Text("前 30 次共抽出紅球 4 次", font="Noto Sans CJK TC").scale(0.55),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        setup.next_to(title, DOWN, buff=0.5).to_edge(LEFT)
        for line in setup:
            self.play(FadeIn(line, shift=RIGHT))
            self.wait(0.3)
        self.wait(0.5)

        # 球的視覺
        whites = VGroup(*[Dot(radius=0.12, color=WHITE) for _ in range(10)])
        whites.arrange_in_grid(rows=2, buff=0.18)
        reds = VGroup(*[Dot(radius=0.12, color=RED) for _ in range(10)])
        reds.arrange(RIGHT, buff=0.18)

        wlabel = Text("白球 50（始終放回）", font="Noto Sans CJK TC").scale(0.45)
        wgroup = VGroup(wlabel, whites).arrange(DOWN, buff=0.25)
        rlabel = Text("紅球 10（拿走 4）", font="Noto Sans CJK TC").scale(0.45)
        rgroup = VGroup(rlabel, reds).arrange(DOWN, buff=0.25)

        balls = VGroup(wgroup, rgroup).arrange(RIGHT, buff=1.2)
        balls.next_to(setup, DOWN, buff=0.6).to_edge(LEFT)
        self.play(FadeIn(wgroup), FadeIn(rgroup))
        self.wait(0.5)

        # 拿走 4 顆紅球
        cross = VGroup()
        for i in range(4):
            x = Cross(reds[i], stroke_color=GREY, stroke_width=4).scale(0.5)
            cross.add(x)
        self.play(LaggedStart(*[Create(c) for c in cross], lag_ratio=0.4))
        self.play(*[reds[i].animate.set_opacity(0.2) for i in range(4)])
        self.wait(0.5)

        # 第 31 次狀態
        calc_title = Text("第 31 次抽球前箱內：", font="Noto Sans CJK TC").scale(0.55)
        line1 = VGroup(
            Text("白球 = 50，紅球 =", font="Noto Sans CJK TC").scale(0.5),
            MathTex(r"10 - 4 = 6").scale(0.65),
        ).arrange(RIGHT, buff=0.2)
        line2 = VGroup(
            Text("總球數 =", font="Noto Sans CJK TC").scale(0.5),
            MathTex(r"50 + 6 = 56").scale(0.65),
        ).arrange(RIGHT, buff=0.2)
        calc = VGroup(calc_title, line1, line2).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3
        )
        calc.to_edge(RIGHT).shift(UP * 1.2)
        for line in calc:
            self.play(Write(line))
            self.wait(0.3)
        self.wait(0.5)

        prob = VGroup(
            Text("P(紅) =", font="Noto Sans CJK TC", color=YELLOW).scale(0.7),
            MathTex(r"\frac{6}{56} = \frac{3}{28}", color=YELLOW).scale(0.9),
        ).arrange(RIGHT, buff=0.25)
        prob.next_to(calc, DOWN, buff=0.6)
        box = SurroundingRectangle(prob, color=GREEN, buff=0.2)
        self.play(Write(prob))
        self.play(Create(box))
        self.wait(0.5)

        ans = Text("答案：(D) 3/28", font="Noto Sans CJK TC", color=GREEN).scale(0.7)
        ans.to_edge(DOWN)
        self.play(FadeIn(ans, shift=UP))
        self.wait(2)