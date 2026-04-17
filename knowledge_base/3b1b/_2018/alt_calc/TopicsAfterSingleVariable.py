# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示三個 PiCreature 角色從隱藏狀態出現並表現出驚恐和疲憊表情，然後聚焦於複分析主題，其他主題淡出消失的過程。



from manim import *
class TopicsAfterSingleVariable(PiCreatureScene, MoreTopics):
    def __init__(self, pi_creatures_start_on_screen=False, **kwargs):
        super().__init__(pi_creatures_start_on_screen=pi_creatures_start_on_screen, **kwargs)

    def construct(self):
        MoreTopics.construct(self)
        self.show_horror()
        self.zero_in_on_complex_analysis()

    def create_pi_creatures(self):
        creatures = VGroup(*[
            PiCreature(color=color)
            for color in [BLUE_E, BLUE_C, BLUE_D]
        ])
        creatures.arrange(RIGHT, buff=LARGE_BUFF)
        creatures.scale(0.5)
        creatures.to_corner(DR)
        return creatures

    def show_horror(self):
        creatures = self.get_pi_creatures()
        modes = ["horrified", "tired", "horrified"]
        for creature, mode in zip(creatures, modes):
            creature.generate_target()
            creature.target.change(mode, self.other_topics)
        creatures.set_opacity(0)

        self.play(LaggedStartMap(MoveToTarget, creatures))
        self.wait(2)

    def zero_in_on_complex_analysis(self):
        creatures = self.get_pi_creatures()
        complex_analysis = self.other_topics[1]
        self.other_topics.remove(complex_analysis)

        self.play(
            complex_analysis.animate.scale(1.25).center().to_edge(UP),
            LaggedStartMap(FadeOut, self.other_topics),
            LaggedStartMap(FadeOut, self.lines),
            FadeOut(self.calculus),
            *[
                creature.animate.change("pondering")
                for creature in creatures
            ]
        )
        self.wait(4)
