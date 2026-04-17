# Source: 3b1b/_2019/diffyq/part1/pendulum.py
# Description: [3b1b translated] 展示低角度單擺的擺動與其理論預測的餘弦函數圖形對比，並標示初始角度。



from manim import *
class LowAnglePendulum(Scene):
    def __init__(
        self,
        pendulum_config={
            "initial_theta": 20 * DEGREES,
            "length": 2.0,
            "damping": 0,
            "top_point": ORIGIN,
        },
        axes_config={
            "y_axis_config": {"unit_size": 0.75},
            "x_axis_config": {
                "unit_size": 0.5,
                "numbers_to_show": range(2, 25, 2),
                "number_scale_val": 0.5,
            },
            "x_max": 25,
            "axis_config": {
                "tip_length": 0.3,
                "stroke_width": 2,
            }
        },
        axes_corner=UL,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.pendulum_config = pendulum_config
        self.axes_config = axes_config
        self.axes_corner = axes_corner

    def construct(self):
        # 注意：Pendulum 和 ThetaVsTAxes 是自定義類別，需要額外定義
        # 這裡假設它們已存在或需要自行實現
        pendulum = Pendulum(**self.pendulum_config)
        axes = ThetaVsTAxes(**self.axes_config)
        axes.center()
        axes.to_corner(self.axes_corner, buff=LARGE_BUFF)
        graph = axes.get_live_drawn_graph(pendulum)

        L = pendulum.length
        g = pendulum.gravity
        theta0 = pendulum.initial_theta
        prediction = axes.plot(
            lambda t: theta0 * np.cos(t * np.sqrt(g / L))
        )
        dashed_prediction = DashedVMobject(prediction, num_dashes=300)
        dashed_prediction.set_stroke(WHITE, 1)
        prediction_formula = MathTex(
            "\\theta_0", "\\cos(\\sqrt{g / L} \\cdot t)"
        )
        prediction_formula.scale(0.75)
        prediction_formula.next_to(
            dashed_prediction, UP, buff=SMALL_BUFF,
        )

        theta0_part = prediction_formula.get_part_by_tex("\\theta_0")
        theta0_brace = Brace(theta0_part, UP, buff=SMALL_BUFF)
        theta0_brace.stretch(0.5, 1, about_edge=DOWN)
        theta0_label = Integer(
            pendulum.initial_theta * 180 / PI,
            unit="^\\circ"
        )
        theta0_label.scale(0.75)
        theta0_label.next_to(theta0_brace, UP, buff=SMALL_BUFF)

        group = VGroup(theta0_brace, theta0_label, prediction_formula)
        # ManimCE 沒有 shift_onto_screen，用 to_edge 替代
        group.to_edge(UP, buff=MED_SMALL_BUFF)

        self.add(axes, dashed_prediction, pendulum)
        self.play(
            Create(dashed_prediction, run_time=2),
            FadeIn(prediction_formula, shift=DOWN),
            FadeIn(theta0_brace, shift=DOWN),
            FadeIn(theta0_label, shift=DOWN),
        )
        self.play(
            # ShowCreationThenFadeAround 在 CE 中為 Indicate 或自訂
            Indicate(theta0_label),
            Indicate(pendulum.theta_label),
        )
        self.wait()

        pendulum.start_swinging()
        self.add(graph)
        self.wait(30)
