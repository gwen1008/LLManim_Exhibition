# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 老師舉手介紹傅立葉變換，學生們呈現不同反應，鏡頭看向左上方。



from manim import *
class BringInFourierTranform(TeacherStudentsScene):
    def construct(self):
        fourier = Text("Fourier", font_size=72)  # OldTexText -> Text
        fourier.scale(1.5)
        fourier.next_to(self.teacher.get_corner(UP+LEFT), UP, buff=LARGE_BUFF)
        fourier.save_state()
        fourier.shift(DOWN)
        fourier.set_opacity(0)  # .fade(1) -> .set_opacity(0)

        self.play(
            self.teacher.change.animate("raise_right_hand"),  # 動畫語法更新
            Restore(fourier)  # fourier.restore 改為 Restore 動畫
        )
        self.play_student_changes("happy", "erm", "confused")
        self.look_at(3*LEFT + 2*UP)
        self.wait(3)
