# Source: 3b1b/_2019/diffyq/part1/phase_space.py
# Description: [3b1b translated] 展示高角速度下單擺相空間中的向量場、軌跡，以及相機跟隨軌跡移動的動畫。



from manim import *
class ShowHighVelocityCase(ShowPendulumPhaseFlow, MovingCameraScene):
    def __init__(
        self,
        coordinate_plane_config={
            "x_range": [-15, 15, 1],
            "y_range": [-8, 8, 1],
            "x_length": 15,
            "y_length": 8,
        },
        vector_field_config={
            "x_range": [-15, 15, 1],
            "y_range": [-8, 8, 1],
        },
        big_pendulum_config={
            "max_velocity_vector_length_to_length_ratio": 1,
        },
        run_time=25,
        initial_theta=0,
        initial_theta_dot=4,
        frame_shift_vect=TAU * RIGHT,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.coordinate_plane_config = coordinate_plane_config
        self.vector_field_config = vector_field_config
        self.big_pendulum_config = big_pendulum_config
        self.run_time = run_time
        self.initial_theta = initial_theta
        self.initial_theta_dot = initial_theta_dot
        self.frame_shift_vect = frame_shift_vect

    def construct(self):
        self.initialize_plane_and_field()
        self.add_flexible_state()
        self.show_high_vector()
        self.show_trajectory()

    def initialize_plane_and_field(self):
        self.initialize_plane()
        self.add(self.plane)
        self.initialize_vector_field()
        self.add(self.vector_field)

    def add_flexible_state(self):
        super().add_flexible_state()
        state = self.state
        plane = self.plane

        state.to_edge(DOWN, buff=SMALL_BUFF)
        start_point = plane.c2p(
            self.initial_theta,
            self.initial_theta_dot,
        )
        dot = self.get_state_controlling_dot(state)
        dot.move_to(start_point)
        state.update()

        self.dot = dot
        self.start_point = start_point

    def show_high_vector(self):
        field = self.vector_field
        top_vectors = VGroup(*filter(
            lambda a: np.all(a.get_center() > [-10, 1.5, -10]),
            field
        )).copy()
        top_vectors.set_stroke(PINK, 3)
        top_vectors.sort(lambda p: p[0])

        self.play(
            Create(top_vectors, run_time=2, lag_ratio=0.01),
            FadeOut(top_vectors, run_time=0.1),
        )

    def show_trajectory(self):
        state = self.state
        frame = self.camera.frame
        dot = self.dot
        start_point = self.start_point

        traj = self.get_trajectory(start_point, self.run_time)

        self.add(traj, dot)
        anims = [
            Create(
                traj,
                rate_func=linear,
            ),
            UpdateFromFunc(
                dot, lambda d: d.move_to(traj.get_points()[-1])
            ),
        ]
        if np.linalg.norm(self.frame_shift_vect) > 0:
            anims += [
                frame.animate.shift(self.frame_shift_vect).set_rate_func(
                    lambda t: smooth(min(t / 0.3, 1))
                ),
                MaintainPositionRelativeTo(state.rect, frame),
            ]
        self.play(*anims, run_time=self.run_time)

    def get_trajectory(self, start_point, time, dt=0.1, added_steps=100):
        field = self.vector_field
        traj = VMobject()
        traj.start_new_path(start_point)
        for x in range(int(time / dt)):
            last_point = traj.get_points()[-1]
            for y in range(added_steps):
                dp_dt = field.func(last_point)
                last_point += dp_dt * dt / added_steps
            traj.add_smooth_curve_to(last_point)
        traj.make_smooth()
        traj.set_stroke(WHITE, 2)
        return traj
