# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示一個黃色文字 "In radians" 被寫出，同時一個包圍著 theta 符號的方框淡出。



from manim import *
class WriteInRadians(Scene):
    def construct(self):
        words = Text("In radians")
        words.set_color(YELLOW)
        square = SurroundingRectangle(MathTex("\\theta"))
        square.next_to(words, UP)
        self.play(Create(square))
        self.play(Write(words), FadeOut(square))
        self.wait()
