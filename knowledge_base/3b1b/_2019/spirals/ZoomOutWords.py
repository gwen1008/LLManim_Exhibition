# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示文字 "Zoom out!" 以縮放淡入的方式出現，然後停留片刻。



from manim import *
class ZoomOutWords(Scene):
    def construct(self):
        words = Text("Zoom out!")
        words.scale(3)
        self.play(FadeIn(words, scale=0.1))  # FadeInFromLarge 替換為 FadeIn 並指定 scale 參數
        self.wait()
