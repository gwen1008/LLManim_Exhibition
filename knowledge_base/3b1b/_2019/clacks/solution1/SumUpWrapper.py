# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示一個總結標題和一個黑色螢幕矩形從上方淡入的場景，背景為半透明灰色。



from manim import *
class SumUpWrapper(Scene):
    def construct(self):
        title = Text("To sum up:", font_size=72)  # OldTexText -> Text, scale 1.5 改用 font_size
        title.to_edge(UP)
        screen_rect = Rectangle(height=6, width=16/9*6)  # ScreenRectangle 用 Rectangle 替代，設定寬高比
        screen_rect.set_fill(BLACK, opacity=1)
        screen_rect.next_to(title, DOWN)
        
        # FullScreenFadeRectangle 用 Rectangle 填滿整個畫面替代
        background_rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=GREY_D,
            fill_opacity=0.5,
            stroke_width=0
        )
        self.add(background_rect)
        
        self.play(
            FadeIn(title, shift=DOWN),  # FadeInFromDown -> FadeIn with shift
            FadeIn(screen_rect),
        )
        self.wait()
