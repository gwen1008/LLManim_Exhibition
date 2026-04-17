# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示數字710的質因數分解過程，並用彩色矩形框突出每個質因數。



from manim import *
class ShowFactorsOf710(Scene):
    def construct(self):
        equation = MathTex(
            "710", "=",
            "71", "\\cdot",
            "5", "\\cdot",
            "2",
        )
        equation.scale(1.5)
        equation.to_corner(UL)
        ten = MathTex("10")
        ten.match_height(equation)
        ten.move_to(equation.get_part_by_tex("5"), LEFT)

        self.add(equation[0])
        self.wait()
        self.play(
            TransformFromCopy(
                equation[0][:2],
                equation[2],
            ),
            FadeIn(equation[1]),
            FadeIn(equation[3]),
            TransformFromCopy(
                equation[0][2:],
                ten,
            )
        )
        self.wait()
        self.remove(ten)
        self.play(*[
            TransformFromCopy(ten, mob)
            for mob in equation[4:]
        ])
        self.wait()

        # Circle factors
        colors = [RED, BLUE, PINK]
        for factor, color in zip(equation[:-6:-2], colors):
            rect = SurroundingRectangle(factor)
            rect.set_color(color)
            self.play(Create(rect))
            self.wait()
            self.play(FadeOut(rect))
