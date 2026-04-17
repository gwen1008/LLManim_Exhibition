# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示一個 PiCreature 角色指向 Brilliant.org 網址，並在思考後開心地再次指向網址的動畫場景。



from manim import *
class Promotion(PiCreatureScene):
    def __init__(self, seconds_to_blink=5, **kwargs):
        super().__init__(**kwargs)
        self.seconds_to_blink = seconds_to_blink

    def construct(self):
        url = Text("https://brilliant.org/3b1b/", font_size=36)
        url.to_corner(UP + LEFT)

        rect = Rectangle(height=9, width=16)
        rect.set_height(5.5)
        rect.next_to(url, DOWN)
        rect.to_edge(LEFT)

        self.play(
            Write(url),
            self.pi_creature.animate.change("raise_right_hand")
        )
        self.play(Create(rect))
        self.wait(2)
        self.pi_creature.animate.change("thinking")
        self.wait()
        self.pi_creature.animate.look_at(url)
        self.wait(10)
        self.pi_creature.animate.change("happy")
        self.wait(10)
        self.pi_creature.animate.change("raise_right_hand")
        self.wait(10)

        self.remove(rect)
        self.play(
            url.animate.next_to(self.pi_creature, UP + LEFT)
        )
        url_rect = SurroundingRectangle(url)
        self.play(Create(url_rect))
        self.play(FadeOut(url_rect))
        self.wait(3)
