# Source: 3b1b/_2019/clacks/solution2/simple_scenes.py
# Description: [3b1b translated] 展示一個帶有標題和灰色背景的包裝場景，其中包含一個黑色螢幕矩形。



from manim import *
class WrapperScene(Scene):
    def __init__(self, title="Title", shade_of_grey="#333333", **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.shade_of_grey = shade_of_grey

    def construct(self):
        title = Text(self.title)
        title.scale(1.5)
        title.to_edge(UP)
        big_rect = self.get_big_rect()
        screen_rect = self.get_screen_rect()
        screen_rect.next_to(title, DOWN)

        self.add(big_rect, screen_rect)
        self.play(
            FadeIn(big_rect),
            FadeIn(title, shift=DOWN),
            FadeIn(screen_rect, shift=UP),
        )
        self.wait()

    def get_big_rect(self):
        big_rect = FullScreenFadeRectangle()
        big_rect.set_fill(self.shade_of_grey, 1)
        return big_rect

    def get_screen_rect(self, height=6):
        screen_rect = ScreenRectangle(height=height)
        screen_rect.set_fill(BLACK, 1)
        return screen_rect
