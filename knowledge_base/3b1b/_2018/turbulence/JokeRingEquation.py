# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一個帶有文字項目的清單，並用箭頭連接前兩個項目到一個點，逐步淡入和創建動畫。



from manim import *
class JokeRingEquation(Scene):
    def construct(self):
        items = VGroup(
            Text("Container with a lip"),
            Text("Fill with smoke (or fog)"),
            Text("Hold awkwardly"),
        )
        line = Line(LEFT, RIGHT).set_width(items.get_width() + 1)
        items.add(line)
        items.add(Text("Vortex ring"))
        items.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        line.shift(LEFT)
        plus = MathTex("+")
        plus.next_to(line.get_left(), UR, buff=SMALL_BUFF)
        line.add(plus)
        items.to_edge(RIGHT)

        point = 3.8 * LEFT + 0.2 * UP
        arrow1 = Arrow(
            items[0].get_left(), point + 0.8 * UP + 0.3 * RIGHT,
            path_arc=90 * DEGREES,
        )
        arrow1.pointwise_become_partial(arrow1, 0, 0.99)

        arrow2 = Arrow(
            items[1].get_left(), point,
        )
        arrows = VGroup(arrow1, arrow2)

        for i in 0, 1:
            self.play(
                FadeIn(items[i], shift=DOWN),
                Create(arrows[i])
            )
            self.wait()
        self.play(LaggedStart(*[FadeIn(item) for item in items[2:]]))
        self.wait()
        self.play(FadeOut(arrows))
        self.wait()
