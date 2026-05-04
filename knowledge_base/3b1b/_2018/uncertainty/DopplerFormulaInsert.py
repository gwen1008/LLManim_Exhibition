# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示一個藍色卡通人物旁邊出現都卜勒效應公式，公式中的回波頻率為藍色、脈衝頻率為黃色，人物做出思考表情並眨眼。



from manim import *
class DopplerFormulaInsert(Scene):
    def construct(self):
        formula = MathTex(
            "f_{\\text{echo}}", "=",
            "\\left(1 + \\frac{v}{c}\\right)",
            "f_{\\text{pulse}}"
        )
        formula[0].set_color(BLUE)
        formula[3].set_color(YELLOW)

        randy = Randolph(color = BLUE_C)
        formula.scale(1.5)
        formula.next_to(randy, UP+LEFT)
        # shift_onto_screen() 在 CE 中沒有直接對應，用 to_edge(UP) 近似
        formula.to_edge(UP, buff=0.5)

        self.add(randy)
        self.play(
            LaggedStartMap(FadeIn, formula),
            randy.animate.change("pondering", randy.get_bottom()),
        )
        self.play(Blink(randy))
        self.wait(2)
        self.play(Blink(randy))
        self.wait()
