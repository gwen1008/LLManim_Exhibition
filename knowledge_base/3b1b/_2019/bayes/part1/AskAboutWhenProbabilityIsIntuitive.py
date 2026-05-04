# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 老師向學生提問「什麼讓機率更直觀？」，並伴隨師生表情和文字動畫變化。



from manim import *
class AskAboutWhenProbabilityIsIntuitive(TeacherStudentsScene):
    def construct(self):
        words = Text("What makes probability\nmore intuitive?")
        words.move_to(self.hold_up_spot, DOWN)
        words.shift_onto_screen()

        self.play(
            self.teacher.animate.change("speaking"),
            self.change_students(
                "pondering", "sassy", "happy",
                look_at=self.screen,
            )
        )
        self.wait(2)

        self.play(
            self.teacher.animate.change("raise_right_hand"),
            FadeIn(words, shift=DOWN),
            self.change_students("erm", "pondering", "confused")
        )
        self.wait(2)
        self.play(
            words.animate.scale(2),
            words.animate.center(),
            words.animate.to_edge(UP),
            self.teacher.animate.change("pondering", 3 * UP),
            self.change_students(
                "pondering", "thinking", "thinking",
                look_at=3 * UP,
            )
        )
        self.wait(6)
