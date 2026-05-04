# Source: 3b1b/_2019/diffyq/part2/staging.py
# Description: [3b1b translated] 展示三維空間中一個曲面上的拉普拉斯算子直觀理解，通過移動點和其對應的曲面上的圓形來觀察曲面的局部變化。



from manim import *
class LaplacianIntuition(ThreeDScene):
    def __init__(
        self,
        three_d_axes_config={
            "x_range": [-5, 5],
            "y_range": [-5, 5],
            "z_range": [-5, 5],
        },
        surface_resolution=32,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.three_d_axes_config = three_d_axes_config
        self.surface_resolution = surface_resolution

    def construct(self):
        axes = ThreeDAxes(**self.three_d_axes_config)
        axes.scale(0.5, about_point=ORIGIN)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        def func(x, y):
            return np.array([
                x, y,
                2.7 + 0.5 * (np.sin(x) + np.cos(y)) -
                0.025 * (x**2 + y**2)
            ])

        surface_config = {
            "u_range": [-5, 5],
            "v_range": [-5, 5],
            "resolution": (self.surface_resolution, self.surface_resolution),
        }
        
        plane = Square(
            side_length=10,
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.1,
        )
        plane.center()
        plane.set_shade_in_3d(True)

        surface = Surface(
            lambda u, v: func(u, v),
            **surface_config
        )
        surface.set_style(
            stroke_color=BLUE,
            stroke_width=0.1,
            fill_color=BLUE,
            fill_opacity=0.25
        )

        self.add(axes, plane, surface)

        point = VectorizedPoint(np.array([2, -2, 0]))
        dot = Dot()
        dot.set_color(GREEN)
        dot.add_updater(lambda d: d.move_to(point.get_location()))
        
        line = always_redraw(lambda: DashedLine(
            point.get_location(),
            func(*point.get_location()[:2]),
        ))

        circle = Circle(radius=0.25)
        circle.set_color(YELLOW)
        circle.insert_n_curves(20)
        circle.add_updater(lambda m: m.move_to(point.get_location()))
        circle.set_shade_in_3d(True)
        
        surface_circle = always_redraw(
            lambda: circle.copy().apply_function(
                lambda p: func(*p[:2])
            ).shift(
                0.02 * IN
            )
        )

        self.play(FadeIn(dot, scale=2))
        self.play(Create(line))
        self.play(TransformFromCopy(dot, circle))
        self.play(
            Transform(
                circle.copy(),
                surface_circle.copy().clear_updaters(),
                remover=True,
            )
        )
        self.add(surface_circle)

        self.wait()
        for vect in [4 * LEFT, DOWN, 4 * RIGHT, UP]:
            self.play(
                point.animate.shift(vect),
                run_time=3,
            )
        self.wait()
