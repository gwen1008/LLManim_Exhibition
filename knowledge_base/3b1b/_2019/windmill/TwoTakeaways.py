# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示教師與學生場景中，標題與兩個要點項目以動畫方式呈現，並在兩個項目之間切換突出顯示的效果。



from manim import *
class TwoTakeaways(TeacherStudentsScene):
    def construct(self):
        title = TexText("Two takeaways")
        title.scale(2)
        title.to_edge(UP)

        line = Line()
        line.match_width(title)
        line.next_to(title, DOWN, buff=SMALL_BUFF)

        items = VGroup(
            TexText("1) Social"),
            TexText("2) Mathematical"),
        )
        items.scale(1.5)
        items.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        items.next_to(line, DOWN, buff=MED_LARGE_BUFF)

        self.play(
            Create(line),
            GrowFromPoint(title, self.hold_up_spot),
            self.teacher.animate.change("raise_right_hand"),
        )
        self.play_all_student_changes("pondering")
        self.wait()
        for item in items:
            self.play(FadeIn(item, shift=LEFT))
            item.big = item.copy()
            item.small = item.copy()
            item.big.scale(1.5, about_edge=LEFT)
            item.big.set_color(BLUE)
            item.small.scale(0.75, about_edge=LEFT)
            item.small.set_opacity(0.5)
        self.play(self.teacher.animate.change("happy"))
        self.wait()
        for i, j in [(0, 1), (1, 0)]:
            self.play(
                items[i].animate.become(items[i].big),
                items[j].animate.become(items[j].small),
            )
            self.wait()
