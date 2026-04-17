# Source: 3b1b/_2019/clacks/solution2/wordy_scenes.py
# Description: [3b1b translated] 展示力學（動量與能量守恆）與光學（光速恆定與反射定律）之間的對應關係，並用箭頭和虛線框將兩組概念視覺化連接。



from manim import *
class ConnectionToOptics(Scene):
    def construct(self):
        e_group, m_group = k_groups = self.get_kinematics_groups()
        c_group, a_group = o_groups = self.get_optics_groups()
        arrows = VGroup()
        for g1, g2 in zip(k_groups, o_groups):
            g2.align_to(g1, UP)
            g2.to_edge(RIGHT)
            arrow = MathTex("\\Rightarrow")
            arrow.scale(1.5)
            arrow.move_to(interpolate(
                g1[0].get_right(), g2[0].get_left(), 0.5
            ))
            arrows.add(arrow)
        everything = VGroup(k_groups, arrows, o_groups)
        everything.to_edge(UP)

        everything.generate_target()
        everything.target.scale(0.9)
        everything.target.to_edge(DOWN)
        width = max([m.get_width() for m in everything.target])
        width += 2 * 0.5  # MED_SMALL_BUFF 近似值
        rects = VGroup()
        for k in [0, 2]:
            rect = DashedVMobject(Rectangle(
                height=config.frame_height - 1.5,
                width=width
            ), num_dashes=100)
            rect.move_to(everything.target[k])
            rect.to_edge(DOWN, buff=0.2)  # SMALL_BUFF 近似值
            rects.add(rect)
        titles = VGroup(
            Tex("Kinematics"),
            Tex("Optics"),
        )
        titles.scale(1.5)
        for title, rect in zip(titles, rects):
            title.next_to(rect, UP)
        titles[0].align_to(titles[1], UP)

        self.play(FadeIn(e_group, shift=DOWN))
        self.play(
            Write(arrows[0]),
            FadeIn(c_group, shift=LEFT)
        )
        self.wait()
        self.play(FadeIn(m_group, shift=DOWN))
        self.play(
            Write(arrows[1]),
            FadeIn(a_group, shift=LEFT)
        )
        self.wait(4)
        for k in range(2):
            anims = [
                Create(rects[k]),
                FadeIn(titles[k], shift=DOWN),
            ]
            if k == 0:
                anims.append(MoveToTarget(everything))
            self.play(*anims)
            self.wait()
        self.wait()
        self.wait(4)

    def get_kinematics_groups(self):
        tex_to_color_map = {
            "m_1": BLUE,
            "m_2": BLUE,
            "v_1": RED,
            "v_2": RED,
        }
        energy_eq = MathTex(
            "\\frac{1}{2} m_1 (v_1)^2 + "
            "\\frac{1}{2} m_2 (v_2)^2 = "
            "\\text{const.}",
            tex_to_color_map=tex_to_color_map
        )
        energy_eq.scale(0.8)
        momentum_eq = MathTex(
            "m_1 v_1 + m_2 v_2 = \\text{const.}",
            tex_to_color_map=tex_to_color_map
        )
        energy_label = Tex(
            "Conservation of energy"
        )
        momentum_label = Tex(
            "Conservation of momentum"
        )
        energy_group = VGroup(energy_label, energy_eq)
        momentum_group = VGroup(momentum_label, momentum_eq)
        groups = VGroup(energy_group, momentum_group)
        for group in groups:
            group.arrange(DOWN, buff=0.7)  # MED_LARGE_BUFF 近似值
            group[0].set_color(GREEN)
        groups.arrange(DOWN, buff=2)
        groups.to_edge(LEFT)
        return groups

    def get_optics_groups(self):
        self.time_tracker = ValueTracker(0)
        self.time_tracker.add_updater(
            lambda m, dt: m.increment_value(dt)
        )
        self.add(self.time_tracker)
        return VGroup(
            self.get_speed_group(),
            self.get_angle_group()
        )

    def get_speed_group(self):
        speed_label = Tex("Constant speed of light")
        speed_label.set_color(YELLOW)
        speed_light_template = Line(LEFT, RIGHT)
        speed_light_template.set_opacity(0)  # 替代 .fade(1)
        speed_light_template.match_width(speed_label)
        speed_light_template.next_to(speed_label, DOWN, buff=0.7)  # MED_LARGE_BUFF 近似值
        speed_light = speed_light_template.copy()

        def update_speed_light(light, period=2, time_width=0.05):
            time = self.time_tracker.get_value()
            alpha = (time / period) % 1
            alpha *= 1.5
            a = alpha - time_width / 2
            b = alpha + time_width / 2
            # 使用 interpolate 模擬 pointwise_become_partial
            if a < 0:
                a = 0
            if b > 1:
                b = 1
            if a < b:
                start = speed_light_template.point_from_proportion(a)
                end = speed_light_template.point_from_proportion(b)
                light.set_points_as_corners([start, end])
            else:
                light.set_points_as_corners([ORIGIN, ORIGIN])
            opacity = speed_label[0].get_fill_opacity()  # 近似 family_members_with_points
            light.set_stroke(YELLOW, width=3, opacity=opacity)

        speed_light.add_updater(update_speed_light)
        result = VGroup(
            speed_label, speed_light_template, speed_light
        )
        return result

    def get_angle_group(self):
        title = VGroup(
            Tex("Angle of\\\\Incidence"),
            Tex("="),
            Tex("Angle of\\\\Reflection"),
        ).arrange(RIGHT)
        title.set_color(YELLOW)
        h_line = Line(LEFT, RIGHT)
        h_line.match_width(title)
        h_line.set_stroke(GREY_B, width=2)
        h_line.set_sheen(1, UL)
        points = [
            h_line.get_left() + UP,
            h_line.get_center(),
            h_line.get_right() + UP,
        ]
        dashed_lines = VGroup(
            DashedLine(*points[0:2]), DashedLine(*points[1:3])
        )
        dashed_lines.set_stroke(WHITE, 2)
        v_shape = VMobject()
        v_shape.set_points_as_corners(points)
        v_shape.set_opacity(0)  # 替代 .fade(1)

        theta = dashed_lines[1].get_angle()
        arcs = VGroup(
            Arc(start_angle=0, angle=theta, radius=0.5),
            Arc(start_angle=PI, angle=-theta, radius=0.5),
        )
        arcs.set_stroke(WHITE, 2)
        thetas = VGroup()
        for v in LEFT, RIGHT:
            theta_symbol = MathTex("\\theta")
            theta_symbol.next_to(arcs, v, aligned_edge=DOWN)
            theta_symbol.shift(0.2 * UP)  # SMALL_BUFF 近似值
            thetas.add(theta_symbol)

        beam = VMobject()

        def update_beam(beam, period=2, time_width=0.05):
            time = self.time_tracker.get_value()
            alpha = (time / period) % 1
            alpha *= 1.5
            a = alpha - time_width / 2
            b = alpha + time_width / 2
            # 使用 interpolate 模擬 pointwise_become_partial
            if a < 0:
                a = 0
            if b > 1:
                b = 1
            if a < b:
                start = v_shape.point_from_proportion(a)
                end = v_shape.point_from_proportion(b)
                beam.set_points_as_corners([start, end])
            else:
                beam.set_points_as_corners([ORIGIN, ORIGIN])
            opacity = title[0].get_fill_opacity()  # 近似 family_members_with_points
            beam.set_stroke(YELLOW, width=3, opacity=opacity)

        beam.add_updater(update_beam)
        title.next_to(v_shape, UP, buff=0.7)  # MED_LARGE_BUFF 近似值

        return VGroup(
            title, h_line, arcs, thetas,
            dashed_lines, v_shape, beam
        )
