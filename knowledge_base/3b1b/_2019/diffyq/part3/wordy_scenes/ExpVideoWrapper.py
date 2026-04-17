# Source: 3b1b/_2019/diffyq/part3/wordy_scenes.py
# Description: [3b1b translated] 在灰色背景上顯示一個帶有白色邊框的圖片，並從下方淡入標題和圖片。



from manim import *
class ExpVideoWrapper(Scene):
    def construct(self):
        self.add(FullScreenFadeRectangle(
            fill_color=GREY_E,
            fill_opacity=1,
        ))

        screen = ImageMobject("eoc_chapter5_thumbnail")
        screen.set_height(6)
        rect = SurroundingRectangle(screen, buff=0)
        rect.set_stroke(WHITE, 2)
        screen.add(rect)
        title = Text("Need a refresher?")  # OldTexText -> Text
        title.scale(1.5)
        title.to_edge(UP)
        screen.next_to(title, DOWN)

        screen.center()
        self.play(
            # FadeIn(title, shift=LEFT),  # 註解掉的代碼保持原樣
            FadeIn(screen, shift=DOWN),
        )
        self.wait()
