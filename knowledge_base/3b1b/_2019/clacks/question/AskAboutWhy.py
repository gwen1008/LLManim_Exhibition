# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示老師與學生互動的場景，學生提問後老師畫出黃色圓圈並寫出動能守恆公式，學生表情從疑惑轉為困惑。



from manim import *
class AskAboutWhy(TeacherStudentsScene):
    def construct(self):
        circle = Circle(radius=2, color=YELLOW)
        circle.next_to(self.teacher, UL)
        ke_conservation = MathTex(
            "\\frac{1}{2}m_1 v_1^2 + "
            "\\frac{1}{2}m_2 v_2^2 = \\text{const.}"
        )
        ke_conservation.move_to(circle)

        self.student_says("But why?")
        self.play_student_changes(
            "erm", "raise_left_hand", "sassy",
            added_anims=[self.teacher.change, "happy"]
        )
        self.wait()
        self.play(
            Create(circle),
            RemovePiCreatureBubble(self.students[1]),
            self.teacher.change, "raise_right_hand",
        )
        self.play_all_student_changes(
            "pondering", look_at=circle
        )
        self.wait(2)
        self.play(
            Write(ke_conservation),
            circle.animate.stretch(1.5, 0),
        )
        self.play_all_student_changes("confused")
        self.look_at(circle)
        self.wait(3)
