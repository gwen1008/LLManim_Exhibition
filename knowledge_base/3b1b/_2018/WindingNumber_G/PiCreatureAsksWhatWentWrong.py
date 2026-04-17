# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 黃色 Pi 生物從困惑轉為提問，顯示「What went wrong?」文字從隱藏到出現的過程。



from manim import *
class PiCreatureAsksWhatWentWrong(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature
        randy.set_color(YELLOW_E)
        randy.flip()
        randy.to_corner(DL)
        question = Text("What went wrong?")
        question.next_to(randy, UP)
        question.shift_onto_screen()
        question.save_state()
        question.shift(DOWN).set_opacity(0)

        self.play(randy.change("erm"))
        self.wait(2)
        self.play(
            Animation(ORIGIN),
            question.animate.restore(),
            randy.change("confused"),
        )
        self.wait(5)
