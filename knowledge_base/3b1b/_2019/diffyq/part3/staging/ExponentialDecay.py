# Source: 3b1b/_2019/diffyq/part3/staging.py
# Description: [3b1b translated] 展示指數衰減函數的微分方程與動態圖形，包含 Pi 生物思考、坐標軸、追蹤點、變化率箭頭和導數推導過程。



from manim import *
class ExponentialDecay(PiCreatureScene):
    def construct(self):
        k = 0.2
        mk_tex = "-0.2"
        mk_tex_color = GREEN
        t2c = {mk_tex: mk_tex_color}

        # Pi creature
        randy = self.pi_creature
        randy.flip()
        randy.set_height(2.5)
        randy.move_to(3 * RIGHT)
        randy.to_edge(DOWN)
        bubble = ThoughtBubble(
            direction=LEFT,
            height=3.5,
            width=3,
        )
        bubble.pin_to(randy)
        bubble.set_fill(GREY_E, opacity=1)
        exp = MathTex(
            "Ce^{", mk_tex, "t}",
            tex_to_color_map=t2c,
        )
        exp.move_to(bubble.get_bubble_center())

        # Setup axes
        axes = Axes(
            x_range=[0, 13, 1],
            y_range=[-4, 4, 1],
            axis_config={"stroke_width": 2, "stroke_color": GREY_B},
        )
        axes.scale(0.9)
        axes.to_edge(LEFT, buff=LARGE_BUFF)
        axes.add_coordinates()
        axes.y_axis.add_numbers([0])
        axes.x_axis.add(
            Text("Time").next_to(
                axes.x_axis.get_end(), DR,
            )
        )
        axes.y_axis.add(
            MathTex("f").next_to(
                axes.y_axis.get_corner(UR), RIGHT,
            ).set_color(YELLOW)
        )
        axes.x_axis.set_opacity(0)

        # Value trackers
        y_tracker = ValueTracker(3)
        x_tracker = ValueTracker(0)
        dydt_tracker = ValueTracker()
        dxdt_tracker = ValueTracker(0)
        self.add(
            y_tracker, x_tracker,
            dydt_tracker, dxdt_tracker,
        )

        get_y = y_tracker.get_value
        get_x = x_tracker.get_value
        get_dydt = dydt_tracker.get_value
        get_dxdt = dxdt_tracker.get_value

        dydt_tracker.add_updater(lambda m: m.set_value(
            - k * get_y()
        ))
        y_tracker.add_updater(lambda m, dt: m.increment_value(
            dt * get_dydt()
        ))
        x_tracker.add_updater(lambda m, dt: m.increment_value(
            dt * get_dxdt()
        ))

        # Tip/decimal
        tip = ArrowTip(color=YELLOW)
        tip.set_width(0.25)
        tip.add_updater(lambda m: m.move_to(
            axes.c2p(get_x(), get_y()), LEFT
        ))
        decimal = DecimalNumber()
        decimal.add_updater(lambda d: d.set_value(get_y()))
        decimal.add_updater(lambda d: d.next_to(
            tip, RIGHT,
            SMALL_BUFF,
        ))

        # Rate of change arrow
        arrow = Arrow(
            start=UP, end=DOWN, color=RED,
            max_stroke_width_to_length_ratio=50,
            max_tip_length_to_length_ratio=0.2,
            stroke_width=4,
        )
        arrow.add_updater(lambda m: m.scale(
            2.5 * abs(get_dydt()) / m.get_length()
        ))
        arrow.add_updater(lambda m: m.move_to(
            tip.get_left(), UP
        ))

        # Graph
        graph = TracedPath(tip.get_left)

        # Equation
        ode = MathTex(
            "{d{f} \\over dt}(t)",
            "=", mk_tex, "\\cdot {f}(t)",
            tex_to_color_map={
                "{f}": YELLOW,
                "=": WHITE,
                mk_tex: mk_tex_color
            }
        )
        ode.to_edge(UP)
        dfdt = ode[:3]
        ft = ode[-2:]

        self.add(axes)
        self.add(tip)
        self.add(decimal)
        self.add(arrow)
        self.add(randy)
        self.add(ode)

        # Show rate of change dependent on itself
        rect = SurroundingRectangle(dfdt)
        self.play(Create(rect))
        self.wait()
        self.play(
            Transform(
                rect,
                SurroundingRectangle(ft)
            )
        )
        self.wait(3)

        # Show graph over time
        self.play(
            DrawBorderThenFill(bubble),
            Write(exp),
            FadeOut(rect),
            randy.animate.change("thinking"),
        )
        axes.x_axis.set_opacity(1)
        self.play(
            y_tracker.animate.set_value(3),
            Create(axes.x_axis),
        )
        dxdt_tracker.set_value(1)
        self.add(graph)
        randy.add_updater(lambda r: r.look_at(tip))
        self.wait(4)

        # Show derivative of exponential
        eq = MathTex("=")
        eq.next_to(ode.get_part_by_tex("="), DOWN, LARGE_BUFF)
        exp.generate_target()
        exp.target.next_to(eq, LEFT)
        d_dt = MathTex("{d \\over dt}")
        d_dt.next_to(exp.target, LEFT)
        const = MathTex(mk_tex)
        const.set_color(mk_tex_color)
        dot = MathTex("\\cdot")
        const.next_to(eq, RIGHT)
        dot.next_to(const, RIGHT, 2 * SMALL_BUFF)
        exp_copy = exp.copy()
        exp_copy.next_to(dot, RIGHT, 2 * SMALL_BUFF)
        VGroup(const, dot, eq).align_to(exp_copy, DOWN)

        self.play(
            MoveToTarget(exp),
            FadeOut(bubble),
            FadeIn(d_dt),
            FadeIn(eq),
        )
        self.wait(2)
        self.play(
            Transform(
                exp[1].copy(),
                const[0],
            )
        )
        self.wait()
        rect = SurroundingRectangle(exp)
        rect.set_stroke(BLUE, 2)
        self.play(FadeIn(rect))
        self.play(
            Write(dot),
            TransformFromCopy(exp, exp_copy),
            rect.animate.move_to(exp_copy)
        )
        self.play(FadeOut(rect))
        self.wait(5)
