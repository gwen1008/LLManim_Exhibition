# Source: 3b1b/_2019/diffyq/part2/pi_scenes.py
# Description: [3b1b translated] 展示老師與學生對話場景，學生提問「為什麼？」，老師回答「離導數更近一步」，學生們陷入思考。



from manim import *
class AskWhyRewriteIt(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Why?",
            target_mode="raise_right_hand",
            bubble_config={"height": 2, "width": 2},
            student_index=1
        )
        self.students[1].bubble = None
        self.teacher_says(
            "One step closer\nto derivatives"
        )
        self.play(
            self.students[0].animate.change("thinking", 4 * LEFT + 2 * UP),
            self.students[1].animate.change("thinking", 4 * LEFT + 2 * UP),
            self.students[2].animate.change("thinking", 4 * LEFT + 2 * UP),
        )
        self.wait(2)
