# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示四元數旋轉三維點的數學表達式，並用弧線箭頭標示運算順序。



from manim import *
class HowQuaternionsRotate3dPoints(Scene):
    def construct(self):
        title = Text(
            "Coming up:\nHow quaternions act on 3d points",
            font_size=36
        )
        title.to_edge(UP)

        expression = MathTex(
            "q", "\\cdot", "p", "\\cdot", "q^{-1}"
        )
        expression.scale(2)
        expression.set_color_by_tex("q", PINK)
        expression.set_color_by_tex("p", YELLOW)

        # 創建右側弧線箭頭
        right_arrow = ArcBetweenPoints(
            expression[0].get_top(),
            expression[2].get_top(),
            angle=-PI,
            color=WHITE,
            stroke_width=4
        )
        # 創建左側弧線箭頭（翻轉右側箭頭）
        left_arrow = right_arrow.copy()
        left_arrow.rotate(PI, about_point=expression[2].get_top())
        left_arrow.shift(SMALL_BUFF * RIGHT)

        self.add(title)
        self.play(Write(expression))
        self.play(Create(right_arrow))
        self.play(Create(left_arrow))
        self.wait()
