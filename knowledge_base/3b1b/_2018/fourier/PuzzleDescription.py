# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示一個數學問題的描述，包含凸集、邊界和集合運算的定義，並用顏色標示不同符號。



from manim import *
class PuzzleDescription(Scene):
    def construct(self):
        lines = VGroup(
            MathTex(r"\text{Convex set }", "C", r"\text{ in } \mathbb{R}^3"),
            MathTex(r"\text{Boundary }", "B", "=", r"\partial C"),
            MathTex("D", r"=\{p+q \mid p, q \in B\}"),
            MathTex(r"\text{Prove that }", "D", r"\text{ is convex}")
        )
        for line in lines:
            line.set_color_by_tex_to_color_map({
                "C" : BLUE_D,
                r"\partial C" : BLUE_D,
                "B" : BLUE_C,
                "D" : YELLOW,
            })
        # 手動設置特定字符顏色
        # lines[2][1][2] 和 lines[2][1][6] 對應 p 和 q
        lines[2][1][2].set_color(RED)
        lines[2][1][6].set_color(RED)
        # lines[2][1][4] 和 lines[2][1][8] 對應 + 和 |
        lines[2][1][4].set_color(MAROON_B)
        lines[2][1][8].set_color(MAROON_B)
        # lines[2][1][10] 對應 B
        lines[2][1][10].set_color(BLUE_C)
        
        lines.scale(1.25)
        lines.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        lines.to_corner(UP+RIGHT)

        for line in lines:
            self.play(Write(line))
            self.wait(2)
