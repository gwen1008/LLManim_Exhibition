from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("三次多項式根與 f(0)>0", font_size=40)
        title.to_edge(UP, buff=0.4)
        underline = Line(LEFT, RIGHT).set_width(title.width + 0.5)
        underline.next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Create(underline))
        self.wait(0.5)

        setup = VGroup(
            MathTex(r"a \in \{-6,-4,-2,2,4,6\}"),
            Text("f(x) 為三次多項式，最高次係數 = a", font_size=26),
            Text("三根成首項 -7、公差 a 的等差數列", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        setup.next_to(underline, DOWN, buff=0.5)
        for line in setup:
            self.play(FadeIn(line, shift=RIGHT), run_time=0.6)
        self.wait(0.5)

        roots_label = Text("三根：", font_size=28)
        roots_math = MathTex(r"-7,\ -7+a,\ -7+2a").scale(0.85)
        roots = VGroup(roots_label, roots_math).arrange(RIGHT, buff=0.2)
        roots.next_to(setup, DOWN, buff=0.5)
        self.play(Write(roots))
        self.wait(0.5)

        factored = MathTex(
            r"f(x)=a(x+7)(x+7-a)(x+7-2a)"
        ).scale(0.85)
        factored.next_to(roots, DOWN, buff=0.4)
        self.play(Write(factored))
        self.wait(0.5)

        f0 = MathTex(
            r"f(0)=7a(7-a)(7-2a)"
        ).scale(0.9).set_color(YELLOW)
        f0.next_to(factored, DOWN, buff=0.4)
        self.play(TransformFromCopy(factored, f0))
        self.wait(1)

        self.play(
            FadeOut(setup), FadeOut(roots), FadeOut(factored)
        )
        self.play(f0.animate.next_to(underline, DOWN, buff=0.5))
        self.wait(0.3)

        # Build table of evaluations
        data = [
            ("-6", r"7(-6)(13)(19)", "<0", False),
            ("-4", r"7(-4)(11)(15)", "<0", False),
            ("-2", r"7(-2)(9)(11)", "<0", False),
            ("2", r"7(2)(5)(3)=210", ">0", True),
            ("4", r"7(4)(3)(-1)=-84", "<0", False),
            ("6", r"7(6)(1)(-5)", "<0", False),
        ]

        rows = VGroup()
        for a_val, expr, sign, ok in data:
            color = GREEN if ok else RED
            row = VGroup(
                MathTex(rf"a={a_val}").scale(0.7),
                MathTex(expr).scale(0.7),
                MathTex(rf"f(0){sign}").scale(0.7).set_color(color),
            ).arrange(RIGHT, buff=0.5)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.next_to(f0, DOWN, buff=0.5)

        for row in rows:
            self.play(FadeIn(row, shift=UP), run_time=0.5)
        self.wait(0.5)

        # highlight the winning row
        win = rows[3]
        box = SurroundingRectangle(win, color=GREEN, buff=0.15)
        self.play(Create(box))
        self.wait(0.5)

        ans = Text("共有 1 個 a 使 f(0)>0", font_size=30, color=GREEN)
        ans.to_edge(DOWN, buff=0.4)
        self.play(Write(ans))
        self.wait(2)