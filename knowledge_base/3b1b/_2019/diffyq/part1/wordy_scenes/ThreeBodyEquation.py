# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示三體問題的運動方程組，三個方程分別對應三個物體，以不同顏色標示並從上方漸次淡入。



from manim import *
class ThreeBodyEquation(Scene):
    def construct(self):
        x1 = "\\vec{\\textbf{x}}_1"
        x2 = "\\vec{\\textbf{x}}_2"
        x3 = "\\vec{\\textbf{x}}_3"
        kw = {
            "tex_to_color_map": {
                x1: RED,
                x2: GREEN,
                x3: BLUE,
            }
        }
        equations = VGroup(*[
            MathTex(
                "{d^2", t1, "\\over dt^2}", "=",
                "G", "\\left("
                "{" + m2, "(", t2, "-", t1, ")"
                "\\over"
                "||", t2, "-", t1, "||^3}",
                "+",
                "{" + m3, "(", t3, "-", t1, ")"
                "\\over"
                "||", t3, "-", t1, "||^3}",
                "\\right)",
                **kw
            )
            for t1, t2, t3, m1, m2, m3 in [
                (x1, x2, x3, "m_1", "m_2", "m_3"),
                (x2, x3, x1, "m_2", "m_3", "m_1"),
                (x3, x1, x2, "m_3", "m_1", "m_2"),
            ]
        ])
        equations.arrange(DOWN, buff=LARGE_BUFF)

        self.play(LaggedStart(
            *[FadeIn(eq, shift=UP) for eq in equations],
            lag_ratio=0.2,
        ))
        self.wait()
