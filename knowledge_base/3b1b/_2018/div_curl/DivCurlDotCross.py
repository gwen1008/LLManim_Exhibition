# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示四個標題為「散度」、「旋度」、「點積」、「叉積」的矩形排列成兩行兩列的網格佈局。



from manim import *
class DivCurlDotCross(Scene):
    def construct(self):
        rects = VGroup(*[
            ScreenRectangle(height=2.5)
            for n in range(4)
        ])
        rects.arrange_in_grid(n_rows=2, buff=LARGE_BUFF)
        rects[2:].shift(MED_LARGE_BUFF * DOWN)
        titles = VGroup(*list(map(Text, [
            "Divergence", "Curl",
            "Dot product", "Cross product"
        ])))
        for title, rect in zip(titles, rects):
            title.next_to(rect, UP)

        self.add(rects, titles)
