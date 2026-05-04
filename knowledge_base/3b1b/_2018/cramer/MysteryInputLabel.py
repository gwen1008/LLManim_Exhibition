# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示一個帶有文字標籤的大括號從中心生長出來的動畫。



from manim import *
class MysteryInputLabel(Scene):
    def construct(self):
        brace = Brace(Line(ORIGIN, RIGHT), DOWN)
        text = brace.get_text("Mystery input")
        self.play(
            GrowFromCenter(brace),
            Write(text)
        )
        self.wait()
