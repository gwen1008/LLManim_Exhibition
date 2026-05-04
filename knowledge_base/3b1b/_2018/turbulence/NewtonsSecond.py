# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一個帶有質量標籤的方塊在受到向上和向右的力作用後，沿著拋物線軌跡移動的動畫。



from manim import *
class NewtonsSecond(Scene):
    def construct(self):
        square = Square(
            stroke_color=WHITE,
            fill_color=GREY_B,
            fill_opacity=0.5,
            side_length=1
        )
        label = MathTex("m")
        label.scale(1.5)
        label.move_to(square)
        square.add(label)
        square.save_state()
        arrows = VGroup(
            Vector(0.5 * UP).next_to(square, UP, buff=0),
            Vector(RIGHT).next_to(square, RIGHT, buff=0),
        )

        self.play(
            square.animate.shift(4 * RIGHT + 2 * UP),
            rate_func=lambda t: t**2,
            run_time=2
        )
        self.wait()
        square.restore()
        self.play(
            LaggedStartMap(GrowArrow, arrows)
        )
        square.add(arrows)
        self.play(
            square.animate.shift(4 * RIGHT + 2 * UP),
            rate_func=lambda t: t**2,
            run_time=2
        )
        self.wait()
