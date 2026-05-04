# Source: 3b1b/_2019/diffyq/part3/wordy_scenes.py
# Description: [3b1b translated] 展示教師與學生場景中，一個微分方程被標記為常見主題的視覺過程。



from manim import *
class WorryAboutGenerality(TeacherStudentsScene, WriteHeatEquationTemplate):
    def construct(self):
        eq = self.get_d1_equation()
        diffyq = self.get_diffyq_set()
        is_in = MathTex("\\in")
        is_in.scale(2)

        group = VGroup(eq, is_in, diffyq)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        group.to_edge(UP)

        arrow = Arrow(start=UP, end=DOWN, stroke_width=5)
        arrow.set_color(WHITE)
        arrow.next_to(eq, DOWN)
        themes = Text("Frequent themes")
        themes.scale(1.5)
        themes.next_to(arrow, DOWN)

        self.play(
            self.change_students(
                "sad", "tired", "pleading"
            ),
            self.teacher.animate.change("raise_right_hand"),
            FadeIn(eq, shift=DOWN)
        )
        self.play(Write(group[1:]))
        self.wait(2)
        self.play(
            Create(arrow),
            self.change_students(*3 * ["pondering"]),
        )
        self.play(
            FadeIn(themes, shift=UP),
            self.change_students(*3 * ["thinking"]),
            self.teacher.animate.change("happy")
        )
        self.wait(4)

    def get_diffyq_set(self):
        words = Text(
            "Differential\nequations"
        )
        words.scale(1.5)
        words.set_color(BLUE)
        lb = Brace(words, LEFT)
        rb = Brace(words, RIGHT)
        return VGroup(lb, words, rb)
