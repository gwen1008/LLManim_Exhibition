# Source: 3b1b/_2018/eop/chapter1/show_uncertainty_dice.py
# Description: [3b1b translated] 展示骰子隨機擲出點數的動畫，模擬不確定性過程。



from manim import *
class ShowUncertaintyDice(Scene):

    def throw_a_die(self, run_time=0.3):
        eye = np.random.randint(1, 7)
        face = self.row_of_dice.submobjects[eye - 1]
        
        self.play(
            face.submobjects[0].animate.set_opacity(1),
            rate_func=there_and_back,
            run_time=run_time,
        )

    def construct(self):
        self.row_of_dice = RowOfDice(direction=DOWN).scale(0.5)
        self.add(self.row_of_dice)

        for i in range(5):
            self.throw_a_die()
            self.wait(1)

        for i in range(10):
            self.throw_a_die()
            self.wait(0.3)

        for i in range(100):
            self.throw_a_die(0.05)
            self.wait(0.0)
