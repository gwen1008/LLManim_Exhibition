# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 老師向學生展示一個無窮級數求和問題，學生提出關於任意指數的級數求和疑問，老師反問求和符號的意義。



from manim import *
class AskPuzzle(TeacherStudentsScene):
    def construct(self):
        series = MathTex(
            "\\frac{1}{1} + \\frac{1}{4} + \\frac{1}{9} + \\cdots + " +\
            "\\frac{1}{n^2} + \\cdots = ", "\\,???"
        )
        series[0].set_color_by_gradient(BLUE_C, BLUE_B)
        series[1].set_color(YELLOW)

        question = TexText(
            "How should we think about\\\\",
            "$\\displaystyle \\sum_{n=1}^\\infty \\frac{1}{n^s}$",
            "for arbitrary $s$?"
        )
        question[1].set_color(BLUE)
        question[0].shift(SMALL_BUFF*UP)

        response = TexText(
            "What do you mean by ", 
            "$\\displaystyle \\sum_{n = 1}^{\\infty}$", 
            "?"
        )
        response[1].set_color(BLUE)

        self.teacher_says(series)
        self.play_all_student_changes("pondering", look_at = series)
        self.wait(3)
        self.play(
            FadeOut(self.teacher.bubble),
            self.teacher.animate.change("happy"),
            series.animate.scale(0.5),
            series.animate.to_corner(UL),
            PiCreatureSays(
                self.students[0], question,
                target_mode = "raise_left_hand"
            )
        )
        self.play_student_changes(
            None, "confused", "confused",
            added_anims = [self.students[0].animate.look_at(question)]
        )
        self.wait(2)

        self.students[0].bubble.content = VGroup()
        self.play(
            RemovePiCreatureBubble(self.students[0]),
            question.animate.scale(0.5),
            question.animate.next_to(series, DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT),
            PiCreatureSays(self.teacher, response)
        )
        self.play_all_student_changes("erm")
        self.wait(3)
