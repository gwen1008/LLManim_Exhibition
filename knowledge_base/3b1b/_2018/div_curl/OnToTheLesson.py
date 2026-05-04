# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示文字 "On to the lesson!" 從下方淡入並停留在畫面中央的過程。



from manim import *
class OnToTheLesson(Scene):
    def construct(self):
        words = Text("On to the lesson!")
        words.scale(1.5)
        self.play(FadeIn(words, shift=DOWN))
        self.wait()
