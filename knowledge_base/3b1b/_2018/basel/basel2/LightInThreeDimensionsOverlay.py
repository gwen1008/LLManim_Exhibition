# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示文字「立體角（以立體弧度為單位）」的寫入動畫。



from manim import *
class LightInThreeDimensionsOverlay(Scene):
    def construct(self):
        words = MathTex(r"""
            \text{``Solid angle''} \\
            \text{(measured in ``steradians'')}
        """)
        self.play(Write(words))
        self.wait()
