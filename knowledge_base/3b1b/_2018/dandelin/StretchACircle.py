# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示一個圓形在平面上沿水平方向拉伸的過程，並標記拉伸前後的點座標變化。



from manim import *
class StretchACircle(Scene):
    def construct(self):
        plane = NumberPlane(
            x_unit_size=2,
            y_unit_size=2
        )

        circle = Circle(radius=2)
        circle.set_stroke(YELLOW, 5)
        circle_ghost = circle.copy()
        circle_ghost.set_stroke(width=1)

        plane_circle_group = VGroup(plane, circle)
        plane_circle_group.save_state()

        arrows = self.get_arrows()

        prop = 1.0 / 8
        start_point = Dot(circle.point_from_proportion(prop))
        end_point = start_point.copy().stretch(2, 0, about_point=ORIGIN)
        end_point.stretch(0.5, 0)
        end_point.set_color(RED)

        xy = MathTex("(x, y)")
        cxy = MathTex("(c \\cdot x, y)")
        cxy[1].set_color(RED)
        for tex in xy, cxy:
            tex.scale(1.5)
            tex.add_background_rectangle()

        xy_arrow = Vector(DOWN, color=WHITE)
        cxy_arrow = Vector(DL, color=WHITE)
        xy_arrow.next_to(start_point, UP, SMALL_BUFF)
        xy.next_to(xy_arrow, UP, SMALL_BUFF)
        cxy_arrow.next_to(end_point, UR, SMALL_BUFF)
        cxy.next_to(cxy_arrow, UR, SMALL_BUFF)

        self.add(plane_circle_group)
        self.wait()
        self.play(
            plane_circle_group.animate.stretch(2, 0),
            LaggedStartMap(
                GrowArrow, arrows,
                run_time=1,
                lag_ratio=1
            ),
            run_time=2
        )
        self.play(FadeOut(arrows))
        self.wait()
        self.play(Restore(plane_circle_group))
        self.play(
            GrowArrow(xy_arrow),
            Write(xy),
            FadeIn(start_point, shift=UP),
        )
        self.wait()
        self.add(circle_ghost)
        self.play(
            circle.animate.stretch(2, 0),
            ReplacementTransform(start_point.copy(), end_point),
            run_time=2
        )
        self.play(
            GrowArrow(cxy_arrow),
            Write(cxy)
        )
        self.wait(2)

    def get_arrows(self):
        result = VGroup()
        for vect in [LEFT, RIGHT]:
            for y in range(-3, 4):
                arrow = Vector(vect)
                arrow.move_to(2 * vect + y * UP)
                result.add(arrow)
        result.set_color(RED)
        return result
