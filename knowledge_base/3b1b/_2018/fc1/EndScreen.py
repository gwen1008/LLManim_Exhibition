# Source: 3b1b/_2018/fc1.py
# Description: [3b1b translated] 展示一個 PiCreature 角色在標題文字下方，以不同姿勢和位置進行一系列動畫變換的結束畫面。



from manim import *
class EndScreen(PiCreatureScene):
    def __init__(self, seconds_to_blink=3, **kwargs):
        super().__init__(**kwargs)
        self.seconds_to_blink = seconds_to_blink

    def construct(self):
        words = Text("Clicky stuffs")
        words.scale(1.5)
        words.next_to(self.pi_creature, UP)
        words.to_edge(UP)

        self.play(
            FadeIn(
                words,
                run_time=2,
                lag_ratio=0.5
            ),
            self.pi_creature.animate.change_mode("hooray")
        )
        self.wait()
        mode_point_pairs = [
            ("raise_left_hand", 5 * LEFT + 3 * UP),
            ("raise_right_hand", 5 * RIGHT + 3 * UP),
            ("thinking", 5 * LEFT + 2 * DOWN),
            ("thinking", 5 * RIGHT + 2 * DOWN),
            ("thinking", 5 * RIGHT + 2 * DOWN),
            ("happy", 5 * LEFT + 3 * UP),
            ("raise_right_hand", 5 * RIGHT + 3 * UP),
        ]
        for mode, point in mode_point_pairs:
            self.play(self.pi_creature.animate.change_mode(mode).move_to(point))
            self.wait()
        self.wait(3)

    def create_pi_creature(self):
        self.pi_creature = Randolph()
        self.pi_creature.shift(2 * DOWN + 1.5 * LEFT)
        return self.pi_creature
