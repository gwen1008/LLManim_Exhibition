from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = MathTex(r"u(x,t) = \sin(x - ct)").to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            y_length=4,
            axis_config={"include_tip": False},
        ).shift(DOWN * 0.3)
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("u")
        self.play(Create(axes), Write(x_label), Write(y_label))

        c = 1.5
        t = ValueTracker(0)

        wave = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(x - c * t.get_value()),
                x_range=[0, 4 * PI],
                color=BLUE,
            )
        )

        t_label = always_redraw(
            lambda: MathTex(f"t = {t.get_value():.2f}").to_corner(UR).shift(DOWN * 0.5)
        )

        c_label = MathTex(f"c = {c}").next_to(t_label, DOWN, aligned_edge=RIGHT)

        self.add(wave, t_label, c_label)
        self.play(t.animate.set_value(2 * PI / c), run_time=6, rate_func=linear)
        self.wait(0.5)

        arrow = Arrow(
            start=axes.c2p(PI, 1.2),
            end=axes.c2p(2 * PI, 1.2),
            color=YELLOW,
            buff=0,
        )
        prop = Text("向右傳播", font_size=24).next_to(arrow, UP, buff=0.1)
        self.play(GrowArrow(arrow), FadeIn(prop))
        self.play(t.animate.set_value(4 * PI / c), run_time=4, rate_func=linear)
        self.wait(1)