# Source: 3b1b/_2019/diffyq/part2/pi_scenes.py
# Description: [3b1b translated] 展示一個藍色 PiCreature 角色對熱方程式的反應，從驚恐到思考再到困惑，最後又回到驚恐的動畫過程。



from manim import *
class ReactionsToInitialHeatEquation(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature
        randy.set_color(BLUE_C)
        randy.center()

        point = Dot(radius=0).next_to(randy, UL, LARGE_BUFF)
        randy.add_updater(lambda r: r.look_at(point))

        self.play(randy.animate.change("horrified"))
        self.wait()
        self.play(randy.animate.change("pondering"))
        self.wait()
        self.play(
            randy.animate.change("confused"),
            point.animate.next_to(randy, UR, LARGE_BUFF),
        )
        self.wait(2)
        self.play(
            point.animate.shift(2 * DOWN),
            randy.animate.change("horrified")
        )
        self.wait(4)
