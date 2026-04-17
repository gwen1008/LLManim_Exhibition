# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 在頂部文字上創建一個叉號，表示否定或刪除的視覺效果。



from manim import *
class TopQuestionCross(Scene):
    def construct(self):
        top_q = MathTex(r"\text{Why do}", r"\text{ primes}", r"\text{ cause}", r"\text{ spirals}", r"?")
        top_q.scale(2)
        top_q.to_edge(UP)
        cross = Cross(top_q)

        self.play(Create(cross))
        self.wait()
