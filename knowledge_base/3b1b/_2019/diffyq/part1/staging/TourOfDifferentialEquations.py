# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示一系列微分方程相關的視覺化縮圖沿著曲線排列，並將鏡頭聚焦到其中一個縮圖上。


from manim import *
import numpy as np

class TourOfDifferentialEquations(MovingCameraScene):
    def __init__(
        self,
        screen_rect_style=None,
        zoomed_thumbnail_index=0,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if screen_rect_style is None:
            screen_rect_style = {
                "stroke_width": 2,
                "stroke_color": WHITE,
                "fill_opacity": 1,
                "fill_color": BLACK,
            }
        self.screen_rect_style = screen_rect_style
        self.zoomed_thumbnail_index = zoomed_thumbnail_index
        self.camera.background_color = GREY_E

    def construct(self):
        self.add_title()
        self.show_thumbnails()
        self.zoom_in_to_one_thumbnail()
        # self.show_words()

    def add_title(self):
        title = Text(
            "A Tourist's Guide\nto Differential\nEquations",
            font_size=48
        )
        title.scale(1.5)
        title.to_corner(UR)
        self.add(title)

    def show_thumbnails(self):
        thumbnails = self.thumbnails = Group(
            Group(Rectangle(**self.screen_rect_style)),
            Group(Rectangle(**self.screen_rect_style)),
            Group(Rectangle(**self.screen_rect_style)),
            Group(Rectangle(**self.screen_rect_style)),
            Group(Rectangle(**self.screen_rect_style)),
        )
        n = len(thumbnails)
        thumbnails.set_height(1.5)

        line = self.line = CubicBezier(
            [-5, 3, 0],
            [3, 3, 0],
            [-3, -3, 0],
            [5, -3, 0],
        )
        line.shift(MED_SMALL_BUFF * LEFT)
        for thumbnail, a in zip(thumbnails, np.linspace(0, 1, n)):
            thumbnail.move_to(line.point_from_proportion(a))
        dots = MathTex("\\dots")
        dots.next_to(thumbnails[-1], RIGHT)

        self.add_phase_space_preview(thumbnails[0])
        self.add_heat_preview(thumbnails[1])
        self.add_fourier_series(thumbnails[2])
        self.add_matrix_exponent(thumbnails[3])
        self.add_laplace_symbol(thumbnails[4])

        self.play(
            Create(
                line,
                rate_func=lambda t: np.clip(t * (n + 1) / n, 0, 1)
            ),
            LaggedStart(*[
                GrowFromCenter(
                    thumbnail,
                    rate_func=squish_rate_func(
                        smooth,
                        0, 0.7,
                    )
                )
                for thumbnail in thumbnails
            ], lag_ratio=1),
            run_time=5
        )
        self.play(Write(dots))
        self.wait()

        self.thumbnails = thumbnails

    def zoom_in_to_one_thumbnail(self):
        self.play(
            self.camera.frame.animate.replace(
                self.thumbnails[self.zoomed_thumbnail_index]
            ),
            run_time=3,
        )
        self.wait()

    def show_words(self):
        words = VGroup(
            Text("Generalize", font_size=36),
            Text("Put in context", font_size=36),
            Text("Modify", font_size=36),
        )
        words.scale(1.5)
        words.to_corner(UR)
        words.add_to_back(Dot(words.get_center(), radius=0))
        words.add(Dot(words.get_center(), radius=0))

        diffEq = Text("Differential\nequations", font_size=36)
        diffEq.scale(1.5)
        diffEq.to_corner(DL, buff=LARGE_BUFF)

        for word1, word2 in zip(words, words[1:]):
            self.play(
                FadeIn(word2, shift=DOWN),
                FadeOut(word1, shift=UP),
            )
            self.wait()
        self.play(
            ReplacementTransform(
                VGroup(self.thumbnails).copy().set_opacity(0),
                diffEq,
                lag_ratio=0.01,
            )
        )
        self.wait()

    def add_phase_space_preview(self, thumbnail):
        # 注意：ImageMobject 在 ManimCE 中已棄用，使用 Image 替代
        # 由於無法實際載入圖片，這裡使用替代方案
        image = Rectangle(
            width=thumbnail.width,
            height=thumbnail.height,
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_width=0
        )
        image.move_to(thumbnail)
        thumbnail.add(image)

    def add_heat_preview(self, thumbnail):
        image = Rectangle(
            width=thumbnail.width,
            height=thumbnail.height,
            fill_color=RED,
            fill_opacity=0.5,
            stroke_width=0
        )
        image.move_to(thumbnail)
        thumbnail.add(image)

    def add_matrix_exponent(self, thumbnail):
        matrix = Matrix(
            [[3, 1], [4, 1]],
            v_buff=MED_LARGE_BUFF,
            h_buff=MED_LARGE_BUFF,
            bracket_h_buff=SMALL_BUFF,
            bracket_v_buff=SMALL_BUFF,
        )
        e = MathTex("e")
        t = MathTex("t")
        t.scale(1.5)
        t.next_to(matrix, RIGHT, SMALL_BUFF)
        e.scale(2)
        e.move_to(matrix.get_corner(DL), UR)
        group = VGroup(e, matrix, t)
        group.set_height(0.7 * thumbnail.get_height())
        
        # 注意：Randolph 角色在 ManimCE 中不存在，使用替代方案
        randy = SVGMobject("person", color=BLUE_C, height=0.75)
        randy.next_to(group, LEFT, aligned_edge=DOWN)
        randy.look_at(matrix)
        group.add(randy)
        group.move_to(thumbnail)
        thumbnail.add(group)

    def add_fourier_series(self, thumbnail):
        colors = [BLUE, GREEN, YELLOW, RED, RED_E, PINK]

        waves = VGroup(*[
            self.get_square_wave_approx(N, color)
            for N, color in enumerate(colors)
        ])
        waves.set_stroke(width=1.5)
        waves.replace(thumbnail, stretch=True)
        waves.scale(0.8)
        waves.move_to(thumbnail)
        thumbnail.add(waves)

    def get_square_wave_approx(self, N, color):
        return FunctionGraph(
            lambda x: sum([
                (1 / n) * np.sin(n * PI * x)
                for n in range(1, 2 * N + 3, 2)
            ]),
            x_range=[0, 2],
            color=color
        )

    def add_laplace_symbol(self, thumbnail):
        mob = MathTex(
            "\\mathcal{L}\\left\\{f(t)\\right\\}"
        )
        mob.set_width(0.8 * thumbnail.get_width())
        mob.move_to(thumbnail)
        thumbnail.add(mob)
