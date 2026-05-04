# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示老師舉起右手，學生們看向畫面左上角並表現出思考、困惑等表情的場景。



from manim import *
class ScreensIntroWrapper(TeacherStudentsScene):
    def construct(self):
        point = VectorizedPoint(config.frame_width * LEFT / 4 + config.frame_height * UP / 4)
        self.play(self.teacher.animate.change("raise_right_hand"))
        self.play_student_changes(
            "pondering", "erm", "confused",
            look_at=point,
        )
        self.play(self.teacher.animate.look_at(point))
        self.wait(5)
