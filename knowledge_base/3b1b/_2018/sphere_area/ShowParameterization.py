# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示球面參數化的數學表達式及其參數範圍，使用不同顏色區分 u 和 v 變量。



from manim import *
class ShowParameterization(Scene):
    def construct(self):
        u_color = PINK
        v_color = GREEN
        tex_kwargs = {
            "tex_to_color_map": {
                "u": u_color,
                "v": v_color,
            }
        }
        vector = Matrix(
            [
                ["\\text{cos}(u)\\text{sin}(v)"],
                ["\\text{sin}(u)\\text{sin}(v)"],
                ["\\text{cos}(v)"]
            ],
            element_to_mobject_config=tex_kwargs,
            element_alignment_corner=DOWN,
        )
        vector.to_edge(UP)

        ranges = VGroup(
            MathTex("0 \\le u \\le 2\\pi", **tex_kwargs),
            MathTex("0 \\le v \\le \\pi", **tex_kwargs),
            Tex(
                "Sample $u$ and $v$ with \\\\ the same density",
                tex_to_color_map={
                    "$u$": u_color,
                    "$v$": v_color,
                }
            )
        )
        ranges.arrange(DOWN)
        ranges.next_to(vector, DOWN)

        self.add(vector)
        self.add(ranges)
