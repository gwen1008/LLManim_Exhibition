# Source: 3b1b/_2019/diffyq/part2/pi_scenes.py
# Description: [3b1b translated] 展示教師與學生場景中，比較偏微分方程與常微分方程的文字標籤動畫，包含標籤顏色、排列、交換以及角色表情變化。



from manim import *
class ContrastPDEToODE(TeacherStudentsScene):
    def __init__(self, random_seed=2, **kwargs):
        super().__init__(random_seed=random_seed, **kwargs)

    def construct(self):
        student = self.students[2]
        pde, ode = words = VGroup(*[
            MathTex(
                text + "\\\\",
                "Differential\\\\",
                "Equation"
            )
            for text in ("Partial", "Ordinary")
        ])
        pde[0].set_color(YELLOW)
        ode[0].set_color(BLUE)
        for word in words:
            word.arrange(DOWN, aligned_edge=LEFT)

        words.arrange(RIGHT, buff=LARGE_BUFF)
        words.next_to(student.get_corner(UR), UP, MED_LARGE_BUFF)
        words.shift(UR)
        lt = MathTex("<")
        lt.scale(1.5)
        lt.move_to(Line(pde.get_right(), ode.get_left()))

        for pi in self.pi_creatures:
            pi.add_updater(lambda p: p.look_at(pde))

        self.play(
            FadeIn(VGroup(words, lt), shift=DOWN),
            student.animate.change("raise_right_hand"),
        )
        self.play(
            self.change_students("pondering", "pondering", "hooray"),
            self.teacher.animate.change("happy")
        )
        self.wait(3)
        self.play(
            Swap(ode, pde),
            self.teacher.animate.change("raise_right_hand"),
            self.change_students(
                "erm", "sassy", "confused"
            )
        )
        self.look_at(words)
        self.play_student_changes(
            "thinking", "thinking", "tease",
        )
        self.wait(3)
