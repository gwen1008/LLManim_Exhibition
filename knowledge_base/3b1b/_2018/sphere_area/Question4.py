# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個問題標題和內容的漸入動畫，其中特定詞彙以不同顏色標示。



from manim import *
class Question4(Scene):
    def construct(self):
        question = MathTex(
            r"\text{Question \#4:}",
            r"\text{Explain how the shadows relate to}\\\\"
            r"\text{every other ring on the sphere.}",
            tex_to_color_map={
                r"\text{shadows}": YELLOW,
                r"\text{every other ring}": BLUE,
            }
        )

        self.add(question[0])
        self.wait()
        self.play(FadeIn(question[1:], shift=DOWN))
        self.wait()
