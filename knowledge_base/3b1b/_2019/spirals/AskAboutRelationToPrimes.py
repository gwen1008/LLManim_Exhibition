# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示教師與學生場景中，一組數字與質數之間關係的疑問動畫，包含箭頭、問號和角色表情變化。



from manim import *
class AskAboutRelationToPrimes(TeacherStudentsScene):
    def construct(self):
        numbers = MathTex("20, 280")  # 原為 OldTexText，改為 MathTex
        arrow = Arrow(LEFT, RIGHT)
        primes = MathTex("2, 3, 5, 7, 11, \\dots")  # 原為 OldTexText，改為 MathTex
        q_marks = MathTex("???")  # 原為 OldTexText，改為 MathTex
        q_marks.set_color(YELLOW)

        group = VGroup(primes, arrow, numbers)
        group.arrange(RIGHT)
        q_marks.next_to(arrow, UP)
        group.add(q_marks)
        group.scale(1.5)
        group.next_to(self.pi_creatures, UP, buff=LARGE_BUFF)  # LARGE_BUFF 改為 buff=LARGE_BUFF

        self.play(
            self.change_students(
                *3 * ["maybe"],
                look_at=numbers,
            ),
            self.teacher.animate.change("maybe", numbers),  # 改為 .animate 語法
            Create(arrow),  # ShowCreation 改為 Create
            FadeIn(numbers, shift=RIGHT)  # FadeIn 方向參數調整
        )
        self.play(
            FadeIn(primes, shift=LEFT),  # FadeIn 方向參數調整
        )
        self.play(
            LaggedStartMap(FadeIn, q_marks, shift=DOWN),  # FadeInFromDown 改為 FadeIn(shift=DOWN)
            Blink(self.teacher)
        )
        self.wait(3)
