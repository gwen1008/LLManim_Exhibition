# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示一個推薦 Mathologer 影片的標題和螢幕矩形，背景為灰色。



from manim import *
class RecommendedMathologerVideo(Scene):
    def construct(self):
        full_rect = FullScreenFadeRectangle()
        full_rect.set_fill(GREY_D, 1)
        self.add(full_rect)

        title = Text("Recommended Mathologer video")
        title.set_width(config.frame_width - 1)
        title.to_edge(UP)
        screen_rect = SurroundingRectangle(ScreenRectangle(height=5.9), buff=SMALL_BUFF)
        screen_rect.next_to(title, DOWN)
        screen_rect.set_fill(BLACK, 1)
        screen_rect.set_stroke(WHITE, 3)

        self.add(screen_rect)
        self.play(Write(title))
        self.wait()
