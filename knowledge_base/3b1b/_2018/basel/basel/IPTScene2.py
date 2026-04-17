# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示三個光強度指示器及其對應的公式，組合成逆畢氏定理的可視化表示，並用方框和標題強調。



from manim import *
class IPTScene2(Scene):
    def construct(self):
        intensity1 = 0.3
        intensity2 = 0.2
        formula_scale = 1.2
        indy_radius = 1

        # 注意：LightIndicator 不是 ManimCE 內建類別
        # 假設它是自定義的 Mobject，這裡用 Circle 替代以保持視覺結構
        indy1 = Circle(radius=indy_radius, color=LIGHT_COLOR, fill_opacity=intensity1)
        reading1 = MathTex(r"{1\over a^2}").scale(formula_scale).move_to(indy1)
        indy1.add(reading1)

        indy2 = Circle(radius=indy_radius, color=LIGHT_COLOR, fill_opacity=intensity2)
        reading2 = MathTex(r"{1\over b^2}").scale(formula_scale).move_to(indy2)
        indy2.add(reading2)

        indy3 = Circle(radius=indy_radius, color=LIGHT_COLOR, fill_opacity=intensity1 + intensity2)
        reading3 = MathTex(r"{1\over h^2}").scale(formula_scale).move_to(indy3)
        indy3.add(reading3)

        plus_sign = MathTex("+").scale(formula_scale)
        equals_sign = MathTex("=").scale(formula_scale)

        plus_sign.next_to(indy1, RIGHT)
        indy2.next_to(plus_sign, RIGHT)
        equals_sign.next_to(indy2, RIGHT)
        indy3.next_to(equals_sign, RIGHT)

        formula = VGroup(indy1, plus_sign, indy2, equals_sign, indy3)
        formula.move_to(ORIGIN)

        self.play(FadeIn(indy1))
        self.play(FadeIn(plus_sign), FadeIn(indy2))
        self.play(FadeIn(equals_sign), FadeIn(indy3))

        buffer = 1.5
        box = Rectangle(
            width=formula.get_width() * buffer,
            height=formula.get_height() * buffer
        )
        box.move_to(formula)
        text = Tex("Inverse Pythagorean Theorem").scale(formula_scale)
        text.next_to(box, UP)
        self.play(Create(box), Write(text))
