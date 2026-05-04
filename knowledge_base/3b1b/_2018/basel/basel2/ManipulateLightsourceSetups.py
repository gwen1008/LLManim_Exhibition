# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示光源在不同位置時，對觀察者（Morty）的光強度指示器讀數的影響，並演示多個光源的疊加效果。



from manim import *
class ManipulateLightsourceSetups(PiCreatureScene):
    def __init__(self, num_levels=100, radius=10, pi_creature_point=2*LEFT+2*DOWN, **kwargs):
        super().__init__(**kwargs)
        self.num_levels = num_levels
        self.radius = radius
        self.pi_creature_point = pi_creature_point

    def construct(self):
        unit_distance = 3

        # Morty
        morty = self.pi_creature
        observer_point = morty.eyes[1].get_center()

        bubble = ThoughtBubble(height=3, width=4, direction=RIGHT)
        bubble.set_fill(BLACK, 1)
        bubble.pin_to(morty)

        # Indicator
        light_indicator = LightIndicator(
            opacity_for_unit_intensity=0.5,
            fill_color=YELLOW,
            radius=0.4,
            reading_height=0.2,
        )
        light_indicator.move_to(bubble.get_bubble_center())
        def update_light_indicator(light_indicator):
            distance = get_norm(light_source.get_source_point()-observer_point)
            light_indicator.set_intensity((unit_distance/distance)**2)

        # Light source
        light_source = LightSource(
            opacity_function=inverse_quadratic(1, 2, 1),
            num_levels=self.num_levels,
            radius=self.radius,
            max_opacity_ambient=AMBIENT_FULL,
        )
        light_source.move_to(observer_point + unit_distance*RIGHT)

        # Light source copies
        light_source_copies = VGroup(*[light_source.copy() for x in range(2)])
        for lsc, vect in zip(light_source_copies, [RIGHT, UP]):
            lsc.move_to(observer_point + np.sqrt(2)*unit_distance*vect)

        self.add(light_source)
        self.add_foreground_mobjects(morty, bubble, light_indicator)
        light_indicator.add_updater(update_light_indicator)
        self.add(light_indicator)
        self.play(
            light_source.animate.shift(0.66*unit_distance*LEFT),
            morty.animate.change("erm"),
            rate_func=wiggle,
            run_time=5,
        )
        self.play(
            UpdateFromAlphaFunc(
                light_source,
                lambda ls, a: ls.move_to(
                    observer_point + rotate_vector(
                        unit_distance*RIGHT, (1+1./8)*a*TAU
                    )
                ),
                run_time=6,
                rate_func=bezier([0, 0, 1, 1])
            ),
            morty.animate.change("pondering"),
            UpdateFromFunc(morty, lambda m: m.look_at(light_source))
        )
        self.wait()

        plus = MathTex("+")
        point = light_indicator.get_center()
        plus.move_to(point)
        light_indicator_copy = light_indicator.copy()
        self.add_foreground_mobjects(plus, light_indicator_copy)
        self.play(
            ReplacementTransform(
                light_source, light_source_copies[0]
            ),
            ReplacementTransform(
                light_source.copy().set_opacity(0),
                light_source_copies[1]
            ),
            FadeIn(plus),
            UpdateFromFunc(
                light_indicator_copy,
                lambda li: update_light_indicator(li),
            ),
            UpdateFromAlphaFunc(
                light_indicator, lambda m, a: m.move_to(
                    point + a*0.75*RIGHT,
                )
            ),
            UpdateFromAlphaFunc(
                light_indicator_copy, lambda m, a: m.move_to(
                    point + a*0.75*LEFT,
                )
            ),
            run_time=2
        )
        self.play(morty.animate.change("hooray"))
        self.wait(2)

    ##

    def create_pi_creature(self):
        morty = Mortimer()
        morty.flip()
        morty.scale(0.5)
        morty.move_to(self.pi_creature_point)
        return morty
