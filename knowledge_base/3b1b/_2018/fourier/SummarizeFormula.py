# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示傅立葉變換公式中不同部分的矩形框高亮效果，並在下方添加一個螢幕矩形。



from manim import *
class SummarizeFormula(Scene):
    def construct(self):
        expression = self.get_expression()
        screen_rect = ScreenRectangle(height=5)
        screen_rect.to_edge(DOWN)

        # 建立三個包圍不同公式部分的矩形
        exp_rect, g_exp_rect, int_rect = [
            SurroundingRectangle(VGroup(
                expression.get_part_by_tex(p1),
                expression.get_part_by_tex(p2),
            ))
            for p1, p2 in [("e", "t}"), ("g({}", "t}"), ("\\int", "dt")]
        ]

        self.add(expression)
        self.wait()
        self.play(
            Create(screen_rect),
            Create(exp_rect),
        )
        self.wait(2)
        self.play(Transform(exp_rect, g_exp_rect))
        self.wait(2)
        self.play(Transform(exp_rect, int_rect))
        self.wait(2)

    def get_expression(self):
        expression = MathTex(
            "\\hat g(", "f", ")", "=", "\\int", "_{t_1}", "^{t_2}",
            "g({}", "t", ")", "e", "^{-2\\pi i", "f", "t}", "dt"
        )
        # 設定顏色
        expression.set_color_by_tex(
            "t", YELLOW, substring=False,
        )
        expression.set_color_by_tex("t}", YELLOW)
        expression.set_color_by_tex(
            "f", RED, substring=False,
        )
        expression.scale(1.2)
        expression.to_edge(UP)
        return expression
