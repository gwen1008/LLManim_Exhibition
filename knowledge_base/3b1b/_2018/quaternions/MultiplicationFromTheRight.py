# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示四元數乘法中將 i 視為作用、j 視為點的視覺解釋，並通過箭頭和矩形框強調兩者的角色。



from manim import *
class MultiplicationFromTheRight(Scene):
    def construct(self):
        i, dot, j = product = MathTex("i", "\\cdot", "j")
        product.set_height(1.5)
        product.to_edge(UP, buff=LARGE_BUFF)
        i.set_color(GREEN)
        j.set_color(RED)
        i_rect = SurroundingRectangle(i)
        j_rect = SurroundingRectangle(j)
        i_rect.match_height(j_rect, about_edge=UP, stretch=True)
        VGroup(i_rect, j_rect).set_color(WHITE)
        action_words = TexText("Think of as \\\\ an action")
        point_words = TexText("Think of as \\\\ a point")
        action_words.next_to(i_rect, LEFT)
        point_words.next_to(j_rect, RIGHT)

        arrow = Arrow(
            i.get_top(),
            j.get_top(),
            path_arc=-PI,
        )
        arrow.set_stroke(width=2)

        self.add(product)
        self.play(Create(arrow))
        self.play(
            FadeIn(i_rect),
            Write(action_words)
        )
        self.wait()
        self.play(
            FadeIn(j_rect),
            Write(point_words)
        )
        self.wait(2)
        self.play(arrow.animate.flip())
        self.play(Swap(point_words, action_words))
