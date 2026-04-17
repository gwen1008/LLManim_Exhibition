# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示組合數公式從具體例子到一般形式的漸進呈現，並用顏色標示對應部分。



from manim import *
class ShowFormula(Scene):
    def construct(self):
        specific_formula = MathTex(
            "{9 \\choose 4}", "=",
            "{9 \\cdot 8 \\cdot 7 \\cdot 6", "\\over",
            "4 \\cdot 3 \\cdot 2 \\cdot 1}"
        )
        general_formula = MathTex(
            "{n \\choose k}", "=",
            "{n \\cdot (n-1) \\cdots (n-k+1)", "\\over",
            "k \\cdot (k-1) \\cdots 2 \\cdot 1}"
        )
        # 標示藍色部分
        for i, j in (0, 1), (2, 0), (2, 3), (2, 11):
            general_formula[i][j].set_color(BLUE)
        # 標示黃色部分
        for i, j in (0, 2), (2, 13), (4, 0), (4, 3):
            general_formula[i][j].set_color(YELLOW)
        
        formulas = VGroup(specific_formula, general_formula)
        formulas.arrange(DOWN, buff=2)
        formulas.to_edge(UP)

        self.play(FadeIn(specific_formula))
        self.play(FadeIn(general_formula))
        self.wait(3)
