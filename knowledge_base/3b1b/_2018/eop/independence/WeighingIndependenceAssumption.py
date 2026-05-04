# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示一個角色舉起雙手，同時顯示「獨立性」標題和機率公式，並將公式中的變數著色。



from manim import *
class WeighingIndependenceAssumption(PiCreatureScene):
    def construct(self):
        randy = self.randy

        title = Text("Independence")
        title.scale(1.5)
        title.to_edge(UP)
        self.add(title)
        formula = MathTex(
            "P(", "A", "B", ")", "=",
            "P(", "A", ")", "P(", "B", ")"
        )
        formula.set_color_by_tex("A", BLUE)
        formula.set_color_by_tex("B", GREEN)

        clean = Text("Clean")
        clean.next_to(formula, UP)
        VGroup(clean, formula).next_to(randy, UP+LEFT)
        clean.save_state()
        clean.shift(2*(DOWN+RIGHT))
        clean.set_opacity(0)

        self.play(
            randy.animate.change("raise_left_hand", clean),
            clean.animate.restore()
        )
        self.play(Write(formula))
        self.play(
            randy.animate.change("raise_right_hand"),
            randy.animate.look(UP+RIGHT),
        )
        self.wait(2)

    def create_pi_creature(self):
        self.randy = Randolph().to_edge(DOWN)
        return self.randy
