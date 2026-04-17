# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示一個紅色警告三角形搭配驚嘆號，並在下方顯示「Probability」文字，強調機率中的危險性。



from manim import *
class DangerInProbability(Scene):
    def construct(self):
        warning = self.get_warning_sign()
        probability = Text("Probability")
        probability.scale(2)

        self.play(Write(warning, run_time=1))
        self.play(
            warning.animate.next_to(probability, UP, buff=LARGE_BUFF),
            LaggedStartMap(FadeIn, probability)
        )
        self.wait()

    def get_warning_sign(self):
        triangle = RegularPolygon(n=3, start_angle=PI/2)
        triangle.set_stroke(RED, width=12)
        triangle.set_height(2)
        bang = Text("!")
        bang.set_height(0.6 * triangle.get_height())
        bang.move_to(interpolate(
            triangle.get_bottom(),
            triangle.get_top(),
            0.4,
        ))
        triangle.add(bang)
        return triangle
