from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("指數遞減規律", font_size=44)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        rule = Text("每次指數 -1，數值 ÷2", font_size=28, color=YELLOW)
        rule.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(rule))
        self.wait(0.5)

        rows = [
            ("2^3", "8"),
            ("2^2", "4"),
            ("2^1", "2"),
            ("2^0", "1"),
            ("2^{-1}", r"\frac{1}{2}"),
        ]

        start_y = 1.5
        dy = 1.0
        x_left = -3.0
        x_eq = -1.5
        x_val = 0.0

        mobjects = []
        prev_val = None

        for i, (exp_str, val_str) in enumerate(rows):
            y = start_y - i * dy
            exp_tex = MathTex(exp_str, font_size=46).move_to([x_left, y, 0])
            eq_tex = MathTex("=", font_size=46).move_to([x_eq, y, 0])
            val_tex = MathTex(val_str, font_size=46, color=BLUE).move_to([x_val, y, 0])

            if i < 3:
                self.play(
                    FadeIn(exp_tex),
                    FadeIn(eq_tex),
                    FadeIn(val_tex),
                    run_time=0.6,
                )
            else:
                # highlight derivation: divide previous by 2
                arrow = Arrow(
                    start=[x_val + 1.2, prev_y - 0.15, 0],
                    end=[x_val + 1.2, y + 0.15, 0],
                    buff=0.05,
                    color=GREEN,
                )
                div_label = MathTex(r"\div 2", font_size=30, color=GREEN)
                div_label.next_to(arrow, RIGHT, buff=0.15)

                self.play(GrowArrow(arrow), FadeIn(div_label), run_time=0.6)
                self.play(
                    FadeIn(exp_tex),
                    FadeIn(eq_tex),
                    TransformFromCopy(prev_val, val_tex),
                    run_time=0.9,
                )
                if i == 3:
                    box = SurroundingRectangle(
                        VGroup(exp_tex, eq_tex, val_tex), color=YELLOW, buff=0.15
                    )
                    self.play(Create(box), run_time=0.6)
                else:
                    box = SurroundingRectangle(
                        VGroup(exp_tex, eq_tex, val_tex), color=RED, buff=0.15
                    )
                    self.play(Create(box), run_time=0.6)
                mobjects.append(arrow)
                mobjects.append(div_label)
                mobjects.append(box)

            self.wait(0.4)
            prev_val = val_tex
            prev_y = y
            mobjects.extend([exp_tex, eq_tex, val_tex])

        concl = MathTex(
            r"2^0 = 1 \quad,\quad 2^{-1} = \frac{1}{2}",
            font_size=40,
            color=YELLOW,
        )
        concl.to_edge(DOWN, buff=0.6)
        self.play(Write(concl))
        self.wait(2)