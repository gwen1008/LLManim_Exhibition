# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示老師對學生說「再來一個小技巧」後，學生從疲憊轉為歡呼的場景。



from manim import *
class OneMoreTrick(TeacherStudentsScene):
    def construct(self):
        for student in self.students:
            student.change("tired")
        self.teacher_says("Just one more \\\\ tricky bit!")
        self.play_all_student_changes("hooray")
        self.wait(3)
