# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示老師向學生說明「湍流意味著渦度，但渦度不一定意味著湍流」的概念，使用文字變換和叉號動畫。



from manim import *
class VorticityDoesNotImplyTurbulence(TeacherStudentsScene):
    def construct(self):
        t_to_v = TexText(
            "Turbulence", "$\\Rightarrow$", "Vorticity",
        )
        v_to_t = TexText(
            "Vorticity", "$\\Rightarrow$", "Turbulence",
        )
        for words in t_to_v, v_to_t:
            words.move_to(self.hold_up_spot, DR)
            words.set_color_by_tex_to_color_map({
                "Vorticity": BLUE,
                "Turbulence": GREEN,
            })
        v_to_t.submobjects.reverse()
        cross = Cross(v_to_t[1])

        morty = self.teacher
        self.play(
            morty.change, "raise_right_hand",
            FadeIn(t_to_v, shift=DOWN)
        )
        self.wait()
        self.play(t_to_v.animate.shift(2 * UP))
        self.play(
            TransformFromCopy(t_to_v, v_to_t, path_arc=PI / 2),
            self.change_students(
                "erm", "confused", "sassy",
                run_time=1
            ),
            Create(cross, run_time=2),
        )
        self.add(cross)
        self.wait(4)
