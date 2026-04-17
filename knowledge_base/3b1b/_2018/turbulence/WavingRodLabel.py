# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一個文字標籤寫出「在空中揮舞小旗子」的動畫。



from manim import *
class WavingRodLabel(Scene):
    def construct(self):
        words = Text("(Waving a small flag\nthrough the air)")
        self.play(Write(words))
        self.wait()
