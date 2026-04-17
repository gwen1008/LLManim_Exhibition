# Source: 3b1b/_2019/diffyq/part1/pendulum.py
# Description: [3b1b translated] 分析單擺受力，展示重力分解為切線與法線分量，推導加速度公式並探討角度變化。


from manim import *
import numpy as np

class AnalyzePendulumForce(MovingCameraScene):
    def __init__(
        self,
        pendulum_config={
            "length": 5,
            "top_point": 3.5 * UP,
            "initial_theta": 60 * DEGREES,
            "set_theta_label_height_cap": True,
        },
        g_vect_config={
            "length_multiple": 0.25,
        },
        tan_line_color=BLUE,
        perp_line_color=PINK,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.pendulum_config = pendulum_config
        self.g_vect_config = g_vect_config
        self.tan_line_color = tan_line_color
        self.perp_line_color = perp_line_color

    def construct(self):
        self.add_pendulum()
        self.show_arc_length()
        self.add_g_vect()
        self.show_constraint()
        self.break_g_vect_into_components()
        self.show_angle_geometry()
        self.show_gsin_formula()
        self.show_sign()
        self.show_acceleration_formula()
        # self.ask_about_what_to_do()

        # self.emphasize_theta()
        # self.show_angular_velocity()
        # self.show_angular_acceleration()
        # self.circle_g_sin_formula()

    def add_pendulum(self):
        pendulum = Pendulum(**self.pendulum_config)
        theta_tracker = ValueTracker(pendulum.get_theta())
        pendulum.add_updater(lambda p: p.set_theta(
            theta_tracker.get_value()
        ))

        self.add(pendulum)
        self.pendulum = pendulum
        self.theta_tracker = theta_tracker

    def show_arc_length(self):
        pendulum = self.pendulum
        angle = pendulum.get_theta()
        height = pendulum.length
        top = pendulum.get_fixed_point()

        line = Line(UP, DOWN)
        line.set_height(height)
        line.move_to(top, UP)
        arc = always_redraw(lambda: Arc(
            start_angle=-90 * DEGREES,
            angle=pendulum.get_theta(),
            arc_center=pendulum.get_fixed_point(),
            radius=pendulum.length,
            stroke_color=GREEN,
        ))

        brace = Brace(Line(ORIGIN, 5 * UP), RIGHT)
        brace.point = VectorizedPoint(brace.get_right())
        brace.add(brace.point)
        brace.set_height(angle)
        brace.move_to(ORIGIN, DL)
        brace.apply_complex_function(np.exp)
        brace.scale(height)
        brace.rotate(-90 * DEGREES)
        brace.move_to(arc)
        brace.shift(MED_SMALL_BUFF * normalize(
            arc.point_from_proportion(0.5) - top
        ))
        x_sym = MathTex("x")
        x_sym.set_color(GREEN)
        x_sym.next_to(brace.point, DR, buff=SMALL_BUFF)

        rhs = MathTex("=", "L", "\\theta")
        rhs.set_color_by_tex("\\theta", BLUE)
        rhs.next_to(x_sym, RIGHT)
        rhs.shift(0.7 * SMALL_BUFF * UP)
        line_L = MathTex("L")
        line_L.next_to(
            pendulum.rod.get_center(), UR, SMALL_BUFF,
        )

        self.play(
            Create(arc),
            Rotate(line, angle, about_point=top),
            UpdateFromAlphaFunc(
                line, lambda m, a: m.set_stroke(
                    width=2 * (2 * a if a < 0.5 else 2 * (1 - a))
                )
            ),
            GrowFromPoint(
                brace, line.get_bottom(),
                path_arc=angle
            ),
        )
        self.play(FadeIn(x_sym, shift=UP))
        self.wait()

        # Show equation
        line.set_stroke(BLUE, 5)
        self.play(
            Create(line),
            FadeOut(line),
            FadeIn(line_L, shift=DOWN)
        )
        self.play(
            TransformFromCopy(
                line_L, rhs.get_part_by_tex("L")
            ),
            Write(rhs.get_part_by_tex("="))
        )
        self.play(
            TransformFromCopy(
                pendulum.theta_label,
                rhs.get_parts_by_tex("\\theta"),
            )
        )
        self.add(rhs)

        x_eq = VGroup(x_sym, rhs)

        self.play(
            FadeOut(brace),
            x_eq.animate.rotate(angle / 2),
            x_eq.animate.next_to(arc.point_from_proportion(0.5),
            UL, buff=-MED_SMALL_BUFF)
        )

        self.x_eq = x_eq
        self.arc = arc
        self.line_L = line_L

    def add_g_vect(self):
        pendulum = self.pendulum

        g_vect = self.g_vect = GravityVector(
            pendulum, **self.g_vect_config,
        )
        g_word = self.g_word = Text("Gravity")
        g_word.rotate(-90 * DEGREES)
        g_word.scale(0.75)
        g_word.add_updater(lambda m: m.next_to(
            g_vect, RIGHT, buff=-SMALL_BUFF,
        ))

        self.play(
            GrowArrow(g_vect),
            FadeIn(g_word, shift=UP, lag_ratio=0.1),
        )
        self.wait()

    def show_constraint(self):
        pendulum = self.pendulum

        arcs = VGroup()
        for u in [-1, 2, -1]:
            d_theta = 40 * DEGREES * u
            arc = Arc(
                start_angle=pendulum.get_theta() - 90 * DEGREES,
                angle=d_theta,
                radius=pendulum.length,
                arc_center=pendulum.get_fixed_point(),
                stroke_width=2,
                stroke_color=YELLOW,
                stroke_opacity=0.5,
            )
            self.play(
                self.theta_tracker.increment_value(d_theta),
                Create(arc)
            )
            arcs.add(arc)
        self.play(FadeOut(arcs))

    def break_g_vect_into_components(self):
        g_vect = self.g_vect
        g_vect.component_lines = always_redraw(
            g_vect.create_component_lines
        )
        tan_line, perp_line = g_vect.component_lines
        g_vect.tangent = always_redraw(lambda: Arrow(
            tan_line.get_start(),
            tan_line.get_end(),
            buff=0,
            color=self.tan_line_color,
        ))
        g_vect.perp = always_redraw(lambda: Arrow(
            perp_line.get_start(),
            perp_line.get_end(),
            buff=0,
            color=self.perp_line_color,
        ))

        self.play(Create(g_vect.component_lines))
        self.play(GrowArrow(g_vect.tangent))
        self.wait()
        self.play(GrowArrow(g_vect.perp))
        self.wait()

    def show_angle_geometry(self):
        g_vect = self.g_vect

        arc = Arc(
            start_angle=90 * DEGREES,
            angle=self.pendulum.get_theta(),
            radius=0.5,
            arc_center=g_vect.get_end(),
        )
        q_mark = MathTex("?")
        q_mark.next_to(arc.get_center(), UL, SMALL_BUFF)
        theta_label = MathTex("\\theta")
        theta_label.move_to(q_mark)

        self.add(g_vect)
        self.play(
            Create(arc),
            Write(q_mark)
        )
        self.play(Indicate(q_mark))
        self.wait()
        self.play(Indicate(
            self.pendulum.theta_label
        ))
        self.play(
            TransformFromCopy(
                self.pendulum.theta_label,
                theta_label,
            ),
            FadeOut(q_mark)
        )
        self.wait()
        self.play(Wiggle(g_vect.tangent))
        self.play(Wiggle(
            Line(
                *g_vect.get_start_and_end(),
                buff=0,
            ).add_tip().match_style(g_vect),
        ))
        self.wait()
        self.play(
            FadeOut(arc),
            FadeOut(theta_label),
        )

    def show_gsin_formula(self):
        g_vect = self.g_vect
        g_word = self.g_word
        g_word.clear_updaters()

        g_term = self.g_term = MathTex("-g")
        g_term.add_updater(lambda m: m.next_to(
            g_vect,
            RIGHT if self.pendulum.get_theta() >= 0 else LEFT,
            SMALL_BUFF
        ))

        def create_vect_label(vect, tex, direction):
            label = MathTex(tex)
            label.set_stroke(width=0, background=True)
            label.add_background_rectangle()
            label.scale(0.7)
            max_width = 0.9 * vect.get_length()
            if label.get_width() > max_width:
                label.set_width(max_width)
            angle = vect.get_angle()
            angle = (angle + PI / 2) % PI - PI / 2
            label.next_to(ORIGIN, direction, SMALL_BUFF)
            label.rotate(angle, about_point=ORIGIN)
            label.shift(vect.get_center())
            return label

        g_sin_label = always_redraw(lambda: create_vect_label(
            g_vect.tangent, "-g\\sin(\\theta)", UP,
        ))
        g_cos_label = always_redraw(lambda: create_vect_label(
            g_vect.perp, "-g\\cos(\\theta)", DOWN,
        ))

        self.play(
            ReplacementTransform(g_word[0][0], g_term[0][1]),
            FadeOut(g_word[0][1:]),
            Write(g_term[0][0]),
        )
        self.add(g_term)
        self.wait()
        for label in g_sin_label, g_cos_label:
            self.play(
                GrowFromPoint(label[0], g_term.get_center()),
                TransformFromCopy(g_term, label[1][:2]),
                GrowFromPoint(label[1][2:], g_term.get_center()),
            )
            self.add(label)
            self.wait()

        self.g_sin_label = g_sin_label
        self.g_cos_label = g_cos_label

    def show_sign(self):
        get_theta = self.pendulum.get_theta
        theta_decimal = DecimalNumber(include_sign=True)
        theta_decimal.add_updater(lambda d: d.set_value(
            get_theta()
        ))
        theta_decimal.add_updater(lambda m: m.next_to(
            self.pendulum.theta_label, DOWN
        ))
        theta_decimal.add_updater(lambda m: m.set_color(
            GREEN if get_theta() > 0 else RED
        ))

        self.play(
            FadeIn(theta_decimal, shift=UP),
            FadeOut(self.x_eq),
            FadeOut(self.line_L),
        )
        self.set_theta(-60 * DEGREES, run_time=4)
        self.set_theta(60 * DEGREES, run_time=4)
        self.play(
            FadeOut(theta_decimal),
            FadeIn(self.x_eq),
        )

    def show_acceleration_formula(self):
        x_eq = self.x_eq
        g_sin_theta = self.g_sin_label

        equation = MathTex(
            "a", "=",
            "\\ddot", "x",
            "=",
            "-", "g", "\\sin\\big(", "\\theta", "\\big)",
        )
        equation.to_edge(LEFT)

        second_deriv = equation[2:4]
        x_part = equation.get_part_by_tex("x")
        x_part.set_color(GREEN)
        a_eq = equation[:2]
        eq2 = equation.get_parts_by_tex("=")[1]
        rhs = equation[5:]

        second_deriv_L_form = MathTex(
            "L", "\\ddot", "\\theta"
        )
        second_deriv_L_form.move_to(second_deriv, DOWN)
        eq3 = MathTex("=")
        eq3.rotate(90 * DEGREES)
        eq3.next_to(second_deriv_L_form, UP)

        g_L_frac = MathTex(
            "-", "{g", "\\over", "L}"
        )
        g_L_frac.move_to(rhs[:2], LEFT)
        g_L_frac.shift(SMALL_BUFF * UP / 2)

        mu_term = MathTex(
            "-\\mu", "\\dot", "\\theta",
        )
        mu_term.next_to(g_L_frac, LEFT)
        mu_term.shift(SMALL_BUFF * UP / 2)

        mu_brace = Brace(mu_term, UP)
        mu_word = mu_brace.get_text("Air resistance")

        for mob in equation, second_deriv_L_form, mu_term:
            mob.set_color_by_tex("\\theta", BLUE)

        self.play(
            TransformFromCopy(x_eq[0], x_part),
            Write(equation[:3]),
        )
        self.wait()
        self.play(
            Write(eq2),
            TransformFromCopy(g_sin_theta, rhs)
        )
        self.wait()
        #
        self.show_acceleration_at_different_angles()
        #
        self.play(
            FadeInFromDown(second_deriv_L_form),
            Write(eq3),
            second_deriv.animate.next_to(eq3, UP),
            a_eq.animate.shift(SMALL_BUFF * LEFT),
            eq2.animate.shift(SMALL_BUFF * RIGHT),
            rhs.animate.shift(SMALL_BUFF * RIGHT),
        )
        self.wait()
        self.wait()
        self.play(
            FadeOut(a_eq),
            FadeOut(second_deriv),
            FadeOut(eq3),
            ReplacementTransform(
                second_deriv_L_form.get_part_by_tex("L"),
                g_L_frac.get_part_by_tex("L"),
            ),
            ReplacementTransform(
                equation.get_part_by_tex("-"),
                g_L_frac.get_part_by_tex("-"),
            ),
            ReplacementTransform(
                equation.get_part_by_tex("g"),
                g_L_frac.get_part_by_tex("g"),
            ),
            Write(g_L_frac.get_part_by_tex("\\over")),
            rhs[2:].animate.next_to(g_L_frac, RIGHT, buff=SMALL_BUFF),
        )
        self.wait()
        self.play(
            GrowFromCenter(mu_term),
            VGroup(eq2, second_deriv_L_form[1:]).animate.next_to(
            mu_term, LEFT),
        )
        self.play(
            GrowFromCenter(mu_brace),
            FadeInFromDown(mu_word),
        )

    def show_acceleration_at_different_angles(self):
        to_fade = VGroup(
            self.g_cos_label,
            self.g_vect.perp,
        )
        new_comp_line_sytle = {
            "stroke_width": 0.5,
            "stroke_opacity": 0.25,
        }

        self.play(
            FadeOut(self.x_eq),
            to_fade.animate.set_opacity(0.25),
            self.g_vect.component_lines.animate.set_style(
            new_comp_line_sytle)
        )
        self.g_vect.component_lines.add_updater(
            lambda m: m.set_style(**new_comp_line_sytle)
        )
        for mob in to_fade:
            mob.add_updater(lambda m: m.set_opacity(0.25))

        self.set_theta(0)
        self.wait(2)
        self.set_theta(89.9 * DEGREES, run_time=3)
        self.wait(2)
        self.set_theta(
            60 * DEGREES,
            FadeIn(self.x_eq),
            run_time=2,
        )
        self.wait()

    def ask_about_what_to_do(self):
        g_vect = self.g_vect
        g_sin_label = self.g_sin_label
        angle = g_vect.tangent.get_angle()
        angle = (angle - PI) % TAU

        randy = You()
        randy.to_corner(DL)
        bubble = randy.get_bubble(
            height=2,
            width=3.5,
        )
        g_sin_copy = g_sin_label.copy()
        g_sin_copy.remove(g_sin_copy[0])
        g_sin_copy.generate_target()
        g_sin_copy.target.scale(1 / 0.75)
        g_sin_copy.target.rotate(-angle)
        a_eq = MathTex("a=")
        thought_term = VGroup(a_eq, g_sin_copy.target)
        thought_term.arrange(RIGHT, buff=SMALL_BUFF)
        thought_term.move_to(bubble.get_bubble_center())

        rect = SurroundingRectangle(g_sin_copy.target)
        rect.rotate(angle)
        rect.move_to(g_sin_label)

        randy.save_state()
        randy.fade(1)
        self.play(randy.restore, randy.change, "pondering")
        self.play(Create(rect), FadeOut(rect))
        self.play(
            Create(bubble),
            Write(a_eq),
            MoveToTarget(g_sin_copy),
            randy.look_at, bubble,
        )
        thought_term.remove(g_sin_copy.target)
        thought_term.add(g_sin_copy)
        self.play(Blink(randy))
        self.wait()
        self.play(
            Create(thought_term.copy().set_style(
                stroke_color=YELLOW,
                stroke_width=2,
                fill_opacity=0,
            )),
            FadeOut(thought_term.copy()),
            run_time=2,
            lag_ratio=0.2,
        )
        self.play(Blink(randy))
        self.play(
            FadeOut(randy),
            FadeOut(bubble),
            thought_term.animate.next_to(self.pendulum, DOWN, LARGE_BUFF)
        )

        self.accleration_equation = thought_term

    def emphasize_theta(self):
        pendulum = self.pendulum

        self.play(Indicate(pendulum.theta_label))
        self.play(Indicate(pendulum.theta_label))

        pendulum_copy = pendulum.deepcopy()
        pendulum_copy.clear_updaters()
        pendulum_copy.fade(1)
        pendulum_copy.start_swinging()

        def new_updater(p):
            p.set_theta(pendulum_copy.get_theta())
        pendulum.add_updater(new_updater)

        self.add(pendulum_copy)
        self.wait(5)
        pendulum_copy.end_swinging()
        self.remove(pendulum_copy)
        pendulum.remove_updater(new_updater)
        self.update_mobjects(0)

    def show_angular_velocity(self):
        pass

    def show_angular_acceleration(self):
        pass

    def circle_g_sin_formula(self):
        self.play(
            Indicate(self.accleration_equation)
        )

    #
    def set_theta(self, value, *added_anims, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 2)
        self.play(
            self.theta_tracker.animate.set_value(value),
            *added_anims,
            **kwargs,
        )

# 注意：GravityVector 和 Pendulum 類別需要另外定義或從原專案導入
