# Source: 3b1b/_2019/diffyq/part2/pi_scenes.py
# Description: [3b1b translated] 展示老師指向螢幕，學生思考，然後可汗學院標誌從下方淡入的教學場景。



from manim import *
class ReferenceKhanVideo(TeacherStudentsScene):
    def construct(self):
        khan_logo = ImageMobject("KhanLogo")
        khan_logo.set_height(1)
        khan_logo.next_to(self.teacher, UP, buff=2)
        khan_logo.shift(2 * LEFT)

        self.play(
            self.teacher.animate.change("raise_right_hand"),
        )
        self.play_student_changes(
            "thinking", "pondering", "thinking",
            look_at=self.screen
        )
        self.wait()
        self.play(FadeIn(khan_logo, shift=DOWN))
        self.look_at(self.screen)
        self.wait(15)
