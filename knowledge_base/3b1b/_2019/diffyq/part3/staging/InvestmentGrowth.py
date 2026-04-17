# Source: 3b1b/_2019/diffyq/part3/staging.py
# Description: [3b1b translated] 展示投資隨時間指數增長的動畫，包含坐標軸、增長曲線和微分方程公式。


from manim import *
import numpy as np

class InvestmentGrowth(Scene):
    def __init__(
        self,
        output_tex="{M}",
        output_color=GREEN,
        initial_value=1,
        initial_value_tex="{M_0}",
        k=0.05,
        k_tex="0.05",
        total_time=43,
        time_rate=3,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.output_tex = output_tex
        self.output_color = output_color
        self.initial_value = initial_value
        self.initial_value_tex = initial_value_tex
        self.k = k
        self.k_tex = k_tex
        self.total_time = total_time
        self.time_rate = time_rate

    def construct(self):
        # Axes
        axes = Axes(
            x_range=[0, self.total_time, 5],
            y_range=[0, 6, 1],
            x_length=self.total_time * 0.3,
            axis_config={
                "include_numbers": True,
                "font_size": 24,
            },
            x_axis_config={
                "numbers_to_include": range(0, self.total_time, 5),
            },
        )
        axes.to_corner(DL, buff=LARGE_BUFF)

        time_label = Text("Time", font_size=24)
        time_label.next_to(
            axes.x_axis.get_right(),
            UP, MED_LARGE_BUFF
        )
        time_label.shift_onto_screen()
        axes.x_axis.add(time_label)
        
        money_label = MathTex(self.output_tex)
        money_label.set_color(self.output_color)
        money_label.next_to(
            axes.y_axis.get_top(),
            UP,
        )
        axes.y_axis.add(money_label)

        # Graph
        graph = axes.plot(
            lambda x: self.initial_value * np.exp(self.k * x),
            color=self.output_color
        )
        full_graph = graph.copy()
        time_tracker = self.get_time_tracker()
        
        def update_graph(m):
            t = time_tracker.get_value()
            proportion = np.clip(t / self.total_time, 0, 1)
            m.become(axes.plot(
                lambda x: self.initial_value * np.exp(self.k * x),
                x_range=[0, self.total_time * proportion],
                color=self.output_color
            ))
        
        graph.add_updater(update_graph)

        # Equation
        tex_kwargs = {
            "tex_to_color_map": {
                self.output_tex: self.output_color,
                self.initial_value_tex: BLUE,
            }
        }
        ode = MathTex(
            "{d",
            "\\over dt}",
            self.output_tex,
            "(t)",
            "=", self.k_tex,
            "\\cdot", self.output_tex, "(t)",
            **tex_kwargs
        )
        ode.to_edge(UP)
        
        exp = MathTex(
            self.output_tex,
            "(t) =", self.initial_value_tex,
            "e^{", self.k_tex, "t}",
            **tex_kwargs
        )
        exp.next_to(ode, DOWN, LARGE_BUFF)

        M0_part = exp.get_part_by_tex(self.initial_value_tex)
        exp_part = exp[-3:]
        M0_label = M0_part.copy()
        M0_label.next_to(
            axes.c2p(0, self.initial_value),
            LEFT
        )
        M0_part.set_opacity(0)
        exp_part.save_state()
        exp_part.align_to(M0_part, LEFT)

        self.add(axes)
        self.add(graph)
        self.add(time_tracker)

        self.play(FadeIn(ode, shift=DOWN))
        self.wait(6)
        self.play(FadeIn(exp, shift=UP))
        self.wait(2)
        self.play(
            Restore(exp_part),
            M0_part.animate.set_opacity(1),
        )
        self.play(TransformFromCopy(
            M0_part, M0_label
        ))
        self.wait(5)

    def get_time_tracker(self):
        time_tracker = ValueTracker(0)
        time_tracker.add_updater(
            lambda m, dt: m.increment_value(
                self.time_rate * dt
            )
        )
        return time_tracker
