# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示一個教師與學生場景，標題和文字動畫呈現「比預期更難」的主題，伴隨角色表情變化。



from manim import *
class HarderThanExpected(TeacherStudentsScene):
    def construct(self):
        title = TexText("Unusual aspect \\#2")
        title.scale(1.5)
        title.to_edge(UP)

        line = Line(LEFT, RIGHT)
        line.match_width(title)
        line.next_to(title, DOWN)

        words = TexText("Harder than expected")
        words.set_color(RED)
        words.scale(1.5)
        words.next_to(line, DOWN, buff=LARGE_BUFF)

        self.play(
            FadeIn(title, shift=DOWN),
            Create(line),
            self.teacher.change, "raise_right_hand",
            self.change_students("pondering", "confused", "sassy")
        )
        self.wait()
        self.play(
            FadeIn(words, shift=UP),
            self.change_students(*3 * ["horrified"]),
        )
        self.wait(3)
