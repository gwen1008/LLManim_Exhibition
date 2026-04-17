# Source: 3b1b/_2019/diffyq/part5/staging.py
# Description: [3b1b translated] 展示歐拉公式 e^(iπ) = -1 的視覺化解釋，從常見誤解（重複乘法）轉向正確的泰勒級數展開。



from manim import *
class ReferenceWhatItMeans(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature

        tex_config = {
            "tex_to_color_map": {
                "{i}": BLUE,
                "\\pi": GREEN,
                "-1": RED,
            },
        }
        # 使用 MathTex 替代 OldTex
        epii = MathTex(
            "e^{{i} \\pi} = -1",
            **tex_config
        )
        epii.scale(2)

        many_es = MathTex("e \\cdot e \\cdots e", "= -1", **tex_config)
        many_es.scale(2)
        brace = Brace(many_es[0], DOWN)
        pi_i = MathTex("{i} \\pi \\text{ times}", **tex_config)
        pi_i.next_to(brace, DOWN, buff=SMALL_BUFF)
        repeated_mult = VGroup(many_es, brace, pi_i)

        arrow = MathTex("\\Rightarrow")
        arrow.scale(2)

        group = VGroup(epii, arrow, repeated_mult)
        group.arrange(
            RIGHT, buff=LARGE_BUFF,
        )
        # 對齊底部
        for mob in group[1:]:
            mob.shift(
                (epii[0].get_bottom() - mob[0].get_bottom())[1] * UP
            )
        group.to_edge(UP)

        does_not_mean = Tex("Does \\emph{not}\\\\mean")
        does_not_mean.set_color(RED)
        does_not_mean.move_to(arrow)

        nonsense = Tex(
            "\\dots because that's "
            "literal nonsense!"
        )
        nonsense.next_to(repeated_mult, DOWN)
        nonsense.to_edge(RIGHT, buff=MED_SMALL_BUFF)
        nonsense.set_color(RED)

        down_arrow = MathTex("\\Downarrow")
        down_arrow.scale(2)
        down_arrow.stretch(1.5, 1)
        down_arrow.set_color(GREEN)
        down_arrow.next_to(epii, DOWN, buff=LARGE_BUFF)
        actually_means = Tex("It actually\\\\means")
        actually_means.next_to(down_arrow, RIGHT)
        actually_means.set_color(GREEN)

        series = MathTex(
            "{({i} \\pi )^0 \\over 0!} + ",
            "{({i} \\pi )^1 \\over 1!} + ",
            "{({i} \\pi )^2 \\over 2!} + ",
            "{({i} \\pi )^3 \\over 3!} + ",
            "{({i} \\pi )^4 \\over 4!} + ",
            "\\cdots = -1",
            **tex_config
        )
        series.set_width(config.frame_width - 1)
        series.next_to(down_arrow, DOWN, buff=LARGE_BUFF)
        series.set_x(0)

        self.add(epii)
        self.play(
            FadeIn(arrow, shift=LEFT),
            FadeIn(repeated_mult, shift=2 * LEFT),
            randy.animate.change("maybe"),
        )
        self.wait()
        self.play(randy.animate.change("confused"))
        self.play(
            FadeOut(arrow, shift=DOWN),
            FadeIn(does_not_mean, shift=UP),
        )
        self.play(Write(nonsense))
        self.play(randy.animate.change("angry"))
        self.wait()
        self.play(
            FadeOut(randy, shift=DOWN),
            FadeIn(down_arrow, shift=UP),
            FadeIn(actually_means, shift=LEFT),
            FadeIn(series, lag_ratio=0.1, run_time=2)
        )
        self.wait()
