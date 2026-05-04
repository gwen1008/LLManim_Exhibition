# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示一個角色分別指向左右兩個螢幕矩形，然後思考兩者之間的關聯。



from manim import *
class CompareTwoSituations(PiCreatureScene):
    def construct(self):
        randy = self.randy
        top_left, top_right = screens = [
            ScreenRectangle(height=3).to_corner(vect)
            for vect in (UP + LEFT, UP + RIGHT)
        ]
        arrow = DoubleArrow(*screens, buff=SMALL_BUFF)
        arrow.set_color(BLUE)

        for screen, s in zip(screens, ["left", "right"]):
            self.play(
                randy.change, f"raise_{s}_hand", screen,
                Create(screen)
            )
            self.wait(3)
        self.play(
            randy.change, "pondering", arrow,
            Create(arrow)
        )
        self.wait(2)

    def create_pi_creature(self):
        self.randy = Randolph().to_edge(DOWN)
        return self.randy
