# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示老師鼓勵學生後，學生們從開心轉為思考，最後老師表達喜愛並展示費曼和棋局圖片的場景。



from manim import *
class PatYourselfOnTheBack(TeacherStudentsScene):
    def __init__(self, **kwargs):
        super().__init__(camera_config={"background_opacity": 1}, **kwargs)

    def construct(self):
        self.teacher_says(
            "Pat yourself \\\\ on the back!",
            target_mode="hooray"
        )
        self.play_all_student_changes("happy")
        self.wait(3)
        self.play(
            RemovePiCreatureBubble(
                self.teacher,
                target_mode="raise_right_hand"
            ),
            self.change_students(
                *3 * ["pondering"],
                look_at=self.screen
            )
        )
        self.look_at(UP)
        self.wait(8)
        self.play_student_changes(*3 * ["thinking"])
        self.look_at(UP)
        self.wait(12)
        self.teacher_says("I just love this!")

        feynman = ImageMobject("Feynman", height=4)
        feynman.to_corner(UL)
        chess = ImageMobject("ChessGameOfTheCentury")
        chess.set_height(4)
        chess.next_to(feynman)

        self.play(FadeIn(feynman, shift=DOWN))
        self.wait()
        self.play(
            RemovePiCreatureBubble(self.teacher, target_mode="happy"),
            FadeIn(chess, shift=DOWN)
        )
        self.wait(2)
