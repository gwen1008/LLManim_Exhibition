# Source: 3b1b/_2019/moduli.py
# Description: [3b1b translated] 展示製作人員名單，從底部開始顯示版權資訊，然後從下方淡入作者和插畫師資訊。



from manim import *
class Credits(Scene):
    def construct(self):
        items = VGroup(
            Text("Written by\nJayadev Athreya"),
            Text("Illustrated and Narrated by\nGrant Sanderson"),
            Text(
                "3Blue1Brown\n"
                "\\copyright {} Copyright 2019\n"
                "www.3blue1brown.com\n"
            ),
        )
        items.arrange(DOWN, buff=LARGE_BUFF)

        items[-1].set_color(GREY_B)
        items[-1].scale(0.8, about_edge=UP)
        items[-1].to_edge(DOWN)

        self.add(items[-1])
        self.play(LaggedStart(
            *[FadeIn(item, shift=DOWN) for item in items[:-1]],
            lag_ratio=0.5
        ))
        self.wait()
