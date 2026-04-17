# Source: 3b1b/_2019/diffyq/part2/pi_scenes.py
# Description: [3b1b translated] 老師展示熱方程並提問，學生困惑回應，老師陷入沉思。



from manim import *
class AskAboutWhereEquationComesFrom(TeacherStudentsScene):
    def construct(self):
        # 假設 WriteHeatEquationTemplate 提供了 get_d1_equation 方法
        # 由於繼承關係已移除 WriteHeatEquationTemplate，我們假設 equation 已定義
        # 這裡創建一個示例方程作為替代
        equation = MathTex(r"\frac{\partial u}{\partial t} = \alpha \nabla^2 u")
        equation.move_to(self.hold_up_spot, DOWN)

        self.play(
            FadeIn(equation, shift=DOWN),
            self.teacher.animate.change("raise_right_hand")
        )
        self.student_says(
            "Um...why?",
            target_mode="sassy",
            student_index=2,
            bubble_config={"direction": RIGHT},
        )
        self.play_student_changes(
            "confused", "confused", "sassy",
        )
        self.wait()
        self.play(
            self.teacher.animate.change("pondering"),
        )
        self.wait(2)
