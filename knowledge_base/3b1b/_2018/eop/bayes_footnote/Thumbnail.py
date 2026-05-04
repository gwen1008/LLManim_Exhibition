# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 展示一個標題、一個困惑的角色和一個條件概率公式的縮圖場景。



from manim import *
class Thumbnail(Scene):
    def construct(self):
        title = Text("Why is this\ncounterintuitive?")  # OldTexText -> Text
        title.scale(2)
        title.to_edge(UP)

        randy = Randolph(mode="sick", color=SICKLY_GREEN)
        randy.scale(1.5)
        randy.shift(3 * LEFT)
        randy.to_edge(DOWN)

        prob = MathTex("P(", "\\text{Sick}", "|", "\\text{Test+}", ")")  # OldTex -> MathTex
        prob.scale(2)
        prob.set_color_by_tex("Sick", YELLOW)
        prob.set_color_by_tex("Test", GREEN)
        prob.next_to(randy, RIGHT)

        self.add(title, randy, prob)
