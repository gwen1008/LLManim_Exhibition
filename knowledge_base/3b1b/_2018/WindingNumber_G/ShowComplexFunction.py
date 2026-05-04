# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示複數平面上一個點 x 經過函數 f(x) = x^5 - x - 1 映射到另一個點的過程，並將函數標籤移動到標題位置。



from manim import *
class ShowComplexFunction(Scene):
    def construct(self):
        plane = ComplexPlane()
        plane.add_coordinates()
        four_i = plane.coordinate_labels[-1]
        plane.coordinate_labels.remove(four_i)
        plane.remove(four_i)

        title = Tex("Complex Plane")
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        rect = BackgroundRectangle(title, fill_opacity=1, buff=MED_SMALL_BUFF)

        x = complex(1, 0.4)
        f = lambda x: x**5 - x - 1

        x_point = plane.number_to_point(x)
        fx_point = plane.number_to_point(f(x))

        x_dot = Dot(x_point)
        fx_dot = Dot(fx_point, color=YELLOW)
        arrow = Arrow(
            x_point, fx_point,
            path_arc=TAU/3,
            color=YELLOW
        )
        arrow.pointwise_become_partial(arrow, 0, 0.95)

        x_label = MathTex("x = %d+%.1fi" % (x.real, x.imag))
        x_label.next_to(x_dot, RIGHT)
        x_label.add_background_rectangle()

        fx_label = MathTex("f(x) = x^5 - x - 1")
        fx_label.next_to(fx_dot, DOWN, buff=SMALL_BUFF)
        fx_label.set_color(YELLOW)
        fx_label.add_background_rectangle()
        fx_label.generate_target()
        fx_label.target.move_to(title)
        fx_label.target[1].set_color(WHITE)

        self.play(
            Write(plane),
            FadeIn(rect),
            LaggedStartMap(FadeIn, title)
        )
        self.play(*[FadeIn(obj) for obj in [x_dot, x_label]])
        self.wait()
        self.play(
            ReplacementTransform(x_dot.copy(), fx_dot, path_arc=arrow.path_arc),
            Create(arrow, rate_func=squish_rate_func(smooth, 0.2, 1))
        )
        self.play(FadeIn(fx_label))
        self.wait(2)
        self.play(
            MoveToTarget(fx_label),
            *[FadeOut(obj) for obj in [title, x_dot, x_label, arrow, fx_dot]]
        )
        self.play(FadeOut(plane.coordinate_labels))
        self.wait()
