# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示在重複應用函數的場景中，當種子值為負數時，添加一個問題框並放大鏡頭，然後恢復原狀的過程。



from manim import *
class RepeatedApplicationWithNegativeSeed(RepeatedApplicationWithPhiBro, MovingCameraScene):
    def __init__(self, value=-0.65, value_str="-0.65", **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.value_str = value_str

    def construct(self):
        super().construct()

        rect = SurroundingRectangle(self.top_line)
        question = Text("What about a negative seed?")
        question.set_color(rect.get_color())
        question.next_to(rect, UP)
        self.play(Create(rect))
        self.play(
            Write(question),
            self.camera.frame.animate.set_height(FRAME_HEIGHT + 1.5)
        )
        self.wait()
        self.play(
            FadeOut(question),
            FadeOut(rect),
            self.camera.frame.animate.set_height(FRAME_HEIGHT)
        )
