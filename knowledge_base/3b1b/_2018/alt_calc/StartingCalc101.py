# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示一個 PiCreature 角色在「微積分 101」標題下，透過一系列圖像（數學公式、物理動畫、圖形直覺等）逐步介紹微積分主題，最後聚焦於一個神秘方框的過程。


from manim import *
import itertools as it
import cv2
import numpy as np

class StartingCalc101(PiCreatureScene):
    def __init__(self, camera_config={"background_opacity": 1}, image_frame_width=3.5, image_frame_height=2.5, **kwargs):
        super().__init__(camera_config=camera_config, **kwargs)
        self.image_frame_width = image_frame_width
        self.image_frame_height = image_frame_height

    def construct(self):
        self.show_you()
        self.show_images()
        self.show_mystery_topic()

    def show_you(self):
        randy = self.pi_creature
        title = self.title = Title("Calculus 101")
        you = Text("You")
        arrow = Vector(DL, color=WHITE)
        arrow.next_to(randy, UR)
        you.next_to(arrow.get_start(), UP)

        self.play(
            Write(you),
            GrowArrow(arrow),
            randy.animate.change("erm", title)
        )
        self.wait()
        self.play(Write(title, run_time=1))
        self.play(FadeOut(VGroup(arrow, you)))

    def show_images(self):
        randy = self.pi_creature
        images = self.get_all_images()
        modes = [
            "pondering",  # hard_work_image
            "pondering",  # neat_example_image
            "hesitant",  # not_so_neat_example_image
            "hesitant",  # physics_image
            "horrified",  # piles_of_formulas_image
            "horrified",  # getting_stuck_image
            "thinking",  # aha_image
            "thinking",  # graphical_intuition_image
        ]

        for i, image, mode in zip(it.count(), images, modes):
            anims = []
            if hasattr(image, "fade_in_anim"):
                anims.append(image.fade_in_anim)
                anims.append(FadeIn(image.frame))
            else:
                anims.append(FadeIn(image))

            if i >= 3:
                image_to_fade_out = images[i - 3]
                if hasattr(image_to_fade_out, "fade_out_anim"):
                    anims.append(image_to_fade_out.fade_out_anim)
                else:
                    anims.append(FadeOut(image_to_fade_out))

            if hasattr(image, "continual_animations"):
                self.add(*image.continual_animations)

            anims.append(randy.animate.change(mode))
            self.play(*anims)
            self.wait()
            if i >= 3:
                if hasattr(image_to_fade_out, "continual_animations"):
                    self.remove(*image_to_fade_out.continual_animations)
                self.remove(image_to_fade_out.frame)
        self.wait(3)

        self.remaining_images = images[-3:]

    def show_mystery_topic(self):
        images = self.remaining_images
        randy = self.pi_creature

        mystery_box = Rectangle(
            width=self.image_frame_width,
            height=self.image_frame_height,
            stroke_color=YELLOW,
            fill_color=GREY_D,
            fill_opacity=0.5,
        )
        mystery_box.scale(1.5)
        mystery_box.next_to(self.title, DOWN, buff=MED_LARGE_BUFF)

        rects = images[-1].rects.copy()
        rects.center()
        rects.set_height(config.frame_height - 1)
        # 注意：以下路徑需要根據實際檔案位置調整
        # open_cv_image = cv2.imread(get_full_raster_image_path("alt_calc_hidden_image"))
        # 暫時用一個空白圖像替代
        open_cv_image = np.zeros((100, 100, 3), dtype=np.uint8)
        blurry_image = cv2.blur(open_cv_image, (50, 50))
        array = np.array(blurry_image)[:, :, ::-1]
        im_mob = ImageMobject(array)
        im_mob.replace(mystery_box, stretch=True)
        mystery_box.add(im_mob)

        q_marks = MathTex("???").scale(3)
        q_marks.space_out_submobjects(1.5)
        q_marks.set_stroke(BLACK, 1)
        q_marks.move_to(mystery_box)
        mystery_box.add(q_marks)

        for image in images:
            if hasattr(image, "continual_animations"):
                self.remove(*image.continual_animations)
            self.play(
                image.animate.shift(DOWN),
                image.animate.set_opacity(0),
                randy.animate.change("erm"),
                run_time=1.5
            )
            self.remove(image)
        self.wait()
        self.play(
            FadeIn(mystery_box, shift=DOWN),
            randy.animate.change("confused")
        )
        self.wait(5)

    # Helpers

    def get_all_images(self):
        # Images matched to narration's introductory list
        images = VGroup(
            self.get_hard_work_image(),
            self.get_neat_example_image(),
            self.get_not_so_neat_example_image(),
            self.get_physics_image(),
            self.get_piles_of_formulas_image(),
            self.get_getting_stuck_image(),
            self.get_aha_image(),
            self.get_graphical_intuition_image(),
        )
        colors = color_gradient([BLUE, YELLOW], len(images))
        for i, image, color in zip(it.count(), images, colors):
            self.adjust_size(image)
            frame = Rectangle(
                width=self.image_frame_width,
                height=self.image_frame_height,
                color=color,
                stroke_width=2,
            )
            frame.move_to(image)
            image.frame = frame
            image.add(frame)
            image.next_to(self.title, DOWN)
            alt_i = (i % 3) - 1
            vect = (self.image_frame_width + LARGE_BUFF) * RIGHT
            image.shift(alt_i * vect)
        return images

    def adjust_size(self, group):
        group.set_width(min(
            group.get_width(),
            self.image_frame_width - 2 * MED_SMALL_BUFF
        ))
        group.set_height(min(
            group.get_height(),
            self.image_frame_height - 2 * MED_SMALL_BUFF
        ))
        return group

    def get_hard_work_image(self):
        new_randy = self.pi_creature.copy()
        new_randy.change_mode("telepath")
        bubble = new_randy.get_bubble(height=3.5, width=4)
        bubble.add_content(MathTex("\\frac{d}{dx}(\\sin(\\sqrt{x}))"))
        bubble.add(bubble.content)  # Remove?

        return VGroup(new_randy, bubble)

    def get_neat_example_image(self):
        filled_circle = Circle(
            stroke_width=0,
            fill_color=BLUE_E,
            fill_opacity=1
        )
        area = MathTex("\\pi r^2")
        area.move_to(filled_circle)
        unfilled_circle = Circle(
            stroke_width=3,
            stroke_color=YELLOW,
            fill_opacity=0,
        )
        unfilled_circle.next_to(filled_circle, RIGHT)
        circles = VGroup(filled_circle, unfilled_circle)
        circumference = MathTex("2\\pi r")
        circumference.move_to(unfilled_circle)
        equation = MathTex(
            "{d (\\pi r^2) \\over dr}  = 2\\pi r",
            tex_to_color_map={
                "\\pi r^2": BLUE_D,
                "2\\pi r": YELLOW,
            }
        )
        equation.next_to(circles, UP)

        return VGroup(
            filled_circle, area,
            unfilled_circle, circumference,
            equation
        )

    def get_not_so_neat_example_image(self):
        return MathTex("\\int x \\cos(x) \\, dx")

    def get_physics_image(self):
        t_max = 6.5
        r = 0.2
        spring = ParametricFunction(
            lambda t: np.array([
                r * np.sin(TAU * t),
                -t,
                0
            ]),
            t_range=[0, t_max],
            color=WHITE,
            stroke_width=2,
        )
        # 移除 color_using_background_image，改用 set_color
        spring.set_color(WHITE)

        weight = Square()
        weight.set_stroke(width=0)
        weight.set_fill(opacity=1)
        weight.set_color(WHITE)  # 替代 color_using_background_image
        weight.set_height(0.4)

        t_tracker = ValueTracker(0)
        group = VGroup(spring, weight)
        group.continual_animations = [
            t_tracker.add_updater(
                lambda tracker, dt: tracker.set_value(
                    tracker.get_value() + dt
                )
            ),
            spring.add_updater(
                lambda s: s.stretch_to_fit_height(
                    1.5 + 0.5 * np.cos(3 * t_tracker.get_value()),
                    about_edge=UP
                )
            ),
            weight.add_updater(
                lambda w: w.move_to(spring.get_points()[-1])
            )
        ]

        def update_group_style(alpha):
            spring.set_stroke(width=2 * alpha)
            weight.set_fill(opacity=alpha)

        group.fade_in_anim = UpdateFromAlphaFunc(
            group,
            lambda g, a: update_group_style(a)
        )
        group.fade_out_anim = UpdateFromAlphaFunc(
            group,
            lambda g, a: update_group_style(1 - a)
        )
        return group

    def get_piles_of_formulas_image(self):
        return MathTex("(f/g)' = \\frac{gf' - fg'}{g^2}")

    def get_getting_stuck_image(self):
        creature = self.pi_creature.copy()
        creature.change_mode("angry")
        equation = MathTex("\\frac{d}{dx}(x^x)")
        equation.set_height(creature.get_height() / 2)
        equation.next_to(creature, RIGHT, aligned_edge=UP)
        creature.look_at(equation)
        return VGroup(creature, equation)

    def get_aha_image(self):
        creature = self.pi_creature.copy()
        creature.change_mode("hooray")
        # 由於無法導入 NudgeSideLengthOfCube，用一個簡單的立方體替代
        cube = Cube(side_length=1)
        cube.set_fill(BLUE, opacity=0.8)
        cube.set_stroke(WHITE, width=2)
        group = VGroup(cube)
        group.set_height(0.75 * creature.get_height())
        group.next_to(creature, RIGHT)
        creature.look_at(group)
        return VGroup(creature, group)

    def get_graphical_intuition_image(self):
        ax = Axes(
            x_range=[2, 8, 1],
            y_range=[0, 6, 1],
            axis_config={"include_numbers": True}
        )
        graph = ax.plot(
            lambda x: 0.2 * (x - 3) * (x - 5) * (x - 6) + 4,
            x_range=[2, 8],
            color=BLUE
        )
        rects = ax.get_riemann_rectangles(
            graph, x_range=[2, 8],
            stroke_width=0.5,
            dx=0.25
        )
        group = VGroup(ax, graph, rects)
        self.adjust_size(group)
        group.next_to(self.title, DOWN, buff=MED_LARGE_BUFF)
        group.rects = rects
        # 簡化 continual_animations，用一個簡單的寫入動畫
        group.continual_animations = [
            Write(rects, run_time=2, rate_func=linear),
            Create(graph, run_time=2, rate_func=linear),
            Write(ax, run_time=2, rate_func=linear),
        ]
        self.adjust_size(group)
        return group
