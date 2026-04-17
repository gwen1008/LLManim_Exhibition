# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示一個灰色棕色的 PiCreature 角色說出 "What will happen?" 並帶有疑問表情的場景。



from manim import *
class AskWhatWillHappen(PiCreatureScene):
    def construct(self):
        morty = self.pi_creature
        morty.set_color(GREY_BROWN)

        self.pi_creature_says(
            "What will\\\\"
            "happen?",
            target_mode="maybe",
            look_at=4 * DR,
        )
        self.wait(3)
