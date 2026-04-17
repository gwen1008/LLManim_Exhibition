# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示複數平面上的單位圓通過球極投影映射到實數軸的過程，包括點與線的動態投影和特殊點的說明。


from manim import *
import numpy as np

class IntroduceStereographicProjection(MovingCameraScene):
    def __init__(self, n_sample_points=16, circle_config=None, example_angles=None, **kwargs):
        super().__init__(**kwargs)
        self.n_sample_points = n_sample_points
        if circle_config is None:
            circle_config = {
                "n_pieces": 16,
                "radius": 2,
                "stroke_width": 7,
            }
        self.circle_config = circle_config
        if example_angles is None:
            example_angles = [
                30 * DEGREES,
                120 * DEGREES,
                240 * DEGREES,
                80 * DEGREES,
                -60 * DEGREES,
                135 * DEGREES,
            ]
        self.example_angles = example_angles

    def construct(self):
        self.setup_plane()
        self.draw_lines()
        self.describe_individual_points()
        self.remind_that_most_points_are_not_projected()

    def setup_plane(self):
        self.plane = self.get_plane()
        self.circle = self.get_circle()
        self.circle_shadow = self.get_circle_shadow()

        self.add(self.plane)
        self.add(self.circle_shadow)
        self.add(self.circle)

    def draw_lines(self):
        plane = self.plane
        circle = self.circle
        circle.save_state()
        circle.generate_target()
        self.project_mobject(circle.target)

        circle_points = self.get_sample_circle_points()
        dots = VGroup(*[Dot(p) for p in circle_points])
        dots.set_sheen(-0.2, DR)
        dots.set_stroke(GREY_D, 2, background=True)
        arrows = VGroup()
        for dot in dots:
            dot.scale(0.75)
            dot.generate_target()
            dot.target.move_to(
                self.project(dot.get_center())
            )
            arrow = Arrow(
                dot.get_center(),
                dot.target.get_center(),
            )
            arrows.add(arrow)
        neg_one_point = plane.number_to_point(-1)
        neg_one_dot = Dot(neg_one_point)
        neg_one_dot.set_fill(YELLOW)

        lines = self.get_lines()

        special_index = self.n_sample_points // 2 + 1
        line = lines[special_index]
        dot = dots[special_index]
        arrow = arrows[special_index]
        dot_target_outline = dot.target.copy()
        dot_target_outline.set_stroke(RED, 2)
        dot_target_outline.set_fill(opacity=0)
        dot_target_outline.scale(1.5)

        v_line = Line(UP, DOWN)
        v_line.set_height(config.frame_height)
        v_line.set_stroke(RED, 5)

        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots]))
        self.play(FadeIn(neg_one_dot, scale=2))
        self.add(lines, neg_one_dot, dots)
        self.play(LaggedStart(*[Create(line) for line in lines]))
        self.wait()
        self.play(
            lines.animate.set_stroke(width=0.5),
            line.animate.set_stroke(width=4),
        )
        self.play(Create(dot_target_outline))
        self.play(Create(v_line), run_time=0.5)
        self.play(FadeOut(v_line), run_time=0.5)
        self.play(MoveToTarget(dot))
        self.wait()
        self.play(
            lines.animate.set_stroke(width=1),
            FadeOut(dot_target_outline),
            MoveToTarget(circle),
            *[MoveToTarget(d) for d in dots],
            run_time=2,
        )
        self.wait()

        self.lines = lines
        self.dots = dots

    def describe_individual_points(self):
        plane = self.plane
        one_point, zero_point, i_point, neg_i_point, neg_one_point = [
            plane.number_to_point(n)
            for n in [1, 0, complex(0, 1), complex(0, -1), -1]
        ]
        
        # 自定義 PushPin 類
        class PushPin(Dot):
            def pin_to(self, point):
                self.move_to(point)
                return self
        
        i_pin = PushPin()
        i_pin.pin_to(i_point)
        neg_i_pin = PushPin()
        neg_i_pin.pin_to(neg_i_point)

        dot = Dot()
        dot.set_stroke(RED, 3)
        dot.set_fill(opacity=0)
        dot.scale(1.5)
        dot.move_to(one_point)

        arc1 = Arc(angle=TAU / 4, radius=2)
        arc2 = Arc(
            angle=85 * DEGREES, radius=2,
            start_angle=TAU / 4,
        )
        arc3 = Arc(
            angle=-85 * DEGREES, radius=2,
            start_angle=-TAU / 4,
        )
        VGroup(arc1, arc2, arc3).set_stroke(RED)

        frame = self.camera.frame
        frame_height_tracker = ValueTracker(frame.height)
        
        def frame_height_growth(mob, dt):
            mob.set_value(mob.get_value() + 0.5 * dt)
        
        frame_height_tracker.add_updater(frame_height_growth)

        neg_one_tangent = VGroup(
            Line(ORIGIN, UP),
            Line(ORIGIN, DOWN),
        )
        neg_one_tangent.set_height(25)
        neg_one_tangent.set_stroke(YELLOW, 5)
        neg_one_tangent.move_to(neg_one_point)

        self.play(Create(dot))
        self.wait()
        self.play(dot.animate.move_to(zero_point))
        self.wait()
        dot.move_to(i_point)
        self.play(Create(dot))
        self.play(FadeIn(i_pin, shift=UL))
        self.wait()
        self.play(
            dot.animate.move_to(neg_i_point).set_path_arc(-60 * DEGREES)
        )
        self.play(FadeIn(neg_i_pin, shift=UL))
        self.wait()
        self.play(
            dot.animate.move_to(one_point).set_path_arc(-60 * DEGREES)
        )
        
        def update_frame(mob):
            mob.set_height(frame_height_tracker.get_value())
        
        frame.add_updater(update_frame)

        triplets = [
            (arc1, i_point, TAU / 4),
            (arc2, neg_one_point, TAU / 4),
            (arc3, neg_one_point, -TAU / 4),
        ]
        for arc, point, path_arc in triplets:
            self.play(
                Create(arc),
                dot.animate.move_to(point).set_path_arc(path_arc),
                run_time=2
            )
            self.wait()
            self.play(
                ApplyFunction(self.project_mobject, arc, run_time=2)
            )
            self.wait()
            self.play(FadeOut(arc))
            self.wait()
            if arc is arc1:
                self.add(frame, frame_height_tracker)
            elif arc is arc2:
                self.play(dot.animate.move_to(neg_i_point))
        self.wait(2)
        self.play(*[Create(t) for t in neg_one_tangent])
        self.wait()
        self.play(FadeOut(neg_one_tangent))
        self.wait(2)
        frame.clear_updaters()
        frame_height_tracker.clear_updaters()
        self.play(
            frame.animate.set_height(config.frame_height),
            self.lines.animate.set_stroke(width=0.5),
            FadeOut(self.dots),
            FadeOut(dot),
            run_time=2,
        )

    def remind_that_most_points_are_not_projected(self):
        plane = self.plane
        circle = self.circle

        sample_values = [0, complex(1, 1), complex(-2, -1)]
        sample_points = [
            plane.number_to_point(value)
            for value in sample_values
        ]
        sample_dots = VGroup(*[Dot(p) for p in sample_points])
        sample_dots.set_fill(GREEN)

        self.play(
            FadeOut(self.lines),
            Restore(circle),
        )

        for value, dot in zip(sample_values, sample_dots):
            cross = Cross(dot)
            cross.scale(2)
            label = Integer(value) if isinstance(value, (int, float)) else Text(str(value))
            if value is sample_values[1]:
                label.next_to(dot, UL, buff=SMALL_BUFF)
            else:
                label.next_to(dot, UR, buff=SMALL_BUFF)
            self.play(
                FadeIn(dot, scale=3),
                FadeIn(label, shift=DOWN)
            )
            self.play(Create(cross))
            self.play(*[FadeOut(mob) for mob in [dot, cross, label]])
        self.wait()
        self.play(
            FadeIn(self.lines),
            MoveToTarget(circle, run_time=2),
        )
        self.wait()

    # Helpers
    def get_plane(self):
        plane = ComplexPlane(
            unit_size=2,
            color=GREY,
            secondary_color=GREY_D,
            x_range=[-config.frame_width/2, config.frame_width/2],
            y_range=[-config.frame_height/2, config.frame_height/2],
            stroke_width=2,
        )
        plane.add_coordinates()
        return plane

    def get_circle(self):
        # 自定義 CheckeredCircle 類
        class CheckeredCircle(Circle):
            def __init__(self, n_pieces=16, radius=2, stroke_width=7, **kwargs):
                super().__init__(radius=radius, stroke_width=stroke_width, **kwargs)
                self.n_pieces = n_pieces
                
        circle = CheckeredCircle(
            **self.circle_config
        )
        circle.set_stroke(width=7)
        return circle

    def get_circle_shadow(self):
        class CheckeredCircle(Circle):
            def __init__(self, n_pieces=16, radius=2, stroke_width=7, **kwargs):
                super().__init__(radius=radius, stroke_width=stroke_width, **kwargs)
                self.n_pieces = n_pieces
                
        circle_shadow = CheckeredCircle(
            **self.circle_config
        )
        circle_shadow.set_stroke(opacity=0.65)
        return circle_shadow

    def get_sample_circle_points(self):
        plane = self.plane
        n = self.n_sample_points
        rotater = 1
        if hasattr(self, "circle_shadow"):
            point = self.circle_shadow[0].get_points()[0]
            rotater = complex(*point[:2])
            rotater /= abs(rotater)
        numbers = [
            rotater * np.exp(complex(0, TAU * x / n))
            for x in range(-(n // 2) + 1, n // 2)
        ]
        return [
            plane.number_to_point(number)
            for number in numbers
        ]

    def get_lines(self):
        plane = self.plane
        neg_one_point = plane.number_to_point(-1)
        circle_points = self.get_sample_circle_points()

        lines = VGroup(*[
            Line(neg_one_point, point)
            for point in circle_points
        ])
        for line in lines:
            length = line.get_length()
            line.scale(20 / length, about_point=neg_one_point)
            line.set_stroke(YELLOW, np.clip(length, 0, 1))
        return lines

    def project(self, point):
        # 簡化的球極投影函數
        x, y, z = point
        r = 2
        if abs(x + r) < 0.001:
            return np.array([100, 0, 0])  # 處理奇點
        factor = 2 * r / (x + r)
        return np.array([factor * r - r, factor * y, 0])

    def project_mobject(self, mobject):
        # 對整個物體應用投影
        mobject.apply_function(lambda p: self.project(p))
        return mobject
