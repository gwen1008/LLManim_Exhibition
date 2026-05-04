# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示傅立葉分析機器的三個視圖：時間軸上的波形、複數平面上的極化軌跡，以及頻率軸上的傅立葉變換圖形。


from manim import *
import numpy as np

class FourierMachineScene(Scene):
    def __init__(
        self,
        time_axes_config={
            "x_range": [0, 4.4],
            "x_length": 3 * 4.4,  # unit_size * x_max
            "y_range": [0, 2],
            "y_length": 0.8 * 2,  # unit_size * y_max
            "axis_config": {
                "include_numbers": True,
                "numbers_to_include": [1, 2, 3],
            },
        },
        time_label_t=3.4,
        circle_plane_config={
            "x_range": [-2.1, 2.1],
            "y_range": [-2.1, 2.1],
            "x_length": 2.1 * 2,
            "y_length": 2.1 * 2,
        },
        frequency_axes_config={
            "x_range": [0, 5.0],
            "y_range": [-1.0, 1.0],
            "x_length": 1.4 * 5.0,
            "y_length": 1.8 * 2.0,
            "axis_config": {
                "color": TEAL,
                "include_numbers": True,
                "numbers_to_include": list(range(1, 6)),
            },
        },
        frequency_axes_box_color=TEAL_E,
        text_scale_val=0.75,
        default_graph_config={
            "color": YELLOW,
        },
        equilibrium_height=1,
        default_y_vector_animation_config={
            "run_time": 5,
            "rate_func": linear,
            "remover": True,
        },
        default_time_sweep_config={
            "rate_func": linear,
            "run_time": 5,
        },
        default_num_v_lines_indicating_periods=20,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.time_axes_config = time_axes_config
        self.time_label_t = time_label_t
        self.circle_plane_config = circle_plane_config
        self.frequency_axes_config = frequency_axes_config
        self.frequency_axes_box_color = frequency_axes_box_color
        self.text_scale_val = text_scale_val
        self.default_graph_config = default_graph_config
        self.equilibrium_height = equilibrium_height
        self.default_y_vector_animation_config = default_y_vector_animation_config
        self.default_time_sweep_config = default_time_sweep_config
        self.default_num_v_lines_indicating_periods = default_num_v_lines_indicating_periods

    def get_time_axes(self):
        time_axes = Axes(**self.time_axes_config)
        time_label = Text("Time")
        intensity_label = Text("Intensity")
        labels = VGroup(time_label, intensity_label)
        for label in labels:
            label.scale(self.text_scale_val)
        time_label.next_to(
            time_axes.c2p(self.time_label_t, 0),
            DOWN
        )
        intensity_label.next_to(time_axes.y_axis.get_top(), RIGHT)
        time_axes.labels = labels
        time_axes.add(labels)
        time_axes.to_corner(UP+LEFT)
        self.time_axes = time_axes
        return time_axes

    def get_circle_plane(self):
        circle_plane = NumberPlane(**self.circle_plane_config)
        circle_plane.to_corner(DOWN+LEFT)
        circle = DashedLine(ORIGIN, TAU*UP).apply_complex_function(np.exp)
        circle.scale(circle_plane.x_length / (2 * 2.1))  # 調整縮放
        circle.move_to(circle_plane.c2p(0, 0))
        circle_plane.circle = circle
        circle_plane.add(circle)
        circle_plane.set_opacity(0.5)
        self.circle_plane = circle_plane
        return circle_plane

    def get_frequency_axes(self):
        frequency_axes = Axes(**self.frequency_axes_config)
        box = SurroundingRectangle(
            frequency_axes,
            buff=MED_SMALL_BUFF,
            color=self.frequency_axes_box_color,
        )
        frequency_axes.box = box
        frequency_axes.add(box)
        frequency_axes.to_corner(DOWN+RIGHT, buff=MED_SMALL_BUFF)

        frequency_label = Text("Frequency")
        frequency_label.scale(self.text_scale_val)
        frequency_label.next_to(
            frequency_axes.x_axis.get_right(), DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=RIGHT,
        )
        frequency_axes.label = frequency_label
        frequency_axes.add(frequency_label)

        self.frequency_axes = frequency_axes
        return frequency_axes

    def get_time_graph(self, func, **kwargs):
        if not hasattr(self, "time_axes"):
            self.get_time_axes()
        config = dict(self.default_graph_config)
        config.update(kwargs)
        graph = self.time_axes.plot(func, **config)
        return graph

    def get_cosine_wave(self, freq=1, shift_val=1, scale_val=0.9):
        return self.get_time_graph(
            lambda t: shift_val + scale_val*np.cos(TAU*freq*t)
        )

    def get_fourier_transform_graph(self, time_graph, **kwargs):
        if not hasattr(self, "frequency_axes"):
            self.get_frequency_axes()
        func = time_graph.underlying_function
        t_axis = self.time_axes.x_axis
        t_min = t_axis.p2n(time_graph.get_points()[0])
        t_max = t_axis.p2n(time_graph.get_points()[-1])
        f_max = self.frequency_axes.x_range[1]
        # 簡化：直接繪製函數圖形
        return self.frequency_axes.plot(
            lambda f: np.cos(2*np.pi*f*t_max) - np.cos(2*np.pi*f*t_min),  # 佔位函數
            color=YELLOW,
            **kwargs
        )

    def get_polarized_mobject(self, mobject, freq=1.0):
        if not hasattr(self, "circle_plane"):
            self.get_circle_plane()
        polarized_mobject = mobject.copy()
        polarized_mobject.apply_function(lambda p: self.polarize_point(p, freq))
        mobject.polarized_mobject = polarized_mobject
        polarized_mobject.frequency = freq
        return polarized_mobject

    def polarize_point(self, point, freq=1.0):
        t, y = self.time_axes.p2c(point)
        z = y*np.exp(complex(0, -2*np.pi*freq*t))
        return self.circle_plane.c2p(z.real, z.imag)

    def get_polarized_animation(self, mobject, freq=1.0):
        p_mob = self.get_polarized_mobject(mobject, freq=freq)
        def update_p_mob(p_mob):
            Transform(
                p_mob,
                self.get_polarized_mobject(mobject, freq=freq)
            ).update(1)
            mobject.polarized_mobject = p_mob
            return p_mob
        return UpdateFromFunc(p_mob, update_p_mob)

    def animate_frequency_change(self, mobjects, new_freq, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 3.0)
        added_anims = kwargs.get("added_anims", [])
        self.play(*[
            self.get_frequency_change_animation(mob, new_freq, **kwargs)
            for mob in mobjects
        ] + added_anims)

    def get_frequency_change_animation(self, mobject, new_freq, **kwargs):
        if not hasattr(mobject, "polarized_mobject"):
            mobject.polarized_mobject = self.get_polarized_mobject(mobject)
        start_freq = mobject.polarized_mobject.frequency
        def update(pm, alpha):
            freq = interpolate(start_freq, new_freq, alpha)
            new_pm = self.get_polarized_mobject(mobject, freq)
            Transform(pm, new_pm).update(1)
            mobject.polarized_mobject = pm
            mobject.polarized_mobject.frequency = freq
            return pm
        return UpdateFromAlphaFunc(mobject.polarized_mobject, update, **kwargs)

    def get_time_graph_y_vector_animation(self, graph, **kwargs):
        config = dict(self.default_y_vector_animation_config)
        config.update(kwargs)
        vector = Vector(UP, color=WHITE)
        graph_copy = graph.copy()
        x_axis = self.time_axes.x_axis
        x_min = x_axis.p2n(graph.get_points()[0])
        x_max = x_axis.p2n(graph.get_points()[-1])
        def update_vector(vector, alpha):
            x = interpolate(x_min, x_max, alpha)
            vector.put_start_and_end_on(
                self.time_axes.c2p(x, 0),
                self.time_axes.input_to_graph_point(x, graph_copy)
            )
            return vector
        return UpdateFromAlphaFunc(vector, update_vector, **config)

    def get_polarized_vector_animation(self, polarized_graph, **kwargs):
        config = dict(self.default_y_vector_animation_config)
        config.update(kwargs)
        vector = Vector(RIGHT, color=WHITE)
        origin = self.circle_plane.c2p(0, 0)
        graph_copy = polarized_graph.copy()
        def update_vector(vector, alpha):
            point = center_of_mass([
                graph_copy.point_from_proportion(alpha+d)
                for d in np.linspace(-0.001, 0.001, 5)
            ])
            vector.put_start_and_end_on(origin, point)
            return vector
        return UpdateFromAlphaFunc(vector, update_vector, **config)

    def get_vector_animations(self, graph, draw_polarized_graph=True, **kwargs):
        config = dict(self.default_y_vector_animation_config)
        config.update(kwargs)
        anims = [
            self.get_time_graph_y_vector_animation(graph, **config),
            self.get_polarized_vector_animation(graph.polarized_mobject, **config),
        ]
        if draw_polarized_graph:
            new_config = dict(config)
            new_config["remover"] = False
            anims.append(Create(graph.polarized_mobject, **new_config))
        return anims

    def animate_time_sweep(self, freq, n_repeats=1, t_max=None, **kwargs):
        added_anims = kwargs.pop("added_anims", [])
        config = dict(self.default_time_sweep_config)
        config.update(kwargs)
        time_axes = self.time_axes
        ctp = time_axes.c2p
        t_max = t_max or time_axes.x_range[1]
        v_line = DashedLine(
            ctp(0, 0), ctp(0, time_axes.y_range[1]),
            stroke_width=6,
        )
        v_line.set_color(RED)

        for x in range(n_repeats):
            v_line.move_to(ctp(0, 0), DOWN)
            self.play(
                v_line.animate.move_to(ctp(t_max, 0), DOWN),
                self.get_polarized_animation(v_line, freq=freq),
                *added_anims,
                **config
            )
            self.remove(v_line.polarized_mobject)
        self.play(FadeOut(VGroup(v_line, v_line.polarized_mobject)))

    def get_v_lines_indicating_periods(self, freq, n_lines=None):
        if n_lines is None:
            n_lines = self.default_num_v_lines_indicating_periods
        period = np.divide(1., max(freq, 0.01))
        v_lines = VGroup(*[
            DashedLine(ORIGIN, 1.5*UP).move_to(
                self.time_axes.c2p(n*period, 0),
                DOWN
            )
            for n in range(1, n_lines + 1)
        ])
        v_lines.set_color(GREY_B)
        return v_lines

    def get_period_v_lines_update_anim(self):
        def update_v_lines(v_lines):
            freq = self.graph.polarized_mobject.frequency
            Transform(
                v_lines,
                self.get_v_lines_indicating_periods(freq)
            ).update(1)
        return UpdateFromFunc(
            self.v_lines_indicating_periods, update_v_lines
        )
