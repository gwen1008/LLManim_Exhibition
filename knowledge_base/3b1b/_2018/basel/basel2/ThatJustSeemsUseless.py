# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示老師和學生場景中，一名學生提出質疑，老師和所有學生都表現出尷尬或諷刺的表情。



from manim import *
class ThatJustSeemsUseless(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "How would \\\\ that help?",
            target_mode="sassy",
            index=2,
            bubble_config={"direction": LEFT},
        )
        self.play(
            self.teacher.animate.change("guilty"),
            *[self.students[i].animate.change("sassy") for i in range(3)]
        )
        self.wait()
