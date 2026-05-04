# Source: 3b1b/_2019/diffyq/part1/pi_scenes.py
# Description: [3b1b translated] 展示一位老師和三位學生在教室場景中，老師舉手示意，學生們看著螢幕思考，其中一位學生說出「Well...yeah」的對話場景。



from manim import *
class SomeOfYouWatching(TeacherStudentsScene):
    def __init__(self, **kwargs):
        super().__init__(
            camera_config={"background_color": GREY_E},
            **kwargs
        )

    def construct(self):
        screen = self.screen
        screen.scale(1.25, about_edge=UL)
        screen.set_fill(BLACK, 1)
        self.add(screen)

        self.teacher.change("raise_right_hand")
        for student in self.students:
            student.change("pondering", screen)

        self.student_says(
            "Well...yeah",
            target_mode="tease"
        )
        self.wait(3)
