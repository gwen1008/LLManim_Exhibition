# Source: 3b1b/_2019/diffyq/part3/staging.py
# Description: [3b1b translated] 展示傅立葉系列與傅立葉變換的多種變體文字從兩側淡入再淡出的過程。



from manim import *
class ManyCousinsOfFourierThings(Scene):
    def construct(self):
        series_variants = VGroup(
            Text("Complex Fourier Series"),
            Text("Discrete Fourier Series"),
        )
        transform_variants = VGroup(
            Text("Discrete Fourier Transform"),
            Text("Fast Fourier Transform"),
            Text("Quantum Fourier Transform"),
        )
        groups = VGroup(series_variants, transform_variants)
        for group, vect in zip(groups, [LEFT, RIGHT]):
            group.scale(0.7)
            group.arrange(DOWN, aligned_edge=LEFT)
            group.move_to(
                vect * config.frame_width / 4
            )
            group.set_color(YELLOW)

        self.play(*[
            LaggedStartMap(FadeIn, group)
            for group in groups
        ])
        self.play(*[
            LaggedStartMap(FadeOut, group)
            for group in groups
        ])
