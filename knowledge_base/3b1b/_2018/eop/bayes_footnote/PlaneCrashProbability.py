# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 展示飛機失事與汽車事故死亡機率的對比，透過文字動畫呈現兩者數值的差異。



from manim import *
class PlaneCrashProbability(Scene):
    def construct(self):
        plane_prob = MathTex(
            "P(\\text{Dying in a }", "\\text{plane}", "\\text{ crash})", 
            "\\approx", "1/", "11{,}000{,}000"
        )
        plane_prob.set_color_by_tex("plane", BLUE)
        car_prob = MathTex(
            "P(\\text{Dying in a }", "\\text{car}", "\\text{ crash})", 
            "\\approx", "1/", "5{,}000"
        )
        car_prob.set_color_by_tex("car", YELLOW)
        plane_prob.shift(UP)
        car_prob.shift(
            plane_prob.get_part_by_tex("approx").get_center() -\
            car_prob.get_part_by_tex("approx").get_center() +\
            DOWN
        )

        self.play(Write(plane_prob))
        self.wait(2)
        self.play(TransformFromCopy(
            plane_prob, car_prob
        ))
        self.wait(2)
