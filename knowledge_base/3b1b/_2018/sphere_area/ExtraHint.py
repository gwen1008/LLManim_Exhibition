# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個標題和一個三角恆等式的數學公式。



from manim import *
class ExtraHint(Scene):
    def construct(self):
        title = Text("Extra hint")
        title.scale(2.5)
        title.shift(UP)
        equation = MathTex(
            "\\sin(2\\theta) = 2\\sin(\\theta)\\cos(\\theta)"
        )
        equation.next_to(title, DOWN)
        self.add(title, equation)
