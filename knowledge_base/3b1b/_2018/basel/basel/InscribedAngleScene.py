# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示一個圓形湖泊中燈塔光源的幾何分割過程，並說明內接角與圓周角的關係。


from manim import *
import numpy as np

class InscribedAngleScene(ThreeDScene):
    def construct(self):
        BASELINE_YPOS = -2.5
        OBSERVER_POINT = np.array([0, BASELINE_YPOS, 0])
        LAKE0_RADIUS = 1.5
        INDICATOR_RADIUS = 0.6
        TICK_SIZE = 0.5
        LIGHTHOUSE_HEIGHT = 0.3
        LAKE_COLOR = BLUE
        LAKE_OPACITY = 0.15
        LAKE_STROKE_WIDTH = 5.0
        LAKE_STROKE_COLOR = BLUE
        TEX_SCALE = 0.8
        DOT_COLOR = BLUE

        LIGHT_MAX_INT = 1
        LIGHT_SCALE = 5
        LIGHT_CUTOFF = 1

        self.cumulated_zoom_factor = 1

        def zoom_out_scene(factor):
            phi0 = self.camera.get_phi()  # default is 0 degs
            theta0 = self.camera.get_theta()  # default is -90 degs
            distance0 = self.camera.get_distance()

            distance1 = 2 * distance0
            camera_target_point = self.camera.get_spherical_coords(phi0, theta0, distance1)

            self.play(
                self.camera.rotation_mobject.animate.move_to(camera_target_point),
                self.zoomable_mobs.animate.shift(self.obs_dot.get_center()),
                self.unzoomable_mobs.animate.scale(2, about_point=ORIGIN),
            )

            self.cumulated_zoom_factor *= factor

        def shift_scene(v):
            self.play(
                self.zoomable_mobs.animate.shift(v),
                self.unzoomable_mobs.animate.shift(v)
            )

        self.force_skipping()

        self.zoomable_mobs = VMobject()
        self.unzoomable_mobs = VMobject()

        baseline = VMobject()
        baseline.set_points_as_corners([[-8, BASELINE_YPOS, 0], [8, BASELINE_YPOS, 0]])
        baseline.set_stroke(width=0)  # in case it gets accidentally added to the scene
        self.zoomable_mobs.add(baseline)  # prob not necessary

        self.obs_dot = Dot(OBSERVER_POINT, color=DOT_COLOR)
        self.ls0_dot = Dot(OBSERVER_POINT + 2 * LAKE0_RADIUS * UP, color=WHITE)
        self.unzoomable_mobs.add(self.obs_dot)  # , self.ls0_dot)

        # lake
        lake0 = Circle(radius=LAKE0_RADIUS,
                       stroke_width=0,
                       fill_color=LAKE_COLOR,
                       fill_opacity=LAKE_OPACITY
                       )
        lake0.move_to(OBSERVER_POINT + LAKE0_RADIUS * UP)
        self.zoomable_mobs.add(lake0)

        # Morty and indicator
        morty = Mortimer().scale(0.3)
        morty.next_to(OBSERVER_POINT, DOWN)
        # Note: LightIndicator is not a standard ManimCE class
        # We'll create a simple replacement
        indicator = Circle(radius=INDICATOR_RADIUS, color=BLUE)
        indicator.next_to(morty, LEFT)
        self.unzoomable_mobs.add(morty, indicator)

        # first lighthouse
        # Note: LightSource, inverse_quadratic, AMBIENT_SCALE, NUM_LEVELS are not standard
        # We'll create a simple replacement
        original_op_func = lambda x: 1 / (x ** 2 + 1)  # simplified
        ls0 = Dot(color=YELLOW).scale(2)  # simplified light source
        ls0.move_to(OBSERVER_POINT + LAKE0_RADIUS * 2 * UP)
        lighthouse = Square(side_length=0.5, color=WHITE).move_to(ls0.get_center())
        ambient_light = Circle(radius=1, color=YELLOW, fill_opacity=0.2).move_to(ls0.get_center())
        
        self.zoomable_mobs.add(ls0, lighthouse, ambient_light)

        self.add(lake0, morty, self.obs_dot, self.ls0_dot, lighthouse)

        self.wait()

        # shore arcs
        arc_left = Arc(-TAU / 2,
                       radius=LAKE0_RADIUS,
                       start_angle=-TAU / 4,
                       stroke_width=LAKE_STROKE_WIDTH,
                       stroke_color=LAKE_STROKE_COLOR
                       )
        arc_left.move_arc_center_to(OBSERVER_POINT + LAKE0_RADIUS * UP)

        one_left = MathTex("1", color=LAKE_COLOR).scale(TEX_SCALE)
        one_left.next_to(arc_left, LEFT)

        arc_right = Arc(TAU / 2,
                        radius=LAKE0_RADIUS,
                        start_angle=-TAU / 4,
                        stroke_width=LAKE_STROKE_WIDTH,
                        stroke_color=LAKE_STROKE_COLOR
                        )
        arc_right.move_arc_center_to(OBSERVER_POINT + LAKE0_RADIUS * UP)

        one_right = MathTex("1", color=LAKE_COLOR).scale(TEX_SCALE)
        one_right.next_to(arc_right, RIGHT)

        self.play(
            Create(arc_left),
            Write(one_left),
            Create(arc_right),
            Write(one_right),
        )

        self.play(
            FadeIn(ambient_light),
            lake0.animate.set_stroke(color=LAKE_STROKE_COLOR, width=LAKE_STROKE_WIDTH),
        )

        self.play(FadeIn(indicator))

        self.play(
            indicator.animate.set_opacity(0.5)
        )

        # diameter
        diameter = DoubleArrow(OBSERVER_POINT,
                               ls0.get_center(),
                               buff=0,
                               color=WHITE,
                               )
        diameter_text = MathTex("d").scale(TEX_SCALE)
        diameter_text.next_to(diameter, RIGHT)

        self.play(
            Create(diameter),
            Write(diameter_text),
            FadeOut(self.ls0_dot)
        )

        indicator_reading = MathTex("{1\\over d^2}").scale(TEX_SCALE)
        indicator_reading.move_to(indicator)
        self.unzoomable_mobs.add(indicator_reading)

        self.play(
            FadeIn(indicator_reading)
        )

        # replace d with its value
        new_diameter_text = MathTex("{2\\over \\pi}").scale(TEX_SCALE)
        new_diameter_text.set_color(LAKE_COLOR)
        new_diameter_text.move_to(diameter_text)
        self.play(
            Transform(diameter_text, new_diameter_text)
        )

        # insert into indicator reading
        new_reading = MathTex("{\\pi^2 \\over 4}").scale(TEX_SCALE)
        new_reading.move_to(indicator)

        self.play(
            Transform(indicator_reading, new_reading)
        )

        self.play(
            FadeOut(one_left),
            FadeOut(one_right),
            FadeOut(diameter_text),
            FadeOut(arc_left),
            FadeOut(arc_right)
        )

        def indicator_wiggle():
            INDICATOR_WIGGLE_FACTOR = 1.3

            self.play(
                indicator.animate.scale(INDICATOR_WIGGLE_FACTOR).set_rate_func(wiggle),
                indicator_reading.animate.scale(INDICATOR_WIGGLE_FACTOR).set_rate_func(wiggle)
            )

        def angle_for_index(i, step):
            return -TAU / 4 + TAU / 2 ** step * (i + 0.5)

        def position_for_index(i, step, scaled_down=False):
            theta = angle_for_index(i, step)
            radial_vector = np.array([np.cos(theta), np.sin(theta), 0])
            position = self.lake_center + self.lake_radius * radial_vector

            if scaled_down:
                return position * 0.5 + self.obs_dot.get_center() * 0.5
            else:
                return position

        def split_light_source(i, step, show_steps=True, run_time=1):
            ls_new_loc1 = position_for_index(i, step + 1)
            ls_new_loc2 = position_for_index(i + 2 ** step, step + 1)

            hyp = VMobject()
            hyp1 = Line(self.lake_center, ls_new_loc1)
            hyp2 = Line(self.lake_center, ls_new_loc2)
            hyp.add(hyp2, hyp1)
            self.new_hypotenuses.append(hyp)

            if show_steps == True:
                self.play(
                    Create(hyp, run_time=run_time)
                )

            leg1 = Line(self.obs_dot.get_center(), ls_new_loc1)
            leg2 = Line(self.obs_dot.get_center(), ls_new_loc2)
            self.new_legs_1.append(leg1)
            self.new_legs_2.append(leg2)

            if show_steps == True:
                self.play(
                    Create(leg1, run_time=run_time),
                    Create(leg2, run_time=run_time),
                )

            ls1 = self.light_sources_array[i]

            ls2 = ls1.copy()
            self.add(ls2)
            self.additional_light_sources.append(ls2)

            # check if the light sources are on screen
            ls_old_loc = np.array(ls1.get_center())
            onscreen_old = np.all(np.abs(ls_old_loc[:2]) < 10 ** 2 ** step)
            onscreen_1 = np.all(np.abs(ls_new_loc1[:2]) < 10 ** 2 ** step)
            onscreen_2 = np.all(np.abs(ls_new_loc2[:2]) < 10 ** 2 ** step)
            show_animation = (onscreen_old or onscreen_1 or onscreen_2)

            if show_animation:
                print("animating (", i, ",", step, ")")
                self.play(
                    ls1.animate.move_to(ls_new_loc1, run_time=run_time),
                    ls2.animate.move_to(ls_new_loc2, run_time=run_time),
                )
            else:
                ls1.move_to(ls_new_loc1)
                ls2.move_to(ls_new_loc1)

        def construction_step(n, show_steps=True, run_time=1,
                              simultaneous_splitting=False):
            # first, fade out all of the hypotenuses and altitudes
            if show_steps == True:
                self.zoomable_mobs.remove(self.hypotenuses, self.altitudes, self.inner_lake)
                self.play(
                    FadeOut(self.hypotenuses),
                    FadeOut(self.altitudes),
                    FadeOut(self.inner_lake)
                )
            else:
                self.zoomable_mobs.remove(self.inner_lake)
                self.play(
                    FadeOut(self.inner_lake)
                )

            # create a new, outer lake
            self.lake_center = self.obs_dot.get_center() + self.lake_radius * UP

            new_outer_lake = Circle(radius=self.lake_radius,
                                    stroke_width=LAKE_STROKE_WIDTH,
                                    fill_color=LAKE_COLOR,
                                    fill_opacity=LAKE_OPACITY,
                                    stroke_color=LAKE_STROKE_COLOR
                                    )
            new_outer_lake.move_to(self.lake_center)

            if show_steps == True:
                self.play(
                    FadeIn(new_outer_lake, run_time=run_time),
                    FadeIn(self.ls0_dot)
                )
            else:
                self.play(
                    FadeIn(new_outer_lake, run_time=run_time),
                )

            self.wait()

            self.inner_lake = self.outer_lake
            self.outer_lake = new_outer_lake
            self.altitudes = self.legs

            self.additional_light_sources = []
            self.new_legs_1 = []
            self.new_legs_2 = []
            self.new_hypotenuses = []

            for i in range(2 ** n):
                split_light_source(i,
                                   step=n,
                                   show_steps=show_steps,
                                   run_time=run_time
                                   )

            # collect the newly created mobs (in arrays)
            # into the appropriate Mobject containers
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

            # update scene
            self.add(
                self.light_sources,
                self.inner_lake,
                self.outer_lake,
            )
            self.zoomable_mobs.add(self.light_sources, self.inner_lake, self.outer_lake)

            if show_steps == True:
                self.add(
                    self.legs,
                    self.hypotenuses,
                    self.altitudes,
                )
                self.zoomable_mobs.add(self.legs, self.hypotenuses, self.altitudes)

            self.wait()

            if show_steps == True:
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

        self.lake_radius = 2 * LAKE0_RADIUS  # don't ask...

        self.zoomable_mobs.add(self.inner_lake, self.outer_lake, self.altitudes, self.light_sources)

        self.add(self.inner_lake,
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

        self.revert_to_original_skipping_status()

        construction_step(0)
        indicator_wiggle()
        self.play(FadeOut(self.ls0_dot))
        zoom_out_scene(2)

        # Note: The original code has "return" here which stops execution
        # I'll comment it out to allow the rest to run
        # return

        construction_step(1)
        indicator_wiggle()
        self.play(FadeOut(self.ls0_dot))
        zoom_out_scene(2)

        construction_step(2)
        indicator_wiggle()
        self.play(FadeOut(self.ls0_dot))

        self.revert_to_original_skipping_status()

        ANGLE_COLOR1 = BLUE_C
        ANGLE_COLOR2 = GREEN_D

        for mob in self.mobjects:
            mob.set_opacity(0)

        for hyp in self.hypotenuses:
            hyp.set_stroke(width=0)
        for alt in self.altitudes:
            alt.set_stroke(width=0)
        for leg in self.legs:
            leg.set_stroke(width=0)
        self.inner_lake.set_stroke(width=0)
        self.outer_lake.set_stroke(width=0)

        self.wait()

        inner_lake_center = self.inner_lake.get_center()
        inner_lake_radius = self.lake_radius * 0.25
        inner_ls = VGroup()
        for i in range(4):
            theta = -TAU / 4 + (i + 0.5) * TAU / 4
            point = inner_lake_center + inner_lake_radius * np.array([np.cos(theta), np.sin(theta), 0])
            dot = Dot(point, color=LAKE_STROKE_COLOR, radius=0.3)
            inner_ls.add(dot)

        self.add(inner_ls)

        inner_ls1 = inner_ls.submobjects[0]
        inner_ls2 = inner_ls.submobjects[1]
        inner_ls1_center = inner_ls1.get_center()
        inner_ls2_center = inner_ls2.get_center()

        outer_lake_center = self.outer_lake.get_center()
        outer_lake_radius = self.lake_radius * 0.5
        outer_ls = VGroup()
        for i in range(8):
            theta = -TAU / 4 + (i + 0.5) * TAU / 8
            point = outer_lake_center + outer_lake_radius * np.array([np.cos(theta), np.sin(theta), 0])
            dot = Dot(point, color=LAKE_STROKE_COLOR, radius=0.3)
            outer_ls.add(dot)

        self.add(outer_ls)

        outer_ls1 = outer_ls.submobjects[0]
        outer_ls2 = outer_ls.submobjects[1]
        outer_ls1_center = outer_ls1.get_center()
        outer_ls2_center = outer_ls2.get_center()

        self.wait()

        arc_radius = 2.0

        line1 = Line(inner_lake_center, inner_ls1_center, color=WHITE)
        line2 = Line(inner_lake_center, inner_ls2_center, color=WHITE)

        inner_angle_arc = Arc(angle=TAU / 4, start_angle=-TAU / 8, radius=arc_radius,
                              stroke_color=ANGLE_COLOR1)
        inner_angle_arc.move_arc_center_to(inner_lake_center)

        inner_label = MathTex("\\theta", color=ANGLE_COLOR1).scale(3).next_to(inner_angle_arc, LEFT, buff=-0.1)

        self.play(
            Create(line1),
            Create(line2),
        )
        self.play(
            Create(inner_angle_arc),
            FadeIn(inner_label)
        )

        self.wait()

        line3 = Line(outer_lake_center, inner_ls1_center, color=WHITE)
        line4 = Line(outer_lake_center, inner_ls2_center, color=WHITE)
        outer_angle_arc = Arc(angle=TAU / 8, start_angle=-3 * TAU / 16, radius=arc_radius,
                              stroke_color=ANGLE_COLOR2)
        outer_angle_arc.move_arc_center_to(outer_lake_center)

        outer_label = MathTex("{\\theta \\over 2}", color=ANGLE_COLOR2).scale(2.5).move_to(outer_angle_arc)
        outer_label.shift([-2, -1, 0])

        self.play(
            Create(line3),
            Create(line4),
        )
        self.play(
            Create(outer_angle_arc),
            FadeIn(outer_label)
        )

        self.wait()

        line5 = Line(outer_lake_center, outer_ls1_center, color=WHITE)
        line6 = Line(outer_lake_center, outer_ls2_center, color=WHITE)

        self.play(
            Create(line5),
            Create(line6)
        )

        self.wait()

        self.play(
            FadeOut(line1),
            FadeOut(line2),
            FadeOut(line3),
            FadeOut(line4),
            FadeOut(line5),
            FadeOut(line6),
            FadeOut(inner_angle_arc),
            FadeOut(outer_angle_arc),
            FadeOut(inner_label),
            FadeOut(outer_label),
        )

        self.wait()

        inner_lines = VGroup()
        inner_arcs = VGroup()

        for i in range(-2, 2):
            theta = -TAU / 4 + (i + 0.5) * TAU / 4
            ls_point = inner_lake_center + inner_lake_radius * np.array([
                np.cos(theta), np.sin(theta), 0])
            line = Line(inner_lake_center, ls_point, color=WHITE)
            inner_lines.add(line)

            arc = Arc(angle=TAU / 4, start_angle=theta, radius=arc_radius,
                      stroke_color=ANGLE_COLOR1)
            arc.move_arc_center_to(inner_lake_center)
            inner_arcs.add(arc)

            if i == 1:
                arc.set_stroke(width=0)

        for line in inner_lines.submobjects:
            self.play(
                Create(line),
            )
        self.add_foreground_mobject(inner_lines)
        for arc in inner_arcs.submobjects:
            self.play(
                Create(arc)
            )

        self.wait()

        outer_lines = VGroup()
        outer_arcs = VGroup()

        for i in range(-2, 2):
            theta = -TAU / 4 + (i + 0.5) * TAU / 4

            ls_point = inner_lake_center + inner_lake_radius * np.array([
                np.cos(theta), np.sin(theta), 0])
            line = Line(outer_lake_center, ls_point, color=WHITE)
            outer_lines.add(line)

            theta = -TAU / 4 + (i + 0.5) * TAU / 8
            arc = Arc(angle=TAU / 8, start_angle=theta, radius=arc_radius,
                      stroke_color=ANGLE_COLOR2)
            arc.move_arc_center_to(outer_lake_center)
            outer_arcs.add(arc)

            if i == 1:
                arc.set_stroke(width=0)

        for line in outer_lines.submobjects:
            self.play(
                Create(line),
            )
        self.add_foreground_mobject(outer_lines)
        for arc in outer_arcs.submobjects:
            self.play(
                Create(arc)
            )

        self.wait()

        self.play(
            FadeOut(inner_lines),
            FadeOut(inner_arcs)
        )

        outer_lines2 = VGroup()

        for i in range(-2, 2):
            theta = -TAU / 4 + (i + 0.5) * TAU / 8
            ls_point = outer_lake_center + outer_lake_radius * np.array([
                np.cos(theta), np.sin(theta), 0])
            line = Line(outer_lake_center, ls_point, color=WHITE)
            outer_lines2.add(line)

        self.play(
            Create(outer_lines2),
        )

        self.wait()

        outer_lines3 = outer_lines2.copy().rotate(TAU / 2, about_point=outer_lake_center)
        outer_arcs3 = outer_arcs.copy().rotate(TAU / 2, about_point=outer_lake_center)

        self.play(
            Create(outer_lines3),
        )
        self.add_foreground_mobject(outer_lines3)
        for arc in outer_arcs3.submobjects:
            self.play(
                Create(arc)
            )

        last_arc = outer_arcs3.submobjects[0].copy()
        last_arc.rotate(-TAU / 8, about_point=outer_lake_center)
        last_arc2 = last_arc.copy()
        last_arc2.rotate(TAU / 2, about_point=outer_lake_center)

        self.play(
            Create(last_arc),
            Create(last_arc2),
        )

        self.wait()

        self.play(
            FadeOut(outer_lines2),
            FadeOut(outer_lines3),
            FadeOut(outer_arcs),
            FadeOut(outer_arcs3),
            FadeOut(last_arc),
            FadeOut(last_arc2),
        )

        self.play(
            FadeOut(inner_ls),
            FadeOut(outer_ls),
        )

        self.wait()
