# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示彗星在橢圓軌道上運行時的速度向量如何隨時間變化，並將所有速度向量收集到一個圓形區域中，形成速度空間的視覺化。


from manim import *
import numpy as np

class IntroduceShapeOfVelocities(Scene, MovingCameraScene):
    def __init__(
        self,
        animate_sun=True,
        sun_center=2 * RIGHT,
        a=4.0,
        b=3.5,
        num_vectors=25,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.animate_sun = animate_sun
        self.sun_center = sun_center
        self.a = a
        self.b = b
        self.num_vectors = num_vectors

    def construct(self):
        self.setup_orbit()
        self.warp_orbit()
        self.reference_inverse_square_law()
        self.show_velocity_vectors()
        self.collect_velocity_vectors()

    def setup_orbit(self):
        self.add_sun()
        self.add_orbit()
        self.add_foreground_mobjects(self.comet)

    def warp_orbit(self):
        def func(z, c=3.5):
            return 1 * (np.exp((1.0 / c) * (z) + 1) - np.exp(1))

        ellipse = self.ellipse
        ellipse.save_state()
        ellipse.generate_target()
        ellipse.target.stretch(0.7, 1)
        ellipse.target.apply_complex_function(func)
        ellipse.target.replace(ellipse, dim_to_match=1)

        self.wait(5)
        self.play(MoveToTarget(ellipse, run_time=2))
        self.wait(5)

    def reference_inverse_square_law(self):
        ellipse = self.ellipse
        force_equation = MathTex(
            "F", "=", "{G", "M", "m", "\\over", "R^2}"
        )
        force_equation.move_to(ellipse)
        force_equation.set_color_by_tex("F", YELLOW)

        force_arrow, force_arrow_update = self.get_force_arrow_and_update(
            self.comet, scale_factor=3,
        )
        radial_line, radial_line_update = self.get_radial_line_and_update(
            self.comet
        )

        self.add(radial_line_update)
        self.add(force_arrow_update)
        self.play(
            Restore(ellipse),
            Write(force_equation),
            UpdateFromAlphaFunc(
                force_arrow,
                lambda m, a: m.set_fill(opacity=a)
            ),
            UpdateFromAlphaFunc(
                radial_line,
                lambda m, a: m.set_stroke(width=a)
            ),
        )
        self.wait(10)

    def show_velocity_vectors(self):
        alphas = np.linspace(0, 1, self.num_vectors, endpoint=False)
        vectors = VGroup(*[
            self.get_velocity_vector(alpha)
            for alpha in alphas
        ])

        moving_vector, moving_vector_animation = self.get_velocity_vector_and_update()

        self.play(LaggedStartMap(
            Create, vectors,
            lag_ratio=0.2,
            run_time=3,
        ))
        self.wait(5)

        self.add(moving_vector_animation)
        self.play(
            FadeOut(vectors),
            VFadeIn(moving_vector)
        )
        self.wait(10)
        vectors.set_fill(opacity=0.5)
        self.play(
            LaggedStartMap(Create, vectors),
            Animation(moving_vector)
        )
        self.wait(5)

        self.velocity_vectors = vectors
        self.moving_vector = moving_vector

    def collect_velocity_vectors(self):
        vectors = self.velocity_vectors.copy()
        frame = self.camera.frame
        ellipse = self.ellipse

        frame_shift = 2.5 * LEFT
        root_point = ellipse.get_left() + 3 * LEFT + 1 * UP
        vector_targets = VGroup()
        for vector in vectors:
            vector.target = Arrow(
                root_point,
                root_point + vector.get_vector(),
                buff=0,
                stroke_width=0.025,
                tip_length=0.2,
                color=vector.get_color(),
            )
            vector.target.add_to_back(
                vector.target.copy().set_stroke(BLACK, 5)
            )
            vector_targets.add(vector.target)

        circle = Circle(color=YELLOW)
        circle.replace(vector_targets)
        circle.scale(1.04)

        velocity_space = TexText("Velocity space")
        velocity_space.next_to(circle, UP)

        rect = SurroundingRectangle(
            VGroup(circle, velocity_space),
            buff=MED_LARGE_BUFF,
            color=WHITE,
        )

        self.play(
            frame.animate.shift(frame_shift).set_run_time(2),
            LaggedStartMap(
                MoveToTarget, vectors,
                run_time=4,
            ),
            FadeIn(velocity_space, shift=DOWN),
            FadeIn(rect, shift=DOWN),
        )
        self.wait(2)
        self.play(
            Create(circle),
            Animation(vectors)
        )
        self.wait(24)

    # Helpers
    def get_velocity_vector(self, alpha, d_alpha=0.01, scalar=3.0):
        norm = np.linalg.norm
        ellipse = self.ellipse
        sun_center = self.sun.get_center()

        min_length = 0.1 * scalar
        max_length = 0.5 * scalar

        p1, p2 = [
            ellipse.point_from_proportion(a)
            for a in (alpha, alpha + d_alpha)
        ]
        vector = Arrow(
            p1, p2, buff=0
        )
        radius_vector = p1 - sun_center
        curr_v_perp = norm(np.cross(
            vector.get_vector(),
            radius_vector / norm(radius_vector)
        ))
        vector.scale(
            scalar / (norm(curr_v_perp) * norm(radius_vector)),
            about_point=vector.get_start()
        )
        vector.set_color(
            interpolate_color(
                BLUE, RED, inverse_interpolate(
                    min_length, max_length,
                    vector.get_length()
                )
            )
        )
        vector.add_to_back(
            vector.copy().set_stroke(BLACK, 5)
        )
        return vector

    def get_velocity_vector_and_update(self):
        moving_vector = self.get_velocity_vector(0)

        def update_moving_vector(vector):
            new_vector = self.get_velocity_vector(
                self.orbit.proportion,
            )
            Transform(vector, new_vector).update(1)

        moving_vector_animation = moving_vector.add_updater(update_moving_vector)
        return moving_vector, moving_vector_animation

    # 以下方法需要從父類別 AskAboutEllipses 繼承或自行實現
    def add_sun(self):
        # 需要實現太陽的添加
        pass

    def add_orbit(self):
        # 需要實現軌道的添加
        pass

    def get_force_arrow_and_update(self, comet, scale_factor):
        # 需要實現力箭頭的獲取和更新
        pass

    def get_radial_line_and_update(self, comet):
        # 需要實現徑向線的獲取和更新
        pass
