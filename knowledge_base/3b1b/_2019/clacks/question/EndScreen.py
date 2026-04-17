# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示一個帶有日期和作者標籤的影片預覽框，周圍有彩色邊框循環閃爍的動畫效果。



from manim import *
class EndScreen(Scene):
    def construct(self):
        width = (475 / 1280) * config.frame_width
        height = width * (323 / 575)
        video_rect = Rectangle(
            width=width,
            height=height,
        )
        video_rect.shift(UP)
        video_rects = VGroup(*[
            video_rect.copy().set_color(color)
            for color in [BLUE_E, BLUE_C, BLUE_D, GREY_BROWN]
        ])
        for rect in video_rects[1::2]:
            rect.reverse_points()
        video_rect.set_fill(GREY_D, 0.5)
        video_rect.set_stroke(GREY_BROWN, 0.5)
        date = Text(
            "Solution will be\n"
            "posted", "1/20/19",
        )
        date[1].set_color(YELLOW)
        date.set_width(video_rect.get_width() - 2 * MED_SMALL_BUFF)
        date.move_to(video_rect)

        handle = Text("@3blue1brown")
        handle.next_to(video_rect, DOWN, MED_LARGE_BUFF)

        self.add(video_rect, date, handle)
        for n in range(10):
            self.play(
                FadeOut(video_rects[(n - 1) % 4]),
                Create(video_rects[n % 4]),
                run_time=2,
            )
