from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("試試手氣：玩偶定價期望值", font_size=40, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        rule = VGroup(
            Text("投擲均勻硬幣至多 5 次，目標累積 3 個正面", font_size=26),
            Text("前 3 次連得 3 正 → $240", font_size=24),
            Text("第 4 次才累積 3 正 → $320", font_size=24),
            Text("第 5 次才累積 3 正 → $400", font_size=24),
            Text("5 次仍未滿 3 正 → $480", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rule.next_to(title, DOWN, buff=0.4)
        for line in rule:
            self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(1)

        self.play(FadeOut(rule))

        # Probability table
        header = VGroup(
            Text("金額", font_size=28, color=BLUE),
            Text("機率", font_size=28, color=BLUE),
            Text("乘積", font_size=28, color=BLUE),
        ).arrange(RIGHT, buff=1.6)
        header.next_to(title, DOWN, buff=0.5)

        rows_data = [
            ("$240", r"\frac{1}{8}", "30"),
            ("$320", r"\frac{3}{16}", "60"),
            ("$400", r"\frac{3}{16}", "75"),
            ("$480", r"\frac{1}{2}", "240"),
        ]

        rows = VGroup()
        prev = header
        for amt, prob, prod in rows_data:
            a = Text(amt, font_size=26)
            p = MathTex(prob, font_size=34)
            pr = Text(prod, font_size=26, color=GREEN)
            row = VGroup(a, p, pr)
            a.move_to(header[0]).set_x(header[0].get_x())
            p.set_x(header[1].get_x())
            pr.set_x(header[2].get_x())
            row.next_to(prev, DOWN, buff=0.4)
            row.set_x(0)
            # realign columns
            a.set_x(header[0].get_x())
            p.set_x(header[1].get_x())
            pr.set_x(header[2].get_x())
            rows.add(row)
            prev = row

        self.play(Write(header))
        for row in rows:
            self.play(FadeIn(row, shift=UP * 0.2), run_time=0.6)
        self.wait(1)

        # Expectation
        formula = MathTex(
            r"E = 240\cdot\tfrac{1}{8} + 320\cdot\tfrac{3}{16}"
            r" + 400\cdot\tfrac{3}{16} + 480\cdot\tfrac{1}{2}",
            font_size=32,
        )
        formula.next_to(rows, DOWN, buff=0.6)
        self.play(Write(formula))
        self.wait(0.5)

        step = MathTex(r"E = 30 + 60 + 75 + 240", font_size=34)
        step.next_to(formula, DOWN, buff=0.4)
        self.play(Write(step))
        self.wait(0.5)

        result = VGroup(
            MathTex(r"E = 405", font_size=48, color=YELLOW),
            Text("元", font_size=36, color=YELLOW),
        ).arrange(RIGHT, buff=0.2)
        result.next_to(step, DOWN, buff=0.5)
        box = SurroundingRectangle(result, color=RED, buff=0.25)
        self.play(Write(result))
        self.play(Create(box))
        self.wait(2)