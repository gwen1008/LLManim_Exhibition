# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 老師對學生們說「今天：我們民族的歷史」，學生們歡呼並開心地看向螢幕。



from manim import *
class HistoryOfOurPeople(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Today: The history \\\\ of our people.",
            bubble_config = {"width" : 4, "height" : 3}
        )
        self.play_all_student_changes("hooray")
        self.wait()
        self.play(*[
            pi.animate.change("happy", self.screen)
            for pi in self.pi_creatures
        ])
        self.wait(4)
