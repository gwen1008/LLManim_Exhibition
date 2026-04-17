# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示老師在課堂上舉手，學生們從思考轉為困惑的表情變化，背景有 Mathematics Stack Exchange 標題。



from manim import *
class HoldUpMathExchange(TeacherStudentsScene):
    def construct(self):
        title = Tex("Mathematics Stack Exchange")
        title.scale(1.5)
        title.to_edge(UP)

        self.add(title)
        self.play(self.teacher.animate.change("raise_right_hand", ORIGIN))
        self.play_all_student_changes("thinking", look_at=ORIGIN)
        self.wait(3)
        self.play_all_student_changes("confused", look_at=ORIGIN)
        self.wait(3)
