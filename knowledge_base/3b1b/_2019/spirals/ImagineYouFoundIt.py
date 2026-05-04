# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示一個學生在課堂上發現某個想法時，從猶豫到思考再到興奮的過程，並用對話框和表情變化來表現。



from manim import *
class ImagineYouFoundIt(TeacherStudentsScene):
    def construct(self):
        you = self.students[1]
        others = VGroup(
            self.students[0],
            self.students[2],
            self.teacher,
        )
        bubble = you.get_bubble(direction=LEFT)
        bubble[-1].set_fill(GREEN_SCREEN, 1)

        you_label = Text("You")
        arrow = Arrow(start=UP, end=DOWN)
        arrow.next_to(you, UP)
        you_label.next_to(arrow, UP)

        self.play(
            you.animate.change("hesitant", you_label),
            FadeIn(you_label, shift=DOWN),
            GrowArrow(arrow),
            others.animate.set_opacity(0.25),
        )
        self.play(Blink(you))
        self.play(
            FadeIn(bubble),
            FadeOut(you_label),
            FadeOut(arrow),
            you.animate.change("pondering"),
        )
        self.play(you.animate.look_at(bubble.get_corner(UR)))
        self.play(Blink(you))
        self.wait()
        self.play(you.animate.change("hooray"))
        self.play(Blink(you))
        self.wait()
        self.play(you.animate.change("sassy", bubble.get_top()))
        self.wait(6)
