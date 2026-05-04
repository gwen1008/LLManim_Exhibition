# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示一個時鐘指針旋轉，模擬48小時時間流逝的動畫過程。



from manim import *
class PassageOfTime(Scene):
    def construct(self):
        clock = Clock()
        clock[0].set_color(BLUE)
        clock.set_stroke(width=1)
        clock.scale(0.8)
        clock.to_corner(UL)
        
        # ManimCE 中沒有 ClockPassesTime，用 Rotate 模擬時針旋轉
        # 48小時 = 24圈（每小時30度，48小時 = 1440度）
        passage = Rotate(clock.get_hands(), angle=48 * 30 * DEGREES, about_point=clock.get_center())
        
        self.play(passage, run_time=10)
