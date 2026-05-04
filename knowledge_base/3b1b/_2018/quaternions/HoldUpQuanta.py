# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示老師和學生場景中，老師舉起右手並展示 Quanta 標誌和相關四元數文章的動畫。



from manim import *
class HoldUpQuanta(TeacherStudentsScene):
    def construct(self):
        logo = ImageMobject("Quanta logo")
        logo.set_width(6)
        logo.next_to(self.teacher, UR)
        logo.to_edge(RIGHT, buff=2)

        words = Text("Associated quaternion post")
        words.to_edge(UP, buff=LARGE_BUFF)
        arrow = Arrow(logo.get_top(), words.get_bottom())

        self.play(
            FadeIn(logo, shift=DOWN),
            self.teacher.change, "raise_right_hand"
        )
        self.play_all_student_changes("hooray")
        self.play(
            GrowArrow(arrow),
            GrowFromPoint(words, arrow.get_start())
        )
        self.wait(3)
