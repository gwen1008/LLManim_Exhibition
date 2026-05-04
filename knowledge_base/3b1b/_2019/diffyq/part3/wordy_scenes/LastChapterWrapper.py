# Source: 3b1b/_2019/diffyq/part3/wordy_scenes.py
# Description: [3b1b translated] 展示一個全屏灰色背景，中央出現一個帶有白色邊框的黑色矩形，上方顯示「Last chapter」標題。



from manim import *
class LastChapterWrapper(Scene):
    def construct(self):
        full_rect = FullScreenFadeRectangle(
            fill_color=GREY_D,
            fill_opacity=1,
        )
        rect = ScreenRectangle(height=6)
        rect.set_stroke(WHITE, 2)
        rect.set_fill(BLACK, 1)
        title = Text("Last chapter")  # OldTexText -> Text
        title.scale(2)
        title.to_edge(UP)
        rect.next_to(title, DOWN)

        self.add(full_rect)
        self.play(
            FadeIn(rect),
            Write(title, run_time=2),
        )
        self.wait()
