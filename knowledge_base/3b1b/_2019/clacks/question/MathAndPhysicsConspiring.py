# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示數學與物理兩個領域的標題和相關圖形元素從下方淡入，同時一條垂直線從中心展開的動畫過程。



from manim import *
class MathAndPhysicsConspiring(Scene):
    def construct(self):
        v_line = Line(DOWN, UP).scale(config.frame_height)
        v_line.save_state()
        v_line.set_opacity(0)
        v_line.scale(0)
        
        math_title = Text("Math")
        math_title.set_color(BLUE)
        physics_title = Text("Physics")
        physics_title.set_color(YELLOW)
        
        for title, vect in [(math_title, LEFT), (physics_title, RIGHT)]:
            title.scale(2)
            title.shift(vect * config.frame_width / 4)
            title.to_edge(UP)

        math_stuffs = VGroup(
            MathTex("\\pi = {:.16}\\dots".format(PI)),
            self.get_tangent_image(),
        )
        math_stuffs.arrange(DOWN, buff=MED_LARGE_BUFF)
        math_stuffs.next_to(math_title, DOWN, LARGE_BUFF)
        to_fade = VGroup(math_title, *math_stuffs, physics_title)

        self.play(
            LaggedStart(
                *[FadeIn(obj, shift=DOWN) for obj in to_fade],
                lag_ratio=0.7,
                run_time=3,
            ),
            Restore(v_line, run_time=2, path_arc=PI / 2),
        )
        self.wait()

    def get_tangent_image(self):
        axes = Axes(
            x_range=[-1.5, 1.5],
            y_range=[-1.5, 1.5],
        )
        circle = Circle()
        circle.set_color(WHITE)
        theta = 30 * DEGREES
        arc = Arc(angle=theta, radius=0.4)
        theta_label = MathTex("\\theta")
        theta_label.scale(0.5)
        theta_label.next_to(arc.get_center(), RIGHT, buff=SMALL_BUFF)
        theta_label.shift(0.025 * UL)
        line = Line(ORIGIN, rotate_vector(RIGHT, theta))
        line.set_color(WHITE)
        one = MathTex("1").scale(0.5)
        one.next_to(line.point_from_proportion(0.7), UL, 0.5 * SMALL_BUFF)
        tan_line = Line(
            line.get_end(),
            (1.0 / np.cos(theta)) * RIGHT
        )
        tan_line.set_color(RED)
        tan_text = MathTex("\\tan(\\theta)")
        tan_text.rotate(tan_line.get_angle())
        tan_text.scale(0.5)
        tan_text.move_to(tan_line)
        tan_text.set_color(tan_line.get_color())
        tan_text.shift(0.2 * normalize(line.get_vector()))

        result = VGroup(
            axes, circle,
            line, one,
            arc, theta_label,
            tan_line, tan_text,
        )
        result.set_height(4)
        return result
