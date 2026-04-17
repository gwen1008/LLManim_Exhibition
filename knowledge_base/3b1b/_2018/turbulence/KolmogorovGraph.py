# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示 Kolmogorov 湍流能量谱在對數坐標軸上的分佈，包含慣性子區間和比例關係標籤。



from manim import *
class KolmogorovGraph(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-1, 7],
            y_range=[-1, 9],
            y_length=7,  # 替代 y_axis_config 中的 unit_size
            tips=False,
        )
        axes.center().shift(1.5 * RIGHT)
        
        x_label = MathTex("\\log(D)")
        x_label.next_to(axes.x_axis.get_right(), UP)
        
        y_label = MathTex("\\log(\\text{K.E. at length scale D})")
        y_label.scale(0.8)
        y_label.next_to(axes.y_axis.get_top(), LEFT)
        y_label.shift_onto_screen()
        
        axes.add(x_label, y_label)

        v_lines = VGroup(*[
            DashedLine(
                axes.c2p(x, 0),
                axes.c2p(x, 9),
                color=YELLOW,
                stroke_width=1
            )
            for x in [0.5, 5]
        ])
        
        inertial_subrange = Text("``Inertial subrange''")
        inertial_subrange.scale(0.7)
        inertial_subrange.next_to(v_lines.get_bottom(), UP)

        def func(x):
            if 0.5 < x < 5:
                return (5 / 3) * x
            elif x < 0.5:
                return 5 * (x - 0.5) + 0.5 * (5 / 3)
            elif x > 5:
                return np.log(x) + (5 / 3) * 5 - np.log(5)

        graph = axes.plot(func, x_range=[0.3, 7], color=WHITE)

        prop_label = MathTex("\\text{K.E.} \\propto D^{5/3}")
        prop_label.next_to(
            graph.point_from_proportion(0.5), UL,
            buff=0
        )

        self.add(axes)
        self.play(Create(graph))
        self.play(FadeIn(prop_label, shift=DOWN))
        self.wait()
        self.add(v_lines)
        self.play(Write(inertial_subrange))
        self.wait()
