# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示課堂場景中學生提問「沒有聲音，對吧？」後老師露出愧疚表情，接著老師引導學生專注於碰撞，學生們呈現思考、困惑、沉思等反應，最後大家看向螢幕。



from manim import *
class AskAboutSoundlessness(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "No sound,\\\\right?"
        )
        self.play(self.teacher.animate.change("guilty"))
        self.wait(2)
        self.teacher_says(
            "Focus on \\\\ collisions",
            target_mode="speaking",
            added_anims=[
                self.change_students("pondering", "confused", "thinking")
            ]
        )
        self.look_at(self.screen)
        self.wait(3)
