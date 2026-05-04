# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示一個藍色 PiCreature 角色從下方淡入，思考並顯示「...why?」文字，然後出現思考泡泡的動畫過程。



from manim import *
class AskAboutWhyYouWouldAddSpheres(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature
        randy.flip()
        randy.set_height(2)
        randy.set_color(BLUE_C)
        randy.to_edge(RIGHT)
        randy.shift(2 * UP)
        randy.look(UP)

        graph_spot = VectorizedPoint()

        why = Text("...why?")
        why.next_to(randy, UP)

        bubble = ThoughtBubble(height=2, width=2)
        bubble.pin_to(randy)

        self.play(FadeIn(randy, shift=DOWN))
        self.play(
            Animation(graph_spot),
            randy.animate.change("maybe"),
            Write(why),
        )
        self.wait(3)
        self.play(randy.animate.change("pondering"))
        self.play(
            why.animate.to_corner(DR),
            why.animate.set_fill(GREY_B, 0.5),
        )
        self.wait()
        self.play(
            Create(bubble),
            randy.animate.change("thinking")
        )
        self.wait()
        self.look_at(graph_spot)
        self.wait(2)
