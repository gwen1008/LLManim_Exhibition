# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示教師與學生場景中，帕斯卡三角形縮小移動並顯示機率問題的過程。



from manim import *
class BeforeCounting(TeacherStudentsScene):
    def construct(self):
        triangle = PascalsTriangle(nrows=7)
        triangle.set_height(4)
        triangle.next_to(self.teacher, UP + LEFT)

        prob = get_probability_of_slot_group([True, True, False])
        prob.to_edge(UP)
        brace = Brace(prob, DOWN)
        q_marks = brace.get_text("???")

        self.teacher.change_mode("raise_right_hand")
        self.add(triangle)
        self.play_student_changes(*["hooray"] * 3)
        self.play(
            triangle.animate.scale(0.5).to_corner(UP + RIGHT),
            self.teacher.change_mode("sassy")
        )
        self.play_student_changes(*["confused"] * 3)
        self.play(Write(prob))
        self.play(
            GrowFromCenter(brace),
            LaggedStart(*[FadeIn(mark) for mark in q_marks])
        )
        self.wait(2)
