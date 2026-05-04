# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示一個 PiCreature 角色先說出一句話，然後轉變為思考表情的動畫過程。



from manim import *
class AskQuestionOfGraph(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature

        self.pi_creature_says(
            randy,
            "What sine waves\\\\are you made of?",
            target_mode="sassy",
        )
        self.wait(2)
        self.play(
            randy.animate.change("pondering"),
            randy.bubble.animate.get_right()
        )
        self.wait(2)
