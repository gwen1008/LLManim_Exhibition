# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示一個圓形和旋轉的半徑，隨著角度變化動態更新數值標籤，並在圓弧上繪製對應的扇形區域。



from manim import *
class UsingTheta(Scene):
    def construct(self):
        plane = NumberPlane(x_length=20, y_length=20)
        plane.set_opacity(0.5)
        self.add(plane)

        circle = Circle(radius=3)
        circle.set_stroke(YELLOW, 2)
        self.add(circle)

        radius = Line(ORIGIN, circle.get_right())
        arc = Arc(radius=0.5, angle=TAU, num_anchors=200)
        arc.set_color(GREEN)
        start_arc = arc.copy()

        theta = MathTex("\\theta", "=")
        theta[0].set_color(GREEN)
        theta.add_background_rectangle()
        
        def update_theta(mob):
            mob.move_to(
                rotate_vector(0.9*RIGHT, radius.get_angle()/2)
            )
        theta.add_updater(update_theta)

        angle = Integer(0, unit="^\\circ")
        def update_angle(mob):
            mob.set_value(radius.get_angle()*(360/TAU))
            mob.next_to(theta, RIGHT, SMALL_BUFF)
        angle.add_updater(update_angle)

        self.add(theta, angle)
        last_frac = 0
        for frac in [1./4, 1./12, 3./8, 1./6, 5./6]:
            self.play(
                Rotate(radius, angle=(frac-last_frac)*TAU, about_point=ORIGIN),
                UpdateFromAlphaFunc(
                    arc,
                    lambda m, a: m.become(
                        start_arc.copy().pointwise_become_partial(
                            start_arc, 0, interpolate(last_frac, frac, a)
                        )
                    )
                ),
                run_time=3
            )
            last_frac = frac
            self.wait()
