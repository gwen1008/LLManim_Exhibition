# Source: 3b1b/_2018/quat3d.py
# Description: [3b1b translated] 展示一個帶有背景矩形和藍色邊框的文字，以及一個綠色箭頭在文字上方反覆縮放的動畫效果。



from manim import *
class Link(Scene):
    def construct(self):
        # 使用 Text 替代 OldTexText，並添加背景矩形
        word = Text("eater.net/quaternions")
        # 在 ManimCE 中，Text 沒有 add_background_rectangle 方法
        # 改用 SurroundingRectangle 並設置填充色來模擬背景
        word_bg = SurroundingRectangle(word, color=WHITE, fill_color=BLACK, fill_opacity=1, buff=0.1)
        # 將背景矩形置於文字下方
        word_bg.z_index = -1
        word_group = VGroup(word_bg, word)
        
        rect = SurroundingRectangle(word_group, color=BLUE)
        arrow = Arrow(start=ORIGIN, end=UR, color=GREEN, buff=0)
        arrow.next_to(rect, UP)
        arrow.align_to(rect, RIGHT)
        short_arrow = arrow.copy().scale(0.8, about_edge=DL)

        self.add(word_group)
        self.play(
            Create(rect),
            GrowArrow(arrow),
        )
        for x in range(10):
            self.play(Transform(
                arrow, short_arrow,
                rate_func=there_and_back,
                run_time=2
            ))
