# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示一個 PiCreature 角色試圖回憶證明過程，帶有思考表情和文字對話框的動畫。



from manim import *
class TryToRememberProof(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature

        words = Text("Oh god...how\ndid it go?")  # OldTexText -> Text
        words.next_to(randy, UP)
        words.shift_onto_screen()

        # FadeInFromDown -> FadeIn with shift
        self.play(
            randy.change, "telepath",
            FadeIn(words, shift=DOWN)
        )
        self.look_at(ORIGIN)
        self.wait(2)
        self.play(randy.change, "concerned_musician")
        self.look_at(ORIGIN)
        self.wait(3)
