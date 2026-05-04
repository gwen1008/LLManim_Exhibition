# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示一個從原點到右側的線段下方出現大括號，並伴隨文字「Air resistance」從上方淡入的動畫。



from manim import *
class AirResistanceBrace(Scene):
    def construct(self):
        brace = Brace(Line(ORIGIN, RIGHT), DOWN)
        word = Text("Air resistance")
        word.next_to(brace, DOWN)
        self.play(GrowFromCenter(brace), FadeIn(word, shift=UP))
        self.wait()
