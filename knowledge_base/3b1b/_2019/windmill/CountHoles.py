# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示從三個標籤過渡到一個數學方程和相關文本說明的動畫過程。



from manim import *
class CountHoles(Scene):
    def construct(self):
        labels = VGroup(
            MathTex(r"\text{Genus }", "0"),
            MathTex(r"\text{Genus }", "1"),
            MathTex(r"\text{Genus }", "2"),
        )

        labels.scale(2)
        labels.arrange(RIGHT, buff=1.5)
        labels.move_to(2 * DOWN)

        equation = MathTex("y^2 = x^3 + ax + b")
        equation.scale(1.5)
        equation.shift(UP)
        equation.to_edge(LEFT)
        # arrow = MathTex(r"\approx").scale(2)
        arrow = Vector(2 * RIGHT)
        arrow.next_to(equation, RIGHT)

        equation_text = Text("Some other problem")
        equation_text.next_to(equation, DOWN, buff=MED_LARGE_BUFF)
        equation_text.match_width(equation)
        equation_text.set_color(YELLOW)

        self.play(LaggedStart(
            *[FadeIn(label, shift=DOWN) for label in labels],
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(
            labels[1].animate.shift(4 * RIGHT),
            FadeOut(labels[0::2]),
        )
        self.play(
            FadeIn(equation, shift=RIGHT),
            GrowArrow(arrow),
        )
        self.play(FadeIn(equation_text, shift=UP))
        self.wait()
