# [VISUAL REASONING]
# Prime factorizations of 28, 42, 105 shown as a clean column-aligned table.
# Each column = one prime (2, 3, 5, 7). Missing primes show "—" instead of phantom whitespace.
# GCD highlighted in green (common to all rows), LCM in yellow (max exponent per column).

from manim import *


class GCDLCMAndSum(Scene):
    def construct(self):
        # Step 1
        title = Text("GCD + LCM of 28, 42, 105", color=WHITE, font_size=38)
        title.move_to(ORIGIN + np.array([0, 3.2, 0]))
        self.play(Write(title), run_time=1.5)
        self.wait(1.5)

        # Step 2 — Build factorization table: columns = primes 2,3,5,7
        # Header row
        col_labels = VGroup(
            MathTex("n", color=GREY_B),
            MathTex("2", color=BLUE),
            MathTex("3", color=BLUE),
            MathTex("5", color=BLUE),
            MathTex("7", color=BLUE),
        ).arrange(RIGHT, buff=0.9)
        col_labels.move_to(ORIGIN + np.array([0, 1.8, 0]))

        def make_row(n_str, p2, p3, p5, p7, color=WHITE):
            row = VGroup(
                MathTex(n_str, color=color),
                MathTex(p2, color=color),
                MathTex(p3, color=color),
                MathTex(p5, color=color),
                MathTex(p7, color=color),
            ).arrange(RIGHT, buff=0.9)
            return row

        # 28 = 2² × 7;  42 = 2 × 3 × 7;  105 = 3 × 5 × 7
        row_28 = make_row("28", "2^2", "-", "-", "7")
        row_42 = make_row("42", "2", "3", "-", "7")
        row_105 = make_row("105", "-", "3", "5", "7")

        for row, ref in [(row_28, col_labels), (row_42, None), (row_105, None)]:
            if row is row_28:
                row.next_to(col_labels, DOWN, buff=0.4)
            elif row is row_42:
                row.next_to(row_28, DOWN, buff=0.3)
            else:
                row.next_to(row_42, DOWN, buff=0.3)
            # column-align by matching x of each cell to corresponding header
            for cell, header in zip(row, col_labels):
                cell.set_x(header.get_x())

        self.play(Write(col_labels), run_time=1.5)
        self.play(LaggedStart(Write(row_28), Write(row_42), Write(row_105), lag_ratio=0.4), run_time=3.0)
        self.wait(2.5)

        # Step 3 — Highlight GCD: prime 7 is common to all three rows (last column)
        gcd_box = SurroundingRectangle(
            VGroup(row_28[4], row_42[4], row_105[4]),
            color=GREEN, buff=0.1
        )
        gcd_label = MathTex(r"\gcd = 7", color=GREEN, font_size=42).move_to(ORIGIN + np.array([0, -1.5, 0]))
        self.play(Create(gcd_box), run_time=1.0)
        self.play(Write(gcd_label), run_time=1.5)
        self.wait(2.5)

        # Step 4 — Highlight LCM: max exponent per column
        # LCM = 2² × 3 × 5 × 7 = 420
        self.play(FadeOut(gcd_box), run_time=0.5)
        lcm_box_2 = SurroundingRectangle(row_28[1], color=YELLOW, buff=0.08)  # 2²
        lcm_box_3 = SurroundingRectangle(row_42[2], color=YELLOW, buff=0.08)  # 3
        lcm_box_5 = SurroundingRectangle(row_105[3], color=YELLOW, buff=0.08)  # 5
        lcm_box_7 = SurroundingRectangle(row_28[4], color=YELLOW, buff=0.08)  # 7
        self.play(Create(lcm_box_2), Create(lcm_box_3), Create(lcm_box_5), Create(lcm_box_7), run_time=1.5)
        lcm_label = MathTex(r"\operatorname{lcm} = 2^2 \cdot 3 \cdot 5 \cdot 7 = 420", color=YELLOW, font_size=38)
        lcm_label.next_to(gcd_label, DOWN, buff=0.3)
        self.play(Write(lcm_label), run_time=2.0)
        self.wait(2.5)

        # Step 5 — Final answer
        self.play(
            FadeOut(col_labels), FadeOut(row_28), FadeOut(row_42), FadeOut(row_105),
            FadeOut(lcm_box_2), FadeOut(lcm_box_3), FadeOut(lcm_box_5), FadeOut(lcm_box_7),
            FadeOut(gcd_label), FadeOut(lcm_label),
            run_time=1.0
        )
        final_sum = MathTex(r"\gcd + \operatorname{lcm} = 7 + 420 = 427", color=WHITE, font_size=44).move_to(ORIGIN)
        self.play(Write(final_sum), run_time=2.0)
        self.play(Indicate(final_sum, color=RED), run_time=1.2)
        self.wait(2.0)
