# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示一個藍色卡通人物翻轉後露出驚訝表情並眨眼的動畫。



from manim import *
class Enthusiast(Scene):
    def construct(self):
        randy = Randolph(color=BLUE_C)
        randy.flip()
        self.play(randy.animate.change("surprised"))
        self.play(Blink(randy))
        self.wait()
