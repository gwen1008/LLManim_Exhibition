# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示一個描述圓錐截面離心率的數學公式，並將特定術語著色後從下方淡入。



from manim import *
class EccentricityForSlicedConed(Scene):
    def construct(self):
        equation = MathTex(
            "\\text{Eccentricity} = ",
            "{\\sin(", "\\text{angle of plane}", ")", "\\over",
            "\\sin(", "\\text{angle of cone slant}", ")}"
        )
        # ManimCE 中 set_color_by_tex 已改名為 set_color_by_tex_to_color_map
        # 但更簡單的方式是直接對部分設置顏色
        # 這裡手動設置顏色
        plane_part = equation.get_part_by_tex("angle of plane")
        cone_part = equation.get_part_by_tex("angle of cone slant")
        plane_part.set_color(YELLOW)
        cone_part.set_color(BLUE)
        equation.to_edge(LEFT)
        self.play(FadeIn(equation, shift=DOWN))
