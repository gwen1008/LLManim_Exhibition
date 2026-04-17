# Source: 3b1b/_2019/diffyq/part1/pendulum.py
# Description: [3b1b translated] 展示一個擺錘從線性化到混沌的轉變過程，包含彈簧系統和公式的動畫。



from manim import *
class WherePendulumLeads(PiCreatureScene):
    def construct(self):
        pendulum = Pendulum(
            top_point=UP,
            length=3,
            gravity=20,
        )
        pendulum.start_swinging()

        l_title = Tex("Linearization")
        l_title.scale(1.5)
        l_title.to_corner(UL)
        c_title = Tex("Chaos")
        c_title.scale(1.5)
        c_title.move_to(l_title)
        c_title.move_to(
            c_title.get_center() * np.array([-1, 1, 1])
        )

        get_theta = pendulum.get_theta
        spring = always_redraw(
            lambda: ParametricFunction(
                lambda t: np.array([
                    np.cos(TAU * t) + (1.4 + get_theta()) * t,
                    np.sin(TAU * t) - 0.5,
                    0,
                ]),
                t_range=[-0.5, 7],
                color=GREY,
                stroke_width=2,
            ).scale(0.2).to_edge(LEFT, buff=0)
        )
        spring_rect = SurroundingRectangle(
            spring, buff=MED_LARGE_BUFF,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=0,
        )

        weight = Dot(radius=0.25)
        weight.add_updater(lambda m: m.move_to(
            spring.get_points()[-1]
        ))
        weight.set_color(BLUE)
        spring_system = VGroup(spring, weight)

        linear_formula = MathTex(
            "\\frac{d \\vec{\\textbf{x}}}{dt}="
            "A\\vec{\\textbf{x}}"
        )
        linear_formula.next_to(spring, UP, LARGE_BUFF)
        linear_formula.match_x(l_title)

        randy = self.pi_creature
        randy.set_height(2)
        randy.center()
        randy.to_edge(DOWN)
        randy.shift(3 * LEFT)
        q_marks = MathTex("???")
        q_marks.next_to(randy, UP)

        self.add(pendulum, randy)
        self.play(
            randy.animate.change("pondering", pendulum),
            FadeIn(q_marks, shift=DOWN, lag_ratio=0.3)
        )
        self.play(randy.animate.look_at(pendulum))
        self.wait(5)
        self.play(
            Animation(VectorizedPoint(pendulum.get_top())),
            FadeOut(q_marks, shift=UP, lag_ratio=0.3),
        )
        self.add(spring_system)
        self.play(
            FadeOut(spring_rect),
            FadeIn(linear_formula, shift=UP),
            FadeIn(l_title, shift=DOWN),
        )
        self.play(FadeIn(c_title, shift=DOWN))
        self.wait(8)
