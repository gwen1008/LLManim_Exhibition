# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示老師在黑板上寫出一個無窮級數等於 π²/8，然後學生提問關於另一個類似級數的場景。



from manim import *
class WaitScene(TeacherStudentsScene):
    def construct(self):
        # 老師說出第一個級數等式
        self.teacher_says(MathTex("{1\\over 1^2}+{1\\over 3^2}+{1\\over 5^2}+{1\\over 7^2}+\\dots = {\\pi^2 \\over 8}!"))

        # 學生提問第二個級數
        student_q = Text("What about")
        full_sum = MathTex("{1\\over 1^2}+{1\\over 2^2}+{1\\over 3^2}+{1\\over 4^2}+\\dots?")
        full_sum.next_to(student_q, RIGHT)
        student_q.add(full_sum)

        # 學生以生氣的表情提問
        self.student_says(student_q, target_mode="angry")
        self.wait()
