# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示綠色字母 "i" 與 "· w" 組成的數學公式被書寫出來的過程。



from manim import *
class WriteITimesW(Scene):
    def construct(self):
        mob = MathTex("i", "\\cdot", "w")
        mob[0].set_color(GREEN)
        mob.scale(3)
        self.play(Write(mob))
        self.wait()
