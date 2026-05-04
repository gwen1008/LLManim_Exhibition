# Source: 3b1b/_2019/diffyq/part4/complex_functions.py
# Description: [3b1b translated] 展示餘弦波在實數軸上的輸出，過渡到複數平面，並用兩個旋轉向量解釋餘弦函數的複數表示。


from manim import *
import numpy as np

class GeneralizeToComplexFunctions(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.axes_config = {
            "x_range": [0, 10],
            "y_range": [-2.5, 2.5],
            "x_length": 10,
            "y_length": 5,
            "axis_config": {
                "stroke_width": 2,
            },
            "y_axis_config": {
                "tick_frequency": 0.25,
                "unit_size": 1.5,
                "include_tip": False,
                "stroke_width": 2,
            },
        }
        self.complex_plane_config = {
            "axis_config": {
                "unit_size": 2
            }
        }

    def construct(self):
        self.show_cosine_wave()
        self.transition_to_complex_plane()
        self.add_rotating_vectors_making_cos()

    def show_cosine_wave(self):
        axes = Axes(**self.axes_config)
        axes.shift(2 * LEFT - axes.c2p(0, 0))
        y_axis = axes.y_axis
        y_labels = VGroup(*[
            DecimalNumber(
                num,
                num_decimal_places=1,
                font_size=24
            ).next_to(
                axes.c2p(0, num),
                LEFT,
                buff=SMALL_BUFF
            )
            for num in range(-2, 3)
        ])

        t_tracker = ValueTracker(0)
        t_tracker.add_updater(lambda t: t.increment_value(self.frame_rate * self.dt))
        get_t = t_tracker.get_value

        def func(x):
            return 2 * np.cos(x)

        cos_x_max = 20
        cos_wave = axes.plot(func, x_range=[0, cos_x_max], color=YELLOW)
        shown_cos_wave = cos_wave.copy()
        shown_cos_wave.add_updater(
            lambda m: m.become(
                axes.plot(
                    func,
                    x_range=[0, np.clip(get_t(), 0, cos_x_max)],
                    color=YELLOW
                )
            )
        )

        dot = Dot(color=PINK)
        dot.add_updater(lambda d: d.move_to(
            axes.c2p(0, func(get_t())),
        ))

        h_line = always_redraw(lambda: Line(
            dot.get_right(),
            shown_cos_wave.get_end(),
            stroke_width=1,
        ))

        real_words = Text(
            "Real number\noutput",
            font_size=36
        )
        real_words.to_edge(LEFT)
        real_words.shift(2 * UP)
        real_arrow = Arrow()
        real_arrow.add_updater(
            lambda m: m.put_start_and_end_on(
                real_words.get_corner(DR),
                dot.get_center(),
            ).scale(0.9),
        )

        self.add(t_tracker)
        self.add(axes)
        self.add(y_labels)
        self.add(shown_cos_wave)
        self.add(dot)
        self.add(h_line)

        self.wait(2)
        self.play(
            FadeIn(real_words, shift=RIGHT),
            FadeIn(real_arrow),
        )
        self.wait(5)

        y_axis.generate_target()
        y_axis.target.rotate(-90 * DEGREES)
        y_axis.target.center()
        y_axis.target.scale(2 / 1.5)
        y_labels.generate_target()
        for label in y_labels.target:
            label.next_to(
                axes.c2p(0, label.get_value()),
                DOWN, MED_SMALL_BUFF,
            )
        self.play(
            FadeOut(shown_cos_wave),
            FadeOut(axes.x_axis),
            FadeOut(h_line),
        )
        self.play(
            MoveToTarget(y_axis),
            MoveToTarget(y_labels),
            real_words.animate.shift(2 * RIGHT + UP),
        )
        self.wait()

        self.y_axis = y_axis
        self.y_labels = y_labels
        self.real_words = real_words
        self.real_arrow = real_arrow
        self.dot = dot
        self.t_tracker = t_tracker

    def transition_to_complex_plane(self):
        y_axis = self.y_axis
        y_labels = self.y_labels

        plane = self.get_complex_plane()
        plane_words = plane.label

        self.add(plane, *self.mobjects)
        self.play(
            FadeOut(y_labels),
            FadeOut(y_axis),
            Create(plane),
        )
        self.play(Write(plane_words))
        self.wait()

        self.plane = plane
        self.plane_words = plane_words

    def add_rotating_vectors_making_cos(self):
        plane = self.plane
        real_words = self.real_words
        real_arrow = self.real_arrow
        t_tracker = self.t_tracker
        get_t = t_tracker.get_value

        v1 = Vector(2 * RIGHT, color=BLUE)
        v2 = Vector(2 * RIGHT, color=interpolate_color(GREY_BROWN, WHITE, 0.5))
        v1.add_updater(
            lambda v: v.set_angle(get_t())
        )
        v2.add_updater(
            lambda v: v.set_angle(-get_t())
        )
        v1.add_updater(
            lambda v: v.shift(plane.c2p(0, 0) - v.get_start())
        )
        v2.add_updater(
            lambda v: v.shift(plane.c2p(0, 0) - v.get_start())
        )

        ghost_v1 = v1.copy()
        ghost_v1.set_opacity(0.5)
        ghost_v1.add_updater(
            lambda v: v.shift(
                v2.get_end() - v.get_start()
            )
        )

        ghost_v2 = v2.copy()
        ghost_v2.set_opacity(0.5)
        ghost_v2.add_updater(
            lambda v: v.shift(
                v1.get_end() - v.get_start()
            )
        )

        circle = Circle(color=GREY_BROWN, radius=v1.get_length())
        circle.set_stroke(width=1)
        circle.move_to(plane.c2p(0, 0))

        formula = MathTex(
            "2\\cos(x) =",
            "e^{ix}", "+", "e^{-ix}",
            tex_to_color_map={
                "e^{ix}": v1.get_color(),
                "e^{-ix}": v2.get_color(),
            }
        )
        formula.next_to(ORIGIN, UP, buff=0.75)
        formula.set_stroke(BLACK, 3, background=True)
        formula.to_edge(LEFT, buff=MED_SMALL_BUFF)
        formula_brace = Brace(formula[1:], UP)
        formula_words = formula_brace.get_text(
            "Sum of\nrotations"
        )
        formula_words.set_stroke(BLACK, 3, background=True)

        randy = Randolph()
        randy.to_corner(DL)
        randy.look_at(formula)

        self.play(
            FadeOut(real_words),
            FadeOut(real_arrow),
        )
        self.play(
            FadeIn(v1),
            FadeIn(v2),
            FadeIn(circle),
            FadeIn(ghost_v1),
            FadeIn(ghost_v2),
        )
        self.wait(3)
        self.play(FadeIn(formula, shift=DOWN))
        self.play(
            GrowFromCenter(formula_brace),
            FadeIn(formula_words),
        )
        self.wait(2)
        self.play(FadeIn(randy))
        self.play(randy.animate.change("pleading"))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.animate.change("confused"))
        self.play(Blink(randy))
        self.wait()
        self.play(FadeOut(randy))
        self.wait(20)

    def get_complex_plane(self):
        plane = ComplexPlane(
            x_range=[-3, 3],
            y_range=[-3, 3],
            **self.complex_plane_config
        )
        plane.add_coordinates()

        plane.label = Text("Complex plane", font_size=36)
        plane.label.scale(1.5)
        plane.label.to_corner(UR, buff=MED_SMALL_BUFF)
        return plane
