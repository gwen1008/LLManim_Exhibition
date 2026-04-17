# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個問題文字從上方淡入的場景，問題內容涉及計算圓環陰影的面積。



from manim import *
class Question2(Scene):
    def construct(self):
        question = TexText(
            """
            Question \\#2: What is the area of the shadow of\\\\
            one of these rings?  (In terms of $R$, $\\theta$, and $d\\theta$).
            """,
            tex_to_color_map={
                "shadow": YELLOW,
            }
        )
        question.set_width(FRAME_WIDTH - 1)

        self.play(FadeIn(question, shift=DOWN))
        self.wait()
