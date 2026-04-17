# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 兩個藍色卡通人物困惑地看著上方一排男女圖標不斷隨機交換位置，表達對排列順序的疑問。


from manim import *
import random

class StudentsGetConfused(PiCreatureScene):
    def construct(self):
        pi1, pi2 = self.pi_creatures
        line = VGroup(
            Male(), Female(), Female(), Male(), Female()
        )
        width = line.get_width()
        for i, mob in enumerate(line):
            mob.shift((i*width+SMALL_BUFF)*RIGHT)
        line.scale(1.5)
        line.arrange(RIGHT, SMALL_BUFF)
        line.move_to(self.pi_creatures, UP)

        self.add(line)
        self.play(
            self.get_shuffle_anim(line),
            PiCreatureSays(
                pi1, "Wait \\dots order matters now?",
                target_mode = "confused",
                look_at = line
            )
        )
        self.play(
            self.get_shuffle_anim(line),
            *[
                ApplyMethod(pi.change, "confused", line)
                for pi in self.pi_creatures
            ]
        )
        for x in range(4):
            self.play(self.get_shuffle_anim(line))
        self.wait()

    def create_pi_creatures(self):
        pis = VGroup(*[
            Randolph(color = color)
            for color in (BLUE_D, BLUE_B)
        ])
        pis[1].flip()
        pis.arrange(RIGHT, buff = 5)
        pis.to_edge(DOWN)
        return pis

    def get_shuffle_anim(self, line):
        indices = list(range(len(line)))
        random.shuffle(indices)
        line.generate_target()
        for i, m in zip(indices, line.target):
            m.move_to(line[i])
        return MoveToTarget(line, path_arc = PI)
