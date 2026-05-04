# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示一個具有縮放功能的數線變換場景，包含輸入與輸出數線，並能對樣本點進行函數映射動畫。



from manim import *
class NumberlineTransformationScene(ZoomedScene):
    def __init__(
        self,
        input_line_zero_point=0.5 * UP + (config.frame_width / 2 - 1) * LEFT,
        output_line_zero_point=2 * DOWN + (config.frame_width / 2 - 1) * LEFT,
        number_line_config={
            "include_numbers": True,
            "x_range": [-3.5, 3.5, 1],
            "length": 14,  # unit_size=2 * (3.5 - (-3.5)) = 14
        },
        input_line_config={"color": BLUE},
        output_line_config={},
        num_inserted_number_line_curves=20,
        default_delta_x=0.1,
        default_sample_dot_radius=0.07,
        default_sample_dot_colors=[RED, YELLOW],
        default_mapping_animation_config={"run_time": 3},
        local_coordinate_num_decimal_places=2,
        zoom_factor=0.1,
        zoomed_display_height=2.5,
        zoomed_display_corner_buff=MED_SMALL_BUFF,
        mini_line_scale_factor=2,
        default_coordinate_value_dx=0.05,
        zoomed_camera_background_rectangle_fill_opacity=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.input_line_zero_point = input_line_zero_point
        self.output_line_zero_point = output_line_zero_point
        self.number_line_config = number_line_config
        self.input_line_config = input_line_config
        self.output_line_config = output_line_config
        self.num_inserted_number_line_curves = num_inserted_number_line_curves
        self.default_delta_x = default_delta_x
        self.default_sample_dot_radius = default_sample_dot_radius
        self.default_sample_dot_colors = default_sample_dot_colors
        self.default_mapping_animation_config = default_mapping_animation_config
        self.local_coordinate_num_decimal_places = local_coordinate_num_decimal_places
        self.zoom_factor = zoom_factor
        self.zoomed_display_height = zoomed_display_height
        self.zoomed_display_corner_buff = zoomed_display_corner_buff
        self.mini_line_scale_factor = mini_line_scale_factor
        self.default_coordinate_value_dx = default_coordinate_value_dx
        self.zoomed_camera_background_rectangle_fill_opacity = zoomed_camera_background_rectangle_fill_opacity

    def setup(self):
        super().setup()
        self.setup_number_lines()
        self.setup_titles()
        self.setup_zoomed_camera_background_rectangle()

    def setup_number_lines(self):
        number_lines = self.number_lines = VGroup()
        added_configs = (self.input_line_config, self.output_line_config)
        zero_points = (self.input_line_zero_point, self.output_line_zero_point)
        for added_config, zero_point in zip(added_configs, zero_points):
            full_config = dict(self.number_line_config)
            full_config.update(added_config)
            number_line = NumberLine(**full_config)
            # ManimCE 的 NumberLine 沒有 insert_n_curves 方法，改用增加曲線數量的替代方案
            # 這裡我們保持原樣，因為這不影響核心功能
            number_line.shift(zero_point - number_line.number_to_point(0))
            number_lines.add(number_line)
        self.input_line, self.output_line = number_lines

        self.add(number_lines)

    def setup_titles(self):
        input_title, output_title = self.titles = VGroup(*[
            Text(word)
            for word in ("Inputs", "Outputs")
        ])
        vects = [UP, DOWN]
        for title, line, vect in zip(self.titles, self.number_lines, vects):
            title.next_to(line, vect, aligned_edge=LEFT)
            # shift_onto_screen 在 ManimCE 中不存在，改用 ensure_on_screen
            title.ensure_on_screen()

        self.add(self.titles)

    def setup_zoomed_camera_background_rectangle(self):
        frame = self.zoomed_camera.frame
        frame.next_to(self.camera.frame, UL)
        self.zoomed_camera_background_rectangle = BackgroundRectangle(
            frame, fill_opacity=self.zoomed_camera_background_rectangle_fill_opacity
        )
        self.zoomed_camera_background_rectangle_anim = UpdateFromFunc(
            self.zoomed_camera_background_rectangle,
            lambda m: m.replace(frame, stretch=True)
        )
        self.zoomed_camera_background_rectangle_group = VGroup(
            self.zoomed_camera_background_rectangle,
        )

    def get_sample_input_points(self, x_min=None, x_max=None, delta_x=None):
        x_min = x_min or self.input_line.x_range[0]
        x_max = x_max or self.input_line.x_range[1]
        delta_x = delta_x or self.default_delta_x
        return [
            self.get_input_point(x)
            for x in np.arange(x_min, x_max + delta_x, delta_x)
        ]

    def get_sample_dots(self, x_min=None, x_max=None,
                        delta_x=None, dot_radius=None, colors=None):
        dot_radius = dot_radius or self.default_sample_dot_radius
        colors = colors or self.default_sample_dot_colors

        dots = VGroup(*[
            Dot(point, radius=dot_radius)
            for point in self.get_sample_input_points(x_min, x_max, delta_x)
        ])
        dots.set_color_by_gradient(*colors)
        return dots

    def get_local_sample_dots(self, x, sample_radius=None, **kwargs):
        zoom_factor = self.get_zoom_factor()
        delta_x = kwargs.get("delta_x", self.default_delta_x * zoom_factor)
        dot_radius = kwargs.get("dot_radius", self.default_sample_dot_radius * zoom_factor)

        if sample_radius is None:
            unrounded_radius = self.zoomed_camera.frame.get_width() / 2
            sample_radius = int(unrounded_radius / delta_x) * delta_x
        config = {
            "x_min": x - sample_radius,
            "x_max": x + sample_radius,
            "delta_x": delta_x,
            "dot_radius": dot_radius,
        }
        config.update(kwargs)
        return self.get_sample_dots(**config)

    def add_sample_dot_ghosts(self, sample_dots, fade_factor=0.5):
        self.sample_dot_ghosts = sample_dots.copy()
        self.sample_dot_ghosts.set_opacity(1 - fade_factor)
        self.add(self.sample_dot_ghosts, sample_dots)

    def get_local_coordinate_values(self, x, dx=None, n_neighbors=1):
        dx = dx or self.default_coordinate_value_dx
        return [
            x + n * dx
            for n in range(-n_neighbors, n_neighbors + 1)
        ]

    # Mapping animations
    def get_mapping_animation(self, func, mobject,
                              how_to_apply_func=lambda f, m: None,  # 預設空函數
                              **kwargs):
        anim_config = dict(self.default_mapping_animation_config)
        anim_config.update(kwargs)

        point_func = self.number_func_to_point_func(func)

        mobject.generate_target()
        how_to_apply_func(point_func, mobject.target)
        return MoveToTarget(mobject, **anim_config)

    def get_line_mapping_animation(self, func, **kwargs):
        input_line_copy = self.input_line.copy()
        self.moving_input_line = input_line_copy
        # 移除數字標籤
        for mob in input_line_copy:
            if isinstance(mob, DecimalNumber):
                input_line_copy.remove(mob)
        # 在 ManimCE 中，NumberLine 沒有 insert_n_curves 方法
        # 這裡我們跳過這個步驟，因為它不影響核心動畫
        return AnimationGroup(
            self.get_mapping_animation(
                func, input_line_copy,
                lambda f, m: setattr(m, "points", f(m.get_points()))  # 簡化版本
            ),
            self.get_mapping_animation(
                func, VGroup(*[m for m in input_line_copy if isinstance(m, Line)]),
                lambda f, m: [setattr(submob, "points", f(submob.get_points())) for submob in m]
            ),
        )

    def get_sample_dots_mapping_animation(self, func, dots, **kwargs):
        return self.get_mapping_animation(
            func, dots, how_to_apply_func=lambda f, m: [submob.move_to(f(submob.get_center())) for submob in m]
        )

    def get_zoomed_camera_frame_mapping_animation(self, func, x=None, **kwargs):
        frame = self.zoomed_camera.frame
        if x is None:
            point = frame.get_center()
        else:
            point = self.get_input_point(x)
        point_mob = Dot(point, radius=0)  # 使用不可見的點
        return AnimationGroup(
            self.get_mapping_animation(func, point_mob),
            UpdateFromFunc(frame, lambda m: m.move_to(point_mob)),
        )

    def apply_function(self, func,
                       apply_function_to_number_line=True,
                       sample_dots=None,
                       local_sample_dots=None,
                       target_coordinate_values=None,
                       added_anims=None,
                       **kwargs
                       ):
        zcbr_group = self.zoomed_camera_background_rectangle_group
        zcbr_anim = self.zoomed_camera_background_rectangle_anim
        frame = self.zoomed_camera.frame

        anims = []
        if apply_function_to_number_line:
            anims.append(self.get_line_mapping_animation(func))
        if hasattr(self, "mini_line"):
            anims.append(self.get_mapping_animation(
                func, self.mini_line,
                how_to_apply_func=lambda f, m: m.move_to(f(m.get_center()))
            ))
        if sample_dots:
            anims.append(
                self.get_sample_dots_mapping_animation(func, sample_dots)
            )
        if hasattr(self, "zoom_activated") and self.zoom_activated:
            zoom_anim = self.get_zoomed_camera_frame_mapping_animation(func)
            anims.append(zoom_anim)
            anims.append(zcbr_anim)

            # 手動更新動畫到結束狀態
            for anim in anims:
                if hasattr(anim, "update"):
                    anim.update(1)
            
            target_mini_line = Line(frame.get_left(), frame.get_right())
            target_mini_line.scale(self.mini_line_scale_factor)
            target_mini_line.set_style(**self.output_line.get_style())
            # 重置動畫狀態
            for anim in anims:
                if hasattr(anim, "update"):
                    anim.update(0)
                    
            zcbr_group.add(target_mini_line)
        if target_coordinate_values:
            coordinates = self.get_local_coordinates(
                self.output_line,
                *target_coordinate_values
            )
            anims.append(FadeIn(coordinates))
            zcbr_group.add(coordinates)
            self.local_target_coordinates = coordinates
        if local_sample_dots:
            anims.append(
                self.get_sample_dots_mapping_animation(func, local_sample_dots)
            )
            zcbr_group.add(local_sample_dots)
        if added_anims:
            anims += added_anims
        anims.append(Animation(zcbr_group))

        self.play(*anims, **kwargs)

    # Zooming
    def zoom_in_on_input(self, x,
                         local_sample_dots=None,
                         local_coordinate_values=None,
                         pop_out=True,
                         first_added_anims=None,
                         first_anim_kwargs=None,
                         second_added_anims=None,
                         second_anim_kwargs=None,
                         zoom_factor=None,
                         ):

        first_added_anims = first_added_anims or []
        first_anim_kwargs = first_anim_kwargs or {}
        second_added_anims = second_added_anims or []
        second_anim_kwargs = second_anim_kwargs or {}
        input_point = self.get_input_point(x)

        # Decide how to move camera frame into place
        frame = self.zoomed_camera.frame
        frame.generate_target()
        frame.target.move_to(input_point)
        if zoom_factor:
            frame.target.set_height(
                self.zoomed_display.get_height() * zoom_factor
            )
        movement = MoveToTarget(frame)
        zcbr = self.zoomed_camera_background_rectangle
        zcbr_group = self.zoomed_camera_background_rectangle_group
        zcbr_anim = self.zoomed_camera_background_rectangle_anim
        anims = []
        if hasattr(self, "zoom_activated") and self.zoom_activated:
            anims.append(movement)
            anims.append(zcbr_anim)
        else:
            # 手動更新動畫到結束狀態
            movement.update(1)
            zcbr_anim.update(1)
            anims.append(self.get_zoom_in_animation())
            anims.append(FadeIn(zcbr))

        # Make sure frame is in final place
        for anim in anims:
            if hasattr(anim, "update"):
                anim.update(1)

        # Add miniature number_line
        mini_line = self.mini_line = Line(frame.get_left(), frame.get_right())
        mini_line.scale(self.mini_line_scale_factor)
        # 跳過 insert_n_curves，因為在 ManimCE 中不可用
        mini_line.set_style(**self.input_line.get_style())
        mini_line_copy = mini_line.copy()
        zcbr_group.add(mini_line_copy, mini_line)
        anims += [FadeIn(mini_line), FadeIn(mini_line_copy)]

        # Add tiny coordinates
        if local_coordinate_values is None:
            local_coordinate_values = [x]
        local_coordinates = self.get_local_coordinates(
            self.input_line,
            *local_coordinate_values
        )
        anims.append(FadeIn(local_coordinates))
        zcbr_group.add(local_coordinates)
        self.local_coordinates = local_coordinates

        # Add tiny dots
        if local_sample_dots is not None:
            anims.append(LaggedStart(GrowFromCenter, local_sample_dots))
            zcbr_group.add(local_sample_dots)

        if first_added_anims:
            anims += first_added_anims

        anims.append(Animation(zcbr_group))
        if not pop_out:
            self.activate_zooming(animate=False)
        self.play(*anims, **first_anim_kwargs)

        if not hasattr(self, "zoom_activated") or not self.zoom_activated:
            if pop_out:
                self.activate_zooming(animate=False)
                added_anims = second_added_anims or []
                self.play(
                    self.get_zoomed_display_pop_out_animation(),
                    *added_anims,
                    **second_anim_kwargs
                )

    def get_local_coordinates(self, line, *x_values, **kwargs):
        num_decimal_places = kwargs.get(
            "num_decimal_places", self.local_coordinate_num_decimal_places
        )
        result = VGroup()
        result.tick_marks = VGroup()
        result.numbers = VGroup()
        result.add(result.tick_marks, result.numbers)
        for x in x_values:
            tick_mark = Line(UP, DOWN)
            tick_mark.set_height(
                0.15 * self.zoomed_camera.frame.get_height()
            )
            tick_mark.move_to(line.number_to_point(x))
            result.tick_marks.add(tick_mark)

            number = DecimalNumber(x, num_decimal_places=num_decimal_places)
            number.scale(self.get_zoom_factor())
            number.scale(0.5)  # To make it seem small
            number.next_to(tick_mark, DOWN, buff=0.5 * number.get_height())
            result.numbers.add(number)
        return result

    def get_mobjects_in_zoomed_camera(self, mobjects):
        frame = self.zoomed_camera.frame
        x_min = frame.get_left()[0]
        x_max = frame.get_right()[0]
        y_min = frame.get_bottom()[1]
        y_max = frame.get_top()[1]
        result = VGroup()
        for mob in mobjects:
            for point in mob.get_all_points():
                if (x_min < point[0] < x_max) and (y_min < point[1] < y_max):
                    result.add(mob)
                    break
        return result

    # Helpers
    def get_input_point(self, x):
        return self.input_line.number_to_point(x)

    def get_output_point(self, fx):
        return self.output_line.number_to_point(fx)

    def number_func_to_point_func(self, number_func):
        input_line, output_line = self.number_lines

        def point_func(point):
            input_number = input_line.point_to_number(point)
            output_number = number_func(input_number)
            return output_line.number_to_point(output_number)
        return point_func

    def get_zoom_factor(self):
        return self.zoom_factor
