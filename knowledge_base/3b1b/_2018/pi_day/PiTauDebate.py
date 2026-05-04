# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示 Pi 和 Tau 兩個角色爭論圓周率與圓周率兩倍的數值，並分別用圓的周長與直徑的關係來視覺化這兩個常數。



from manim import *
class PiTauDebate(PiCreatureScene):
    def construct(self):
        pi, tau = self.pi, self.tau
        self.add(pi, tau)

        pi_value = Text("3.1415...!", color=BLUE)
        tau_value = Text("6.2831...!", color=GREEN)

        self.play(PiCreatureSays(
            pi, pi_value,
            target_mode="angry",
            look_at=tau.eyes,
        ))
        self.play(PiCreatureSays(
            tau, tau_value,
            target_mode="angry",
            look_at=pi.eyes,
            bubble_config={"width": 3, "height": 2},
        ))
        self.wait()

        # Show tau
        terms, generate_anims1, generate_anims2 = get_circle_drawing_terms(
            radius=1.25,
            positioning_func=lambda m: m.to_edge(RIGHT, buff=2).to_edge(UP, buff=1)
        )
        circle, radius, one, decimal = terms

        self.play(
            RemovePiCreatureBubble(pi),
            RemovePiCreatureBubble(tau),
            *generate_anims1()
        )
        self.play(
            tau.animate.change("hooray"),
            pi.animate.change("sassy"),
            *generate_anims2()
        )
        self.wait()

        # Show pi
        circle = Circle(color=RED, radius=1.25/2)
        circle.rotate(TAU/4)
        circle.move_to(pi)
        circle.to_edge(UP, buff=MED_LARGE_BUFF)
        diameter = Line(circle.get_left(), circle.get_right())
        one = MathTex("1")
        one.scale(0.75)
        one.next_to(diameter, UP, buff=SMALL_BUFF)

        circum_line = diameter.copy().scale(np.pi)
        circum_line.set_style(stroke_color=circle.get_color(), stroke_width=circle.get_stroke_width())
        circum_line.next_to(circle, DOWN, buff=MED_LARGE_BUFF)
        brace = Brace(circum_line, DOWN, buff=SMALL_BUFF)
        decimal = DecimalNumber(np.pi, num_decimal_places=4, include_sign=False)
        decimal.scale(0.75)
        decimal.next_to(brace, DOWN, buff=SMALL_BUFF)

        self.play(
            FadeIn(VGroup(circle, diameter, one)),
            tau.animate.change("confused"),
            pi.animate.change("hooray")
        )
        self.add(circle.copy().set_opacity(0.5))
        self.play(
            ReplacementTransform(circle, circum_line, run_time=2)
        )
        self.play(GrowFromCenter(brace), Write(decimal))
        self.wait(3)

    def create_pi_creatures(self):
        pi = self.pi = Randolph()
        pi.to_edge(DOWN).shift(4*LEFT)
        tau = self.tau = TauCreature(
            file_name_prefix="TauCreatures",
            color=GREEN_E
        ).flip()
        tau.to_edge(DOWN).shift(4*RIGHT)
        return VGroup(pi, tau)
