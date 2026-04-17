# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 在灰色背景上顯示提示文字和兩個數學公式，並垂直排列。



from manim import *
class HintToGeneralChallenge(Scene):
    def construct(self):
        self.add(FullScreenFadeRectangle(
            fill_color=GREY_E,
            fill_opacity=1,
        ))
        words1 = Text("Hint: Try writing")
        formula1 = MathTex(
            "c_{n} =",
            "{", "a_{n} \\over 2} +",
            "{", "b_{n} \\over 2} i",
            tex_to_color_map={
                "{n}": YELLOW,
            }
        )
        words2 = Text("and")
        formula2 = MathTex(
            "e^{i{x}} =",
            "\\cos\\left({x}\\right) +",
            "i\\sin\\left({x}\\right)",
            tex_to_color_map={
                "{x}": GREEN
            }
        )

        all_words = VGroup(
            words1, formula1,
            words2, formula2
        )
        all_words.arrange(DOWN, buff=LARGE_BUFF)

        self.add(all_words)
