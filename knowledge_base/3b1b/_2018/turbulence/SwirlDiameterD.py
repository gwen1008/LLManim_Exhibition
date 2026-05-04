# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一個由兩個箭頭組成的漩渦圖形，並從中心生長出一條黃色虛線和標籤"D"來表示直徑。



from manim import *
class SwirlDiameterD(Scene):
    def construct(self):
        kwargs = {
            "path_arc": PI,
            "buff": SMALL_BUFF,
            "color": WHITE
        }
        swirl = VGroup(
            Arrow(RIGHT, LEFT, **kwargs),
            Arrow(LEFT, RIGHT, **kwargs),
        )
        swirl.set_stroke(width=5)
        f = 1.5
        swirl.scale(f)

        h_line = DashedLine(
            f * LEFT, f * RIGHT,
            color=YELLOW,
        )
        D_label = MathTex("D")
        D_label.scale(2)
        D_label.next_to(h_line, UP, SMALL_BUFF)
        D_label.set_color(h_line.get_color())
        # diam = VGroup(h_line, D_label)

        self.play(*map(Create, swirl))
        self.play(
            GrowFromCenter(h_line),
            FadeIn(D_label, shift=UP),
        )
        self.wait()
