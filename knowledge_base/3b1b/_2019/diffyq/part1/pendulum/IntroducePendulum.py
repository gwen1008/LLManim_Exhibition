# Source: 3b1b/_2019/diffyq/part1/pendulum.py
# Description: [3b1b translated] 展示單擺運動及其對應的θ-t正弦曲線圖，並標註週期公式與物理參數（擺長、重力）的視覺化關聯。


from manim import *
import numpy as np

class IntroducePendulum(Scene):
    def __init__(
        self,
        pendulum_config=None,
        theta_vs_t_axes_config=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        if pendulum_config is None:
            pendulum_config = {
                "length": 3,
                "top_point": 4 * RIGHT,
                "weight_diameter": 0.35,
                "gravity": 20,
            }
        if theta_vs_t_axes_config is None:
            theta_vs_t_axes_config = {
                "y_max": PI / 4,
                "y_min": -PI / 4,
                "y_axis_config": {
                    "tick_frequency": PI / 16,
                    "unit_size": 2,
                    "tip_length": 0.3,
                },
                "x_max": 12,
                "axis_config": {
                    "stroke_width": 2,
                }
            }
        self.pendulum_config = pendulum_config
        self.theta_vs_t_axes_config = theta_vs_t_axes_config

    def construct(self):
        self.add_pendulum()
        self.label_pendulum()
        self.add_graph()
        self.label_function()
        self.show_graph_period()
        self.show_length_and_gravity()

    def add_pendulum(self):
        # 注意：Pendulum 類別需要自行定義或從原專案移植
        pendulum = self.pendulum = Pendulum(**self.pendulum_config)
        pendulum.start_swinging()
        frame = self.camera.frame
        frame.save_state()
        frame.scale(0.5)
        frame.move_to(pendulum.dashed_line)

        self.add(pendulum, frame)

    def label_pendulum(self):
        pendulum = self.pendulum
        label = pendulum.theta_label
        rect = SurroundingRectangle(label, buff=0.5 * SMALL_BUFF)
        rect.add_updater(lambda r: r.move_to(label))

        self.wait(3)
        self.play(Create(rect))
        self.play(FadeOut(rect))
        self.wait()

    def add_graph(self):
        axes = self.axes = ThetaVsTAxes(**self.theta_vs_t_axes_config)
        axes.y_axis.label.next_to(axes.y_axis, UP, buff=0)
        axes.to_corner(UL)

        self.play(
            Restore(
                self.camera.frame,
                rate_func=lambda t: squish_rate_func(smooth, 0, 0.9)(t),
            ),
            Create(axes),
            Transform(
                self.pendulum.theta_label.copy().clear_updaters(),
                axes.y_axis.label.copy(),
                rate_func=lambda t: squish_rate_func(smooth, 0, 0.8)(t),
            ),
            run_time=3,
        )

        self.wait(1.5)
        self.graph = axes.get_live_drawn_graph(self.pendulum)
        self.add(self.graph)

    def label_function(self):
        hm_word = Text("Simple harmonic motion")
        hm_word.scale(1.25)
        hm_word.to_edge(UP)

        formula = MathTex("=\\theta_0 \\cos(\\sqrt{g / L} t)")
        formula.next_to(
            self.axes.y_axis_label, RIGHT, SMALL_BUFF
        )
        formula.set_stroke(width=0, background=True)

        self.play(FadeIn(hm_word, shift=DOWN))
        self.wait()
        self.play(
            Write(formula),
            hm_word.animate.to_corner(UR)
        )
        self.wait(4)

    def show_graph_period(self):
        pendulum = self.pendulum
        axes = self.axes

        period = self.period = TAU * np.sqrt(
            pendulum.length / pendulum.gravity
        )
        amplitude = pendulum.initial_theta

        line = Line(
            axes.c2p(0, amplitude),
            axes.c2p(period, amplitude),
        )
        line.shift(SMALL_BUFF * RIGHT)
        brace = Brace(line, UP, buff=SMALL_BUFF)
        brace.add_to_back(brace.copy().set_style(stroke_color=BLACK, stroke_width=10))
        formula = get_period_formula()
        formula.next_to(brace, UP, SMALL_BUFF)

        self.period_formula = formula
        self.period_brace = brace

        self.play(
            GrowFromCenter(brace),
            FadeIn(formula, shift=DOWN),
        )
        self.wait(2)

    def show_length_and_gravity(self):
        formula = self.period_formula
        L = formula.get_part_by_tex("L")
        g = formula.get_part_by_tex("g")

        rod = self.pendulum.rod
        new_rod = rod.copy()
        new_rod.set_stroke(BLUE, 7)
        new_rod.add_updater(lambda r: r.put_start_and_end_on(
            *rod.get_start_and_end()
        ))

        g_vect = GravityVector(
            self.pendulum,
            length_multiple=0.5 / 9.8,
        )
        down_vectors = self.get_down_vectors()
        down_vectors.set_color(YELLOW)
        down_vectors.set_opacity(0.5)

        self.play(
            Create(SurroundingRectangle(L)),
            Create(new_rod),
        )
        self.play(FadeOut(new_rod))

        self.play(
            Create(SurroundingRectangle(g)),
            GrowArrow(g_vect),
        )
        self.play(self.get_down_vectors_animation(down_vectors))
        self.wait(6)

        self.gravity_vector = g_vect

    def get_down_vectors(self):
        down_vectors = VGroup(*[
            Vector(0.5 * DOWN)
            for x in range(10 * 150)
        ])
        down_vectors.arrange_in_grid(10, 150, buff=MED_SMALL_BUFF)
        down_vectors.set_color_by_gradient(BLUE, RED)
        down_vectors.to_edge(RIGHT)
        return down_vectors

    def get_down_vectors_animation(self, down_vectors):
        return LaggedStart(
            *[
                GrowArrow(v, rate_func=there_and_back)
                for v in down_vectors
            ],
            lag_ratio=0.0005,
            run_time=2,
            remover=True
        )
