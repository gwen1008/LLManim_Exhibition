# Source: 3b1b/_2018/eop/bayes.py
# Description: [3b1b translated] 展示教師與學生場景中，標題淡入並創建螢幕矩形，教師舉手示意，學生們轉向螢幕思考的過程。



from manim import *
class NextVideoWrapper(TeacherStudentsScene):
    def __init__(self, title="Upcoming chapter: Bayesian networks", **kwargs):
        super().__init__(**kwargs)
        self.title = title

    def construct(self):
        title = TexText(self.title)
        title.scale(0.8)
        title.to_edge(UP, buff=SMALL_BUFF)
        screen = ScreenRectangle(height=4)
        screen.next_to(title, DOWN)
        title.save_state()
        title.shift(DOWN)
        title.set_opacity(0)

        self.play(
            title.animate.restore(),
            self.teacher.animate.change("raise_right_hand")
        )
        self.play(Create(screen))
        self.play_student_changes(
            *["pondering"]*3,
            look_at=screen
        )
        self.play(Animation(screen))
        self.wait(5)
