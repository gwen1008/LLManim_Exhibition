# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示一個帶有 Minute Physics 標誌和標題的場景，並在標題下方創建一個螢幕矩形。



from manim import *
class MinutPhysicsWrapper(Scene):
    def construct(self):
        logo = ImageMobject("minute_physics_logo", invert=True)
        logo.to_corner(UP + LEFT)
        self.add(logo)

        title = Tex("Minute Physics on special relativity")
        title.to_edge(UP).shift(MED_LARGE_BUFF * RIGHT)

        screen_rect = ScreenRectangle()
        screen_rect.set_width(title.get_width() + LARGE_BUFF)
        screen_rect.next_to(title, DOWN)

        self.play(Create(screen_rect))
        self.play(Write(title))
        self.wait(2)
