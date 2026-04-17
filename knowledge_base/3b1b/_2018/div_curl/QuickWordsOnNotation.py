# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示標題文字從上方淡入的動畫效果。



from manim import *
class QuickWordsOnNotation(Scene):
    def construct(self):
        words = Text("Quick words on notation:")
        words.scale(1.5)
        self.play(FadeIn(words, shift=DOWN))
        self.wait()
