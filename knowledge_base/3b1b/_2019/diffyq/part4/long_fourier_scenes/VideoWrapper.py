# Source: 3b1b/_2019/diffyq/part4/long_fourier_scenes.py
# Description: [3b1b translated] 展示一個帶有動態邊界的灰色背景屏幕矩形，上方有標題文字淡入。



from manim import *
class VideoWrapper(Scene):
    def construct(self):
        fade_rect = FullScreenFadeRectangle()
        fade_rect.set_fill(GREY_D, 1)
        screen_rect = ScreenRectangle()
        screen_rect.set_height(4)
        screen_rect.set_fill(BLACK, 1)
        screen_rect.set_stroke(width=0)

        boundary = AnimatedBoundary(screen_rect)

        title = Text("Learn the math")
        title.scale(1.5)
        title.next_to(screen_rect, UP)

        self.add(fade_rect)
        self.add(screen_rect)
        self.add(boundary)

        self.play(FadeIn(title, shift=DOWN))
        self.wait(19)
