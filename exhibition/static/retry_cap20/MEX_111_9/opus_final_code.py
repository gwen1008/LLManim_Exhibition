from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("剩球抽取機率問題", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        underline = Line(title.get_left(), title.get_right()).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), Create(underline))
        self.wait(0.5)

        setup = VGroup(
            Text("箱中：號碼 1~6，每號各 2 顆，共 12 顆", font_size=28),
            Text("小茹抽出 5 顆（不放回）：1, 2, 2, 3, 5", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        setup.next_to(underline, DOWN, buff=0.4)
        self.play(FadeIn(setup, shift=UP))
        self.wait(1)

        headers = ["號碼", "原有", "已抽", "剩下"]
        nums = [1, 2, 3, 4, 5, 6]
        orig = [2, 2, 2, 2, 2, 2]
        drawn = [1, 2, 1, 0, 1, 0]
        remain = [o - d for o, d in zip(orig, drawn)]

        rows = []
        for i in range(6):
            rows.append([str(nums[i]), str(orig[i]), str(drawn[i]), str(remain[i])])

        table = Table(
            rows,
            col_labels=[Text(h, font_size=26) for h in headers],
            include_outer_lines=True,
        ).scale(0.55)
        table.next_to(setup, DOWN, buff=0.4)
        self.play(Create(table))
        self.wait(1)

        match_note = Text("小茹抽出的號碼集合：{1, 2, 3, 5}", font_size=26, color=YELLOW)
        match_note.to_edge(DOWN, buff=1.2)
        self.play(Write(match_note))
        self.wait(0.5)

        match_rows = [2, 4, 6]  # data rows for nums 1,3,5 (row 1 is header)
        rects = VGroup()
        for r in match_rows:
            cell = table.get_rows()[r]
            rect = SurroundingRectangle(cell, color=GREEN, buff=0.05)
            rects.add(rect)
        self.play(Create(rects))
        self.wait(1)

        self.play(FadeOut(setup), FadeOut(match_note))

        line1 = VGroup(
            Text("剩下總數 =", font_size=30),
            MathTex(r"1+0+1+2+1+2 = 7", font_size=34),
        ).arrange(RIGHT, buff=0.2)
        line2 = VGroup(
            Text("號碼符合者（1,3,5）=", font_size=30, color=GREEN),
            MathTex(r"1+1+1 = 3", font_size=34, color=GREEN),
        ).arrange(RIGHT, buff=0.2)
        line3 = MathTex(r"P = \frac{3}{7}", font_size=48, color=YELLOW)

        calc = VGroup(line1, line2, line3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        calc.next_to(table, RIGHT, buff=0.6)
        if calc.get_right()[0] > config.frame_width / 2 - 0.3:
            calc.next_to(underline, DOWN, buff=0.5).to_edge(RIGHT, buff=0.3)

        self.play(Write(calc[0]))
        self.wait(0.5)
        self.play(Write(calc[1]))
        self.wait(0.5)
        self.play(Write(calc[2]))
        self.wait(0.5)

        ans = SurroundingRectangle(calc[2], color=RED, buff=0.2)
        ans_label = Text("(C)", font_size=36, color=RED).next_to(ans, RIGHT, buff=0.3)
        self.play(Create(ans), FadeIn(ans_label))
        self.wait(2)