# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示不可壓縮流體流動的條件，標題和方程式以背景矩形突出顯示。



from manim import *
class DivergenceZeroCondition(Scene):
    def construct(self):
        title = Text(
            "For actual (incompressible) fluid flow:",
            font_size=36
        )
        title.to_edge(UP)
        equation = MathTex(
            r"\text{div} \, \textbf{F} = 0 \quad \text{everywhere}"
        )
        equation.next_to(title, DOWN)

        for mob in [title, equation]:
            mob.add_background_rectangle(buff=MED_SMALL_BUFF / 2)
            self.add(mob)
        self.wait(1)
