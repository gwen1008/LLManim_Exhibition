# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 展示一個圓周上均勻分佈的箭頭群組，每個箭頭根據其旋轉圈數設定顏色，並以線性速率同時創建出來。



from manim import *
class ArrowCircleTest(Scene):
    def construct(self):
        circle_radius = 3
        circle = Circle(radius=circle_radius, color=WHITE)
        self.add(circle)

        base_arrow = Arrow(circle_radius * 0.7 * RIGHT, circle_radius * 1.3 * RIGHT)

        def rev_rotate(x, revs):
            x.rotate(revs * TAU, about_point=ORIGIN)
            x.set_color(rev_to_color(revs))
            return x

        num_arrows = 8 * 3

        # 0.5 - fdiv below so as to get a clockwise rotation from left
        arrows = [rev_rotate(base_arrow.copy(), 0.5 - (i / num_arrows)) for i in range(num_arrows)]
        arrows_vgroup = VGroup(*arrows)

        self.play(Create(arrows_vgroup), run_time=2.5, rate_func=linear)

        self.wait()
