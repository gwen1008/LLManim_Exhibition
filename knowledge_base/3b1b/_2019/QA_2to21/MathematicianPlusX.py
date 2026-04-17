# Source: 3b1b/_2019/QA_2to21.py
# Description: [3b1b translated] 展示一段文字，內容是關於「數學家 + X」作為樂團名稱的註解。



from manim import *
class MathematicianPlusX(Scene):
    def construct(self):
        text = Tex(
            "Side note:\\\\",
            "``The Mathematician + X''\\\\",
            "would make a great band name.",
        )
        text.set_width(config.frame_width - 1)
        self.add(text)
