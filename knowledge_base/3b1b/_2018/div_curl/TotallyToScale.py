# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 顯示一段帶有背景矩形的文字，聲稱圖形是按比例繪製的。



from manim import *
class TotallyToScale(Scene):
    def construct(self):
        words = Text(
            "Totally drawn to scale. \\\\ Don't even worry about it.",
            font_size=48
        )
        words.set_width(config.frame_width - 1)
        words.add_background_rectangle()
        self.add(words)
        self.wait()
