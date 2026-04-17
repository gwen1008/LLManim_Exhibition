# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一個複數平面上的路徑經過零點，並在輸出平面上對應到原點，同時有 Pi 生物角色評論零點沒有方向性的動畫。



from manim import *
class PathContainingZero(Scene):
    def __init__(
        self,
        default_pi_creature_kwargs=None,
        default_pi_creature_start_corner=DOWN+LEFT,
        **kwargs
    ):
        super().__init__(**kwargs)
        if default_pi_creature_kwargs is None:
            default_pi_creature_kwargs = {
                "flip_at_start": False,
                "height": 1.5,
            }
        self.default_pi_creature_kwargs = default_pi_creature_kwargs
        self.default_pi_creature_start_corner = default_pi_creature_start_corner

    def construct(self):
        self.setup_planes()
        self.draw_path_hitting_zero()
        self.comment_on_zero()

    def setup_planes(self):
        # 注意：get_colorings() 和 get_planes() 方法需要從父類別繼承或自行定義
        colorings = VGroup(*self.get_colorings())
        self.input_coloring, self.output_coloring = colorings
        colorings.set_fill(opacity=0.3)

        planes = VGroup(*self.get_planes())
        self.input_plane, self.output_plane = planes
        for plane in planes:
            # plane.white_parts.set_color(BLACK)
            plane.lines_to_fade.set_stroke(width=0)

        v_line = Line(UP, DOWN).scale(FRAME_Y_RADIUS)
        v_line.set_stroke(WHITE, 5)

        self.add(colorings, planes)
        self.add(v_line)

    def draw_path_hitting_zero(self):
        morty = self.pi_creature

        path = self.path = VMobject(
            stroke_width=5,
            stroke_color=WHITE,
            fill_opacity=0,
        )
        # 注意：match_background_image_file 方法在 ManimCE 中不存在
        # 這裡假設它是設置背景圖像的方法，用 set_background_image 替代
        path.set_background_image(self.input_coloring)
        path.set_points_smoothly([
            self.input_plane.coords_to_point(x, y)
            for x, y in [(1, 2.5), (2.5, 2.5), (2, 0.5), (1, 1), (0.5, 1), (0.5, 2), (1, 2.5)]
        ])

        out_path = self.out_path = path.copy()
        out_path.apply_function(self.point_function)
        out_path.set_background_image(self.output_coloring)
        out_path.make_smooth()

        self.play(
            Flash(
                VectorizedPoint(self.output_plane.coords_to_point(0, 0)),
                color=WHITE,
                flash_radius=0.3,
                line_length=0.2,
                num_lines=13,
                rate_func=lambda t: squish_rate_func(smooth, 0.5, 0.6)(t),
            ),
            morty.animate.change("pondering"),
            *[
                Create(mob, rate_func=lambda t: bezier([0, 0, 1, 1])(t))
                for mob in (path, out_path)
            ],
            run_time=5
        )

    def comment_on_zero(self):
        morty = self.pi_creature

        words = Text(
            "Output is zero\nwhich has no direction",
            font_size=36
        )
        origin = self.output_plane.coords_to_point(0, 0)
        words.to_edge(DOWN, buff=LARGE_BUFF)
        background_rect = BackgroundRectangle(
            words, buff=SMALL_BUFF,
            fill_opacity=1.0
        )
        background_rect.stretch_to_fit_width(0.1)

        arrow = Arrow(words.get_top(), origin)

        circles = VGroup()
        for point in [self.input_plane.coords_to_point(1, 1), origin]:
            circle = Circle(color=BLACK, radius=0.5, stroke_width=0)
            circle.move_to(point)
            circle.generate_target()
            circle.target.scale(0)
            circle.target.set_stroke(width=4)
            circles.add(circle)
        in_circle, out_circle = circles

        new_words = Text(
            "But we want x\nwhere f(x) = 0",
            font_size=36
        )
        new_words.move_to(words)

        self.play(
            FadeIn(background_rect),
            Write(words[0]),
            GrowArrow(arrow),
        )
        self.play(
            Write(words[1]),
            morty.animate.change("pleading"),
            MoveToTarget(out_circle, run_time=2)
        )
        self.wait()
        self.play(FadeOut(words))
        self.play(
            FadeIn(new_words),
            morty.animate.change("happy")
        )
        self.play(MoveToTarget(in_circle, run_time=2))
        self.play(morty.animate.change("hooray"))
        self.wait(3)

    # 以下方法需要從原父類別繼承或自行定義
    def get_colorings(self):
        # 返回輸入和輸出的著色對象
        pass

    def get_planes(self):
        # 返回輸入和輸出平面
        pass

    @property
    def pi_creature(self):
        # 返回 Pi 生物角色
        pass

    def point_function(self, point):
        # 定義點轉換函數
        pass
