# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 展示一個從原點向外擴散的閃光動畫效果。



from manim import *
class ShowFlash(Scene):
    def construct(self):
        dot = Dot(ORIGIN, color=YELLOW)
        dot.set_stroke(width=0)
        dot.set_fill(opacity=0)
        # ManimCE 使用 Flash 類別，參數名稱略有不同
        self.play(Flash(dot, flash_radius=0.8, line_length=0.6, run_time=2))
        self.wait()
