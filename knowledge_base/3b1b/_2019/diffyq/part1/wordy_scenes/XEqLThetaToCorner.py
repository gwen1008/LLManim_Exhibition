# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 將方程 "x = Lθ" 從右下角移動到左下角，並為變數 x 和 θ 著色。



from manim import *
class XEqLThetaToCorner(Scene):
    def construct(self):
        equation = MathTex(
            "x = L\\theta",
            tex_to_color_map={
                "x": GREEN,
                "\\theta": BLUE,
            }
        )
        equation.move_to(DOWN + 3 * RIGHT)
        self.add(equation)
        self.play(equation.animate.to_corner(DL, buff=LARGE_BUFF))
        self.wait()
