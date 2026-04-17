# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示三個不同質量的球體在三維空間中受萬有引力作用下的運動軌跡。


from manim import *
import numpy as np
from functools import reduce
import operator as op

class ThreeBodiesInSpace(ThreeDScene):
    def __init__(
        self,
        masses=[1, 6, 3],
        colors=[RED_E, GREEN_E, BLUE_E],
        G=0.5,
        play_time=60,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.masses = masses
        self.colors = colors
        self.G = G
        self.play_time = play_time

    def construct(self):
        self.add_axes()
        self.add_bodies()
        self.add_trajectories()
        self.let_play()

    def add_axes(self):
        axes = self.axes = ThreeDAxes()
        axes.set_stroke(width=0.5)
        self.add(axes)

        # Orient
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-110 * DEGREES,
        )
        self.begin_ambient_camera_rotation(rate=0.1)

    def add_bodies(self):
        masses = self.masses
        colors = self.colors

        bodies = self.bodies = VGroup()
        velocity_vectors = VGroup()

        centers = self.get_initial_positions()

        for mass, color, center in zip(masses, colors, centers):
            body = Sphere(
                checkerboard_colors=[color, color],
                color=color,
                stroke_width=0.1,
            )
            body.set_opacity(0.75)
            body.mass = mass
            body.radius = 0.08 * np.sqrt(mass)
            body.set_width(2 * body.radius)

            body.point = center
            body.move_to(center)

            body.velocity = self.get_initial_velocity(
                center, centers, mass
            )

            vect = self.get_velocity_vector_mob(body)

            bodies.add(body)
            velocity_vectors.add(vect)

        total_mass = np.sum([body.mass for body in bodies])
        center_of_mass = reduce(op.add, [
            body.mass * body.get_center() / total_mass
            for body in bodies
        ])
        average_momentum = reduce(op.add, [
            body.mass * body.velocity / total_mass
            for body in bodies
        ])
        for body in bodies:
            body.shift(-center_of_mass)
            body.velocity -= average_momentum

    def get_initial_positions(self):
        return [
            np.dot(
                4 * (np.random.random(3) - 0.5),
                [RIGHT, UP, OUT]
            )
            for x in range(len(self.masses))
        ]

    def get_initial_velocity(self, center, centers, mass):
        to_others = [
            center - center2
            for center2 in centers
        ]
        # Filter out zero vectors
        non_zero_diffs = list(filter(
            lambda diff: np.linalg.norm(diff) > 0,
            to_others
        ))
        if len(non_zero_diffs) >= 2:
            velocity = 0.2 * mass * normalize(np.cross(*non_zero_diffs[:2]))
        else:
            velocity = np.zeros(3)
        return velocity

    def add_trajectories(self):
        def update_trajectory(traj):
            new_point = traj.body.point
            if np.linalg.norm(new_point - traj.get_points()[-1]) > 0.01:
                traj.add_smooth_curve_to(new_point)

        for body in self.bodies:
            traj = VMobject()
            traj.body = body
            traj.start_new_path(body.point)
            traj.set_stroke(body.color, 1, opacity=0.75)
            traj.add_updater(update_trajectory)
            self.add(traj, body)

    def let_play(self):
        bodies = self.bodies
        bodies.add_updater(self.update_bodies)
        # Break it up to see partial files as
        # it's rendered
        self.add(bodies)
        for x in range(int(self.play_time)):
            self.wait()

    def get_velocity_vector_mob(self, body):
        def draw_vector():
            center = body.get_center()
            vect = Arrow(
                center,
                center + body.velocity,
                buff=0,
                color=RED,
            )
            vect.set_shade_in_3d(True)
            return vect
        return always_redraw(draw_vector)

    def update_bodies(self, bodies, dt):
        G = self.G

        num_mid_steps = 1000
        for x in range(num_mid_steps):
            for body in bodies:
                acceleration = np.zeros(3)
                for body2 in bodies:
                    if body2 is body:
                        continue
                    diff = body2.point - body.point
                    m2 = body2.mass
                    R = np.linalg.norm(diff)
                    acceleration += G * m2 * diff / (R**3)
                body.point += body.velocity * dt / num_mid_steps
                body.velocity += acceleration * dt / num_mid_steps
        for body in bodies:
            body.move_to(body.point)
        return bodies
