# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示兩個 Pi 生物討論 π 日與數學公式的對話場景，包含標題、對話氣泡和角色表情變化。



from manim import *
class ChangeTopic(PiCreatureScene):
    def construct(self):
        pi, tau = self.pi_creatures
        title = Text("Happy $\\pi$ day!")
        title.scale(1.5)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        self.add(title)

        question = MathTex(
            "\\text{Have you ever seen why }",
            "\\displaystyle \\frac{2}{1} \\cdot \\frac{2}{3} \\cdots",
            "\\frac{4}{3} \\cdot \\frac{4}{5} \\cdot",
            "\\frac{6}{5} \\cdot \\frac{6}{7} \\cdots = \\frac{\\pi}{2}",
            "?"
        )
        question[0].shift(MED_SMALL_BUFF * UP)
        question[1:4].set_color_by_gradient(YELLOW, GREEN)

        self.play(
            PiCreatureSays(
                tau, "We should \\emph{really} celebrate \\\\ on 6/28!",
                target_mode="angry",
            ),
            pi.animate.change("guilty"),
        )
        self.wait(2)
        self.play(
            PiCreatureSays(pi, question),
            RemovePiCreatureBubble(
                tau, target_mode="pondering", look_at=question,
            )
        )
        self.play(pi.animate.change("pondering", question))
        self.wait(4)

    def create_pi_creatures(self):
        tau = TauCreature(color=GREEN_E)
        pi = Randolph().flip()
        VGroup(pi, tau).scale(0.75)
        tau.to_edge(DOWN).shift(3 * LEFT)
        pi.to_edge(DOWN).shift(3 * RIGHT)
        return pi, tau
