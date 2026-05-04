# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個矩形在拉伸變形過程中，其寬度和高度分別乘以不同比例係數的視覺效果，並與旋轉後的矩形進行對比。



from manim import *
class SameEffectAsRotating(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rectangle_config = {
            "height": 2,
            "width": 1,
            "stroke_width": 0,
            "fill_color": YELLOW,
            "fill_opacity": 1,
            "stroke_width": 2,
            "stroke_color": BLACK,
        }
        self.x_stretch = 2
        self.y_stretch = 0.5

    def construct(self):
        rect1 = Rectangle(**self.rectangle_config)
        rect2 = rect1.copy()
        rect2.stretch(self.x_stretch, 0)
        rect2.stretch(self.y_stretch, 1)
        rotated_rect1 = rect1.copy()
        rotated_rect1.rotate(-90 * DEGREES)

        arrow = Arrow(ORIGIN, RIGHT, buff=0, color=WHITE)
        group = VGroup(rect1, arrow, rect2)
        group.arrange(RIGHT)
        group.center()
        moving_rect = rect1.copy()

        low_brace = always_redraw(
            lambda: Brace(
                moving_rect, DOWN, buff=SMALL_BUFF,
                min_num_quads=2,
            )
        )
        right_brace = always_redraw(
            lambda: Brace(
                moving_rect, RIGHT, buff=SMALL_BUFF,
                min_num_quads=2,
            )
        )
        times_R_over_d = MathTex("\\times \\frac{R}{d}")
        times_d_over_R = MathTex("\\times \\frac{d}{R}")
        times_R_over_d.add_updater(
            lambda m: m.next_to(low_brace, DOWN, SMALL_BUFF)
        )
        times_d_over_R.add_updater(
            lambda m: m.next_to(right_brace, RIGHT, SMALL_BUFF)
        )

        self.add(rect1, arrow)
        self.play(moving_rect.animate.move_to(rect2))
        self.add(low_brace)
        self.play(
            moving_rect.animate.match_width(rect2, stretch=True),
            FadeIn(times_R_over_d),
        )
        self.add(right_brace)
        self.play(
            moving_rect.animate.match_height(rect2, stretch=True),
            FadeIn(times_d_over_R),
        )
        self.wait()
        rotated_rect1.move_to(moving_rect)
        self.play(TransformFromCopy(
            rect1, rotated_rect1,
            path_arc=-90 * DEGREES,
            run_time=2
        ))
