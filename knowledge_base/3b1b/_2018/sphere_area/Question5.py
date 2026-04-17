# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個問題文字從下方淡入的場景，問題內容是關於陰影面積為何是表面積的四分之一。



from manim import *
class Question5(Scene):
    def construct(self):
        question = MathTex(
            r"""
            \text{Question \#5: Why does this imply that the }\\
            \text{shadow is }\frac{1}{4}\text{ the surface area?}
            """
        )
        self.play(FadeIn(question, shift=DOWN))
        self.wait()
