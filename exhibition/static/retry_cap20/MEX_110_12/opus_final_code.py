from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("摸彩券問題", font_size=44, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        rule = Text("每滿 100 元 → 1 張摸彩券", font_size=30)
        rule.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(rule, shift=DOWN))
        self.wait(0.8)

        # Meimei condition
        mei = VGroup(
            Text("美美：5 盒餅乾 → 3 張", font_size=30, color=BLUE),
            MathTex(r"300 \leq 5x < 400", font_size=40),
            MathTex(r"60 \leq x < 80", font_size=40, color=BLUE),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        mei.next_to(rule, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)

        self.play(Write(mei[0]))
        self.play(Write(mei[1]))
        self.wait(0.4)
        self.play(TransformFromCopy(mei[1], mei[2]))
        self.wait(0.8)

        # Xiaoyi condition
        yi = VGroup(
            Text("小儀：5 盒 + 蛋糕(150) → 4 張", font_size=28, color=GREEN),
            MathTex(r"400 \leq 5x+150 < 500", font_size=38),
            MathTex(r"250 \leq 5x < 350", font_size=38),
            MathTex(r"50 \leq x < 70", font_size=40, color=GREEN),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        yi.next_to(rule, DOWN, buff=0.5).to_edge(RIGHT, buff=0.8)

        self.play(Write(yi[0]))
        self.play(Write(yi[1]))
        self.wait(0.3)
        self.play(Write(yi[2]))
        self.play(TransformFromCopy(yi[2], yi[3]))
        self.wait(0.8)

        # Number line intersection
        line_group = VGroup()
        nl = NumberLine(
            x_range=[40, 90, 10],
            length=8,
            include_numbers=True,
            font_size=24,
        )
        nl.to_edge(DOWN, buff=1.2)

        def seg(a, b, color, yoff):
            la = nl.number_to_point(a)
            lb = nl.number_to_point(b)
            l = Line(la, lb, color=color, stroke_width=8)
            l.shift(UP * yoff)
            return l

        mei_seg = seg(60, 80, BLUE, 0.35)
        yi_seg = seg(50, 70, GREEN, 0.15)
        ans_seg = seg(60, 70, YELLOW, -0.15)

        self.play(Create(nl))
        self.play(Create(mei_seg))
        self.play(Create(yi_seg))
        self.wait(0.5)
        self.play(Create(ans_seg))

        answer = MathTex(r"60 \leq x < 70", font_size=46, color=YELLOW)
        answer.next_to(nl, DOWN, buff=0.4)
        box = SurroundingRectangle(answer, color=YELLOW, buff=0.2)
        self.play(Write(answer), Create(box))
        self.wait(0.5)

        choice = Text("答案：(B)", font_size=36, color=RED)
        choice.next_to(answer, RIGHT, buff=0.6)
        self.play(FadeIn(choice, scale=1.3))
        self.wait(2)