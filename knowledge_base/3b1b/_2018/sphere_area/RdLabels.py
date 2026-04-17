# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個矩形及其左側和下方的標籤，標籤中的第二個字符以藍色顯示並從下方淡入。



from manim import *
class RdLabels(Scene):
    def construct(self):
        rect = Rectangle(height=1, width=0.5)
        cR = MathTex("cR")
        cR.next_to(rect, LEFT, SMALL_BUFF)
        cd = MathTex("cd")
        cd.next_to(rect, DOWN, SMALL_BUFF)

        labels = VGroup(cd, cR)
        for label in labels:
            label[1].set_color(BLUE)
            self.play(FadeIn(label, shift=DOWN))
