from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("插入數使數列仍為等差", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Original sequence
        orig_label = Text("原數列：", font_size=30).to_edge(LEFT).shift(UP * 2)
        orig_seq = MathTex("1,\\;2,\\;3,\\;4,\\;5", font_size=44).next_to(orig_label, RIGHT)
        self.play(FadeIn(orig_label), Write(orig_seq))
        self.wait(0.5)

        cond = VGroup(
            Text("新數列：首項 1、末項 5，共 n 項", font_size=30),
            MathTex("d = \\dfrac{5-1}{n-1} = \\dfrac{4}{n-1}", font_size=40),
        ).arrange(DOWN, buff=0.4).next_to(orig_seq, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(cond[0]))
        self.play(Write(cond[1]))
        self.wait(0.5)

        # Key condition
        key = VGroup(
            Text("原數列各項須出現 → 公差 1 為 d 的整數倍", font_size=28),
            MathTex("\\frac{1}{d} = \\frac{n-1}{4} \\in \\mathbb{Z}"
                    "\\;\\Rightarrow\\; 4 \\mid (n-1)", font_size=40, color=YELLOW),
        ).arrange(DOWN, buff=0.4).next_to(cond, DOWN, buff=0.6).to_edge(LEFT)
        self.play(Write(key[0]))
        self.play(Write(key[1]))
        self.wait(0.5)

        # Check options
        rows = VGroup()
        data = [("(A) 11", 10, False), ("(B) 15", 14, False),
                ("(C) 30", 29, False), ("(D) 33", 32, True)]
        for opt, val, ok in data:
            mark = "✓" if ok else "✗"
            col = GREEN if ok else RED
            line = MathTex(f"\\text{{{opt}}}:\\; n-1={val}", font_size=34)
            m = Text(mark, font_size=34, color=col).next_to(line, RIGHT, buff=0.4)
            rows.add(VGroup(line, m))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT).shift(DOWN * 0.3)

        for r in rows:
            self.play(Write(r), run_time=0.6)
        self.wait(0.5)

        ans = MathTex("32 = 4 \\times 8 \\Rightarrow \\boxed{(D)\\;33}",
                      font_size=48, color=GREEN).to_edge(DOWN)
        self.play(Write(ans))
        self.play(Indicate(rows[3], color=GREEN))
        self.wait(2)