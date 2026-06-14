from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("向量與直線垂直問題", font_size=40, weight=BOLD)
        title.to_edge(UP)
        underline = Line(title.get_left(), title.get_right()).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), Create(underline))
        self.wait(0.5)

        prob1 = VGroup(
            Text("向量", font_size=28),
            MathTex(r"(a,b)", font_size=36),
            Text("與直線", font_size=28),
            MathTex(r"y = bx - 1", font_size=36),
            Text("垂直", font_size=28),
        ).arrange(RIGHT, buff=0.15)
        prob2 = VGroup(
            Text("求", font_size=28),
            MathTex(r"a + b", font_size=36),
            Text("的最大可能值", font_size=28),
        ).arrange(RIGHT, buff=0.15)
        problem = VGroup(prob1, prob2).arrange(DOWN, buff=0.3).next_to(underline, DOWN, buff=0.5)
        self.play(FadeIn(problem, shift=UP))
        self.wait(1)

        s1a = VGroup(
            Text("直線", font_size=26),
            MathTex(r"y = bx - 1", font_size=34),
            Text("的方向向量為", font_size=26),
            MathTex(r"(1, b)", font_size=34),
        ).arrange(RIGHT, buff=0.15)
        s1b = VGroup(
            Text("垂直條件：", font_size=26),
            MathTex(r"(a,b)\cdot(1,b) = 0", font_size=34),
        ).arrange(RIGHT, buff=0.15)
        step1 = VGroup(s1a, s1b).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        step1.next_to(problem, DOWN, buff=0.5)
        self.play(Write(step1[0]))
        self.wait(0.5)
        self.play(Write(step1[1]))
        self.wait(1)

        eq1 = MathTex(r"a + b^2 = 0", r"\;\Rightarrow\;", r"a = -b^2")
        eq1.next_to(step1, DOWN, buff=0.5)
        self.play(Write(eq1))
        self.wait(1)

        self.play(
            FadeOut(problem),
            FadeOut(step1),
            eq1.animate.next_to(underline, DOWN, buff=0.5),
        )
        self.wait(0.5)

        sub = MathTex(
            r"a + b", r"=", r"-b^2 + b",
        ).next_to(eq1, DOWN, buff=0.6)
        self.play(Write(sub))
        self.wait(1)

        complete = MathTex(
            r"-b^2 + b", r"=", r"-\left(b - \tfrac{1}{2}\right)^2 + \tfrac{1}{4}",
        ).next_to(sub, DOWN, buff=0.6)
        self.play(Write(complete))
        self.wait(1)

        box = SurroundingRectangle(complete[2][-4:], color=YELLOW)
        note = VGroup(
            Text("當", font_size=26),
            MathTex(r"b = \tfrac{1}{2}", font_size=34),
            Text("時取最大值", font_size=26),
        ).arrange(RIGHT, buff=0.15).next_to(complete, DOWN, buff=0.5)
        self.play(Create(box), FadeIn(note, shift=UP))
        self.wait(1)

        answer = MathTex(
            r"(a+b)_{\max} = \frac{1}{4}",
            color=YELLOW,
        ).scale(1.3).next_to(note, DOWN, buff=0.6)
        ans_box = SurroundingRectangle(answer, color=GREEN, buff=0.2)
        self.play(Write(answer))
        self.play(Create(ans_box))
        self.wait(2)