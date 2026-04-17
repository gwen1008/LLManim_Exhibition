# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示文字 "Seek order amidst chaos" 以書寫動畫出現。



from manim import *
class SeekOrderWords(Scene):
    def construct(self):
        words = Text("Seek order amidst chaos")
        words.scale(1.5)
        self.play(Write(words))
        self.wait()
