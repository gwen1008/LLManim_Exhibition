# Source: 3b1b/_2018/eop/chapter1/area_model_erf.py
# Description: [3b1b translated] 展示高斯分佈的機率密度函數圖形，並動態計算從 -a 到 a 的積分面積，對應誤差函數的視覺化。


from manim import *
import numpy as np
import scipy.special

class IllustrateAreaModelErf(Scene):
    def __init__(
        self,
        x_min=-3.0,
        x_max=3.0,
        y_min=0,
        y_max=1.0,
        num_rects=400,
        y_axis_label="",
        x_axis_label="",
        variable_point_label="a",
        graph_origin=2.5 * DOWN + 4 * RIGHT,
        x_axis_width=5,
        y_axis_height=5,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.num_rects = num_rects
        self.y_axis_label = y_axis_label
        self.x_axis_label = x_axis_label
        self.variable_point_label = variable_point_label
        self.graph_origin = graph_origin
        self.x_axis_width = x_axis_width
        self.y_axis_height = y_axis_height

    def construct(self):
        # integral bounds
        x_min_1 = -0.0001
        x_max_1 = 0.0001

        x_min_2 = self.x_min
        x_max_2 = self.x_max

        # Create axes
        ax = Axes(
            x_range=[self.x_min, self.x_max, 1],
            y_range=[self.y_min, self.y_max, 0.2],
            axis_config={"include_numbers": False},
            x_length=self.x_axis_width,
            y_length=self.y_axis_height,
        ).shift(self.graph_origin)
        
        # Remove axes initially (will be added later)
        self.remove(ax)
        
        # Create graph
        graph = ax.plot(
            lambda x: np.exp(-x**2) * 2.0 / np.sqrt(2 * np.pi),
            color=BLUE
        )
        
        # Create area under curve
        area = ax.get_area(
            graph,
            x_range=(x_min_1, x_max_1),
            color=BLUE_E,
            opacity=0.5
        )
        self.area = area

        # Create formulas
        pdf_formula = MathTex(r"p(x) = {1\over \sigma\sqrt{2\pi}}e^{-{1\over 2}({x\over\sigma})^2}")
        pdf_formula.set_color(graph.get_color())

        cdf_formula = MathTex(r"P(|X| < ", "a", r") = \int", "_{-a}", "^a", "p(x) dx")
        cdf_formula.set_color_by_tex("a", YELLOW)
        cdf_formula.next_to(graph, LEFT, buff=2)
        pdf_formula.next_to(cdf_formula, UP)

        formulas = VGroup(pdf_formula, cdf_formula)
        self.play(Write(pdf_formula))
        self.play(Write(cdf_formula))
        
        self.wait()

        # Add axes and graph
        self.play(Create(ax.x_axis))
        self.play(Create(graph))
        self.play(FadeIn(area))

        self.v_graph = graph
        
        # Create vertical lines at bounds
        left_v_line = ax.get_vertical_line(
            ax.c2p(x_min_1, 0),
            line_config={"color": YELLOW}
        )
        right_v_line = ax.get_vertical_line(
            ax.c2p(x_max_1, 0),
            line_config={"color": YELLOW}
        )
        
        # Create labels for bounds
        left_label = MathTex("-a", color=YELLOW).next_to(
            ax.c2p(x_min_1, 0), DOWN
        )
        right_label = MathTex("a", color=YELLOW).next_to(
            ax.c2p(x_max_1, 0), DOWN
        )
        
        self.left_T_label_group = VGroup(left_v_line, left_label)
        self.right_T_label_group = VGroup(right_v_line, right_label)
        
        # Store right_v_line for later use
        self.right_v_line = right_v_line
        
        # Don't show the labels just yet
        self.remove(left_label, right_label)

        def integral_update_func():
            x_coord = ax.p2c(self.right_v_line.get_center())[0]
            return scipy.special.erf(x_coord)

        def integral_update_func_percent():
            return 100 * integral_update_func()
            
        equals_sign = MathTex("=").next_to(cdf_formula, buff=MED_LARGE_BUFF)

        cdf_value = DecimalNumber(0, color=graph.get_color(), num_decimal_places=3)
        cdf_value.next_to(equals_sign, RIGHT)
        self.play(
            FadeIn(equals_sign),
            FadeIn(cdf_value)
        )

        cdf_percentage = DecimalNumber(0, unit="\\%")
        cdf_percentage.move_to(ax.c2p(0, 0.2))

        # Add updater for cdf_value
        cdf_value.add_updater(
            lambda m: m.set_value(integral_update_func())
        )

        # Animate the area expanding from x_min_2 to x_max_2
        anim_area = ax.animate_area_under_curve(
            graph,
            x_range=(x_min_2, x_max_2),
            color=BLUE_E,
            opacity=0.5
        )
        
        # Animate vertical lines moving
        anim_left_line = left_v_line.animate.move_to(ax.c2p(x_min_2, 0))
        anim_right_line = right_v_line.animate.move_to(ax.c2p(x_max_2, 0))
        
        # Animate labels moving
        anim_left_label = left_label.animate.next_to(ax.c2p(x_min_2, 0), DOWN)
        anim_right_label = right_label.animate.next_to(ax.c2p(x_max_2, 0), DOWN)
        
        # Show labels during animation
        self.add(left_label, right_label)
        
        self.play(
            anim_area,
            anim_left_line,
            anim_right_line,
            anim_left_label,
            anim_right_label,
            run_time=3
        )

        rect = SurroundingRectangle(formulas, buff=0.5 * MED_LARGE_BUFF)
        self.play(Create(rect))
