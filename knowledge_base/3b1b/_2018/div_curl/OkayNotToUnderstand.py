# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示一個困惑的 Morty 角色和一段文字，文字內容是「現在不理解這個也沒關係」。



from manim import *
class OkayNotToUnderstand(Scene):
    def construct(self):
        words = Text(
            "It's okay not to\nunderstand this just yet.",
            font_size=48
        )
        morty = Mortimer()
        morty.change("confused")
        words.next_to(morty, UP)
        self.add(morty, words)
