# Source: 3b1b/_2018/mvcr.py
# Description: [3b1b translated] 展示老師舉手指向螢幕上的「多變數鏈鎖法則」標題，學生們困惑地看著螢幕的場景。



from manim import *
class HoldUpMultivariableChainRule(TeacherStudentsScene):
    def construct(self):
        title = Text("Multivariable chain rule")
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        screen = ScreenRectangle()
        screen.next_to(title, DOWN)

        morty = self.teacher

        self.add(title)
        self.play(
            morty.change, "raise_right_hand",
            FadeIn(screen, shift=DOWN)
        )
        self.play_all_student_changes(
            "confused", look_at=screen
        )
        self.look_at(screen)
        self.wait(10)
