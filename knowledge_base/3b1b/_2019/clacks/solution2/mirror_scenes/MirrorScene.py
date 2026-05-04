# Source: 3b1b/_2019/clacks/solution2/mirror_scenes.py
# Description: [3b1b translated] 展示光束在兩面鏡子之間反射的軌跡，隨著鏡子夾角變化，光束反射次數也隨之改變。


from manim import *
import numpy as np

class MirrorScene(Scene):
    def __init__(
        self,
        center=DOWN + 3 * LEFT,
        line_length=config.frame_width,
        start_theta=np.arctan(0.25),
        start_y_offset=0.5,
        start_x_offset=8,
        arc_config={
            "radius": 1,
            "stroke_color": WHITE,
            "stroke_width": 2,
        },
        trajectory_point_spacing=0.1,
        trajectory_style={
            "stroke_color": YELLOW,
            "stroke_width": 2,
        },
        ghost_lines_style={
            "stroke_color": WHITE,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        },
        reflect_sound="pen_click",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.center = center
        self.line_length = line_length
        self.start_theta = start_theta
        self.start_y_offset = start_y_offset
        self.start_x_offset = start_x_offset
        self.arc_config = arc_config
        self.trajectory_point_spacing = trajectory_point_spacing
        self.trajectory_style = trajectory_style
        self.ghost_lines_style = ghost_lines_style
        self.reflect_sound = reflect_sound

    def setup(self):
        self.theta_tracker = ValueTracker(self.start_theta)
        self.start_y_offset_tracker = ValueTracker(self.start_y_offset)
        self.start_x_offset_tracker = ValueTracker(self.start_x_offset)
        self.center_tracker = VectorizedPoint(self.center)
        self.beam_point = VectorizedPoint(np.array([
            self.get_start_x_offset(),
            self.get_start_y_offset(),
            0
        ]))
        self.ghost_beam_point = self.beam_point.copy()
        self.is_sound_allowed = False

        self.mirrors = self.get_mirrors()
        self.arc = self.get_arc()
        self.theta_symbol = self.get_theta_symbol()
        self.trajectory = self.get_trajectory()
        self.ghost_trajectory = self.get_ghost_trajectory()
        self.theta_display = self.get_theta_display()
        self.count_display_word = self.get_count_display_word()
        self.count_display_number = self.get_count_display_number()
        self.last_count = self.get_count()

        # Add some of them
        self.add(
            self.mirrors,
            self.arc,
            self.theta_symbol,
            self.theta_display,
            self.count_display_word,
            self.count_display_number,
        )

    def get_center(self):
        return self.center_tracker.get_location()

    def get_theta(self):
        return self.theta_tracker.get_value()

    def get_start_y_offset(self):
        return self.start_y_offset_tracker.get_value()

    def get_start_x_offset(self):
        return self.start_x_offset_tracker.get_value()

    def get_mirror(self):
        mirror = VGroup(
            Line(ORIGIN, 2 * RIGHT),
            Line(ORIGIN, 2 * RIGHT),
            Line(ORIGIN, (self.line_length - 4) * RIGHT),
        )
        mirror.arrange(RIGHT, buff=0)
        mirror.set_stroke(width=5)
        mirror[0::2].set_color((WHITE, GREY))
        mirror[1::2].set_color((GREY, WHITE))
        return mirror

    def get_mirrors(self):
        mirrors = VGroup(self.get_mirror(), self.get_mirror())

        def update_mirrors(mirrors):
            m1, m2 = mirrors
            center = self.get_center()
            theta = self.get_theta()
            m1.move_to(center, DL)
            m2.become(m1)
            m2.rotate(theta, about_point=center)

        mirrors.add_updater(update_mirrors)
        return mirrors

    def get_arc(self, radius=0.5):
        return always_redraw(lambda: Arc(
            start_angle=0,
            angle=self.get_theta(),
            arc_center=self.get_center(),
            **self.arc_config,
        ))

    def get_theta_symbol(self, arc=None, buff=0.15):
        if arc is None:
            arc = self.arc
        symbol = MathTex("\\theta")

        def update_symbol(symbol):
            midpoint = arc.point_from_proportion(0.5)
            center = arc.arc_center
            vect = (midpoint - center)
            max_height = 0.8 * arc.get_height()
            if symbol.get_height() > max_height:
                symbol.set_height(max_height)
            symbol.move_to(
                center + vect + buff * normalize(vect)
            )
        symbol.add_updater(update_symbol)
        return symbol

    def get_ghost_collision_points(self):
        x = self.get_start_x_offset()
        y = self.get_start_y_offset()
        theta = self.get_theta()

        points = [np.array([x, y, 0])]
        points += [
            np.array([x, y, 0])
            for k in range(1, int(PI / theta) + 1)
            for x in [y / np.tan(k * theta)]
            if abs(x) < config.frame_width
        ]
        points.append(points[-1] + x * LEFT)
        points = np.array(points)
        points += self.get_center()
        return points

    def get_collision_points(self, ghost_points=None):
        if ghost_points is None:
            ghost_points = self.get_ghost_collision_points()
        theta = self.get_theta()
        center = self.get_center()
        points = []
        for ghost_point in ghost_points:
            vect = ghost_point - center
            angle = angle_of_vector(vect)
            k = int(angle / theta)
            if k % 2 == 0:
                vect = rotate_vector(vect, -k * theta)
            else:
                vect = rotate_vector(vect, -(k + 1) * theta)
                vect[1] = abs(vect[1])
            points.append(center + vect)
        return points

    def get_trajectory(self, collision_points=None):
        if collision_points is None:
            collision_points = self.get_collision_points()
        points = []
        spacing = self.trajectory_point_spacing
        for p0, p1 in zip(collision_points, collision_points[1:]):
            n_intervals = max(1, int(np.linalg.norm(p1 - p0) / spacing))
            for alpha in np.linspace(0, 1, n_intervals + 1):
                points.append(interpolate(p0, p1, alpha))
        trajectory = VMobject()
        trajectory.set_points_as_corners(points)
        trajectory.set_style(**self.trajectory_style)
        return trajectory

    def get_ghost_trajectory(self):
        return self.get_trajectory(self.get_ghost_collision_points())

    def get_collision_point_counts(self, collision_points=None):
        if collision_points is None:
            collision_points = self.get_collision_points()[1:-1]
        result = VGroup()
        for n, point in enumerate(collision_points):
            count = Integer(n + 1)
            count.set_height(0.25)
            vect = UP if n % 2 == 0 else DOWN
            count.next_to(point, vect, SMALL_BUFF)
            result.add(count)
        return result

    def get_collision_count_anim(self, collision_point_counts=None):
        if collision_point_counts is None:
            collision_point_counts = self.get_collision_point_counts()
        group = VGroup()

        def update(group):
            count = self.get_count()
            if count == 0:
                group.submobjects = []
            elif count < len(collision_point_counts) + 1:
                group.submobjects = [
                    collision_point_counts[count - 1]
                ]

        return UpdateFromFunc(group, update, remover=True)

    def get_ghost_lines(self):
        line = self.mirrors[0]
        center = self.get_center()
        theta = self.get_theta()
        lines = VGroup()
        for k in range(1, int(PI / theta) + 2):
            new_line = line.copy()
            new_line.rotate(k * theta, about_point=center)
            lines.add(new_line)
        lines.set_style(**self.ghost_lines_style)
        return lines

    # Displays
    def get_theta_display(self):
        lhs = MathTex("\\theta = ")
        radians = DecimalNumber()
        radians.add_updater(
            lambda m: m.set_value(self.get_theta())
        )
        radians_word = Text("radians")
        radians_word.next_to(
            radians, RIGHT, aligned_edge=DOWN
        )
        equals = MathTex("=")
        degrees = Integer(0, unit="^\\circ")
        degrees.add_updater(
            lambda m: m.set_value(
                int(np.round(self.get_theta() / DEGREES))
            )
        )
        group = VGroup(lhs, radians, radians_word, equals, degrees)
        group.arrange(RIGHT, aligned_edge=DOWN)
        equals.align_to(lhs[-1], DOWN)
        group.to_corner(UL)
        return group

    def get_count_display_word(self):
        result = Text("\\# Bounces: ")
        result.to_corner(UL)
        result.shift(DOWN)
        result.set_color(YELLOW)
        return result

    def get_count_display_number(self, count_display_word=None, ghost_beam_point=None):
        if count_display_word is None:
            count_display_word = self.count_display_word
        result = Integer()
        result.next_to(
            count_display_word[-1], RIGHT,
            aligned_edge=DOWN,
        )
        result.set_color(YELLOW)
        result.add_updater(
            lambda m: m.set_value(self.get_count())
        )
        return result

    def get_count(self, ghost_beam_point=None):
        if ghost_beam_point is None:
            ghost_beam_point = self.ghost_beam_point.get_location()
        angle = angle_of_vector(
            ghost_beam_point - self.get_center()
        )
        return int(angle / self.get_theta())

    # Sounds
    def allow_sound(self):
        self.is_sound_allowed = True

    def disallow_sound(self):
        self.is_sound_allowed = False

    def update_mobjects(self, dt):
        super().update_mobjects(dt)
        if self.get_count() != self.last_count:
            self.last_count = self.get_count()
            if self.is_sound_allowed:
                self.add_sound(
                    self.reflect_sound,
                    gain=-20,
                )

    # Bouncing animations
    def show_bouncing(self, run_time=5):
        trajectory = self.trajectory
        ghost_trajectory = self.get_ghost_trajectory()

        beam_anims = self.get_shooting_beam_anims(
            trajectory, ghost_trajectory
        )
        count_anim = self.get_collision_count_anim()

        self.allow_sound()
        self.play(count_anim, *beam_anims, run_time=run_time)
        self.disallow_sound()

    def get_special_flash(self, mobject, stroke_width, time_width, rate_func=linear, **kwargs):
        kwargs["rate_func"] = rate_func
        mob_copy = mobject.copy()
        mob_copy.set_stroke(width=stroke_width)
        mob_copy.time_width = time_width
        return UpdateFromAlphaFunc(
            mob_copy,
            lambda m, a: m.pointwise_become_partial(
                mobject,
                max(a - (1 - a) * m.time_width, 0),
                a,
            ),
            **kwargs
        )

    def get_shooting_beam_anims(self,
                                trajectory,
                                ghost_trajectory=None,
                                update_beam_point=True,
                                num_flashes=20,
                                min_time_width=0.01,
                                max_time_width=0.5,
                                min_stroke_width=0.01,
                                max_stroke_width=6,
                                fade_trajectory=True,
                                faded_trajectory_width=0.25,
                                faded_trajectory_time_exp=0.2,
                                ):
        # Most flashes
        result = [
            self.get_special_flash(trajectory, stroke_width, time_width)
            for stroke_width, time_width in zip(
                np.linspace(max_stroke_width, min_stroke_width, num_flashes),
                np.linspace(min_time_width, max_time_width, num_flashes),
            )
        ]

        # Make sure beam point is updated
        if update_beam_point:
            smallest_flash = result[0]
            result.append(
                UpdateFromFunc(
                    self.beam_point,
                    lambda m: m.move_to(smallest_flash.mobject.get_points()[-1])
                )
            )

        # Make sure ghost beam point is updated
        if ghost_trajectory:
            ghost_flash = self.get_special_flash(
                ghost_trajectory, 0, min_time_width,
            )
            ghost_beam_point_update = UpdateFromFunc(
                self.ghost_beam_point,
                lambda m: m.move_to(ghost_flash.mobject.get_points()[-1])
            )
            result += [
                ghost_flash,
                ghost_beam_point_update,
            ]

        # Fade trajectory
        if fade_trajectory:
            ftte = faded_trajectory_time_exp
            result.append(
                ApplyMethod(
                    trajectory.animate.set_stroke(
                        width=faded_trajectory_width
                    ),
                    rate_func=lambda t: there_and_back(t)**ftte
                ),
            )
        return result
