# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一個名為 Randy 的角色從驚訝表情到眨眼、向上看，再來回向右看的動畫過程。



from manim import *
class PiCreatureInAwe(Scene):
    def construct(self):
        randy = Randolph()

        self.play(randy.animate.change("awe"))
        self.play(Blink(randy))
        self.play(randy.animate.look(UP), run_time=2)
        self.play(
            randy.animate.look(RIGHT),
            run_time=4,
            rate_func=there_and_back,
            path_arc=-TAU/4
        )
        self.wait()
