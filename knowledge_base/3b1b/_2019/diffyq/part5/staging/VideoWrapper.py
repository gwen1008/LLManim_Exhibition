# Source: 3b1b/_2019/diffyq/part5/staging.py
# Description: [3b1b translated] 展示兩個並排的螢幕矩形，帶有動態邊界和標題文字，在灰色背景上淡入。



from manim import *
class VideoWrapper(Scene):
    def construct(self):
        fade_rect = FullScreenFadeRectangle()
        fade_rect.set_fill(GREY_D, 1)
        screen_rects = VGroup(
            ScreenRectangle(),
            ScreenRectangle(),
        )
        screen_rects.set_height(3)
        screen_rects.set_fill(BLACK, 1)
        screen_rects.set_stroke(width=0)
        screen_rects.arrange(RIGHT, buff=LARGE_BUFF)
        screen_rects.shift(1.25 * UP)

        boundary = VGroup(*map(AnimatedBoundary, screen_rects))

        titles = VGroup(
            Text("Want more?"),
            Text("Learn calculus"),
        )
        titles.scale(1.5)
        for rect, title in zip(screen_rects, titles):
            title.next_to(rect, UP)

        self.add(fade_rect)
        self.add(screen_rects)

        self.add(boundary[0])
        self.play(FadeIn(titles[0], shift=DOWN))
        self.add(boundary[1])
        self.play(FadeIn(titles[1], shift=DOWN))
        self.wait(18)
