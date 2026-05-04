# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示教師與學生互動的場景，教師指向螢幕並說話，學生們有不同反應。



from manim import *
class FromKAWrapper(TeacherStudentsScene):
    def construct(self):
        screen = self.screen
        self.play(
            self.teacher.animate.change("raise_right_hand"),
            self.change_students("pondering", "confused", "hooray")
        )
        self.look_at(screen)
        self.wait(2)
        self.play_student_changes("erm", "happy", "confused")
        self.wait(3)
        self.teacher_says(
            "Our focus is \\\\ the 2d version",
            bubble_config={"width": 4, "height": 3},
            added_anims=[self.change_students("happy", "hooray", "happy")]
        )
        self.wait()
