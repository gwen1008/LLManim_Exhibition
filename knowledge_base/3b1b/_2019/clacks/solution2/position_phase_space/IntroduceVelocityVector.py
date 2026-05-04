# Source: 3b1b/_2019/clacks/solution2/position_phase_space.py
# Description: [3b1b translated] 展示相空間中的速度向量如何對應到物理空間中兩個方塊的速度，並分解為分量、計算大小，最後與動能關聯。



from manim import *
class IntroduceVelocityVector(PositionPhaseSpaceScene, MovingCameraScene):
    def __init__(
        self,
        zoom=True,
        ps_x_line_config={
            "color": WHITE,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        },
        ps_y_line_config={
            "color": WHITE,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        },
        axes_center=6 * LEFT + 0.65 * DOWN,
        slide_time=20,
        new_vect_config={
            "tip_length": 0.1,
            "rectangular_stem_width": 0.02,
        },
        **kwargs
    ):
        super().__init__(**kwargs)
        self.zoom = zoom
        self.ps_x_line_config = ps_x_line_config
        self.ps_y_line_config = ps_y_line_config
        self.axes_center = axes_center
        self.slide_time = slide_time
        self.new_vect_config = new_vect_config

    def setup(self):
        MovingCameraScene.setup(self)
        PositionPhaseSpaceScene.setup(self)
        self.add(
            self.floor,
            self.wall,
            self.blocks,
            self.axes,
            self.d1_eq_d2_line,
            self.d1_eq_d2_label,
            self.d2_eq_w2_line,
            self.x_line,
            self.y_line,
            self.ps_dot,
        )

    def construct(self):
        self.show_velocity_vector()
        self.contrast_with_physical_velocities()
        self.zoom_in_on_vector()
        self.break_down_components()
        self.zoom_out()
        self.relate_x_dot_y_dot_to_v1_v2()
        self.calculate_magnitude()
        self.let_process_play_out()

    def show_velocity_vector(self):
        self.slide(2)
        ps_vect = self.get_ps_velocity_vector(self.trajectory)
        self.play(GrowArrow(ps_vect))
        self.play(CreateThenFadeAround(ps_vect))
        self.wait()

    def contrast_with_physical_velocities(self):
        ps_vect = self.ps_velocity_vector
        block_vectors = self.get_block_velocity_vectors(ps_vect)

        self.play(LaggedStartMap(GrowArrow, block_vectors))
        self.play(Rotating(
            ps_vect,
            angle=TAU,
            about_point=ps_vect.get_start(),
            run_time=5,
            rate_func=smooth,
        ))
        self.wait()
        self.slide_until(lambda: self.get_d2() < 2.5)

    def zoom_in_on_vector(self):
        if not self.zoom:
            self.wait(3)
            return
        ps_vect = self.ps_velocity_vector
        new_vect = Arrow(
            ps_vect.get_start(),
            ps_vect.get_end(),
            buff=0,
            **self.new_vect_config
        )
        new_vect.match_style(ps_vect)

        camera_frame = self.camera_frame
        camera_frame.save_state()
        point = self.ps_point.get_location()
        point += MED_SMALL_BUFF * DOWN
        self.play(
            camera_frame.animate.scale(0.25).move_to(point),
            Transform(ps_vect, new_vect),
            run_time=2,
        )
        self.wait()

    def break_down_components(self):
        # Create vectors
        ps_vect = self.ps_velocity_vector
        start = ps_vect.get_start()
        end = ps_vect.get_end()
        ul_corner = np.array(start)
        dr_corner = np.array(start)
        ul_corner[0] = end[0]
        dr_corner[1] = end[1]

        x_vect = Arrow(
            start, ul_corner,
            buff=0,
            **self.new_vect_config
        )
        y_vect = Arrow(
            start, dr_corner,
            buff=0,
            **self.new_vect_config
        )
        x_vect.set_fill(GREEN, opacity=0.75)
        y_vect.set_fill(RED, opacity=0.75)
        vects = VGroup(x_vect, y_vect)

        # Projection lines
        x_line, y_line = [
            DashedLine(
                ps_vect.get_end(),
                vect.get_end(),
                dash_length=0.01,
                color=vect.get_color(),
            )
            for vect in (x_vect, y_vect)
        ]
        self.projection_lines = VGroup(x_line, y_line)

        # Vector labels
        dx_label = MathTex("\\frac{dx}{dt}")
        dy_label = MathTex("\\frac{dy}{dt}")
        labels = VGroup(dx_label, dy_label)
        for label, arrow, direction in zip(labels, vects, [UP, RIGHT]):
            label.scale(0.25)
            buff = 0.25 * SMALL_BUFF
            label.next_to(arrow, direction, buff=buff)
        label.set_stroke(BLACK, 3, background=True)

        if not self.zoom:
            self.grow_labels(labels)

        self.play(
            TransformFromCopy(ps_vect, x_vect),
            Create(x_line),
        )
        self.play(FadeIn(dx_label, shift=0.25 * DOWN))
        self.wait()
        self.play(
            TransformFromCopy(ps_vect, y_vect),
            Create(y_line),
        )
        self.play(FadeIn(dy_label, shift=0.25 * LEFT))
        self.wait()

        # Ask about dx_dt
        randy = Randolph()
        randy.match_height(dx_label)
        randy.next_to(dx_label, LEFT, SMALL_BUFF)
        randy.change("confused", dx_label)
        randy.save_state()
        randy.set_opacity(0)
        randy.change("plain")

        self.play(Restore(randy))
        self.play(WiggleOutThenIn(dx_label))
        self.play(Blink(randy))
        self.play(FadeOut(randy))

        self.derivative_labels = labels
        self.component_vectors = vects

    def zoom_out(self):
        if not self.zoom:
            self.wait(2)
            return
        labels = self.derivative_labels
        self.play(
            Restore(self.camera_frame),
            ApplyFunction(self.grow_labels, labels),
            run_time=2
        )

    def relate_x_dot_y_dot_to_v1_v2(self):
        derivative_labels = self.derivative_labels.copy()
        dx_label, dy_label = derivative_labels
        x_label, y_label = self.axes.labels
        m_part = x_label[2]
        block1 = self.block1
        block_vectors = self.block_velocity_vectors

        x_eq = x_label[1]
        dx_eq = MathTex("=")
        dx_eq.next_to(
            x_eq, DOWN,
            buff=LARGE_BUFF,
            aligned_edge=RIGHT,
        )
        for label in derivative_labels:
            label.generate_target()
            label.target.scale(1.5)
        dx_label.target.next_to(dx_eq, LEFT)
        dx_rhs = MathTex("\\sqrt{m_1}", "v_1")
        dx_rhs[0][2:].set_color(BLUE)
        dx_rhs[1].set_color(GREEN)
        dx_rhs.next_to(dx_eq, RIGHT)
        alt_v1 = dx_rhs[1].copy()

        self.play(CreateThenFadeAround(x_label))
        self.play(MoveToTarget(dx_label))
        self.play(TransformFromCopy(x_eq, dx_eq))
        self.wait()
        self.play(
            VGroup(block1, m_part).animate.shift(SMALL_BUFF * UP),
            rate_func=wiggle,
        )
        self.wait()
        self.d1_brace.update()
        self.d1_label.update()
        self.play(
            CreateThenFadeAround(x_label[3]),
            FadeIn(self.d1_brace),
            FadeIn(self.d1_label),
        )
        self.wait()
        self.play(
            TransformFromCopy(x_label[3], dx_rhs[1]),
            TransformFromCopy(x_label[2], VGroup(dx_rhs[0])),
        )
        block_vectors.suspend_updating()
        self.play(alt_v1.animate.next_to(block_vectors[0], UP, SMALL_BUFF))
        self.play(
            Rotate(
                block_vectors[0], 10 * DEGREES,
                about_point=block_vectors[0].get_start(),
                rate_func=wiggle,
                run_time=1,
            )
        )
        self.play(FadeOut(alt_v1))
        block_vectors.resume_updating()
        self.wait()

        # dy_label
        y_eq = y_label[1]
        dy_eq = MathTex("=")
        dy_eq.next_to(y_eq, DOWN, LARGE_BUFF)
        dy_label.target.next_to(dy_eq, LEFT)
        dy_rhs = MathTex("\\sqrt{m_2}", "v_2")
        dy_rhs[0][2:].set_color(BLUE)
        dy_rhs[1].set_color(RED)
        dy_rhs.next_to(dy_eq, RIGHT)
        VGroup(dy_label.target, dy_eq, dy_rhs).align_to(y_label, LEFT)
        alt_v2 = dy_rhs[1].copy()
        self.play(MoveToTarget(dy_label))
        self.play(
            Write(dy_eq),
            Write(dy_rhs),
        )
        self.play(alt_v2.animate.next_to(block_vectors[1], UP, SMALL_BUFF))
        self.wait()
        self.play(FadeOut(alt_v2))
        self.wait()

        self.derivative_equations = VGroup(
            VGroup(dx_label, dx_eq, dx_rhs),
            VGroup(dy_label, dy_eq, dy_rhs),
        )

    def calculate_magnitude(self):
        corner_rect = Rectangle(
            stroke_color=WHITE,
            stroke_width=1,
            fill_color=BLACK,
            fill_opacity=1,
            height=2.5,
            width=8.5,
        )
        corner_rect.to_corner(UR, buff=0)

        ps_vect = self.ps_velocity_vector
        big_ps_vect = Arrow(
            ps_vect.get_start(), ps_vect.get_end(),
            buff=0,
        )
        big_ps_vect.match_style(ps_vect)
        big_ps_vect.scale(1.5)
        magnitude_bars = MathTex("||", "||")
        magnitude_bars.match_height(
            big_ps_vect, stretch=True
        )
        rhs_scale_val = 0.8
        rhs = MathTex(
            "=\\sqrt{"
            "\\left( dx/dt \\right)^2 + "
            "\\left( dy/dt \\right)^2"
            "}"
        )
        rhs.scale(rhs_scale_val)
        group = VGroup(
            magnitude_bars[0], big_ps_vect,
            magnitude_bars[1], rhs
        )
        group.arrange(RIGHT)
        group.next_to(corner_rect.get_corner(UL), DR)

        new_rhs = MathTex(
            "=", "\\sqrt", "{m_1(v_1)^2 + m_2(v_2)^2}",
            tex_to_color_map={
                "m_1": BLUE,
                "m_2": BLUE,
                "v_1": GREEN,
                "v_2": RED,
            }
        )
        new_rhs.scale(rhs_scale_val)
        new_rhs.next_to(rhs, DOWN, aligned_edge=LEFT)

        final_rhs = MathTex(
            "=", "\\sqrt{2(\\text{Kinetic energy})}"
        )
        final_rhs.scale(rhs_scale_val)
        final_rhs.next_to(new_rhs, DOWN, aligned_edge=LEFT)

        self.play(
            FadeIn(corner_rect),
            TransformFromCopy(ps_vect, big_ps_vect)
        )
        self.play(Write(magnitude_bars), Write(rhs[0]))
        self.wait()
        self.play(Write(rhs[1:]))
        self.wait()
        self.play(FadeIn(new_rhs, shift=UP))
        for equation in self.derivative_equations:
            self.play(CreateThenFadeAround(equation))
        self.wait()
        self.play(FadeIn(final_rhs, shift=UP))
        self.wait()

    def let_process_play_out(self):
        self.play(*map(FadeOut, [
            self.projection_lines,
            self.derivative_labels,
            self.component_vectors,
            self.d1_brace,
            self.d1_label,
        ]))
        self.add(self.blocks, self.derivative_equations)
        self.blocks.resume_updating()
        self.slide(self.slide_time)

    #
    def grow_labels(self, labels):
        for label, vect in zip(labels, [DOWN, LEFT]):
            p = label.get_edge_center(vect)
            p += SMALL_BUFF * vect
            label.scale(2.5, about_point=p)
        return labels
