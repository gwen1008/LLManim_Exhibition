# Source: 3b1b/_2019/diffyq/part2/staging.py
# Description: [3b1b translated] 展示兩體問題的運動方程式，透過顏色區分變數並逐步呈現方程式的各個部分。



from manim import *
class TwoBodyEquations(Scene):
    def construct(self):
        kw = {
            "tex_to_color_map": {
                "x_1": GREY_B,
                "y_1": GREY_B,
                "x_2": BLUE,
                "y_2": BLUE,
                "=": WHITE,
            }
        }
        equations = VGroup(
            MathTex(
                "{d^2 x_1 \\over dt^2}",
                "=",
                "{x_2 - x_1 \\over m_1 \\left(",
                "(x_2 - x_1)^2 + (y_2 - y_1)^2",
                "\\right)^{3/2}",
                **kw
            ),
            MathTex(
                "{d^2 y_1 \\over dt^2}",
                "=",
                "{y_2 - y_1 \\over m_1 \\left(",
                "(x_2 - x_1)^2 + (y_2 - y_1)^2",
                "\\right)^{3/2}",
                **kw
            ),
            MathTex(
                "{d^2 x_2 \\over dt^2}",
                "=",
                "{x_1 - x_2 \\over m_2 \\left(",
                "(x_2 - x_1)^2 + (y_2 - y_1)^2",
                "\\right)^{3/2}",
                **kw
            ),
            MathTex(
                "{d^2 y_2 \\over dt^2}",
                "=",
                "{y_1 - y_2 \\over m_2 \\left(",
                "(x_2 - x_1)^2 + (y_2 - y_1)^2",
                "\\right)^{3/2}",
                **kw
            ),
        )

        equations.arrange(DOWN, buff=LARGE_BUFF)
        equations.set_height(6)
        equations.to_edge(LEFT)

        variables = VGroup()
        lhss = VGroup()
        rhss = VGroup()
        for equation in equations:
            variable = equation[1]  # "=" 符號
            lhs = equation[:4]
            rhs = equation[4:]
            variables.add(variable)
            lhss.add(lhs)
            rhss.add(rhs)
        lhss_copy = lhss.copy()

        for variable, lhs in zip(variables, lhss):
            variable.save_state()
            variable.match_height(lhs)
            variable.scale(0.7)
            variable.move_to(lhs, LEFT)

        self.play(LaggedStart(*[
            FadeIn(v, shift=RIGHT)
            for v in variables
        ]))
        self.wait()
        self.play(
            LaggedStartMap(Restore, variables),
            FadeIn(
                lhss_copy,
                remover=True,
                lag_ratio=0.1,
                run_time=2,
            )
        )
        self.add(lhss)
        self.wait()
        self.play(LaggedStartMap(
            FadeIn, rhss
        ))
        self.wait()
        self.play(
            LaggedStart(*[
                Indicate(lhs[:3], color=YELLOW)
                for lhs in lhss
            ])
        )
        self.wait()
        self.play(
            LaggedStartMap(
                Indicate, rhss,
                color=YELLOW
            )
        )
        self.wait()
