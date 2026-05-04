# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 老師向學生展示一本推薦的測量書籍封面，學生們表現出高興和思考的反應。



from manim import *
class ShowMeasurementBook(TeacherStudentsScene):
    def __init__(self, camera_config={"background_opacity": 1}, **kwargs):
        super().__init__(camera_config=camera_config, **kwargs)

    def construct(self):
        measurement = ImageMobject("MeasurementCover")
        measurement.set_height(3.5)
        measurement.move_to(self.hold_up_spot, DOWN)

        words = Text("Highly recommended")
        arrow = Vector(RIGHT, color=WHITE)
        arrow.next_to(measurement, LEFT)
        words.next_to(arrow, LEFT)

        self.play(
            self.teacher.animate.change("raise_right_hand"),
            FadeIn(measurement, shift=DOWN)
        )
        self.play_all_student_changes("hooray")
        self.wait()
        self.play(
            GrowArrow(arrow),
            FadeIn(words, shift=RIGHT),
            self.change_students(
                "thinking", "happy", "pondering",
                look_at=arrow
            )
        )
        self.wait(3)
