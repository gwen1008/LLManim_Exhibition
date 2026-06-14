from manim import *


class GeneratedScene(Scene):
    def construct(self):
        data = [3, 7, 5, 7, 2, 8, 7]

        title = Text("資料的平均數、中位數、眾數", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Show data boxes
        boxes = VGroup()
        for n in data:
            sq = Square(side_length=0.9, color=BLUE)
            num = Text(str(n), font_size=34)
            num.move_to(sq.get_center())
            boxes.add(VGroup(sq, num))
        boxes.arrange(RIGHT, buff=0.25)
        boxes.next_to(title, DOWN, buff=0.8)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN) for b in boxes], lag_ratio=0.15))
        self.wait(0.5)

        # ===== (1) Mean =====
        step1 = Text("（1）平均數 = 總和 ÷ 個數", font_size=32, color=YELLOW)
        step1.next_to(boxes, DOWN, buff=0.7)
        self.play(Write(step1))
        self.wait(0.3)

        total = sum(data)
        mean_eq = MathTex(
            r"\frac{3+7+5+7+2+8+7}{7}",
            "=",
            r"\frac{%d}{7}" % total,
            r"\approx 5.57",
            font_size=40,
        )
        mean_eq.next_to(step1, DOWN, buff=0.5)
        self.play(Write(mean_eq[0]))
        self.wait(0.4)
        self.play(Write(mean_eq[1]), Write(mean_eq[2]))
        self.wait(0.4)
        self.play(Write(mean_eq[3]))
        self.wait(1)

        self.play(
            FadeOut(step1), FadeOut(mean_eq),
        )

        # ===== (2) Median =====
        step2 = Text("（2）排序後取中位數", font_size=32, color=GREEN)
        step2.next_to(boxes, DOWN, buff=0.7)
        self.play(Write(step2))
        self.wait(0.3)

        sorted_data = sorted(data)
        sboxes = VGroup()
        for n in sorted_data:
            sq = Square(side_length=0.9, color=GREEN)
            num = Text(str(n), font_size=34)
            num.move_to(sq.get_center())
            sboxes.add(VGroup(sq, num))
        sboxes.arrange(RIGHT, buff=0.25)
        sboxes.next_to(step2, DOWN, buff=0.6)

        self.play(TransformFromCopy(boxes, sboxes))
        self.wait(0.5)

        # Highlight 4th element (median)
        mid_idx = len(sorted_data) // 2
        highlight = SurroundingRectangle(sboxes[mid_idx], color=RED, buff=0.05)
        median_label = Text("第 4 個數 = 中位數", font_size=28, color=RED)
        median_label.next_to(sboxes, DOWN, buff=0.5)
        self.play(Create(highlight), Write(median_label))
        self.wait(0.5)

        median_val = Text("中位數 = %d" % sorted_data[mid_idx], font_size=36, color=RED)
        median_val.next_to(median_label, DOWN, buff=0.4)
        self.play(Write(median_val))
        self.wait(1)

        self.play(
            FadeOut(step2), FadeOut(sboxes), FadeOut(highlight),
            FadeOut(median_label), FadeOut(median_val),
        )

        # ===== (3) Mode =====
        step3 = Text("（3）出現最多次的眾數", font_size=32, color=ORANGE)
        step3.next_to(boxes, DOWN, buff=0.7)
        self.play(Write(step3))
        self.wait(0.3)

        # Count frequencies
        from collections import Counter
        counts = Counter(data)
        mode_val = max(counts, key=counts.get)

        freq_lines = VGroup()
        for val in sorted(counts):
            txt = Text("數字 %d 出現 %d 次" % (val, counts[val]),
                       font_size=28,
                       color=ORANGE if val == mode_val else WHITE)
            freq_lines.add(txt)
        freq_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        freq_lines.next_to(step3, DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(t) for t in freq_lines], lag_ratio=0.2))
        self.wait(0.5)

        mode_result = Text("眾數 = %d" % mode_val, font_size=40, color=ORANGE)
        mode_result.next_to(freq_lines, DOWN, buff=0.5)
        self.play(Write(mode_result))
        self.wait(1)

        self.play(FadeOut(step3), FadeOut(freq_lines), FadeOut(mode_result))

        # ===== Summary =====
        summary = VGroup(
            Text("平均數 ≈ 5.57", font_size=34, color=YELLOW),
            Text("中位數 = 7", font_size=34, color=GREEN),
            Text("眾數 = 7", font_size=34, color=ORANGE),
        ).arrange(DOWN, buff=0.4)
        summary.next_to(boxes, DOWN, buff=0.8)
        self.play(LaggedStart(*[Write(s) for s in summary], lag_ratio=0.3))
        self.wait(2)

        self.play(FadeOut(summary), FadeOut(boxes), FadeOut(title))
        self.wait(0.5)