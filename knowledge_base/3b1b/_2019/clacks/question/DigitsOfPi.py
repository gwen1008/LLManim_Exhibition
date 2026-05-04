# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示圓周率 π 的小數位數逐漸顯示，同時旁邊有一個黃色卡通人物眨眼。



from manim import *
class DigitsOfPi(Scene):
    def __init__(self, n_digits=9, **kwargs):
        super().__init__(**kwargs)
        self.n_digits = n_digits

    def construct(self):
        nd = self.n_digits
        pow10 = int(10**nd)
        rounded_pi = int(pow10 * PI) / pow10
        equation = MathTex(
            ("\\pi = {:." + str(nd) + "f}...").format(rounded_pi)
        )
        equation.set_color(YELLOW)
        pi_creature = Randolph(color=YELLOW)
        pi_creature.match_width(equation[0])
        pi_creature.scale(1.4)
        pi_creature.move_to(equation[0], DOWN)
        self.add(pi_creature, equation[1])
        self.play(ShowIncreasingSubsets(
            equation[2:],
            rate_func=linear,
            run_time=1,
        ))
        self.play(Blink(pi_creature))
        self.wait()
