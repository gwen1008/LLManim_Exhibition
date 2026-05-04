# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示一個圓形從四分之一圓弧動態擴展成完整圓形，並在過程中顯示 π/2 和 τ/4 的數學標記。



from manim import *
class QuarterTurn(Scene):
    def construct(self):
        terms, generate_anims1, generate_anims2 = get_circle_drawing_terms(
            radius = 2,
            positioning_func = lambda circ : circ.move_to(4*RIGHT)
        )
        circle, radius, one, decimal = terms
        circle_ghost = circle.copy().set_stroke(YELLOW_E, 1)
        radius_ghost = radius.copy().set_stroke(WHITE, 1)

        self.add(circle_ghost, radius_ghost)
        self.play(
            *generate_anims2(),
            rate_func = lambda t : 0.25*smooth(t)
        )
        self.wait()

        pi_halves = MathTex("\\pi", "/2")
        pi_halves[0].set_color(RED)
        tau_fourths = MathTex("\\tau", "/4")
        tau_fourths[0].set_color(GREEN)
        for mob in pi_halves, tau_fourths:
            mob.next_to(decimal, UP)

        self.play(FadeIn(pi_halves, shift=DOWN))
        self.wait()
        self.play(
            pi_halves.animate.shift(0.75*UP),
            FadeIn(tau_fourths, shift=DOWN)
        )
        self.wait()
