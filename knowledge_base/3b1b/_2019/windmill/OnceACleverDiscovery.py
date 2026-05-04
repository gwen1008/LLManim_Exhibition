# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示一個帶有黃色箭頭和矩形框的「energy」文字，以及從上方淡入的黃色標題文字。



from manim import *
class OnceACleverDiscovery(Scene):
    def construct(self):
        energy = Text("energy")
        rect = SurroundingRectangle(energy)
        words = Text("Once a clever discovery")
        vect = Vector(DR)
        vect.next_to(rect.get_top(), UL, buff=SMALL_BUFF)
        words.next_to(vect.get_start(), UP)
        words.set_color(YELLOW)
        vect.set_color(YELLOW)

        self.play(
            Create(vect),
            Create(rect),
        )
        self.play(FadeIn(words, shift=DOWN))
        self.wait()
