# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示從圓心出發的線段繞著一個偏心點旋轉後，所有線段端點形成一個完美橢圓的過程。


from manim import *
import random

class ShowEmergingEllipse(Scene):
    def __init__(
        self,
        circle_radius=3,
        circle_color=BLUE,
        num_lines=150,
        lines_stroke_width=1,
        eccentricity_vector=2 * RIGHT,
        ghost_lines_stroke_color=GREY_B,
        ghost_lines_stroke_width=0.5,
        ellipse_color=PINK,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.circle_radius = circle_radius
        self.circle_color = circle_color
        self.num_lines = num_lines
        self.lines_stroke_width = lines_stroke_width
        self.eccentricity_vector = eccentricity_vector
        self.ghost_lines_stroke_color = ghost_lines_stroke_color
        self.ghost_lines_stroke_width = ghost_lines_stroke_width
        self.ellipse_color = ellipse_color

    def construct(self):
        circle = self.get_circle()
        e_point = self.get_eccentricity_point()
        e_dot = Dot(e_point, color=YELLOW)
        lines = self.get_lines()
        ellipse = self.get_ellipse()

        fade_rect = FullScreenFadeRectangle()

        line = lines[len(lines) // 5]
        line_dot = Dot(line.get_center(), color=YELLOW)
        line_dot.scale(0.5)

        ghost_line = self.get_ghost_lines(line)
        ghost_lines = self.get_ghost_lines(lines)

        rot_words = Text("Rotate $90^\\circ$ \\\\ about center")
        rot_words.next_to(line_dot, RIGHT)

        elbow = self.get_elbow(line)

        eccentric_words = Text("``Eccentric'' point")
        eccentric_words.next_to(circle.get_center(), DOWN)

        ellipse_words = Text("Perfect ellipse")
        ellipse_words.next_to(ellipse, UP, buff=SMALL_BUFF)

        for text in [rot_words, ellipse_words]:
            text.add_to_back(text.copy().set_stroke(BLACK, 5))

        shuffled_lines = VGroup(*lines)
        random.shuffle(shuffled_lines.submobjects)

        self.play(Create(circle))
        self.play(
            FadeIn(e_dot, shift=LEFT),
            Write(eccentric_words, run_time=1)
        )
        self.wait()
        self.play(
            LaggedStartMap(Create, shuffled_lines),
            Animation(VGroup(e_dot, circle)),
            FadeOut(eccentric_words)
        )
        self.add(ghost_lines)
        self.add(e_dot, circle)
        self.wait()
        self.play(
            FadeIn(fade_rect),
            Animation(line),
            GrowFromCenter(line_dot),
            FadeIn(rot_words, shift=DOWN),
        )
        self.wait()
        self.add(ghost_line)
        self.play(
            MoveToTarget(line, path_arc=90 * DEGREES),
            Animation(rot_words),
            Create(elbow)
        )
        self.wait()
        self.play(
            FadeOut(fade_rect),
            FadeOut(line_dot),
            FadeOut(rot_words),
            FadeOut(elbow),
            Animation(line),
            Animation(ghost_line)
        )
        self.play(
            LaggedStartMap(MoveToTarget, lines, run_time=4),
            Animation(VGroup(e_dot, circle))
        )
        self.wait()
        self.play(
            Create(ellipse),
            FadeIn(ellipse_words, shift=DOWN)
        )
        self.wait()

    def get_circle(self):
        circle = self.circle = Circle(
            radius=self.circle_radius,
            color=self.circle_color
        )
        return circle

    def get_eccentricity_point(self):
        return self.circle.get_center() + self.eccentricity_vector

    def get_lines(self):
        center = self.circle.get_center()
        radius = self.circle.get_width() / 2
        e_point = self.get_eccentricity_point()
        lines = VGroup(*[
            Line(
                e_point,
                center + rotate_vector(radius * RIGHT, angle)
            )
            for angle in np.linspace(0, TAU, self.num_lines)
        ])
        lines.set_stroke(width=self.lines_stroke_width)
        for line in lines:
            line.generate_target()
            line.target.rotate(90 * DEGREES)
        return lines

    def get_ghost_lines(self, lines):
        return lines.copy().set_stroke(
            color=self.ghost_lines_stroke_color,
            width=self.ghost_lines_stroke_width
        )

    def get_elbow(self, line):
        elbow = VGroup(Line(UP, UL), Line(UL, LEFT))
        elbow.set_stroke(width=1)
        elbow.scale(0.2, about_point=ORIGIN)
        elbow.rotate(
            line.get_angle() - 90 * DEGREES,
            about_point=ORIGIN
        )
        elbow.shift(line.get_center())
        return elbow

    def get_ellipse(self):
        center = self.circle.get_center()
        e_point = self.get_eccentricity_point()
        radius = self.circle.get_width() / 2

        # Ellipse parameters
        a = radius / 2
        c = np.linalg.norm(e_point - center) / 2
        b = np.sqrt(a**2 - c**2)

        result = Circle(radius=b, color=self.ellipse_color)
        result.stretch(a / b, 0)
        result.move_to(Line(center, e_point))
        return result
