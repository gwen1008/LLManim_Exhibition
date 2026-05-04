# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示一個湖邊燈塔的光照模型如何逐步擴展成數軸上的奇數平方倒數和，最終導出 π²/8 的結果。


from manim import *
import numpy as np

class PondScene(ThreeDScene):
    def construct(self):
        BASELINE_YPOS = -2.5
        OBSERVER_POINT = np.array([0, BASELINE_YPOS, 0])
        LAKE0_RADIUS = 1.5
        INDICATOR_RADIUS = 0.6
        TICK_SIZE = 0.5
        LIGHTHOUSE_HEIGHT = 0.5
        LAKE_COLOR = BLUE
        LAKE_OPACITY = 0.15
        LAKE_STROKE_WIDTH = 5.0
        LAKE_STROKE_COLOR = BLUE
        TEX_SCALE = 0.8
        DOT_COLOR = BLUE

        LIGHT_MAX_INT = 1
        LIGHT_SCALE = 2.5
        LIGHT_CUTOFF = 1

        RIGHT_ANGLE_SIZE = 0.3

        self.cumulated_zoom_factor = 1

        def right_angle(pointA, pointB, pointC, size=1):
            v1 = pointA - pointB
            v1 = size * v1 / np.linalg.norm(v1)
            v2 = pointC - pointB
            v2 = size * v2 / np.linalg.norm(v2)
            
            P = pointB
            Q = pointB + v1
            R = Q + v2
            S = R - v1
            angle_sign = VMobject()
            angle_sign.set_points_as_corners([P, Q, R, S, P])
            angle_sign.set_fill(color=WHITE, opacity=1)
            angle_sign.set_stroke(width=0)
            return angle_sign

        def triangle(pointA, pointB, pointC):
            mob = VMobject()
            mob.set_points_as_corners([pointA, pointB, pointC, pointA])
            mob.set_fill(color=WHITE, opacity=0.5)
            mob.set_stroke(width=0)
            return mob

        def zoom_out_scene(factor):
            self.remove(self.ls0_dot)

            phi0 = self.camera.phi  # default is 0 degs
            theta0 = self.camera.theta  # default is -90 degs
            distance0 = self.camera.distance

            distance1 = 2 * distance0
            camera_target_point = self.camera.get_spherical_coords(phi0, theta0, distance1)

            self.play(
                self.camera.rotation_mobject.animate.move_to(camera_target_point),
                self.zoomable_mobs.animate.shift(self.obs_dot.get_center()),
                self.unzoomable_mobs.animate.scale(2, about_point=ORIGIN),
            )

            self.cumulated_zoom_factor *= factor
            self.ls0_dot.scale(2, about_point=ORIGIN)

        def shift_scene(v):
            self.play(
                self.zoomable_mobs.animate.shift(v),
                self.unzoomable_mobs.animate.shift(v)
            )

        self.zoomable_mobs = VMobject()
        self.unzoomable_mobs = VMobject()

        baseline = VMobject()
        baseline.set_points_as_corners([[-8, BASELINE_YPOS, 0], [8, BASELINE_YPOS, 0]])
        baseline.set_stroke(width=0)
        self.zoomable_mobs.add(baseline)

        obs_dot = self.obs_dot = Dot(OBSERVER_POINT, color=DOT_COLOR)
        ls0_dot = self.ls0_dot = Dot(OBSERVER_POINT + 2 * LAKE0_RADIUS * UP, color=WHITE)
        self.unzoomable_mobs.add(self.obs_dot)

        # lake
        lake0 = Circle(
            radius=LAKE0_RADIUS,
            stroke_width=0,
            fill_color=LAKE_COLOR,
            fill_opacity=LAKE_OPACITY
        )
        lake0.move_to(OBSERVER_POINT + LAKE0_RADIUS * UP)
        self.zoomable_mobs.add(lake0)

        # Morty and indicator
        morty = Mortimer().flip().scale(0.3)
        morty.next_to(OBSERVER_POINT, DOWN)
        # LightIndicator 在 ManimCE 中不存在，用替代方案
        indicator = Circle(radius=INDICATOR_RADIUS, color=YELLOW)
        indicator.next_to(morty, LEFT)
        self.unzoomable_mobs.add(morty, indicator)

        # first lighthouse
        # inverse_quadratic 和 LightSource 在 ManimCE 中不存在，用簡單替代
        original_op_func = lambda x: 1 / (1 + x**2)  # 簡單替代函數
        # 用 Dot 代替 LightSource
        ls0 = Dot(color=YELLOW, radius=0.2)
        lighthouse = Rectangle(height=LIGHTHOUSE_HEIGHT, width=0.3, color=WHITE)
        lighthouse.move_to(OBSERVER_POINT + LAKE0_RADIUS * 2 * UP)
        ls0.move_to(OBSERVER_POINT + LAKE0_RADIUS * 2 * UP)
        ambient_light = Circle(radius=1.5, color=YELLOW, fill_opacity=0.2, stroke_width=0)
        ambient_light.move_to(OBSERVER_POINT + LAKE0_RADIUS * 2 * UP)
        
        self.zoomable_mobs.add(ls0, lighthouse, ambient_light)

        # shore arcs
        arc_left = Arc(
            angle=-TAU/2,
            radius=LAKE0_RADIUS,
            start_angle=-TAU/4,
            stroke_width=LAKE_STROKE_WIDTH,
            color=LAKE_STROKE_COLOR
        )
        arc_left.move_arc_center_to(OBSERVER_POINT + LAKE0_RADIUS * UP)

        one_left = MathTex("1", color=LAKE_COLOR).scale(TEX_SCALE)
        one_left.next_to(arc_left, LEFT)
    
        arc_right = Arc(
            angle=TAU/2,
            radius=LAKE0_RADIUS,
            start_angle=-TAU/4,
            stroke_width=LAKE_STROKE_WIDTH,
            color=LAKE_STROKE_COLOR
        )
        arc_right.move_arc_center_to(OBSERVER_POINT + LAKE0_RADIUS * UP)

        one_right = MathTex("1", color=LAKE_COLOR).scale(TEX_SCALE)
        one_right.next_to(arc_right, RIGHT)

        # New introduction
        lake0.save_state()
        morty.save_state()
        lake0.set_height(6)
        morty.to_corner(UP+LEFT)
        morty.set_opacity(0)
        lake0.center()

        lake_word = Text("Lake")
        lake_word.scale(2)
        lake_word.move_to(lake0)

        self.play(
            Create(lake0, stroke_width=1),
            Write(lake_word)
        )
        self.play(
            Restore(lake0),
            lake_word.animate.scale(0.5, about_point=lake0.get_bottom()),
            lake_word.animate.set_opacity(0)
        )
        self.remove(lake_word)
        self.play(Restore(morty))
        self.play(
            GrowFromCenter(obs_dot),
            GrowFromCenter(ls0_dot),
            FadeIn(lighthouse)
        )
        self.add(lighthouse, obs_dot, ls0_dot)
        self.play(
            FadeIn(ambient_light),
            Animation(lighthouse),
        )
        self.wait()
        self.play(
            morty.animate.move_to(lighthouse),
            run_time=3,
            path_arc=TAU/2,
            rate_func=there_and_back
        )

        self.play(
            Create(arc_right),
            Write(one_right),
        )
        self.play(
            Create(arc_left),
            Write(one_left),
        )
        self.play(
            lake0.animate.set_stroke(color=LAKE_STROKE_COLOR, width=LAKE_STROKE_WIDTH),
        )
        self.wait()
        self.add(morty)

        # Show indicator
        self.play(FadeIn(indicator))
        # 簡單替代 indicator.set_intensity
        self.play(indicator.animate.set_fill(opacity=0.5))

        diameter_start = interpolate(OBSERVER_POINT, ls0.get_center(), 0.02)
        diameter_stop = interpolate(OBSERVER_POINT, ls0.get_center(), 0.98)

        # diameter
        diameter = DoubleArrow(
            diameter_start,
            diameter_stop,
            buff=0,
            color=WHITE,
        )
        diameter_text = MathTex("d").scale(TEX_SCALE)
        diameter_text.next_to(diameter, RIGHT)

        self.play(
            GrowFromCenter(diameter),
            Write(diameter_text),
            FadeOut(ls0_dot)
        )
        self.wait()

        indicator_reading = MathTex("{1 \\over d^2}").scale(TEX_SCALE)
        indicator_reading.move_to(indicator)
        self.unzoomable_mobs.add(indicator_reading)

        self.play(
            ReplacementTransform(
                diameter_text[0].copy(),
                indicator_reading[2],
            ),
            FadeIn(indicator_reading)
        )
        self.wait()

        # replace d with its value
        new_diameter_text = MathTex("{2 \\over \\pi}").scale(TEX_SCALE)
        new_diameter_text.set_color(LAKE_COLOR)
        new_diameter_text.move_to(diameter_text)
        self.play(FadeOut(diameter_text))
        self.play(FadeIn(new_diameter_text))
        self.wait(2)

        # insert into indicator reading
        new_reading = MathTex("{\\pi^2 \\over 4}").scale(TEX_SCALE)
        new_reading.move_to(indicator)
        new_diameter_text_copy = new_diameter_text.copy()
        new_diameter_text_copy.submobjects.reverse()

        self.play(
            FadeOut(indicator_reading),
            ReplacementTransform(
                new_diameter_text_copy,
                new_reading,
                path_arc=30*DEGREES
            )
        )
        indicator_reading = new_reading

        self.wait(2)

        self.play(
            FadeOut(one_left),
            FadeOut(one_right),
            FadeOut(new_diameter_text),
            FadeOut(arc_left),
            FadeOut(arc_right)
        )
        self.add(indicator, indicator_reading)
        self.unzoomable_mobs.add(indicator_reading)

        def indicator_wiggle():
            INDICATOR_WIGGLE_FACTOR = 1.3
            self.play(
                indicator.animate.scale(INDICATOR_WIGGLE_FACTOR, about_point=indicator.get_center()).set_rate_func(wiggle),
                indicator_reading.animate.scale(INDICATOR_WIGGLE_FACTOR, about_point=indicator_reading.get_center()).set_rate_func(wiggle)
            )

        def angle_for_index(i, step):
            return -TAU/4 + TAU/2**step * (i + 0.5)

        def position_for_index(i, step, scaled_down=False):
            theta = angle_for_index(i, step)
            radial_vector = np.array([np.cos(theta), np.sin(theta), 0])
            position = self.lake_center + self.lake_radius * radial_vector

            if scaled_down:
                return position * 0.5 + self.obs_dot.get_center() * 0.5
            else:
                return position

        def split_light_source(i, step, show_steps=True, animate=True, run_time=1):
            ls_new_loc1 = position_for_index(i, step + 1)
            ls_new_loc2 = position_for_index(i + 2**step, step + 1)

            hyp = VMobject()
            hyp1 = Line(self.lake_center, ls_new_loc1)
            hyp2 = Line(self.lake_center, ls_new_loc2)
            hyp.add(hyp2, hyp1)
            self.new_hypotenuses.append(hyp)

            if show_steps:
                self.play(Create(hyp, run_time=run_time))

            leg1 = Line(self.obs_dot.get_center(), ls_new_loc1)
            leg2 = Line(self.obs_dot.get_center(), ls_new_loc2)
            self.new_legs_1.append(leg1)
            self.new_legs_2.append(leg2)

            if show_steps:
                self.play(
                    Create(leg1, run_time=run_time),
                    Create(leg2, run_time=run_time),
                )

            ls1 = self.light_sources_array[i]
            ls2 = ls1.copy()
            if animate:
                self.add(ls2)

            self.additional_light_sources.append(ls2)

            ls_old_loc = np.array(ls1.get_center())
            onscreen_old = np.any(np.abs(ls_old_loc) < 10)
            onscreen_1 = np.any(np.abs(ls_new_loc1) < 10)
            onscreen_2 = np.any(np.abs(ls_new_loc2) < 10)
            show_animation = (onscreen_old or onscreen_1 or onscreen_2)

            if show_animation or animate:
                ls1.generate_target()
                ls2.generate_target()
                ls1.target.move_to(ls_new_loc1)
                ls2.target.move_to(ls_new_loc2)
                ls1.set_opacity(0)
                self.play(
                    MoveToTarget(ls1), MoveToTarget(ls2),
                    run_time=run_time
                )
            else:
                ls1.move_to(ls_new_loc1)
                ls2.move_to(ls_new_loc1)

        def construction_step(n, show_steps=True, run_time=1, simultaneous_splitting=False):
            if show_steps:
                self.zoomable_mobs.remove(self.hypotenuses, self.altitudes, self.inner_lake)
                self.play(
                    FadeOut(self.hypotenuses),
                    FadeOut(self.altitudes),
                    FadeOut(self.inner_lake)
                )
            else:
                self.zoomable_mobs.remove(self.inner_lake)
                self.play(FadeOut(self.inner_lake))

            # create a new, outer lake
            self.lake_center = self.obs_dot.get_center() + self.lake_radius * UP

            new_outer_lake = Circle(
                radius=self.lake_radius,
                stroke_width=LAKE_STROKE_WIDTH,
                fill_color=LAKE_COLOR,
                fill_opacity=LAKE_OPACITY,
                stroke_color=LAKE_STROKE_COLOR
            )
            new_outer_lake.move_to(self.lake_center)

            if show_steps: 
                self.play(
                    FadeIn(new_outer_lake, run_time=run_time),
                    FadeIn(self.ls0_dot)
                )
            else:
                self.play(FadeIn(new_outer_lake, run_time=run_time))

            self.wait()

            self.inner_lake = self.outer_lake
            self.outer_lake = new_outer_lake
            self.altitudes = self.legs

            self.additional_light_sources = []
            self.new_legs_1 = []
            self.new_legs_2 = []
            self.new_hypotenuses = []

            if not simultaneous_splitting:
                for i in range(2**n):
                    split_light_source(i, step=n, show_steps=show_steps, run_time=run_time)

                    if n == 1 and i == 0:
                        A = self.light_sources[0].get_center()
                        B = self.additional_light_sources[0].get_center()
                        C = self.obs_dot.get_center()

                        triangle1 = triangle(A, C, B)
                        right_angle1 = right_angle(A, C, B, size=2 * RIGHT_ANGLE_SIZE)

                        self.play(FadeIn(triangle1), FadeIn(right_angle1))
                        self.wait()
                        self.play(FadeOut(triangle1), FadeOut(right_angle1))
                        self.wait()

                        H = self.inner_lake.get_center() + self.lake_radius/2 * RIGHT
                        L = self.outer_lake.get_center()
                        triangle2 = triangle(L, H, C)
                        right_angle2 = right_angle(L, H, C, size=2 * RIGHT_ANGLE_SIZE)

                        self.play(FadeIn(triangle2), FadeIn(right_angle2))
                        self.wait()
                        self.play(FadeOut(triangle2), FadeOut(right_angle2))
                        self.wait()
            else:
                old_lake = self.outer_lake.copy()
                old_ls = self.light_sources.copy()
                old_ls2 = old_ls.copy()
                for submob in old_ls2.submobjects:
                    old_ls.add(submob)

                self.remove(self.outer_lake, self.light_sources)
                self.add(old_lake, old_ls)

                for i in range(2**n):
                    split_light_source(i, step=n, show_steps=show_steps, run_time=run_time, animate=False)

                self.play(
                    ReplacementTransform(old_ls, self.light_sources, run_time=run_time),
                    ReplacementTransform(old_lake, self.outer_lake, run_time=run_time),
                )

            self.legs = VMobject()
            for leg in self.new_legs_1:
                self.legs.add(leg)
                self.zoomable_mobs.add(leg)
            for leg in self.new_legs_2:
                self.legs.add(leg)
                self.zoomable_mobs.add(leg)

            for hyp in self.hypotenuses.submobjects:
                self.zoomable_mobs.remove(hyp)

            self.hypotenuses = VMobject()
            for hyp in self.new_hypotenuses:
                self.hypotenuses.add(hyp)
                self.zoomable_mobs.add(hyp)

            for ls in self.additional_light_sources:
                self.light_sources.add(ls)
                self.light_sources_array.append(ls)
                self.zoomable_mobs.add(ls)

            self.add(self.light_sources, self.inner_lake, self.outer_lake)
            self.zoomable_mobs.add(self.light_sources, self.inner_lake, self.outer_lake)

            if show_steps:
                self.add(self.legs, self.hypotenuses, self.altitudes)
                self.zoomable_mobs.add(self.legs, self.hypotenuses, self.altitudes)

            self.wait()

            if show_steps:
                self.play(FadeOut(self.ls0_dot))

            self.lake_radius *= 2

        self.lake_center = ls0_loc = ls0.get_center()

        self.inner_lake = VMobject()
        self.outer_lake = lake0
        self.legs = VMobject()
        self.legs.add(Line(OBSERVER_POINT, self.lake_center))
        self.altitudes = VMobject()
        self.hypotenuses = VMobject()
        self.light_sources_array = [ls0]
        self.light_sources = VMobject()
        self.light_sources.add(ls0)

        self.lake_radius = 2 * LAKE0_RADIUS

        self.zoomable_mobs.add(self.inner_lake, self.outer_lake, self.altitudes, self.light_sources)

        self.add(
            self.inner_lake,
            self.outer_lake,
            self.legs,
            self.altitudes,
            self.hypotenuses
        )

        self.play(FadeOut(diameter))
        
        self.additional_light_sources = []
        self.new_legs_1 = []
        self.new_legs_2 = []
        self.new_hypotenuses = []

        construction_step(0)

        my_triangle = triangle(
            self.light_sources[0].get_center(),
            OBSERVER_POINT,
            self.light_sources[1].get_center()
        )

        angle_sign1 = right_angle(
            self.light_sources[0].get_center(),
            OBSERVER_POINT,
            self.light_sources[1].get_center(),
            size=RIGHT_ANGLE_SIZE
        )

        self.play(FadeIn(angle_sign1), FadeIn(my_triangle))

        angle_sign2 = right_angle(
            self.light_sources[1].get_center(),
            self.lake_center,
            OBSERVER_POINT,
            size=RIGHT_ANGLE_SIZE
        )

        self.play(FadeIn(angle_sign2))
        self.wait()

        self.play(
            FadeOut(angle_sign1),
            FadeOut(angle_sign2),
            FadeOut(my_triangle)
        )

        indicator_wiggle()
        self.remove(self.ls0_dot)
        zoom_out_scene(2)

        construction_step(1)
        indicator_wiggle()
        zoom_out_scene(2)

        construction_step(2)
        indicator_wiggle()
        self.play(FadeOut(self.ls0_dot))

        self.play(
            FadeOut(self.altitudes),
            FadeOut(self.hypotenuses),
            FadeOut(self.legs)
        )

        max_it = 6
        scale = 2**(max_it - 4)
        TEX_SCALE *= scale

        self.play(FadeOut(self.inner_lake))

        for n in range(3, max_it + 1):
            new_lake = self.outer_lake.copy().scale(2, about_point=self.obs_dot.get_center())
            for ls in self.light_sources_array:
                lsp = ls.copy()
                self.light_sources.add(lsp)
                self.add(lsp)
                self.light_sources_array.append(lsp)

            new_lake_center = new_lake.get_center()
            new_lake_radius = 0.5 * new_lake.width

            shift_list = (Transform(self.outer_lake, new_lake),)

            for i in range(2**n):
                theta = -TAU/4 + (i + 0.5) * TAU / 2**n
                v = np.array([np.cos(theta), np.sin(theta), 0])
                pos1 = new_lake_center + new_lake_radius * v
                pos2 = new_lake_center - new_lake_radius * v
                shift_list += (self.light_sources.submobjects[i].animate.move_to(pos1),)
                shift_list += (self.light_sources.submobjects[i+2**n].animate.move_to(pos2),)

            self.play(*shift_list)

        # Now create a straight number line and transform into it
        MAX_N = 17

        origin_point = self.obs_dot.get_center()

        self.number_line = NumberLine(
            x_range=[-MAX_N, MAX_N + 1, 1],
            color=WHITE,
            stroke_width=LAKE_STROKE_WIDTH,
            stroke_color=LAKE_STROKE_COLOR,
            numbers_with_elongated_ticks=list(range(-MAX_N, MAX_N + 1, 2)),
            length=LAKE0_RADIUS * TAU/4 / 2 * scale * (2*MAX_N + 1),
            include_numbers=True,
            numbers_to_include=list(range(-MAX_N, MAX_N + 1, 2)),
            label_direction=UP,
        ).shift(scale * 2.5 * DOWN)

        self.number_line_labels = self.number_line.get_number_mobjects()
        self.wait()

        origin_point = self.number_line.number_to_point(0)
        nl_sources = VMobject()
        pond_sources = VMobject()

        for i in range(-MAX_N, MAX_N+1):
            anchor = self.number_line.number_to_point(2*i + 1)
            ls = self.light_sources_array[i].copy()
            ls.move_to(anchor)
            nl_sources.add(ls)
            pond_sources.add(self.light_sources_array[i].copy())

        self.add(pond_sources)
        self.remove(self.light_sources)

        self.outer_lake.rotate(TAU/8)

        # open sea
        open_sea = Rectangle(
            width=20 * scale,
            height=10 * scale,
            stroke_width=LAKE_STROKE_WIDTH,
            stroke_color=LAKE_STROKE_COLOR,
            fill_color=LAKE_COLOR,
            fill_opacity=LAKE_OPACITY,
        ).flip().next_to(origin_point, UP, buff=0)

        self.play(
            ReplacementTransform(pond_sources, nl_sources),
            ReplacementTransform(self.outer_lake, open_sea),
            FadeOut(self.inner_lake)
        )
        self.play(FadeIn(self.number_line))
        self.wait()

        v = 4 * scale * UP
        self.play(
            nl_sources.animate.shift(v),
            morty.animate.shift(v),
            self.number_line.animate.shift(v),
            indicator.animate.shift(v),
            indicator_reading.animate.shift(v),
            open_sea.animate.shift(v),
            self.obs_dot.animate.shift(v),
        )
        self.number_line_labels.shift(v)

        origin_point = self.number_line.number_to_point(0)
        self.play(
            indicator.animate.move_to(origin_point + scale * UP),
            indicator_reading.animate.move_to(origin_point + scale * UP),
            FadeOut(open_sea),
            FadeOut(morty),
            FadeIn(self.number_line_labels)
        )

        two_sided_sum = MathTex(
            "\\dots", "+", "{1\\over (-11)^2}",
            "+", "{1\\over (-9)^2}", " + ", "{1\\over (-7)^2}", " + ", "{1\\over (-5)^2}", " + ",
            "{1\\over (-3)^2}", " + ", "{1\\over (-1)^2}", " + ", "{1\\over 1^2}", " + ",
            "{1\\over 3^2}", " + ", "{1\\over 5^2}", " + ", "{1\\over 7^2}", " + ",
            "{1\\over 9^2}", " + ", "{1\\over 11^2}", " + ", "\\dots"
        )

        nb_symbols = len(two_sided_sum)
        two_sided_sum.scale(TEX_SCALE)
        
        for i, submob in enumerate(two_sided_sum):
            submob.next_to(self.number_line.number_to_point(i - 13), DOWN, buff=2*scale)
            if i == 0 or i % 2 == 1 or i == nb_symbols - 1:
                submob.shift(0.3 * scale * DOWN)

        self.play(Write(two_sided_sum))

        covering_rectangle = Rectangle(
            width=config.frame_width * scale,
            height=config.frame_height * scale,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=1,
        )
        covering_rectangle.next_to(ORIGIN, LEFT, buff=0)

        half_indicator_reading = MathTex("{\\pi^2 \\over 8}").scale(TEX_SCALE)
        half_indicator_reading.move_to(indicator)

        central_plus_sign = two_sided_sum[13]

        self.play(
            FadeIn(covering_rectangle),
            Transform(indicator_reading, half_indicator_reading),
            FadeOut(central_plus_sign)
        )

        equals_sign = MathTex("=").scale(TEX_SCALE)
        equals_sign.move_to(central_plus_sign)
        p = 2 * scale * LEFT + central_plus_sign.get_center()[1] * UP

        self.play(
            indicator.animate.move_to(p),
            indicator_reading.animate.move_to(p),
            FadeIn(equals_sign),
        )

        # show Randy admiring the result
        randy = Randolph(color=MAROON_E).scale(scale).move_to(2*scale*DOWN+5*scale*LEFT)
        self.play(FadeIn(randy))
        # 簡單替代 randy.change
        self.play(randy.animate.set_color(GREEN))
        self.play(randy.animate.set_color(YELLOW))
