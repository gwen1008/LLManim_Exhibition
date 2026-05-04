# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示三個數字（3、7、9）分別以不同顏色從上方淡入的動畫過程。



from manim import *
class InsertNewResidueClasses(Scene):
    def construct(self):
        nums = VGroup(*map(Integer, [3, 7, 9]))
        colors = [GREEN, TEAL, BLUE]
        for num, color in zip(nums, colors):
            num.set_color(color)
            num.add_background_rectangle(buff=SMALL_BUFF, opacity=1)
            self.play(FadeIn(num, shift=UP))
            self.wait()
