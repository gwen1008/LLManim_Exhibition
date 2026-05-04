# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示一個藍色 PiCreature 思考左右兩側數學陳述的對比，包括無窮級數、導數定義和除以零的定義問題。



from manim import *
class WhatIsRight(PiCreatureScene):
    def __init__(
        self,
        default_pi_creature_kwargs={
            "color": BLUE_D,
            "flip_at_start": False,
        },
        default_pi_creature_start_corner=DOWN,
        **kwargs
    ):
        super().__init__(
            default_pi_creature_kwargs=default_pi_creature_kwargs,
            default_pi_creature_start_corner=default_pi_creature_start_corner,
            **kwargs
        )

    def construct(self):
        randy = self.pi_creature
        randy.scale(0.75, about_edge=DOWN)
        title = Tex("Which is ``right''?")
        title.scale(1.5)
        title.to_edge(UP)
        self.add(title)

        sum_over_N_converges = MathTex("1+2+3+\\cdots = -\\frac{1}{12}")
        sum_over_N_diverges = MathTex("1+2+3+\\cdots \\text{ Diverges}")

        literal_derivative = MathTex(
            "f'(x) = \\frac{f(x+dx) - f(x)}{dx}"
        )
        limit_derivative = MathTex(
            "f'(x) = \\lim_{h \\to 0}\\frac{f(x+h) - f(x)}{h}"
        )

        divide_by_zero_definable = MathTex(
            "\\frac{1}{0}", "\\text{ has meaning}"
        )
        divide_by_zero_undefinable = MathTex(
            "\\frac{1}{0}", "\\text{ is undefined}"
        )

        left_mobs = VGroup(
            sum_over_N_converges, literal_derivative,
            divide_by_zero_definable
        )
        right_mobs = VGroup(
            sum_over_N_diverges, limit_derivative,
            divide_by_zero_undefinable
        )

        for mob in left_mobs:
            mob.next_to(randy, UP)
            mob.shift(3.5 * LEFT)
        for mob in right_mobs:
            mob.next_to(randy, UP)
            mob.shift(3.5 * RIGHT)

        left_mobs.set_color_by_gradient(YELLOW_C, YELLOW_D)
        right_mobs.set_color_by_gradient(GREEN_C, GREEN_D)

        self.play(randy.change("pondering"), title)
        self.wait()
        self.play(randy.change("sassy"), title)
        self.wait()

        last_terms = VGroup()
        for left, right in zip(left_mobs, right_mobs)[:-1]:
            right.align_to(left)
            self.play(
                randy.change("raise_right_hand"),
                FadeIn(left, shift=DOWN),
                last_terms.animate.shift(1.75 * UP)
            )
            self.wait()
            self.play(
                randy.change("raise_left_hand"),
                FadeIn(right, shift=DOWN)
            )
            self.play(randy.change("plain"), right)
            last_terms.add(left, right, title)
        self.play(
            randy.change("shruggie"),
            FadeIn(left_mobs[-1], shift=DOWN),
            FadeIn(right_mobs[-1], shift=DOWN),
            last_terms.animate.shift(1.75 * UP),
        )
        self.wait(4)
