# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 展示一條線段被三個上括號分割成三個部分，每個部分標記為 x_i^2，並帶有漸變顏色。



from manim import *
class DivisionOfUnity(Scene):
    def construct(self):
        factor = 2
        line = Line(factor * LEFT, factor * RIGHT)
        lower_brace = Brace(line, DOWN)
        lower_brace.add(lower_brace.get_text("1"))
        v_lines = VGroup(*[
            DashedLine(0.2 * UP, 0.2 * DOWN).shift(factor * v)
            for v in [LEFT, 0.3 * LEFT, 0.1 * RIGHT, RIGHT]
        ])
        upper_braces = VGroup(*[
            Brace(VGroup(vl1, vl2), UP)
            for vl1, vl2 in zip(v_lines[:-1], v_lines[1:])
        ])
        colors = color_gradient([GREEN, BLUE], 3)
        for i, color, brace in zip(it.count(1), colors, upper_braces):
            label = MathTex("x_%d^2" % i)
            label.set_color(color)
            brace.add(label)

        self.add(line, lower_brace)
        self.play(LaggedStart(
            *[Create(vl) for vl in v_lines[1:3]],
            lag_ratio=0.8,
            run_time=1
        ))
        self.play(LaggedStart(
            *[GrowFromCenter(brace) for brace in upper_braces]
        ))
        self.wait()
