# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 在畫面頂部顯示一個問題文字，詢問每個點是否會被無限次擊中。



from manim import *
class TheQuestion(Scene):
    def construct(self):
        words = Text(
            "Will each point be hit infinitely many times?",
            font_size=48
        )
        words.set_width(config.frame_width - 1)
        words.to_edge(UP)

        self.add(words)
