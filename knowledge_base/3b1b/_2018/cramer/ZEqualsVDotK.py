# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示一個向量點積等式的動畫，其中向量元素以漸變顏色標示，矩陣元素以藍色標示。



from manim import *
class ZEqualsVDotK(Scene):
    def construct(self):
        equation = VGroup(
            MathTex("z"),
            MathTex("="),
            Matrix([["x"], ["y"], ["z"]]),
            MathTex("\\cdot"),
            Matrix([["0"], ["0"], ["1"]]),
        )
        # 設置顏色
        equation[2].get_entries()[0].set_color(X_COLOR)
        equation[2].get_entries()[1].set_color(Y_COLOR)
        equation[2].get_entries()[2].set_color(Z_COLOR)
        equation[4].get_entries().set_color(BLUE)
        
        equation.arrange(RIGHT, buff=MED_SMALL_BUFF)
        equation.to_edge(LEFT)

        self.play(Write(equation))
        self.wait()
