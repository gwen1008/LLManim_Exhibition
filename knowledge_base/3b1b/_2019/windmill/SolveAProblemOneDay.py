# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示一個 PiCreature 角色思考問題，然後出現燈泡靈感，最後燈泡發光的動畫過程。



from manim import *
class SolveAProblemOneDay(SpiritOfIMO, PiCreatureScene):
    def construct(self):
        randy = self.pi_creature
        light_bulb = Lightbulb()
        light_bulb.base = light_bulb[:3]
        light_bulb.light = light_bulb[3:]
        light_bulb.set_height(1)
        light_bulb.next_to(randy, UP, buff=MED_LARGE_BUFF)

        light = self.get_light(light_bulb.get_center())

        bubble = ThoughtBubble()
        bubble.pin_to(randy)

        you = Text("You")
        you.scale(1.5)
        arrow = Vector(LEFT)
        arrow.next_to(randy, RIGHT)
        you.next_to(arrow)

        self.play(
            Create(bubble),
            randy.animate.change("pondering"),
        )
        self.play(
            FadeIn(you, shift=LEFT),
            GrowArrow(arrow)
        )
        self.wait(2)
        self.play(
            FadeIn(light_bulb, shift=DOWN),
            randy.animate.change("hooray"),
        )
        self.play(
            LaggedStartMap(
                VFadeInThenOut, light,
                run_time=2
            ),
            randy.animate.change("thinking", light),
        )
        self.wait(2)
