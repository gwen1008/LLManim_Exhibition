# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示一個常微分方程問題，先提出「求精確解」的目標，然後轉為探討解的「個性」，並用眼睛動畫表現思考過程。



from manim import *
class SetAsideSeekingSolution(Scene):
    def construct(self):
        ode = get_ode()
        ode.to_edge(UP)
        q1 = Text("Find an exact solution", color=YELLOW)
        q2 = MathTex(
            "\\text{What is }", "\\theta", "(t)",
            "\\text{'s personality?}",
            tex_to_color_map={"\\theta": BLUE},
        )
        theta = q2.get_part_by_tex("\\theta")

        for q in [q1, q2]:
            q.scale(1.5)
            q.next_to(ode, DOWN, buff=MED_LARGE_BUFF)
        eyes = Eyes(theta, height=0.1)

        self.add(ode)
        self.add(q1)
        self.wait()
        self.play(
            q1.animate.scale(0.3).to_corner(UR, buff=MED_SMALL_BUFF),
        )
        self.play(FadeIn(q2, shift=DOWN))
        self.play(
            eyes.blink,
            rate_func=lambda t: smooth(1 - t),
        )
        self.play(eyes.look_at(q2.get_left()))
        self.play(eyes.look_at(q2.get_right()))
        self.play(
            eyes.blink,
            rate_func=squish_rate_func(there_and_back)
        )
        self.wait()
        self.play(
            eyes.change_mode("confused"),
            eyes.look_at(ode.get_left()),
        )
        self.play(
            eyes.blink,
            rate_func=squish_rate_func(there_and_back)
        )
