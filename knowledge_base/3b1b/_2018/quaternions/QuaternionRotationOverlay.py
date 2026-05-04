# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示四元數旋轉公式的層疊變換過程，從單一旋轉逐步擴展到三重複合旋轉。



from manim import *
class QuaternionRotationOverlay(Scene):
    def construct(self):
        equations = VGroup(
            MathTex(
                "p", "\\rightarrow",
                "{}",
                "{}",
                "\\left(q_1",
                "p",
                "q_1^{-1}\\right)",
                "{}",
                "{}",
            ),
            MathTex(
                "p", "\\rightarrow",
                "{}",
                "\\left(q_2",
                "\\left(q_1",
                "p",
                "q_1^{-1}\\right)",
                "q_2^{-1}\\right)",
                "{}",
            ),
            MathTex(
                "p", "\\rightarrow",
                "\\left(q_3",
                "\\left(q_2",
                "\\left(q_1",
                "p",
                "q_1^{-1}\\right)",
                "q_2^{-1}\\right)",
                "q_3^{-1}\\right)",
            ),
        )
        for equation in equations:
            # ManimCE 使用 set_color_by_tex 替代 set_color_by_tex_to_color_map
            for tex, color in [("1", GREEN), ("2", RED), ("3", BLUE)]:
                equation.set_color_by_tex(tex, color)
            equation.set_color_by_tex("rightarrow", WHITE)
            equation.to_corner(UL)

        equation = equations[0].copy()
        self.play(Write(equation))
        self.wait()
        for new_equation in equations[1:]:
            self.play(
                Transform(equation, new_equation)
            )
            self.wait(2)
