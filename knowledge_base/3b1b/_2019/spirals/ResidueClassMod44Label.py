# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 在畫面的左上角顯示「Residue class mod 44」文字標籤。



from manim import *
class ResidueClassMod44Label(Scene):
    def construct(self):
        text = MathTex(r"\text{``Residue class mod 44''}")
        text.scale(2)
        text.to_corner(UL)

        self.play(Write(text))
        self.wait()
