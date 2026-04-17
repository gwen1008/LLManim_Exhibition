# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示 Mathologer 影片標題和 Logo 從畫面外滑入，並創建一個代表影片播放的矩形螢幕。



from manim import *
class MathologerVideoWrapper(Scene):
    def construct(self):
        title = Text(
            "Mathologer's excellent video on\nthe many Pythagorean theorem cousins",
            font_size=36
        )
        title.to_edge(UP)
        
        # 注意：ImageMobject 在 ManimCE 中改為 Image
        # 假設圖片檔案名為 "mathologer_logo.png" 並放在 assets 資料夾
        logo = Image("mathologer_logo.png")
        logo.height = 1
        logo.to_corner(UP + LEFT)
        logo.shift(FRAME_WIDTH * RIGHT)
        
        screen = ScreenRectangle(height=5.5)
        screen.next_to(title, DOWN)

        # 動畫：logo 從右側滑入，標題淡入
        self.play(
            logo.animate.shift(FRAME_WIDTH * LEFT),
            LaggedStart(*[FadeIn(word) for word in title]),
            run_time=2
        )
        self.play(Create(screen))
        self.wait(5)
