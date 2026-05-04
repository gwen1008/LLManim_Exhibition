# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 展示一個圓周上等距排列的燈塔，從觀察者點到各燈塔的距離計算與乘積結果的視覺化過程。


from manim import *
import numpy as np
import operator as op
from functools import reduce

class DistanceProductScene(MovingCameraScene):
    def __init__(
        self,
        ambient_light_config=None,
        circle_color=BLUE,
        circle_radius=3,
        num_lighthouses=6,
        lighthouse_height=0.5,
        ignored_lighthouse_indices=[],
        observer_config=None,
        observer_fraction=1.0 / 3,
        d_label_height=0.35,
        numeric_distance_label_height=0.25,
        default_product_column_top=FRAME_WIDTH * RIGHT / 4 + 1.5 * UP,
        include_lighthouses=True,
        include_distance_labels_background_rectangle=True,
        **kwargs
    ):
        super().__init__(**kwargs)
        if ambient_light_config is None:
            ambient_light_config = {}
        if observer_config is None:
            observer_config = {
                "color": MAROON_B,
                "mode": "pondering",
                "height": 0.25,
                "flip_at_start": True,
            }
        self.ambient_light_config = ambient_light_config
        self.circle_color = circle_color
        self.circle_radius = circle_radius
        self.num_lighthouses = num_lighthouses
        self.lighthouse_height = lighthouse_height
        self.ignored_lighthouse_indices = ignored_lighthouse_indices
        self.observer_config = observer_config
        self.observer_fraction = observer_fraction
        self.d_label_height = d_label_height
        self.numeric_distance_label_height = numeric_distance_label_height
        self.default_product_column_top = default_product_column_top
        self.include_lighthouses = include_lighthouses
        self.include_distance_labels_background_rectangle = include_distance_labels_background_rectangle

    def setup(self):
        super().setup()
        self.circle = Circle(
            color=self.circle_color,
            radius=self.circle_radius,
        )

    def get_circle_point_at_proportion(self, alpha):
        radius = self.get_radius()
        center = self.circle.get_center()
        angle = alpha * TAU
        unit_circle_point = np.cos(angle) * RIGHT + np.sin(angle) * UP
        return radius * unit_circle_point + center

    def get_lh_points(self):
        return np.array([
            self.get_circle_point_at_proportion(i / self.num_lighthouses)
            for i in range(self.num_lighthouses)
            if i not in self.ignored_lighthouse_indices
        ])

    def get_observer_point(self, fraction=None):
        if fraction is None:
            fraction = self.observer_fraction
        return self.get_circle_point_at_proportion(fraction / self.num_lighthouses)

    def get_observer(self):
        # Note: PiCreature is not available in ManimCE by default
        # Using a simple Dot as placeholder
        observer = self.observer = Dot(
            color=self.observer_config["color"],
            radius=self.observer_config.get("height", 0.25) / 2
        )
        observer.next_to(self.get_observer_point(), RIGHT, buff=SMALL_BUFF)
        return observer

    def get_observer_dot(self):
        self.observer_dot = Dot(
            self.get_observer_point(),
            color=self.observer_config["color"]
        )
        return self.observer_dot

    def get_lighthouses(self):
        self.lighthouses = VGroup()
        for point in self.get_lh_points():
            # Lighthouse class not available in ManimCE, using Triangle as placeholder
            lighthouse = Triangle(color=YELLOW, fill_opacity=1)
            lighthouse.set_height(self.lighthouse_height)
            lighthouse.move_to(point)
            self.lighthouses.add(lighthouse)
        return self.lighthouses

    def get_lights(self):
        self.lights = VGroup()
        for point in self.get_lh_points():
            # AmbientLight not available in ManimCE, using Dot as placeholder
            light = Dot(point, color=YELLOW, radius=0.1, fill_opacity=0.5)
            self.lights.add(light)
        return self.lights

    def get_distance_lines(self, start_point=None, line_class=Line):
        if start_point is None:
            start_point = self.get_observer_point()
        lines = VGroup(*[
            line_class(start_point, point)
            for point in self.get_lh_points()
        ])
        lines.set_stroke(width=2)
        self.distance_lines = lines
        return self.distance_lines

    def get_symbolic_distance_labels(self):
        if not hasattr(self, "distance_lines"):
            self.get_distance_lines()
        self.d_labels = VGroup()
        for i, line in enumerate(self.distance_lines):
            d_label = MathTex(f"d_{{{i}}}")
            d_label.set_height(self.d_label_height)
            vect = rotate_vector(line.get_vector(), 90 * DEGREES)
            vect *= 2.5 * SMALL_BUFF / np.linalg.norm(vect)
            d_label.move_to(line.get_center() + vect)
            self.d_labels.add(d_label)
        return self.d_labels

    def get_numeric_distance_labels(self, lines=None, num_decimal_places=3, show_ellipsis=True):
        radius = self.circle.get_width() / 2
        if lines is None:
            if not hasattr(self, "distance_lines"):
                self.get_distance_lines()
            lines = self.distance_lines
        labels = self.numeric_distance_labels = VGroup()
        for line in lines:
            label = DecimalNumber(
                line.get_length() / radius,
                num_decimal_places=num_decimal_places,
            )
            label.set_height(self.numeric_distance_label_height)
            max_width = 0.5 * max(line.get_length(), 0.1)
            if label.get_width() > max_width:
                label.set_width(max_width)
            angle = (line.get_angle() % TAU) - TAU / 2
            if np.abs(angle) > TAU / 4:
                angle += np.sign(angle) * PI
            label.angle = angle
            label.next_to(line.get_center(), UP, SMALL_BUFF)
            label.rotate(angle, about_point=line.get_center())
            labels.add(label)
        return labels

    def get_distance_product_column(self, column_top=None, labels=None, fraction=None):
        if column_top is None:
            column_top = self.default_product_column_top
        if labels is None:
            if not hasattr(self, "numeric_distance_labels"):
                self.get_numeric_distance_labels()
            labels = self.numeric_distance_labels
        stacked_labels = labels.copy()
        for label in stacked_labels:
            label.rotate(-label.angle)
            label.set_height(self.numeric_distance_label_height)
        stacked_labels.arrange(DOWN)
        stacked_labels.move_to(column_top, UP)

        h_line = Line(LEFT, RIGHT)
        h_line.set_width(1.5 * stacked_labels.get_width())
        h_line.next_to(stacked_labels, DOWN, aligned_edge=RIGHT)
        times = MathTex("\\times")
        times.next_to(h_line, UP, SMALL_BUFF, aligned_edge=LEFT)

        product_decimal = DecimalNumber(
            self.get_distance_product(fraction),
            num_decimal_places=3,
        )
        product_decimal.set_height(self.numeric_distance_label_height)
        product_decimal.next_to(h_line, DOWN)
        product_decimal.align_to(stacked_labels, RIGHT)
        product_decimal.set_color(BLUE)
        self.distance_product_column = VGroup(
            stacked_labels, h_line, times, product_decimal
        )
        return self.distance_product_column

    def get_fractional_arc(self, fraction, start_fraction=0):
        arc = Arc(
            angle=fraction * TAU,
            start_angle=start_fraction * TAU,
            radius=self.get_radius(),
        )
        arc.shift(self.circle.get_center())
        return arc

    def get_halfway_indication_arcs(self):
        fraction = 0.5 / self.num_lighthouses
        arcs = VGroup(
            self.get_fractional_arc(fraction),
            self.get_fractional_arc(-fraction, start_fraction=2 * fraction),
        )
        arcs.set_stroke(YELLOW, 4)
        return arcs

    def get_circle_group(self):
        group = VGroup(self.circle)
        if not hasattr(self, "observer_dot"):
            self.get_observer_dot()
        if not hasattr(self, "observer"):
            self.get_observer()
        if not hasattr(self, "lighthouses"):
            self.get_lighthouses()
        if not hasattr(self, "lights"):
            self.get_lights()
        group.add(self.observer_dot, self.observer)
        if self.include_lighthouses:
            group.add(self.lighthouses)
        group.add(self.lights)
        return group

    def setup_lighthouses_and_observer(self):
        self.add(*self.get_circle_group())

    # Numerical results

    def get_radius(self):
        return self.circle.get_width() / 2.0

    def get_distance_product(self, fraction=None):
        radius = self.get_radius()
        observer_point = self.get_observer_point(fraction)
        distances = [
            np.linalg.norm(point - observer_point) / radius
            for point in self.get_lh_points()
        ]
        return reduce(op.mul, distances, 1.0)

    # Animating methods

    def add_numeric_distance_labels(self, show_line_creation=True):
        anims = []
        if not hasattr(self, "distance_lines"):
            self.get_distance_lines()
        if not hasattr(self, "numeric_distance_labels"):
            self.get_numeric_distance_labels()
        if show_line_creation:
            anims.append(LaggedStart(Create, self.distance_lines))
        anims.append(LaggedStart(FadeIn, self.numeric_distance_labels))

        self.play(*anims)

    def show_distance_product_in_column(self, **kwargs):
        group = self.get_distance_product_column(**kwargs)
        stacked_labels, h_line, times, product_decimal = group
        labels = self.numeric_distance_labels

        self.play(ReplacementTransform(labels.copy(), stacked_labels))
        self.play(
            Create(h_line),
            Write(times)
        )
        self.play(
            ReplacementTransform(
                stacked_labels.copy(),
                VGroup(product_decimal)
            )
        )
