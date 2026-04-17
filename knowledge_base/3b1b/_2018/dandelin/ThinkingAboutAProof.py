# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示一個思考數學證明的 PiCreature 角色，帶有思想泡泡和文字標籤的動畫。



from manim import *
class ThinkingAboutAProof(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature
        randy.scale(0.5, about_edge=DL)
        bubble = ThoughtBubble()
        bubble.pin_to(randy)
        bubble.shift(MED_SMALL_BUFF * RIGHT)
        cloud = bubble[-1]
        cloud.rotate(90 * DEGREES)
        cloud.set_height(FRAME_HEIGHT - 0.5)
        cloud.stretch(2.8, 0)
        cloud.next_to(bubble[2], RIGHT)
        cloud.to_edge(UP, buff=0.25)
        bubble[1].shift(0.25 * UL)

        you_arrow = Arrow(start=RIGHT, end=LEFT, color=WHITE)
        you_arrow.next_to(randy, RIGHT)
        you = Text("You")
        you.next_to(you_arrow, RIGHT)
        lm_arrow = Arrow(start=UP, end=DOWN, color=WHITE)
        lm_arrow.next_to(randy, UP)
        love_math = Text("Love math")
        love_math.next_to(lm_arrow, UP)
        love_math.shift_onto_screen()

        self.add(bubble)
        self.play(
            FadeIn(you, shift=LEFT),
            GrowArrow(you_arrow),
        )
        self.play(
            FadeIn(love_math, shift=DOWN),
            GrowArrow(lm_arrow),
            randy.animate.change("erm")
        )
        self.wait(2)
        self.play(
            randy.animate.change("pondering", cloud)
        )
        self.wait(10)
