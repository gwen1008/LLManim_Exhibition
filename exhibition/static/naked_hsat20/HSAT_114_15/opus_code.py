from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title("玩偶定價期望值問題", include_underline=True)
        self.play(Write(title))
        self.wait(0.5)

        intro = VGroup(
            Text("投擲均勻硬幣至多 5 次，累積得 3 個正面", font_size=26),
            Text("依完成的時機決定價格", font_size=26),
        ).arrange(DOWN, buff=0.2).next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(intro, shift=UP))
        self.wait(1)
        self.play(FadeOut(intro))

        # 四種情況
        rows = [
            ("前 3 次連得 3 正面", "$240", r"\left(\tfrac{1}{2}\right)^3=\tfrac{1}{8}"),
            ("第 4 次才湊滿 3 正面", "$320", r"\binom{3}{2}\tfrac{1}{2^3}\cdot\tfrac{1}{2}=\tfrac{3}{16}"),
            ("第 5 次才湊滿 3 正面", "$400", r"\binom{4}{2}\tfrac{1}{2^4}\cdot\tfrac{1}{2}=\tfrac{3}{16}"),
            ("5 次仍未滿 3 正面", "$480", r"1-\tfrac{1}{8}-\tfrac{3}{16}-\tfrac{3}{16}=\tfrac{1}{2}"),
        ]

        table = VGroup()
        for desc, price, prob in rows:
            d = Text(desc, font_size=22)
            p = Text(price, font_size=24, color=YELLOW)
            pr = MathTex(prob, font_size=28, color=BLUE)
            d.to_edge(LEFT, buff=0.6)
            p.next_to(d, RIGHT, buff=0.5).align_to(d, UP)
            pr.next_to(p, RIGHT, buff=0.6).align_to(d, UP)
            line = VGroup(d, p, pr)
            table.add(line)

        table.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        table.next_to(title, DOWN, buff=0.6).to_edge(LEFT, buff=0.6)

        for line in table:
            self.play(FadeIn(line[0]), run_time=0.4)
            self.play(Write(line[1]), Write(line[2]), run_time=0.7)
            self.wait(0.3)
        self.wait(0.8)

        self.play(table.animate.scale(0.8).to_edge(LEFT, buff=0.3))

        # 期望值計算
        exp = MathTex(
            r"E", r"=", r"240\cdot\tfrac{1}{8}", r"+", r"320\cdot\tfrac{3}{16}",
            r"+", r"400\cdot\tfrac{3}{16}", r"+", r"480\cdot\tfrac{1}{2}",
            font_size=30,
        )
        exp.to_edge(DOWN, buff=1.5)
        self.play(Write(exp))
        self.wait(0.8)

        terms = MathTex(
            r"E", r"=", r"30", r"+", r"60", r"+", r"75", r"+", r"240",
            font_size=32,
        ).next_to(exp, DOWN, buff=0.5)
        self.play(TransformMatchingShapes(exp.copy(), terms))
        self.wait(0.8)

        result = MathTex(r"E = 405", font_size=44, color=GREEN)
        result.next_to(terms, DOWN, buff=0.5)
        box = SurroundingRectangle(result, color=GREEN, buff=0.2)
        self.play(Write(result))
        self.play(Create(box))
        self.wait(0.5)

        ans = Text("購得一個玩偶的期望花費為 405 元", font_size=26, color=GREEN)
        ans.next_to(box, DOWN, buff=0.3)
        self.play(FadeIn(ans, shift=UP))
        self.wait(2)