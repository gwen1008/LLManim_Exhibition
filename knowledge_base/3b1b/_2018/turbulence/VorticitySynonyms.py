# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示「高渦度」及其同義詞以帶背景的矩形框從下方淡入出現的過程。



from manim import *
class VorticitySynonyms(Scene):
    def construct(self):
        words = VGroup(
            Text("High", "vorticity"),  # OldTexText 改為 Text
            MathTex(
                "\\text{a.k.a} \\,",
                "|\\nabla \\times \\vec{\\textbf{v}}| > 0"
            ),
            Text("a.k.a", "high", "swirly-swirly", "factor"),
        )
        # set_color_by_tex 改為 set_color，並指定對應的子字串
        words[0][1].set_color(BLUE)  # "vorticity" 部分設為藍色
        words[1][1].set_color(BLUE)  # "nabla" 部分設為藍色
        words[2][2].set_color(BLUE)  # "swirly-swirly" 部分設為藍色
        words.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=MED_LARGE_BUFF
        )

        for word in words:
            # 為每個文字物件添加背景矩形
            word.add_background_rectangle()
            # FadeInFromDown 改為 FadeIn 並指定 shift 方向
            self.play(FadeIn(word, shift=DOWN))
            self.wait()
