# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個 PiCreature 角色從思考、猶豫、俏皮到生氣的一系列表情變化。



from manim import *
class ThinkingCritically(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature

        self.play(randy.animate.change("pondering"))
        self.wait()
        self.play(
            randy.animate.change("hesitant", 2 * UP),
        )
        self.wait()
        self.play(randy.animate.change("sassy"))
        self.wait()
        self.play(randy.animate.change("angry"))
        self.wait(4)
