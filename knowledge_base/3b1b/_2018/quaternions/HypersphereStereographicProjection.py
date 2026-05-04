# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示四元數的立體投影，從四維單位超球面投影到三維空間，並動態顯示不同四元數對應的投影點與球面。


from manim import *
import numpy as np

class HypersphereStereographicProjection(ThreeDScene):
    def __init__(
        self,
        fancy_dot=True,
        initial_quaternion_sample_values=[
            [0, 1, 0, 0],
            [-1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 1, -1, 1],
        ],
        unit_labels_scale_factor=1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.fancy_dot = fancy_dot
        self.initial_quaternion_sample_values = initial_quaternion_sample_values
        self.unit_labels_scale_factor = unit_labels_scale_factor

    def construct(self):
        self.setup_axes()
        self.introduce_quaternion_label()
        self.show_one()
        self.show_unit_sphere()
        self.show_quaternions_with_nonzero_real_part()
        self.emphasize_only_units()
        self.show_reference_spheres()

    def setup_axes(self):
        axes = self.axes = ThreeDAxes()
        axes.set_stroke(width=1)
        self.add(axes)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.01)

    def introduce_quaternion_label(self):
        # 簡化：使用 ValueTracker 追蹤四元數
        q_tracker = ValueTracker(np.array([0, 0, 0, 0], dtype=float))
        coords = [
            DecimalNumber(0, color=color, include_sign=sign)
            for color, sign in zip(
                [YELLOW, GREEN, RED, BLUE],
                [False, True, True, True],
            )
        ]
        for coord in coords:
            coord.fix_in_frame()
        label = VGroup(
            coords[0], VectorizedPoint(),
            coords[1], MathTex("i"),
            coords[2], MathTex("j"),
            coords[3], MathTex("k"),
        )
        label.arrange(RIGHT, buff=SMALL_BUFF)
        label.to_corner(UR)
        label.fix_in_frame()

        def update_label(label):
            quat = q_tracker.get_value()
            for i, coord in enumerate(coords):
                coord.set_value(quat[i])
            return label

        label.add_updater(update_label)
        self.pink_dot_label = label

        def get_pq_point():
            # 簡化投影：直接取後三維作為座標
            quat = q_tracker.get_value()
            point = np.array([quat[1], quat[2], quat[3]])
            norm = np.linalg.norm(point)
            if norm > 100:
                point = point * 100 / norm
            return point

        pq_dot = self.get_dot()
        pq_dot.add_updater(lambda d: d.move_to(get_pq_point()))

        def get_pq_line():
            point = get_pq_point()
            origin = self.axes.c2p(0, 0, 0)
            result = Line(origin, self.axes.c2p(*point))
            result.set_stroke(width=1)
            return result

        pq_line = get_pq_line()
        pq_line.add_updater(lambda cl: cl.become(get_pq_line()))

        self.add(q_tracker, label, pq_line, pq_dot)

        self.q_tracker = q_tracker
        self.q_label = label
        self.pq_line = pq_line
        self.pq_dot = pq_dot

        rect = SurroundingRectangle(label, color=WHITE)
        rect.fix_in_frame()
        self.add(rect)
        self.play(Create(rect))
        self.play(FadeOut(rect))

        for value in self.initial_quaternion_sample_values:
            self.set_quat(value)
            self.wait()

    def show_one(self):
        q_tracker = self.q_tracker

        one_label = MathTex("1")
        one_label.rotate(PI / 2, RIGHT)
        one_label.next_to(ORIGIN, IN + RIGHT, SMALL_BUFF)
        one_label.set_background_stroke(width=0)

        self.play(
            q_tracker.animate.set_value(np.array([1, 0, 0, 0])),
            FadeIn(one_label, shift=DOWN),
            run_time=2
        )
        self.wait(4)

    def show_unit_sphere(self):
        # 簡化：使用 Sphere 物件
        sphere = self.sphere = Sphere(radius=1, resolution=(24, 24))
        sphere.set_color_by_gradient(BLUE, GREEN, PINK)
        sphere.set_opacity(0.3)
        sphere.set_stroke(width=0.5)
        labels = self.get_unit_labels()
        labels.remove(labels[3])

        real_part = self.q_label[0]
        brace = Brace(real_part, DOWN)
        words = Text("Real part zero")
        words.next_to(brace, DOWN, SMALL_BUFF, LEFT)
        brace.fix_in_frame()
        words.fix_in_frame()

        self.play(Create(sphere))
        self.play(LaggedStart(
            *[FadeIn(label, shift=IN) for label in labels]
        ))
        self.add(brace, words)
        self.set_quat(
            [0, 1, 0, 0],
            added_anims=[
                GrowFromCenter(brace),
                Write(words),
            ]
        )
        self.wait()
        self.set_quat([0, 1, -1, 1])
        self.wait(2)
        self.set_quat([0, -1, -1, 1])
        self.wait(2)
        self.set_quat([0, 0, 0, 1])
        self.wait(2)
        self.set_quat([0, 0, -1, 0])
        self.wait(2)
        self.set_quat([0, 1, 0, 0])
        self.wait(2)
        self.play(FadeOut(words))

        self.real_part_brace = brace

    def show_quaternions_with_nonzero_real_part(self):
        # Positive real part
        self.set_quat(
            [1, 1, 2, 0],
            added_anims=[
                self.sphere.copy().animate.scale(0).set_opacity(0)
            ]
        )
        self.wait(2)
        self.set_quat([4, 0, -1, -1])
        self.wait(2)
        # Negative real part
        self.set_quat(
            [-1, 1, 2, 0],
            added_anims=[
                self.sphere.copy().animate.scale(10).set_opacity(0)
            ]
        )
        self.wait(2)
        self.set_quat([-2, 0, -1, 1])
        self.wait(2)
        self.set_quat([-1, 1, 0, 0])
        self.move_camera(theta=-160 * DEGREES, run_time=3)
        self.set_quat([-1, 0.001, 0, 0])
        self.wait(2)

    def emphasize_only_units(self):
        q_label = self.q_label
        brace = self.real_part_brace

        brace.target = Brace(q_label, DOWN, buff=SMALL_BUFF)
        words = MathTex(
            "\\text{Only those where }\\\\",
            "w^2 + x^2 + y^2 + z^2 = 1"
        )
        words.next_to(brace.target, DOWN, SMALL_BUFF)
        brace.target.fix_in_frame()
        words.fix_in_frame()

        self.add(words)
        self.play(
            Transform(brace, brace.target),
            Write(words)
        )
        self.set_quat([1, 1, 1, 1])
        self.wait(2)
        self.set_quat([1, 1, -1, 1])
        self.wait(2)
        self.set_quat([-1, 1, -1, 1])
        self.wait(8)
        self.play(FadeOut(brace), FadeOut(words))

    def show_reference_spheres(self):
        sphere = self.sphere
        self.move_camera(
            phi=60 * DEGREES,
            theta=-150 * DEGREES,
        )
        self.play(
            self.q_tracker.animate.set_value(np.array([1, 0, 0, 0]))
        )
        # 簡化：使用預先定義的球體
        sphere_ijk = Sphere(radius=1, resolution=(24, 24))
        sphere_ijk.set_color_by_gradient(BLUE, GREEN, PINK)
        sphere_ijk.set_opacity(0.3)
        sphere_1ij = Sphere(radius=1, resolution=(24, 24))
        sphere_1ij.set_color(BLUE_E)
        sphere_1ij.set_opacity(0.25)
        circle = Circle(radius=1)
        circle.set_stroke(WHITE, width=2)
        circle.rotate(PI/2, RIGHT)

        circle_words = MathTex(
            "\\text{Circle through}\\\\", "1, i, -1, -i"
        )
        sphere_1ij_words = MathTex(
            "\\text{Sphere through}\\\\", "1, i, j, -1, -i, -j"
        )
        for words in [circle_words, sphere_1ij_words]:
            words.to_corner(UL)
            words.fix_in_frame()

        self.play(
            Create(circle),
            Write(circle_words),
        )
        self.set_quat([0, 1, 0, 0])
        self.set_quat([1, 0, 0, 0])
        self.remove(sphere)
        self.add(sphere_ijk)

        # Show xy plane
        self.play(
            FadeOut(circle_words, shift=DOWN),
            FadeIn(sphere_1ij_words, shift=DOWN),
            FadeOut(circle),
            sphere_ijk.animate.set_stroke(width=0.0)
        )
        self.play(Create(sphere_1ij))
        self.wait(10)

    def get_dot(self):
        if self.fancy_dot:
            sphere = Sphere(radius=0.1, resolution=(12, 12))
            sphere.set_stroke(width=0)
            sphere.set_fill(PINK, opacity=1)
            return sphere
        else:
            return VGroup(
                Dot(color=PINK),
                Dot(color=PINK).rotate(PI / 2, RIGHT),
            )

    def get_unit_labels(self):
        c2p = self.axes.c2p
        tex_coords_vects = [
            ("i", [1, 0, 0], IN + RIGHT),
            ("-i", [-1, 0, 0], IN + LEFT),
            ("j", [0, 1, 0], UP + OUT + RIGHT),
            ("-j", [0, -1, 0], RIGHT + DOWN),
            ("k", [0, 0, 1], OUT + RIGHT),
            ("-k", [0, 0, -1], IN + RIGHT),
        ]
        labels = VGroup()
        for tex, coords, vect in tex_coords_vects:
            label = MathTex(tex)
            label.scale(self.unit_labels_scale_factor)
            label.rotate(90 * DEGREES, RIGHT)
            label.next_to(c2p(*coords), vect, SMALL_BUFF)
            labels.add(label)
        labels.set_background_stroke(width=0)
        return labels

    def set_quat(self, value, run_time=3, added_anims=None):
        if added_anims is None:
            added_anims = []
        self.play(
            self.q_tracker.animate.set_value(np.array(value, dtype=float)),
            *added_anims,
            run_time=run_time
        )
