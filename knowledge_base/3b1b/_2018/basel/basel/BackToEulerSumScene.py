# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示一個數線上的燈塔發光，光強度指示器沿數線移動並收集到思想泡泡中，最後匯總成 π²/6 的過程。



from manim import *
class BackToEulerSumScene(PiCreatureScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_pi_creature_class = Randolph

    def construct(self):
        self.remove(self.get_primary_pi_creature())

        NUM_CONES = 7
        NUM_VISIBLE_CONES = 6
        INDICATOR_RADIUS = 0.5
        OPACITY_FOR_UNIT_INTENSITY = 1.0

        self.number_line = NumberLine(
            x_range=[0, 5, 1],
            length=8,
            color=WHITE,
            stroke_width=1,
            include_numbers=True,
            numbers_to_include=list(range(1, 5)),
            label_direction=DOWN,
        )
        self.number_line_labels = self.number_line.get_number_mobjects()
        self.add(self.number_line, self.number_line_labels)
        self.wait()

        origin_point = self.number_line.number_to_point(0)

        randy = self.get_primary_pi_creature()
        randy.scale(0.5)
        randy.flip()
        right_pupil = randy.pupils[1]
        randy.next_to(origin_point, LEFT, buff=0)
        randy.align_to(right_pupil, RIGHT)

        bubble = ThoughtBubble(
            direction=RIGHT,
            width=4,
            height=3,
        )
        bubble.next_to(randy, LEFT + UP)
        bubble.set_fill(color=BLACK, opacity=1)

        self.play(
            randy.change("wave_2"),
            Create(bubble),
        )

        euler_sum = MathTex("1", "+", "{1\\over 4}",
                            "+", "{1\\over 9}", "+", "{1\\over 16}", "+", "{1\\over 25}", "+", "\\cdots", " ")

        intensities = np.array([1. / (n + 1) ** 2 for n in range(NUM_CONES)])
        opacities = intensities * OPACITY_FOR_UNIT_INTENSITY

        point = self.number_line.number_to_point(1)
        v = point - self.number_line.number_to_point(0)

        # 模擬 LightSource
        lighthouse = Dot(point, color=YELLOW, radius=0.2)
        ambient_light = Circle(radius=0.5, color=YELLOW, fill_opacity=0.3).move_to(point)

        self.play(FadeIn(lighthouse))
        self.play(FadeIn(ambient_light))

        # 模擬 LightIndicator
        indicator = Circle(
            radius=INDICATOR_RADIUS,
            color=LIGHT_COLOR,
            fill_opacity=opacities[0],
            stroke_width=2
        ).move_to(point)
        indicator_reading = euler_sum[0].copy()
        indicator_reading.set_height(0.5 * indicator.get_height())
        indicator_reading.move_to(indicator.get_center())
        indicator.add(indicator_reading)
        indicator.tex_reading = indicator_reading
        indicator.tex_reading.set_fill(color=BLACK)

        self.play(FadeIn(indicator))
        self.add_foreground_mobject(indicator)

        collection_point = np.array([-6., 2., 0.])
        left_shift = 0.2 * LEFT
        collected_indicators = VGroup()

        for i in range(2, NUM_VISIBLE_CONES + 1):
            previous_point = self.number_line.number_to_point(i - 1)
            point = self.number_line.number_to_point(i)
            v = point - previous_point

            indicator_target = indicator.copy()
            indicator_target.shift(v)

            bubble_indicator = indicator.copy()
            bubble_indicator_target = bubble_indicator.copy()
            bubble_indicator_target.set_fill(opacity=opacities[i - 2])

            euler_sum[2 * i - 4].move_to(bubble_indicator_target)
            bubble_indicator_target.remove(bubble_indicator_target.tex_reading)
            bubble_indicator_target.tex_reading = euler_sum[2 * i - 4].copy()
            bubble_indicator_target.add(bubble_indicator_target.tex_reading)

            if bubble_indicator_target.tex_reading.get_tex_string() != "1":
                bubble_indicator_target.tex_reading.set_height(0.8 * indicator.get_height())
            if intensities[i - 2] < 0.7:
                bubble_indicator.tex_reading.set_fill(color=WHITE)

            bubble_indicator_target.move_to(collection_point)

            self.add_foreground_mobject(bubble_indicator)

            self.wait()

            self.play(
                Transform(bubble_indicator, bubble_indicator_target),
                collected_indicators.animate.shift(left_shift),
            )

            collected_indicators.add(bubble_indicator)

            new_lighthouse = lighthouse.copy()
            new_ambient = ambient_light.copy()

            self.add(new_lighthouse)
            self.play(
                Transform(indicator, indicator_target),
                new_lighthouse.animate.shift(v),
            )
            new_lighthouse.shift(v)
            new_ambient.shift(v)

            self.play(FadeIn(new_ambient))

        # 快速開啟螢幕外的光錐
        for i in range(NUM_VISIBLE_CONES, NUM_CONES):
            ls = Circle(radius=0.5, color=YELLOW, fill_opacity=0.3).move_to(
                self.number_line.number_to_point(i)
            )
            self.play(
                FadeIn(ls, run_time=0.5),
            )

        # 將收集的指示器變形成極限值
        sum_indicator = Circle(
            radius=INDICATOR_RADIUS,
            color=LIGHT_COLOR,
            fill_opacity=opacities[0] * np.pi ** 2 / 6,
            stroke_width=2
        ).move_to(collection_point)
        sum_indicator_reading = MathTex("{\\pi^2 \\over 6}")
        sum_indicator_reading.set_fill(color=BLACK)
        sum_indicator_reading.set_height(0.8 * sum_indicator.get_height())
        sum_indicator.add(sum_indicator_reading)

        self.play(
            FadeOut(collected_indicators),
            FadeIn(sum_indicator)
        )

        self.wait()
