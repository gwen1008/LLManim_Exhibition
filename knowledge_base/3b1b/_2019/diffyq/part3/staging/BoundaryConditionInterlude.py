# Source: 3b1b/_2019/diffyq/part3/staging.py
# Description: [3b1b translated] 展示一個帶有邊界條件插曲的動畫流程，其中圖像沿著故事線排列並通過箭頭連接，最終重組成左右兩組並標示下一部分。



from manim import *
class BoundaryConditionInterlude(Scene):
    def construct(self):
        background = FullScreenFadeRectangle(
            fill_color=GREY_D
        )
        storyline = self.get_main_storyline()
        storyline.generate_target()
        v_shift = 2 * DOWN
        storyline.target.shift(v_shift)
        im_to_im = storyline[1].get_center() - storyline[0].get_center()

        bc_image = self.get_labeled_image(
            "Boundary\\\\conditions",
            "boundary_condition_thumbnail"
        )
        bc_image.next_to(storyline[1], UP)
        new_arrow0 = Arrow(
            storyline.arrows[0].get_start() + v_shift,
            bc_image.get_left() + SMALL_BUFF * LEFT,
            path_arc=-90 * DEGREES,
            buff=0,
        )
        new_mid_arrow = Arrow(
            bc_image.get_bottom(),
            storyline[1].get_top() + v_shift,
            buff=SMALL_BUFF,
            path_arc=60 * DEGREES,
        )

        # BC detour
        self.add(background)
        self.add(storyline[0])
        for im1, im2, arrow in zip(storyline, storyline[1:], storyline.arrows):
            self.add(im2, im1)
            self.play(
                FadeIn(im2, shift=-im_to_im),
                Create(arrow),
            )
        self.wait()
        self.play(
            GrowFromCenter(bc_image),
            MoveToTarget(storyline),
            Transform(
                storyline.arrows[0],
                new_arrow0,
            ),
            MaintainPositionRelativeTo(
                storyline.arrows[1],
                storyline,
            ),
        )
        self.play(Create(new_mid_arrow))
        self.wait()

        # From BC to next step
        rect1 = bc_image[2].copy()
        rect2 = storyline[1][2].copy()
        rect3 = storyline[2][2].copy()
        for rect in rect1, rect2, rect3:
            rect.set_stroke(YELLOW, 3)

        self.play(FadeIn(rect1))
        kw = {"path_arc": 60 * DEGREES}
        self.play(
            LaggedStart(
                Transform(rect1, rect2, **kw),
                # TransformFromCopy(rect1, rect3, **kw),
                lag_ratio=0.4,
            )
        )
        self.play(
            FadeOut(rect1),
            # FadeOut(rect3),
        )

        # Reorganize images
        im1, im3, im4 = storyline
        im2 = bc_image
        l_group = Group(im1, im2)
        r_group = Group(im3, im4)
        for group in l_group, r_group:
            group.generate_target()
            group.target.arrange(DOWN, buff=LARGE_BUFF)
            group.target.center()

        l_group.target.to_edge(LEFT)
        r_group.target.move_to(
            FRAME_WIDTH * RIGHT / 4
        )
        brace = Brace(r_group.target, LEFT)
        nv_text = brace.get_text("Next\\\\video")
        nv_text.scale(1.5, about_edge=RIGHT)
        nv_text.set_color(YELLOW)
        brace.set_color(YELLOW)

        arrows = VGroup(
            storyline.arrows,
            new_mid_arrow,
        )

        self.play(
            LaggedStart(
                MoveToTarget(l_group),
                MoveToTarget(r_group),
                lag_ratio=0.3,
            ),
            FadeOut(arrows),
        )
        self.play(
            GrowFromCenter(brace),
            FadeIn(nv_text, shift=RIGHT)
        )
        self.wait()

    def get_main_storyline(self):
        images = Group(
            self.get_sine_curve_image(),
            self.get_linearity_image(),
            self.get_fourier_series_image(),
        )
        for image in images:
            image.set_height(3)
        images.arrange(RIGHT, buff=1)
        images.set_width(config.frame_width - 1)

        arrows = VGroup()
        for im1, im2 in zip(images, images[1:]):
            arrow = Arrow(
                im1.get_top(),
                im2.get_top(),
                color=WHITE,
                buff=MED_SMALL_BUFF,
                path_arc=-120 * DEGREES,
                rectangular_stem_width=0.025,
            )
            arrow.scale(0.7, about_edge=DOWN)
            arrows.add(arrow)
        images.arrows = arrows

        return images

    def get_sine_curve_image(self):
        return self.get_labeled_image(
            "Sine curves",
            "sine_curve_temp_graph",
        )

    def get_linearity_image(self):
        return self.get_labeled_image(
            "Linearity",
            "linearity_thumbnail",
        )

    def get_fourier_series_image(self):
        return self.get_labeled_image(
            "Fourier series",
            "fourier_series_thumbnail",
        )

    def get_labeled_image(self, text, image_file):
        rect = ScreenRectangle(height=2)
        border = rect.copy()
        rect.set_fill(BLACK, 1)
        rect.set_stroke(WHITE, 0)
        border.set_stroke(WHITE, 2)

        text_mob = Text(text)
        text_mob.set_stroke(BLACK, 5, background=True)
        text_mob.next_to(rect.get_top(), DOWN, SMALL_BUFF)

        # 注意：ManimCE 中 ImageMobject 已改為 Image
        # 但由於 image_file 參數不確定，這裡保持原結構
        # 實際使用時可能需要調整為 Image(image_file)
        image = ImageMobject(image_file)
        image.replace(rect, dim_to_match=1)
        image.scale(0.8, about_edge=DOWN)

        return Group(rect, image, border, text_mob)
