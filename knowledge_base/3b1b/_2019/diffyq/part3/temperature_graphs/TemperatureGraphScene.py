# Source: 3b1b/_2019/diffyq/part3/temperature_graphs.py
# Description: [3b1b translated] 展示三維溫度場的坐標系統，包含坐標軸、標籤、時間切片平面和參數化曲面。



from manim import *
class TemperatureGraphScene(ThreeDScene):
    def __init__(
        self,
        axes_config=None,
        default_graph_style=None,
        default_surface_config=None,
        temp_text="Temperature",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # 設定預設值
        if axes_config is None:
            axes_config = {
                "x_range": [0, TAU, TAU/8],
                "y_range": [0, 10, 1],
                "z_range": [-3, 3, 1],
                "x_length": 7,
                "y_length": 7,
                "z_length": 5,
            }
        if default_graph_style is None:
            default_graph_style = {
                "stroke_width": 2,
                "stroke_color": WHITE,
            }
        if default_surface_config is None:
            default_surface_config = {
                "fill_opacity": 0.1,
                "checkerboard_colors": [GREY_B],
                "stroke_width": 0.5,
                "stroke_color": WHITE,
                "stroke_opacity": 0.5,
            }
        
        self.axes_config = axes_config
        self.default_graph_style = default_graph_style
        self.default_surface_config = default_surface_config
        self.temp_text = temp_text

    def get_three_d_axes(self, include_labels=True, include_numbers=False, **kwargs):
        config = dict(self.axes_config)
        config.update(kwargs)
        axes = ThreeDAxes(**config)
        axes.set_stroke(width=2)

        if include_numbers:
            self.add_axes_numbers(axes)

        if include_labels:
            self.add_axes_labels(axes)

        # 調整坐標軸方向
        axes.x_axis.rotate(
            90 * DEGREES, RIGHT,
            about_point=axes.c2p(0, 0, 0),
        )
        axes.y_axis.rotate(
            90 * DEGREES, UP,
            about_point=axes.c2p(0, 0, 0),
        )

        # 添加 xy 平面
        input_plane = self.get_surface(
            axes, lambda x, t: 0
        )
        input_plane.set_style(
            fill_opacity=0.5,
            fill_color=BLUE_B,
            stroke_width=0.5,
            stroke_color=WHITE,
        )

        axes.input_plane = input_plane

        return axes

    def add_axes_numbers(self, axes):
        x_axis = axes.x_axis
        y_axis = axes.y_axis
        
        tex_vals = [
            (r"\frac{\pi}{2}", TAU / 4),
            (r"\pi", TAU / 2),
            (r"\frac{3\pi}{2}", 3 * TAU / 4),
            (r"2\pi", TAU)
        ]
        x_labels = VGroup()
        for tex, val in tex_vals:
            label = MathTex(tex)
            label.scale(0.5)
            label.next_to(x_axis.n2p(val), DOWN)
            x_labels.add(label)
        axes.add(x_labels)
        axes.x_labels = x_labels

        # y 軸數字
        y_labels = VGroup()
        for val in np.arange(axes.y_range[0], axes.y_range[1] + axes.y_range[2], axes.y_range[2]):
            if val != 0:
                label = MathTex(str(int(val)))
                label.scale(0.5)
                label.next_to(y_axis.n2p(val), LEFT)
                label.rotate(90 * DEGREES)
                y_labels.add(label)
        axes.add(y_labels)
        axes.y_labels = y_labels
        
        return axes

    def add_axes_labels(self, axes):
        x_label = MathTex("x")
        x_label.next_to(axes.x_axis.get_end(), RIGHT)
        axes.x_axis_label = x_label
        axes.add(x_label)

        t_label = Text("Time")
        t_label.rotate(90 * DEGREES, OUT)
        t_label.next_to(axes.y_axis.get_end(), UP)
        axes.y_axis_label = t_label
        axes.add(t_label)

        temp_label = Text(self.temp_text)
        temp_label.rotate(90 * DEGREES, RIGHT)
        temp_label.next_to(axes.z_axis.get_zenith(), RIGHT)
        axes.z_axis_label = temp_label
        axes.add(temp_label)
        
        return axes

    def get_time_slice_graph(self, axes, func, t, **kwargs):
        config = dict()
        config.update(self.default_graph_style)
        config.update({
            "t_range": [axes.x_range[0], axes.x_range[1]],
        })
        config.update(kwargs)
        
        return ParametricFunction(
            lambda x: axes.c2p(
                x, t, func(x, t)
            ),
            **config
        )

    def get_initial_state_graph(self, axes, func, **kwargs):
        return self.get_time_slice_graph(
            axes,
            lambda x, t: func(x),
            t=0,
            **kwargs
        )

    def get_surface(self, axes, func, **kwargs):
        config = {
            "u_range": [axes.y_range[0], axes.y_range[1]],
            "v_range": [axes.x_range[0], axes.x_range[1]],
            "resolution": (24, 24),  # 簡化解析度設定
        }
        config.update(self.default_surface_config)
        config.update(kwargs)
        
        return Surface(
            lambda u, v: axes.c2p(
                v, u, func(v, u)
            ),
            **config
        )

    def orient_three_d_mobject(self, mobject,
                               phi=85 * DEGREES,
                               theta=-80 * DEGREES):
        mobject.rotate(-90 * DEGREES - theta, OUT)
        mobject.rotate(phi, LEFT)
        return mobject

    def get_rod_length(self):
        return self.axes_config.get("x_range", [0, TAU])[1]

    def get_const_time_plane(self, axes):
        t_tracker = ValueTracker(0)
        
        # 創建時間平面
        plane = Polygon(
            *[
                axes.c2p(x, 0, z)
                for x, z in [
                    (axes.x_range[0], axes.z_range[0]),
                    (axes.x_range[1], axes.z_range[0]),
                    (axes.x_range[1], axes.z_range[1]),
                    (axes.x_range[0], axes.z_range[1]),
                ]
            ],
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.2
        )
        
        # 更新平面位置
        def update_plane(m):
            m.move_to(axes.c2p(
                axes.x_range[0],
                t_tracker.get_value(),
                axes.z_range[0],
            ))
        
        plane.add_updater(update_plane)
        plane.t_tracker = t_tracker
        
        return plane
