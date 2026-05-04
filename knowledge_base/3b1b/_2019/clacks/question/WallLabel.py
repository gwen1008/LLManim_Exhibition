# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示一個垂直的黃色牆壁線條和旋轉的文字標籤，並以閃爍動畫呈現牆壁。



from manim import *
class WallLabel(Scene):
    def construct(self):
        wall = Line(UP, 2 * DOWN)
        wall.set_stroke(YELLOW, 10)
        word = Text("Wall")
        word.rotate(-90 * DEGREES)
        word.next_to(wall, RIGHT, buff=MED_SMALL_BUFF)
        self.play(
            Write(word),
            ShowPassingFlash(wall)
        )
        self.wait()
