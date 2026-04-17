# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示一個標題文字動畫，其中關鍵洞察部分以黃色強調，文字從上方淡入。



from manim import *
class InsightNumber1(Scene):
    def construct(self):
        words = MathTex(
            "\\text{Key insight 1: }",
            "\\text{\\# Points on either side is constant}"
        )
        words[0].set_color(YELLOW)
        words.set_width(config.frame_width - 1)
        self.play(FadeIn(words, shift=DOWN))
        self.wait()
