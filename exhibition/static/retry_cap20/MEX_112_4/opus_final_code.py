from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("比較負數大小").scale(0.9).to_edge(UP)
        underline = Line(LEFT, RIGHT).set_width(title.width + 0.5)
        underline.next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Create(underline))
        self.wait(0.5)

        given = MathTex(
            r"a = -1,\quad b = -1\tfrac{3}{4},\quad c = -1\tfrac{5}{8}"
        ).scale(0.9)
        given.next_to(underline, DOWN, buff=0.5)
        self.play(Write(given))
        self.wait(0.5)

        convert = VGroup(
            MathTex(r"a = -1 = -1.000"),
            MathTex(r"b = -1\tfrac{3}{4} = -1.750"),
            MathTex(r"c = -1\tfrac{5}{8} = -1.625"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.8)
        convert.next_to(given, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)

        a_col, b_col, c_col = YELLOW, BLUE, GREEN
        convert[0].set_color(a_col)
        convert[1].set_color(b_col)
        convert[2].set_color(c_col)

        self.play(LaggedStart(*[Write(m) for m in convert], lag_ratio=0.4))
        self.wait(0.5)

        result = MathTex(r"a", r">", r"c", r">", r"b").scale(1.2)
        result[0].set_color(a_col)
        result[2].set_color(c_col)
        result[4].set_color(b_col)
        result.next_to(convert, RIGHT, buff=1.2)

        self.play(Write(result))
        self.wait(0.5)

        ans = Text("答案：(A)", color=RED).scale(0.8)
        ans.next_to(result, DOWN, buff=0.4)
        box = SurroundingRectangle(ans, color=RED, buff=0.2)
        self.play(Write(ans), Create(box))
        self.wait(0.5)

        # Number line
        nl = NumberLine(
            x_range=[-2, 0, 0.25],
            length=9,
            include_numbers=False,
            include_tip=True,
        )
        labels = VGroup()
        for x in [-2, -1.75, -1.625, -1, 0]:
            tick = MathTex(f"{x:g}").scale(0.5)
            tick.next_to(nl.n2p(x), DOWN, buff=0.2)
            labels.add(tick)
        nl_group = VGroup(nl, labels)
        nl_group.to_edge(DOWN, buff=1.0)

        self.play(Create(nl), FadeIn(labels))
        self.wait(0.3)

        def make_dot(x, color, name):
            d = Dot(nl.n2p(x), color=color, radius=0.1)
            t = MathTex(name, color=color).scale(0.8).next_to(d, UP, buff=0.2)
            return VGroup(d, t)

        pa = make_dot(-1, a_col, "a")
        pb = make_dot(-1.75, b_col, "b")
        pc = make_dot(-1.625, c_col, "c")

        self.play(FadeIn(pb, shift=UP))
        self.play(FadeIn(pc, shift=UP))
        self.play(FadeIn(pa, shift=UP))
        self.wait(2)