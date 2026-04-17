# Source: 3b1b/_2019/clacks/solution2/simple_scenes.py
# Description: [3b1b translated] 展示一個數學公式及其相關的推導過程，包含顏色標記和動畫效果。



from manim import *
class FinalFormula(Scene):
    def construct(self):
        text = Text("Final answer: ")
        t2c_map = {
            "\\theta": BLUE,
            "m_1": GREEN,
            "m_2": RED,
        }

        formula = MathTex(
            "\\left\\lfloor",
            "{\\pi", "\\over", "\\theta}",
            "\\right\\rfloor"
        )
        # ManimCE 使用 set_color_by_tex 替代 set_color_by_tex_to_color_map
        for tex, color in t2c_map.items():
            formula.set_color_by_tex(tex, color)
        group = VGroup(text, formula)
        group.arrange(RIGHT)
        group.scale(1.5)
        group.to_edge(UP)

        self.play(Write(text))
        self.play(FadeIn(formula))
        # ManimCE 使用 Circumscribe 替代 ShowCreationThenFadeAround
        self.play(Circumscribe(formula))
        self.wait()

        theta_eq = MathTex(
            "\\theta", "=", "\\arctan", "\\left(",
            "\\sqrt",
            "{{m_2", "\\over", "m_1}}",
            "\\right)"
        )
        for tex, color in t2c_map.items():
            theta_eq.set_color_by_tex(tex, color)
        theta_eq.scale(1.5)
        theta_eq.next_to(group, DOWN, buff=MED_LARGE_BUFF)

        # 使用 Transform 和 Copy 來模擬 TransformFromCopy
        theta_copy = formula.get_part_by_tex("\\theta").copy()
        self.play(Transform(theta_copy, theta_eq.get_part_by_tex("\\theta")))
        self.play(Write(theta_eq[1:]))
        self.wait()
