# Source: 3b1b/_2019/diffyq/part3/wordy_scenes.py
# Description: [3b1b translated] 展示一個文字物件，包含「Flat at boundary」和數學符號 t > 0 的組合。



from manim import *
class FlatAtBoundaryWords(Scene):
    def construct(self):
        words = self.get_bc_words()
        self.play(Write(words))
        self.wait()

    def get_bc_words(self):
        return MathTex(
            "\\text{Flat at boundary}\\\\",
            "\\text{for all }",
            "t",
            "> 0",
        )
